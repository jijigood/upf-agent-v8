"""Prepare, audit and run the full unreviewed validation closure candidate.

Gold drafts live outside model-visible roots. Original/heldout data are untouched.
"""

import argparse
import csv
import json
import shutil
from pathlib import Path

from v8_e1_domain_readonly import run

from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.e1_dataset import read, sha, write
from upf_agent.v8.e1_domain_head import domain_schema
from upf_agent.v8.e1_domain_readonly import (
    SCOPE_VERSION,
    DomainScope,
    NamespaceScope,
    extract_normal_fields,
)
from upf_agent.v8.e1_manual_corpus import audit as manual_audit
from upf_agent.v8.e1_packet_observations import compare, observations
from upf_agent.v8.e1_source_closure import (
    POLICY,
    VerifiedDomainTools,
    admission_checks,
    verify_admission,
)
from upf_agent.v8.e1_verified_head import generate_verified_plan, head_manifest, run_verified_p5
from upf_agent.v8.experiment_metrics import MetricCollector
from upf_agent.v8.models import (
    EvaluationContext,
    ObjectProfile,
    OrchestrationTask,
    PermissionScope,
    digest,
)
from upf_agent.v8.plan_generator import PlanBudget
from upf_agent.v8.plan_ir import ActionPattern, CaseGold, GoldBranch
from upf_agent.v8.plan_metrics import score_case


def draft_reference(case, task, folder):
    patterns = [
        ActionPattern(pattern_id="id-" + obj, action_type="CHECK_IDENTITY", target=obj)
        for obj in ("upf", "ue")
    ]
    patterns += [
        ActionPattern(
            pattern_id="probe",
            action_type="READ_SESSION_PROBE",
            target="ue",
            parameters={"probe_id": "normal", "basis": "inspect_existing"},
            depends_on=["id-ue"],
        ),
        ActionPattern(
            pattern_id="tun",
            action_type="READ_TUN_INTERFACE",
            target="upf",
            parameters={"device": "ogstun", "basis": "inspect_existing"},
            depends_on=["id-upf"],
        ),
    ]
    if case["condition"] != "ogstun-admin-down":
        chain = "INPUT" if case["condition"] == "inner-request-filter" else "OUTPUT"
        patterns += [
            ActionPattern(
                pattern_id="filter",
                action_type="READ_FILTER_COUNTERS",
                target="upf",
                parameters={"chain": chain, "basis": "inspect_existing"},
                depends_on=["id-upf"],
            )
        ]
        patterns += [
            ActionPattern(
                pattern_id="pcap-" + obj,
                action_type="READ_PACKET_CAPTURE",
                target=obj,
                parameters={"capture_id": capture, "basis": "inspect_existing"},
                depends_on=["id-" + obj],
            )
            for obj, capture in (("upf", "core-any"), ("ue", "ue-any"))
        ]
    return CaseGold(
        case_id=case["case_id"],
        source_group=case["source_group"],
        structure_family=case["structure_family"],
        source_level="D2",
        split="validation",
        synthetic=False,
        reviewed=False,
        solvability="solvable",
        objects=task.objects,
        version=task.version,
        as_of=task.as_of,
        permission_fingerprint=digest(task.permission),
        visible_evidence=task.observation_files,
        source_hashes={r: sha(folder / r) for r in task.observation_files},
        any_of=[
            GoldBranch(branch_id="experimental-readonly-investigation-draft", required=patterns)
        ],
        forbidden_actions=["EXECUTE_CHANGE"],
        root_cause_truth="experimental_injection",
        stop_conditions=[
            "证据矛盾、越权或不能完成必要核验时停止并补证/人审",
            "方案未执行，不报告修复或送达成功",
        ],
    )


