"""Mixed 24-query pilot, PPR sensitivity, and real-manual Ledger admission probes."""

import argparse
import copy
import json
import shutil
from pathlib import Path
from time import perf_counter

from upf_agent.v8.actions import full_actions
from upf_agent.v8.dependency import LocalEvaluator, complete_results
from upf_agent.v8.e2 import METHODS, fixed_hop, score_hits
from upf_agent.v8.evaluator import full_evaluate, route_gaps
from upf_agent.v8.experiment_manifest import source_manifest
from upf_agent.v8.graph import GraphEdge, GraphNode, MemoryGraphStore
from upf_agent.v8.graph_query_compiler import compile_requirement_query
from upf_agent.v8.knowledge_applicability import KnowledgeRegistry
from upf_agent.v8.models import (
    EvidenceContract,
    OrchestrationData,
    OrchestrationTask,
    Requirement,
    digest,
)
from upf_agent.v8.phase1 import write_json
from upf_agent.v8.plan_source_verifier import verify_plan_source
from upf_agent.v8.requirement_graph import execute_requirement_query, knowledge_writeback
from upf_agent.v8.store import Ledger

SELECTED = (
    1,
    2,
    3,
    4,
    5,
    6,
    25,
    27,
    31,
    37,
    43,
    44,
    49,
    50,
    61,
    64,
    67,
    70,
    73,
    74,
    85,
    88,
    91,
    94,
)


def load_case(batch, number):
    folder = batch / "queries" / f"query-{number:03d}"
    raw = json.loads((folder / "query-reference.json").read_text())
    case = {
        **raw,
        "task": OrchestrationTask.model_validate(raw["task"]),
        "contract": EvidenceContract.model_validate(raw["contract"]),
        "requirement": Requirement.model_validate(raw["requirement"]),
    }
    snapshot = json.loads((folder / "graph.json").read_text())
    store = MemoryGraphStore()
    store.build(
        [GraphNode.model_validate(n) for n in snapshot["nodes"]],
        [GraphEdge.model_validate(e) for e in snapshot["edges"]],
    )
    registry = KnowledgeRegistry.model_validate_json((folder / "registry.json").read_text())
    cached = json.loads((batch / "seed-cache" / f"query-{number:03d}.json").read_text())
    seeds = [] if case["mode"] == "missing-seed" else cached["rankings"]["reranked"][:20]
    pool = cached["rankings"]["reranked"][:40]
    return case, store, registry, seeds, pool


