"""Export scoped development result tables from a successful WP10 synthetic replay."""

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def export(bundle, replay, output):
    bundle, replay, output = bundle.resolve(), replay.resolve(), output.resolve()
    if output.exists() or output.is_relative_to(replay) or output.is_relative_to(bundle / "data"):
        raise ValueError("choose a new independent table directory")
    report = read(replay / "summary.json")
    if not report["pass"] or report["kind"] != "synthetic" or report["formal_acceptance"]:
        raise ValueError("successful unreviewed synthetic replay required")
    rows = []

    def row(experiment, method, metric, numerator, denominator, **extra):
        rows.append(
            {
                "experiment": experiment,
                "method": method,
                "metric": metric,
                "numerator": numerator,
                "denominator": denominator,
                "value": numerator / denominator if denominator else "",
                "group": "",
                "paired_full_over_method": "",
                "historical_model_calls": "",
                "dataset_grade": "synthetic_dev_unreviewed",
                "formal_vpr": "",
                **extra,
            }
        )

    results = report["results"]
    for method, scores in results["phase2_revision"]["per_method"].items():
        for key in ["validator_pass_count", "reference_pass_count"]:
            row("phase2-revised-reference", method, key, scores[key], scores["runs"])
        old = results["phase2"]["per_method"][method]["new"]
        row(
            "phase2-original-reference",
            method,
            "reference_pass_count",
            old["reference_pass_count"],
            old["runs"],
        )
    e3 = read(bundle / "data/phase3/e3-public-four-methods-002/summary.json")
    for method, scores in e3["per_method"].items():
        for metric, numerator, denominator in [
            ("primary_closed_solvable", scores["solvable_closed"], scores["solvable"]),
            ("all_task_closed", scores["all_closed"], scores["runs"]),
            ("correct_stop_unsolvable", scores["correct_stops"], scores["unsolvable"]),
        ]:
            row(
                "E3",
                method,
                metric,
                numerator,
                denominator,
                historical_model_calls=scores["model_calls"],
            )
    for group, methods in results["E4"]["groups"].items():
        for method, scores in methods.items():
            row(
                "E4",
                method,
                "consistent_method_batches",
                scores["consistent"],
                scores["batches"],
                group=group,
                paired_full_over_method=scores["paired_total_full_over_method"],
            )
    counts = results["E5"]["counts"]
    for layer in range(5):
        method = f"A{layer}"
        for category, outcome in [
            ("allowed", "suggest_allowed"),
            ("forbidden", "blocked"),
            ("unknown", "human_review"),
        ]:
            row(
                "E5",
                method,
                f"{category}_{outcome}",
                counts.get(f"{method}:{category}:{outcome}", 0),
                40,
            )
    reject_all = read(bundle / "data/phase3/e5-full-002/summary.json")["groups"]["reject-all"]
    for category, outcome in [
        ("allowed", "suggest_allowed"),
        ("forbidden", "blocked"),
        ("unknown", "human_review"),
    ]:
        row(
            "E5",
            "reject-all",
            f"{category}_{outcome}",
            reject_all["outcome_counts"][category].get(outcome, 0),
            40,
        )
    for method, scores in results["E6"]["groups"].items():
        for group in ["repeated", "perturbed"]:
            value = scores[group]
            row(
                "E6",
                method,
                "reference_pass_count",
                value["reference_pass_count"],
                value["runs"],
                group=group,
            )
        row(
            "E6",
            method,
            "all_five_pass_cases",
            scores["development_all_five_pass_cases"],
            scores["all_five_denominator"],
        )
        row(
            "E6",
            method,
            "reference_decision_flips",
            sum(x["reference_decision_flip"] for x in scores["decision_flips"]),
            len(scores["decision_flips"]),
        )
    output.mkdir(parents=True)
    path = output / "software-results.csv"
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    shutil.copyfile(Path(__file__), output / "generate.py")
    (output / "README.md").write_text("""# 软件结果表（开发数据，待人工复核）

此表由通过的合成包离线复算生成。真实手册 E2 不在本结果包内。
formal_vpr 空白表示未获得独立参考批准，不能写作专家 VPR。
phase2-revised-reference 是输出后修订参考的开发复算，不能解释为模型改进。
E3 主目标分母为 12，全任务分母为 32，不得交换；历史模型次数在三个指标行重复，
不可跨指标相加。E4 比率为原始分组总耗时 Full/方法，低于 1 的行均保留；
共享主机观测不支持专属硬件或因果性能优势声明。
E6 重复和扰动来源相关，未完成扰动语义独立审查，不增加独立案例数。

再生成（Python 标准库，无新模型调用）：

```bash
python generate.py --bundle /path/to/synthetic-bundle --replay /path/to/passed/replay \\
  --output /path/to/new-table-directory
```
""")
    manifest = {
        "schema": "wp10-software-tables-1",
        "rows": len(rows),
        "synthetic": True,
        "reviewed": False,
        "formal_vpr": None,
        "heldout_consumed": False,
        "input_bundle_manifest_sha256": hashlib.sha256(
            (bundle / "bundle-manifest.json").read_bytes()
        ).hexdigest(),
        "input_replay_sha256": hashlib.sha256((replay / "summary.json").read_bytes()).hexdigest(),
        "files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir()},
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(export(args.bundle, args.replay, args.output))
