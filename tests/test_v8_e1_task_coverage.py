"""Task omissions, false coverage claims and real deadline reservation controls."""

import json
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from upf_agent.v8 import e1_covered_head as head
from upf_agent.v8.e1_dataset import write
from upf_agent.v8.e1_expert_revision import REGISTRY, RevisionValidation
from upf_agent.v8.e1_formal import runner_options
from upf_agent.v8.e1_task_coverage import (
    TaskAction,
    TaskObligation,
    TaskRequest,
    covered_obligations,
    load_task_request,
)
from upf_agent.v8.experiment_metrics import MetricCollector
from upf_agent.v8.models import OrchestrationTask, digest


def task_request():
    task = OrchestrationTask(
        question="synthetic explicit log request",
        template="runtime_investigation",
        objects=["upf", "ue"],
        as_of=datetime(2026, 10, 13, tzinfo=UTC),
    )
    request = TaskRequest(
        question_sha256=digest(task.question),
        permission_sha256=digest(task.permission),
        object_profiles_sha256=digest(task.object_profiles),
        obligations=[
            TaskObligation(
                requirement_id="upf-log",
                description="read UPF log",
                any_of=[
                    TaskAction(
                        action_type="READ_LOG", target="upf", required_fields=["log_excerpt"]
                    ),
                ],
            ),
            TaskObligation(
                requirement_id="ue-log",
                description="read UE log or same-source session",
                any_of=[
                    TaskAction(
                        action_type="READ_LOG", target="ue", required_fields=["log_excerpt"]
                    ),
                    TaskAction(
                        action_type="READ_SESSION_PROBE",
                        target="ue",
                        parameters={"probe_id": "normal"},
                        required_fields=["session_probe_inventory.session_log_excerpt"],
                    ),
                ],
            ),
        ],
    )
    return task, request


def wire(request):
    return {
        "registry_version": REGISTRY,
        "context_fingerprint": "unit",
        "scope_fingerprint": "unit",
        "batch_id": "unit",
        "evaluation_as_of": "2026-10-13T00:00:00+00:00",
        "target_objects": ["upf", "ue"],
        "identity_source_admission_sha256": "0" * 64,
        "task_request_sha256": digest(request),
        "task_coverage": {"upf-log": "s1", "ue-log": "s2"},
        "citation_table": {
            f"c{i}": {
                "evidence_id": f"e{i}",
                "revision": 1,
                "source_sha256": "a" * 64,
                "locator": f"raw:{i}",
            }
            for i in (1, 2)
        },
        "steps": [
            {
                "step_id": "s1",
                "action_type": "READ_LOG",
                "target": "upf",
                "text": "核对日志",
                "evidence": ["c1"],
            },
            {
                "step_id": "s2",
                "action_type": "READ_SESSION_PROBE",
                "target": "ue",
                "text": "核对同源日志",
                "parameters": {"probe_id": "normal"},
                "evidence": ["c2"],
            },
        ],
        "stop_conditions": ["unknown remains unknown"],
    }


def sources():
    return [
        SimpleNamespace(evidence_id="e1", object_id="upf", fields={"log_excerpt": ""}),
        SimpleNamespace(
            evidence_id="e2",
            object_id="ue",
            fields={"session_probe_inventory": {"session_log_excerpt": "session remains unknown"}},
        ),
    ]


def test_declared_defaults_are_lossless_and_do_not_claim_execution():
    _, request = task_request()
    raw = json.dumps(wire(request), ensure_ascii=False)
    result = head.translate_covered(raw)
    assert result.plan is not None and result.cost_model_calls == 0
    assert len(result.spans) == 2
    assert result.plan.steps[0].on_unknown == "request_evidence"
    assert result.plan.steps[0].non_executable and not result.plan.steps[0].claimed_executed
    assert raw[result.spans[0].text_start : result.spans[0].text_end] == '"核对日志"'


