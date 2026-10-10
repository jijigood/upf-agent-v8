import json

import httpx
import pytest

from upf_agent.config import load_model_config
from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.e6 import PERTURBATIONS, TEMPERATURE, perturb, sampled_factory
from upf_agent.v8.experiment_metrics import MetricCollector
from upf_agent.v8.models import digest
from upf_agent.v8.plan_cases import prepare_case
from upf_agent.v8.plan_generator import PlanBudget


@pytest.mark.parametrize("index", [0, 3, 7, 16, 19, 23])
@pytest.mark.parametrize("kind", PERTURBATIONS)
def test_perturbation_rebinds_all_sources_without_changing_facts(tmp_path, index, kind):
    task, gold = prepare_case(tmp_path / "case", index)
    root = tmp_path / "case"
    constraints = digest([task.permission, task.path.positions, task.version, task.as_of])
    branches = digest(gold.any_of)
    proof = perturb(root, task, gold, kind)
    assert proof["facts_equal"]
    assert not proof["human_semantic_reviewed"]
    assert digest([task.permission, task.path.positions, task.version, task.as_of]) == constraints
    assert digest(gold.any_of) == branches
    assert not gold.reviewed
    compile_contract(task)
    body = json.loads((root / task.observation_files[0]).read_text())
    registry = json.loads((root / "data/v8/knowledge_applicability.json").read_text())
    for a in registry["annotations"]:
        row = body["observations"][int(a["locator"].rsplit("/", 1)[1])]
        assert row["category"] == "K"
        assert a["source_sha256"] == task.path.source_sha256
        assert a["object_ids"] == [row["object_id"]]


def test_sampling_applies_to_head_and_planner_http_requests(tmp_path):
    from pathlib import Path

    task, _ = prepare_case(tmp_path / "case", 0)
    collector = MetricCollector(task.run_id)
    budget = PlanBudget(task, collector)
    model = load_model_config(
        Path(__file__).resolve().parents[1] / "config/models.yaml"
    ).generation["baseline"]
    requests = []

    def respond(request):
        requests.append(json.loads(request.content))
        return httpx.Response(
            200,
            json={
                "choices": [{"message": {"content": "{}"}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 1, "completion_tokens": 1},
            },
        )

    with sampled_factory(1104)(
        model, collector, budget, transport=httpx.MockTransport(respond)
    ) as client:
        for operation in ["p5_plan", "common_plan_head"]:
            client.complete([{"role": "user", "content": "bounded test"}], operation=operation)
    assert len(requests) == 2
    assert all(r["seed"] == 1104 and r["temperature"] == TEMPERATURE for r in requests)
