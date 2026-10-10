"""Requirement retrieval on a bounded, sourced candidate graph; only K may be written back."""

from collections import deque
from itertools import islice
from pathlib import Path
from time import perf_counter

from upf_agent.contracts import TimeWindow
from upf_agent.v8.adapters import source_path
from upf_agent.v8.evaluator import _eligibility
from upf_agent.v8.graph import MemoryGraphStore, Neo4jGraphStore, exclusion
from upf_agent.v8.graph_query_compiler import compile_requirement_query
from upf_agent.v8.graph_ranking import personalized_pagerank
from upf_agent.v8.knowledge_applicability import KnowledgeRegistry, annotate_knowledge
from upf_agent.v8.models import EvidenceBinding, digest


class SourceChecks:
    def __init__(self, root):
        self.root, self.hashes = root, {}
        self.reads, self.bytes = 0, 0

    def valid(self, pointer):
        import hashlib

        relative = pointer.relative_path
        if not relative:
            return False
        if relative not in self.hashes:
            try:
                body = source_path(self.root, relative).read_bytes()
                self.reads += 1
                self.bytes += len(body)
                self.hashes[relative] = hashlib.sha256(body).hexdigest()
            except (OSError, ValueError):
                self.hashes[relative] = None
        return self.hashes[relative] == pointer.sha256


def _binding(node, query, registry):
    req, task, contract = query.requirement, query.task, query.contract
    if req.kind == "K":
        if node.kind not in {"DocumentBlock", "Command"}:
            return None, None
        text = node.attributes.get("text")
        if not isinstance(text, str) or not text.strip():
            return None, "unknown_knowledge_text"
        from upf_agent.v8.models import object_product_version

        product, _ = object_product_version(task, req.objects[0])
        if node.attributes.get("product") != product:
            return None, "wrong_product"
        if set(req.fields) - {"instruction"}:
            return None, "unsupported_knowledge_fields"
        if len(req.objects) != 1:
            return None, "knowledge_requires_single_object"
        mapping = registry.resolve(node.source, text, product, node.version, req.objects[0])
        if req.purpose not in mapping["purposes"]:
            return None, "unknown_or_wrong_knowledge_purpose"
        if bool(node.valid_from) != bool(node.valid_to):
            return None, "partial_validity_window"
        binding = EvidenceBinding(
            evidence_id=f"{task.run_id}:graph:{node.node_id}:{req.objects[0]}",
            native_id=node.node_id,
            task_id=task.run_id,
            contract_id=contract.contract_id,
            requirement_id=req.requirement_id,
            object_id=req.objects[0],
            category="K",
            fields={"instruction": text},
            source=node.source,
            product=product,
            version=node.version,
            synthetic=node.synthetic,
            source_verified=True,
            purposes=mapping["purposes"],
            knowledge_applicability=mapping,
            observed=node.attributes.get("observed"),
            receipt_id="candidate-only",
            valid=TimeWindow(
                start=node.valid_from, end=node.valid_to, timezone_source="sourced graph validity"
            )
            if node.valid_from and node.valid_to
            else None,
        )
        return binding, None
    if node.kind != "EvidenceBinding":
        return None, None
    try:
        binding = EvidenceBinding.model_validate(node.attributes.get("binding"))
    except ValueError:
        return None, "invalid_native_binding"
    if binding.category != req.kind or binding.requirement_id != req.requirement_id:
        return None, None  # Other declared evidence can be a transit node, never an answer.
    if set(req.fields) - set(binding.fields):
        return None, "missing_required_fields"
    if binding.source != node.source:
        return None, "node_binding_source_mismatch"
    denied = _eligibility(binding, req, task, contract, task.as_of, True)
    if denied:
        return None, denied[1]
    binding = binding.model_copy(deep=True)
    binding.fields = {f: binding.fields[f] for f in req.fields}
    return binding, None


