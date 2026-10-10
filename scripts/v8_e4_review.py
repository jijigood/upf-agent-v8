"""Recompute saved E4 CSV costs and denominators without rerunning experiments."""

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

from upf_agent.v8.e4 import MODES, matrix_groups, write_json
from upf_agent.v8.evaluation import percentiles


def review(root, output):
    if output.exists():
        raise ValueError("review output exists; choose a new ID")
    summary_path = root / "summary.json"
    summary = json.loads(summary_path.read_text())
    errors, groups, hashes = [], {}, {}
    specifications = matrix_groups(summary["profile"])
    expected_per_method = sum(spec[2] * spec[3] for spec in specifications)
    counts = Counter()
    for name, group in summary["groups"].items():
        path = root / name / "batches.csv"
        hashes[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
        with path.open() as stream:
            rows = list(csv.DictReader(stream))
        identities = [(r["seed"], r["batch"], r["method"]) for r in rows]
        if len(identities) != len(set(identities)):
            errors.append(f"{name}: duplicate batch/method")
        pairs = Counter((r["seed"], r["batch"]) for r in rows)
        if set(pairs.values()) != {4}:
            errors.append(f"{name}: incomplete pairs")
        methods = {}
        for mode in MODES:
            selected = [r for r in rows if r["method"] == mode]
            actual = {
                "batches": len(selected),
                "consistent": sum(r["consistent"] == "True" for r in selected),
                "seconds": percentiles([float(r["seconds"]) for r in selected]),
                "total_seconds": sum(float(r["seconds"]) for r in selected),
                "cpu_seconds": sum(float(r["cpu_seconds"]) for r in selected),
                "fallbacks": sum(r["fallback"] == "full_fallback" for r in selected),
                "cost_totals": {
                    key: sum(float(r[key]) for r in selected)
                    for key in selected[0]
                    if key.endswith("_seconds") and key != "cpu_seconds"
                },
            }
            expected = group["methods"][mode]
            for key in ("batches", "consistent", "fallbacks"):
                if actual[key] != expected[key]:
                    errors.append(f"{name}/{mode}/{key}")
            for key in ("total_seconds", "cpu_seconds"):
                if not math.isclose(actual[key], expected[key], rel_tol=1e-12):
                    errors.append(f"{name}/{mode}/{key}")
            for category in ("seconds", "cost_totals"):
                for key, value in actual[category].items():
                    if not math.isclose(value, expected[category][key], rel_tol=1e-12):
                        errors.append(f"{name}/{mode}/{category}/{key}")
            actual["initialization"] = {
                "samples": sum(r["method"] == mode for r in group["initialization"]),
                "cold_seconds": expected["cold_seconds"],
                "component_totals": {
                    key: sum(r.get(key, 0) for r in group["initialization"] if r["method"] == mode)
                    for key in {
                        k for r in group["initialization"] for k in r if k.endswith("_seconds")
                    }
                },
            }
            counts[mode] += actual["batches"]
            methods[mode] = actual
        for actual in methods.values():
            actual["paired_total_full_over_method"] = (
                methods["L0-Full"]["total_seconds"] / actual["total_seconds"]
            )
        groups[name] = methods
    result = {
        "schema": "e4-saved-results-review-1",
        "input": str(root),
        "summary_sha256": hashlib.sha256(summary_path.read_bytes()).hexdigest(),
        "csv_hashes": hashes,
        "source_sha256": summary["source"]["sha256"],
        "method_batches": dict(counts),
        "profile": summary["profile"],
        "expected_method_batches": expected_per_method * len(MODES),
        "groups": groups,
        "negative_groups": {
            mode: [
                name
                for name, methods in groups.items()
                if methods[mode]["paired_total_full_over_method"] < 1
            ]
            for mode in MODES
            if mode != "L0-Full"
        },
        "workers": summary["workers"],
        "throughput_4_workers": (
            summary["method_batches"] / summary["elapsed_seconds"]
            if summary["workers"] == 4
            else None
        ),
        "throughput_units": "matrix method-batches/second including initialization and export",
        "throughput_status": (
            "actual four-worker matrix; shared-host observation"
            if summary["workers"] == 4
            else "single-worker matrix"
        ),
        "cold_status": "initialization on an already running process; no OS cache eviction",
        "fallback_cost": "subset of propagation/recompute; do not add twice",
        "shared_host": "concurrent work recorded; observational timings, no exclusive-host claim",
        "errors": errors,
        "pass": not errors
        and summary["pass"]
        and summary["method_batches"] == expected_per_method * len(MODES)
        and sum(counts.values()) == expected_per_method * len(MODES)
        and set(counts) == set(MODES)
        and all(v == expected_per_method for v in counts.values()),
    }
    write_json(output, result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = review(args.input, args.output)
    print(
        json.dumps(
            {k: v for k, v in result.items() if k not in {"groups", "csv_hashes"}},
            ensure_ascii=False,
        )
    )
