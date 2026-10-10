"""Formal data audit must reject development reuse, split leakage and forged provenance."""

import importlib.util
import json
from pathlib import Path

import pytest

from upf_agent.v8.models import digest
from upf_agent.v8.plan_cases import prepare_case
from upf_agent.v8.plan_review import GoldReview

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
spec = importlib.util.spec_from_file_location(
    "formal_readiness", SCRIPTS / "v8_formal_readiness.py"
)
readiness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(readiness)


@pytest.fixture
def cases(tmp_path):
    root = tmp_path / "cases"
    for i in range(3):
        prepare_case(root / f"pilot-{i + 1:02}", i)
    return root


def change_gold(root, number, **fields):
    path = root / f"pilot-{number:02}" / "case-reference.json"
    value = json.loads(path.read_text())
    value.update(fields)
    path.write_text(json.dumps(value))


def test_repeated_development_variations_cannot_be_formal_heldout(cases):
    result = readiness.assess(cases, minimum_cases=3)
    assert len(result["connected_components"]) == 1
    assert not result["data_ready"]
    assert not result["heldout_consumed"] and result["formal_vpr"] is None
    assert result["hash_bound_approved_gold"] == 0


def test_relabeling_a_shared_family_is_detected(cases):
    change_gold(cases, 2, split="validation")
    change_gold(cases, 3, split="heldout")
    result = readiness.assess(cases, minimum_cases=3)
    assert "case family leakage across split: structure_family" in result["problems"]


def test_source_hash_and_path_boundaries_are_verified(cases):
    change_gold(cases, 1, source_hashes={"../pilot-02/case-reference.json": "0" * 64})
    result = readiness.assess(cases, minimum_cases=3)
    assert any(p.startswith("source_integrity:pilot-01:") for p in result["problems"])


def test_duplicate_reviewer_or_wrong_hash_never_approves_gold(cases):
    gold = readiness.CaseGold.model_validate_json(
        (cases / "pilot-01/case-reference.json").read_text()
    )
    record = GoldReview(
        case_id=gold.case_id,
        reviewer="unit-reviewer-a",
        reference_sha256=digest(gold),
        decision="approve",
        review_version="unit",
        review_source="synthetic unit control",
    )
    assert readiness.assess(cases, [record, record], 3)["hash_bound_approved_gold"] == 0
    second = record.model_copy(update={"reviewer": "unit-reviewer-b", "reference_sha256": "0" * 64})
    assert readiness.assess(cases, [record, second], 3)["hash_bound_approved_gold"] == 0


def test_mechanical_success_does_not_consume_or_complete_formal_experiment(cases):
    records = []
    for i, split in enumerate(("dev", "validation", "heldout"), 1):
        # Distinct group labels here are artificial unit inputs, not real independent cases.
        change_gold(cases, i, split=split, structure_family=f"unit-family-{i}")
        gold = readiness.CaseGold.model_validate_json(
            (cases / f"pilot-{i:02}/case-reference.json").read_text()
        )
        for reviewer in ("unit-reviewer-a", "unit-reviewer-b"):
            records.append(
                GoldReview(
                    case_id=gold.case_id,
                    reviewer=reviewer,
                    reference_sha256=digest(gold),
                    decision="approve",
                    review_version="unit",
                    review_source="synthetic unit control",
                )
            )
    result = readiness.assess(cases, records, 3)
    assert result["data_ready"] and result["hash_bound_approved_gold"] == 3
    assert not result["formal_experiment_completed"] and not result["heldout_consumed"]