def test_explicit_empty_log_and_same_source_session_can_be_planned_without_claiming_known():
    _, request = task_request()
    plan = head.translate_covered(json.dumps(wire(request))).plan
    assert all(r["covered"] for r in covered_obligations(plan, request, sources()))
    assert not plan.goal_achieved


@pytest.mark.parametrize(
    "fault",
    [
        "omitted",
        "wrong_object",
        "false_claim",
        "missing_source_field",
        "missing_nested_log",
        "wrong_probe",
        "uncited_source",
    ],
)
def test_coverage_cannot_be_faked_by_a_declaration_or_related_action(fault):
    _, request = task_request()
    value, bindings = wire(request), sources()
    if fault == "omitted":
        value["steps"].pop(0)
    elif fault == "wrong_object":
        value["steps"][0]["target"] = "ue"
    elif fault == "false_claim":
        value["task_coverage"]["upf-log"] = "s2"
    elif fault == "missing_source_field":
        bindings[0].fields = {"event_type": "observation"}
    elif fault == "missing_nested_log":
        bindings[1].fields = {"session_probe_inventory": {"returncode": 0}}
    elif fault == "wrong_probe":
        value["steps"][1]["parameters"]["probe_id"] = "other"
    else:
        value["steps"][0]["evidence"] = []
    plan = head.translate_covered(json.dumps(value)).plan
    assert not all(r["covered"] for r in covered_obligations(plan, request, bindings))


def test_incomplete_plan_is_rejected_even_if_structural_validator_passes(monkeypatch):
    task, request = task_request()
    value = wire(request)
    value["steps"].pop(0)
    plan = head.translate_covered(json.dumps(value)).plan
    monkeypatch.setattr(head, "load_task_request", lambda *_: request)
    monkeypatch.setattr(
        head,
        "validate_revision",
        lambda *args: RevisionValidation(
            raw_plan_validity=True,
            published_plan_validity=True,
            published_plan=args[0],
            retained_steps=len(args[0].steps),
        ),
    )
    result = head.validate_covered(plan, sources(), task, None, None, None)
    assert result.structural_validity and not result.raw_plan_validity
    assert result.published_plan is None and not result.task_coverage_complete
    assert "task_requirement_missing:upf-log" in {i.code for i in result.issues}


def test_complete_plan_keeps_coverage_metadata_on_published_model(monkeypatch):
    task, request = task_request()
    plan = head.translate_covered(json.dumps(wire(request))).plan
    monkeypatch.setattr(head, "load_task_request", lambda *_: request)
    monkeypatch.setattr(
        head,
        "validate_revision",
        lambda *args: RevisionValidation(
            raw_plan_validity=True,
            published_plan_validity=True,
            published_plan=args[0],
            retained_steps=len(args[0].steps),
        ),
    )
    result = head.validate_covered(plan, sources(), task, None, None, None)
    assert result.task_coverage_complete and result.raw_plan_validity
    assert result.validator_version == "v8-covered-readonly-validator-1"
    assert result.published_plan.task_request_sha256 == digest(request)


@pytest.mark.parametrize("fault", ["question", "permission", "profiles"])
def test_request_is_bound_to_question_permissions_and_versions(tmp_path, fault):
    task, request = task_request()
    write(tmp_path / "data/task-request.json", request.model_dump(mode="json"))
    assert load_task_request(tmp_path, task) == request
    if fault == "question":
        task.question = "another question"
    elif fault == "permission":
        task.permission.revision = "another permission revision"
    else:
        task.object_profiles = {
            "upf": {"role": "upf", "product": "Unit", "version": "2"},
            "ue": {"role": "unspecified", "product": "Unit", "version": "2"},
        }
    with pytest.raises(ValueError, match="changed"):
        load_task_request(tmp_path, task)


