"""Opt-in production Engine using the same public category tools as native P5."""

import json
from time import perf_counter

from upf_agent.agent_contracts import AgentTask, ToolCall
from upf_agent.contracts import TaskType
from upf_agent.v8.e3 import METHODS, RoundEvidenceBackend
from upf_agent.v8.e3_p5 import PublishedEvidenceTools
from upf_agent.v8.engine import OrchestrationEngine
from upf_agent.v8.experiment_metrics import MetricCollector
from upf_agent.v8.models import OrchestrationData, QueryPlan, QueryStep, digest
from upf_agent.v8.phase1 import write_json
from upf_agent.v8.plan_generator import PlanBudget
from upf_agent.v8.store import BudgetStop


def publication_generation(publication):
    return digest(
        [
            publication["file"],
            publication["sha256"],
            publication["available"],
            "e3-public-category-service",
        ]
    )[:20]


def public_steps(task, contract, gaps=None):
    wanted = (
        {r.requirement_id for r in contract.requirements if r.kind in {"K", "R", "P"}}
        if gaps is None
        else {g.requirement_id for g in gaps if g.route != "human"}
    )
    result = []
    knowledge = [
        r.requirement_id
        for r in contract.requirements
        if r.kind == "K" and r.requirement_id in wanted
    ]
    if knowledge:
        result.append(
            QueryStep(
                step_id="public:K:all",
                requirement_ids=knowledge,
                tool="search_manual",
                object_id=task.objects[0],
                arguments={"query": task.question},
                capability="e3-public-category-service",
            )
        )
    for kind, name in [("R", "analyze_log_window"), ("P", "lookup_topology")]:
        for obj in task.objects:
            ids = [
                r.requirement_id
                for r in contract.requirements
                if r.kind == kind and r.requirement_id in wanted and obj in r.objects
            ]
            if ids:
                result.append(
                    QueryStep(
                        step_id=f"public:{kind}:{obj}",
                        requirement_ids=ids,
                        tool=name,
                        object_id=obj,
                        arguments={"device_id": obj},
                        capability="e3-public-category-service",
                    )
                )
    return result


