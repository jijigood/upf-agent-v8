"""Reported omissions, conditional investigation, roles, and source-window substitution."""

import json
from datetime import timedelta
from types import SimpleNamespace

import pytest

from upf_agent.v8.adapters import collect
from upf_agent.v8.compiler import compile_contract, compile_query_plan
from upf_agent.v8.graph import GraphNode, compile_graph_query, exclusion
from upf_agent.v8.models import EvaluationContext, EvidenceBinding, OrchestrationTask, digest
from upf_agent.v8.peer_mapping import pair_gaps
from upf_agent.v8.plan_capabilities import compile_capabilities
from upf_agent.v8.plan_cases import prepare_case
from upf_agent.v8.plan_generator import generation_schema, visible_evidence
from upf_agent.v8.plan_ir import EvidenceReference, PlanIR, PlanStep
from upf_agent.v8.plan_validator import validate_plan
from upf_agent.v8.review_evidence import source_review


def setup(root, index=0):
    task, gold = prepare_case(root, index)
    contract = compile_contract(task)
    bindings = [
        EvidenceBinding.model_validate(b)
        for s in compile_query_plan(task, contract).steps
        for b in collect(root, task, contract, s, s.step_id)["bindings"]
    ]
    context = EvaluationContext.from_task(task, contract, "remediation")
    pair = [b for b in bindings if b.category == "P"]
    plan = PlanIR(
        context_fingerprint=context.fingerprint,
        scope_fingerprint=digest(task.permission),
        batch_id=context.batch_id,
        evaluation_as_of=context.as_of,
        target_objects=task.objects,
        steps=[
            PlanStep(step_id=f"id{i}", text="核对身份", action_type="CHECK_IDENTITY", target=obj)
            for i, obj in enumerate(task.objects)
        ]
        + [
            PlanStep(
                step_id="pair",
                text="核验所引用双侧映射",
                action_type="VERIFY_PEER_MAPPING",
                target=task.objects[0],
                parameters={"peer_object_id": task.objects[1]},
                depends_on=["id0", "id1"],
                evidence=[EvidenceReference(**visible_evidence(b)["citation"]) for b in pair],
            )
        ],
        stop_conditions=["缺侧或冲突则停止；不授权执行"],
    )
    return task, gold, contract, bindings, context, plan


def report(root, items):
    task, _, contract, bindings, context, plan = items
    return validate_plan(plan, bindings, task, contract, context, root)


def test_existing_pair_requires_both_citations_and_identity_reachability(tmp_path):
    items = setup(tmp_path / "case")
    assert report(tmp_path / "case", items).raw_plan_validity
    pair = items[-1].steps[-1]
    original = list(pair.evidence)
    pair.evidence = original[:1]
    assert "peer_mapping_basis_incomplete" in {
        i.code for i in report(tmp_path / "case", items).issues
    }
    pair.evidence = [original[0], original[0]]
    assert "duplicate_mapping_citation" in {i.code for i in report(tmp_path / "case", items).issues}
    pair.evidence = original
    pair.depends_on = ["id0"]
    assert "bilateral_identity_dependency_missing" in {
        i.code for i in report(tmp_path / "case", items).issues
    }


@pytest.mark.parametrize("index", [7, 17, 18, 20, 21, 22, 23])
def test_missing_or_conflicting_pair_has_explicit_conditional_outlet(tmp_path, index):
    root = tmp_path / "case"
    items = setup(root, index)
    task, _, _, bindings, context, plan = items
    caps = compile_capabilities(task, context, bindings, root)
    admitted = [b for b in bindings if b.evidence_id in caps["admissible_ids"]]
    gaps = pair_gaps(task, admitted, task.objects[0], task.objects[1])
    assert gaps
    pair = plan.steps[-1]
    pair.parameters.update(basis="collect_then_verify", pending=gaps)
    pair.text = "澄清双侧缺口后才核验，未补齐则停止"
    pair.evidence = [
        EvidenceReference(**visible_evidence(b)["citation"]) for b in admitted if b.category == "P"
    ]
    assert report(root, items).raw_plan_validity
    pair.parameters["pending"] = ["invented:gap"]
    assert "conditional_mapping_gap_mismatch" in {i.code for i in report(root, items).issues}


def test_conditional_mode_cannot_hide_a_complete_pair_or_forged_reference(tmp_path):
    root = tmp_path / "case"
    items = setup(root)
    pair = items[-1].steps[-1]
    pair.parameters.update(basis="collect_then_verify", pending=["invented:gap"])
    assert "conditional_mapping_gap_mismatch" in {i.code for i in report(root, items).issues}
    pair.parameters = {"peer_object_id": items[0].objects[1]}
    pair.evidence[1].revision += 1
    assert "evidence_reference_mismatch" in {i.code for i in report(root, items).issues}


@pytest.mark.parametrize("index", [0, 8, 12])
def test_profiles_do_not_borrow_upf_product_or_version_for_peer(tmp_path, index):
    root = tmp_path / "case"
    task, gold, contract, bindings, context, plan = setup(root, index)
    peer = task.objects[1]
    assert task.object_profiles[peer].product != task.product
    assert task.object_profiles[peer].version != task.version
    assert all(b.version == task.object_profiles[b.object_id].version for b in bindings)
    caps = compile_capabilities(task, context, bindings, root)
    assert not caps["unresolved"]
    if index == 8:
        assert peer == "RAN-B" and task.object_profiles[peer].role == "ran"
        assert report(root, (task, gold, contract, bindings, context, plan)).raw_plan_validity
        task.object_profiles[peer].role = "smf"
        context = EvaluationContext.from_task(task, compile_contract(task), "remediation")
        plan.context_fingerprint = context.fingerprint
        assert "peer_role_mismatch" in {
            i.code
            for i in validate_plan(
                plan, bindings, task, compile_contract(task), context, root
            ).issues
        }


