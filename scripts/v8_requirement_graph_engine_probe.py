"""Persist three CPU-only engine/ledger integration probes; not retrieval-quality comparisons."""

import argparse
import hashlib
from pathlib import Path

from upf_agent.v8.e4 import write_json
from upf_agent.v8.engine import OrchestrationEngine
from upf_agent.v8.experiment_manifest import source_manifest
from upf_agent.v8.graph import MemoryGraphStore
from upf_agent.v8.models import digest
from upf_agent.v8.wp08 import STRATEGIES, make_case


def run(project, output):
    if output.exists():
        raise ValueError("use a new experiment ID")
    output.mkdir(parents=True)
    source = source_manifest(project)
    fixtures = []
    for strategy in STRATEGIES:
        root = output / strategy
        task, _, req, store, _, _, _, _ = make_case(root)
        if strategy != "bfs-reseed":
            # Synthetic cached anchor equals the deterministic ordinary K tool's native ID.
            # This is an integration input, not an executed P3 embedding/search experiment.
            alias = digest(
                [task.run_id, req.requirement_id, req.objects[0], task.observation_files[0], 0]
            )[:24]
            snapshot = store.snapshot()
            for node in snapshot["nodes"]:
                if node["node_id"] == "doc":
                    node["node_id"] = alias
            for edge in snapshot["edges"]:
                if edge["target_id"] == "doc":
                    edge["target_id"] = alias
            claims = root / "data/fixtures/wp08/graph-claims.json"
            write_json(
                claims,
                {
                    "synthetic": True,
                    "logical_relations": [
                        {
                            "source": e["source_id"],
                            "target": e["target_id"],
                            "relation": e["relation"],
                        }
                        for e in snapshot["edges"]
                    ],
                },
            )
            sha = hashlib.sha256(claims.read_bytes()).hexdigest()
            for record in [*snapshot["nodes"], *snapshot["edges"]]:
                if record["source"]["source_id"] == "wp08-logical-claims":
                    record["source"]["sha256"] = sha
            store = MemoryGraphStore.restore(snapshot)
        write_json(root / "data/v8/manual_graph.json", store.snapshot())
        write_json(
            root / "input-before-engine.json",
            {
                "task": task.model_dump(mode="json"),
                "synthetic": True,
                "reviewed": False,
                "strategy": strategy,
                "reseed_ids": ["doc"] if strategy == "bfs-reseed" else [],
            },
        )
        fixtures.append((strategy, root, task))
    rows = []
    for strategy, root, task in fixtures:
        engine = OrchestrationEngine(
            root,
            requirement_graph_strategy=strategy,
            graph_reseed_ids=["doc"] if strategy == "bfs-reseed" else [],
        )
        try:
            result = engine.run(task)
            graph_bindings = [b for b in result["bindings"] if ":graph:" in b["evidence_id"]]
            import json

            trace = json.loads(
                (root / "runs/v8" / task.run_id / "requirement-graph-0.json").read_text()
            )
            counters = engine.ledger.metrics(task.run_id)
            rows.append(
                {
                    "strategy": strategy,
                    "run_id": task.run_id,
                    "status": result["status"],
                    "graph_binding_ids": [b["evidence_id"] for b in graph_bindings],
                    "nodes_scanned_with_audit": trace["discovery_and_audit_nodes_scanned"],
                    "adjacency_scanned_with_audit": trace[
                        "discovery_and_audit_adjacency_entries_scanned"
                    ],
                    "metrics": counters,
                    "pass": bool(graph_bindings)
                    and result["status"] == "completed"
                    and all(s["code"] == "satisfied" for s in result["states"].values())
                    and trace["discovery_and_audit_nodes_scanned"] <= 100
                    and trace["discovery_and_audit_adjacency_entries_scanned"] <= 200
                    and all(not a["execute_authorized"] for a in result["actions"]),
                }
            )
        finally:
            engine.close()
    summary = {
        "source": source,
        "rows": rows,
        "synthetic": True,
        "reviewed": False,
        "model_calls": 0,
        "formal_e2": False,
        "source_unchanged": source_manifest(project) == source,
        "pass": len(rows) == 3 and all(r["pass"] for r in rows),
    }
    summary["pass"] &= summary["source_unchanged"]
    write_json(output / "summary.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.project.resolve(), args.output.resolve())
    print({"pass": result["pass"], "engine_runs": len(result["rows"])})
    raise SystemExit(0 if result["pass"] else 1)
