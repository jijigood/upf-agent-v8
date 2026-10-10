"""Recompute E7 infrastructure evidence; never substitute it for RCA accuracy."""

import argparse
import hashlib
import json
from pathlib import Path

from v8_e7_agent import parse_log
from v8_e7_runner import CONDITIONS, injection_verified, write

from upf_agent.v8.adapters import verify_binding
from upf_agent.v8.models import EvidenceBinding


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def audit(root):
    summary = read(root / "summary.json")
    rows = []
    for row in summary["rows"]:
        n = row["round"]
        private = root / "private" / f"round-{n:03d}"
        round_root = root / "rounds" / f"round-{n:03d}"
        snapshot = read(round_root / "input/snapshot.json")
        external = read(private / "external-verification.json")
        truth = read(private / "truth.json")
        integration = read(round_root / "agent/integration.json")
        source = read(round_root / "agent/data/e7/observations.json")
        condition = CONDITIONS[(n - 1) // 3]
        verified = injection_verified(
            condition, external["probe"], external["independent_state"], snapshot
        )
        reports = list((round_root / "agent/runs/v8").glob("*/report.json"))
        report = read(reports[0]) if len(reports) == 1 else None
        bindings_ok = report is not None and all(
            verify_binding(round_root / "agent", EvidenceBinding.model_validate(b))
            for b in report["bindings"]
        )
        bindings_ok &= (
            report is not None
            and len(report["bindings"]) == integration["binding_count"]
            and not any(g.startswith("tool_failed:") for g in report["query_plan"]["gaps"])
            and not any(a["execute_authorized"] for a in report["actions"])
            and source["raw_capture_sha256"] == sha(round_root / "input/snapshot.json")
            and len(source["observations"]) == integration["expected_runtime_observations"]
        )
        parsed = read(round_root / "agent/parsed-logs.json")
        parse_ok = True
        lines, headers = 0, 0
        for role in ("core", "ue"):
            for name, text in snapshot[role]["logs_and_config"].items():
                if not name.endswith(".log"):
                    continue
                expected = parse_log(text, name[:-4])
                parse_ok &= expected == parsed[name]
                parse_ok &= (expected[-1]["byte_end"] if expected else 0) == len(text.encode())
                lines += len(expected)
                headers += sum(x["parsed_header"] for x in expected)
        visible_ok = set(snapshot) == {"core", "ue", "window_start", "window_end"}
        before = read(private / "health-before.json")["pass"]
        after = read(private / "health-after.json")["pass"]
        passed = (
            verified
            and truth["verified"]
            and truth["condition"] == condition == row["condition"]
            and before
            and after
            and bindings_ok
            and parse_ok
            and visible_ok
            and integration["pass"]
            and integration["tool_errors"] == []
            and integration["binding_count"] == integration["expected_runtime_observations"]
            and not integration["execute_authorized"]
            and integration["root_cause_ranking"] is None
        )
        rows.append(
            {
                "round": n,
                "condition": condition,
                "source_bindings_verified": bindings_ok,
                "parser_recomputed": parse_ok,
                "lines": lines,
                "headers_matched": headers,
                "unmatched_preserved": lines - headers,
                "injection_recomputed": verified,
                "recovered": after,
                "engine_status": integration["status"],
                "binding_count": integration["binding_count"],
                "integration_seconds": integration["diagnosis_seconds"],
                "process_seconds": read(private / "agent-process.json")["seconds"],
                "pass": passed,
            }
        )
    return {
        "schema": "e7-infrastructure-audit-1",
        "rows": rows,
        "pass": len(rows) == 18
        and all(r["pass"] for r in rows)
        and all(r["returncode"] == 0 for r in read(root / "private/teardown.json")),
        "root_cause_top1": None,
        "root_cause_top3": None,
        "formal_quality": False,
        "model_calls": 0,
        "reviewed": False,
        "helper_bytes_unchanged": all(
            sha(root / "code" / name) == value
            for name, value in read(root / "code-hashes.json").items()
        ),
        "raw_manifest": {
            str(p.relative_to(root)): sha(p) for p in sorted(root.rglob("*")) if p.is_file()
        },
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    if a.output.exists() or a.output.resolve().is_relative_to(a.root.resolve()):
        p.error("new audit file outside immutable experiment required")
    result = audit(a.root.resolve())
    result["pass"] &= result["helper_bytes_unchanged"]
    write(a.output, result)
    print({"pass": result["pass"], "rounds": len(result["rows"])})
    raise SystemExit(0 if result["pass"] else 1)
