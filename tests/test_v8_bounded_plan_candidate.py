import importlib
import json
import shutil
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest

from upf_agent.config import load_model_config
from upf_agent.v8.adapters import collect
from upf_agent.v8.bounded_plan_generator import candidate_schema, generate_bounded_plan
from upf_agent.v8.compiler import compile_contract, compile_query_plan
from upf_agent.v8.experiment_metrics import MetricCollector
from upf_agent.v8.models import EvaluationContext, EvidenceBinding
from upf_agent.v8.plan_capabilities import compile_capabilities
from upf_agent.v8.plan_cases import prepare_case
from upf_agent.v8.plan_generator import ObservedPlanClient, PlanBudget, generation_schema

PROJECT = Path(__file__).resolve().parents[1]


def inputs(root, index=0):
    task, _ = prepare_case(root, index)
    contract = compile_contract(task)
    context = EvaluationContext.from_task(task, contract, "candidate-test")
    bindings = []
    for step in compile_query_plan(task, contract).steps:
        packet = collect(root, task, contract, step, step.step_id)
        bindings.extend(EvidenceBinding.model_validate(b) for b in packet["bindings"])
    caps = compile_capabilities(task, context, bindings, root)
    return task, context, bindings, caps


def test_candidate_retains_source_gates_and_allows_action_choice_with_dependency_anchors(tmp_path):
    task, _, bindings, caps = inputs(tmp_path / "case")
    schema = candidate_schema(
        bindings, {"target_objects": task.objects}, capabilities=caps, task=task
    )
    assert schema["properties"]["steps"] == {
        "type": "array",
        "items": {"$ref": "#/$defs/PlanStep"},
        "minItems": 1,
        "maxItems": 8,
    }
    branches = schema["$defs"]["PlanStep"]["anyOf"]
    assert len(branches) > 8  # Alternatives exist; not an eight-step mandatory workflow.
    evidence = {b.evidence_id: b for b in bindings}
    for branch in branches:
        p = branch["properties"]
        action, target = p["action_type"]["const"], p["target"]["const"]
        assert action != "PROPOSE_CHANGE"
        if action != "CHECK_IDENTITY":
            anchors = [i["const"] for i in p["depends_on"]["prefixItems"]]
            assert caps["identity_steps"][target] in anchors
            assert p["step_id"]["const"] not in p["depends_on"]["items"]["enum"]
            if action == "VERIFY_PEER_MAPPING":
                assert len(anchors) == 2
        if action == "CHECK_CONFIGURATION":
            refs = schema["$defs"][p["evidence"]["items"]["$ref"].split("/")[-1]]["anyOf"]
            assert p["evidence"]["minItems"] == 1
            assert all(
                evidence[r["const"]["evidence_id"]].category == "K"
                and evidence[r["const"]["evidence_id"]].object_id == target
                for r in refs
            )


def test_wrong_version_cannot_be_used_by_candidate_and_legacy_slots_stay_frozen(tmp_path):
    task, _, bindings, caps = inputs(tmp_path / "case", 5)
    assert caps["admissible_ids"] == []
    header = {"target_objects": task.objects}
    old = generation_schema(bindings, header, capabilities=caps, task=task)
    before = json.dumps(old, sort_keys=True)
    candidate = candidate_schema(bindings, header, capabilities=caps, task=task)
    assert (
        json.dumps(
            generation_schema(bindings, header, capabilities=caps, task=task), sort_keys=True
        )
        == before
    )
    assert "prefixItems" in old["properties"]["steps"]
    assert "prefixItems" not in candidate["properties"]["steps"]
    for branch in candidate["$defs"]["PlanStep"]["anyOf"]:
        assert branch["properties"]["action_type"]["const"] != "CHECK_CONFIGURATION"
        assert branch["properties"]["evidence"]["maxItems"] == 0


