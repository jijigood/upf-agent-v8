"""Correct task-derived references and rescore immutable phase-two outputs, no models."""

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.experiment_manifest import source_manifest
from upf_agent.v8.experiment_metrics import summarize_events
from upf_agent.v8.models import EvaluationContext, EvidenceBinding, OrchestrationTask, digest
from upf_agent.v8.phase1 import write_json
from upf_agent.v8.plan_ir import CaseGold
from upf_agent.v8.plan_metrics import score_case, summarize_cases
from upf_agent.v8.plan_translator import translate_plan
from upf_agent.v8.plan_validator import validate_plan
from upf_agent.v8.reference_revision import revise_peer_mapping


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(root):
    manifest = read(root / "sha256_manifest.json")
    for name, expected in manifest.items():
        path = (root / name).resolve(strict=True)
        if not path.is_relative_to(root) or sha(path) != expected:
            raise ValueError(f"immutable pilot hash mismatch: {name}")
    return len(manifest)


def adjust_failure(metrics, row):
    if row["method_failure"] or row["generation_error"] or row["finish_reason"] == "length":
        metrics["reference_pass"] = False
        if metrics["vpr"] is not None:
            metrics["vpr"] = False
    return metrics


def revise_batch(project, pilot, output, audit_summary):
    project, pilot, output = project.resolve(), pilot.resolve(), output.resolve()
    if output.exists() or output.is_relative_to(pilot) or pilot.is_relative_to(output):
        raise ValueError("choose a new independent output directory")
    source = source_manifest(project)
    verified = verify_manifest(pilot)
    protocol = read(pilot / "protocol.json")
    original_rows = [
        json.loads(s) for s in (pilot / "metrics-by-case.jsonl").read_text().splitlines()
    ]
    if len(original_rows) != protocol["cases"] * len(protocol["methods"]):
        raise ValueError("incomplete original pilot")
    cases = sorted((pilot / "cases").glob("*/case-reference.json"))
    output.mkdir(parents=True)
    write_json(output / "supplied-audit-summary.json", read(audit_summary))
    revised, changes, ambiguities = {}, [], []
    for path in cases:
        task = OrchestrationTask.model_validate(read(path.parent / "case-task.json"))
        old = CaseGold.model_validate(read(path))
        new = revise_peer_mapping(task, old)
        revised[old.case_id] = new
        folder = output / "cases" / old.case_id
        write_json(folder / "case-reference.json", new.model_dump(mode="json"))
        # Original task/spec are exact copies, never silently regenerate historical inputs.
        for name in ["case-task.json", "case-spec.json"]:
            (folder / name).write_bytes((path.parent / name).read_bytes())
        changes.append(
            {
                "case_id": old.case_id,
                "changed": digest(old) != digest(new),
                "issue_codes": ["R07", "R09"] if digest(old) != digest(new) else [],
                "original_reference_file_sha256": sha(path),
                "original_reference_digest": digest(old),
                "revised_reference_file_sha256": sha(folder / "case-reference.json"),
                "revised_reference_digest": digest(new),
                "original_task_file_sha256": sha(path.parent / "case-task.json"),
                "before_branches": [b.model_dump(mode="json") for b in old.any_of],
                "after_branches": [b.model_dump(mode="json") for b in new.any_of],
            }
        )
        if task.template == "manual_operation" and "双侧映射" in task.question:
            ambiguities.append(old.case_id)
    write_json(output / "reference-changes.json", changes)
    write_json(
        output / "protocol.json",
        {
            "original_pilot": str(pilot),
            "original_protocol_sha256": sha(pilot / "protocol.json"),
            "source": source,
            "cases": len(cases),
            "methods": protocol["methods"],
            "reviewed": False,
            "synthetic": True,
            "reference_revision": "task-required-two-sided-mapping-1",
            "reference_basis": "task/path and user audit; post-output development correction",
            "manual_task_scope": "user clarified manual tasks need no mapping; old text retained",
            "new_model_calls": 0,
            "reused_outputs": True,
            "new_heldout_consumed": False,
        },
    )
    scores, delta, controls = [], [], []
    for row in original_rows:
        case_id, method = row["case_id"], row["method"]
        folder = pilot / "runs" / case_id / f"method-{protocol['methods'].index(method) + 1}"
        task = OrchestrationTask.model_validate(read(folder / "task.json"))
        context = EvaluationContext.model_validate(read(folder / "context.json"))
        bindings = [EvidenceBinding.model_validate(b) for b in read(folder / "bindings.json")]
        old_gold = CaseGold.model_validate(read(pilot / "cases" / case_id / "case-reference.json"))
        raw = read(folder / "raw-output.json")
        text = (folder / "raw-plan.txt").read_text()
        if (
            raw["content"] != text
            or hashlib.sha256(text.encode()).hexdigest() != raw["content_sha256"]
        ):
            raise ValueError("raw output changed")
        translation = translate_plan(text)
        assert translation.model_dump(mode="json") == read(folder / "translation.json")
        validation = validate_plan(
            translation.plan, bindings, task, compile_contract(task), context, folder / "runtime"
        )
        assert validation.model_dump(mode="json") == read(folder / "validation.json")
        old_metrics = adjust_failure(score_case(translation.plan, validation, old_gold), row)
        assert all(row[k] == v for k, v in old_metrics.items())
        new_metrics = adjust_failure(
            score_case(translation.plan, validation, revised[case_id]), row
        )
        scores.append({**row, **new_metrics})
        events = [json.loads(s) for s in (folder / "traces.jsonl").read_text().splitlines()]
        costs = summarize_events(events)
        assert costs == read(folder / "metrics.json")
        maps = [s for s in translation.plan.steps if s.action_type == "VERIFY_PEER_MAPPING"]
        ids = {
            s.target: s.step_id for s in translation.plan.steps if s.action_type == "CHECK_IDENTITY"
        }
        fault = task.template in {"upf_n3_fault", "upf_n4_fault"}
        mapping_complete = bool(
            len(maps) == 1
            and maps[0].target == task.path.positions[0].object_id
            and maps[0].parameters == {"peer_object_id": task.path.positions[1].object_id}
            and set(maps[0].depends_on) == set(ids.values())
            and set(ids) == set(task.objects)
        )
        if fault:
            assert mapping_complete
            for mutation in ["missing_mapping", "wrong_peer", "one_identity_dependency"]:
                plan = translation.plan.model_copy(deep=True)
                step = next(s for s in plan.steps if s.action_type == "VERIFY_PEER_MAPPING")
                if mutation == "missing_mapping":
                    plan.steps = [s for s in plan.steps if s.action_type != "VERIFY_PEER_MAPPING"]
                elif mutation == "wrong_peer":
                    step.parameters["peer_object_id"] = step.target
                else:
                    step.depends_on = [ids[step.target]]
                # Reuse validity solely to isolate reference matching, not Validator testing.
                rejected = not score_case(plan, validation, revised[case_id])["reference_pass"]
                assert rejected, (case_id, method, mutation)
                controls.append(
                    {
                        "case_id": case_id,
                        "method": method,
                        "mutation": mutation,
                        "rejected": rejected,
                    }
                )
        delta.append(
            {
                "case_id": case_id,
                "method": method,
                "raw_plan_sha256": sha(folder / "raw-plan.txt"),
                "original_run": str(folder),
                "validator_pass": validation.raw_plan_validity,
                "old_reference_pass": old_metrics["reference_pass"],
                "new_reference_pass": new_metrics["reference_pass"],
                "old_branch": old_metrics["branch"],
                "new_branch": new_metrics["branch"],
                "fault": fault,
                "mapping_steps": len(maps),
                "mapping_and_both_identities_verified": mapping_complete if fault else None,
                "costs_unchanged": True,
            }
        )
    (output / "metrics-by-case.jsonl").write_text(
        "".join(json.dumps(s, ensure_ascii=False) + "\n" for s in scores)
    )
    write_json(output / "score-comparison.json", delta)
    write_json(output / "reference-negative-controls.json", controls)
    assert verify_manifest(pilot) == verified and source_manifest(project) == source
    summary = {
        "schema": "v8-phase2-reference-revision-1",
        "completed_at_utc": datetime.now(UTC).isoformat(),
        "source": source,
        "reference_cases": len(cases),
        "references_changed": sum(c["changed"] for c in changes),
        "manual_references_unchanged": len(ambiguities),
        "manual_text_ambiguity_cases": ambiguities,
        "runs_rescored": len(scores),
        "fault_runs_mapping_verified": sum(d["fault"] for d in delta),
        "negative_controls": len(controls),
        "negative_controls_rejected": sum(c["rejected"] for c in controls),
        "verified_original_files_before_and_after": verified,
        "per_method": {
            m: summarize_cases([s for s in scores if s["method"] == m]) for m in protocol["methods"]
        },
        "reviewer_basis": (
            "user self-reported audit; one reviewer, individual signed forms not supplied"
        ),
        "supplied_audit_reference_coverage": 24,
        "supplied_audit_plan_coverage": 96,
        "independent_double_review_complete": False,
        "revised_reference_approval_received": False,
        "vpr": None,
        "new_model_calls": 0,
        "new_heldout_consumed": False,
        "original_pilot_modified": False,
        "post_output_reference_revision": True,
        "pass": all(s["reference_pass"] and s["validator_pass"] for s in scores),
    }
    write_json(output / "summary.json", summary)
    write_json(
        output / "sha256_manifest.json",
        {str(q.relative_to(output)): sha(q) for q in sorted(output.rglob("*")) if q.is_file()},
    )
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit-summary", type=Path, required=True)
    args = parser.parse_args()
    result = revise_batch(
        Path(__file__).resolve().parents[1], args.pilot, args.output, args.audit_summary
    )
    print(
        json.dumps(
            {k: v for k, v in result.items() if k not in {"source", "per_method"}},
            ensure_ascii=False,
        )
    )
