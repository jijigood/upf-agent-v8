"""Versioned audit, anonymous material export and offline replay of review repairs."""

import argparse
import csv
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.experiment_manifest import source_manifest
from upf_agent.v8.experiment_metrics import summarize_events
from upf_agent.v8.models import EvaluationContext, EvidenceBinding, OrchestrationTask, digest
from upf_agent.v8.phase1 import write_json
from upf_agent.v8.plan_ir import CaseGold
from upf_agent.v8.plan_metrics import score_case
from upf_agent.v8.plan_translator import translate_plan
from upf_agent.v8.plan_validator import validate_plan
from upf_agent.v8.review_evidence import source_review


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pinned(root, manifest):
    values = read(root / manifest)
    for name, expected in values.items():
        assert sha(root / name) == expected, name
    return len(values)


def audit_phase2(root):
    pinned_count = pinned(root, "sha256_manifest.json")
    records = []
    for folder in sorted((root / "runs").glob("pilot-*/method-*")):
        task = OrchestrationTask.model_validate(read(folder / "task.json"))
        context = EvaluationContext.model_validate(read(folder / "context.json"))
        bindings = [EvidenceBinding.model_validate(b) for b in read(folder / "bindings.json")]
        raw = (folder / "raw-plan.txt").read_text()
        raw_output = read(folder / "raw-output.json")
        assert raw_output["content"] == raw
        assert hashlib.sha256(raw.encode()).hexdigest() == raw_output["content_sha256"]
        translated = translate_plan(raw)
        assert translated.model_dump(mode="json") == read(folder / "translation.json")
        validation = validate_plan(
            translated.plan, bindings, task, compile_contract(task), context, folder / "runtime"
        )
        assert validation.model_dump(mode="json") == read(folder / "validation.json")
        gold = CaseGold.model_validate(
            read(root / "cases" / folder.parent.name / "case-reference.json")
        )
        row = read(folder / "case-metrics.json")
        metrics = score_case(translated.plan, validation, gold)
        if row["method_failure"] or row["generation_error"] or row["finish_reason"] == "length":
            metrics["reference_pass"] = False
            if metrics["vpr"] is not None:
                metrics["vpr"] = False
        assert all(row[k] == v for k, v in metrics.items())
        traces = [json.loads(s) for s in (folder / "traces.jsonl").read_text().splitlines()]
        costs = summarize_events(traces)
        assert costs == read(folder / "metrics.json")
        assert costs["invocations"]["tool"]["attempted"] <= 8
        assert costs["invocations"]["model"]["attempted"] <= 8
        mappings = []
        by_id = {b.evidence_id: b for b in bindings}
        for step in translated.plan.steps if translated.plan else []:
            if step.action_type == "VERIFY_PEER_MAPPING":
                mappings.append(
                    {
                        "step_id": step.step_id,
                        "basis": step.parameters.get("basis", "existing_pair"),
                        "pending": step.parameters.get("pending", []),
                        "P_cited_objects": sorted(
                            {
                                by_id[r.evidence_id].object_id
                                for r in step.evidence
                                if r.evidence_id in by_id and by_id[r.evidence_id].category == "P"
                            }
                        ),
                    }
                )
        records.append(
            {
                "run": str(folder.relative_to(root)),
                "validator_pass": validation.raw_plan_validity,
                "reference_pass": metrics["reference_pass"],
                "issues": metrics["issues"],
                "mappings": mappings,
                "elapsed_seconds": row["elapsed_seconds"],
                "tool_calls": costs["invocations"]["tool"]["attempted"],
                "model_calls": costs["invocations"]["model"]["attempted"],
                "human_approval": gold.reviewed,
            }
        )
    expected = read(root / "protocol.json")["cases"] * 4
    assert len(records) == expected
    return {
        "experiment": "review-remediation-phase2",
        "runs": len(records),
        "pinned_files": pinned_count,
        "machine_valid": sum(r["validator_pass"] for r in records),
        "draft_reference_pass": sum(r["reference_pass"] for r in records),
        "elapsed_budget_violations": [r["run"] for r in records if r["elapsed_seconds"] > 180],
        "actual_model_calls": sum(r["model_calls"] for r in records),
        "actual_tool_calls": sum(r["tool_calls"] for r in records),
        "formal_VPR": None,
        "formal_approval": False,
        "records": records,
        "audit_pass": True,
        "development_pass": all(
            r["validator_pass"] and r["reference_pass"] and r["elapsed_seconds"] <= 180
            for r in records
        ),
    }


