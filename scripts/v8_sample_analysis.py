"""Paired development comparisons with explicit source/family clustering and no formal claims."""

import argparse
import csv
import json
import random
from collections import defaultdict
from pathlib import Path

from v8_sample_export import encoded, read, sha


def boolean(value):
    result = json.loads(value) if isinstance(value, str) else value
    if not isinstance(result, bool):
        raise ValueError("binary metric must be an explicit boolean")
    return result


def identity(row):
    return tuple(row.get(k, "") for k in ["case_id", "condition", "replicate", "top_k", "alpha"])


def percentile(values, fraction):
    position = (len(values) - 1) * fraction
    left = int(position)
    right = min(left + 1, len(values) - 1)
    return values[left] + (values[right] - values[left]) * (position - left)


def table_rows(path):
    # Evidence references can exceed Python's default 128 KiB CSV field limit.
    csv.field_size_limit(max(csv.field_size_limit(), path.stat().st_size))
    with path.open(encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def paired(rows, baseline, treatment, metric, continuous=False):
    index = {method: {} for method in [baseline, treatment]}
    for row in rows:
        method = row["method"]
        if method not in index:
            continue
        key = identity(row)
        if key in index[method]:
            raise ValueError("duplicate paired observation")
        index[method][key] = row
    if not index[baseline] or set(index[baseline]) != set(index[treatment]):
        raise ValueError("paired methods must cover exactly the same observations")
    keys = sorted(index[baseline])
    parent = list(range(len(keys)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    labels = {}
    values = []
    for i, key in enumerate(keys):
        a, b = index[baseline][key], index[treatment][key]
        for field in ["source_group", "structure_family"]:
            if a.get(field) != b.get(field):
                raise ValueError("paired methods disagree on source/family")
            if a.get(field):
                label = (field, a[field])
                if label in labels:
                    parent[find(i)] = find(labels[label])
                labels[label] = i
        x, y = (
            (float(a[metric]), float(b[metric]))
            if continuous
            else (boolean(a[metric]), boolean(b[metric]))
        )
        values.append((float(x), float(y)))
    clusters = defaultdict(list)
    for i, value in enumerate(values):
        clusters[find(i)].append(value)
    groups = list(clusters.values())
    ci = None
    if len(groups) >= 2:
        rng = random.Random(20261010)
        deltas = []
        for _ in range(2000):
            sample = [v for _ in groups for v in groups[rng.randrange(len(groups))]]
            deltas.append(sum(y - x for x, y in sample) / len(sample))
        deltas.sort()
        ci = [percentile(deltas, 0.025), percentile(deltas, 0.975)]
    return {
        "baseline": baseline,
        "treatment": treatment,
        "metric": metric,
        "paired_observations": len(values),
        "source_structure_components": len(groups),
        "baseline_mean": sum(x for x, _ in values) / len(values),
        "treatment_mean": sum(y for _, y in values) / len(values),
        "mean_difference": sum(y - x for x, y in values) / len(values),
        "improved_pairs": sum(y > x for x, y in values),
        "regressed_pairs": sum(y < x for x, y in values),
        "unchanged_pairs": sum(y == x for x, y in values),
        "cluster_bootstrap95_exploratory": ci,
        "interval_reason": "too few disjoint source/structure components"
        if ci is None
        else "descriptive cluster resampling of controlled development inputs",
        "formal_inference": False,
        "approved_gold": False,
        "population_superiority_claim": False,
    }


def paired_costs(rows, baseline, treatment):
    selected = [r for r in rows if r["method"] in {baseline, treatment}]
    costs = []
    for metric in [
        "tool_attempts",
        "model_attempts",
        "input_tokens",
        "output_tokens",
        "tool_calls",
        "model_calls",
        "elapsed_seconds",
        "diagnosis_seconds",
    ]:
        present = sum(r.get(metric) not in {None, ""} for r in selected)
        if not present:
            continue
        if present != len(selected):
            raise ValueError("partial cost coverage cannot silently drop failed observations")
        result = paired(selected, baseline, treatment, metric, continuous=True)
        costs.append(
            {
                "metric": metric,
                "paired_observations": result["paired_observations"],
                "baseline_total": result["baseline_mean"] * result["paired_observations"],
                "treatment_total": result["treatment_mean"] * result["paired_observations"],
                "baseline_mean": result["baseline_mean"],
                "treatment_mean": result["treatment_mean"],
                "mean_cost_difference": result["mean_difference"],
                "cost_increased": result["mean_difference"] > 0,
                "formal_cost_inference": False,
            }
        )
    return costs


def analyze(tables, output):
    if output.exists() or output.resolve().is_relative_to(tables.resolve()):
        raise ValueError("fresh analysis directory outside the frozen tables required")
    manifest = read(tables / "sha256_manifest.json")
    if any(sha(tables / name) != expected for name, expected in manifest.items()):
        raise ValueError("sample table manifest mismatch")

    def rows(experiment):
        return table_rows(tables / f"{experiment}-samples.csv")

    comparisons, quality_costs = [], []

    def add(experiment, selected, baseline, treatment, metric, scope, continuous=False):
        result = paired(selected, baseline, treatment, metric, continuous)
        result.update(experiment=experiment, scope=scope)
        comparisons.append(result)
        for cost in paired_costs(selected, baseline, treatment):
            quality_costs.append(
                {
                    "experiment": experiment,
                    "scope": scope,
                    "baseline": baseline,
                    "treatment": treatment,
                    "quality_metric": metric,
                    "quality_difference": result["mean_difference"],
                    **cost,
                }
            )

    common = "+CommonPlanHead"
    add(
        "E1",
        rows("E1"),
        "P5" + common,
        "v8-full" + common,
        "reference_pass",
        "unapproved-development-reference",
    )
    add(
        "E1",
        rows("E1"),
        "v8-no-graph" + common,
        "v8-full" + common,
        "reference_pass",
        "graph-ablation",
    )
    e2 = [
        r
        for r in rows("E2")
        if r["batch"] == "review-e2-full-001" and r["top_k"] == "20" and r["development_recall"]
    ]
    add(
        "E2",
        e2,
        "G0-P3",
        "G2-contract-BFS",
        "development_recall",
        "57 relevant-query controls; 39 no-evidence queries reported separately",
        True,
    )
    add(
        "E2",
        e2,
        "G2-contract-BFS",
        "G3-PPR",
        "development_recall",
        "same-budget ranking ablation",
        True,
    )
    e3 = [r for r in rows("E3") if boolean(r["solvable"])]
    add("E3", e3, "T2-native-P5", "T3-typed", "primary_closed", "12 predeclared solvable targets")
    add("E3", rows("E3"), "T2-native-P5", "T3-typed", "all_closed", "32 whole tasks")
    e5 = rows("E5")
    add("E5", e5, "A0", "A4", "correct", "same 120 development-labelled candidates")
    e6 = rows("E6")
    for condition in ["repeat", "perturbed"]:
        selected = [r for r in e6 if (r["condition"] == "repeat") == (condition == "repeat")]
        add("E6", selected, "P5" + common, "v8-full" + common, "reference_pass", condition)
        add(
            "E6",
            selected,
            "v8-no-graph" + common,
            "v8-full" + common,
            "reference_pass",
            condition + "/graph-ablation",
        )
    e7 = [
        r
        for r in rows("E7-rules")
        if r["batch"] == "e7-evidence-full-001" and not boolean(r["healthy"])
    ]
    add("E7", e7, "flat", "joined", "top1_correct", "fresh same-lab controlled fault families")
    add("E7", e7, "joined", "graph", "top1_correct", "same joint rules; graph ablation")
    costs = []
    by_group = defaultdict(lambda: defaultdict(float))
    for row in rows("E4"):
        by_group[(row["batch"], row["group"], row["workers"])][row["method"]] += float(
            row["seconds"]
        )
    for (batch, group, workers), methods in sorted(by_group.items()):
        for method, seconds in methods.items():
            ratio = methods["L0-Full"] / seconds
            costs.append(
                {
                    "batch": batch,
                    "group": group,
                    "workers": workers,
                    "method": method,
                    "seconds": seconds,
                    "paired_full_over_method": ratio,
                    "negative_benefit": ratio < 1,
                    "scope": "shared-host update timing; four workers are throughput only",
                }
            )
    output.mkdir(parents=True)
    (output / "paired-comparisons.json").write_text(encoded(comparisons) + "\n")
    for name, values in [
        ("paired-comparisons.csv", comparisons),
        ("quality-cost.csv", quality_costs),
        ("E4-costs.csv", costs),
    ]:
        with (output / name).open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(values[0]))
            writer.writeheader()
            writer.writerows(
                {k: encoded(v) if isinstance(v, (list, bool)) else v for k, v in r.items()}
                for r in values
            )
    summary = {
        "comparisons": len(comparisons),
        "paired_quality_cost_rows": len(quality_costs),
        "cost_groups": len(costs),
        "formal_statistics_completed": False,
        "formal_vpr": None,
        "heldout_consumed": False,
        "source_table_manifest_sha256": sha(tables / "sha256_manifest.json"),
        "note": (
            "paired descriptive development results; no new independent Gold or population test"
        ),
    }
    (output / "summary.json").write_text(encoded(summary) + "\n")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tables", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(analyze(args.tables, args.output), ensure_ascii=False))
