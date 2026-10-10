"""Explicit synthetic development controls for requirement retrieval, not expert query Gold."""

import hashlib
from datetime import timedelta
from pathlib import Path
from time import perf_counter

from upf_agent.v8.e4 import write_json
from upf_agent.v8.evaluator import full_evaluate
from upf_agent.v8.experiment_manifest import source_manifest
from upf_agent.v8.graph import GraphEdge, GraphNode, MemoryGraphStore
from upf_agent.v8.graph_query_compiler import compile_requirement_query
from upf_agent.v8.knowledge_applicability import KnowledgeAnnotation, KnowledgeRegistry
from upf_agent.v8.models import SourcePointer, digest
from upf_agent.v8.phase1 import prepared
from upf_agent.v8.requirement_graph import execute_requirement_query, knowledge_writeback

CASES = [
    "legal",
    "wrong_version",
    "unknown_version",
    "wrong_purpose",
    "missing_mapping",
    "revoked_mapping",
    "unreviewed_mapping",
    "source_tamper",
    "wrong_object",
    "wrong_domain",
    "object_denied",
    "field_denied",
    "expired",
    "future",
    "partial_validity",
    "unsupported_relation",
    "unverified_edge",
    "edge_source_tamper",
    "missing_seed",
    "no_seed_pool",
    "two_hops",
    "three_hops",
    "node_budget",
    "edge_budget",
]
STRATEGIES = ["bfs", "ppr", "bfs-reseed"]


def make_case(root: Path, name="legal"):
    if name not in CASES:
        raise ValueError("unknown synthetic control")
    task, _, bindings = prepared(root)
    from upf_agent.v8.compiler import compile_contract

    binding = next(b for b in bindings if b.category == "K")
    annotation = KnowledgeAnnotation(
        annotation_id="wp08-synthetic-rule",
        source_sha256=binding.source.sha256,
        locator=binding.source.locator,
        content_sha256=hashlib.sha256(binding.fields["instruction"].encode()).hexdigest(),
        product=task.product,
        version=task.version,
        object_ids=[binding.object_id],
        purposes=[task.template],
        basis_kind="trusted_rule",
        basis_source="wp08-synthetic-control",
        basis_version="1",
        rule_id="wp08-fixture-1",
        reviewed=False,
    )
    doc = GraphNode(
        node_id="doc",
        kind="DocumentBlock",
        layer="knowledge",
        source=binding.source,
        object_ids=[binding.object_id],
        version=task.version,
        synthetic=True,
        attributes={
            "text": binding.fields["instruction"],
            "product": task.product,
            "domain": "domain-0",
            "observed": binding.observed.model_dump(mode="json") if binding.observed else None,
        },
    )
    topology = ["seed", "doc"]
    if name in {"two_hops", "node_budget"}:
        topology = ["seed", "bridge", "doc"]
    if name == "three_hops":
        topology = ["seed", "bridge-1", "bridge-2", "doc"]
    if name == "wrong_version":
        doc.version = "4.0"
    if name == "unknown_version":
        doc.version = None
    if name == "wrong_purpose":
        annotation.purposes = ["manual_operation"]
    if name == "revoked_mapping":
        annotation.revoked = True
    if name == "unreviewed_mapping":
        annotation.basis_kind = "expert_review"
    if name == "wrong_object":
        doc.object_ids = ["outside"]
    if name == "wrong_domain":
        doc.attributes["domain"] = "domain-1"
    if name == "object_denied":
        task.permission.objects = []
    if name == "field_denied":
        task.permission.readable_fields.remove("instruction")
    if name in {"expired", "future"}:
        offset = -2 if name == "expired" else 1
        doc.valid_from = task.as_of + timedelta(hours=offset)
        doc.valid_to = doc.valid_from + timedelta(minutes=30)
    if name == "partial_validity":
        doc.valid_to = task.as_of + timedelta(hours=1)
    if name == "source_tamper":
        (root / binding.source.relative_path).write_text("synthetic source changed\n")
    relations = [
        {"source": a, "target": b, "relation": "CONTAINS"}
        for a, b in zip(topology, topology[1:], strict=False)
    ]
    if name == "unsupported_relation":
        relations[0]["relation"] = "CARRIES"
    if name == "edge_budget":
        relations.insert(0, {"source": "seed", "target": "noise", "relation": "CARRIES"})
    claims = root / "data/fixtures/wp08/graph-claims.json"
    write_json(claims, {"synthetic": True, "reviewed": False, "logical_relations": relations})
    pointer = SourcePointer(
        source_id="wp08-logical-claims",
        sha256=hashlib.sha256(claims.read_bytes()).hexdigest(),
        relative_path=str(claims.relative_to(root)),
        locator="/logical_relations",
    )
    nodes = [doc] + [
        GraphNode(
            node_id=n,
            kind="Section",
            layer="knowledge",
            source=pointer,
            object_ids=[binding.object_id],
            version=task.version,
            synthetic=True,
        )
        for n in topology
        if n != "doc"
    ]
    if name == "edge_budget":
        nodes.append(nodes[1].model_copy(update={"node_id": "noise"}))
    edges = [
        GraphEdge(
            edge_id=f"edge-{i}",
            source_id=r["source"],
            target_id=r["target"],
            relation=r["relation"],
            source=pointer,
            synthetic=True,
            corroborated=name != "unverified_edge",
        )
        for i, r in enumerate(relations)
    ]
    if name == "edge_source_tamper":
        edges[0].source = pointer.model_copy(update={"sha256": "0" * 64})
    registry = KnowledgeRegistry(
        version="wp08-synthetic-1", annotations=[annotation] if name != "missing_mapping" else []
    )
    write_json(root / "data/v8/knowledge_applicability.json", registry.model_dump(mode="json"))
    store = MemoryGraphStore()
    store.build(nodes, edges)
    contract = compile_contract(task)
    requirement = next(
        r for r in contract.requirements if r.requirement_id == binding.requirement_id
    )
    missing = name in {"missing_seed", "no_seed_pool"}
    seeds = ["missing"] if missing else ["seed"]
    pool = ["doc"] if name == "missing_seed" else []
    options = {
        "max_nodes": 2 if name == "node_budget" else 50,
        "max_edges": 1 if name == "edge_budget" else 100,
    }
    expected = name in {"legal", "two_hops"}
    return task, contract, requirement, store, seeds, pool, options, expected


