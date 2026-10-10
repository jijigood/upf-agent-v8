"""E7 read-only CPU collector/Engine probe; not a validated RCA model comparator."""

import argparse
import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter

from upf_agent.v8.engine import OrchestrationEngine
from upf_agent.v8.models import OrchestrationTask, PermissionScope

OPEN5GS = re.compile(r"^\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d{3}: \[(\w+)\] (\w+): (.*)$")
UERANSIM = re.compile(
    r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})\] \[([^]]+)\] \[(\w+)\] (.*)$"
)


def parse_log(text, component):
    events = []
    offset = 0
    for number, line in enumerate(text.splitlines(keepends=True), 1):
        clean = re.sub(r"\x1b\[[0-9;]*m", "", line.rstrip())
        match = (UERANSIM if component in {"gnb", "ue"} else OPEN5GS).match(clean)
        events.append(
            {
                "line": number,
                "byte_start": offset,
                "byte_end": offset + len(line.encode()),
                "parsed_header": bool(match),
                "component": component,
                "severity": match.groups()[-2] if match else None,
                "message": match.groups()[-1] if match else line.rstrip(),
                "timestamp_inference": None,
            }
        )
        offset += len(line.encode())
    return events


def guard(input_root, output, private_root):
    experiment_root = private_root.parent

    def audit(event, args):
        if event in {
            "socket.connect",
            "socket.bind",
            "subprocess.Popen",
            "os.system",
            "os.exec",
            "os.posix_spawn",
        }:
            raise PermissionError("E7 agent cannot contact or execute lab controls")
        if event == "open" and isinstance(args[0], (str, bytes)):
            p = Path(args[0]).resolve()
            if p.is_relative_to(private_root):
                raise PermissionError("E7 hidden truth denied")
            if (
                p.is_relative_to(experiment_root)
                and not p.is_relative_to(input_root)
                and not p.is_relative_to(output)
            ):
                raise PermissionError("E7 agent reads limited to visible capture and result root")
            mode, flags = args[1], args[2]
            write = (isinstance(mode, str) and any(c in mode for c in "wax+")) or (flags & 3 != 0)
            if write and not p.is_relative_to(output):
                raise PermissionError("E7 agent writes confined to result root")
        if event in {"os.remove", "os.rmdir", "os.mkdir", "os.rename", "os.chmod", "os.truncate"}:
            paths = args[:2] if event == "os.rename" else args[:1]
            if any(
                isinstance(p, (str, bytes)) and not Path(p).resolve().is_relative_to(output)
                for p in paths
            ):
                raise PermissionError("E7 agent mutation outside result root")
        if event == "sqlite3.connect" and str(args[0]) != ":memory:":
            if not Path(args[0]).resolve().is_relative_to(output):
                raise PermissionError("E7 SQLite restricted to result root")

    sys.addaudithook(audit)


def run(input_root, output, private_root):
    if output.exists():
        raise ValueError("new output ID required")
    output.mkdir(parents=True)
    guard(input_root.resolve(), output.resolve(), private_root.resolve())
    snapshot = json.loads((input_root / "snapshot.json").read_text())
    started = perf_counter()
    parsed = {}
    for role in ("core", "ue"):
        for name, text in snapshot[role]["logs_and_config"].items():
            if name.endswith(".log"):
                parsed[name] = parse_log(text, name[:-4])
    # Provenance-backed runtime facts: no handbook instruction or physical mapping invented.
    now = datetime.now(UTC).isoformat()
    observations = []
    for obj in ("upf", "smf"):
        events = parsed.get(obj + ".log", [])
        if events:
            observations.append(
                {
                    "object_id": obj,
                    "category": "R",
                    "fields": {"event_type": "open5gs_log_observation"},
                    "product": "Open5GS",
                    "version": "2.7.6",
                    "config_version": None,
                    "observed": {
                        "start": snapshot["window_start"],
                        "end": snapshot["window_end"],
                        "timezone_source": "UTC controller capture clock; not inferred event time",
                    },
                    "purposes": ["log_observation"],
                    "raw_events": events,
                }
            )
    source = {
        "source_id": "e7-real-log-capture",
        "synthetic": False,
        "corroborated": False,
        "observations": observations,
        "raw_capture_sha256": hashlib.sha256(
            (input_root / "snapshot.json").read_bytes()
        ).hexdigest(),
    }
    data = output / "data/e7"
    data.mkdir(parents=True)
    (data / "observations.json").write_text(json.dumps(source))
    task = OrchestrationTask(
        template="log_observation",
        question="只读核验 UPF/SMF 实际日志；缺少知识或双侧映射时保留缺口。",
        objects=["upf", "smf"],
        product="Open5GS",
        version="2.7.6",
        as_of=now,
        permission=PermissionScope(objects=["upf", "smf"], readable_fields=["event_type"]),
        observation_files=["data/e7/observations.json"],
        synthetic=False,
        graph_enabled=False,
        model_enabled=False,
        retrieval_device="cpu",
    )
    engine = OrchestrationEngine(output)
    try:
        result = engine.run(task)
    finally:
        engine.close()
    summary = {
        "method": "v8-log-observation-integration",
        "root_cause_ranking": None,
        "status": result["status"],
        "binding_count": len(result["bindings"]),
        "expected_runtime_observations": len(observations),
        "tool_errors": [g for g in result["query_plan"]["gaps"] if g.startswith("tool_failed:")],
        "execute_authorized": any(x["execute_authorized"] for x in result["actions"]),
        "model_calls": 0,
        "synthetic": False,
        "reviewed": False,
        "parser": {
            "version": "open5gs-ueransim-lines-001",
            "files": {
                k: {
                    "lines": len(v),
                    "headers_matched": sum(e["parsed_header"] for e in v),
                    "unmatched_preserved": sum(not e["parsed_header"] for e in v),
                }
                for k, v in parsed.items()
            },
        },
        "diagnosis_seconds": perf_counter() - started,
        "pass": result["status"] in {"completed", "needs_evidence", "blocked"}
        and len(result["bindings"]) == len(observations)
        and not any(g.startswith("tool_failed:") for g in result["query_plan"]["gaps"])
        and not any(x["execute_authorized"] for x in result["actions"]),
    }
    (output / "parsed-logs.json").write_text(json.dumps(parsed, indent=2))
    (output / "integration.json").write_text(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--private-root", type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(run(a.input, a.output, a.private_root)))
