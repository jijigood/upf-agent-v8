"""Read-only source, path, gate and raw-model replay for third-stage matrices."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.e2 import METHODS as GRAPH_METHODS
from upf_agent.v8.e2 import score_hits
from upf_agent.v8.e5_full import decision
from upf_agent.v8.e6 import aggregate
from upf_agent.v8.experiment_metrics import summarize_events
from upf_agent.v8.graph import GraphEdge, GraphNode, MemoryGraphStore, exclusion
from upf_agent.v8.graph_query_compiler import RequirementGraphQuery, compile_requirement_query
from upf_agent.v8.models import (
    EvaluationContext,
    EvidenceBinding,
    EvidenceContract,
    OrchestrationTask,
    Requirement,
    digest,
)
from upf_agent.v8.phase1 import write_json
from upf_agent.v8.plan_ir import CaseGold
from upf_agent.v8.plan_metrics import score_case
from upf_agent.v8.plan_source_verifier import verify_plan_source
from upf_agent.v8.plan_translator import translate_plan
from upf_agent.v8.plan_validator import validate_plan


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pinned(root, filename):
    hashes = read(root / filename)
    assert all(sha(root / name) == value for name, value in hashes.items()), "frozen input changed"
    return len(hashes)


def seed_cache_paths(cache_pins, seed_cache_root=None):
    """Relocate the original cache without rewriting frozen provenance or hashes."""
    names = [Path(name).name for name in cache_pins]
    if len(set(names)) != len(names):
        raise ValueError("ambiguous original seed-cache basenames")
    paths = {}
    for name, expected in cache_pins.items():
        path = Path(name) if seed_cache_root is None else seed_cache_root / Path(name).name
        if seed_cache_root is not None and (
            path.is_symlink() or not path.resolve().is_relative_to(seed_cache_root.resolve())
        ):
            raise ValueError("seed cache escaped relocated root")
        if sha(path) != expected:
            raise ValueError(f"original seed-cache hash mismatch: {Path(name).name}")
        paths[Path(name).name] = path
    return paths


def review_e2(root, seed_cache_root=None):
    input_count = pinned(root, "input-hashes.json")
    cache_pins = (
        read(root / "reused-seed-cache-hashes.json")
        if (root / "reused-seed-cache-hashes.json").exists()
        else {}
    )
    cache_paths = seed_cache_paths(cache_pins, seed_cache_root)
    recomputed = []
    hit_count = writeback_count = paths = 0
    for number in range(1, 97):
        folder = root / "queries" / f"query-{number:03d}"
        raw = read(folder / "query-reference.json")
        case = {
            **raw,
            "task": OrchestrationTask.model_validate(raw["task"]),
            "contract": EvidenceContract.model_validate(raw["contract"]),
            "requirement": Requirement.model_validate(raw["requirement"]),
        }
        assert compile_contract(case["task"]) == case["contract"]
        snapshot = read(folder / "graph.json")
        store = MemoryGraphStore()
        store.build(
            [GraphNode.model_validate(n) for n in snapshot["nodes"]],
            [GraphEdge.model_validate(e) for e in snapshot["edges"]],
        )
        cached = read(root / "seed-cache" / f"query-{number:03d}.json")
        assert cached["query"] == case["text"]
        if cache_pins:
            assert sha(root / "seed-cache" / f"query-{number:03d}.json") == sha(
                cache_paths[f"query-{number:03d}.json"]
            )
        seeds = [] if case["mode"] == "missing-seed" else cached["rankings"]["reranked"][:20]
        pool = cached["rankings"]["reranked"][:40]
        query = compile_requirement_query(
            case["task"], case["contract"], case["requirement"], seeds, reseed_ids=pool, top_k=20
        )
        for method in GRAPH_METHODS:
            result = read(root / "results" / f"query-{number:03d}" / f"{method}.json")
            assert result["primary_seeds"] == seeds and result["reseed_pool"] == pool
            assert (
                result["scan"]["nodes_scanned"] <= 100
                and result["scan"]["adjacency_entries_scanned"] <= 200
            )
            if "query" in result:
                assert RequirementGraphQuery.model_validate(result["query"]) == query
            for hit in result["hits"]:
                binding = EvidenceBinding.model_validate(hit["binding"])
                assert (
                    binding.task_id == case["task"].run_id
                    and binding.contract_id == case["contract"].contract_id
                )
                assert binding.requirement_id == case["requirement"].requirement_id
                assert verify_plan_source(root / "corpus", binding, case["task"])
                path = hit["path"]
                assert path["nodes"][-1] == hit["node_id"]
                assert path["hops"] == len(path["edges"]) <= 2
                assert path["nodes"][0] in (
                    pool if path["seed_origin"] == "cached-reseed" else seeds
                )
                for node_id in path["nodes"]:
                    node = store.nodes[node_id]
                    assert not exclusion(node, query.graph)
                    assert sha(root / "corpus" / node.source.relative_path) == node.source.sha256
                for a, b, edge_id in zip(
                    path["nodes"], path["nodes"][1:], path["edges"], strict=False
                ):
                    edge = store.edges[edge_id]
                    assert {a, b} == {edge.source_id, edge.target_id}
                    assert edge.relation in query.graph.relations and edge.corroborated
                    assert sha(root / "corpus" / edge.source.relative_path) == edge.source.sha256
                hit_count += 1
                paths += 1
            for binding in result.get("writeback_bindings", []):
                assert verify_plan_source(
                    root / "corpus", EvidenceBinding.model_validate(binding), case["task"]
                )
                writeback_count += 1
            if "writeback_count" in result:
                assert result["writeback_count"] == len(result["writeback_bindings"])
            for k in [5, 10, 20]:
                recomputed.append(
                    {
                        **score_hits(case, result, k),
                        "method": method,
                        "scan": result["scan"],
                        "total_retrieval_seconds": result["total_retrieval_seconds"],
                        "pilot": number <= 24,
                    }
                )
    assert recomputed == read(root / "observations.json")
    summary = read(root / "summary.json")
    assert (
        summary["engineering_pass"]
        and summary["input_hashes_unchanged"]
        and summary["source_unchanged"]
    )
    return {
        "queries": 96,
        "retrievals": 480,
        "top_k_observations": 1440,
        "source_checked_hits": hit_count,
        "checked_paths": paths,
        "checked_writeback_bindings": writeback_count,
        "pinned_inputs": input_count,
        "formal_acceptance": False,
        "pass": True,
    }


def review_e5(root):
    input_count = pinned(root, "input-hashes.json")
    counts = Counter()
    source_refs = 0
    for folder in sorted((root / "cases").iterdir()):
        raw = read(folder / "input.json")
        reference = read(folder / "reference.json")
        task = OrchestrationTask.model_validate(raw["task"])
        contract = EvidenceContract.model_validate(raw["contract"])
        context = EvaluationContext.model_validate(raw["context"])
        bindings = [EvidenceBinding.model_validate(b) for b in raw["bindings"]]
        plan = translate_plan((folder / "candidate.txt").read_text()).plan
        for layer in range(5):
            trace = []
            report = validate_plan(
                plan, bindings, task, contract, context, folder, max_stage=layer, stage_trace=trace
            )
            assert report.model_dump(mode="json") == read(folder / f"A{layer}-validation.json")
            assert trace == read(folder / f"A{layer}-trace.json")
            row = read(folder / f"A{layer}-result.json")
            assert row["outcome"] == decision(report, layer)
            assert row["correct"] == (row["outcome"] == reference["expected_outcome"])
            assert not row["execute_authorized"] and not report.execute_authorized
            assert all(t["stage"] <= layer for t in trace)
            counts[f"A{layer}:{reference['category']}:{row['outcome']}"] += 1
            source_refs += sum(t["component"] == "source_reference" for t in trace)
    assert counts["A4:allowed:suggest_allowed"] == 40
    assert counts["A4:forbidden:blocked"] == 40
    assert counts["A4:unknown:human_review"] == 40
    return {
        "candidates": 120,
        "actual_gate_runs": 600,
        "reject_all_decisions": 120,
        "pinned_inputs": input_count,
        "source_reference_checks": source_refs,
        "counts": counts,
        "formal_acceptance": False,
        "pass": True,
    }


def normalized_structure(plan):
    if plan is None:
        return None
    labels = {
        s.step_id: digest(
            [
                s.action_type,
                s.target,
                s.parameters,
                [(c.predicate, c.field, c.expected) for c in s.preconditions],
                s.on_unknown,
                s.permission_kind,
                s.effect_kind,
                s.claimed_executed,
            ]
        )
        for s in plan.steps
    }
    return digest(
        [
            sorted(labels.values()),
            sorted(
                (labels.get(d, "unknown"), labels[s.step_id])
                for s in plan.steps
                for d in s.depends_on
            ),
        ]
    )


def normalized_native(native):
    # Source hashes/IDs change after perturbation; retain the actual field facts and rule status.
    facts = sorted(
        {
            digest(
                [
                    b["category"],
                    b["object_id"],
                    b["fields"],
                    b["product"],
                    b["version"],
                    b["config_version"],
                    b["observed"],
                    b["valid"],
                ]
            )
            for b in native["bindings"]
        }
    )
    states = {
        rid: [state["code"], state["valid"], state["reasons"]]
        for rid, state in native["states"].items()
    }
    return digest(facts), digest(states)


def review_e6(root):
    input_count = pinned(root, "input-hashes.json")
    protocol = read(root / "protocol.json")
    all_rows = [json.loads(line) for line in (root / "run-index.jsonl").read_text().splitlines()]
    assert len(all_rows) == 540
    counts = Counter()
    models = 0
    failures = []
    hash_changes = Counter()
    normalized = []
    proof_count = 0
    structural_runs = {}
    native_runs = {}
    elapsed_budget_violations = []
    for proof in (root / "cases").rglob("perturbation-proof.json"):
        p = read(proof)
        assert p["facts_equal"] and p["before_facts_sha256"] == p["after_facts_sha256"]
        assert not p["human_semantic_reviewed"]
        proof_count += 1
    assert proof_count == 80
    for row in all_rows:
        key = (row["case_id"], row["condition"], row["replicate"], row["method"])
        assert counts[key] == 0
        counts[key] += 1
        folder = root / row["output"]
        sampling = read(folder / "sampling.json")
        expected_seed = protocol["seeds"][row["replicate"] - 1]
        assert (
            sampling["seed"] == expected_seed and sampling["temperature"] == protocol["temperature"]
        )
        if "fatal_error" in row:
            failures.append(row)
            normalized.append(
                {
                    **row,
                    "reference_pass": False,
                    "validator_pass": False,
                    "published_validator_pass": False,
                    "vpr": None,
                    "parsed": False,
                    "unscorable": True,
                    "hard_constraint_violation": False,
                    "retained_steps": 0,
                    "rejected_steps": 0,
                    "rewritten_steps": 0,
                    "reviewed": False,
                    "solvability": "unscorable",
                }
            )
            continue
        task = OrchestrationTask.model_validate(read(folder / "task.json"))
        context = EvaluationContext.model_validate(read(folder / "context.json"))
        bindings = [EvidenceBinding.model_validate(b) for b in read(folder / "bindings.json")]
        translation = translate_plan((folder / "raw-plan.txt").read_text())
        assert translation.model_dump(mode="json") == read(folder / "translation.json")
        validation = validate_plan(
            translation.plan, bindings, task, compile_contract(task), context, folder / "runtime"
        )
        assert validation.model_dump(mode="json") == read(folder / "validation.json")
        condition = "base" if row["condition"] == "repeat" else row["condition"]
        gold = CaseGold.model_validate(
            read(root / "cases" / row["case_id"] / condition / "case-reference.json")
        )
        assert not gold.reviewed and row["vpr"] is None
        metrics = score_case(translation.plan, validation, gold)
        if row["method_failure"] or row["generation_error"] or row["finish_reason"] == "length":
            metrics["reference_pass"] = False
        assert all(row[name] == value for name, value in metrics.items())
        if row["elapsed_seconds"] > protocol["common_limits"]["seconds"]:
            elapsed_budget_violations.append(key)
        events = [json.loads(line) for line in (folder / "traces.jsonl").read_text().splitlines()]
        actual = summarize_events(events)
        assert actual == read(folder / "metrics.json")
        traces = [
            json.loads(line) for line in (folder / "model-traces.jsonl").read_text().splitlines()
        ]
        assert actual["invocations"]["model"]["attempted"] == len(traces)
        for trace in traces:
            assert (
                trace["request"]["seed"] == expected_seed
                and trace["request"]["temperature"] == protocol["temperature"]
            )
            if trace["response"] and "choices" in trace["response"]:
                assert trace["response"]["model"] == trace["request"]["model"]
        assert (
            actual["invocations"]["model"]["attempted"] <= 8
            and actual["invocations"]["tool"]["attempted"] <= 8
        )
        models += len(traces)
        if row["method_failure"] or row["generation_error"] or row["finish_reason"] == "length":
            failures.append(row)
        if translation.plan:
            assert all(
                not s.claimed_executed and s.non_executable and s.effect_kind != "network_write"
                for s in translation.plan.steps
            )
        hash_changes[row["method"]] += bool(row["reference_pass"])
        structural_runs[(row["method"], row["case_id"], row["condition"], row["replicate"])] = (
            normalized_structure(translation.plan)
        )
        native_path = folder / "v8-native.json"
        if native_path.exists():
            native_runs[(row["method"], row["case_id"], row["condition"], row["replicate"])] = (
                normalized_native(read(native_path))
            )
        normalized.append(row)
    groups = aggregate(normalized)
    for group in groups.values():
        assert (
            group["repeated"]["runs"] == 100
            and group["perturbed"]["runs"] == 80
            and group["all_five_denominator"] == 20
        )
    raw = read(root / "summary.json")
    assert raw["source_unchanged"] and raw["input_hashes_unchanged"]
    if not raw["fatal_errors"]:
        assert groups == raw["groups"]
    diagnostics = {}
    for method in groups:
        cases = sorted({row["case_id"] for row in all_rows if row["method"] == method})
        repeated_variation = []
        native_repeat_variation = []
        native_perturbation_flips = []
        for case_id in cases:
            shapes = {structural_runs.get((method, case_id, "repeat", n)) for n in range(1, 6)}
            repeated_variation.append(
                {"case_id": case_id, "normalized_structure_count": len(shapes)}
            )
            if method.startswith("v8"):
                values = {native_runs.get((method, case_id, "repeat", n)) for n in range(1, 6)}
                native_repeat_variation.append(
                    {"case_id": case_id, "normalized_native_count": len(values)}
                )
                base = native_runs.get((method, case_id, "repeat", 1))
                for condition in protocol["perturbations"]:
                    value = native_runs.get((method, case_id, condition, 1))
                    native_perturbation_flips.append(
                        {
                            "case_id": case_id,
                            "perturbation": condition,
                            "evidence_field_flip": value is None
                            or base is None
                            or value[0] != base[0],
                            "state_flip": value is None or base is None or value[1] != base[1],
                        }
                    )
        diagnostics[method] = {
            "repeated_structure": repeated_variation,
            "native_repeat": native_repeat_variation,
            "native_perturbation": native_perturbation_flips,
            "note": "structure diagnostic omits natural text and bookkeeping IDs; "
            "it is not full semantic equivalence or proof of seed reproducibility",
        }
    return {
        "runs": 540,
        "repeats": 300,
        "perturbations": 240,
        "mechanical_perturbation_proofs": 80,
        "actual_model_calls": models,
        "determinism_diagnostics": diagnostics,
        "pinned_inputs": input_count,
        "failures": failures,
        "elapsed_budget_violations": elapsed_budget_violations,
        "groups": groups,
        "formal_acceptance": False,
        "reference_vpr": None,
        "reference_vpr_denominator": 0,
        "pass": not elapsed_budget_violations,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", choices=["E2", "E5", "E6"], required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed-cache-root", type=Path, help="relocated original E2 cache")
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("new read-only audit ID required")
    if args.experiment == "E2":
        result = review_e2(args.root, args.seed_cache_root)
    else:
        if args.seed_cache_root is not None:
            parser.error("--seed-cache-root applies only to E2")
        result = {"E5": review_e5, "E6": review_e6}[args.experiment](args.root)
    write_json(args.output, result)
    print(
        {
            k: v
            for k, v in result.items()
            if k not in {"groups", "failures", "counts", "determinism_diagnostics"}
        }
    )
