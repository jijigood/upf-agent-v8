import pytest

from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.e3 import FAMILIES, METHODS, prepare_case
from upf_agent.v8.e3_public import run_public_engine


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("variant", range(4))
def test_production_public_tool_backend_is_bounded_and_keeps_unknowns(tmp_path, family, variant):
    root = tmp_path / "case"
    task, _, reference = prepare_case(root, family, variant)
    task.graph_enabled = False
    contract = compile_contract(task)
    result = run_public_engine(root, task, contract, reference, METHODS[3])
    assert result["production_engine"]
    assert result["shared_public_tool_units"]
    assert result["tool_calls"] <= 8
    assert result["uncommitted_tool_receipts"] == 0
    assert not result["false_closure"]
    assert not result["execute_authorized"]
    assert all(
        h["equal"]
        for h in result["history"]
        if h.get("event") == "production_engine_semantic_comparison"
    )
    assert all(
        c["request"].get("name") in {"search_manual", "analyze_log_window", "lookup_topology"}
        for c in result["calls"]
    )


def test_public_p5_does_not_reserve_a_nonexistent_plan_head(tmp_path):
    import json
    from types import SimpleNamespace

    from upf_agent.v8.e3_p5 import PublishedP5Backend

    calls = []

    class Client:
        def complete(self, messages, **kwargs):
            calls.append((json.loads(messages[1]["content"]), kwargs))
            return "{}"

    tools = SimpleNamespace(
        task=SimpleNamespace(
            as_of=__import__("datetime").datetime.now(__import__("datetime").UTC), version="5.0"
        ),
        staged=SimpleNamespace(catalog=[], publication={"edition": 1}),
    )
    backend = PublishedP5Backend(tools, Client(), shared_public_tools=True)
    backend.client.complete(
        [{"role": "system", "content": "bounded test"}, {"role": "user", "content": "{}"}],
        operation="p5_plan",
        reserve_head=True,
    )
    assert not calls[0][1]["reserve_head"]
    assert calls[0][0]["public_task_constraints"]["freshness_seconds"] == 300
