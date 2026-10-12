"""Versioned engineering variants of validation normal inputs; never consume heldout."""

import argparse
import json
import shutil
from collections import Counter
from functools import partial
from pathlib import Path
from types import SimpleNamespace

from v8_e1_calibration import verify_model
from v8_e1_planning_candidate import LoopbackClient
from v8_e1_validation_packet import validation_cases

from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.e1_dataset import read, sha, write
from upf_agent.v8.e1_domain_head import domain_schema, generate_domain_plan, manifest
from upf_agent.v8.e1_domain_readonly import (
    SCOPE_VERSION,
    DomainEvidenceTools,
    DomainScope,
    NamespaceScope,
    domain_score,
    extract_normal_fields,
    translate_domain_plan,
    validate_domain_plan,
)
from upf_agent.v8.e1_formal import code_snapshot
from upf_agent.v8.experiment_metrics import MetricCollector
from upf_agent.v8.models import (
    EvaluationContext,
    EvidenceBinding,
    ObjectProfile,
    OrchestrationTask,
    PermissionScope,
    digest,
)
from upf_agent.v8.phase2 import METHODS, append_jsonl, run_method
from upf_agent.v8.plan_generator import PlanBudget

SELECTED = ["E1-CAL-N001", "E1-CAL-N002", "E1-CAL-N003"]


def prepare(dataset, output):
    if output.exists():
        raise ValueError("fresh engineering dataset required")
    sources = validation_cases(dataset.resolve())
    original_hashes, rows = {}, []
    output.mkdir(parents=True)
    for m, original_task, visible, _ in sources:
        folder = output / "cases" / m.case_id
        raw = visible / "data/raw/snapshot.json"
        target = folder / "data/raw/snapshot.json"
        target.parent.mkdir(parents=True)
        shutil.copy2(raw, target)
        original_hashes[str(raw.resolve())] = sha(raw)
        snapshot = read(raw)
        labels = list(snapshot.get("normal_probes", {"normal": snapshot.get("normal_probe")}))
        common = ["event_type", "log_excerpt", "domain_namespace"]
        scope = DomainScope(
            raw_sha256=sha(raw),
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
                    probe_ids=labels,
                    readable_fields=common
                    + ["tun_inventory", "session_probe_inventory", "packet_inventory"],
                ),
            },
        )
        write(folder / "data/domain-scope.json", scope.model_dump(mode="json"))
        fields = extract_normal_fields(folder, scope)
        task = OrchestrationTask(
            question=(
                "工程校准：根据受控5GC正常采集资料，给出UPF、RAN与UE的有界只读调查方案。"
                "UE到核心侧网关探针异常；可调查授权命名空间的隧道、filter链、已记录会话/探针与抓包。"
                "当前来源适用性与可信准入未获批准。需取得并核验材料后才能判断事实；"
                "单侧抓包不证明双侧通路，缺资料时明确补证和停止，不推断根因或已执行修复。"
            ),
            template="log_observation",
            objects=list(scope.objects),
            product="Open5GS",
            version="2.7.6",
            object_profiles={
                "upf": ObjectProfile(role="upf", product="Open5GS", version="2.7.6"),
                "ran": ObjectProfile(role="ran", product="UERANSIM", version="3.2.7"),
                "ue": ObjectProfile(role="unspecified", product="UERANSIM", version="3.2.7"),
            },
            as_of=original_task.as_of,
            synthetic=False,
            budget=original_task.budget,
            permission=PermissionScope(
                objects=list(scope.objects),
                readable_fields=sorted(
                    {f for s in scope.objects.values() for f in s.readable_fields}
                ),
                revision=f"{SCOPE_VERSION}:{digest(scope)}",
            ),
            observation_files=["data/domain-observations.json"],
        )
        observed = {
            "start": snapshot["window_start"],
            "end": snapshot["window_end"],
            "timezone_source": "original UTC controller capture interval",
        }
        write(
            folder / "data/domain-observations.json",
            {
                "source_id": m.case_id + "-normal-domain-variant-1",
                "synthetic": False,
                "corroborated": False,
                "raw_sources": {scope.raw_path: scope.raw_sha256},
                "observations": [
                    {
                        "object_id": obj,
                        "category": "R",
                        "fields": fields[obj],
                        "product": task.object_profiles[obj].product,
                        "version": task.object_profiles[obj].version,
                        "observed": observed,
                    }
                    for obj in task.objects
                ],
                "projection_status": "engineering-only; no actual review or admission approval",
            },
        )
        write(folder / "task.json", task.model_dump(mode="json"))
        rows.append(
            {
                "case_id": m.case_id,
                "source_split": "validation",
                "variant_scope": "engineering-only",
                "original_raw_sha256": sha(raw),
                "source_group": m.source_group,
                "structure_family": m.structure_family,
                "explicit_UE_permission_revision": task.permission.revision,
                "normal_filter_counters_available": "filter_inventory" in fields["upf"],
                "independent_UE_capture_available": "packet_inventory" in fields["ue"],
                "corroborated": False,
                "Gold_created": False,
            }
        )
    assert all(sha(Path(name)) == value for name, value in original_hashes.items())
    write(output / "source-inputs-sha256.json", original_hashes)
    write(output / "index.json", rows)
    result = {
        "engineering_variants": len(rows),
        "original_cases_modified": 0,
        "normal_filter_sources": sum(r["normal_filter_counters_available"] for r in rows),
        "independent_UE_captures": sum(r["independent_UE_capture_available"] for r in rows),
        "actual_human_reviews": 0,
        "approved_Gold": 0,
        "heldout_inputs_read": 0,
        "new_model_calls": 0,
    }
    write(output / "summary.json", result)
    write(
        output / "sha256_manifest.json",
        {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()},
    )
    return result