def candidate_graph(root, store, query, *, allow_reseed=False, registry=None):
    if not isinstance(store, MemoryGraphStore) or isinstance(store, Neo4jGraphStore):
        raise ValueError("requirement retrieval needs a frozen Memory snapshot; Neo4j not adapted")
    registry = registry if registry is not None else KnowledgeRegistry.load(root)
    checks = SourceChecks(root)
    nodes, edges, candidates, paths, rejected, cache = {}, {}, {}, {}, [], {}
    roots, counts = [], {"nodes_scanned": 0, "adjacency_entries_scanned": 0}
    truncated = False
    req = query.requirement

    def admit(identifier):
        nonlocal truncated
        if identifier in cache:
            return cache[identifier]
        if counts["nodes_scanned"] >= query.graph.max_nodes:
            truncated = True
            return None
        counts["nodes_scanned"] += 1
        node = store.nodes.get(identifier)
        reason = "unknown_node" if node is None else exclusion(node, query.graph)
        binding = None
        if node is not None and reason is None:
            if node.kind == "EvidenceBinding":
                try:
                    native = EvidenceBinding.model_validate(node.attributes.get("binding"))
                    if (
                        native.deleted
                        or not native.readable
                        or not native.source_verified
                        or not native.corroborated
                        or native.source != node.source
                        or native.object_id not in query.graph.objects
                    ):
                        reason = "unusable_native_binding"
                    elif (
                        native.task_id != query.task.run_id
                        or native.contract_id != query.contract.contract_id
                    ):
                        reason = "cross_task_or_contract"
                except ValueError:
                    reason = "invalid_native_binding"
        if node is not None and reason is None:
            if (
                node.attributes.get("text")
                and "instruction" not in query.task.permission.readable_fields
            ):
                reason = "node_field_permission_denied"
            elif not checks.valid(node.source):
                reason = "source_hash_unverified"
            else:
                try:
                    binding, reason = _binding(node, query, registry)
                except ValueError:
                    reason = "invalid_candidate_metadata"
        if reason:
            rejected.append({"id": identifier, "reason": reason})
            cache[identifier] = None
            return None
        # Do not emit unreadable fields from a native binding even when it is only transit.
        node = node.model_copy(deep=True)
        if node.kind == "EvidenceBinding":
            raw = node.attributes.get("binding", {})
            if (
                raw.get("task_id") != query.task.run_id
                or raw.get("contract_id") != query.contract.contract_id
            ):
                rejected.append({"id": identifier, "reason": "cross_task_or_contract"})
                cache[identifier] = None
                return None
            raw["fields"] = {
                k: v
                for k, v in raw.get("fields", {}).items()
                if k in query.task.permission.readable_fields
            }
        cache[identifier] = node
        nodes[identifier] = node
        if binding:
            candidates[identifier] = binding
        return node

    def expand(seed_ids, origin):
        nonlocal truncated
        queue = deque()
        for identifier in seed_ids:
            if admit(identifier) is not None:
                if identifier not in roots:
                    roots.append(identifier)
                if identifier not in paths:
                    paths[identifier] = {
                        "nodes": [identifier],
                        "edges": [],
                        "seed_origin": origin,
                        "hops": 0,
                    }
                    queue.append(identifier)
        while queue:
            identifier = queue.popleft()
            if paths[identifier]["hops"] >= query.graph.max_hops:
                continue
            # Snapshot adjacency order is fixed by its materialization. No unrestricted
            # neighbors query or full list sorting precedes the charged bounded scan.
            adjacency = store.adjacency.get(identifier, ())
            remaining = query.graph.max_edges - counts["adjacency_entries_scanned"]
            if len(adjacency) > remaining:
                truncated = True
            for edge in islice(adjacency, remaining):
                counts["adjacency_entries_scanned"] += 1
                reason = None
                if edge.relation not in query.graph.relations:
                    reason = "relation_not_allowed"
                elif not edge.corroborated or edge.synthetic and not query.graph.allow_synthetic:
                    reason = "unverified_relation"
                elif not checks.valid(edge.source):
                    reason = "edge_source_hash_unverified"
                if reason:
                    rejected.append({"id": edge.edge_id, "reason": reason})
                    continue
                other = edge.target_id if edge.source_id == identifier else edge.source_id
                if admit(other) is None:
                    continue
                edges[edge.edge_id] = edge
                if other not in paths:
                    paths[other] = {
                        "nodes": [*paths[identifier]["nodes"], other],
                        "edges": [*paths[identifier]["edges"], edge.edge_id],
                        "seed_origin": origin,
                        "hops": paths[identifier]["hops"] + 1,
                    }
                    queue.append(other)
            if counts["adjacency_entries_scanned"] >= query.graph.max_edges:
                return

    if not query.denied_reasons:
        expand(query.graph.seed_ids, "primary")
        if allow_reseed and not candidates:
            expand(query.reseed_ids, "cached-reseed")
    return {
        "nodes": nodes,
        "edges": edges,
        "bindings": candidates,
        "paths": paths,
        "roots": roots,
        "excluded": rejected,
        "truncated": truncated,
        "scan": {
            **counts,
            "physical_source_hash_reads": checks.reads,
            "physical_source_hash_bytes": checks.bytes,
        },
        "requirement_kind": req.kind,
    }


