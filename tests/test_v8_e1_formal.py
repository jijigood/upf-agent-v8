"""Workflow controls use synthetic unit fixtures, never real review facts."""

import json
from pathlib import Path

import httpx
import pytest

from upf_agent.v8 import e1_formal
from upf_agent.v8.e1_dataset import CaseManifest, DatasetIndex, load_dataset, readiness, sha, write
from upf_agent.v8.e1_output_review import finalize
from upf_agent.v8.models import digest
from upf_agent.v8.phase2 import METHODS, run_method
from upf_agent.v8.plan_cases import prepare_case
from upf_agent.v8.plan_generator import ObservedPlanClient
from upf_agent.v8.plan_ir import ActionPattern, GoldBranch, PlanIR, PlanStep

PROJECT = Path(__file__).resolve().parents[1]


def case(root, case_id, split, *, approved=False):
    folder = (
        root
        / {"dev": "development", "validation": "validation", "heldout": "heldout"}[split]
        / case_id
    )
    visible = folder / "visible"
    task, gold = prepare_case(visible, 0)
    observation = visible / task.observation_files[0]
    body = json.loads(observation.read_text())
    body["source_id"] = "distinct-synthetic-unit-source-" + case_id
    write(observation, body)
    task.path.source_id = body["source_id"]
    task.path.source_sha256 = sha(observation)
    write(visible / "case-task.json", task.model_dump(mode="json"))
    gold.case_id = case_id
    gold.split = split
    gold.source_group = split + "-synthetic-unit-source-" + case_id
    gold.structure_family = split + "-synthetic-unit-family"
    if split == "heldout":
        gold.structure_family += str(int(case_id.split("-")[-1]) % 2)
    gold.source_hashes = {task.observation_files[0]: sha(observation)}
    gold.any_of = [
        GoldBranch(
            branch_id="synthetic-unit-identity-only",
            required=[
                ActionPattern(
                    pattern_id="identity" + str(i), action_type="CHECK_IDENTITY", target=obj
                )
                for i, obj in enumerate(task.objects)
            ],
        )
    ]
    reference = f"gold/{split}/{case_id}.json"
    write(root / reference, gold.model_dump(mode="json"))
    (visible / "case-reference.json").unlink()
    provenance = f"gold/provenance/{case_id}.json"
    write(root / provenance, {"fixture_only": True, "not_actual_case_or_human_review": True})
    manifest = CaseManifest(
        case_id=case_id,
        split=split,
        visible_root=str(visible.relative_to(root)),
        task_file=str((visible / "case-task.json").relative_to(root)),
        reference_file=reference,
        source_group=gold.source_group,
        structure_family=gold.structure_family,
        source_kind="new-synthetic",
        previously_evaluated=False,
        provenance_file=provenance,
    )
    name = str((folder / "case.json").relative_to(root))
    write(root / name, manifest.model_dump(mode="json"))
    records = (
        [
            {
                "case_id": case_id,
                "reviewer": "unit-reviewer-" + str(i),
                "reference_sha256": digest(gold),
                "decision": "approve",
                "review_version": "synthetic-unit-test-only",
                "review_source": "reviews/records/unit-receipt.txt",
            }
            for i in [1, 2]
        ]
        if approved
        else []
    )
    return name, records, task, gold


def index(root, entries, records):
    write(root / "dataset.json", DatasetIndex(cases=entries).model_dump(mode="json"))
    write(root / "reviews/received-reviews.json", records)
    (root / "reviews/records").mkdir(parents=True, exist_ok=True)
    (root / "reviews/records/unit-receipt.txt").write_text(
        "Synthetic unit receipt, not expert approval."
    )
    write(root / "history-index.json", {"visible_source_hashes": [], "structure_families": []})


