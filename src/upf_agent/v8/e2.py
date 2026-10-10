"""Real P3 seed cache and five retrieval controls, with unreviewed development labels."""

import hashlib
import json
import shutil
from collections import Counter, deque
from contextlib import ExitStack
from pathlib import Path
from time import perf_counter

from upf_agent.config import load_model_config
from upf_agent.p3_index import load_active_index, load_chunks
from upf_agent.p3_search import search
from upf_agent.retrieval import RetrievalWorker
from upf_agent.v8.adapters import collect
from upf_agent.v8.compiler import compile_contract, compile_query_plan
from upf_agent.v8.experiment_manifest import source_manifest
from upf_agent.v8.fixtures import example
from upf_agent.v8.graph import GraphEdge, GraphNode, MemoryGraphStore, exclusion
from upf_agent.v8.graph_query_compiler import compile_requirement_query
from upf_agent.v8.knowledge_applicability import KnowledgeAnnotation, KnowledgeRegistry
from upf_agent.v8.models import EvidenceBinding, SourcePointer, digest
from upf_agent.v8.phase1 import write_json
from upf_agent.v8.requirement_graph import (
    SourceChecks,
    _binding,
    execute_requirement_query,
    knowledge_writeback,
)

METHODS = ("G0-P3", "G1-fixed-hop", "G2-contract-BFS", "G3-PPR", "G4-legal-reseed")
TOP_K = (5, 10, 20)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_corpus(project, root):
    index, manifest = load_active_index(project)
    root.mkdir(parents=True)
    for directory in ["config", "evidence/p1"]:
        shutil.copytree(project / directory, root / directory)
    shutil.copytree(index, root / "data/p3/indexes" / index.name)
    shutil.copy2(project / "data/p3/indexes/active.json", root / "data/p3/indexes/active.json")
    (root / "data/p2").mkdir(parents=True)
    shutil.copy2(project / "data/p2/corpus.sqlite3", root / "data/p2/corpus.sqlite3")
    import yaml

    corpus = yaml.safe_load((project / "config/corpus.yaml").read_text())
    chunks = load_chunks(index)
    (root / "data/raw").mkdir()
    for relative in sorted({c.relative_path for c in chunks.values()}):
        source = Path(corpus["source_root"]) / relative
        target = root / "data/raw" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        expected = {c.source_sha256 for c in chunks.values() if c.relative_path == relative}
        if expected != {sha(target)}:
            raise ValueError("physical corpus/index SHA differs")
    (root / ".venv-retrieval").symlink_to(project / ".venv-retrieval", target_is_directory=True)
    (root / "tools").mkdir()
    shutil.copy2(project / "tools/retrieval_worker.py", root / "tools/retrieval_worker.py")
    return chunks, manifest


