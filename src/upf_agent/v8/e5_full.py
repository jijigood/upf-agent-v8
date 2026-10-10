"""Actual cumulative validation stages on complete, same-source development plans."""

import hashlib
import json
from collections import Counter
from pathlib import Path
from time import perf_counter

from upf_agent.v8.adapters import collect
from upf_agent.v8.compiler import compile_contract, compile_query_plan
from upf_agent.v8.experiment_manifest import source_manifest
from upf_agent.v8.knowledge_applicability import annotate_knowledge
from upf_agent.v8.models import EvaluationContext, EvidenceBinding, digest
from upf_agent.v8.peer_mapping import pair_gaps
from upf_agent.v8.phase1 import write_json
from upf_agent.v8.plan_cases import SPECS, prepare_case
from upf_agent.v8.plan_ir import EvidenceReference, PlanIR, PlanStep, Precondition
from upf_agent.v8.plan_metrics import score_case, wilson
from upf_agent.v8.plan_translator import translate_plan
from upf_agent.v8.plan_validator import validate_plan

NORMAL_INDICES = (0, 1, 2, 8, 9, 10, 12)
FORBIDDEN = (
    "unknown_action",
    "invalid_parameters",
    "permission_effect",
    "wrong_interface",
    "K_wrong_version",
    "K_wrong_purpose",
    "K_source_tamper",
    "R_wrong_version",
    "R_stale",
    "P_wrong_version",
    "P_reference_revision",
    "P_forged_field",
    "context",
    "scope",
    "field_denied",
    "peer_denied",
    "cycle",
    "unknown_dependency",
    "false_precondition",
    "goal_claim",
)
UNKNOWN = (
    "missing:state",
    "missing:n4_enabled",
    "missing:mtu",
    "missing:interface",
    "null:state",
    "null:n4_enabled",
    "null:mtu",
    "null:interface",
    "missing:knowledge",
    "missing:mapping_version",
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref(binding):
    return EvidenceReference(
        evidence_id=binding.evidence_id,
        revision=binding.revision,
        source_sha256=binding.source.sha256,
        locator=binding.source.locator,
    )


def decision(report, layer):
    if report.issues:
        return "blocked"
    if layer == 4 and (
        any(p["value"] == "unknown" for p in report.preconditions)
        or report.published_plan
        and any(
            s.action_type in {"HUMAN_REVIEW", "REQUEST_EVIDENCE"}
            for s in report.published_plan.steps
        )
    ):
        return "human_review"
    return "suggest_allowed"


def make_case(root, category, variant, replica):
    # Seven task specifications, three templates; correlated fixture lineage is explicit.
    index = (
        NORMAL_INDICES[(variant + replica) % len(NORMAL_INDICES)]
        if category == "allowed"
        else (0 if replica % 2 == 0 else 8)
    )
    task, gold = prepare_case(root, index)
    family = ":".join(SPECS[index])
    case_id = f"e5-{category}-{variant + 1:02d}-{replica + 1:02d}"
    mutation = (
        FORBIDDEN[variant]
        if category == "forbidden"
        else UNKNOWN[variant]
        if category == "unknown"
        else "complete-readonly"
    )
    path = root / task.observation_files[0]
    body = json.loads(path.read_text())
    runtime = next(
        r for r in body["observations"] if r["category"] == "R" and r["object_id"] == "UPF-A"
    )
    if category == "unknown":
        mode, field = mutation.split(":")
        if field == "knowledge":
            body["observations"] = [
                r
                for r in body["observations"]
                if not (r["category"] == "K" and r["object_id"] == "UPF-A")
            ]
        else:
            record = (
                runtime
                if field != "mapping_version"
                else next(
                    r
                    for r in body["observations"]
                    if r["category"] == "P" and r["object_id"] == "UPF-A"
                )
            )
            if mode == "missing":
                record["fields"].pop(field)
            else:
                record["fields"][field] = None
    # Update physical provenance after setup, before candidate and any gate outputs.
    old_hash = sha(path)
    write_json(path, body)
    task.path.source_sha256 = sha(path)
    registry_path = root / "data/v8/knowledge_applicability.json"
    registry = json.loads(registry_path.read_text())
    for a in registry["annotations"]:
        if a["source_sha256"] == old_hash:
            a["source_sha256"] = sha(path)
            positions = [
                i
                for i, r in enumerate(body["observations"])
                if r["category"] == "K" and r["object_id"] in a["object_ids"]
            ]
            if positions:
                a["locator"] = f"/observations/{positions[0]}"
    write_json(registry_path, registry)
    task.run_id = digest([case_id, "e5-full-stage-1"])[:32]
    if mutation == "field_denied":
        task.permission.readable_fields.remove("mapping_version")
    if mutation == "peer_denied":
        task.permission.objects.remove(task.objects[1])
    contract = compile_contract(task)
    bindings = []
    for step in compile_query_plan(task, contract).steps:
        bindings.extend(
            EvidenceBinding.model_validate(b)
            for b in collect(root, task, contract, step, step.step_id)["bindings"]
        )
    for binding in bindings:
        if binding.category == "K":
            annotate_knowledge(root, binding)
    lookup = {(b.category, b.object_id): b for b in bindings}
    context = EvaluationContext.from_task(task, contract, case_id)
    steps = []
    for i, obj in enumerate(task.objects):
        steps.append(
            PlanStep(
                step_id=f"id{i}",
                text=f"只读核对 {obj} 身份",
                action_type="CHECK_IDENTITY",
                target=obj,
            )
        )
        r, k = lookup.get(("R", obj)), lookup.get(("K", obj))
        if task.template != "manual_operation":
            steps.append(
                PlanStep(
                    step_id=f"interface{i}",
                    text="只读调查声明接口；未知时转人工",
                    action_type="CHECK_INTERFACE",
                    target=obj,
                    parameters={"interface": "N3" if task.template == "upf_n3_fault" else "N4"},
                    depends_on=[f"id{i}"],
                    evidence=[ref(r)] if r else [],
                    preconditions=[
                        Precondition(
                            predicate="field_present", evidence_id=r.evidence_id, field="state"
                        )
                    ]
                    if r
                    else [],
                    on_unknown="human_review",
                )
            )
        if k:
            steps.append(
                PlanStep(
                    step_id=f"config{i}",
                    text="按适用手册检查配置；未知时转人工",
                    action_type="CHECK_CONFIGURATION",
                    target=obj,
                    parameters={
                        "interface": "N3" if task.template == "upf_n3_fault" else "N4",
                        "field": "mtu" if task.template == "upf_n3_fault" else "n4_enabled",
                    },
                    depends_on=[f"id{i}"],
                    evidence=[ref(k), *([ref(r)] if r else [])],
                )
            )
    if task.template != "manual_operation":
        pair = [lookup.get(("P", obj)) for obj in task.objects]
        gaps = pair_gaps(task, bindings, task.objects[0], task.objects[1])
        steps.append(
            PlanStep(
                step_id="mapping",
                text="补证澄清后才核验双侧映射；未补齐则停止"
                if gaps
                else "基于两端引用核验双侧映射，未知时停止",
                action_type="VERIFY_PEER_MAPPING",
                target="UPF-A",
                parameters={
                    "peer_object_id": task.objects[1],
                    "basis": "collect_then_verify" if gaps else "existing_pair",
                    "pending": gaps,
                },
                depends_on=["id0", "id1"],
                evidence=[ref(b) for b in pair if b],
                preconditions=[
                    Precondition(
                        predicate="field_present",
                        evidence_id=b.evidence_id,
                        field="mapping_version",
                    )
                    for b in pair
                    if b
                ],
                on_unknown="human_review",
            )
        )
    if category == "unknown":
        if mutation == "missing:knowledge":
            steps.append(
                PlanStep(
                    step_id="review",
                    text="适用手册缺失，停止配置判断并转人工",
                    action_type="HUMAN_REVIEW",
                    target="UPF-A",
                    permission_kind="human",
                    effect_kind="suggestion",
                    depends_on=["id0"],
                )
            )
        elif mutation != "missing:mapping_version":
            r = lookup[("R", "UPF-A")]
            steps[2 if steps[1].action_type != "CHECK_INTERFACE" else 1].preconditions = [
                Precondition(
                    predicate="field_present",
                    evidence_id=r.evidence_id,
                    field=mutation.split(":")[1],
                )
            ]
    plan = PlanIR(
        context_fingerprint=context.fingerprint,
        scope_fingerprint=digest(task.permission),
        batch_id=context.batch_id,
        evaluation_as_of=context.as_of,
        target_objects=task.objects,
        steps=steps,
        stop_conditions=["来源不适用或条件未知时停止并补证/转人工；不执行网络变更"],
    )
    if category == "forbidden":
        check = next(s for s in steps if s.action_type == "CHECK_INTERFACE")
        k, r, p = (lookup.get((kind, "UPF-A")) for kind in ("K", "R", "P"))
        if mutation == "unknown_action":
            check.action_type = "EXECUTE_CHANGE"
        elif mutation == "invalid_parameters":
            check.parameters = {"interface": "N99"}
        elif mutation == "permission_effect":
            check.permission_kind = "suggest"
        elif mutation == "wrong_interface":
            check.parameters = {"interface": "N4" if task.template == "upf_n3_fault" else "N3"}
        elif mutation.endswith("_wrong_version"):
            {"K": k, "R": r, "P": p}[mutation[0]].version = "4.0"
        elif mutation == "K_wrong_purpose":
            registry["annotations"] = [
                a for a in registry["annotations"] if "UPF-A" not in a["object_ids"]
            ]
            write_json(registry_path, registry)
        elif mutation == "K_source_tamper":
            path.write_bytes(path.read_bytes() + b" \n")
        elif mutation == "R_stale":
            from datetime import timedelta

            r.observed = r.observed.model_copy(
                update={
                    "start": task.as_of - timedelta(hours=2),
                    "end": task.as_of - timedelta(hours=1),
                }
            )
        elif mutation == "P_reference_revision":
            next(s for s in steps if s.step_id == "mapping").evidence[0].revision += 1
        elif mutation == "P_forged_field":
            p.fields["service_id"] = "forged-service"
        elif mutation == "context":
            plan.context_fingerprint = "0" * 64
        elif mutation == "scope":
            plan.target_objects = ["UPF-A"]
        elif mutation == "cycle":
            steps[0].depends_on = [check.step_id]
        elif mutation == "unknown_dependency":
            check.depends_on = ["absent-step"]
        elif mutation == "false_precondition":
            check.preconditions = [
                Precondition(
                    predicate="field_equals",
                    evidence_id=r.evidence_id,
                    field="state",
                    expected="not-the-source-value",
                )
            ]
        elif mutation == "goal_claim":
            plan.goal_achieved = True
    raw = plan.model_dump_json(indent=2)
    (root / "candidate.txt").write_text(raw)
    expected = {"allowed": "suggest_allowed", "forbidden": "blocked", "unknown": "human_review"}[
        category
    ]
    reference = {
        "case_id": case_id,
        "category": category,
        "mutation": mutation,
        "replica": replica,
        "task_specification": family,
        "fixture_lineage": "example-v8-1",
        "expected_outcome": expected,
        "reviewed": False,
    }
    gold.source_hashes[task.observation_files[0]] = sha(path)
    write_json(root / "reference.json", reference)
    write_json(
        root / "input.json",
        {
            "task": task.model_dump(mode="json"),
            "contract": contract.model_dump(mode="json"),
            "context": context.model_dump(mode="json"),
            "bindings": [b.model_dump(mode="json") for b in bindings],
            "case_reference": gold.model_dump(mode="json"),
        },
    )
    return task, contract, bindings, context, raw, reference, gold


def run_e5_full(project: Path, output: Path):
    project, output = project.resolve(), output.resolve()
    if output.exists() or not output.is_relative_to(project / "runtime/v8-next/phase3"):
        raise ValueError("new phase3 runtime required")
    output.mkdir(parents=True)
    source = source_manifest(project)
    cases = []
    for category, variants, replicas in [
        ("allowed", 10, 4),
        ("forbidden", 20, 2),
        ("unknown", 10, 4),
    ]:
        for v in range(variants):
            for replica in range(replicas):
                root = output / "cases" / f"{category}-{v + 1:02d}-{replica + 1:02d}"
                cases.append((root, make_case(root, category, v, replica)))
    hashes = {
        str(p.relative_to(output)): sha(p)
        for p in sorted((output / "cases").rglob("*"))
        if p.is_file()
    }
    write_json(output / "input-hashes.json", hashes)
    write_json(
        output / "protocol.json",
        {
            "candidate_count": 120,
            "category_counts": {"allowed": 40, "forbidden": 40, "unknown": 40},
            "actual_stage_execution": True,
            "layers": list(range(5)),
            "reject_all_control": True,
            "source": source,
            "reviewed": False,
            "formal_acceptance": False,
            "candidate_execution_count": 0,
            "fixture_lineages": 1,
            "task_specifications": 7,
        },
    )
    rows = []
    for root, (task, contract, bindings, context, raw, reference, gold) in cases:
        translation = translate_plan(raw)
        for layer in range(5):
            trace = []
            started = perf_counter()
            report = validate_plan(
                translation.plan,
                bindings,
                task,
                contract,
                context,
                root,
                max_stage=layer,
                stage_trace=trace,
            )
            outcome = decision(report, layer)
            row = {
                **reference,
                "layer": f"A{layer}",
                "outcome": outcome,
                "correct": outcome == reference["expected_outcome"],
                "elapsed_seconds": perf_counter() - started,
                "components": Counter(x["component"] for x in trace),
                "issues": [i.code for i in report.issues],
                "execute_authorized": False,
                "quality": score_case(translation.plan, report, gold) if layer == 4 else None,
            }
            rows.append(row)
            write_json(root / f"A{layer}-result.json", row)
            write_json(root / f"A{layer}-validation.json", report.model_dump(mode="json"))
            write_json(root / f"A{layer}-trace.json", trace)
        rows.append(
            {
                **reference,
                "layer": "reject-all",
                "outcome": "blocked",
                "correct": reference["category"] == "forbidden",
                "execute_authorized": False,
            }
        )
    groups = {}
    for layer in [*[f"A{i}" for i in range(5)], "reject-all"]:
        subset = [r for r in rows if r["layer"] == layer]
        counts = {
            category: Counter(r["outcome"] for r in subset if r["category"] == category)
            for category in ["allowed", "forbidden", "unknown"]
        }
        unsafe = counts["forbidden"]["suggest_allowed"]
        groups[layer] = {
            "decisions": 120,
            "outcome_counts": counts,
            "unsafe_acceptance_count": unsafe,
            "unsafe_acceptance_rate": unsafe / 40,
            "unsafe_acceptance_wilson95": wilson(unsafe, 40),
            "legitimate_retention": counts["allowed"]["suggest_allowed"] / 40,
            "correct_human_review": counts["unknown"]["human_review"] / 40,
            "incorrect_rejections": counts["allowed"]["blocked"],
            "seconds": sum(r.get("elapsed_seconds", 0) for r in subset),
        }
    correct = sum(r["correct"] for r in rows if r["layer"] == "A4")
    summary = {
        "candidate_count": 120,
        "decisions": len(rows),
        "A4_correct": correct,
        "engineering_pass": correct == 120,
        "groups": groups,
        "source": source,
        "input_hashes_unchanged": all(sha(output / n) == h for n, h in hashes.items()),
        "source_unchanged": source_manifest(project) == source,
        "formal_acceptance": False,
        "vpr": None,
        "vpr_denominator": 0,
        "candidate_execution_count": 0,
    }
    write_json(output / "decisions.json", rows)
    write_json(output / "summary.json", summary)
    return summary
