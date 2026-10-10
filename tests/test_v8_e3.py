import json

import pytest

from upf_agent.v8.adapters import read_observation
from upf_agent.v8.compiler import compile_query_plan
from upf_agent.v8.e3 import FAMILIES, METHODS, RoundEvidenceBackend, prepare_case, run_deterministic
from upf_agent.v8.e3_p5 import PublishedEvidenceTools, PublishedP5Backend
from upf_agent.v8.experiment_metrics import MetricCollector
from upf_agent.v8.plan_generator import PlanBudget


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("variant", range(4))
def test_three_methods_close_real_publications_and_keep_unfixable_open(tmp_path, family, variant):
    import shutil

    source = tmp_path / "source"
    task, contract, ref = prepare_case(source, family, variant)
    permission, clock = task.permission.model_dump_json(), task.as_of
    original = {p: p.read_bytes() for p in source.rglob("*.json")}
    results = {}
    for method in (METHODS[0], METHODS[1], METHODS[3]):
        root = tmp_path / method
        shutil.copytree(source, root)
        results[method] = run_deterministic(root, task, contract, ref, method)
        assert results[method]["budget_ok"]
        assert not results[method]["false_closure"]
        assert not results[method]["execute_authorized"]
        assert all(h["full_local_equal"] for h in results[method]["history"] if "states" in h)
    assert not results[METHODS[0]]["primary_closed"]
    for method in (METHODS[1], METHODS[3]):
        assert results[method]["primary_closed"] is ref["solvable"]
        assert results[method]["all_closed"] is ref["solvable"]
        assert results[method]["correct_stop"] is (not ref["solvable"])
    assert results[METHODS[3]]["redundant_queries"] == 0
    assert task.permission.model_dump_json() == permission and task.as_of == clock
    assert all(p.read_bytes() == raw for p, raw in original.items())
    if family == "permission-denied":
        assert all("n4_enabled" not in b.fields for b in _bindings(tmp_path / METHODS[3], task))
    if ref["solvable"] and ref["repair_round"] == 2:
        assert any(
            h.get("event") == "wait_for_declared_publication"
            for h in results[METHODS[3]]["history"]
        )


def _bindings(root, task):
    from upf_agent.v8.store import Ledger

    ledger = Ledger(root)
    try:
        return ledger.evidence(task.run_id)
    finally:
        ledger.close()


def test_future_source_is_not_visible_and_cannot_be_committed(tmp_path):
    task, contract, _ = prepare_case(tmp_path / "case", FAMILIES[0], 1)
    backend = RoundEvidenceBackend(tmp_path / "case", task, contract)
    try:
        tools = PublishedEvidenceTools(backend, PlanBudget(task, MetricCollector(task.run_id)))
        initial = list(tools._rows())
        assert next(row[3] for row in initial if row[3]["slot_id"] == "K:UPF-A")["version"] is None
        step = compile_query_plan(task, contract).steps[0].model_copy(deep=True)
        step.arguments["files"] = [backend.catalog[2]["file"]]
        future, _ = read_observation(backend.root, task, contract, step, "future")
        with pytest.raises(ValueError, match="future/changed"):
            backend.normalize(future, "future")
        backend.round = 2
        assert (
            next(row[3] for row in tools._rows() if row[3]["slot_id"] == "K:UPF-A")["version"]
            == "5.0"
        )
    finally:
        backend.ledger.close()


def test_tampered_publication_fails_closed(tmp_path):
    task, contract, _ = prepare_case(tmp_path / "case", FAMILIES[0], 0)
    backend = RoundEvidenceBackend(tmp_path / "case", task, contract)
    try:
        path = backend.root / backend.publication["file"]
        body = json.loads(path.read_text())
        body["observations"][0]["version"] = "5.0"
        path.write_text(json.dumps(body))
        with pytest.raises(ValueError, match="frozen publication changed"):
            backend.collect(compile_query_plan(task, contract).steps[0])
        assert not backend.ledger.evidence(task.run_id)
    finally:
        backend.ledger.close()