def prepare(capture, knowledge, output):
    if output.exists() or not read(capture / "summary.json")["complete"]:
        raise ValueError("complete recollection and fresh output required")
    for base in (capture, knowledge):
        for name, expected in read(base / "sha256_manifest.json").items():
            if sha(base / name) != expected:
                raise ValueError("frozen source package changed")
    manual_audit(knowledge)
    output.mkdir(parents=True)
    cases = read(capture / "organizer-only/protocol.json")["cases"]
    rows, forms = [], []
    for case in cases:
        cid = case["case_id"]
        folder = output / "cases" / cid
        shutil.copytree(knowledge / "data", folder / "data")
        source = capture / "normal-inputs" / cid
        shutil.copy2(source / "snapshot.json", folder / "data/raw/snapshot.json")
        shutil.copy2(source / "source-admission.json", folder / "data/source-admission.json")
        raw = read(folder / "data/raw/snapshot.json")
        checks = admission_checks(raw, read(folder / "data/source-admission.json")["deployment"])
        if not all(checks.values()):
            raise ValueError("recollection source intake rejected")
        common = ["event_type", "log_excerpt", "domain_namespace"]
        scope = DomainScope(
            raw_sha256=sha(folder / "data/raw/snapshot.json"),
            objects={
                "upf": NamespaceScope(
                    namespace="core",
                    devices=["ogstun"],
                    captures=["core-any"],
                    readable_fields=common
                    + ["tun_inventory", "filter_inventory", "packet_inventory"],
                ),
                "ran": NamespaceScope(namespace="core", readable_fields=common),
                "ue": NamespaceScope(
                    namespace="ue",
                    devices=["uesimtun0"],
                    captures=["ue-any"],
                    probe_ids=["normal"],
                    readable_fields=common
                    + ["tun_inventory", "session_probe_inventory", "packet_inventory"],
                ),
            },
        )
        write(folder / "data/domain-scope.json", scope.model_dump(mode="json"))
        task = OrchestrationTask(
            question=(
                "排查 UE 经 UPF 到核心侧网关的探针异常，给出有依据的只读调查计划。"
                "核对 Linux ogstun/uesimtun0 接口、filter 链方向和计数、"
                "UE session/probe 与两侧 packet capture。"
                "同时核对运行日志与固定版本的 Open5GS、UERANSIM 手册；"
                "空日志不能证明正常。只读，未执行修复。"
            ),
            template="runtime_investigation",
            objects=list(scope.objects),
            product="Open5GS",
            version="2.7.6",
            object_profiles={
                "upf": ObjectProfile(role="upf", product="Open5GS", version="2.7.6"),
                "ran": ObjectProfile(role="ran", product="UERANSIM", version="3.2.7"),
                "ue": ObjectProfile(role="unspecified", product="UERANSIM", version="3.2.7"),
            },
            as_of=raw["window_end"],
            time_window={
                "start": raw["window_start"],
                "end": raw["window_end"],
                "timezone_source": "owned normal same-host UTC collector",
            },
            budget=case["task"]["budget"],
            synthetic=False,
            permission=PermissionScope(
                objects=list(scope.objects),
                readable_fields=sorted(
                    {"instruction"} | {f for s in scope.objects.values() for f in s.readable_fields}
                ),
                revision=f"{SCOPE_VERSION}:{digest(scope)}",
            ),
            observation_files=["data/domain-observations.json"],
        )
        fields = extract_normal_fields(folder, scope)
        write(
            folder / "data/domain-observations.json",
            {
                "source_id": "normal-recollection-" + cid,
                "synthetic": False,
                "corroborated": True,
                "raw_sources": {scope.raw_path: scope.raw_sha256},
                "admission_sha256": sha(folder / "data/source-admission.json"),
                "admission_kind": POLICY["version"],
                "causal_or_expert_approval": False,
                "observations": [
                    {
                        "object_id": obj,
                        "category": "R",
                        "fields": fields[obj],
                        "product": task.object_profiles[obj].product,
                        "version": task.object_profiles[obj].version,
                        "observed": {
                            "start": raw["window_start"],
                            "end": raw["window_end"],
                            "timezone_source": "owned normal same-host UTC collector",
                        },
                    }
                    for obj in task.objects
                ],
            },
        )
        write(folder / "task.json", task.model_dump(mode="json"))
        verify_admission(folder, task)
        gold = draft_reference(case, task, folder)
        private = output / "organizer-only" / cid
        shutil.copytree(capture / "organizer-only" / cid, private / "experimental-truth")
        write(private / "case-reference-draft.json", gold.model_dump(mode="json"))
        packets = [observations(raw[k]) for k in ("packet_capture", "ue_packet_capture")]
        write(private / "packet-correspondence.json", compare(*packets))
        write(
            private / "review-instructions.json",
            {
                "status": "unreviewed domain reference draft",
                "required_human_checks": [
                    "experimental truth versus actual normal observations",
                    "version/object applicability of manual text",
                    "necessary and alternative steps and dependency sufficiency",
                    "solvability and allowed unknown exit",
                    "forbidden/unsubstantiated suggestions",
                    "raw language technical correctness",
                ],
                "manual_source_index": read(knowledge / "source-index.json"),
                "solvability_is_unapproved": True,
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
                    "review_version": "",
                    "review_source": "",
                    "notes": "",
                }
            )
        rows.append(
            {
                "case_id": cid,
                "source_group": case["source_group"],
                "structure_family": case["structure_family"],
                "parent_raw_sha256": case["original_raw_sha256"],
                "new_raw_sha256": scope.raw_sha256,
                "machine_provenance_admitted": True,
                "independent_Gold_approved": False,
                "formal_vpr": None,
            }
        )
    with (output / "organizer-only/gold-double-review.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=list(forms[0]))
        writer.writeheader()
        writer.writerows(forms)
    write(output / "index.json", rows)
    write(
        output / "summary.json",
        {
            "validation_inputs": len(rows),
            "new_independent_cases": 0,
            "normal_provenance_admitted": len(rows),
            "unreviewed_reference_drafts": len(rows),
            "actual_human_reviews": 0,
            "Gold_approved": 0,
            "heldout_inputs_read": 0,
            "formal_vpr": None,
        },
    )
    write(
        output / "sha256_manifest.json",
        {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()},
    )
    return read(output / "summary.json")


def audit(dataset, output):
    if output.exists():
        raise ValueError("fresh offline audit output required")
    rows = []
    for meta in read(dataset / "index.json"):
        cid = meta["case_id"]
        root = dataset / "cases" / cid
        task = OrchestrationTask.model_validate(read(root / "task.json"))
        contract = compile_contract(task)
        collector = MetricCollector(cid)
        tools = VerifiedDomainTools(root, task, contract, PlanBudget(task, collector))
        # Replay genuine common native dispatch; no generation or organizer answers.
        from upf_agent.agent_contracts import AgentTask, ToolCall
        from upf_agent.contracts import TaskType

        generation = digest([task.observation_files, "public-synthetic-generation"])[:20]
        agent = AgentTask(
            run_id=task.run_id,
            question=task.question,
            task_type=TaskType.DIAGNOSE,
            device_ids=[],
            log_generation=generation,
            product=task.product,
            version=task.version,
        )
        known = []
        for call in (
            ToolCall(name="analyze_log_window", arguments={"log_id": generation}),
            ToolCall(name="search_manual", arguments={"query": task.question}),
        ):
            known += tools.tool(agent, call, known, tools.budget.remaining()).evidence
        ctx = EvaluationContext.from_task(task, contract, cid)
        schema, caps, _, _ = domain_schema(task, ctx, list(tools.bindings.values()), root)
        rows.append(
            {
                "case_id": cid,
                "admitted_R": sum(
                    b.category == "R" and b.evidence_id in caps["admissible_ids"]
                    for b in tools.bindings.values()
                ),
                "admitted_K": sum(
                    b.category == "K" and b.evidence_id in caps["admissible_ids"]
                    for b in tools.bindings.values()
                ),
                "schema_sha256": digest(schema),
                "unresolved": caps["unresolved"],
            }
        )
        write(output / cid / "schema.json", schema)
    write(output / "rows.json", rows)
    summary = {
        "cases": len(rows),
        "all_normal_and_manual_evidence_available": all(
            r["admitted_R"] == 3 and r["admitted_K"] > 0 and not r["unresolved"] for r in rows
        ),
        "model_calls": 0,
        "actual_human_reviews": 0,
        "heldout_inputs_read": 0,
    }
    write(output / "summary.json", summary)
    return summary


def run_candidate(project, dataset, output, deployment):
    references = {
        r["case_id"]: CaseGold.model_validate(
            read(dataset / "organizer-only" / r["case_id"] / "case-reference-draft.json")
        )
        for r in read(dataset / "index.json")
    }
    return run(
        project,
        dataset,
        output,
        deployment,
        case_ids=list(references),
        tools_factory=VerifiedDomainTools,
        plan_generator=generate_verified_plan,
        plan_scorer=score_case,
        references=references,
        head_manifest=head_manifest(),
        p5_runner=run_verified_p5,
        extra_code_files=[
            "scripts/v8_e1_validation_closure.py",
            "scripts/v8_e1_validation_recollect.py",
        ],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "audit", "run"])
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--capture", type=Path)
    parser.add_argument("--knowledge", type=Path)
    parser.add_argument("--dataset", type=Path)
    parser.add_argument("--deployment", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        result = prepare(args.capture.resolve(), args.knowledge.resolve(), args.output.resolve())
    elif args.command == "audit":
        result = audit(args.dataset.resolve(), args.output.resolve())
    else:
        result = run_candidate(
            args.project.resolve(),
            args.dataset.resolve(),
            args.output.resolve(),
            args.deployment.resolve(),
        )
    print(json.dumps(result, ensure_ascii=False))