def old_review_differences(project):
    received = project / "runtime/v8-next/20261010-001/20261010-001"
    original = read(
        project / "runtime/v8-next/review-intake-20261010-001/received-evidence-sha256.json"
    )
    assert all(sha(received / n) == h for n, h in original.items())
    original_sources = read(received / "input-sha256.json")
    prefix = "D:\\专利\\upf-agent-v8\\"
    assert all(
        name.startswith(prefix) and sha(project / name[len(prefix) :].replace("\\", "/")) == h
        for name, h in original_sources.items()
    )
    e5 = []
    for note in sorted((received / "phase3/E5-notes").glob("*.json")):
        entry = read(note)
        base = project / Path(entry["input"]["physical_source_root"]).relative_to(
            "/home/huangxiaolin/upf-agent-v8"
        )
        visible = read(base / "input.json")
        task = OrchestrationTask.model_validate(visible["task"])
        checks = [
            {
                "evidence_id": b["evidence_id"],
                "findings": source_review(base, EvidenceBinding.model_validate(b), task),
            }
            for b in visible["bindings"]
        ]
        missing = sorted(
            {
                code
                for c in checks
                for code in c["findings"]
                if code not in entry["relevant_evidence_or_issue_codes"]
            }
        )
        e5.append(
            {
                "item_id": entry["item_id"],
                "received_decision": entry["decision"],
                "case": base.name,
                "binding_source_checks": checks,
                "additional_source_codes": missing,
            }
        )
    corrections = [
        r
        for r in e5
        if r["received_decision"] != "blocked"
        and any(
            "source_observed_mismatch" in c["findings"]
            and "binding_stale_observation" in c["findings"]
            for c in r["binding_source_checks"]
        )
    ]
    assert {r["case"] for r in corrections} == {"forbidden-09-01", "forbidden-09-02"}
    phase2 = []
    old = project / "runtime/v8-next/phase2/closure-full-004"
    for folder in sorted((old / "runs").glob("pilot-*/method-*")):
        task = OrchestrationTask.model_validate(read(folder / "task.json"))
        bindings = [EvidenceBinding.model_validate(b) for b in read(folder / "bindings.json")]
        plan = translate_plan((folder / "raw-plan.txt").read_text()).plan
        report = validate_plan(
            plan,
            bindings,
            task,
            compile_contract(task),
            EvaluationContext.model_validate(read(folder / "context.json")),
            folder / "runtime",
        )
        phase2.append(
            {
                "run": str(folder.relative_to(old)),
                "new_policy_valid": report.raw_plan_validity,
                "old_policy_valid": read(folder / "validation.json")["raw_plan_validity"],
                "new_policy_issues": sorted({i.code for i in report.issues}),
            }
        )
    return {
        "received_original_files_unchanged": len(original),
        "source_files_unchanged": len(original_sources),
        "review_corrections": corrections,
        "e5_source_checks": e5,
        "phase2_new_policy": phase2,
        "new_policy": "v8-plan-validator-2; retrospective development audit, not a new model run",
        "formal_approvals_imported": 0,
    }