def test_native_deadline_cannot_spend_reserved_head_time(monkeypatch):
    clock = [1000.0]
    monkeypatch.setattr("upf_agent.v8.plan_generator.perf_counter", lambda: clock[0])
    task, _ = task_request()
    collector = MetricCollector(task.run_id)
    budget = head.ReservedHeadBudget(task, collector)
    assert budget.remaining() == 40
    clock[0] += 40
    with pytest.raises(TimeoutError):
        budget.check("model", {}, reserve_head=True)
    assert collector.events[-1]["status"] == "blocked"
    budget.enter_head()
    assert budget.remaining() == 140
    budget.check("model", {})
    clock[0] += 140
    with pytest.raises(TimeoutError):
        budget.check("model", {})
    assert budget.stage_summary()["total_elapsed_seconds"] == 180


def test_reservation_does_not_increase_call_limits(monkeypatch):
    monkeypatch.setattr("upf_agent.v8.plan_generator.perf_counter", lambda: 1000)
    task, _ = task_request()
    collector = MetricCollector(task.run_id)
    budget = head.ReservedHeadBudget(task, collector)
    for i in range(7):
        collector.emit(str(i), "model", "unit", "attempted", {})
    with pytest.raises(TimeoutError):
        budget.check("model", {}, reserve_head=True)
    budget.enter_head()
    budget.check("model", {})
    collector.emit("8", "model", "unit", "attempted", {})
    with pytest.raises(TimeoutError):
        budget.check("model", {})


def test_short_native_allowance_is_blocked_before_a_paid_request(monkeypatch):
    clock = [1000.0]
    monkeypatch.setattr("upf_agent.v8.plan_generator.perf_counter", lambda: clock[0])
    task, _ = task_request()
    collector = MetricCollector(task.run_id)
    budget = head.ReservedHeadBudget(task, collector)
    clock[0] += 21
    assert budget.remaining() == 19
    with pytest.raises(TimeoutError):
        budget.check("model", {}, reserve_head=True)
    assert collector.events[-1]["error_type"] == "native_allowance_insufficient"
    assert not any(e["status"] == "attempted" for e in collector.events)
    budget.enter_head()
    assert budget.remaining() == 159
    budget.check("model", {})


def test_formal_profile_is_explicit_and_preserves_existing_profiles():
    options, manifest = runner_options(head.PROFILE)
    assert options["budget_factory"] is head.ReservedHeadBudget
    assert manifest["task_request_source"] == "explicit public user question; never Gold"
    assert "budget_factory" not in runner_options("legacy")[0]
    assert "budget_factory" not in runner_options("expert-readonly-revision-1")[0]


def test_coverage_options_resolve_local_refs_and_reject_absent_nested_fields():
    _, request = task_request()
    schema = {
        "properties": {
            "citation_table": {"const": {"c1": {"evidence_id": "e1"}, "c2": {"evidence_id": "e2"}}}
        },
        "$defs": {
            "LogRefs": {"anyOf": [{"const": "c1"}]},
            "PlanStep": {
                "anyOf": [
                    {
                        "properties": {
                            "action_type": {"const": "READ_LOG"},
                            "target": {"const": "upf"},
                            "step_id": {"const": "s1"},
                            "parameters": {"properties": {}},
                            "evidence": {"items": {"$ref": "#/$defs/LogRefs"}},
                        }
                    },
                    {
                        "properties": {
                            "action_type": {"const": "READ_SESSION_PROBE"},
                            "target": {"const": "ue"},
                            "step_id": {"const": "s2"},
                            "parameters": {"properties": {"probe_id": {"const": "normal"}}},
                            "evidence": {"items": {"const": "c2"}},
                        }
                    },
                ]
            },
        },
    }
    bindings = sources()
    assert head.obligation_options(schema, request, bindings) == {
        "upf-log": ["s1"],
        "ue-log": ["s2"],
    }
    bindings[1].fields = {"session_probe_inventory": {}}
    assert head.obligation_options(schema, request, bindings)["ue-log"] == []