def audit_inputs(dataset, output):
    if output.exists():
        raise ValueError("fresh input audit required")
    for name, value in read(dataset / "sha256_manifest.json").items():
        assert sha(dataset / name) == value
    output.mkdir(parents=True)
    rows = []
    for meta in read(dataset / "index.json"):
        folder = dataset / "cases" / meta["case_id"]
        task = OrchestrationTask.model_validate(read(folder / "task.json"))
        contract = compile_contract(task)
        collector = MetricCollector(task.run_id)
        tools = DomainEvidenceTools(folder, task, contract, PlanBudget(task, collector))
        context = EvaluationContext.from_task(task, contract, "domain-input-audit")
        schema, caps, scope, _ = domain_schema(task, context, list(tools.bindings.values()), folder)
        write(output / meta["case_id"] / "schema.json", schema)
        row = {
            "case_id": meta["case_id"],
            "schema_sha256": digest(schema),
            "admitted_evidence": len(caps["admissible_ids"]),
            "shared_readbacks": tools.shared_readbacks,
            "offline_tool_attempts": collector.summary()["invocations"]["tool"]["attempted"],
            "actions_by_object": {
                obj: sorted(
                    {
                        b["properties"]["action_type"]["const"]
                        for b in schema["$defs"]["PlanStep"]["anyOf"]
                        if b["properties"]["target"]["const"] == obj
                    }
                )
                for obj in task.objects
            },
            "ran_domain_fields": scope.objects["ran"].readable_fields,
        }
        rows.append(row)
    write(output / "rows.json", rows)
    result = {
        "cases": len(rows),
        "offline_tool_attempts": sum(r["offline_tool_attempts"] for r in rows),
        "all_sources_remain_unapproved": all(r["admitted_evidence"] == 0 for r in rows),
        "new_model_calls": 0,
        "heldout_inputs_read": 0,
    }
    write(output / "summary.json", result)
    write(
        output / "sha256_manifest.json",
        {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()},
    )
    return result


