"""Actual native P5 LangGraph on the E3 immutable publication service."""

import json
from time import perf_counter

from upf_agent.agent_contracts import AgentTask
from upf_agent.agent_engine import run_agent
from upf_agent.agent_tools import failure
from upf_agent.config import load_model_config
from upf_agent.contracts import TaskType
from upf_agent.v8.common_tools import CommonEvidenceTools
from upf_agent.v8.compiler import permitted
from upf_agent.v8.e3 import RoundEvidenceBackend
from upf_agent.v8.models import digest
from upf_agent.v8.p5_plan_runner import P5CommonBackend
from upf_agent.v8.plan_generator import ObservedPlanClient, PlanBudget


class PublishedEvidenceTools(CommonEvidenceTools):
    def __init__(self, staged, budget):
        super().__init__(staged.root, staged.task, staged.contract, budget)
        self.staged = staged

    def _rows(self):
        body = self.staged.read_body()
        item = self.staged.publication
        for index, record in enumerate(body.get("observations", [])):
            if not permitted(self.task, record.get("object_id"), []):
                continue
            visible = {
                **record,
                "fields": {
                    k: v
                    for k, v in record["fields"].items()
                    if k in self.task.permission.readable_fields
                },
            }
            yield item["file"], body, index, visible, item["sha256"]

    def tool(self, task, call, known, timeout):
        staged = self.staged
        request = call.model_dump(mode="json") | {"publication": staged.publication}
        key = digest([request, len(staged.calls)])
        staged.ledger.charge(staged.task, key, "tool", request)
        started = perf_counter()
        if not staged.publication["available"]:
            self.budget.check("tool", request)
            with self.budget.collector.measure("tool", call.name, request) as metric:
                # ToolPacket uses the native error vocabulary; availability is source metadata.
                metric["error_type"] = "tool_failed"
                packet = failure("tool_failed", "declared evidence service unavailable")
        else:
            packet = super().tool(task, call, known, timeout)
        entry_ids = {e.evidence_id for e in packet.evidence}
        returned = [
            b.model_copy(deep=True) for b in self.bindings.values() if b.receipt_id in entry_ids
        ]
        staged.commit(
            key,
            request,
            {"gaps": packet.gaps, "packet": packet.model_dump(mode="json")},
            returned,
            perf_counter() - started,
        )
        return packet


class PublishedP5Backend(P5CommonBackend):
    def __init__(self, tools, client, *, shared_public_tools=False):
        self.shared_public_tools = shared_public_tools

        class PublicCatalogClient:
            def complete(self, messages, **kwargs):
                context = json.loads(messages[1]["content"])
                # Same capability schedule available to T1/T3, with no future record contents.
                context["source_publication_catalog"] = tools.staged.catalog
                context["current_source_publication"] = tools.staged.publication
                if shared_public_tools:
                    context["public_task_constraints"] = {
                        "evaluation_as_of": tools.task.as_of.isoformat(),
                        "freshness_seconds": 300,
                        "version": tools.task.version,
                        "unknown_timezone": "unknown; do not infer offsets",
                        "source_generation_policy": (
                            "generation changes only when edition or availability changes"
                        ),
                    }
                messages = [
                    messages[0],
                    {**messages[1], "content": json.dumps(context, ensure_ascii=False)},
                ]
                if shared_public_tools:
                    # E3 has no final plan head; the full shared eight-request ceiling applies.
                    kwargs["reserve_head"] = False
                return client.complete(messages, **kwargs)

        super().__init__(tools, PublicCatalogClient())

    def model(self, operation, data, timeout, allowance, repair=None):
        self.tools.staged.round = min(data.rounds, self.tools.task.budget.max_rounds)
        if self.shared_public_tools:
            from upf_agent.v8.e3_public import publication_generation

            generation = publication_generation(self.tools.staged.publication)
            data.task.log_generation = generation
            data.task.manual_generation = generation
            data.task.topology_generation = generation
        # Source release follows native planning rounds. Repairs keep the same round.
        return super().model(operation, data, timeout, allowance, repair)


def run_native_p5(project, root, task, contract, reference, *, shared_public_tools=False):
    from upf_agent.v8.experiment_metrics import MetricCollector

    staged = RoundEvidenceBackend(root, task, contract)
    events_path, trace_path = root / "dispatch-events.jsonl", root / "model-traces.jsonl"

    def append(path, value):
        with path.open("a") as stream:
            stream.write(json.dumps(value, ensure_ascii=False) + "\n")

    collector = MetricCollector(task.run_id, sink=lambda value: append(events_path, value))
    budget = PlanBudget(task, collector)
    tools = PublishedEvidenceTools(staged, budget)
    generation = digest([task.observation_files, "e3-publication-service-1"])[:20]
    if shared_public_tools:
        from upf_agent.v8.e3_public import publication_generation

        generation = publication_generation(staged.publication)
    native_task = AgentTask(
        run_id=task.run_id,
        question=task.question,
        task_type=TaskType.DIAGNOSE,
        device_ids=[],
        product=task.product,
        version=task.version,
        mode="agent",
        retrieval_device="cpu",
        budget=task.budget.model_copy(
            update={
                "max_model_calls": task.budget.max_model_calls
                if shared_public_tools
                else task.budget.max_model_calls - 1
            }
        ),
        log_generation=generation,
        manual_generation=generation,
        topology_generation=generation,
        time_window=task.time_window,
    )
    model = load_model_config(project / "config/models.yaml").generation[task.model_profile]
    started = perf_counter()
    native, error = None, None
    try:
        with ObservedPlanClient(
            model, collector, budget, sink=lambda value: append(trace_path, value)
        ) as client:
            native = run_agent(
                root,
                native_task,
                backend=PublishedP5Backend(tools, client, shared_public_tools=shared_public_tools),
            )
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    measured = collector.summary()
    extra = {
        "model_calls": measured["invocations"]["model"]["attempted"],
        "dispatcher_metrics": measured,
        "native_error": error,
        "native_state": native.model_dump(mode="json") if native else None,
        "model": model.model_dump(mode="json"),
        "unused_common_head_reservation": 0 if shared_public_tools else 1,
        "p5_graph_and_cache_modified": False,
        "shared_public_tool_units": shared_public_tools,
        "public_task_constraints": shared_public_tools,
        "source_generations_follow_publications": shared_public_tools,
    }
    return staged.finish(
        "native_error" if error else "native_termination",
        reference,
        perf_counter() - started,
        extra,
    )
