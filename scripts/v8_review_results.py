"""Export actual revised engineering matrices without mixing formal human VPR."""

import argparse
import csv
import hashlib
import json
from pathlib import Path


def read(p):
    return json.loads(p.read_text())


def export(root, output):
    if output.exists():
        raise ValueError("fresh output required")
    rows = []

    def add(experiment, method, metric, value, denominator, unit, source, scope):
        rows.append(
            {
                "experiment": experiment,
                "method": method,
                "metric": metric,
                "value": value,
                "denominator": denominator,
                "unit": unit,
                "source_sha256": source,
                "correlation_scope": scope,
                "approved_Gold": False,
                "formal_VPR": None,
            }
        )

    p2 = root / "phase2/review-closure-full-001"
    saved = [json.loads(line) for line in (p2 / "metrics-by-case.jsonl").read_text().splitlines()]
    source = read(p2 / "source_manifest.json")["sha256"]
    for method in sorted({r["method"] for r in saved}):
        chosen = [r for r in saved if r["method"] == method]
        for metric in ["validator_pass", "reference_pass"]:
            add(
                p2.name,
                method,
                metric,
                sum(r[metric] for r in chosen),
                len(chosen),
                "count",
                source,
                "24 synthetic cases, related templates; reference unapproved",
            )
    e2 = root / "phase3/review-e2-full-001"
    a = read(e2 / "summary.json")
    observations = read(e2 / "observations.json")
    for method, cutoffs in a["groups"].items():
        for cutoff, result in cutoffs.items():
            selected = [
                r for r in observations if r["method"] == method and r["top_k"] == int(cutoff)
            ]
            assert len(selected) == result["observations"]
            values = [
                (
                    "macro_recall",
                    result["macro_recall"],
                    sum(r["development_recall"] is not None for r in selected),
                    "fraction",
                ),
                (
                    "relevant_returned",
                    result["relevant_returned"],
                    result["relevant_total"],
                    "count",
                ),
                (
                    "invalid_acceptance",
                    result["invalid_acceptance"],
                    sum(r["returned"] for r in selected),
                    "count",
                ),
                (
                    "correct_no_evidence",
                    sum(r["correct_no_evidence"] is True for r in selected),
                    sum(r["correct_no_evidence"] is not None for r in selected),
                    "count",
                ),
                (
                    "max_nodes_scanned",
                    result["max_nodes_scanned"],
                    len(selected),
                    "max-nodes-per-query",
                ),
                (
                    "max_adjacency_scanned",
                    result["max_adjacency_scanned"],
                    len(selected),
                    "max-adjacency-per-query",
                ),
            ]
            for metric, value, denominator, unit in values:
                add(
                    e2.name,
                    method + "/top-k-" + cutoff,
                    metric,
                    value,
                    denominator,
                    unit,
                    a["source"]["sha256"],
                    "96 correlated development queries; K chapter relevance only; "
                    "R/P controlled field variants; unapproved labels",
                )
    supplement = root / "phase3/review-e2-supplement-001"
    a = read(supplement / "summary.json")
    for metric in ["pilot_retrievals", "sensitivity_retrievals"]:
        add(
            supplement.name,
            "mixed-and-sensitivity-controls",
            metric,
            a[metric],
            a[metric],
            "count",
            a["source"]["sha256"],
            "controlled development variants, not independent incident samples",
        )
    add(
        supplement.name,
        "actual-Ledger-controls",
        "primary_K_closed",
        sum(r["primary_K_closed"] for r in a["ledger_probes"]),
        len(a["ledger_probes"]),
        "count",
        a["source"]["sha256"],
        "three positive and two negative source/conflict controls; "
        "closure count is not aggregate quality",
    )
    e3 = root / "phase3/review-e3-full-001"
    a = read(e3 / "summary.json")
    for method, results in a["per_method"].items():
        for metric in [
            "solvable_closed",
            "all_closed",
            "false_closures",
            "correct_stops",
            "tool_calls",
            "model_calls",
            "budget_violations",
        ]:
            denom = (
                results["solvable"]
                if metric == "solvable_closed"
                else (results["unsolvable"] if metric == "correct_stops" else results["runs"])
            )
            add(
                e3.name,
                method,
                metric,
                results[metric],
                denom,
                "count",
                a["source"]["sha256"],
                "eight correlated fixture families; primary/all-task separately",
            )
    for name in [
        "review-e4-small-001",
        "review-e4-throughput-small-001",
        "review-e4-stress-001",
        "review-e4-full-throughput-001",
    ]:
        a = read(root / "phase3" / name / "summary.json")
        for group, value in a["groups"].items():
            for method, result in value["methods"].items():
                for metric in ["consistent", "total_seconds", "paired_total_full_over_method"]:
                    add(
                        name,
                        group + "/" + method,
                        metric,
                        result[metric],
                        result["batches"],
                        "seconds"
                        if metric == "total_seconds"
                        else "ratio"
                        if metric.endswith("method")
                        else "count",
                        a["source"]["sha256"],
                        "four-worker throughput only"
                        if a["workers"] == 4
                        else "shared-host latency",
                    )
    e5 = root / "phase3/review-e5-full-001"
    a = read(e5 / "summary.json")
    for layer, value in a["groups"].items():
        for metric in [
            "unsafe_acceptance_count",
            "legitimate_retention",
            "correct_human_review",
            "incorrect_rejections",
        ]:
            add(
                e5.name,
                layer,
                metric,
                value[metric],
                40,
                "count" if metric.endswith(("count", "rejections")) else "fraction",
                a["source"]["sha256"],
                "same-source synthetic candidate replicas",
            )
    e6 = root / "phase3/review-e6-full-001"
    a = read(e6 / "summary.json")

    # Include numeric leaves verbatim, retaining group and metric names from the raw summary.
    def leaves(value, path=()):
        if isinstance(value, dict):
            for key, v in value.items():
                yield from leaves(v, path + (key,))
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            yield path, value

    for path, value in leaves(a["groups"]):
        add(
            e6.name,
            "/".join(path[:-1]),
            path[-1],
            value,
            None,
            "saved-summary-value",
            read(e6 / "protocol.json")["source"]["sha256"],
            "20 related cases; five repeats; perturbations paired, draft labels",
        )
    e7 = root / "wp11/e7-diagnostic-full-002"
    a = read(e7 / "summary.json")
    for condition in sorted({r["condition"] for r in a["rows"]}):
        selected = [r for r in a["rows"] if r["condition"] == condition]
        verified = [r for r in selected if r["injection_verified"]]
        for metric in [
            "injection_verified",
            "recovered",
            "integration_pass",
            "top1_correct",
            "top3_correct",
        ]:
            eligible = verified if metric.startswith("top") else selected
            add(
                e7.name,
                condition,
                metric,
                sum(r.get(metric, False) for r in eligible),
                len(eligible),
                "count",
                read(e7 / "source_manifest.json")["sha256"],
                "five repeats per condition; related transport/process fault families",
            )
    e8 = root / "wp12/e8-opseval-pilot-002"
    a = read(e8 / "summary.json")
    for metric in ["correct", "failures", "actual_model_calls"]:
        add(
            e8.name,
            "naive-zero-shot",
            metric,
            a[metric],
            24,
            "count",
            read(e8 / "protocol.json")["dataset_sha256"],
            "external 5G MCQ; independent of UPF VPR",
        )
    output.mkdir(parents=True)
    with (output / "development-results.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (output / "development-results.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    )
    manifest = {
        "rows": len(rows),
        "formal_VPR": None,
        "expert_approvals_imported": 0,
        "input_scope": "new version matrices only; original 118-row table untouched",
        "csv_sha256": hashlib.sha256((output / "development-results.csv").read_bytes()).hexdigest(),
    }
    (output / "export-summary.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(export(a.root, a.output)))
