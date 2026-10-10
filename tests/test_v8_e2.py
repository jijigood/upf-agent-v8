import pytest

from upf_agent.v8.e2 import fixed_hop
from upf_agent.v8.graph_query_compiler import compile_requirement_query
from upf_agent.v8.knowledge_applicability import KnowledgeRegistry
from upf_agent.v8.wp08 import make_case


@pytest.mark.parametrize(
    "name,allowed",
    [
        ("legal", True),
        ("two_hops", True),
        ("wrong_version", False),
        ("unknown_version", False),
        ("wrong_purpose", False),
        ("missing_mapping", False),
        ("unreviewed_mapping", False),
        ("source_tamper", False),
        ("wrong_object", False),
        ("unverified_edge", False),
        ("edge_source_tamper", False),
        ("node_budget", False),
        ("field_denied", False),
    ],
)
def test_fixed_hop_terminal_filter_enforces_paths_sources_and_budget(tmp_path, name, allowed):
    root = tmp_path / "case"
    task, contract, req, store, seeds, pool, options, _ = make_case(root, name)
    query = compile_requirement_query(task, contract, req, seeds, reseed_ids=pool, **options)
    result = fixed_hop(root, store, query, KnowledgeRegistry.load(root))
    assert bool(result["hits"]) == allowed
    assert result["scan"]["nodes_scanned"] <= query.graph.max_nodes
    assert result["scan"]["adjacency_entries_scanned"] <= query.graph.max_edges
