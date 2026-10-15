"""Read-only feasibility audit; all generated observations live in a temporary root.

Run with the project v8 environment. This deliberately reports counterexamples;
it is not a production test suite or a new heldout acceptance run.
"""

from __future__ import annotations

import hashlib
import json
import random
import subprocess
import sys
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory

from upf_agent.v8.actions import full_actions
from upf_agent.v8.adapters import collect
from upf_agent.v8.compiler import compile_contract, compile_query_plan, slot
from upf_agent.v8.dependency import DependencyIndex, LocalEvaluator, semantic_results
from upf_agent.v8.evaluation import scaling_fixture
from upf_agent.v8.evaluator import full_evaluate
from upf_agent.v8.fixtures import example
from upf_agent.v8.models import EvidenceBinding, digest


PROJECT = Path(__file__).resolve().parents[2]


def prepared(root):
    task = example(root)
    contract = compile_contract(task)
    bindings = []
    for step in compile_query_plan(task, contract).steps:
        packet = collect(root, task, contract, step, step.step_id)
        bindings.extend(EvidenceBinding.model_validate(b) for b in packet["bindings"])
    return task, contract, bindings


def outcomes(actions):
    return {name: action.outcome for name, action in actions.items()}


def batch_probe(root):
    task, contract, bindings = prepared(root)
    local = LocalEvaluator(task, contract, bindings, "batch-0")
    receipt = local.update(deepcopy(bindings), "batch-1")
    states = full_evaluate(task, contract, bindings, "batch-1")
    actions = full_actions(task, contract, bindings, states, "batch-1")
    return {
        "changed_slots": receipt["changed_slots"],
        "state_batches": sorted({s.batch_id for s in local.states.values()}),
        "action_batches": sorted({a.batch_id for a in local.actions.values()}),
        "expected_batch": "batch-1",
        "historical_semantic_comparator_equal": semantic_results(local.states, local.actions)
        == semantic_results(states, actions),
        "batch_labels_consistent": all(a.batch_id == "batch-1" for a in local.actions.values()),
        "interpretation": "No-op update retains old action batch labels; no execution is authorized.",
    }


def time_probe(root):
    task, contract, bindings = prepared(root)
    runtime = next(b for b in bindings if b.category == "R" and b.object_id == "UPF-A")
    conflict = runtime.model_copy(deep=True)
    conflict.evidence_id += ":expiring-conflict"
    conflict.fields["n4_enabled"] = False
    conflict.valid = conflict.observed.model_copy(
        update={"end": task.as_of + timedelta(seconds=5)}
    )
    augmented = [*bindings, conflict]
    local = LocalEvaluator(task, contract, augmented, "before")
    later = task.as_of + timedelta(seconds=10)
    receipt = local.update(augmented, "after", later)
    states = full_evaluate(task, contract, augmented, "after", later)
    old_time_actions = full_actions(task, contract, augmented, states, "after")
    # Same deterministic rule functions; normalize gate time to the actual evaluation time.
    effective_task = task.model_copy(update={"as_of": later})
    same_time_actions = full_actions(effective_task, contract, augmented, states, "after")
    return {
        "task_as_of": task.as_of.isoformat(),
        "evaluation_as_of": later.isoformat(),
        "runtime_state_after": states[runtime.requirement_id].code.value,
        "mode": receipt["mode"],
        "local_outcomes": outcomes(local.actions),
        "full_gate_using_task_time": outcomes(old_time_actions),
        "full_gate_using_evaluation_time": outcomes(same_time_actions),
        "local_reasons": {name: a.reasons for name, a in local.actions.items()},
        "time_normalized_outcomes_equal": outcomes(local.actions) == outcomes(same_time_actions),
        "interpretation": "An expired conflicting observation stops blocking states, but the gate reselects at the old task time.",
    }


def initial_index_omission_probe(root):
    task, contract, bindings = prepared(root)
    runtime = next(b for b in bindings if b.category == "R" and b.object_id == "UPF-A")
    original_init = DependencyIndex.__init__
    removed = []

    def faulty_initial_producer(index, *args, **kwargs):
        original_init(index, *args, **kwargs)
        # Inject a construction fault: omit this reader group before self-certification.
        for field in [f"__record__:{runtime.requirement_id}", *runtime.fields]:
            source = slot(runtime.object_id, runtime.category, field)
            if source in index.graph:
                edges = list(index.graph.out_edges(source))
                removed.extend(edges)
                index.graph.remove_edges_from(edges)
        index.expected_edges = frozenset(index.graph.edges)

    DependencyIndex.__init__ = faulty_initial_producer
    try:
        local = LocalEvaluator(task, contract, bindings, "before")
    finally:
        DependencyIndex.__init__ = original_init
    changed = deepcopy(bindings)
    changed_runtime = next(b for b in changed if b.evidence_id == runtime.evidence_id)
    changed_runtime.fields["n4_enabled"] = False
    changed_runtime.revision += 1
    receipt = local.update(changed, "after")
    states = full_evaluate(task, contract, changed, "after")
    actions = full_actions(task, contract, changed, states, "after")
    return {
        "fault_injected": True,
        "fault_stage": "initial_index_production_before_expected_edges_sealing",
        "removed_edge_count": len(removed),
        "index_self_audit": local.index.audit(),
        "mode": receipt["mode"],
        "recomputed_states": receipt["recomputed_states"],
        "local_outcomes": outcomes(local.actions),
        "full_outcomes": outcomes(actions),
        "semantic_equal": semantic_results(local.states, local.actions)
        == semantic_results(states, actions),
        "interpretation": "Injected initial omission evades self-certified audit when readers are never scheduled; this is a fault-injection result, not evidence of a normal producer omission.",
    }