def test_candidate_preserves_raw_reply_and_does_not_insert_reference_coverage(tmp_path):
    task, context, bindings, _ = inputs(tmp_path / "case")

    class Client:
        model = SimpleNamespace(id="unit-fixture-only")

        def compile_candidate_schema(self, schema):
            assert "prefixItems" not in schema["properties"]["steps"]
            return "fixture-only grammar"

        def complete(self, messages, **kwargs):
            self.messages, self.kwargs = messages, kwargs
            return {"content": "not valid JSON; preserve this failure", "finish_reason": "stop"}

    client = Client()
    raw = generate_bounded_plan(
        "fixture", task, context, bindings, client, source_root=tmp_path / "case"
    )
    assert raw.content == "not valid JSON; preserve this failure"
    body = json.loads(client.messages[1]["content"])
    assert "task_workflow" not in body and "gold" not in body and "reference" not in body
    assert client.kwargs["operation"] == "bounded_plan_head_candidate"
    assert client.kwargs["response_grammar"] == "fixture-only grammar"


def test_compact_grammar_is_the_actual_counted_request_and_schema_grammar_are_exclusive(tmp_path):
    task, _, _, _ = inputs(tmp_path / "case")
    collector = MetricCollector(task.run_id)
    budget = PlanBudget(task, collector)
    posted, traces = [], []

    def reply(request):
        posted.append(json.loads(request.content))
        return httpx.Response(
            200,
            json={
                "choices": [{"message": {"content": "{}"}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 2},
            },
        )

    model = load_model_config(PROJECT / "config/models.yaml").generation["baseline"]
    with ObservedPlanClient(
        model, collector, budget, transport=httpx.MockTransport(reply), sink=traces.append
    ) as client:
        client.complete([], operation="fixture-only", response_grammar='root ::= "{}"')
        with pytest.raises(ValueError, match="not both"):
            client.complete(
                [],
                operation="fixture-only",
                response_grammar='root ::= "{}"',
                response_schema={"type": "object"},
            )
    assert len(posted) == 1 and posted[0] == traces[0]["request"]
    assert posted[0]["structured_outputs"] == {"grammar": 'root ::= "{}"'}
    assert "response_format" not in posted[0]
    assert collector.summary()["invocations"]["model"]["attempted"] == 1


@pytest.fixture
def packet(monkeypatch):
    monkeypatch.syspath_prepend(str(PROJECT / "scripts"))
    return importlib.import_module("v8_e1_validation_packet")


def single_case(tmp_path):
    root = tmp_path / "dataset"
    source = PROJECT / "eval/v8/e1/validation/E1-CAL-N001"
    shutil.copytree(source, root / "validation/E1-CAL-N001")
    return root


def test_validation_loader_rejects_heldout_mislabelling_before_normal_data(packet, tmp_path):
    root = single_case(tmp_path)
    path = root / "validation/E1-CAL-N001/case.json"
    body = json.loads(path.read_text())
    body["split"] = "heldout"
    path.write_text(json.dumps(body))
    with pytest.raises(ValueError, match="split disagree"):
        packet.validation_cases(root)


def test_validation_loader_rejects_raw_tampering(packet, tmp_path):
    root = single_case(tmp_path)
    path = root / "validation/E1-CAL-N001/visible/data/raw/snapshot.json"
    path.write_text(path.read_text() + " ")
    with pytest.raises(ValueError, match="raw source hash mismatch"):
        packet.validation_cases(root)


def test_fault_readback_requires_actual_impaired_probe_and_direction_counter(packet):
    snapshot = {"normal_probe": {"returncode": 1}}
    external = {
        "input": {"returncode": 0, "stdout": " 5 420 DROP icmp -- ogstun * 0/0 0/0 icmptype 8\n"}
    }
    assert packet.verify_condition("inner-request-filter", snapshot, external)
    snapshot["normal_probe"]["returncode"] = 0
    assert not packet.verify_condition("inner-request-filter", snapshot, external)
    snapshot["normal_probe"]["returncode"] = 1
    external["input"]["stdout"] = " 0 0 DROP icmp -- ogstun * 0/0 0/0 icmptype 8\n"
    assert not packet.verify_condition("inner-request-filter", snapshot, external)
