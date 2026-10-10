"""Independent graph controls cover bounded access, adversarial metadata and real K admission."""

import pytest

from upf_agent.v8.builders import task_graph
from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.engine import OrchestrationEngine
from upf_agent.v8.graph import MemoryGraphStore
from upf_agent.v8.graph_query_compiler import compile_requirement_query
from upf_agent.v8.graph_ranking import personalized_pagerank
from upf_agent.v8.phase1 import prepared
from upf_agent.v8.requirement_graph import execute_requirement_query, knowledge_writeback
from upf_agent.v8.wp08 import CASES, STRATEGIES, make_case


@pytest.mark.parametrize("name", CASES)
@pytest.mark.parametrize("strategy", STRATEGIES)
def test_twenty_four_frozen_engineering_controls(tmp_path, name, strategy):
    task, contract, req, store, seeds, pool, options, expected = make_case(tmp_path / "case", name)
    query = compile_requirement_query(task, contract, req, seeds, reseed_ids=pool, **options)
    result = execute_requirement_query(tmp_path / "case", store, query, strategy=strategy)
    bindings, rejected = knowledge_writeback(tmp_path / "case", query, result, "test", store=store)
    assert bool(bindings) == (expected or name == "missing_seed" and strategy == "bfs-reseed")
    assert not rejected
    assert result["scan"]["nodes_scanned"] <= options["max_nodes"]
    assert result["scan"]["adjacency_entries_scanned"] <= options["max_edges"]
    assert all(len(h["path"]["edges"]) <= 2 for h in result["hits"])


def test_two_node_pagerank_has_independently_computed_solution():
    result = personalized_pagerank(["A", "B"], [("A", "B")], ["A"], tolerance=1e-11)
    assert result["converged"]
    assert result["scores"]["A"] == pytest.approx(1 / 1.85, abs=1e-10)
    assert result["scores"]["B"] == pytest.approx(0.85 / 1.85, abs=1e-10)
    assert sum(result["scores"].values()) == pytest.approx(1)


def test_dangling_seed_and_failed_convergence_are_explicit():
    result = personalized_pagerank(["A", "B"], [], ["A"])
    assert result["scores"] == {"A": 1.0, "B": 0.0}
    failed = personalized_pagerank(["A", "B"], [("A", "B")], ["A"], max_iterations=1)
    assert failed["status"] == "not_converged"
    assert failed["scores"] == {}


def test_failed_ppr_never_publishes_partial_scores(tmp_path):
    task, contract, req, store, seeds, pool, _, _ = make_case(tmp_path / "case")
    query = compile_requirement_query(task, contract, req, seeds, max_iterations=1)
    result = execute_requirement_query(tmp_path / "case", store, query, strategy="ppr")
    assert result["status"] == "not_converged"
    assert not result["hits"]


@pytest.mark.parametrize("change", ["fields", "objects", "as_of"])
def test_mutated_compiled_scope_is_rejected(tmp_path, change):
    task, contract, req, store, seeds, _, _, _ = make_case(tmp_path / "case")
    query = compile_requirement_query(task, contract, req, seeds)
    if change == "objects":
        query.graph.objects.append("outside")
    if change == "fields":
        query.requirement.fields.append("secret")
    if change == "as_of":
        from datetime import timedelta

        query.graph.as_of += timedelta(hours=1)
    with pytest.raises(ValueError):
        execute_requirement_query(tmp_path / "case", store, query)


@pytest.mark.parametrize("change", ["path", "field", "current_source", "graph_payload", "registry"])
def test_writeback_rechecks_current_trusted_inputs(tmp_path, change):
    from upf_agent.v8.knowledge_applicability import KnowledgeRegistry

    root = tmp_path / "case"
    task, contract, req, store, seeds, _, _, _ = make_case(root)
    query = compile_requirement_query(task, contract, req, seeds)
    result = execute_requirement_query(root, store, query)
    assert result["hits"]
    if change == "path":
        result["hits"][0]["path"]["nodes"] = ["forged"]
    if change == "field":
        result["hits"][0]["binding"]["fields"]["instruction"] = "forged"
    if change == "current_source":
        (root / store.nodes["doc"].source.relative_path).write_text("tampered")
    if change == "graph_payload":
        result["candidate_graph"]["edges"][0]["corroborated"] = False
    if change == "registry":
        KnowledgeRegistry(version="changed").model_dump_json()
        (root / "data/v8/knowledge_applicability.json").write_text(
            KnowledgeRegistry(version="changed").model_dump_json()
        )
    if change in {"registry", "graph_payload"}:
        with pytest.raises(ValueError):
            knowledge_writeback(root, query, result, "test", store=store)
    else:
        accepted, rejected = knowledge_writeback(root, query, result, "test", store=store)
        assert not accepted and rejected


def test_bfs_and_ppr_use_exactly_same_filtered_candidate_graph(tmp_path):
    root = tmp_path / "case"
    task, contract, req, store, seeds, _, _, _ = make_case(root, "two_hops")
    query = compile_requirement_query(task, contract, req, seeds)
    bfs = execute_requirement_query(root, store, query, strategy="bfs")
    ppr = execute_requirement_query(root, store, query, strategy="ppr")
    assert bfs["candidate_graph_sha256"] == ppr["candidate_graph_sha256"]
    assert bfs["scan"] == ppr["scan"]
    assert [h["node_id"] for h in bfs["hits"]] == [h["node_id"] for h in ppr["hits"]]