class PublishedSourceEngine(OrchestrationEngine):
    """Explicit dependency injection; the default production Engine remains unchanged."""

    def __init__(self, root, method):
        if method not in {METHODS[0], METHODS[1], METHODS[3]}:
            raise ValueError("native P5 uses its own graph")
        super().__init__(root)
        self.method = method
        self.staged = None
        self.tools = None
        self.attempted = {}

    def _execution_fingerprint(self):
        catalog = json.loads((self.root / "publication-catalog.json").read_text())
        return digest(
            [super()._execution_fingerprint(), catalog, self.method, "e3-public-engine-1"]
        )

    def _compile(self, state):
        compiled = super()._compile(state)
        data = OrchestrationData.model_validate(compiled["payload"])
        if data.task.graph_enabled:
            raise ValueError("E3 public tool experiment requires explicit graph_enabled=false")
        self.staged = RoundEvidenceBackend(self.root, data.task, data.contract)

        def append(event):
            with (self.root / "dispatch-events.jsonl").open("a") as stream:
                stream.write(json.dumps(event, ensure_ascii=False) + "\n")

        collector = MetricCollector(data.task.run_id, sink=append)
        self.tools = PublishedEvidenceTools(self.staged, PlanBudget(data.task, collector))
        data.query_plan = QueryPlan(
            contract_id=data.contract.contract_id,
            steps=public_steps(data.task, data.contract),
            gaps=[],
        )
        return {"payload": data.model_dump(mode="json")}

    def _collect(self, state):
        data = OrchestrationData.model_validate(state["payload"])
        self.staged.round = data.rounds
        if data.stop_reason:
            return state
        generation = publication_generation(self.staged.publication)
        for step in data.query_plan.steps:
            args = dict(step.arguments)
            if step.tool == "analyze_log_window":
                args["log_id"] = generation
            elif step.tool == "lookup_topology":
                args["topology_id"] = generation
            call = ToolCall(name=step.tool, arguments=args)
            scoped = AgentTask(
                run_id=data.task.run_id,
                question=data.task.question,
                task_type=TaskType.DIAGNOSE,
                device_ids=data.task.objects if step.tool == "search_manual" else [step.object_id],
                product=data.task.product,
                version=data.task.version,
                log_generation=generation,
                manual_generation=generation,
                topology_generation=generation,
                time_window=data.task.time_window,
            )
            try:
                # Check before reserving a Ledger receipt; rejected attempts cannot stay pending.
                self.tools.budget.check("tool", call.model_dump(mode="json"))
                self.tools.tool(scoped, call, [], self.tools.budget.remaining())
            except (TimeoutError, BudgetStop):
                data.stop_reason = "shared_tool_or_time_budget_exhausted"
                break
            for rid in step.requirement_ids:
                self.attempted[(step.tool, step.object_id, rid)] = (
                    self.staged.publication["file"],
                    self.staged.publication["available"],
                )
        data.bindings = self.staged.ledger.evidence(data.task.run_id)
        data.status = "collected"
        return {"payload": data.model_dump(mode="json")}

    def _route(self, state):
        data = OrchestrationData.model_validate(state["payload"])
        if (
            self.method == METHODS[0]
            or not data.gaps
            or data.stop_reason
            or data.rounds >= data.task.budget.max_rounds
        ):
            return "report"
        return "supplement"

    def _supplement(self, state):
        data = OrchestrationData.model_validate(state["payload"])
        data.rounds += 1
        publication = self.staged.catalog[data.rounds]
        steps = public_steps(
            data.task, data.contract, None if self.method == METHODS[1] else data.gaps
        )
        if self.method == METHODS[3]:
            steps = [
                s
                for s in steps
                if any(
                    self.attempted.get((s.tool, s.object_id, rid))
                    != (publication["file"], publication["available"])
                    for rid in s.requirement_ids
                )
            ]
        data.query_plan = QueryPlan(contract_id=data.contract.contract_id, steps=steps, gaps=[])
        return {"payload": data.model_dump(mode="json")}

    def _evaluate(self, state):
        evaluated = super()._evaluate(state)
        data = OrchestrationData.model_validate(evaluated["payload"])
        self.staged.evaluate()
        # Two actual evaluators with different batch IDs must agree on domain semantics.
        left = {rid: (s.code, s.valid, s.reasons) for rid, s in data.states.items()}
        right = {rid: (s.code, s.valid, s.reasons) for rid, s in self.staged.local.states.items()}
        equal = left == right
        self.staged.history.append(
            {
                "round": data.rounds,
                "event": "production_engine_semantic_comparison",
                "equal": equal,
                "production_batch": data.batch_id,
            }
        )
        if not equal:
            raise ValueError("production Engine differs from independent publication evaluator")
        return evaluated

    def close(self):
        if self.staged and self.staged.ledger is not None:
            self.staged.ledger.close()
        super().close()


def run_public_engine(root, task, contract, reference, method):
    task = task.model_copy(deep=True)
    task.graph_enabled = False
    engine = PublishedSourceEngine(root, method)
    started = perf_counter()
    try:
        native = engine.run(task)
        staged = engine.staged
        stop = (
            "no_supplement"
            if method == METHODS[0]
            else "closed"
            if not native["gaps"]
            else "round_budget"
            if native["rounds"] >= task.budget.max_rounds
            else "no_new_permitted_capability"
        )
        if native.get("stop_reason") == "shared_tool_or_time_budget_exhausted":
            stop = "tool_budget"
        summary = engine.tools.budget.collector.summary()
        result = staged.finish(
            stop,
            reference,
            perf_counter() - started,
            {
                "model_calls": 0,
                "production_engine": True,
                "shared_public_tool_units": True,
                "public_task_constraints": True,
                "dispatcher_metrics": summary,
                "engine_stop_reason": native.get("stop_reason"),
            },
        )
        result["correct_stop"] = bool(
            not reference["solvable"]
            and not result["primary_closed"]
            and result["budget_ok"]
            and not result["uncommitted_tool_receipts"]
        )
        write_json(root / "result.json", result)
        return result
    finally:
        engine.close()
