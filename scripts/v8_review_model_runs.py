"""Freeze corrected development cases and run the four methods on one pinned deployment."""

import argparse
import csv
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from time import perf_counter

from upf_agent.v8.experiment_manifest import source_manifest
from upf_agent.v8.phase1 import write_json
from upf_agent.v8.phase2 import METHODS, _blind_export, append_jsonl, run_method
from upf_agent.v8.plan_cases import prepare_case
from upf_agent.v8.plan_generator import ObservedPlanClient, generation_manifest
from upf_agent.v8.plan_metrics import summarize_cases
from upf_agent.v8.plan_review import validate_splits


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(project, output, deployment_file, selected, workers):
    if output.exists() or workers not in range(1, 9):
        raise ValueError("choose a fresh output and 1–8 workers")
    if (
        not selected
        or len(set(selected)) != len(selected)
        or not all(1 <= i <= 24 for i in selected)
    ):
        raise ValueError("unique case IDs from 1–24 required")
    project, output = project.resolve(), output.resolve()
    deployment = json.loads(deployment_file.read_text())
    source = source_manifest(project)
    output.mkdir(parents=True)
    write_json(output / "source_manifest.json", source)
    write_json(output / "common-head.json", generation_manifest())
    write_json(output / "deployment.json", deployment)
    write_json(
        output / "protocol.json",
        {
            "experiment": "review-remediation-phase2-2",
            "cases": len(selected),
            "selected_case_ids": selected,
            "methods": METHODS,
            "workers": workers,
            "synthetic": True,
            "reviewed": False,
            "heldout_consumed": False,
            "cases_frozen_before_outputs": True,
            "max_model_requests": 8,
            "max_tool_dispatches": 8,
            "max_rounds": 3,
            "timeout_seconds": 180,
            "temperature": 0,
            "seed": None,
            "head_max_tokens": 3072,
            "deployment_sha256": sha(deployment_file),
            "driver_sha256": sha(Path(__file__)),
            "same_deployment_all_methods": True,
            "latency_superiority_claim": False,
            "comparison_to_old": (
                "revised task, head, Validator and deployment; not a paired causal test"
            ),
        },
    )
    prepared = [prepare_case(output / "cases" / f"pilot-{i:02d}", i - 1) for i in selected]
    validate_splits([g for _, g in prepared])
    input_hashes = {
        str(p.relative_to(output)): sha(p)
        for p in sorted((output / "cases").rglob("*"))
        if p.is_file()
    }
    write_json(output / "input-hashes.json", input_hashes)

    class PinnedClient(ObservedPlanClient):
        def __init__(self, model, *args, **kwargs):
            model = model.model_copy(
                update={
                    "endpoint": deployment["endpoint"],
                    "max_num_seqs": 8,
                    "gpu_memory_utilization": 0.82,
                }
            )
            super().__init__(model, *args, **kwargs)

    def execute(task, gold, method):
        folder = output / "runs" / gold.case_id / f"method-{METHODS.index(method) + 1}"
        folder.mkdir(parents=True)
        return run_method(
            project,
            output / "cases" / gold.case_id,
            folder,
            task,
            gold,
            method,
            client_factory=PinnedClient,
        )

    rows, started = [], perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(execute, t, g, m): (g.case_id, m) for t, g in prepared for m in METHODS
        }
        for future in as_completed(futures):
            case, method = futures[future]
            # Unexpected runner failures abort visibly; already written originals remain.
            row = future.result()
            rows.append(row)
            append_jsonl(output / "metrics-by-case.jsonl", row)
            write_json(
                output / "progress.json",
                {
                    "completed": len(rows),
                    "expected": len(prepared) * 4,
                    "elapsed_seconds": perf_counter() - started,
                },
            )
            print(
                json.dumps(
                    {
                        "case": case,
                        "method": method,
                        "validator_pass": row["validator_pass"],
                        "reference_pass": row["reference_pass"],
                        "failure": row["method_failure"] or row["generation_error"],
                    }
                ),
                flush=True,
            )
    rows.sort(key=lambda r: (r["case_id"], METHODS.index(r["method"])))
    _blind_export(output, rows)
    flat = [{k: v for k, v in r.items() if k not in {"branch", "issues"}} for r in rows]
    with (output / "metrics-by-case.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(flat[0]))
        writer.writeheader()
        writer.writerows(flat)
    write_json(output / "failures.json", [r for r in rows if not r["reference_pass"]])
    result = {
        "cases": len(prepared),
        "method_runs": len(rows),
        "source": source,
        "source_unchanged": source_manifest(project) == source,
        "input_hashes_unchanged": all(sha(output / n) == h for n, h in input_hashes.items()),
        "summaries": {m: summarize_cases([r for r in rows if r["method"] == m]) for m in METHODS},
        "elapsed_seconds": perf_counter() - started,
        "formal_acceptance": False,
        "development_pass": all(
            r["validator_pass"] and r["reference_pass"] and r["elapsed_seconds"] <= 180
            for r in rows
        ),
    }
    write_json(output / "summary.json", result)
    write_json(
        output / "sha256_manifest.json",
        {
            str(p.relative_to(output)): sha(p)
            for p in sorted(output.rglob("*"))
            if p.is_file() and p.name != "sha256_manifest.json"
        },
    )
    assert result["source_unchanged"] and result["input_hashes_unchanged"]
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--deployment", type=Path, required=True)
    parser.add_argument("--case-ids", type=int, nargs="+", default=list(range(1, 25)))
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    result = run(
        Path(__file__).resolve().parents[1],
        args.output,
        args.deployment,
        args.case_ids,
        args.workers,
    )
    print({k: v for k, v in result.items() if k not in {"source", "summaries"}})
