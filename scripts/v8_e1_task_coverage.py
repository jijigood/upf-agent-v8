"""Two existing validation cases: explicit task requests and a small repair pilot.

Gold is loaded separately for post-generation scoring only. Original data, expert
decisions and heldout are unchanged. All artifacts require a fresh output path.
"""

import argparse
import shutil
from pathlib import Path

from v8_e1_domain_readonly import run

from upf_agent.v8.e1_covered_head import (
    ReservedHeadBudget,
    covered_manifest,
    generate_covered,
    translate_covered,
    validate_covered,
)
from upf_agent.v8.e1_dataset import read, sha, write
from upf_agent.v8.e1_domain_readonly import load_scope
from upf_agent.v8.e1_source_closure import VerifiedDomainTools
from upf_agent.v8.e1_task_coverage import TaskAction, TaskObligation, TaskRequest
from upf_agent.v8.e1_verified_head import run_verified_p5
from upf_agent.v8.models import OrchestrationTask, digest
from upf_agent.v8.plan_ir import CaseGold
from upf_agent.v8.plan_metrics import score_case

SELECTED = ["E1-CAL-N001", "E1-CAL-N003"]


def public_request(task, root):
    # This adapter is intentionally restricted to the existing explicit question,
    # rather than guessing obligations for arbitrary free-text diagnostic tasks.
    required_terms = [
        "只读调查",
        "ogstun/uesimtun0",
        "INPUT",
        "OUTPUT",
        "UPF及UE运行日志",
        "固定版本Open5GS/UERANSIM手册",
        "UE日志也可通过既有session记录",
    ]
    if not all(term in task.question for term in required_terms):
        raise ValueError("this task adapter requires the explicit existing validation question")
    scope = load_scope(root, task)
    obligations = []

    def add(name, description, action, obj, params=None, fields=()):
        obligations.append(
            TaskObligation(
                requirement_id=name,
                description=description,
                any_of=[
                    TaskAction(
                        action_type=action,
                        target=obj,
                        parameters=params or {},
                        required_fields=list(fields),
                    )
                ],
            )
        )

    for obj, device in (("upf", "ogstun"), ("ue", "uesimtun0")):
        add(obj + "-interface", "核对" + device, "READ_TUN_INTERFACE", obj, {"device": device})
    for chain in ("INPUT", "OUTPUT"):
        add(
            "filter-" + chain,
            "核对filter方向及计数",
            "READ_FILTER_COUNTERS",
            "upf",
            {"chain": chain},
        )
    probe_ids = scope.objects["ue"].probe_ids
    if len(probe_ids) != 1:
        raise ValueError("the public scope must identify exactly one recorded probe")
    add(
        "ue-session-probe",
        "核对UE会话及既有探针",
        "READ_SESSION_PROBE",
        "ue",
        {"probe_id": probe_ids[0]},
        ["session_probe_inventory"],
    )
    for obj in ("upf", "ue"):
        captures = scope.objects[obj].captures
        if len(captures) != 1:
            raise ValueError("the public scope must identify one capture per side")
        add(
            obj + "-capture",
            "核对该侧冻结抓包",
            "READ_PACKET_CAPTURE",
            obj,
            {"capture_id": captures[0]},
        )
        add(obj + "-log", "核对运行日志，空日志保留未知", "READ_LOG", obj, fields=["log_excerpt"])
        profile = task.object_profiles[obj]
        add(
            obj + "-manual",
            "核对固定产品版本手册",
            "READ_MANUAL_REFERENCE",
            obj,
            {"product": profile.product, "version": profile.version},
            ["instruction"],
        )
    ue_log = next(r for r in obligations if r.requirement_id == "ue-log")
    ue_log.any_of.append(
        TaskAction(
            action_type="READ_SESSION_PROBE",
            target="ue",
            parameters={"probe_id": probe_ids[0]},
            required_fields=["session_probe_inventory.session_log_excerpt"],
        )
    )
    add(
        "bilateral-capture-comparison",
        "核对两侧冻结库存的位置、时窗和完整性",
        "COMPARE_CAPTURE_WINDOWS",
        "upf",
        {"peer_object_id": "ue", "input_basis": "frozen_capture_inventory"},
    )
    return TaskRequest(
        question_sha256=digest(task.question),
        permission_sha256=digest(task.permission),
        object_profiles_sha256=digest(task.object_profiles),
        obligations=obligations,
    )


def prepare(source, output, case_ids=SELECTED):
    if output.exists():
        raise ValueError("fresh task-coverage input version required")
    if len(set(case_ids)) != len(case_ids) or any(cid not in SELECTED for cid in case_ids):
        raise ValueError("only the two preregistered existing validation cases are supported")
    index = {r["case_id"]: r for r in read(source / "index.json")}
    output.mkdir(parents=True)
    rows = []
    for cid in case_ids:
        original = source / "cases" / cid
        root = output / "cases" / cid
        shutil.copytree(original, root)
        task = OrchestrationTask.model_validate(read(root / "task.json"))
        request = public_request(task, root)
        write(root / "data/task-request.json", request.model_dump(mode="json"))
        # Original unapproved references stay in the organizer-only scoring area.
        shutil.copytree(source / "organizer-only" / cid, output / "organizer-only" / cid)
        gold = CaseGold.model_validate(
            read(output / "organizer-only" / cid / "case-reference-draft.json")
        )
        if gold.reviewed or gold.split != "validation":
            raise ValueError("this repair pilot uses only unapproved validation references")
        rows.append(index[cid] | {"task_request_sha256": digest(request), "formal_vpr": None})
    write(output / "index.json", rows)
    write(
        output / "summary.json",
        {
            "cases": len(rows),
            "new_independent_cases": 0,
            "original_heldout_inputs_read": 0,
            "task_obligations_source": "explicit original public questions and namespace scope",
            "reference_approval": False,
            "new_model_calls": 0,
        },
    )
    write(
        output / "sha256_manifest.json",
        {str(f.relative_to(output)): sha(f) for f in sorted(output.rglob("*")) if f.is_file()},
    )
    return read(output / "summary.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "run"])
    parser.add_argument("--source", type=Path)
    parser.add_argument("--dataset", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--deployment", type=Path)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    if args.command == "prepare":
        result = prepare(args.source.resolve(), args.output.resolve())
    else:
        dataset = args.dataset.resolve()
        references = {
            row["case_id"]: CaseGold.model_validate(
                read(dataset / "organizer-only" / row["case_id"] / "case-reference-draft.json")
            )
            for row in read(dataset / "index.json")
        }
        result = run(
            args.project.resolve(),
            dataset,
            args.output.resolve(),
            args.deployment.resolve(),
            case_ids=list(references),
            tools_factory=VerifiedDomainTools,
            plan_generator=generate_covered,
            plan_translator=translate_covered,
            plan_validator=validate_covered,
            budget_factory=ReservedHeadBudget,
            plan_scorer=score_case,
            references=references,
            head_manifest=covered_manifest(),
            p5_runner=run_verified_p5,
            extra_code_files=["scripts/v8_e1_task_coverage.py"],
        )
    print(result)