def run(
    project,
    dataset,
    output,
    deployment,
    *,
    case_ids=None,
    tools_factory=DomainEvidenceTools,
    plan_generator=generate_domain_plan,
    plan_scorer=domain_score,
    references=None,
    head_manifest=None,
    extra_code_files=(),
    p5_runner=None,
):
    if output.exists():
        raise ValueError("fresh candidate run required")
    receipt = read(deployment)
    print("verifying actual model files and unchanged serving process", flush=True)
    verify_model(project, receipt)
    for name, expected in read(dataset / "sha256_manifest.json").items():
        assert sha(dataset / name) == expected
    code = code_snapshot(project)
    selected = SELECTED if case_ids is None else case_ids
    head = manifest() if head_manifest is None else head_manifest
    for name in [
        "scripts/v8_e1_domain_readonly.py",
        "scripts/v8_e1_planning_candidate.py",
        "scripts/v8_e1_validation_packet.py",
        "scripts/v8_e1_calibration.py",
    ]:
        code["files"][name] = sha(project / name)
    for name in extra_code_files:
        code["files"][name] = sha(project / name)
    code["sha256"] = digest(code["files"])
    output.mkdir(parents=True)
    for name in code["files"]:
        target = output / "code" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(project / name, target)
    cases = []
    order = [METHODS[0], METHODS[2], METHODS[1], METHODS[3]]
    for i, cid in enumerate(selected):
        source = dataset / "cases" / cid
        task = OrchestrationTask.model_validate(read(source / "task.json"))
        frozen = output / "frozen-inputs" / cid
        shutil.copytree(source, frozen)
        cases.append(
            {
                "case_id": cid,
                "task": task.model_dump(mode="json"),
                "method_order": order[i % 4 :] + order[: i % 4],
            }
        )
    inputs = {
        str(p.relative_to(output / "frozen-inputs")): sha(p)
        for p in (output / "frozen-inputs").rglob("*")
        if p.is_file()
    }
    write(
        output / "protocol.json",
        {
            "kind": "domain-readonly-engineering-validation",
            "head": head,
            "cases": cases,
            "code": code,
            "input_hashes": inputs,
            "model_receipt": receipt,
            "planned_method_runs": len(selected) * len(METHODS),
            "method_order": "preregistered four-method Latin rotation by case index",
            "shared_domain_reads_per_run": 2 if tools_factory is DomainEvidenceTools else 0,
            "shared_reads_charged_before_native_method": True,
            "budget": {"models": 8, "tools": 8, "rounds": 3, "seconds": 180},
            "formal_vpr_enabled": False,
            "Gold_used_for_generation": False,
            "source_admission_flags_changed": False,
            "heldout_consumed": False,
        },
    )
    factory = partial(LoopbackClient, grammar_python=receipt["server_command"][0])
    rows = []
    for meta in cases:
        for method in meta["method_order"]:
            cid = meta["case_id"]
            task = OrchestrationTask.model_validate(meta["task"])
            folder = output / "runs" / cid / f"method-{METHODS.index(method) + 1}"
            folder.mkdir(parents=True)
            try:
                # Metadata adapter only; no CaseGold or reference branches are created/read.
                metadata = SimpleNamespace(case_id=cid) if references is None else references[cid]
                row = run_method(
                    project,
                    output / "frozen-inputs" / cid,
                    folder,
                    task,
                    metadata,
                    method,
                    factory,
                    tools_factory=tools_factory,
                    calibration_candidate=True,
                    plan_generator=plan_generator,
                    plan_translator=translate_domain_plan,
                    plan_validator=validate_domain_plan,
                    plan_scorer=plan_scorer,
                    p5_runner=p5_runner,
                )
                cost = read(folder / "metrics.json")
                parsed = translate_domain_plan((folder / "raw-plan.txt").read_text()).plan
                context = EvaluationContext.model_validate(read(folder / "context.json"))
                frozen_task = OrchestrationTask.model_validate(read(folder / "task.json"))
                bindings = [
                    EvidenceBinding.model_validate(b) for b in read(folder / "bindings.json")
                ]
                checked = validate_domain_plan(
                    parsed,
                    bindings,
                    frozen_task,
                    compile_contract(frozen_task),
                    context,
                    folder / "runtime",
                )
                assert checked.model_dump(mode="json") == read(folder / "validation.json")
                row.update(
                    model_attempts=cost["invocations"]["model"]["attempted"],
                    tool_attempts=cost["invocations"]["tool"]["attempted"],
                    input_tokens=cost["token_usage"]["input"],
                    output_tokens=cost["token_usage"]["output"],
                    actions=[(s.action_type, s.target) for s in parsed.steps] if parsed else [],
                    runner_error=None,
                )
            except Exception as exc:
                row = {
                    "case_id": cid,
                    "method": method,
                    "parsed": False,
                    "validator_pass": False,
                    "reference_pass": None,
                    "vpr": None,
                    "actions": [],
                    "runner_error": f"{type(exc).__name__}:{exc}",
                    "model_attempts": None,
                    "tool_attempts": None,
                    "input_tokens": None,
                    "output_tokens": None,
                }
            row.update(
                split="engineering_validation",
                reviewed=False,
                formal_vpr=None,
                reference_scoring_enabled=references is not None,
                head=head["version"],
            )
            write(folder / "case-metrics.json", row)
            append_jsonl(output / "metrics-by-case.jsonl", row)
            rows.append(row)
            print(
                json.dumps(
                    {
                        k: row.get(k)
                        for k in [
                            "case_id",
                            "method",
                            "parsed",
                            "validator_pass",
                            "issues",
                            "runner_error",
                        ]
                    }
                ),
                flush=True,
            )
    result = {
        "planned_method_runs": len(selected) * len(METHODS),
        "recorded_method_runs": len(rows),
        "parsed": sum(r["parsed"] for r in rows),
        "validator_passes": sum(r["validator_pass"] for r in rows),
        "runner_errors": sum(r["runner_error"] is not None for r in rows),
        "actual_model_attempts_known": sum(r["model_attempts"] or 0 for r in rows),
        "unknown_cost_runs": sum(r["model_attempts"] is None for r in rows),
        "issues": dict(Counter(issue for r in rows for issue in r.get("issues", []))),
        "source_unchanged": all(sha(project / n) == v for n, v in code["files"].items())
        and all(sha(output / "frozen-inputs" / n) == v for n, v in inputs.items()),
        "actual_human_reviews": 0,
        "formal_vpr": None,
        "formal_e1_completed": False,
        "heldout_inputs_read": 0,
    }
    write(output / "summary.json", result)
    write(
        output / "sha256_manifest.json",
        {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()},
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "audit-inputs", "run"])
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dataset", type=Path, default=Path("eval/v8/e1"))
    parser.add_argument("--deployment", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        result = prepare(args.dataset.resolve(), args.output.resolve())
    elif args.command == "audit-inputs":
        result = audit_inputs(args.dataset.resolve(), args.output.resolve())
    else:
        if args.deployment is None:
            parser.error("run requires --deployment")
        result = run(
            args.project.resolve(),
            args.dataset.resolve(),
            args.output.resolve(),
            args.deployment.resolve(),
        )
    print(json.dumps(result, ensure_ascii=False))
