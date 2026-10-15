"""Versioned expert-requested engineering revision, validation only, never heldout intake."""

import argparse
import csv
import shutil
from pathlib import Path

from v8_e1_domain_readonly import run

from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.e1_dataset import read, sha, write
from upf_agent.v8.e1_domain_readonly import load_scope
from upf_agent.v8.e1_expert_revision import (
    generate_revision,
    identity_parameters,
    revision_manifest,
    revision_schema,
    translate_revision,
    validate_revision,
)
from upf_agent.v8.e1_source_closure import VerifiedDomainTools, verify_admission
from upf_agent.v8.e1_verified_head import run_verified_p5
from upf_agent.v8.experiment_metrics import MetricCollector
from upf_agent.v8.models import EvaluationContext, OrchestrationTask, digest
from upf_agent.v8.phase2 import _direct
from upf_agent.v8.plan_generator import PlanBudget
from upf_agent.v8.plan_ir import ActionPattern, CaseGold, GoldBranch
from upf_agent.v8.plan_metrics import score_case


def revised_reference(task, meta, root):
    scope = load_scope(root, task)
    patterns = [
        ActionPattern(
            pattern_id="id-" + obj,
            action_type="CHECK_IDENTITY",
            target=obj,
            parameters=identity_parameters(root, task, scope, obj),
        )
        for obj in task.objects
    ]
    for obj, device in (("upf", "ogstun"), ("ue", "uesimtun0")):
        patterns.append(
            ActionPattern(
                pattern_id="tun-" + obj,
                action_type="READ_TUN_INTERFACE",
                target=obj,
                parameters={"device": device, "basis": "inspect_existing"},
                depends_on=["id-" + obj],
            )
        )
    for chain in ("INPUT", "OUTPUT"):
        patterns.append(
            ActionPattern(
                pattern_id="filter-" + chain,
                action_type="READ_FILTER_COUNTERS",
                target="upf",
                parameters={"chain": chain, "basis": "inspect_existing"},
                depends_on=["id-upf"],
            )
        )
    patterns.append(
        ActionPattern(
            pattern_id="probe",
            action_type="READ_SESSION_PROBE",
            target="ue",
            parameters={"probe_id": "normal", "basis": "inspect_existing"},
            depends_on=["id-ue"],
        )
    )
    for obj, capture in (("upf", "core-any"), ("ue", "ue-any")):
        patterns.append(
            ActionPattern(
                pattern_id="pcap-" + obj,
                action_type="READ_PACKET_CAPTURE",
                target=obj,
                parameters={"capture_id": capture, "basis": "inspect_existing"},
                depends_on=["id-" + obj],
            )
        )
        patterns.append(
            ActionPattern(
                pattern_id="log-" + obj,
                action_type="READ_LOG",
                target=obj,
                depends_on=["id-" + obj],
            )
        )
        patterns.append(
            ActionPattern(
                pattern_id="manual-" + obj,
                action_type="READ_MANUAL_REFERENCE",
                target=obj,
                parameters={
                    "product": task.object_profiles[obj].product,
                    "version": task.object_profiles[obj].version,
                },
                depends_on=["id-" + obj],
            )
        )
    patterns.append(
        ActionPattern(
            pattern_id="compare",
            action_type="COMPARE_CAPTURE_WINDOWS",
            target="upf",
            parameters={"peer_object_id": "ue", "input_basis": "frozen_capture_inventory"},
            depends_on=["id-upf", "id-ue"],
        )
    )
    return CaseGold(
        case_id=meta["case_id"],
        source_group=meta["source_group"],
        structure_family=meta["structure_family"],
        source_level="D2",
        split="validation",
        synthetic=False,
        reviewed=False,
        solvability="needs_evidence",
        objects=task.objects,
        version=task.version,
        as_of=task.as_of,
        permission_fingerprint=digest(task.permission),
        visible_evidence=task.observation_files,
        source_hashes={r: sha(root / r) for r in task.observation_files},
        any_of=[
            GoldBranch(branch_id="explicit-upf-ue-log-read-draft", required=patterns),
            GoldBranch(
                branch_id="ue-log-via-projected-session-record-draft",
                required=[p for p in patterns if p.pattern_id != "log-ue"],
            ),
        ],
        root_cause_truth="experimental_injection",
        stop_conditions=[
            "会话未知、空日志、缺捕获、版本不符或冲突时补证；计划不可执行",
            "只检查本地网关观察，不宣称根因、DN送达、真实修复或诊断完成",
        ],
    )