def fake_response(request):
    body = json.loads(request.content)
    context = json.loads(body["messages"][1]["content"])
    if "trusted_header" not in context:
        content = json.dumps({"actions": [], "done": True, "questions": [], "candidates": []})
    else:
        header = context["trusted_header"]
        steps = [
            PlanStep(
                step_id="id" + str(i), text="核对身份", action_type="CHECK_IDENTITY", target=obj
            )
            for i, obj in enumerate(header["target_objects"])
        ]
        content = PlanIR(**header, steps=steps, stop_conditions=["缺证则停止"]).model_dump_json()
    return httpx.Response(
        200,
        json={
            "choices": [{"message": {"content": content}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 20},
        },
    )


def fake_client(model, collector, budget, **kwargs):
    return ObservedPlanClient(
        model, collector, budget, transport=httpx.MockTransport(fake_response), **kwargs
    )


def unit_output_reviews(frozen, run_root, review_root):
    records = []
    selected = json.loads((frozen / "freeze.json").read_text())["selected_cases"]
    for item in load_dataset(frozen / "dataset")["cases"]:
        case_id = item["manifest"].case_id
        if case_id not in selected:
            continue
        for method in METHODS:
            raw = (
                run_root / "runs" / case_id / f"method-{METHODS.index(method) + 1}" / "raw-plan.txt"
            )
            for seat in [1, 2]:
                records.append(
                    {
                        "case_id": case_id,
                        "method": method,
                        "raw_plan_sha256": sha(raw),
                        "reference_sha256": digest(item["gold"]),
                        "reviewer": f"unit-output-reviewer-{seat}",
                        "semantic_valid": True,
                        "review_version": "unit-only",
                        "review_source": "unit-output-receipt.txt",
                        "notes": ["synthetic unit control; not actual expert review"],
                    }
                )
    (review_root / "unit-output-receipt.txt").write_text("Synthetic unit receipt only.")
    return records


@pytest.fixture
def small(tmp_path):
    root = tmp_path / "dataset"
    entry, records, task, gold = case(root, "E1-N4-EXTERNAL", "dev")
    index(root, [entry], records)
    return root, entry, task, gold


def test_file_id_needs_no_pilot_number_and_model_receives_no_reference(
    small, tmp_path, monkeypatch
):
    root, _, task, gold = small
    from upf_agent.v8 import phase2

    monkeypatch.setattr(
        phase2, "prepare_case", lambda *a: pytest.fail("fixed SPECS generation forbidden")
    )
    item = load_dataset(root)["cases"][0]
    output = tmp_path / "method"
    output.mkdir()
    row = run_method(PROJECT, item["visible"], output, task, gold, METHODS[0], fake_client)
    assert row["case_id"] == "E1-N4-EXTERNAL" and not row["calibration_candidate"]
    traces = (output / "model-traces.jsonl").read_text()
    assert "synthetic-unit-identity-only" not in traces
    assert "unit-reviewer" not in traces and "reference_file" not in traces
    assert not (output / "runtime" / "case-reference.json").exists()


@pytest.mark.parametrize(
    "fault", ["scope", "source", "visible-gold", "answer-fields", "review-identity"]
)
def test_corruption_or_answer_leak_rejected_before_model_calls(small, fault):
    root, entry, task, gold = small
    manifest = json.loads((root / entry).read_text())
    visible = root / manifest["visible_root"]
    if fault == "scope":
        task.permission.revision = "changed-after-Gold"
        write(visible / "case-task.json", task.model_dump(mode="json"))
    elif fault == "source":
        (visible / task.observation_files[0]).write_text('{"synthetic":true,"observations":[]}')
    elif fault == "visible-gold":
        write(visible / "data/case-reference.json", gold.model_dump(mode="json"))
    elif fault == "answer-fields":
        body = json.loads((visible / task.observation_files[0]).read_text())
        body["expected_answer"] = "hidden organizer truth"
        write(visible / task.observation_files[0], body)
    else:
        records = [
            {
                "case_id": gold.case_id,
                "reviewer": reviewer,
                "reference_sha256": digest(gold),
                "decision": "approve",
                "review_version": "unit",
                "review_source": "reviews/records/unit-receipt.txt",
            }
            for reviewer in ["same-person", " SAME-PERSON "]
        ]
        write(root / "reviews/received-reviews.json", records)
    with pytest.raises(ValueError):
        load_dataset(root)


def test_no_reviews_never_reaches_deployment_or_consumes_heldout(small, tmp_path, monkeypatch):
    root, _, _, _ = small
    monkeypatch.setattr(
        e1_formal, "deployment_snapshot", lambda *a: pytest.fail("no model probe before Gold ready")
    )
    output = tmp_path / "freeze"
    with pytest.raises(ValueError, match="formal data not ready"):
        e1_formal.freeze(PROJECT, root, output, stage="heldout")
    assert not output.exists() and not (root / "consumption.json").exists()
    assert readiness(load_dataset(root))["hash_bound_approved_gold"] == 0


def test_known_e7_capture_cannot_be_relabelled_as_new_case(small):
    root, entry, task, _ = small
    manifest = json.loads((root / entry).read_text())
    manifest["split"] = "validation"
    (root / "validation").mkdir()
    write(root / "validation/case.json", manifest)
    write(
        root / "dataset.json", DatasetIndex(cases=["validation/case.json"]).model_dump(mode="json")
    )
    fingerprint = sha(root / manifest["visible_root"] / task.observation_files[0])
    write(
        root / "history-index.json",
        {"visible_source_hashes": [fingerprint], "structure_families": []},
    )
    with pytest.raises(ValueError, match="previously evaluated"):
        load_dataset(root)
    assert (root / entry).exists()


def test_review_receipt_required_even_with_two_approve_fields(small):
    root, _, _, gold = small
    records = [
        {
            "case_id": gold.case_id,
            "reviewer": "unit-" + str(i),
            "reference_sha256": digest(gold),
            "decision": "approve",
            "review_version": "unit",
            "review_source": "reviews/missing.txt",
        }
        for i in [1, 2]
    ]
    write(root / "reviews/received-reviews.json", records)
    with pytest.raises(FileNotFoundError):
        load_dataset(root)


def test_real_adapter_preserves_actual_provenance(small, tmp_path):
    root, entry, task, gold = small
    manifest = json.loads((root / entry).read_text())
    visible = root / manifest["visible_root"]
    task.path.synthetic = False
    task.synthetic = False
    body = json.loads((visible / task.observation_files[0]).read_text())
    body["synthetic"] = False
    write(visible / task.observation_files[0], body)
    output = tmp_path / "real-adapter"
    output.mkdir()
    row = run_method(
        PROJECT,
        visible,
        output,
        task,
        gold,
        METHODS[0],
        fake_client,
        tools_factory=e1_formal.NormalizedEvidenceTools,
    )
    bindings = json.loads((output / "bindings.json").read_text())
    assert bindings and all(b["synthetic"] is False for b in bindings)
    assert row["case_id"] == gold.case_id


@pytest.fixture
def full_dataset(tmp_path, monkeypatch):
    root = tmp_path / "dataset"
    entries, records = [], []
    for split, count in [("dev", 24), ("validation", 12), ("heldout", 24)]:
        for i in range(count):
            entry, pair, _, _ = case(root, f"UNIT-{split}-{i}", split, approved=True)
            entries.append(entry)
            records.extend(pair)
    index(root, entries, records)
    monkeypatch.setattr(e1_formal, "deployment_snapshot", lambda *a: {"fixture_only": True})
    monkeypatch.setattr(e1_formal, "heldout_registry", lambda *a: tmp_path / "unit-consumption")
    assert readiness(load_dataset(root))["data_ready"]
    return root


def test_validation_then_heldout_has_complete_denominators_and_single_consumption(
    full_dataset, tmp_path
):
    validation = tmp_path / "validation-freeze"
    frozen = e1_formal.freeze(PROJECT, full_dataset, validation)
    assert len(frozen["selected_cases"]) == 12
    output = tmp_path / "validation-run"
    result = e1_formal.run(PROJECT, validation, output, client_factory=fake_client, probe=False)
    assert result["execution_pass"] and result["recorded_method_runs"] == 48
    assert not result["heldout_consumed"] and not result["formal_e1_completed"]
    heldout = tmp_path / "heldout-freeze"
    with pytest.raises(ValueError, match="validation incomplete"):
        e1_formal.freeze(PROJECT, full_dataset, heldout, stage="heldout", validation_result=output)
    validation_reviews = tmp_path / "validation-output-reviews.json"
    write(validation_reviews, unit_output_reviews(validation, output, tmp_path))
    validation_final = tmp_path / "validation-final"
    finalize(validation, output, validation_reviews, tmp_path, validation_final)
    e1_formal.freeze(
        PROJECT, full_dataset, heldout, stage="heldout", validation_result=validation_final
    )
    result = e1_formal.run(
        PROJECT, heldout, tmp_path / "heldout-run", client_factory=fake_client, probe=False
    )
    assert result["recorded_method_runs"] == 96 and result["heldout_consumed"]
    assert all(s["vpr_denominator"] == 24 for s in result["summaries"].values())
    assert result["formal_vpr"] is None and not result["formal_e1_completed"]
    assert result["formal_e1_execution_completed"]
    statistics = json.loads((tmp_path / "heldout-run/paired-statistics.json").read_text())
    assert all(
        cost["planned_case_denominator"] == 24 and cost["measured_pairs"] == 24
        for comparison in statistics
        for cost in comparison["paired_costs"].values()
    )
    empty = tmp_path / "empty-output-reviews.json"
    write(empty, [])
    with pytest.raises(ValueError, match="two actual semantic"):
        finalize(heldout, tmp_path / "heldout-run", empty, tmp_path, tmp_path / "incomplete-final")
    records = unit_output_reviews(heldout, tmp_path / "heldout-run", tmp_path)
    # Semantically invalid text can never be promoted by a passing structural score.
    invalid = [r for r in records if r["case_id"] == "UNIT-heldout-0" and r["method"] == METHODS[1]]
    for record in invalid:
        record["semantic_valid"] = False
    reviews = tmp_path / "output-reviews.json"
    write(reviews, records)
    final = finalize(heldout, tmp_path / "heldout-run", reviews, tmp_path, tmp_path / "final")
    assert final["formal_e1_completed"]
    assert final["summaries"][METHODS[1]]["vpr"] == 23 / 24
    invalid[0]["semantic_valid"] = True
    conflict = tmp_path / "conflicting-output-reviews.json"
    write(conflict, records)
    with pytest.raises(ValueError, match="third-reviewer adjudication"):
        finalize(heldout, tmp_path / "heldout-run", conflict, tmp_path, tmp_path / "conflict-final")
    with pytest.raises((FileExistsError, ValueError)):
        e1_formal.run(
            PROJECT, heldout, tmp_path / "second-run", client_factory=fake_client, probe=False
        )
    with pytest.raises(ValueError, match="previously consumed"):
        e1_formal.freeze(
            PROJECT,
            full_dataset,
            tmp_path / "renamed-freeze",
            stage="heldout",
            validation_result=validation_final,
        )


def test_frozen_tamper_and_no_validation_block_heldout(full_dataset, tmp_path):
    with pytest.raises(ValueError, match="completed frozen validation"):
        e1_formal.freeze(PROJECT, full_dataset, tmp_path / "premature", stage="heldout")
    frozen = tmp_path / "freeze"
    e1_formal.freeze(PROJECT, full_dataset, frozen)
    (frozen / "dataset/reviews/received-reviews.json").write_text("[]")
    with pytest.raises(ValueError, match="frozen input changed"):
        e1_formal.run(PROJECT, frozen, tmp_path / "run", client_factory=fake_client, probe=False)
    assert not (frozen / "consumption.json").exists()


def test_transport_failure_remains_in_approved_soluble_denominator(full_dataset, tmp_path):
    def failed_client(model, collector, budget, **kwargs):
        return ObservedPlanClient(
            model,
            collector,
            budget,
            transport=httpx.MockTransport(lambda _: httpx.Response(503)),
            **kwargs,
        )

    frozen = tmp_path / "freeze"
    e1_formal.freeze(PROJECT, full_dataset, frozen)
    result = e1_formal.run(
        PROJECT, frozen, tmp_path / "run", client_factory=failed_client, probe=False
    )
    assert result["recorded_method_runs"] == 48 and not result["execution_pass"]
    assert all(s["vpr_denominator"] == 12 and s["vpr"] == 0 for s in result["summaries"].values())


def test_runner_error_keeps_quality_denominator_and_marks_cost_unknown(
    full_dataset, tmp_path, monkeypatch
):
    original = e1_formal.run_method

    def failing_method(*args, **kwargs):
        if args[4].case_id == "UNIT-validation-0" and args[5] == METHODS[1]:
            raise RuntimeError("synthetic unit runner failure")
        return original(*args, **kwargs)

    monkeypatch.setattr(e1_formal, "run_method", failing_method)
    frozen = tmp_path / "freeze"
    e1_formal.freeze(PROJECT, full_dataset, frozen)
    output = tmp_path / "run"
    result = e1_formal.run(PROJECT, frozen, output, client_factory=fake_client, probe=False)
    assert result["runner_errors"] == 1 and result["recorded_method_runs"] == 48
    assert result["summaries"][METHODS[1]]["vpr_denominator"] == 12
    primary = json.loads((output / "paired-statistics.json").read_text())[0]
    for cost in primary["paired_costs"].values():
        assert cost["planned_case_denominator"] == 12 and cost["measured_pairs"] == 11
        assert cost["unknown_case_ids"] == ["UNIT-validation-0"]
        assert cost["mean_difference"] is None and not cost["complete_measurement"]
