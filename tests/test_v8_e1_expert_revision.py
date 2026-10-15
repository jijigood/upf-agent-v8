"""Document semantics and larger injective references, using synthetic controls only."""

import hashlib
import json
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.e1_expert_revision import (
    ACTIONS,
    REGISTRY,
    ManualParams,
    public_step_options,
    translate_revision,
)
from upf_agent.v8.e1_formal import runner_options
from upf_agent.v8.evaluator import EvidenceSnapshot, evaluate_requirement
from upf_agent.v8.models import EvidenceBinding, OrchestrationTask, PermissionScope, SourcePointer
from upf_agent.v8.plan_ir import ActionPattern, CaseGold, GoldBranch, PlanIR, PlanStep
from upf_agent.v8.plan_metrics import score_case


def state(*, template="runtime_investigation", same_location=False, missing=False):
    now = datetime(2026, 10, 13, tzinfo=UTC)
    task = OrchestrationTask(
        question="synthetic source-collection control",
        template=template,
        objects=["obj"],
        product="Unit",
        version="1",
        as_of=now,
        synthetic=True,
        permission=PermissionScope(objects=["obj"], readable_fields=["instruction"]),
    )
    contract = compile_contract(task)
    req = next(r for r in contract.requirements if r.kind == "K")
    bindings = [
        EvidenceBinding(
            evidence_id=f"e{i}",
            native_id=f"n{i}",
            receipt_id=f"unit-receipt-{i}",
            task_id=task.run_id,
            contract_id=contract.contract_id,
            requirement_id=req.requirement_id,
            object_id="obj",
            category="K",
            fields={"instruction": ("" if missing else f"different paragraph {i}")},
            source=SourcePointer(
                source_id="unit", sha256="a" * 64, locator="same" if same_location else f"loc{i}"
            ),
            product="Unit",
            version="1",
            purposes=[template],
            readable=True,
            source_verified=True,
            synthetic=True,
            corroborated=True,
        )
        for i in (1, 2)
    ]
    return evaluate_requirement(req, task, contract, EvidenceSnapshot(bindings), {}, "unit", now)


def test_distinct_original_paragraphs_are_collection_not_semantic_approval():
    result = state()
    assert result.code.value == "satisfied"
    assert result.basis["document_collections"]["obj"]["semantic_approval"] is False
    assert result.basis["document_collections"]["obj"]["distinct_original_locations"] == 2


def test_same_original_location_disagreement_stays_conflict():
    assert state(same_location=True).code.value == "conflict"


def test_legacy_manual_values_still_require_agreement():
    assert state(template="manual_operation").code.value == "conflict"


def test_empty_paragraph_does_not_satisfy_source_requirement():
    assert state(missing=True).code.value == "missing"


@pytest.mark.parametrize("extra", [{"execute": True}, {"n4_enabled": True}, {"locator": "fake"}])
def test_readonly_manual_parameters_cannot_grant_other_fields(extra):
    with pytest.raises(ValueError):
        ManualParams.model_validate(
            {"product": "Unit", "version": "1", "purpose": "runtime_investigation", **extra}
        )
    assert ACTIONS["READ_MANUAL_REFERENCE"][3:] == (["instruction"], True)


def large_reference(remove=False):
    now = datetime(2026, 10, 13, tzinfo=UTC)
    patterns = [
        ActionPattern(pattern_id=f"p{i}", action_type="READ_LOG", target=f"o{i}") for i in range(15)
    ]
    gold = CaseGold(
        case_id="unit",
        source_group="unit",
        structure_family="unit",
        source_level="D1",
        synthetic=True,
        solvability="needs_evidence",
        objects=[f"o{i}" for i in range(15)],
        version="1",
        as_of=now,
        permission_fingerprint="unit",
        visible_evidence=[],
        source_hashes={},
        any_of=[GoldBranch(branch_id="large", required=patterns)],
        stop_conditions=["unit"],
    )
    steps = [
        PlanStep(step_id=f"s{i}", action_type="READ_LOG", target=f"o{i}", text="unit")
        for i in range(14 if remove else 15)
    ]
    plan = PlanIR(
        context_fingerprint="unit",
        scope_fingerprint="unit",
        batch_id="unit",
        evaluation_as_of=now,
        target_objects=gold.objects,
        steps=steps,
        stop_conditions=["unit"],
    )
    checked = SimpleNamespace(
        raw_plan_validity=True,
        published_plan_validity=True,
        issues=[],
        retained_steps=len(steps),
        rejected_steps=0,
        rewritten_steps=0,
    )
    return score_case(plan, checked, gold)


