"""Isolated source-preserving P2 corpus, lexical P3 index and native manual graph.

No dense/reranker reproduction is claimed. Applicability is a preregistered
product/version provenance rule for read-only investigation, not expert causality.
"""

import hashlib
import json
import re
import shutil
from pathlib import Path

from tokenizers import Tokenizer

from upf_agent.contracts import DocumentBlock
from upf_agent.corpus_db import connect
from upf_agent.p3_chunks import RetrievalChunk
from upf_agent.p3_index import load_active_index, load_chunks
from upf_agent.p3_lexical import TechnicalTokenizer, build_bm25, build_exact, search_bm25
from upf_agent.v8.builders import manual_graph
from upf_agent.v8.e1_dataset import read, sha, write
from upf_agent.v8.knowledge_applicability import KnowledgeAnnotation, KnowledgeRegistry
from upf_agent.v8.models import digest

VERSION = "v8-e1-pinned-plaintext-lexical-corpus-2"
RULE = {
    "id": "pinned-upstream-version-readonly-reference-1",
    "purpose": "runtime_investigation",
    "scope": (
        "public original text; exact product/version/object mapping; no causal or command approval"
    ),
    "expert_reviewed": False,
}


def build(project, output):
    if output.exists():
        raise ValueError("fresh isolated manual corpus required")
    previous = project / "runtime/v8-next/e1-planning-progress-20261011-001"
    entries = []
    for item in read(previous / "knowledge-sources/index.json"):
        if item["id"] != "license":
            entries.append({**item, "path": previous / item["file"]})
    for item in read(previous / "knowledge-supplement-002/index.json"):
        if item["upstream_path"] != "LICENSE":
            entries.append(
                {
                    **item,
                    "id": "ueransim-" + Path(item["file"]).stem,
                    "path": project / item["file"],
                }
            )
    for item in entries:
        if sha(item["path"]) != item["sha256"]:
            raise ValueError("pinned upstream source changed")
    output.mkdir(parents=True)
    tokenizer = Tokenizer.from_file("/home/huangxiaolin/models/Qwen3-Embedding-4B/tokenizer.json")
    chunks, blocks, annotations, sources = [], [], [], []
    for item in entries:
        relative = f"e1-manuals/{item['id']}/{item['path'].name}"
        target = output / "data/raw" / relative
        target.parent.mkdir(parents=True)
        shutil.copy2(item["path"], target)
        text = target.read_text()
        encoded = tokenizer.encode(text, add_special_tokens=False)
        for ordinal, token_start in enumerate(range(0, len(encoded.ids), 600)):
            start = 0 if token_start == 0 else encoded.offsets[token_start][0]
            stop_token = token_start + 600
            stop = encoded.offsets[stop_token][0] if stop_token < len(encoded.ids) else len(text)
            content = text[start:stop]
            headings = re.findall(r"^#{1,6}\s+(.+)$", text[:start], flags=re.M)
            section = [item["id"], headings[-1] if headings else "preamble"]
            locator = f"chars:{start}:{stop}"
            cid = "e1-k-" + digest([item["sha256"], locator])[:24]
            block = DocumentBlock(
                source_id=item["id"],
                block_id=cid,
                section_path=section,
                kind="paragraph",
                raw_text=content,
                normalized_text=content,
                locator=locator,
                extraction_method=VERSION,
                ordinal=ordinal,
                quality_flags=["expert_semantics_unreviewed"],
            )
            chunk = RetrievalChunk(
                chunk_id=cid,
                source_id=item["id"],
                source_sha256=item["sha256"],
                relative_path=relative,
                product=item["product"],
                version=item["version"],
                section_path=section,
                parent_id=item["id"],
                kind="prose",
                text=content,
                token_count=len(tokenizer.encode(content, add_special_tokens=False).ids),
                block_ids=[cid],
                locators=[locator],
                ordinal_start=ordinal,
                ordinal_end=ordinal,
                extraction_methods=[VERSION],
                quality_flags=["expert_semantics_unreviewed"],
            )
            blocks.append(block)
            chunks.append(chunk)
            annotations.append(
                KnowledgeAnnotation(
                    annotation_id=cid,
                    source_sha256=item["sha256"],
                    locator=locator,
                    content_sha256=hashlib.sha256(content.encode()).hexdigest(),
                    product=item["product"],
                    version=item["version"],
                    object_ids=["upf"] if item["product"] == "Open5GS" else ["ran", "ue"],
                    purposes=["runtime_investigation"],
                    basis_kind="trusted_rule",
                    basis_source="data/v8/knowledge-rule.json",
                    basis_version=digest(RULE),
                    rule_id=RULE["id"],
                    reviewed=False,
                )
            )
        sources.append(
            {k: item[k] for k in ("id", "sha256", "product", "version", "commit", "url")}
            | {"relative_path": relative}
        )
    generation = digest({"sources": sources, "version": VERSION, "rule": RULE})[:20]
    db = connect(output / "data/p2/corpus.sqlite3")
    try:
        with db:
            db.execute(
                "INSERT INTO generations VALUES(?,?,?,?,?)",
                (
                    generation,
                    VERSION,
                    "ready",
                    json.dumps(sources),
                    json.dumps({"blocks": len(blocks), "sources": len(sources)}),
                ),
            )
            db.execute("INSERT INTO active_generation VALUES(1,?)", (generation,))
            for source in sources:
                db.execute(
                    "INSERT INTO sources VALUES(?,?,?,?,?,?,?)",
                    (
                        generation,
                        source["id"],
                        source["sha256"],
                        source["relative_path"],
                        "manual",
                        source["product"],
                        source["version"],
                    ),
                )
            for block in blocks:
                db.execute(
                    "INSERT INTO blocks VALUES(?,?,?,?,?,?,?,?)",
                    (
                        generation,
                        block.block_id,
                        block.source_id,
                        block.ordinal,
                        block.kind,
                        json.dumps(block.section_path),
                        block.normalized_text,
                        block.model_dump_json(),
                    ),
                )
    finally:
        db.close()
    directory = output / "data/p3/indexes" / generation
    directory.mkdir(parents=True)
    archive = directory / "chunks.jsonl"
    archive.write_text("".join(c.model_dump_json() + "\n" for c in chunks))
    dictionary = output / "data/p3/telecom_dictionary.txt"
    shutil.copy2(project / "config/telecom_dictionary.txt", dictionary)
    stats = build_bm25(chunks, dictionary, directory / "bm25")
    build_exact([], chunks, directory / "exact.json")
    write(
        directory / "manifest.json",
        {
            "index_generation": generation,
            "p2_generation": generation,
            "chunks_sha256": sha(archive),
            "stats": stats,
            "implementation": VERSION,
            "backends": ["BM25", "native-memory-graph"],
            "dense_or_rerank": False,
        },
    )
    write(output / "data/p3/indexes/active.json", {"index_generation": generation})
    write(output / "data/v8/knowledge-rule.json", RULE)
    registry = KnowledgeRegistry(version=VERSION + ":" + generation, annotations=annotations)
    write(output / "data/v8/knowledge_applicability.json", registry.model_dump(mode="json"))
    # Use the original graph builder and archive loader, rather than a dummy graph flag.
    graph = manual_graph(output)
    write(output / "data/v8/manual_graph.json", graph.snapshot())
    write(output / "source-index.json", sources)
    verified = audit(output)
    write(output / "audit.json", verified)
    write(
        output / "sha256_manifest.json",
        {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()},
    )
    return verified