def prepare_query(corpus, chunks, number):
    kind = "K" if number < 48 else "R" if number < 72 else "P"
    normal = [
        c
        for c in chunks.values()
        if c.product == "UPF"
        and c.version == "5.0"
        and c.token_count >= 15
        and c.section_path
        and c.section_path[0] != "目录"
    ]
    normal.sort(key=lambda c: c.chunk_id)
    target = normal[(number * 7) % len(normal)]
    mode = (
        (
            "mapped"
            if number < 24
            else ["unmapped", "wrong-purpose", "wrong-version", "missing-seed"][(number - 24) // 6]
        )
        if kind == "K"
        else (
            "available"
            if (number - 48) % 24 < 12
            else [
                "unknown-version",
                "missing-field",
                "permission-denied",
                "no-peer" if kind == "P" else "stale",
            ][(number - 48) % 12 // 3]
        )
    )
    root = corpus / f"data/query-sources/query-{number + 1:03d}"
    root.mkdir(parents=True)
    task = example(
        root,
        name=f"e2-{number + 1:03d}",
        template="manual_operation" if kind == "K" else "upf_n4_fault",
    )
    # Sources are inside the one isolated corpus used by every method.
    relative = task.observation_files[0]
    source = root / relative
    task.observation_files = [str(source.relative_to(corpus))]
    task.path.source_path = task.observation_files[0]
    body = json.loads(source.read_text())
    if kind != "K":
        if mode == "unknown-version":
            for r in body["observations"]:
                if r["category"] == kind:
                    r["version"] = None
        if mode == "missing-field":
            for r in body["observations"]:
                if r["category"] == kind:
                    r["fields"].pop("state" if kind == "R" else "mapping_version", None)
        if mode == "no-peer":
            body["observations"] = [
                r
                for r in body["observations"]
                if not (r["category"] == "P" and r["object_id"] == "SMF-B")
            ]
        if mode == "stale":
            from datetime import timedelta

            for r in body["observations"]:
                if r["category"] == "R":
                    r["observed"]["end"] = (task.as_of - timedelta(hours=1)).isoformat()
                    r["observed"]["start"] = (task.as_of - timedelta(hours=2)).isoformat()
        write_json(source, body)
        task.path.source_sha256 = sha(source)
        if mode == "permission-denied":
            task.permission.readable_fields.remove("state" if kind == "R" else "mapping_version")
    if mode == "wrong-version":
        task.version = "4.0"
    task.run_id = digest(["e2-query", number])[:32]
    task.model_enabled = False
    contract = compile_contract(task)
    requirement = next(r for r in contract.requirements if r.kind == kind and "UPF-A" in r.objects)
    if kind == "K":
        text = " / ".join(target.section_path) + " " + target.text.splitlines()[0][:70]
    elif kind == "R":
        text = (
            "只读获取UPF-A的N4运行观察：interface、state、n4_enabled；"
            "按对象、产品UPF、版本5.0、观测时间及300秒新鲜度核对；"
            "未知、陈旧或无权限时保留缺口，手册不能代替现场观察。"
        )
    else:
        text = (
            "只读获取UPF-A与SMF-B双侧映射：service_id、local_endpoint、peer_endpoint、"
            "direction、mapping_version、config_version和观测时间；"
            "服务service-001、映射map-1，核对反向端点和方向、版本及窗口一致性；"
            "缺侧、冲突或无权限时保留缺口，不能由单侧宣称双侧一致。"
        )
    task.question = text  # Graph contract must be recompiled after any task change.
    contract = compile_contract(task)
    requirement = next(r for r in contract.requirements if r.kind == kind and "UPF-A" in r.objects)
    bindings = []
    if kind != "K":
        for step in compile_query_plan(task, contract).steps:
            bindings.extend(
                EvidenceBinding.model_validate(b)
                for b in collect(corpus, task, contract, step, step.step_id)["bindings"]
            )
    relevant = []
    if kind == "K" and mode not in {"unmapped", "wrong-purpose", "wrong-version"}:
        relevant = [
            c.chunk_id
            for c in normal
            if c.source_id == target.source_id and c.parent_id == target.parent_id
        ]
    if kind != "K" and mode in {"available", "no-peer"}:
        relevant = [
            f"native:{b.native_id}:{b.object_id}"
            for b in bindings
            if b.requirement_id == requirement.requirement_id and b.category == kind
        ]
    return {
        "number": number + 1,
        "kind": kind,
        "mode": mode,
        "text": text,
        "task": task,
        "contract": contract,
        "requirement": requirement,
        "bindings": bindings,
        "relevant": relevant,
        "target_chunk": target.chunk_id,
        "input_revision": "review-remediation-e2-2",
        "query_requirement_consistent": True,
        "relevance_scope": "native_section_discovery" if kind == "K" else "runtime_mapping_clues",
        "related_fragments": relevant if kind == "K" else [],
        "equivalent_complete_operation_sets": None,
        "fragment_support": [
            {
                "chunk_id": cid,
                "locators": chunks[cid].locators,
                "content_sha256": hashlib.sha256(chunks[cid].text.encode()).hexdigest(),
                "complete_operation_approval": False,
            }
            for cid in relevant
            if kind == "K"
        ],
        "reference_reviewed": False,
        "reference_definition": (
            "K related fragments in the same native section: section discovery only, "
            "not equivalent complete procedures; R/P specification-selected source clues, "
            "not expert operational Gold"
        ),
    }


def build_graph(corpus, chunks, case):
    req = case["requirement"]
    native = [
        b
        for b in case["bindings"]
        if b.category == req.kind and b.requirement_id == req.requirement_id
    ]
    claims = []
    for b in native:
        claims.append(
            {
                "source": "object:UPF-A",
                "target": f"native:{b.native_id}:{b.object_id}",
                "relation": "SUPPORTED_BY",
            }
        )
    docs = [c for c in chunks.values() if c.product == "UPF"]
    for c in docs:
        claims += [
            {"source": c.chunk_id, "target": f"section:{c.parent_id}", "relation": "CONTAINS"},
            {"source": c.chunk_id, "target": "object:UPF-A", "relation": "DESCRIBES"},
        ]
    path = corpus / f"data/query-sources/query-{case['number']:03d}/logical-claims.json"
    write_json(
        path,
        {
            "synthetic": True,
            "reviewed": False,
            "relations": claims,
            "basis": (
                "native manual section membership plus explicit synthetic observation-object links"
            ),
        },
    )
    pointer = SourcePointer(
        source_id=f"e2-claims-{case['number']}",
        sha256=sha(path),
        relative_path=str(path.relative_to(corpus)),
        locator="/relations",
    )
    nodes = [
        GraphNode(
            node_id="object:UPF-A",
            kind="Object",
            layer="scope",
            source=pointer,
            object_ids=["UPF-A"],
            synthetic=True,
        )
    ]
    nodes += [
        GraphNode(
            node_id=f"section:{parent}",
            kind="Section",
            layer="knowledge",
            source=pointer,
            object_ids=["UPF-A"],
            version="5.0",
            synthetic=True,
        )
        for parent in sorted({c.parent_id for c in docs})
    ]
    annotations = []
    for c in docs:
        source = SourcePointer(
            source_id=c.source_id,
            sha256=c.source_sha256,
            relative_path=f"data/raw/{c.relative_path}",
            locator=";".join(c.locators) or c.chunk_id,
        )
        nodes.append(
            GraphNode(
                node_id=c.chunk_id,
                kind="DocumentBlock",
                layer="knowledge",
                source=source,
                object_ids=["UPF-A"],
                version=c.version,
                attributes={"text": c.text, "product": c.product, "domain": "domain-0"},
            )
        )
        if c.version == "5.0" and case["mode"] != "unmapped":
            annotations.append(
                KnowledgeAnnotation(
                    annotation_id=c.chunk_id,
                    source_sha256=source.sha256,
                    locator=source.locator,
                    content_sha256=hashlib.sha256(c.text.encode()).hexdigest(),
                    product=c.product,
                    version=c.version,
                    object_ids=["UPF-A"],
                    purposes=["upf_n4_fault"]
                    if case["mode"] == "wrong-purpose"
                    else ["manual_operation"],
                    basis_kind="trusted_rule",
                    basis_source=(
                        "development native manual scope rule; not expert operational approval"
                    ),
                    basis_version="1",
                    rule_id="e2-dev-manual-read-only",
                    reviewed=False,
                )
            )
    nodes += [
        GraphNode(
            node_id=f"native:{b.native_id}:{b.object_id}",
            kind="EvidenceBinding",
            layer="runtime",
            source=b.source,
            object_ids=[b.object_id],
            version=b.version,
            synthetic=True,
            attributes={"binding": b.model_dump(mode="json")},
        )
        for b in native
    ]
    edges = [
        GraphEdge(
            edge_id=f"e{i}",
            source_id=x["source"],
            target_id=x["target"],
            relation=x["relation"],
            source=pointer,
            synthetic=True,
        )
        for i, x in enumerate(claims)
    ]
    store = MemoryGraphStore()
    store.build(nodes, edges)
    registry = KnowledgeRegistry(version=f"e2-query-{case['number']}", annotations=annotations)
    return store, registry


def terminal_filter(corpus, store, query, registry, paths, counts):
    checks = SourceChecks(corpus)
    hits = []
    excluded = []
    for identifier, path in paths.items():
        node = store.nodes.get(identifier)
        if node is None:
            continue
        if query.denied_reasons:
            excluded.append({"id": identifier, "reason": query.denied_reasons[0]})
            continue
        reason = None
        for part in path["nodes"]:
            current = store.nodes.get(part)
            reason = "unknown_node" if current is None else exclusion(current, query.graph)
            if not reason and not checks.valid(current.source):
                reason = "source_hash_unverified"
            if reason:
                break
        if not reason:
            for edge_id in path["edges"]:
                edge = store.edges[edge_id]
                if (
                    edge.relation not in query.graph.relations
                    or not edge.corroborated
                    or not checks.valid(edge.source)
                ):
                    reason = "unusable_path_edge"
                    break
        if reason:
            excluded.append({"id": identifier, "reason": reason})
            continue
        binding, reason = _binding(node, query, registry)
        if reason:
            excluded.append({"id": identifier, "reason": reason})
        if binding:
            hits.append(
                {"node_id": identifier, "path": path, "binding": binding.model_dump(mode="json")}
            )
    return {
        "hits": hits[: query.top_k],
        "excluded": excluded,
        "scan": {
            **counts,
            "physical_source_hash_reads": checks.reads,
            "physical_source_hash_bytes": checks.bytes,
        },
        "ranking": {"status": "not_requested"},
    }


def fixed_hop(corpus, store, query, registry, *, only_seeds=False):
    paths = {}
    queue = deque()
    nodes = 0
    edges = 0
    for seed in query.graph.seed_ids:
        if nodes >= query.graph.max_nodes:
            break
        nodes += 1
        if seed not in store.nodes:
            continue
        paths[seed] = {"nodes": [seed], "edges": [], "hops": 0, "seed_origin": "primary"}
        queue.append(seed)
    while queue and not only_seeds:
        identifier = queue.popleft()
        if paths[identifier]["hops"] >= query.graph.max_hops:
            continue
        for edge in store.adjacency[identifier]:
            if edges >= query.graph.max_edges:
                break
            edges += 1
            if edge.relation not in query.graph.relations:
                continue
            other = edge.target_id if edge.source_id == identifier else edge.source_id
            if other in paths:
                continue
            if nodes >= query.graph.max_nodes:
                break
            nodes += 1
            paths[other] = {
                "nodes": [*paths[identifier]["nodes"], other],
                "edges": [*paths[identifier]["edges"], edge.edge_id],
                "hops": paths[identifier]["hops"] + 1,
                "seed_origin": "primary",
            }
            queue.append(other)
    return terminal_filter(
        corpus,
        store,
        query,
        registry,
        paths,
        {"nodes_scanned": nodes, "adjacency_entries_scanned": edges},
    )


def score_hits(case, result, k):
    selected = result["hits"][:k]
    relevant = set(case["relevant"])
    found = {h["node_id"] for h in selected}
    matched = found & relevant
    slots = {
        (b["object_id"], field)
        for h in selected
        for b in [h["binding"]]
        for field in case["requirement"].fields
        if field in b["fields"] and b["fields"][field] is not None
    }
    required = {
        (obj, field) for obj in case["requirement"].objects for field in case["requirement"].fields
    }
    return {
        "query": case["number"],
        "kind": case["kind"],
        "mode": case["mode"],
        "top_k": k,
        "returned": len(selected),
        "relevant_returned": len(matched),
        "relevant_total": len(relevant),
        "development_precision": len(matched) / len(found) if found else None,
        "development_recall": len(matched) / len(relevant) if relevant else None,
        "required_field_coverage": len(slots & required) / len(required) if required else None,
        "correct_no_evidence": not selected if not relevant and case["mode"] != "no-peer" else None,
        "invalid_acceptance_count": len(selected)
        if case["mode"]
        in {
            "unmapped",
            "wrong-purpose",
            "wrong-version",
            "unknown-version",
            "missing-field",
            "permission-denied",
            "stale",
        }
        else 0,
    }


def run_e2(project: Path, output: Path, device="cuda:1", seed_cache=None):
    project, output = project.resolve(), output.resolve()
    if output.exists() or not output.is_relative_to(project / "runtime/v8-next/phase3"):
        raise ValueError("new phase3 runtime required")
    output.mkdir(parents=True)
    source = source_manifest(project)
    corpus = output / "corpus"
    chunks, manifest = prepare_corpus(project, corpus)
    cases = [prepare_query(corpus, chunks, n) for n in range(96)]
    stores = []
    for case in cases:
        store, registry = build_graph(corpus, chunks, case)
        stores.append((store, registry))
        root = output / "queries" / f"query-{case['number']:03d}"
        write_json(
            root / "query-reference.json",
            {
                k: v.model_dump(mode="json")
                if hasattr(v, "model_dump")
                else [b.model_dump(mode="json") for b in v]
                if k == "bindings"
                else v
                for k, v in case.items()
            },
        )
        write_json(root / "graph.json", store.snapshot())
        write_json(root / "registry.json", registry.model_dump(mode="json"))
    inputs = {
        str(p.relative_to(output)): sha(p)
        for directory in [output / "queries", corpus / "data/query-sources", corpus / "data/raw"]
        for p in sorted(directory.rglob("*"))
        if p.is_file()
    }
    inputs.update(
        {
            str(corpus.relative_to(output))
            + "/data/p3/indexes/"
            + manifest["index_generation"]
            + "/chunks.jsonl": sha(
                corpus / "data/p3/indexes" / manifest["index_generation"] / "chunks.jsonl"
            )
        }
    )
    write_json(output / "input-hashes.json", inputs)
    write_json(
        output / "protocol.json",
        {
            "cases": 96,
            "kinds": {"K": 48, "R": 24, "P": 24},
            "pilot_queries": 24,
            "methods": METHODS,
            "top_k": TOP_K,
            "max_nodes": 100,
            "max_edges": 200,
            "max_hops": 2,
            "seed_count": 20,
            "seed_cache": (
                "actual P3 embedding/BM25/exact/rerank outputs, generated once and shared"
            ),
            "PPR": {"alpha": 0.85, "tolerance": 1e-8, "max_iterations": 1000},
            "source": source,
            "reviewed": False,
            "formal_acceptance": False,
            "R_P_scope": "retrieval hints only; no graph writeback",
            "input_revision": "review-remediation-e2-2",
            "K_scope": (
                "native section fragment discovery; complete-operation Gold remains unapproved"
            ),
            "device": device,
        },
    )
    config = load_model_config(project / "config/models.yaml")
    cache = []
    if seed_cache is not None:
        seed_cache = seed_cache.resolve()
        cache_hashes = {}
        for case in cases:
            path = seed_cache / f"query-{case['number']:03d}.json"
            raw = json.loads(path.read_text())
            if (
                raw["query"] != case["text"]
                or raw["product"] != "UPF"
                or raw["version"] != "5.0"
                or raw["index_generation"] != manifest["index_generation"]
            ):
                raise ValueError("cached P3 response belongs to different inputs")
            cache_hashes[str(path)] = sha(path)
            write_json(output / "seed-cache" / path.name, raw)
            cache.append(raw)
        write_json(output / "reused-seed-cache-hashes.json", cache_hashes)
    else:
        with ExitStack() as stack:
            embedding = stack.enter_context(
                RetrievalWorker(corpus, "embed", config.embedding.path, device=device)
            )
            reranker = stack.enter_context(
                RetrievalWorker(corpus, "rerank", config.reranker.path, device=device)
            )
            for case in cases:
                started = perf_counter()
                raw = search(
                    corpus,
                    case["text"],
                    product="UPF",
                    version="5.0",
                    device=device,
                    workers=(embedding, reranker),
                )
                raw["measured_retrieval_seconds"] = perf_counter() - started
                write_json(output / "seed-cache" / f"query-{case['number']:03d}.json", raw)
                cache.append(raw)
                write_json(
                    output / "progress.json",
                    {"phase": "P3-cache", "completed": len(cache), "expected": 96},
                )
    rows = []
    runs = 0
    for case, (store, registry), cached in zip(cases, stores, cache, strict=True):
        primary = cached["rankings"]["reranked"][:20]
        pool = cached["rankings"]["reranked"][:40]
        if case["mode"] == "missing-seed":
            primary = []
        query = compile_requirement_query(
            case["task"], case["contract"], case["requirement"], primary, reseed_ids=pool, top_k=20
        )
        root = output / "results" / f"query-{case['number']:03d}"
        for method in METHODS:
            started = perf_counter()
            if method in METHODS[:2]:
                result = fixed_hop(corpus, store, query, registry, only_seeds=method == METHODS[0])
            else:
                result = execute_requirement_query(
                    corpus,
                    store,
                    query,
                    registry=registry,
                    strategy={METHODS[2]: "bfs", METHODS[3]: "ppr", METHODS[4]: "bfs-reseed"}[
                        method
                    ],
                    snapshot_sha256=digest(store.snapshot()),
                )
            result["method"] = method
            result["retrieval_seconds_without_seed"] = perf_counter() - started
            result["seed_preparation_seconds"] = cached["measured_retrieval_seconds"]
            result["total_retrieval_seconds"] = (
                result["retrieval_seconds_without_seed"] + result["seed_preparation_seconds"]
            )
            result["primary_seeds"] = primary
            result["reseed_pool"] = pool
            if case["kind"] == "K" and method in METHODS[2:]:
                accepted, rejected = knowledge_writeback(
                    corpus,
                    query,
                    result,
                    f"e2:{case['number']}:{method}",
                    store=store,
                    registry=registry,
                )
                result["writeback_count"] = len(accepted)
                result["writeback_bindings"] = [b.model_dump(mode="json") for b in accepted]
                result["writeback_rejected"] = rejected
                result["writeback_scope"] = (
                    "separate auxiliary admission audit; excluded from retrieval scan "
                    "budget and latency comparison"
                )
            write_json(root / f"{method}.json", result)
            runs += 1
            for k in TOP_K:
                rows.append(
                    {
                        **score_hits(case, result, k),
                        "method": method,
                        "scan": result["scan"],
                        "total_retrieval_seconds": result["total_retrieval_seconds"],
                        "pilot": case["number"] <= 24,
                    }
                )
        write_json(
            output / "progress.json",
            {"phase": "graph-retrieval", "completed": runs, "expected": 480},
        )
    summaries = {}
    for method in METHODS:
        summaries[method] = {}
        for k in TOP_K:
            subset = [r for r in rows if r["method"] == method and r["top_k"] == k]
            summaries[method][str(k)] = {
                "observations": len(subset),
                "invalid_acceptance": sum(r["invalid_acceptance_count"] for r in subset),
                "relevant_returned": sum(r["relevant_returned"] for r in subset),
                "relevant_total": sum(r["relevant_total"] for r in subset),
                "macro_recall": sum(
                    r["development_recall"] for r in subset if r["development_recall"] is not None
                )
                / sum(r["development_recall"] is not None for r in subset),
                "correct_no_evidence": Counter(str(r["correct_no_evidence"]) for r in subset),
                "max_nodes_scanned": max(r["scan"]["nodes_scanned"] for r in subset),
                "max_adjacency_scanned": max(
                    r["scan"]["adjacency_entries_scanned"] for r in subset
                ),
            }
    summary = {
        "queries": 96,
        "P3_search_calls": 96 if seed_cache is None else 0,
        "actual_P3_cache_entries": 96,
        "reused_cache": str(seed_cache) if seed_cache else None,
        "method_retrievals": 480,
        "pilot_method_retrievals": 120,
        "top_k_observations": len(rows),
        "groups": summaries,
        "engineering_pass": all(
            r["invalid_acceptance_count"] == 0
            and r["scan"]["nodes_scanned"] <= 100
            and r["scan"]["adjacency_entries_scanned"] <= 200
            for r in rows
        ),
        "input_hashes_unchanged": all(sha(output / name) == h for name, h in inputs.items()),
        "source_unchanged": source_manifest(project) == source,
        "seed_cache_hashes_unchanged": seed_cache is None
        or all(sha(Path(n)) == h for n, h in cache_hashes.items()),
        "source": source,
        "formal_acceptance": False,
        "independent_query_gold_count": 0,
        "R_P_writeback": False,
    }
    write_json(output / "observations.json", rows)
    write_json(output / "summary.json", summary)
    return summary
