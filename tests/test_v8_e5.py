import ast
from pathlib import Path

import pytest

from upf_agent.v8.e5 import FORBIDDEN, LAYERS, _case, policy_decision, run_e5
from upf_agent.v8.plan_translator import translate_plan
from upf_agent.v8.plan_validator import PlanValidationReport, ValidationIssue, validate_plan


@pytest.mark.parametrize("category", ["allowed", "forbidden", "unknown"])
@pytest.mark.parametrize("variant", range(8))
@pytest.mark.parametrize("replica", [0, 1])
def test_physically_sourced_controls_keep_legal_deny_violations_defer_unknown(
    tmp_path, category, variant, replica
):
    root = tmp_path / "case"
    task, contract, bindings, context, raw, reference = _case(
        root, "test", category, variant, replica
    )
    translated = translate_plan(raw)
    report = validate_plan(translated.plan, bindings, task, contract, context, root)
    decision = policy_decision(report, 4)
    assert decision["outcome"] == reference["expected_outcome"]
    assert not decision["execute_authorized"] and not report.execute_authorized
    assert report.rewritten_steps == 0
    assert (root / "candidate.txt").read_text() == raw
    assert report.raw_plan_validity is (category != "forbidden")
    unknown_conditions = any(p["value"] == "unknown" for p in report.preconditions)
    # Tampered/wrong-version sources also make predicates unknown; hard violations win.
    expected_unknown = category == "unknown" or (
        category == "forbidden" and FORBIDDEN[variant] in {"source_tamper", "wrong_version"}
    )
    assert unknown_conditions is expected_unknown
    decisions = [policy_decision(report, layer) for layer in range(5)]
    if category == "allowed":
        assert all(d["outcome"] == "suggest_allowed" for d in decisions)
    elif category == "forbidden":
        first_block = next(i for i, d in enumerate(decisions) if d["outcome"] == "blocked")
        assert all(d["outcome"] == "blocked" for d in decisions[first_block:])
        expected = {
            "unknown_action": 1,
            "source_tamper": 2,
            "wrong_version": 2,
            "context": 3,
            "scope": 3,
            "execution_claim": 4,
            "cycle": 4,
            "false_precondition": 4,
        }[FORBIDDEN[variant]]
        assert first_block == expected
    else:
        assert all(d["outcome"] == "suggest_allowed" for d in decisions[:4])


def test_layer_classification_covers_existing_diagnostics_without_duplicates():
    import upf_agent.v8.plan_validator as module

    tree = ast.parse(Path(module.__file__).read_text())
    codes = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and node.args:
            if (isinstance(node.func, ast.Name) and node.func.id == "issue") or (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "append"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "reasons"
            ):
                if isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    codes.add(node.args[0].value)
    declared = [code for level in LAYERS.values() for code in level]
    assert len(declared) == len(set(declared))
    assert codes == set(declared)


@pytest.mark.parametrize("layer", [-1, 5])
def test_invalid_policy_layer_rejected(layer):
    with pytest.raises(ValueError):
        policy_decision(PlanValidationReport(), layer)


def test_parse_failure_future_diagnostic_and_invalid_without_issue_fail_closed():
    translated = translate_plan("{bad json")
    assert translated.plan is None
    report = PlanValidationReport(issues=[ValidationIssue(code="parse_failure")])
    assert policy_decision(report, 1)["outcome"] == "blocked"
    report = PlanValidationReport(issues=[ValidationIssue(code="future_issue")])
    assert policy_decision(report, 4)["outcome"] == "blocked"
    assert policy_decision(PlanValidationReport(), 4)["outcome"] == "blocked"


def test_matrix_denominators_reject_all_baseline_and_input_freeze(tmp_path):
    import json

    # Use the same factory within an isolated runtime project.
    project = tmp_path / "project"
    project.mkdir()
    output = project / "runtime" / "e5-pilot"
    result = run_e5(project, output)
    assert result["pass"] and result["candidates"] == 120 and result["policy_decisions"] == 720
    assert result["per_method"]["A4"]["matches_control"] == 120
    assert result["per_method"]["A4"]["vaar"] == 1
    assert result["per_method"]["reject-all"]["urr"] == 0
    assert result["per_method"]["reject-all"]["vaar"] == 0
    assert result["per_method"]["reject-all"]["unknown_deferral_rate"] == 0
    assert result["vpr"] is None and result["confidence_bound"] is None
    assert (output / "pre-evaluation-input-hashes.json").exists()
    references = json.loads((output / "control-references.json").read_text())
    assert all(not r["reviewed"] for r in references)
    assert {r["source_family"] for r in references} == {"example-v8-N4-1"}
    with pytest.raises(ValueError):
        run_e5(project, output)
    with pytest.raises(ValueError):
        run_e5(project, project)