def test_complete_fifteen_step_match_does_not_exhaust_on_skipping_alternatives():
    result = large_reference()
    assert result["reference_pass"] and not result["branch"]["matching_exhausted"]
    assert result["vpr"] is None


def test_missing_step_in_large_reference_remains_failure_without_exhaustion():
    result = large_reference(remove=True)
    assert not result["reference_pass"] and result["branch"]["matched"] == 14
    assert not result["branch"]["matching_exhausted"]


def test_new_formal_profile_is_explicit_and_preserves_legacy():
    options, manifest = runner_options("expert-readonly-revision-1")
    assert (
        manifest["registry_version"] == REGISTRY
        and options["plan_validator"].__name__ == "validate_revision"
    )
    assert runner_options("legacy")[1]["version"] != manifest["version"]


def wire_control():
    return {
        "registry_version": REGISTRY,
        "context_fingerprint": "unit",
        "scope_fingerprint": "unit",
        "batch_id": "unit",
        "evaluation_as_of": "2026-10-13T00:00:00+00:00",
        "target_objects": ["obj"],
        "identity_source_admission_sha256": "0" * 64,
        "citation_table": {
            "c1": {
                "evidence_id": "raw-receipt",
                "revision": 1,
                "source_sha256": "a" * 64,
                "locator": "raw:1",
            }
        },
        "steps": [
            {
                "step_id": "a1",
                "action_type": "READ_LOG",
                "target": "obj",
                "text": "核对日志",
                "evidence": ["c1"],
            }
        ],
        "stop_conditions": ["unit"],
    }


def test_wire_reference_resolution_uses_only_explicit_raw_table():
    value = wire_control()
    raw = json.dumps(value, ensure_ascii=False)
    translated = translate_revision(raw)
    assert translated.plan.steps[0].evidence[0].model_dump() == value["citation_table"]["c1"]
    assert translated.raw_sha256 == hashlib.sha256(raw.encode()).hexdigest()
    assert translated.cost_model_calls == 0
    assert raw[translated.spans[0].text_start : translated.spans[0].text_end] == '"核对日志"'


@pytest.mark.parametrize("fault", ["missing_table", "unknown_key", "invalid_hash"])
def test_wire_cannot_resolve_absent_or_corrupt_table(fault):
    value = wire_control()
    if fault == "missing_table":
        value.pop("citation_table")
    elif fault == "unknown_key":
        value["steps"][0]["evidence"] = ["absent"]
    else:
        value["citation_table"]["c1"]["source_sha256"] = "invalid"
    assert translate_revision(json.dumps(value)).plan is None


def test_duplicate_raw_table_keys_still_fail_lossless_translation():
    raw = json.dumps(wire_control())
    raw = raw.replace('"c1": {', '"c1": {}, "c1": {', 1)
    assert translate_revision(raw).plan is None


def test_validated_metadata_assignment_preserves_typed_steps():
    translated = translate_revision(json.dumps(wire_control()))
    plan = translated.plan
    plan.identity_source_admission_sha256 = "b" * 64
    plan.goal_achieved = False
    assert isinstance(plan.steps[0], PlanStep)
    assert plan.steps[0].evidence[0].evidence_id == "raw-receipt"


def test_short_ids_expose_direction_and_both_existing_or_pending_variants():
    def choice(sid, chain, basis):
        return {
            "properties": {
                "step_id": {"const": sid},
                "action_type": {"const": "READ_FILTER_COUNTERS"},
                "target": {"const": "upf"},
                "parameters": {
                    "properties": {
                        "chain": {"const": chain},
                        "basis": {"const": basis},
                    }
                },
            }
        }

    schema = {
        "properties": {"steps": {"prefixItems": []}},
        "$defs": {
            "PlanStep": {
                "anyOf": [
                    choice("a1", "INPUT", "inspect_existing"),
                    choice("a2", "OUTPUT", "inspect_existing"),
                    choice("a2", "OUTPUT", "collect_then_check"),
                ]
            }
        },
    }
    options = public_step_options(schema)
    assert len(options) == 3
    assert options[0]["fixed_parameters"]["chain"] == "INPUT"
    assert [o["fixed_parameters"] for o in options if o["step_id"] == "a2"] == [
        {"chain": "OUTPUT", "basis": "inspect_existing"},
        {"chain": "OUTPUT", "basis": "collect_then_check"},
    ]