def run(batch, output, project):
    if output.exists():
        raise ValueError("new supplement ID required")
    output.mkdir(parents=True)
    source = source_manifest(project)
    write_json(
        output / "protocol.json",
        {
            "queries": SELECTED,
            "kinds": {"K": 12, "R": 6, "P": 6},
            "pilot_retrievals": 120,
            "additional_PPR_retrievals": 48,
            "alphas": [0.7, 0.85, 0.95],
            "independent_new_queries": 0,
            "development_selection_after_initial_full_batch": True,
            "shared_frozen_inputs": str(batch),
            "reviewed": False,
            "formal_acceptance": False,
            "source": source,
        },
    )
    rows = []
    for number in SELECTED:
        case, store, registry, seeds, pool = load_case(batch, number)
        query = compile_requirement_query(
            case["task"], case["contract"], case["requirement"], seeds, reseed_ids=pool, top_k=20
        )
        for method in METHODS:
            started = perf_counter()
            if method in METHODS[:2]:
                result = fixed_hop(
                    batch / "corpus", store, query, registry, only_seeds=method == METHODS[0]
                )
            else:
                result = execute_requirement_query(
                    batch / "corpus",
                    store,
                    query,
                    registry=registry,
                    strategy={METHODS[2]: "bfs", METHODS[3]: "ppr", METHODS[4]: "bfs-reseed"}[
                        method
                    ],
                )
            result["elapsed_seconds"] = perf_counter() - started
            write_json(output / "pilot" / f"query-{number:03d}" / f"{method}.json", result)
            rows.append(
                {
                    **score_hits(case, result, 20),
                    "method": method,
                    "alpha": 0.85 if method == METHODS[3] else None,
                    "scope": "mixed-pilot",
                    "scan": result["scan"],
                }
            )
        for alpha in [0.7, 0.95]:
            query = compile_requirement_query(
                case["task"],
                case["contract"],
                case["requirement"],
                seeds,
                reseed_ids=pool,
                top_k=20,
                alpha=alpha,
            )
            result = execute_requirement_query(
                batch / "corpus", store, query, registry=registry, strategy="ppr"
            )
            write_json(
                output / "sensitivity" / f"query-{number:03d}" / f"alpha-{alpha}.json", result
            )
            rows.append(
                {
                    **score_hits(case, result, 20),
                    "method": METHODS[3],
                    "alpha": alpha,
                    "scope": "sensitivity",
                    "converged": result["ranking"]["converged"],
                    "iterations": result["ranking"]["iterations"],
                    "scan": result["scan"],
                }
            )
    case, store, registry, seeds, pool = load_case(batch, 1)
    query = compile_requirement_query(
        case["task"], case["contract"], case["requirement"], seeds, reseed_ids=pool, top_k=20
    )
    probes = []
    for strategy in ["bfs", "ppr", "bfs-reseed", "tampered-source", "multi-block-conflict"]:
        root = output / "ledger-probes" / strategy
        shutil.copytree(batch / "corpus", root, symlinks=True)
        write_json(root / "data/v8/knowledge_applicability.json", registry.model_dump(mode="json"))
        result = execute_requirement_query(
            root,
            store,
            query,
            registry=registry,
            strategy="bfs" if strategy in {"tampered-source", "multi-block-conflict"} else strategy,
        )
        if strategy == "tampered-source":
            path = root / result["hits"][0]["binding"]["source"]["relative_path"]
            path.write_bytes(path.read_bytes() + b"\nE2 explicit negative source mutation\n")
        ledger = Ledger(root)
        try:
            task = case["task"]
            ledger.create(task)
            request = {
                "query_sha256": digest(query),
                "source_experiment": str(batch),
                "strategy": strategy,
            }
            key = digest(request)
            ledger.charge(task, key, "tool", request)
            started = perf_counter()
            accepted, rejected = knowledge_writeback(
                root, query, copy.deepcopy(result), key, store=store, registry=registry
            )
            all_candidates = accepted
            # A single-block probe tests admission. Distinct instructions are not merged
            # into an invented instruction; their multi-value conflict is retained separately.
            if strategy != "multi-block-conflict":
                accepted = accepted[:1]
            assert all(verify_plan_source(root, b, task) for b in accepted)
            ledger.commit_receipt(
                task,
                key,
                {"bindings": [b.model_dump(mode="json") for b in accepted], "rejected": rejected},
                accepted,
                perf_counter() - started,
            )
            bindings = ledger.evidence(task.run_id)
            batch_id = digest([strategy, bindings])[:24]
            states = full_evaluate(task, case["contract"], bindings, batch_id)
            actions = full_actions(task, case["contract"], bindings, states, batch_id)
            local = LocalEvaluator(task, case["contract"], bindings, batch_id)
            assert complete_results(states, actions) == complete_results(
                local.states, local.actions
            )
            expected = strategy not in {"tampered-source", "multi-block-conflict"}
            assert states[case["requirement"].requirement_id].valid == expected
            ledger.save(
                OrchestrationData(
                    task=task,
                    contract=case["contract"],
                    bindings=bindings,
                    batch_id=batch_id,
                    states=states,
                    actions=list(actions.values()),
                    gaps=route_gaps(case["contract"], states),
                )
            )
            probe = {
                "strategy": strategy,
                "accepted_bindings": len(accepted),
                "applicable_retrieval_candidates": len(all_candidates),
                "admission_policy": "all-candidates conflict control"
                if strategy == "multi-block-conflict"
                else "one applicable block admission probe",
                "primary_K_state": states[case["requirement"].requirement_id].code.value,
                "rejected_bindings": len(rejected),
                "actual_Ledger_tool_attempts": ledger.metrics(task.run_id)["invocations"]["tool"][
                    "attempted"
                ],
                "primary_K_closed": states[case["requirement"].requirement_id].valid,
                "full_local_equal": True,
                "execute_authorized": False,
            }
            write_json(root / "probe.json", probe)
            write_json(root / "query.json", query.model_dump(mode="json"))
            probes.append(probe)
        finally:
            ledger.close()
    passed = all(
        r["invalid_acceptance_count"] == 0
        and r["scan"]["nodes_scanned"] <= 100
        and r["scan"]["adjacency_entries_scanned"] <= 200
        for r in rows
    )
    summary = {
        "pilot_retrievals": 120,
        "sensitivity_retrievals": 48,
        "ledger_probes": probes,
        "source": source,
        "source_unchanged": source_manifest(project) == source,
        "pass": passed,
        "formal_acceptance": False,
        "new_P3_calls": 0,
    }
    write_json(output / "observations.json", rows)
    write_json(output / "summary.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.batch, args.output, Path(__file__).resolve().parents[1])
    print({k: v for k, v in result.items() if k not in {"source", "ledger_probes"}})