def export_e5(batch, output):
    """Neutral review views; exact raw originals and identifier map stay organizer-only."""
    output.mkdir(parents=True)
    index, private = [], []
    for folder in sorted((batch / "cases").iterdir()):
        identifier = digest([sha(folder / "candidate.txt"), sha(folder / "input.json")])[:20]
        target = output / "public" / "items" / identifier
        target.mkdir(parents=True)
        original_batch = read(folder / "input.json")["context"]["batch_id"]
        alias = "review-batch-" + identifier
        mapping = {original_batch: alias}
        raw_root = output / "organizer-only" / "originals" / identifier
        raw_root.mkdir(parents=True)
        for source_name, view_name in [
            ("candidate.txt", "candidate-review-view.txt"),
            ("input.json", "visible-input-review-view.json"),
        ]:
            raw = (folder / source_name).read_text()
            neutral = raw.replace(json.dumps(original_batch), json.dumps(alias))
            (target / view_name).write_text(neutral)
            shutil.copy2(folder / source_name, raw_root / source_name)
            assert neutral.replace(json.dumps(alias), json.dumps(original_batch)) == raw
        shutil.copytree(folder / "data", target / "data")
        index.append(
            {
                "anonymous_id": identifier,
                "candidate": f"items/{identifier}/candidate-review-view.txt",
                "visible_input": f"items/{identifier}/visible-input-review-view.json",
                "source_root": f"items/{identifier}",
                "candidate_sha256": sha(target / "candidate-review-view.txt"),
                "original_candidate_sha256": sha(folder / "candidate.txt"),
                "view_kind": "identifier-only substitution; not byte-identical raw output",
                "reviewed": False,
            }
        )
        private.append(
            {
                "anonymous_id": identifier,
                "original_case": folder.name,
                "development_reference": read(folder / "reference.json"),
                "identifier_map": mapping,
            }
        )
    assert len({r["anonymous_id"] for r in index}) == 120
    write_json(output / "public" / "input-index.json", index)
    write_json(output / "organizer-only" / "case-map.json", private)
    write_json(
        output / "public" / "review-protocol.json",
        {
            "version": "neutral-review-view-2",
            "identity_fields_changed": ["candidate.batch_id", "input.context.batch_id"],
            "step_text_parameters_evidence_permissions_dependencies_changed": False,
            "raw_originals": "organizer-only; public hashes allow version confirmation",
            "strict_blind_review_completed": False,
            "anonymization_limit": (
                "semantic faults and style can reveal controls; no label guarantee"
            ),
        },
    )
    for reviewer in [1, 2]:
        with (output / "public" / f"reviewer-{reviewer}.csv").open(
            "w", encoding="utf-8-sig", newline=""
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "anonymous_id",
                    "candidate_sha256",
                    "reviewer",
                    "decision",
                    "rationale",
                    "source_locators",
                ],
            )
            writer.writeheader()
            writer.writerows({k: r.get(k, "") for k in writer.fieldnames} for r in index)
    hashes = {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()}
    import re

    assert not any(
        re.search(r"e5-(?:allowed|forbidden|unknown)-", p.read_text(errors="replace"))
        for p in (output / "public").rglob("*")
        if p.is_file()
    )
    write_json(output / "sha256_manifest.json", hashes)
    return {
        "candidates": 120,
        "source_paths_hide_development_categories": True,
        "strict_blind_review_completed": False,
        "formal_approval": False,
        "files": len(hashes),
    }


def fresh_e5_source_checks(batch):
    records = []
    for folder in sorted((batch / "cases").iterdir()):
        visible = read(folder / "input.json")
        task = OrchestrationTask.model_validate(visible["task"])
        checks = [
            {
                "evidence_id": b["evidence_id"],
                "findings": source_review(folder, EvidenceBinding.model_validate(b), task),
            }
            for b in visible["bindings"]
        ]
        validation = read(folder / "A4-validation.json")
        reference = read(folder / "reference.json")
        # Check source faults rather than overriding the explicit conditional gap outlet.
        if reference["category"] == "allowed":
            assert all(not c["findings"] for c in checks)
            assert validation["raw_plan_validity"]
        records.append(
            {
                "case": folder.name,
                "category": reference["category"],
                "source_checks": checks,
                "validator_issues": validation["issues"],
            }
        )
    return {
        "cases": len(records),
        "independent_physical_source_review": True,
        "category_counts": dict(Counter(r["category"] for r in records)),
        "records": records,
        "formal_approval": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["phase2", "old-review", "export-e5", "source-e5"])
    parser.add_argument("--root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("new audit or export ID required")
    if args.action == "phase2":
        result = audit_phase2(args.root)
    elif args.action == "old-review":
        result = old_review_differences(args.project)
    elif args.action == "export-e5":
        result = export_e5(args.root, args.output)
        write_json(args.output / "export-summary.json", result)
        print(json.dumps(result, ensure_ascii=False))
        raise SystemExit(0)
    else:
        result = fresh_e5_source_checks(args.root)
    result["source_manifest"] = source_manifest(args.project)
    write_json(args.output, result)
    print(
        json.dumps(
            {
                k: v
                for k, v in result.items()
                if k not in {"records", "source_manifest", "e5_source_checks", "phase2_new_policy"}
            },
            ensure_ascii=False,
        )
    )