def run_wp08(project: Path, output: Path):
    project, output = project.resolve(), output.resolve()
    if project != Path(__file__).resolve().parents[3]:
        raise ValueError("declared project differs from imported source root")
    if output.exists():
        raise ValueError("use a new experiment ID")
    output.mkdir(parents=True)
    source = source_manifest(project)
    protocol = {
        "schema": "v8-wp08-development-1",
        "synthetic": True,
        "reviewed": False,
        "expert_gold": False,
        "formal_e2": False,
        "heldout_consumed": False,
        "model_calls": 0,
        "real_network_writes": 0,
        "cases": CASES,
        "strategies": STRATEGIES,
        "expected_method_runs": 72,
        "ppr": {"alpha": 0.85, "tolerance": 1e-8, "max_iterations": 1000, "backend": "pure-python"},
        "seed_cache": "synthetic frozen primary/reseed IDs, not an executed P3 search",
        "discovery_budget": "50 node lookups / 100 adjacency inspections, 2 hops; lower controls",
        "total_with_writeback_audit": "at most 100 node lookups / 200 adjacency inspections",
        "writeback": "K only; R/P retrieval hints do not enter ledger",
        "not_executed": ["G0 Hybrid P3", "G1 fixed-hop", "formal query Gold", "Neo4j WP08"],
        "scope": "engineering controls, no retrieval-quality or real fault claim",
    }
    write_json(output / "protocol.json", protocol)
    write_json(output / "source_manifest.json", source)
    # All control inputs and expected outcomes exist before the first method executes.
    fixtures, references = {}, {}
    for name in CASES:
        root = output / "cases" / name
        fixture = make_case(root, name)
        task, contract, req, store, seeds, pool, options, expected = fixture
        snapshot = store.snapshot()
        reference = {
            s: expected or name == "missing_seed" and s == "bfs-reseed" for s in STRATEGIES
        }
        references[name] = reference
        write_json(
            root / "input.json",
            {
                "task": task.model_dump(mode="json"),
                "contract": contract.model_dump(mode="json"),
                "snapshot": snapshot,
                "seed_cache": seeds,
                "reseed_cache": pool,
                "budgets": options,
            },
        )
        fixtures[name] = (fixture, digest(snapshot))
    write_json(
        output / "control-references.json",
        {"synthetic": True, "reviewed": False, "outcomes": references},
    )
    rows = []
    for name in CASES:
        fixture, snapshot = fixtures[name]
        task, contract, req, store, seeds, pool, options, _ = fixture
        root = output / "cases" / name
        comparison = {}
        for strategy in STRATEGIES:
            started = perf_counter()
            query = compile_requirement_query(
                task, contract, req, seeds, reseed_ids=pool, **options
            )
            result = execute_requirement_query(
                root, store, query, strategy=strategy, snapshot_sha256=snapshot
            )
            discovery = dict(result["scan"])
            bindings, rejected = knowledge_writeback(root, query, result, strategy, store=store)
            elapsed = perf_counter() - started
            audit = result["writeback_audit_scan"]
            nodes = discovery["nodes_scanned"] + audit["nodes_scanned"]
            edges = discovery["adjacency_entries_scanned"] + audit["adjacency_entries_scanned"]
            state = full_evaluate(task, contract, bindings, strategy)[req.requirement_id]
            actual = bool(bindings) and state.valid
            row = {
                "case": name,
                "method": strategy,
                "expected_usable_k": references[name][strategy],
                "usable_k": actual,
                "elapsed_seconds": elapsed,
                "candidate_graph_sha256": result["candidate_graph_sha256"],
                "nodes_scanned_with_audit": nodes,
                "adjacency_scanned_with_audit": edges,
                "status": result["status"],
                "ranking": result["ranking"],
                "excluded": result["excluded"],
                "writeback_rejected": rejected,
                "paths": [h["path"] for h in result["hits"]],
            }
            row["pass"] = actual == references[name][strategy] and nodes <= 2 * options["max_nodes"]
            row["pass"] &= edges <= 2 * options["max_edges"]
            write_json(root / f"{strategy}-retrieval.json", result)
            write_json(
                root / f"{strategy}-writeback.json", [b.model_dump(mode="json") for b in bindings]
            )
            comparison[strategy] = row
            rows.append(row)
        assert (
            comparison["bfs"]["candidate_graph_sha256"]
            == comparison["ppr"]["candidate_graph_sha256"]
        )
    result = {
        **protocol,
        "source": source,
        "method_runs": len(rows),
        "rows": rows,
        "source_unchanged": source_manifest(project) == source,
    }
    result["pass"] = result["source_unchanged"] and len(rows) == 72 and all(r["pass"] for r in rows)
    write_json(output / "summary.json", result)
    return result