def execute_requirement_query(
    root: Path, store, query, *, strategy="bfs", registry=None, snapshot_sha256=None
):
    if strategy not in {"bfs", "ppr", "bfs-reseed"}:
        raise ValueError("unknown requirement retrieval strategy")
    expected = compile_requirement_query(
        query.task,
        query.contract,
        query.requirement,
        query.graph.seed_ids,
        reseed_ids=query.reseed_ids,
        top_k=query.top_k,
        max_nodes=query.graph.max_nodes,
        max_edges=query.graph.max_edges,
        max_hops=query.graph.max_hops,
        alpha=query.alpha,
        tolerance=query.tolerance,
        max_iterations=query.max_iterations,
        relations=query.graph.relations,
    )
    if expected != query:
        raise ValueError("compiled graph query changed; recompile trusted inputs")
    started = perf_counter()
    registry = registry if registry is not None else KnowledgeRegistry.load(root)
    graph = candidate_graph(
        root, store, query, allow_reseed=strategy == "bfs-reseed", registry=registry
    )
    ranked_at = perf_counter()
    ranking = {"status": "not_requested", "iterations": 0, "ranking_edge_visits": 0}
    if strategy == "ppr":
        ranking = personalized_pagerank(
            graph["nodes"],
            [(e.source_id, e.target_id) for e in graph["edges"].values()],
            graph["roots"],
            alpha=query.alpha,
            tolerance=query.tolerance,
            max_iterations=query.max_iterations,
        )
        selected = (
            sorted(graph["bindings"], key=lambda n: (-ranking["scores"].get(n, 0), n))
            if ranking["converged"]
            else []
        )
    else:
        selected = sorted(graph["bindings"], key=lambda n: (graph["paths"][n]["hops"], n))
    selected = selected[: query.top_k]
    serialized_graph = {
        "nodes": [n.model_dump(mode="json") for _, n in sorted(graph["nodes"].items())],
        "edges": [e.model_dump(mode="json") for _, e in sorted(graph["edges"].items())],
    }
    return {
        "schema": "v8-requirement-retrieval-1",
        "strategy": strategy,
        "query": query.model_dump(mode="json"),
        "query_sha256": digest(query),
        "registry_sha256": digest(registry),
        "snapshot_sha256": snapshot_sha256,
        "candidate_graph_sha256": digest(serialized_graph),
        "candidate_graph": serialized_graph,
        "accepted_roots": graph["roots"],
        "excluded": graph["excluded"],
        "truncated": graph["truncated"],
        "scan": graph["scan"],
        "ranking": ranking,
        "hits": [
            {
                "node_id": n,
                "path": graph["paths"][n],
                "binding": graph["bindings"][n].model_dump(mode="json"),
            }
            for n in selected
        ],
        "status": "denied"
        if query.denied_reasons
        else "not_converged"
        if ranking["status"] == "not_converged"
        else "evidence_found"
        if selected
        else "no_usable_evidence",
        "cost": {
            "candidate_seconds": ranked_at - started,
            "ranking_and_serialization_seconds": perf_counter() - ranked_at,
        },
    }


def knowledge_writeback(root, query, result, receipt_id, *, store, registry=None):
    """Recheck current bytes, mapping, policy, time and recorded paths before ledger admission."""
    if query.requirement.kind != "K":
        raise ValueError("graph R/P retrieval is hints only; writeback not implemented")
    if result["query_sha256"] != digest(query):
        raise ValueError("retrieval belongs to a different compiled query")
    registry = registry if registry is not None else KnowledgeRegistry.load(root)
    if result["registry_sha256"] != digest(registry):
        raise ValueError("knowledge registry changed; retrieve with a new context")
    if digest(result["candidate_graph"]) != result["candidate_graph_sha256"]:
        raise ValueError("retrieved candidate graph changed")
    if not result["hits"]:
        result["writeback_audit_scan"] = {"nodes_scanned": 0, "adjacency_entries_scanned": 0}
        return [], []
    started = perf_counter()
    # Recompute against the trusted store, never a caller-provided reconstruction of a path.
    fresh = execute_requirement_query(
        root,
        store,
        query,
        strategy=result["strategy"],
        registry=registry,
        snapshot_sha256=result["snapshot_sha256"],
    )
    fresh_hits = {h["node_id"]: h for h in fresh["hits"]}
    result["writeback_audit_scan"] = fresh["scan"]
    accepted, rejected, binding_checks = [], [], 0
    for hit in result["hits"]:
        node_id = hit["node_id"]
        if (
            node_id not in fresh_hits
            or fresh_hits[node_id] != hit
            or fresh["candidate_graph_sha256"] != result["candidate_graph_sha256"]
        ):
            rejected.append({"id": node_id, "reason": "path_or_evidence_recheck_failed"})
            continue
        binding = EvidenceBinding.model_validate(fresh_hits[node_id]["binding"])
        binding.receipt_id = receipt_id
        binding_checks += 1
        annotate_knowledge(root, binding, registry)
        failure = _eligibility(
            binding,
            query.requirement,
            query.task,
            query.contract,
            query.task.as_of,
            not query.denied_reasons,
        )
        if failure:
            rejected.append({"id": node_id, "reason": failure[1]})
        else:
            accepted.append(binding)
    result["cost"]["writeback_audit_seconds"] = perf_counter() - started
    result["writeback_binding_source_checks"] = binding_checks
    return accepted, rejected
