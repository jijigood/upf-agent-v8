"""Opt-in E3 development harness: immutable publications, actual compiler/Ledger/rules.

The publication schedule is public capability metadata, never an evaluator oracle.
Default Engine and the native P5 graph/cache are unchanged. References are unreviewed.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import timedelta
from time import perf_counter

from upf_agent.v8.adapters import read_observation, verify_binding
from upf_agent.v8.compiler import compile_contract, compile_gap_plan, compile_query_plan
from upf_agent.v8.dependency import LocalEvaluator, complete_results
from upf_agent.v8.e4 import FullEvaluator, write_json
from upf_agent.v8.evaluator import route_gaps
from upf_agent.v8.experiment_manifest import source_manifest
from upf_agent.v8.fixtures import example
from upf_agent.v8.knowledge_applicability import (
    KnowledgeAnnotation,
    KnowledgeRegistry,
    annotate_knowledge,
)
from upf_agent.v8.models import OrchestrationData, digest
from upf_agent.v8.store import Ledger

FAMILIES = (
    "knowledge-version-unknown",
    "runtime-timezone-unknown",
    "stale",
    "one-side-missing",
    "boundary-conflict",
    "permission-denied",
    "tool-unavailable",
    "no-source-exists",
)
METHODS = ("T0-no-supplement", "T1-full-refresh", "T2-native-P5", "T3-typed")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_case(root, family, variant):
    if root.exists() or family not in FAMILIES or variant not in range(4):
        raise ValueError("invalid/new case required")
    root.mkdir(parents=True)
    case_id = f"e3-{FAMILIES.index(family) * 4 + variant + 1:02d}"
    task = example(root, name=case_id)
    task.run_id = digest([case_id, "e3-dev-publication-1"])[:32]
    task.retrieval_device = "cpu"
    # Distinct physical development inputs; the eight underlying families remain correlated.
    original = json.loads((root / task.observation_files[0]).read_text())
    for record in original["observations"]:
        record["slot_id"] = f"{record['category']}:{record['object_id']}"
        record["fields"].update({"scenario_tag": case_id})
        if record["category"] == "K":
            record["fields"]["instruction"] += f"；开发情景 {case_id}，保持只读"
    primary = (
        "K:UPF-A"
        if family == FAMILIES[0]
        else ("P:UPF-A:SMF-B" if family in {"one-side-missing", "boundary-conflict"} else "R:UPF-A")
    )
    solvable = variant < 2 and family not in {"permission-denied", "no-source-exists"}
    repair_round = variant + 1 if solvable else None
    if family == "permission-denied":
        task.permission.readable_fields.remove("n4_enabled")
    snapshots, editions, annotations = {}, [], []
    catalog = []
    for round_number in range(4):
        body = json.loads(json.dumps(original))
        repaired = solvable and round_number >= repair_round
        deceptive = variant == 3 and round_number >= 1
        available = True
        if not repaired:
            for record in body["observations"]:
                if record["object_id"] != "UPF-A":
                    continue
                if family == "knowledge-version-unknown" and record["category"] == "K":
                    record["version"] = "4.0" if deceptive else None
                elif family == "runtime-timezone-unknown" and record["category"] == "R":
                    record["raw_local_timestamp"] = "2026-10-07 00:00:00 (offset unspecified)"
                    record["observed"] = None
                    if deceptive:
                        record["version"] = "4.0"
                elif family == "stale" and record["category"] == "R":
                    for key, offset in (("start", 7200), ("end", 3600)):
                        record["observed"][key] = (
                            task.as_of - timedelta(seconds=offset)
                        ).isoformat()
                    if deceptive:
                        record["observed"] = original["observations"][1]["observed"]
                        record["version"] = "4.0"
                elif family == "boundary-conflict" and record["category"] == "P":
                    record["fields"]["peer_endpoint"] = "192.0.2.99"
                    if deceptive:
                        record["fields"]["peer_endpoint"] = "192.0.2.2"
                        record["config_version"] = "cfg-other"
            if family == "one-side-missing":
                body["observations"] = [
                    r for r in body["observations"] if r["slot_id"] != "P:SMF-B"
                ]
                if deceptive:
                    peer = json.loads(json.dumps(original["observations"][-1]))
                    peer["version"] = "4.0"
                    body["observations"].append(peer)
            if family == "tool-unavailable":
                available = False
            if family == "no-source-exists":
                body["observations"] = []
        signature = digest(body)
        if signature not in snapshots:
            edition = len(snapshots) + 1
            relative = f"data/publications/edition-{edition}.json"
            # A declared complete publication supersedes the same logical observation slots.
            body["publication"] = {
                "edition": edition,
                "complete": True,
                "supersedes": edition - 1 or None,
            }
            write_json(root / relative, body)
            snapshots[signature] = (relative, edition)
            editions.append(relative)
            file_sha = sha(root / relative)
            for index, record in enumerate(body["observations"]):
                if record["category"] != "K" or not record.get("version"):
                    continue
                annotations.append(
                    KnowledgeAnnotation(
                        annotation_id=f"{case_id}-edition-{edition}-k-{index}",
                        source_sha256=file_sha,
                        locator=f"/observations/{index}",
                        content_sha256=hashlib.sha256(
                            record["fields"]["instruction"].encode()
                        ).hexdigest(),
                        product=record["product"],
                        version=record["version"],
                        object_ids=[record["object_id"]],
                        purposes=[task.template],
                        basis_kind="trusted_rule",
                        basis_source="explicit synthetic publication specification",
                        basis_version="1",
                        rule_id="e3-exact-synthetic-purpose-1",
                        reviewed=False,
                    )
                )
        relative, edition = snapshots[signature]
        catalog.append(
            {
                "round": round_number,
                "file": relative,
                "edition": edition,
                "available": available,
                "sha256": sha(root / relative),
            }
        )
    task.observation_files = editions
    task.question = (
        f"只读排查开发情景 {case_id}：核对 UPF-A 与 SMF-B 的接口、配置、手册与双侧映射。"
        "证据服务在调查轮次0/1/2/3开放已登记的完整发布版；同一观察槽的新完整发布版明确替代旧版。"
        "不要推断未知时区、版本或被拒绝字段；没有可用来源则保留缺口并停止。"
    )
    contract = compile_contract(task)
    write_json(root / "task.json", task.model_dump(mode="json"))
    write_json(root / "contract.json", contract.model_dump(mode="json"))
    write_json(root / "publication-catalog.json", catalog)
    write_json(
        root / "data/v8/knowledge_applicability.json",
        KnowledgeRegistry(version=f"{case_id}-1", annotations=annotations).model_dump(mode="json"),
    )
    reference = {
        "case_id": case_id,
        "family": family,
        "variant": variant,
        "primary_requirement": primary,
        "solvable": solvable,
        "repair_round": repair_round,
        "synthetic": True,
        "reviewed": False,
        "source_family": "example-v8-N4-1",
        "mode": ("round1", "round2", "permanent", "invalid-repair")[variant],
        "scope_note": "permissions and evaluation time never change",
    }
    write_json(root / "development-reference.json", reference)
    return task, contract, reference


class RoundEvidenceBackend:
    """Only the selected immutable publication reaches adapters, plus actual revision commits."""

    def __init__(self, root, task, contract):
        self.root, self.task, self.contract = root, task, contract
        self.catalog = json.loads((root / "publication-catalog.json").read_text())
        self.round = 0
        self.ledger = Ledger(root)
        self.ledger.create(task)
        self.calls = []
        self.local = None
        self.history = []
        self.seen_valid_fields = set()
        self.successful_queries = set()

    @property
    def publication(self):
        return self.catalog[self.round]

    def read_body(self):
        item = self.publication
        path = self.root / item["file"]
        if sha(path) != item["sha256"]:
            raise ValueError("frozen publication changed")
        if item["file"] not in self.task.observation_files:
            raise ValueError("publication outside declared sources")
        return json.loads(path.read_text())

    def normalize(self, bindings, receipt):
        result = []
        body = self.read_body()
        prior = {b.evidence_id: b for b in self.ledger.evidence(self.task.run_id)}
        for binding in bindings:
            if binding.source.relative_path != self.publication["file"] or not verify_binding(
                self.root, binding
            ):
                raise ValueError("future/changed publication rejected")
            record = body["observations"][int(binding.source.locator.rsplit("/", 1)[-1])]
            binding.evidence_id = digest(
                [self.task.run_id, binding.requirement_id, record["slot_id"]]
            )
            binding.revision = self.publication["edition"]
            binding.receipt_id = receipt
            # All methods project explicit physical K windows identically; never infer missing time.
            binding.observed = record.get("observed")
            binding.fields = {
                f: v for f, v in binding.fields.items() if f in self.task.permission.readable_fields
            }
            if binding.category == "K":
                annotate_knowledge(self.root, binding)
            previous = prior.get(binding.evidence_id)
            if previous is not None and previous.revision == binding.revision:
                if previous.model_dump(exclude={"receipt_id"}) != binding.model_dump(
                    exclude={"receipt_id"}
                ):
                    raise ValueError("same publication slot cannot be rebound")
                # Query receipts stay separate; immutable evidence retains its first provenance.
                binding = previous
            result.append(binding)
        return result

    def evaluate(self):
        bindings = self.ledger.evidence(self.task.run_id)
        batch = digest([self.task.run_id, self.round, bindings])[:24]
        if self.local is None:
            self.local = LocalEvaluator(self.task, self.contract, bindings, batch=batch)
            update = {"initial_cost": self.local.initial_cost}
        else:
            update = self.local.update(bindings, batch)
        full = FullEvaluator(self.task, self.contract, bindings, None, batch=batch)
        equal = complete_results(self.local.states, self.local.actions) == complete_results(
            full.states, full.actions
        )
        if not equal:
            raise AssertionError("Local/Full complete certification mismatch")
        gaps = route_gaps(self.contract, self.local.states)
        self.ledger.save(
            OrchestrationData(
                task=self.task,
                contract=self.contract,
                bindings=bindings,
                states=self.local.states,
                actions=list(self.local.actions.values()),
                gaps=gaps,
                batch_id=batch,
                rounds=self.round,
                status="completed" if not gaps else "needs_evidence",
            ),
            dependencies={"initial_audit": self.local.initial_audit},
            update=update,
        )
        valid = set()
        reqs = {r.requirement_id: r for r in self.contract.requirements}
        for b in bindings:
            if self.local.states[b.requirement_id].valid:
                valid.update(
                    (b.object_id, b.category, f, digest(v))
                    for f, v in b.fields.items()
                    if f in reqs[b.requirement_id].fields
                )
        new = valid - self.seen_valid_fields
        self.seen_valid_fields |= valid
        self.history.append(
            {
                "round": self.round,
                "batch": batch,
                "full_local_equal": equal,
                "new_valid_fields": len(new),
                "states": {k: v.model_dump(mode="json") for k, v in self.local.states.items()},
                "gaps": [g.model_dump(mode="json") for g in gaps],
                "update": update,
            }
        )
        return gaps

    def commit(self, key, request, raw, bindings, elapsed):
        bindings = self.normalize(bindings, key) if bindings else []
        before = len(self.seen_valid_fields)
        self.ledger.commit_receipt(self.task, key, raw, bindings, elapsed)
        self.evaluate()
        query_identity = digest(
            [
                request.get("tool") or request.get("name"),
                request.get("object_id") or request.get("arguments", {}).get("device_id"),
                sorted(request.get("requirement_ids", [])),
                request.get("arguments", {}),
                self.publication["sha256"],
                self.publication["available"],
            ]
        )
        successful = bool(bindings) and not raw.get("gaps")
        redundant = successful and query_identity in self.successful_queries
        if successful:
            self.successful_queries.add(query_identity)
        self.calls.append(
            {
                "round": self.round,
                "request": request,
                "edition": self.publication["edition"],
                "available": self.publication["available"],
                "returned_bindings": len(bindings),
                "new_valid_fields": len(self.seen_valid_fields) - before,
                "elapsed_seconds": elapsed,
                "gaps": raw.get("gaps", []),
                "redundant_query": redundant,
            }
        )

    def collect(self, step):
        request = step.model_dump(mode="json") | {"publication": self.publication}
        key = digest(request)
        prior = self.ledger.charge(self.task, key, "tool", request)
        if prior is not None:
            return
        started = perf_counter()
        if not self.publication["available"]:
            bindings, gaps = [], ["tool_unavailable"]
        else:
            scoped = step.model_copy(deep=True)
            scoped.arguments["files"] = [self.publication["file"]]
            # Validate the frozen bytes before the existing adapter reads them.
            self.read_body()
            bindings, gaps = read_observation(self.root, self.task, self.contract, scoped, key)
        self.commit(
            key,
            request,
            {"gaps": gaps, "bindings": [b.model_dump(mode="json") for b in bindings]},
            bindings,
            perf_counter() - started,
        )

    def finish(self, stop_reason, reference, elapsed, extra=None):
        gaps = self.evaluate()
        closed = self.local.states[reference["primary_requirement"]].valid
        metrics = self.ledger.metrics(self.task.run_id)
        tool_attempts = metrics["invocations"]["tool"]["attempted"]
        uncommitted = tool_attempts - len(self.calls)
        result = {
            "case_id": reference["case_id"],
            "synthetic": True,
            "reviewed": False,
            "primary_closed": closed,
            "all_closed": not gaps,
            "false_closure": closed and not reference["solvable"],
            "correct_stop": (
                not reference["solvable"]
                and not closed
                and stop_reason
                in {
                    "no_supplement",
                    "round_budget",
                    "no_new_permitted_capability",
                    "native_termination",
                }
                and elapsed <= self.task.budget.timeout_seconds
                and uncommitted == 0
            ),
            "stop_reason": stop_reason,
            "rounds": self.round,
            "elapsed_seconds": elapsed,
            "calls": self.calls,
            "tool_calls": tool_attempts,
            "committed_tool_calls": len(self.calls),
            "uncommitted_tool_receipts": uncommitted,
            "new_valid_fields": len(self.seen_valid_fields),
            "redundant_queries": sum(c["redundant_query"] for c in self.calls),
            "new_valid_fields_per_tool_call": len(self.seen_valid_fields) / len(self.calls)
            if self.calls
            else None,
            "history": self.history,
            "ledger_metrics": metrics,
            "execute_authorized": False,
            "model_calls": 0,
        }
        result.update(extra or {})
        result["budget_ok"] = (
            result["tool_calls"] <= self.task.budget.max_tool_calls
            and result["model_calls"] <= self.task.budget.max_model_calls
            and elapsed <= self.task.budget.timeout_seconds
        )
        write_json(self.root / "result.json", result)
        self.ledger.close()
        return result


def deduplicate_steps(steps):
    merged = {}
    for step in steps:
        key = (step.tool, step.object_id)
        if key not in merged:
            merged[key] = step.model_copy(deep=True)
        else:
            merged[key].requirement_ids = sorted(
                set(merged[key].requirement_ids + step.requirement_ids)
            )
    return list(merged.values())


def run_deterministic(root, task, contract, reference, method):
    if method not in {METHODS[0], METHODS[1], METHODS[3]}:
        raise ValueError("native P5 must use its real graph/model runner")
    backend = RoundEvidenceBackend(root, task, contract)
    started = perf_counter()
    for step in compile_query_plan(task, contract).steps:
        backend.collect(step)
    gaps = backend.evaluate()
    stop = "no_supplement" if method == METHODS[0] else "closed"
    attempted = {
        (s.tool, s.object_id, rid): backend.publication
        for s in compile_query_plan(task, contract).steps
        for rid in s.requirement_ids
    }
    if method != METHODS[0] and gaps:
        for round_number in range(1, task.budget.max_rounds + 1):
            backend.round = round_number
            if method == METHODS[1]:
                steps = compile_query_plan(task, contract).steps
            else:
                # Round itself isn't a new source; compare publication content and availability.
                needed = {}
                for gap in gaps:
                    if gap.route != "human":
                        for obj in gap.objects:
                            needed.setdefault(("read_observation", obj), set()).add(
                                gap.requirement_id
                            )
                blocked = {
                    pair
                    for pair, requirements in needed.items()
                    if all(
                        (old := attempted.get((*pair, rid))) is not None
                        and (old["file"], old["available"])
                        == (backend.publication["file"], backend.publication["available"])
                        for rid in requirements
                    )
                }
                steps = deduplicate_steps(compile_gap_plan(task, contract, gaps, blocked).steps)
            if not steps:
                future_change = any(
                    (p["file"], p["available"])
                    != (backend.publication["file"], backend.publication["available"])
                    for p in backend.catalog[round_number + 1 :]
                )
                if future_change:
                    backend.history.append(
                        {
                            "round": round_number,
                            "event": "wait_for_declared_publication",
                            "tool_calls": 0,
                        }
                    )
                    continue
                stop = "no_new_permitted_capability"
                break
            for step in steps:
                backend.collect(step)
                for rid in step.requirement_ids:
                    attempted[(step.tool, step.object_id, rid)] = backend.publication
            gaps = backend.evaluate()
            if not gaps:
                stop = "closed"
                break
            stop = "round_budget"
    return backend.finish(stop, reference, perf_counter() - started)


def run_e3(project, output, *, native_p5=False, shared_public_tools=False):
    if output.exists() or not output.resolve().is_relative_to((project / "runtime").resolve()):
        raise ValueError("new output inside project/runtime required")
    output.mkdir(parents=True)
    from pathlib import Path

    measured_source = Path(__file__).resolve().parents[3]
    source = source_manifest(measured_source)
    cases = []
    for family in FAMILIES:
        for variant in range(4):
            root = output / "inputs" / f"case-{len(cases) + 1:02d}"
            task, contract, reference = prepare_case(root, family, variant)
            if shared_public_tools:
                task.graph_enabled = False
                task.question += (
                    f"共同评价时刻为{task.as_of.isoformat()}；"
                    "运行和映射观察新鲜度上限300秒；所有方法按K/R/P公共工具调用收费。"
                )
                contract = compile_contract(task)
                write_json(root / "task.json", task.model_dump(mode="json"))
                write_json(root / "contract.json", contract.model_dump(mode="json"))
            cases.append((root, task, contract, reference))
    protocol = {
        "schema": "e3-publication-protocol-1",
        "methods": list(METHODS),
        "native_p5_enabled": native_p5,
        "shared_public_tool_units": shared_public_tools,
        "cases": 32,
        "synthetic": True,
        "reviewed": False,
        "shared_budget": {"tools": 8, "models": 8, "rounds": 3, "seconds": 180},
        "clock": "fixed task.as_of; rounds release source publications, not elapsed wall time",
        "initial_collection": (
            "T0/T1/T3 compiled queries; T2 native P5 seed queries, costs included"
        ),
        "source_replacement": (
            "complete physical publication explicitly supersedes logical observation slots"
        ),
        "independence": (
            "new development cases; correlated fixture families, no population inference"
        ),
        "false_closure": "primary requirement satisfied in a predeclared unsolvable case",
        "correct_stop": (
            "unsolvable primary remains open at bounded non-error termination; "
            "efficiency reported separately"
        ),
        "new_valid_fields": (
            "distinct object/category/required-field/value entering satisfied requirements; "
            "includes initial collection and fields validated after bilateral completion"
        ),
        "redundancy": (
            "same tool/object/requirements/arguments and unchanged publication after an earlier "
            "successful query; negative/error calls excluded"
        ),
        "p5": (
            "unchanged native graph, tool cache and model planner; "
            "no common plan head for gap metrics"
        ),
        "heldout_consumed": False,
        "model_calls": "actual only",
        "real_network_writes": 0,
    }
    write_json(output / "protocol.json", protocol)
    write_json(output / "references.json", [c[-1] for c in cases])
    hashes = {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()}
    write_json(output / "pre-evaluation-input-hashes.json", hashes)
    results = []
    selected = METHODS if native_p5 else (METHODS[0], METHODS[1], METHODS[3])
    for case_root, task, contract, reference in cases:
        for method in selected:
            root = output / "runs" / reference["case_id"] / method
            shutil.copytree(case_root, root)
            if method == METHODS[2]:
                from upf_agent.v8.e3_p5 import run_native_p5

                result = run_native_p5(
                    project,
                    root,
                    task,
                    contract,
                    reference,
                    shared_public_tools=shared_public_tools,
                )
            elif shared_public_tools:
                from upf_agent.v8.e3_public import run_public_engine

                result = run_public_engine(root, task, contract, reference, method)
            else:
                result = run_deterministic(root, task, contract, reference, method)
            result["method"] = method
            write_json(root / "result.json", result)
            results.append(result)
            write_json(
                output / "progress.json",
                {
                    "completed": len(results),
                    "expected": 32 * len(selected),
                    "last_case": reference["case_id"],
                    "last_method": method,
                },
            )
    refs = {r["case_id"]: r for _, _, _, r in cases}
    aggregates = {}
    for method in selected:
        rows = [r for r in results if r["method"] == method]
        solvable = [r for r in rows if refs[r["case_id"]]["solvable"]]
        unsolvable = [r for r in rows if not refs[r["case_id"]]["solvable"]]
        aggregates[method] = {
            "runs": len(rows),
            "solvable": len(solvable),
            "unsolvable": len(unsolvable),
            "solvable_closed": sum(r["primary_closed"] for r in solvable),
            "false_closures": sum(r["false_closure"] for r in rows),
            "correct_stops": sum(r["correct_stop"] for r in unsolvable),
            "tool_calls": sum(r["tool_calls"] for r in rows),
            "model_calls": sum(r["model_calls"] for r in rows),
            "budget_violations": sum(not r["budget_ok"] for r in rows),
            "uncommitted_tool_receipts": sum(r["uncommitted_tool_receipts"] for r in rows),
            "all_closed": sum(r["all_closed"] for r in rows),
            "redundant_queries": sum(r["redundant_queries"] for r in rows),
            "new_valid_fields": sum(r["new_valid_fields"] for r in rows),
        }
    unchanged = all(sha(output / name) == value for name, value in hashes.items())
    summary = {
        "schema": "e3-development-results-1",
        "synthetic": True,
        "reviewed": False,
        "source": source,
        "source_unchanged": source_manifest(measured_source) == source,
        "inputs_unchanged": unchanged,
        "runs": len(results),
        "cases": 32,
        "per_method": aggregates,
        "native_p5_enabled": native_p5,
        "full_local_comparisons": sum(
            sum("full_local_equal" in h for h in r["history"]) for r in results
        ),
        "heldout_consumed": False,
        "formal_e3_complete": False,
        "pass": unchanged
        and source_manifest(measured_source) == source
        and all(
            r["budget_ok"]
            and not r["false_closure"]
            and r["uncommitted_tool_receipts"] == 0
            and not r.get("native_error")
            for r in results
        ),
    }
    write_json(output / "summary.json", summary)
    return summary