def audit(root):
    directory, manifest = load_active_index(root)
    if sha(directory / "chunks.jsonl") != manifest["chunks_sha256"]:
        raise ValueError("manual archive changed")
    chunks = load_chunks(directory)
    for c in chunks.values():
        source = root / "data/raw" / c.relative_path
        _, start, stop = c.locators[0].split(":")
        if sha(source) != c.source_sha256 or source.read_text()[int(start) : int(stop)] != c.text:
            raise ValueError("manual original character projection mismatch")
    probes = {}
    tokenizer = TechnicalTokenizer(root / "data/p3/telecom_dictionary.txt")
    for product, version, query in (
        ("Open5GS", "2.7.6", "ogstun upf session"),
        ("UERANSIM", "3.2.7", "UERANSIM UE sessions"),
    ):
        hits = search_bm25(directory / "bm25", chunks, tokenizer, query, product, version, 3)
        if not hits:
            raise ValueError("actual product-scoped BM25 probe returned no documents")
        probes[product] = hits
    return {
        "p2_p3_pass": True,
        "sources": len({c.source_id for c in chunks.values()}),
        "chunks": len(chunks),
        "original_character_projections_verified": len(chunks),
        "actual_bm25_probes": probes,
        "graph_nodes": len(read(root / "data/v8/manual_graph.json")["nodes"]),
        "human_applicability_reviews": 0,
        "dense_or_rerank": False,
    }
