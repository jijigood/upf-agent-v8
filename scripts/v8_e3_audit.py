"""Read-only E3 artifact/source/cost replay; never call a model or import human reviews."""

import argparse
import hashlib
import json
import sqlite3
from collections import Counter
from pathlib import Path

from upf_agent.contracts import TimeWindow
from upf_agent.v8.actions import full_actions
from upf_agent.v8.dependency import complete_results
from upf_agent.v8.e3 import METHODS
from upf_agent.v8.e4 import write_json
from upf_agent.v8.evaluator import full_evaluate
from upf_agent.v8.models import (
    EvidenceBinding,
    EvidenceContract,
    OrchestrationData,
    OrchestrationTask,
    canonical,
)


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_protocol_public(root):
    return json.loads((root / "protocol.json").read_text()).get("shared_public_tool_units", False)


def audit(root, output):
    if output.exists():
        raise ValueError("audit output exists; choose a new ID")
    summary = json.loads((root / "summary.json").read_text())
    hashes = json.loads((root / "pre-evaluation-input-hashes.json").read_text())
    assert all(file_sha(root / name) == value for name, value in hashes.items())
    refs = {r["case_id"]: r for r in json.loads((root / "references.json").read_text())}
    counts, sources, batches, traces = Counter(), 0, 0, 0
    copied_inputs = 0
    integrity_errors, actual_attempts = [], Counter()
    costs = {method: Counter() for method in METHODS}
    rows = []
    for result_path in sorted((root / "runs").glob("*/*/result.json")):
        folder = result_path.parent
        result = json.loads(result_path.read_text())
        reference = refs[result["case_id"]]
        input_prefix = f"inputs/case-{result['case_id'].rsplit('-', 1)[-1]}/"
        for name, value in hashes.items():
            if name.startswith(input_prefix):
                assert file_sha(folder / name[len(input_prefix) :]) == value
                copied_inputs += 1
        task = OrchestrationTask.model_validate_json((folder / "task.json").read_text())
        contract = EvidenceContract.model_validate_json((folder / "contract.json").read_text())
        catalog = json.loads((folder / "publication-catalog.json").read_text())
        with sqlite3.connect(f"file:{folder / 'data/v8/ledger.sqlite3'}?mode=ro", uri=True) as db:
            input_task, input_contract = task, contract
            actual_task = OrchestrationTask.model_validate_json(
                db.execute("SELECT task FROM runs WHERE run_id=?", (task.run_id,)).fetchone()[0]
            )
            # Production Engine pins a runtime execution fingerprint before compiling.
            assert actual_task.model_dump(
                exclude={"execution_fingerprint"}
            ) == input_task.model_dump(exclude={"execution_fingerprint"})
            from upf_agent.v8.compiler import compile_contract

            task = actual_task
            contract = compile_contract(task)
            assert contract.model_dump(
                exclude={"contract_id", "task_fingerprint"}
            ) == input_contract.model_dump(exclude={"contract_id", "task_fingerprint"})
            versions = [
                EvidenceBinding.model_validate_json(r[0])
                for r in db.execute("SELECT payload FROM evidence WHERE run_id=?", (task.run_id,))
            ]
            for binding in versions:
                path = folder / binding.source.relative_path
                assert file_sha(path) == binding.source.sha256
                body = json.loads(path.read_text())
                record = body["observations"][int(binding.source.locator.rsplit("/", 1)[-1])]
                assert binding.source.source_id == body["source_id"]
                assert (
                    binding.category == record["category"]
                    and binding.object_id == record["object_id"]
                )
                assert set(binding.fields) <= set(task.permission.readable_fields)
                assert all(record["fields"].get(k) == v for k, v in binding.fields.items())
                assert binding.version == record.get("version")
                assert binding.config_version == record.get("config_version")
                expected_window = (
                    TimeWindow.model_validate_json(canonical(record["observed"]))
                    if record.get("observed")
                    else None
                )
                assert binding.observed == expected_window
                assert binding.revision == body["publication"]["edition"]
                receipt = db.execute(
                    "SELECT request FROM receipts WHERE run_id=? AND key=?",
                    (task.run_id, binding.receipt_id),
                ).fetchone()
                assert receipt is not None
                publication = json.loads(receipt[0])["publication"]
                assert (
                    publication["available"] and publication["file"] == binding.source.relative_path
                )
                assert publication == catalog[publication["round"]]
                sources += 1
            data = OrchestrationData.model_validate_json(
                db.execute("SELECT data FROM runs WHERE run_id=?", (task.run_id,)).fetchone()[0]
            )
            states = full_evaluate(task, contract, data.bindings, data.batch_id)
            actions = full_actions(task, contract, data.bindings, states, data.batch_id)
            assert complete_results(states, actions) == complete_results(
                data.states, {a.action_id: a for a in data.actions}
            )
            closed = states[reference["primary_requirement"]].valid
            assert result["primary_closed"] == closed
            assert result["all_closed"] == all(s.valid for s in states.values())
            assert result["false_closure"] == (closed and not reference["solvable"])
            receipts = list(
                db.execute("SELECT kind,status FROM receipts WHERE run_id=?", (task.run_id,))
            )
            tool_attempts = sum(kind == "tool" for kind, status in receipts)
            pending = sum(kind == "tool" and status != "committed" for kind, status in receipts)
            actual_attempts[result["method"]] += tool_attempts
            if pending or tool_attempts != result["tool_calls"]:
                integrity_errors.append(
                    {
                        "case_id": result["case_id"],
                        "method": result["method"],
                        "pending_receipts": pending,
                        "actual_attempts": tool_attempts,
                        "reported_attempts": result["tool_calls"],
                    }
                )
            assert (
                sum(kind == "tool" and status == "committed" for kind, status in receipts)
                == result["tool_calls"]
            )
            batches += db.execute(
                "SELECT count(*) FROM batches WHERE run_id=?", (task.run_id,)
            ).fetchone()[0]
        method = result["method"]
        counts[method] += 1
        for name in ("tool_calls", "model_calls", "redundant_queries", "new_valid_fields"):
            costs[method][name] += result[name]
        if method == METHODS[2]:
            events_file = folder / "dispatch-events.jsonl"
            events = (
                [json.loads(line) for line in events_file.read_text().splitlines()]
                if events_file.exists()
                else []
            )
            assert (
                sum(e["kind"] == "model" and e["status"] == "attempted" for e in events)
                == result["model_calls"]
            )
            trace_path = folder / "model-traces.jsonl"
            model_traces = (
                [json.loads(line) for line in trace_path.read_text().splitlines()]
                if trace_path.exists()
                else []
            )
            assert len(model_traces) == result["model_calls"]
            for trace in model_traces:
                context = json.loads(trace["request"]["messages"][1]["content"])
                assert (
                    not {"reference", "solvable", "repair_round", "states", "contract"}
                    & context.keys()
                )
                assert context["source_publication_catalog"] == catalog
                assert all("observations" not in entry for entry in catalog)
                if summary.get("shared_public_tool_units") or read_protocol_public(root):
                    assert (
                        context["public_task_constraints"]["evaluation_as_of"]
                        == task.as_of.isoformat()
                    )
                    assert context["public_task_constraints"]["freshness_seconds"] == 300
                    from upf_agent.v8.e3_public import publication_generation

                    generation = publication_generation(context["current_source_publication"])
                    assert all(
                        context["confirmed_task"][k] == generation
                        for k in ("manual_generation", "log_generation", "topology_generation")
                    )
                traces += 1
        rows.append(
            {
                "case_id": result["case_id"],
                "method": method,
                "primary_closed": closed,
                "false_closure": result["false_closure"],
                "correct_stop": result["correct_stop"],
                "budget_ok": result["budget_ok"],
            }
        )
    for method, cost in costs.items():
        if counts[method]:
            assert all(summary["per_method"][method][key] == value for key, value in cost.items())
    report = {
        "schema": "e3-readonly-replay-1",
        "input": str(root),
        "input_hashes_verified": len(hashes),
        "method_input_copies_verified": copied_inputs,
        "runs": len(rows),
        "per_method": dict(counts),
        "evidence_revisions_verified": sources,
        "immutable_batches": batches,
        "actual_model_traces_checked": traces,
        "costs": {k: dict(v) for k, v in costs.items()},
        "actual_tool_attempts": dict(actual_attempts),
        "integrity_errors": integrity_errors,
        "results": rows,
        "new_model_calls": 0,
        "human_reviews_imported": 0,
        "source_sha256": summary["source"]["sha256"],
        "pass": not integrity_errors
        and len(rows) == summary["runs"]
        and all(counts[m] == 32 for m in summary["per_method"]),
    }
    write_json(output, report)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit(args.input, args.output)
    print(json.dumps({k: v for k, v in report.items() if k != "results"}, ensure_ascii=False))