def graph_purpose_probe(root):
    task, contract, bindings = prepared(root)
    original = next(b for b in bindings if b.category == "K" and b.object_id == "UPF-A")
    # Project the fields that engine._graph currently sets for an accepted document node.
    graph_binding = EvidenceBinding(
        evidence_id=original.evidence_id + ":graph-projection",
        native_id="synthetic-document-node",
        task_id=task.run_id,
        contract_id=contract.contract_id,
        requirement_id=original.requirement_id,
        object_id=original.object_id,
        category="K",
        fields={"instruction": original.fields["instruction"]},
        source=original.source,
        product=task.product,
        version=task.version,
        receipt_id="synthetic-graph-receipt",
        source_verified=True,
        synthetic=True,
    )
    projected = [graph_binding if b.evidence_id == original.evidence_id else b for b in bindings]
    states = full_evaluate(task, contract, projected, "graph-purpose")
    state = states[original.requirement_id]
    return {
        "engine_field_projection_only": True,
        "full_graph_execution": False,
        "binding_purposes": graph_binding.purposes,
        "knowledge_state": state.code.value,
        "reasons": state.reasons,
        "basis": state.basis,
        "interpretation": "Current graph-created K bindings omit purpose; source/version correctness alone does not close the knowledge gap.",
    }


def small_differential(root):
    results = []
    for size in ["S", "M", "L"]:
        for updates in [1, 5]:
            for seed in [0, 1]:
                task, contract, bindings, actions, field_map = scaling_fixture(
                    root / f"{size}-{updates}-{seed}", size, seed
                )
                local = LocalEvaluator(task, contract, bindings, actions=actions)
                rng = random.Random(seed)
                for batch in range(4):
                    changed = deepcopy(bindings)
                    chosen = rng.sample(sorted(field_map), updates)
                    touched = set()
                    for field in chosen:
                        position = field_map[field]
                        changed[position].fields[field] = rng.randrange(0, 4)
                        touched.add(position)
                    for position in touched:
                        changed[position].revision += 1
                    batch_id = f"{size}-{updates}-{seed}-{batch}"
                    states = full_evaluate(task, contract, changed, batch_id)
                    decisions = full_actions(task, contract, changed, states, batch_id, actions)
                    receipt = local.update(changed, batch_id)
                    results.append({
                        "case": batch_id,
                        "semantic_equal": semantic_results(states, decisions)
                        == semantic_results(local.states, local.actions),
                        "mode": receipt["mode"],
                        "stale_action_batches": sum(a.batch_id != batch_id for a in local.actions.values()),
                    })
                    bindings = changed
    return {
        "matrix": "S/M/L x 1/5 fields x 2 seeds x 4 batches",
        "batches": len(results),
        "semantic_equal": sum(r["semantic_equal"] for r in results),
        "batches_with_stale_action_labels": sum(r["stale_action_batches"] > 0 for r in results),
        "results": results,
        "timing_claim": False,
    }


def main():
    import upf_agent

    code_files = sorted((PROJECT / "src/upf_agent").rglob("*.py"))
    hashes = {str(p.relative_to(PROJECT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in code_files}
    with TemporaryDirectory(prefix="upf-v8-feasibility-") as temporary:
        root = Path(temporary)
        result = {
            "audit_time_utc": datetime.now(UTC).isoformat(),
            "project": str(PROJECT),
            "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=PROJECT, text=True).strip(),
            "python": sys.version.split()[0],
            "import_path": upf_agent.__file__,
            "package_versions": {p: version(p) for p in ["pytest", "langgraph", "pydantic", "networkx", "neo4j"]},
            "source_manifest_sha256": digest(hashes),
            "source_sha256": hashes,
            "synthetic": True,
            "reviewed": False,
            "model_calls": 0,
            "network_agent_tool_calls": 0,
            "real_network_writes": 0,
            "probes": {
                "batch_identity": batch_probe(root / "batch"),
                "evaluation_time": time_probe(root / "time"),
                "initial_read_index_omission": initial_index_omission_probe(root / "index"),
                "graph_knowledge_purpose": graph_purpose_probe(root / "purpose"),
            },
            "small_differential": small_differential(root / "differential"),
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
