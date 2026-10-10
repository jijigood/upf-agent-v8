import importlib.util
import json
from pathlib import Path

import pytest

from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.e5_full import FORBIDDEN, UNKNOWN, decision, make_case
from upf_agent.v8.models import EvaluationContext, EvidenceBinding, OrchestrationTask
from upf_agent.v8.plan_translator import translate_plan
from upf_agent.v8.plan_validator import validate_plan


@pytest.mark.parametrize(
    "category,variant",
    [
        *[("allowed", i) for i in range(10)],
        *[("forbidden", i) for i in range(len(FORBIDDEN))],
        *[("unknown", i) for i in range(len(UNKNOWN))],
    ],
)
def test_complete_same_source_controls_have_expected_final_outlets(tmp_path, category, variant):
    root = tmp_path / "case"
    task, contract, bindings, context, raw, reference, _ = make_case(root, category, variant, 0)
    plan = translate_plan(raw).plan
    report = validate_plan(plan, bindings, task, contract, context, root)
    assert decision(report, 4) == reference["expected_outcome"]
    assert not report.execute_authorized
    if category == "allowed":
        assert report.published_plan_validity
        assert {"CHECK_IDENTITY", "CHECK_CONFIGURATION"} <= {s.action_type for s in plan.steps}
        if task.template != "manual_operation":
            assert "VERIFY_PEER_MAPPING" in {s.action_type for s in plan.steps}


def test_partial_layers_execute_components_only_when_enabled(tmp_path, monkeypatch):
    import upf_agent.v8.plan_validator as module

    task, contract, bindings, context, raw, _, _ = make_case(tmp_path / "case", "allowed", 0, 0)
    plan = translate_plan(raw).plan
    original = module.verify_plan_source
    calls = []

    def checked(*args):
        calls.append(args[1].category)
        return original(*args)

    monkeypatch.setattr(module, "verify_plan_source", checked)
    for stage in range(5):
        calls.clear()
        trace = []
        report = validate_plan(
            plan,
            bindings,
            task,
            contract,
            context,
            tmp_path / "case",
            max_stage=stage,
            stage_trace=trace,
        )
        assert bool(calls) == (stage >= 2)
        assert all(t["stage"] <= stage for t in trace)
        assert ("dependency_DAG" in {t["component"] for t in trace}) == (stage == 4)
        assert not report.execute_authorized
        if stage < 4:
            assert report.published_plan is None


@pytest.mark.parametrize(
    "category,variant",
    [
        ("allowed", 0),
        ("allowed", 6),
        ("forbidden", 6),
        ("forbidden", 14),
        ("forbidden", 16),
        ("unknown", 8),
    ],
)
def test_unaffected_frozen_candidates_keep_decisions_and_issues(category, variant):
    project = Path(__file__).resolve().parents[1]
    path = (
        project
        / "runtime/v8-next/phase3/all-experiments-start-freeze-001/worktree"
        / "src/upf_agent/v8/plan_validator.py"
    )
    if not path.exists():
        pytest.skip("historical local evidence is not shipped with public tests")
    spec = importlib.util.spec_from_file_location("old_validator_for_comparison", path)
    previous = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(previous)
    root = project / f"runtime/v8-next/phase3/e5-full-002/cases/{category}-{variant + 1:02d}-01"
    if not root.exists():
        pytest.skip("historical local evidence is not shipped with public tests")
    inputs = json.loads((root / "input.json").read_text())
    task = OrchestrationTask.model_validate(inputs["task"])
    contract = compile_contract(task)
    bindings = [EvidenceBinding.model_validate(b) for b in inputs["bindings"]]
    context = EvaluationContext.model_validate(inputs["context"])
    raw = (root / "candidate.txt").read_text()
    plan = translate_plan(raw).plan
    current = validate_plan(plan, bindings, task, contract, context, root).model_dump()
    historical = previous.validate_plan(plan, bindings, task, contract, context, root).model_dump()
    assert current.pop("validator_version") == "v8-plan-validator-2"
    historical.pop("validator_version")
    old_codes = {(i["code"], i["step_id"]) for i in historical.pop("issues")}
    new_codes = {(i["code"], i["step_id"]) for i in current.pop("issues")}
    assert old_codes <= new_codes
    assert {code for code, _ in new_codes - old_codes} <= {
        "peer_mapping_basis_incomplete",
        "peer_mapping_conflict_or_gap",
    }
    assert current == historical
