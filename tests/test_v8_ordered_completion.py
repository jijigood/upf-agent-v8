"""Evidence exports and formal intake must preserve failure denominators and real receipts."""

import csv
import importlib
import json
from pathlib import Path

import pytest

from upf_agent.v8.models import digest
from upf_agent.v8.plan_cases import prepare_case


@pytest.fixture
def modules(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("v8_sample_export"), importlib.import_module("v8_formal_intake")


def test_sample_export_preserves_unknown_failure_and_denominator(tmp_path, modules):
    export, _ = modules
    raw = tmp_path / "original.json"
    raw.write_text('{"method_failure":true,"top1_correct":false,"vpr":null}\n')
    table = export.EvidenceTable(tmp_path)
    for case, correct in [("a", True), ("b", False)]:
        table.add(
            "E7",
            "batch",
            "dev",
            "round",
            case,
            "method",
            case,
            {"top1_correct": correct, "method_failure": not correct, "vpr": None},
            table.refs(raw=[raw]),
        )
    out = tmp_path / "runtime/v8-next/export"
    result = table.write(out)
    assert result["sample_rows"] == 2 and result["formal_vpr"] is None
    text = (out / "E7-samples.csv").read_text(encoding="utf-8-sig")
    assert "false" in text and "true" in text
    assert raw.read_text().startswith('{"method_failure":true')


def test_duplicate_case_method_cannot_hide_behind_a_new_line_number(tmp_path, modules):
    export, _ = modules
    table = export.EvidenceTable(tmp_path)
    table.add("E1", "batch", "dev", "plan", "a", "method", "line-1", {}, {})
    with pytest.raises(ValueError, match="duplicate sample"):
        table.add("E1", "batch", "dev", "plan", "a", "method", "line-2", {}, {})


def test_pinned_source_tamper_rejected_without_output(tmp_path, modules):
    export, _ = modules
    original = tmp_path / "raw.txt"
    original.write_text("original")
    table = export.EvidenceTable(tmp_path)
    table.add("E1", "batch", "dev", "plan", "a", "method", "line-1", {}, table.refs(raw=[original]))
    original.write_text("tampered")
    output = tmp_path / "runtime/v8-next/export"
    with pytest.raises(ValueError, match="source changed"):
        table.write(output)
    assert not output.exists()


def test_source_path_escape_and_formal_reclassification_rejected(tmp_path, modules):
    export, _ = modules
    table = export.EvidenceTable(tmp_path / "project")
    outside = tmp_path / "outside.txt"
    outside.write_text("outside")
    with pytest.raises(ValueError, match="inside the project"):
        table.file(outside)
    with pytest.raises(ValueError, match="development batches"):
        table.add("E1", "batch", "dev", "plan", "a", "method", "line-1", {"vpr": True}, {})


def test_empty_intake_does_not_approve_or_consume_any_case(tmp_path, modules):
    _, formal = modules
    cases = tmp_path / "cases"
    prepare_case(cases / "pilot-01", 0)
    before = (cases / "pilot-01/case-reference.json").read_bytes()
    result = formal.intake(tmp_path, cases, tmp_path / "runtime/v8-next/intake")
    assert result["actual_review_records"] == result["hash_bound_approved_gold"] == 0
    assert not result["formal_execution_allowed"] and not result["heldout_consumed"]
    assert (cases / "pilot-01/case-reference.json").read_bytes() == before


def reviews(gold, source):
    return [
        {
            "case_id": gold.case_id,
            "reviewer": reviewer,
            "reference_sha256": digest(gold),
            "decision": "approve",
            "review_version": "synthetic-unit-test",
            "review_source": source,
        }
        for reviewer in ["unit-reviewer-a", "unit-reviewer-b"]
    ]


def test_names_and_approve_fields_without_physical_receipt_are_not_gold(tmp_path, modules):
    _, formal = modules
    cases = tmp_path / "cases"
    _, gold = prepare_case(cases / "pilot-01", 0)
    records = tmp_path / "reviews.json"
    records.write_text(json.dumps(reviews(gold, "nonexistent.txt")))
    result = formal.intake(tmp_path, cases, tmp_path / "runtime/v8-next/intake", records)
    assert result["hash_bound_approved_gold"] == 0
    assert len(result["invalid_review_sources"]) == 2


@pytest.mark.parametrize("fault", ["hash", "identity"])
def test_bad_hash_or_alias_duplicate_rejected_before_intake_output(tmp_path, modules, fault):
    _, formal = modules
    cases = tmp_path / "cases"
    _, gold = prepare_case(cases / "pilot-01", 0)
    rows = reviews(gold, "review.txt")
    if fault == "hash":
        rows[0]["reference_sha256"] = "0" * 64
    else:
        rows[1]["reviewer"] = " UNIT-REVIEWER-A "
    records = tmp_path / "reviews.json"
    records.write_text(json.dumps(rows))
    output = tmp_path / "runtime/v8-next/intake"
    with pytest.raises(ValueError):
        formal.intake(tmp_path, cases, output, records)
    assert not output.exists()


def test_version_bound_pair_creates_new_reference_without_overwriting_original(tmp_path, modules):
    _, formal = modules
    cases = tmp_path / "cases"
    _, gold = prepare_case(cases / "pilot-01", 0)
    original = cases / "pilot-01/case-reference.json"
    before = original.read_bytes()
    receipt = tmp_path / "unit-review.txt"
    receipt.write_text("synthetic test receipt; not actual expert approval")
    records = tmp_path / "reviews.json"
    records.write_text(json.dumps(reviews(gold, receipt.name)))
    output = tmp_path / "runtime/v8-next/intake"
    result = formal.intake(tmp_path, cases, output, records)
    assert result["hash_bound_approved_gold"] == 1
    assert not result["data_ready"] and not result["formal_execution_allowed"]
    assert len(list((output / "approved-references").glob("*.json"))) == 1
    assert original.read_bytes() == before


def test_repeated_case_does_not_create_independent_clusters(modules):
    analysis = importlib.import_module("v8_sample_analysis")
    rows = []
    for repeat in range(5):
        for method, value in [("baseline", False), ("treatment", True)]:
            rows.append(
                {
                    "case_id": "case",
                    "replicate": str(repeat),
                    "method": method,
                    "source_group": "same-source",
                    "structure_family": "same-template",
                    "pass": value,
                }
            )
    result = analysis.paired(rows, "baseline", "treatment", "pass")
    assert result["paired_observations"] == 5
    assert result["source_structure_components"] == 1
    assert result["cluster_bootstrap95_exploratory"] is None
    assert not result["formal_inference"]


def test_failed_or_missing_method_cannot_be_removed_from_paired_comparison(modules):
    analysis = importlib.import_module("v8_sample_analysis")
    rows = [
        {"case_id": "a", "method": "baseline", "pass": True},
        {"case_id": "a", "method": "treatment", "pass": True},
        {"case_id": "b", "method": "baseline", "pass": False},
    ]
    with pytest.raises(ValueError, match="exactly the same observations"):
        analysis.paired(rows, "baseline", "treatment", "pass")
    rows.append({"case_id": "b", "method": "treatment", "pass": False})
    result = analysis.paired(rows, "baseline", "treatment", "pass")
    assert result["paired_observations"] == 2 and result["baseline_mean"] == 0.5


def test_boolean_text_false_is_not_treated_as_truthy(modules):
    analysis = importlib.import_module("v8_sample_analysis")
    assert analysis.boolean("false") is False
    with pytest.raises(ValueError, match="explicit boolean"):
        analysis.boolean("1")


def test_long_evidence_field_keeps_complete_original_record(tmp_path, modules):
    analysis = importlib.import_module("v8_sample_analysis")
    path = tmp_path / "samples.csv"
    reference = "evidence," * 20000
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["pass", "artifact_refs"])
        writer.writeheader()
        writer.writerow({"pass": "false", "artifact_refs": reference})
    rows = analysis.table_rows(path)
    assert rows == [{"pass": "false", "artifact_refs": reference}]


def test_quality_gain_does_not_hide_increased_cost_or_missing_failure_cost(modules):
    analysis = importlib.import_module("v8_sample_analysis")
    rows = [
        {"case_id": "a", "method": "baseline", "tool_attempts": "1"},
        {"case_id": "a", "method": "treatment", "tool_attempts": "3"},
        {"case_id": "b", "method": "baseline", "tool_attempts": "1"},
        {"case_id": "b", "method": "treatment", "tool_attempts": "3"},
    ]
    result = analysis.paired_costs(rows, "baseline", "treatment")[0]
    assert result["cost_increased"] and result["mean_cost_difference"] == 2
    assert result["baseline_total"] == 2 and result["treatment_total"] == 6
    rows[-1]["tool_attempts"] = ""
    with pytest.raises(ValueError, match="partial cost coverage"):
        analysis.paired_costs(rows, "baseline", "treatment")