def test_high_fanout_does_not_scan_or_sort_an_unbounded_neighbor_list(tmp_path):
    from upf_agent.v8.graph import GraphEdge

    root = tmp_path / "case"
    task, contract, req, store, seeds, _, _, _ = make_case(root)
    origin = store.edges["edge-0"]
    store.build(
        [],
        [
            GraphEdge(
                edge_id=f"extra-{i}",
                source_id="seed",
                target_id="doc",
                relation="CONTAINS",
                source=origin.source,
                synthetic=True,
            )
            for i in range(300)
        ],
    )

    class Counted(list):
        yielded = 0

        def __iter__(self):
            for edge in super().__iter__():
                self.yielded += 1
                yield edge

    adjacency = Counted(store.adjacency["seed"])
    store.adjacency["seed"] = adjacency
    query = compile_requirement_query(task, contract, req, seeds, max_edges=7)
    result = execute_requirement_query(root, store, query)
    assert adjacency.yielded == 7
    assert result["scan"]["adjacency_entries_scanned"] == 7
    assert result["truncated"]


def test_pair_retrieval_remains_hints_until_pair_writeback_is_implemented(tmp_path):
    task, contract, bindings = prepared(tmp_path / "case")
    req = next(r for r in contract.requirements if r.kind == "P")
    nodes, edges = task_graph(task, bindings)
    store = MemoryGraphStore()
    store.build(nodes, edges)
    seeds = [f"binding:{b.evidence_id}:{b.revision}" for b in bindings if b.category == "P"]
    query = compile_requirement_query(task, contract, req, seeds)
    result = execute_requirement_query(tmp_path / "case", store, query)
    assert {h["binding"]["object_id"] for h in result["hits"]} == set(req.objects)
    with pytest.raises(ValueError, match="hints only"):
        knowledge_writeback(tmp_path / "case", query, result, "test", store=store)


def test_runtime_retrieval_projects_fields_and_cannot_write_back(tmp_path):
    from upf_agent.v8.adapters import collect
    from upf_agent.v8.compiler import compile_query_plan
    from upf_agent.v8.models import EvidenceBinding

    task, _, bindings = prepared(tmp_path / "case")
    task.permission.readable_fields = ["interface", "state", "n4_enabled"]
    contract = compile_contract(task)
    req = next(r for r in contract.requirements if r.kind == "R")
    step = next(
        s
        for s in compile_query_plan(task, contract).steps
        if req.requirement_id in s.requirement_ids
    )
    bindings = [
        EvidenceBinding.model_validate(b)
        for b in collect(tmp_path / "case", task, contract, step, "current-permission")["bindings"]
    ]
    b = next(b for b in bindings if b.requirement_id == req.requirement_id)
    nodes, edges = task_graph(task, bindings)
    store = MemoryGraphStore()
    store.build(nodes, edges)
    query = compile_requirement_query(
        task, contract, req, [f"binding:{b.evidence_id}:{b.revision}"]
    )
    result = execute_requirement_query(tmp_path / "case", store, query)
    assert result["hits"]
    for node in result["candidate_graph"]["nodes"]:
        if node["kind"] == "EvidenceBinding":
            assert set(node["attributes"]["binding"]["fields"]) <= set(
                task.permission.readable_fields
            )
    with pytest.raises(ValueError, match="hints only"):
        knowledge_writeback(tmp_path / "case", query, result, "test", store=store)


def test_engine_opt_in_has_real_ledger_admission_and_charged_total_budget(tmp_path, monkeypatch):
    root = tmp_path / "case"
    task, _, _, store, _, _, _, _ = make_case(root)
    monkeypatch.setattr("upf_agent.v8.engine.load_manual_graph", lambda _root: store)
    engine = OrchestrationEngine(
        root, requirement_graph_strategy="bfs-reseed", graph_reseed_ids=["doc"]
    )
    try:
        result = engine.run(task)
        assert result["status"] == "completed"
        assert all(s["code"] == "satisfied" for s in result["states"].values())
        graph_ids = [b["evidence_id"] for b in result["bindings"] if ":graph:" in b["evidence_id"]]
        assert graph_ids
        assert all(not a["execute_authorized"] for a in result["actions"])
        import json

        traces = json.loads(
            (root / "runs/v8" / task.run_id / "requirement-graph-0.json").read_text()
        )
        assert traces["discovery_and_audit_nodes_scanned"] <= 100
        assert traces["discovery_and_audit_adjacency_entries_scanned"] <= 200
        assert engine.ledger.inspect(task.run_id)["receipts"]
    finally:
        engine.close()
    default = OrchestrationEngine(root)
    try:
        with pytest.raises(ValueError, match="configuration changed"):
            default.resume(task.run_id)
    finally:
        default.close()


def test_graph_change_blocks_resume_and_snapshot_does_not_mutate_manual_store(
    tmp_path, monkeypatch
):
    root = tmp_path / "case"
    task, _, _, store, _, _, _, _ = make_case(root)
    snapshot = store.snapshot()
    monkeypatch.setattr("upf_agent.v8.engine.load_manual_graph", lambda _root: store)
    engine = OrchestrationEngine(
        root, requirement_graph_strategy="bfs-reseed", graph_reseed_ids=["doc"]
    )
    try:
        engine.run(task)
        assert store.snapshot() == snapshot
    finally:
        engine.close()
    store.nodes["doc"].object_ids = ["outside"]
    engine = OrchestrationEngine(
        root, requirement_graph_strategy="bfs-reseed", graph_reseed_ids=["doc"]
    )
    try:
        with pytest.raises(ValueError, match="configuration changed"):
            engine.resume(task.run_id)
    finally:
        engine.close()