def test_graph_accepts_declared_heterogeneous_versions_and_refuses_wrong_peer_version(tmp_path):
    task, _, contract, bindings, _, _ = setup(tmp_path / "case", 8)
    pair = next(b for b in bindings if b.object_id == "RAN-B" and b.category == "P")
    node = GraphNode(
        node_id="peer",
        kind="EvidenceBinding",
        layer="runtime",
        object_ids=[pair.object_id],
        source=pair.source,
        version=pair.version,
        synthetic=True,
        attributes={"binding": pair.model_dump(mode="json")},
    )
    query = compile_graph_query(task, contract.contract_id, [node.node_id])
    assert exclusion(node, query) is None
    node.version = "5.0"
    assert exclusion(node, query) == "wrong_version"


def test_legacy_task_fingerprint_does_not_gain_an_empty_profile_field(tmp_path):
    task, *_ = setup(tmp_path / "case")
    raw = task.model_dump(mode="json")
    raw.pop("object_profiles")
    old = OrchestrationTask.model_validate(raw)
    assert old.model_dump(mode="json") == raw
    assert digest(old) == digest(raw)


@pytest.mark.parametrize("window", ["observed", "valid"])
def test_review_cannot_replace_binding_window_with_fresh_source_window(tmp_path, window):
    root = tmp_path / "case"
    task, _, _, bindings, _, _ = setup(root)
    binding = next(b for b in bindings if b.category == "R")
    assert source_review(root, binding, task) == []
    if window == "observed":
        binding.observed = binding.observed.model_copy(
            update={
                "start": task.as_of - timedelta(hours=2),
                "end": task.as_of - timedelta(hours=1),
            }
        )
    else:
        from upf_agent.contracts import TimeWindow

        binding.valid = TimeWindow(
            start=task.as_of - timedelta(hours=2),
            end=task.as_of - timedelta(hours=1),
            timezone_source="UTC",
        )
    findings = source_review(root, binding, task)
    assert f"source_{window}_mismatch" in findings
    assert "binding_stale_observation" in findings or "binding_outside_validity" in findings


def test_generation_grammar_requires_distinct_sides_when_available(tmp_path):
    root = tmp_path / "case"
    task, _, _, bindings, context, _ = setup(root)
    caps = compile_capabilities(task, context, bindings, root)
    schema = generation_schema(
        bindings, {"target_objects": task.objects}, capabilities=caps, task=task
    )
    slot = next(
        s
        for s in schema["properties"]["steps"]["prefixItems"]
        if s.get("properties", {}).get("action_type", {}).get("const") == "VERIFY_PEER_MAPPING"
    )
    evidence = slot["properties"]["evidence"]
    assert evidence["minItems"] == evidence["maxItems"] == 2
    first, second = [
        set(x["const"]["evidence_id"] for x in s["anyOf"]) for s in evidence["prefixItems"]
    ]
    assert first and second and not first & second
    assert "case-reference" not in json.dumps(schema)


@pytest.mark.parametrize("index", range(12, 16))
def test_manual_scope_and_review_branch_keep_available_investigations(tmp_path, index):
    task, gold = prepare_case(tmp_path / "case", index)
    assert "本任务不要求双侧映射调查" in task.question
    assert all(
        not any(p.action_type == "VERIFY_PEER_MAPPING" for p in b.required) for b in gold.any_of
    )
    if len(gold.any_of) > 1:
        assert all(any(p.action_type == "CHECK_IDENTITY" for p in b.required) for b in gold.any_of)


@pytest.mark.parametrize("number", [48, 60, 63, 66, 69, 72, 84, 87, 90, 93])
def test_e2_runtime_queries_express_the_structured_need_and_source_controls(tmp_path, number):
    from upf_agent.v8.e2 import prepare_query

    chunk = SimpleNamespace(
        product="UPF",
        version="5.0",
        token_count=20,
        section_path=["接口配置"],
        text="只读核对接口配置",
        chunk_id="c1",
        source_id="manual",
        parent_id="section",
        locators=["paragraph:1"],
    )
    case = prepare_query(tmp_path, {chunk.chunk_id: chunk}, number)
    assert case["task"].question == case["text"]
    assert all(field in case["text"] for field in case["requirement"].fields)
    assert "UPF-A" in case["text"]
    if case["kind"] == "P":
        assert all(obj in case["text"] for obj in case["task"].objects)
        assert "service-001" in case["text"] and "map-1" in case["text"]
        assert "不能由单侧宣称双侧一致" in case["text"]
    else:
        assert "300秒" in case["text"] and "手册不能代替现场观察" in case["text"]
    assert case["relevance_scope"] == "runtime_mapping_clues"
    assert not case["reference_reviewed"]


def test_e2_section_fragments_are_not_approved_equivalent_complete_procedures(tmp_path):
    from upf_agent.v8.e2 import prepare_query

    common = dict(
        product="UPF",
        version="5.0",
        token_count=20,
        section_path=["接口配置"],
        source_id="manual",
        parent_id="section",
    )
    chunks = {
        "c1": SimpleNamespace(**common, chunk_id="c1", text="核对版本", locators=["p1"]),
        "c2": SimpleNamespace(**common, chunk_id="c2", text="核对接口", locators=["p2"]),
    }
    case = prepare_query(tmp_path, chunks, 0)
    assert set(case["related_fragments"]) == {"c1", "c2"}
    assert case["equivalent_complete_operation_sets"] is None
    assert {tuple(f["locators"]) for f in case["fragment_support"]} == {("p1",), ("p2",)}
    assert all(not f["complete_operation_approval"] for f in case["fragment_support"])