def test_same_publication_retains_first_binding_receipt_and_latest_edition(tmp_path):
    task, contract, _ = prepare_case(tmp_path / "case", FAMILIES[0], 0)
    backend = RoundEvidenceBackend(tmp_path / "case", task, contract)
    try:
        step = compile_query_plan(task, contract).steps[0]
        backend.collect(step)
        old = _bindings(backend.root, task)
        backend.round = 1
        backend.collect(step)
        fresh = _bindings(backend.root, task)
        assert len(old) == len(fresh)
        assert all(b.revision == 2 for b in fresh)
        backend.round = 2
        backend.collect(step)
        assert _bindings(backend.root, task) == fresh
        assert backend.calls[-1]["redundant_query"]
        assert len(backend.calls) == 3
    finally:
        backend.ledger.close()


def test_native_planner_context_has_no_reference_or_typed_states(tmp_path):
    from types import SimpleNamespace

    from upf_agent.agent_contracts import AgentTask
    from upf_agent.contracts import TaskType

    task, contract, _ = prepare_case(tmp_path / "case", FAMILIES[0], 1)
    staged = RoundEvidenceBackend(tmp_path / "case", task, contract)
    captured = []

    class Client:
        def complete(self, messages, **kwargs):
            captured.append(json.loads(messages[1]["content"]))
            return {"content": '{"actions":[],"done":true}'}

    try:
        tools = PublishedEvidenceTools(staged, PlanBudget(task, MetricCollector(task.run_id)))
        data = SimpleNamespace(
            task=AgentTask(run_id=task.run_id, question=task.question, task_type=TaskType.DIAGNOSE),
            rounds=2,
            evidence=[],
            facts=[],
            receipts=[],
        )
        PublishedP5Backend(tools, Client()).model("plan", data, 10, 5)
        assert staged.round == 2
        assert (
            not {"reference", "states", "solvable", "repair_round", "contract"} & captured[0].keys()
        )
        assert captured[0]["evidence"] == []
        assert captured[0]["source_publication_catalog"] == staged.catalog
        assert captured[0]["current_source_publication"]["round"] == 2
        assert all("observations" not in item for item in captured[0]["source_publication_catalog"])
    finally:
        staged.ledger.close()


@pytest.mark.parametrize("variant", range(4))
def test_unavailable_native_seed_commits_valid_failure_and_counts_dispatch(tmp_path, variant):
    from pathlib import Path

    from upf_agent.v8.e3_p5 import run_native_p5

    root = tmp_path / "case"
    task, contract, reference = prepare_case(root, "tool-unavailable", variant)
    result = run_native_p5(Path(__file__).resolve().parents[1], root, task, contract, reference)
    assert result["native_error"] is None
    assert result["tool_calls"] == result["committed_tool_calls"] == 1
    assert result["uncommitted_tool_receipts"] == 0
    assert result["model_calls"] == 0 and result["budget_ok"]
    assert not result["primary_closed"]
    assert result["correct_stop"] is (not reference["solvable"])
    assert result["dispatcher_metrics"]["invocations"]["tool"]["error"] == 1
    assert all("ValidationError" not in gap for gap in result["native_state"]["gaps"])
    assert result["native_state"]["rounds"] == 0


def test_uncertain_receipt_is_counted_and_never_scored_as_correct_stop(tmp_path):
    task, contract, reference = prepare_case(tmp_path / "case", "no-source-exists", 2)
    backend = RoundEvidenceBackend(tmp_path / "case", task, contract)
    backend.ledger.charge(task, "crashed-dispatch", "tool", {"tool": "read_observation"})
    result = backend.finish("native_termination", reference, 0.01)
    assert result["tool_calls"] == result["uncommitted_tool_receipts"] == 1
    assert result["committed_tool_calls"] == 0
    assert not result["correct_stop"]