def prepare(source, output):
    if output.exists():
        raise ValueError("fresh revision input required")
    for name, expected in read(source / "sha256_manifest.json").items():
        if sha(source / name) != expected:
            raise ValueError("old validation source changed")
    rows = read(source / "index.json")
    if len(rows) != 12 or any(
        not r["case_id"].startswith("E1-CAL-N")
        or read(source / "organizer-only" / r["case_id"] / "case-reference-draft.json")["split"]
        != "validation"
        for r in rows
    ):
        raise ValueError("only the existing twelve validation cases permitted")
    output.mkdir(parents=True)
    shutil.copytree(source / "cases", output / "cases")
    forms = []
    for row in rows:
        cid = row["case_id"]
        root = output / "cases" / cid
        task = OrchestrationTask.model_validate(read(root / "task.json"))
        task.question = (
            "排查 UE 经 UPF 到本地网关10.45.0.1的探针异常，给出只读调查计划。"
            "核对ogstun/uesimtun0、filter的INPUT与OUTPUT方向和计数、UE会话/探针、"
            "两侧冻结抓包的位置/时窗/完整性、UPF及UE运行日志和固定版本Open5GS/UERANSIM手册。"
            "UE日志也可通过既有session记录的原文核对；RAN先核对身份，必要时补充日志。"
            "session=null和空日志保留未知，operstate=UNKNOWN不能独立判故障。"
            "源于本地网关的观察不证明DN/应用送达；只读，未执行修复。"
        )
        write(root / "task.json", task.model_dump(mode="json"))
        verify_admission(root, task)
        private = output / "organizer-only" / cid
        shutil.copytree(source / "organizer-only" / cid, private)
        old_ref = private / "case-reference-draft.json"
        old_ref.rename(private / "prior-reference-draft.json")
        gold = revised_reference(task, row, root)
        write(private / "case-reference-draft.json", gold.model_dump(mode="json"))
        write(
            private / "revision-response.json",
            {
                "expert_opinions_source": "docs/v8/technical_review_records.json",
                "reference_is_revised_draft": True,
                "reviewed": False,
                "R01_R04": (
                    "both interfaces, both filter directions, captures/comparison, logs "
                    "and manual checks cover all cases"
                ),
                "R02": "normal admission SHA, version and namespace parameters",
                "R03": (
                    "needs_evidence; causal/semantic success not approved; "
                    "two investigation branches"
                ),
                "UE_log_alternative_basis": (
                    "verified session_probe_inventory.session_log_excerpt projects "
                    "the same existing ue.log"
                ),
                "human_reapproval_required": True,
            },
        )
        for seat in ("A", "B"):
            forms.append(
                {
                    "case_id": cid,
                    "seat": seat,
                    "reference_sha256": digest(gold),
                    "reviewer": "",
                    "decision": "",
                    "notes": "",
                    "review_version": "",
                    "review_source": "",
                }
            )
    write(output / "index.json", rows)
    with (output / "organizer-only/gold-double-review.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as f:
        w = csv.DictWriter(f, fieldnames=list(forms[0]))
        w.writeheader()
        w.writerows(forms)
    write(
        output / "summary.json",
        {
            "validation_inputs": 12,
            "revised_unapproved_references": 12,
            "required_patterns": [15, 14],
            "expert_origin_accepted": True,
            "new_revision_Gold_approved": 0,
            "new_independent_cases": 0,
            "heldout_inputs_read": 0,
            "common_budget_seconds": 180,
        },
    )
    write(
        output / "sha256_manifest.json",
        {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()},
    )
    return read(output / "summary.json")


def offline(dataset, output):
    if output.exists():
        raise ValueError("fresh audit output required")
    rows = []
    for meta in read(dataset / "index.json"):
        root = dataset / "cases" / meta["case_id"]
        task = OrchestrationTask.model_validate(read(root / "task.json"))
        contract = compile_contract(task)
        collector = MetricCollector(task.run_id)
        tools = VerifiedDomainTools(root, task, contract, PlanBudget(task, collector))
        _direct(task, tools)
        schema, caps, _, _ = revision_schema(
            task,
            EvaluationContext.from_task(task, contract, meta["case_id"]),
            list(tools.bindings.values()),
            root,
        )
        branches = schema["$defs"]["PlanStep"]["anyOf"]
        count = sum(
            b["properties"]["action_type"]["const"] == "READ_MANUAL_REFERENCE" for b in branches
        )
        rows.append(
            {
                "case_id": meta["case_id"],
                "admitted_K": sum(
                    b.category == "K" and b.evidence_id in caps["admissible_ids"]
                    for b in tools.bindings.values()
                ),
                "manual_branches": count,
                "identity_prefix": len(schema["properties"]["steps"]["prefixItems"]),
            }
        )
        write(output / meta["case_id"] / "schema.json", schema)
    write(output / "rows.json", rows)
    write(
        output / "summary.json",
        {
            "cases": len(rows),
            "all_manual_actions_reachable": all(r["manual_branches"] > 0 for r in rows),
            "all_identity_anchors_present": all(r["identity_prefix"] == 3 for r in rows),
            "model_calls": 0,
            "heldout_inputs_read": 0,
        },
    )
    return read(output / "summary.json")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["prepare", "audit", "run"])
    p.add_argument("--source", type=Path)
    p.add_argument("--dataset", type=Path)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--deployment", type=Path)
    p.add_argument("--cases", nargs="+")
    args = p.parse_args()
    if args.command == "prepare":
        result = prepare(args.source.resolve(), args.output.resolve())
    elif args.command == "audit":
        result = offline(args.dataset.resolve(), args.output.resolve())
    else:
        references = {
            r["case_id"]: CaseGold.model_validate(
                read(args.dataset / "organizer-only" / r["case_id"] / "case-reference-draft.json")
            )
            for r in read(args.dataset / "index.json")
            if not args.cases or r["case_id"] in args.cases
        }
        result = run(
            args.project.resolve(),
            args.dataset.resolve(),
            args.output.resolve(),
            args.deployment.resolve(),
            case_ids=list(references),
            tools_factory=VerifiedDomainTools,
            plan_generator=generate_revision,
            plan_translator=translate_revision,
            plan_validator=validate_revision,
            plan_scorer=score_case,
            references=references,
            head_manifest=revision_manifest(),
            p5_runner=run_verified_p5,
            extra_code_files=["scripts/v8_e1_expert_revision.py"],
        )
    print(result)
