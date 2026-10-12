"""Export original per-sample evidence; never promote development labels to approved Gold."""

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class EvidenceTable:
    def __init__(self, project):
        self.project = project.resolve()
        self.artifacts = {}
        self.rows = defaultdict(list)
        self.identities = set()
        self.hash_cache = {}

    def file(self, path):
        path = path.resolve(strict=True)
        if not path.is_relative_to(self.project) or not path.is_file():
            raise ValueError("artifact must be a physical file inside the project")
        relative = str(path.relative_to(self.project))
        if relative not in self.hash_cache:
            self.hash_cache[relative] = sha(path)
        identity = hashlib.sha256(
            encoded([relative, self.hash_cache[relative]]).encode()
        ).hexdigest()
        self.artifacts[identity] = {"path": relative, "sha256": self.hash_cache[relative]}
        return identity

    def refs(self, **roles):
        return {role: [self.file(p) for p in paths] for role, paths in roles.items() if paths}

    def pins(self, root, filename):
        for relative, expected in read(root / filename).items():
            identity = self.file(root / relative)
            if self.artifacts[identity]["sha256"] != expected:
                raise ValueError(f"pinned input changed: {root.name}/{relative}")

    def add(self, experiment, batch, scope, unit, case, method, locator, metrics, refs, **extra):
        variant = {k: metrics.get(k) for k in ("condition", "replicate", "top_k", "alpha", "scope")}
        key = [experiment, batch, unit, case, method, variant]
        identity = hashlib.sha256(encoded(key).encode()).hexdigest()
        if identity in self.identities:
            raise ValueError(f"duplicate sample identity: {key}")
        self.identities.add(identity)
        row = {
            "row_id": identity,
            "experiment": experiment,
            "batch": batch,
            "scope": scope,
            "unit": unit,
            "case_id": case,
            "method": method,
            "record_locator": locator,
            "reviewed": False,
            "formal_vpr": None,
            "artifact_refs": refs,
            **extra,
            **metrics,
        }
        if row.get("formal_vpr") is not None or row.get("vpr") is not None:
            raise ValueError("this export covers development batches only")
        self.rows[experiment].append(row)

    def verify_sources(self):
        changed = [
            name
            for name, expected in self.hash_cache.items()
            if sha(self.project / name) != expected
        ]
        if changed:
            raise ValueError(f"source changed during export: {changed[:5]}")

    def write(self, output):
        output = output.resolve()
        if output.exists() or not output.is_relative_to(self.project / "runtime/v8-next"):
            raise ValueError("fresh v8-next export directory required")
        if any((self.project / name).is_relative_to(output) for name in self.hash_cache):
            raise ValueError("output overlaps original evidence")
        self.verify_sources()
        output.mkdir(parents=True)
        primary = ["row_id", "experiment", "batch", "scope", "unit", "case_id", "method"]
        all_rows = []
        counts = {}
        for experiment, rows in sorted(self.rows.items()):
            rows.sort(key=lambda r: (r["batch"], r["case_id"], r["method"], r["record_locator"]))
            all_rows.extend(rows)
            fields = primary + sorted(set().union(*(r.keys() for r in rows)) - set(primary))
            self.write_csv(output / f"{experiment}-samples.csv", rows, fields)
            counts[experiment] = dict(Counter(r["batch"] for r in rows))
        fields = primary + sorted(set().union(*(r.keys() for r in all_rows)) - set(primary))
        self.write_csv(output / "all-samples.csv", all_rows, fields)
        (output / "artifact-index.json").write_text(encoded(self.artifacts) + "\n")
        result = {
            "schema": "v8-original-per-sample-export-1",
            "sample_rows": len(all_rows),
            "counts_by_experiment_batch": counts,
            "artifact_files": len(self.artifacts),
            "original_source_hashes_verified": True,
            "new_model_calls": 0,
            "new_network_experiments": 0,
            "formal_vpr": None,
            "heldout_consumed": False,
            "mixed_units_must_not_be_summed_as_independent_cases": True,
            "organizer_only": True,
            "exporter_sha256": sha(Path(__file__)),
        }
        (output / "summary.json").write_text(encoded(result) + "\n")
        (output / "README.md").write_text(
            "# 逐样本证据表（组织者使用）\n\n"
            "每个 CSV 行保留原始运行或观测，不将开发标签变成人工批准。"
            "artifact_refs 中的 ID 在 artifact-index.json 中对应原文件路径及 SHA256。"
            "record_locator 定位原 JSON/JSONL/CSV 记录。scope、batch 和 unit 必须分别汇总，"
            "不能把 top-K、多次生成、门控层、批更新或历史失败计作独立案例。\n\n"
            "E1 为开发试点；E2 包含主矩阵与单列补充；E4 的原单 worker 与新四 worker"
            "版本不混算；E7 保留原模型失败前序和新规则结果，二者不作同协议模型比较。"
            "本表含候选开发标签和注入真值，不提供给第一遍盲审人员。正式 VPR 留空。\n"
        )
        self.verify_sources()
        manifest = {p.name: sha(p) for p in sorted(output.iterdir()) if p.is_file()}
        (output / "sha256_manifest.json").write_text(encoded(manifest) + "\n")
        return result

    @staticmethod
    def write_csv(path, rows, fields):
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(
                {k: encoded(v) if isinstance(v, (dict, list, bool)) else v for k, v in row.items()}
                for row in rows
            )


def available(root, *names):
    return [root / name for name in names if (root / name).is_file()]


def batch_refs(table, root):
    return table.refs(
        protocol=available(root, "protocol.json"),
        code=available(root, "source_manifest.json", "code-hashes.json", "common-head.json"),
        model=available(
            root, "actual-deployment.json", "deployment.json", "actual-model-deployment.json"
        ),
    )


def plan_rows(table, root, experiment):
    index = "metrics-by-case.jsonl" if experiment == "E1" else "run-index.jsonl"
    source_rows = [json.loads(line) for line in (root / index).read_text().splitlines()]
    table.pins(root, "sha256_manifest.json" if experiment == "E1" else "input-hashes.json")
    common = batch_refs(table, root)
    methods = read(root / "protocol.json")["methods"]
    for number, row in enumerate(source_rows, 1):
        if experiment == "E1":
            folder = root / "runs" / row["case_id"] / f"method-{methods.index(row['method']) + 1}"
            case = root / "cases" / row["case_id"]
        else:
            folder = root / row["output"]
            condition = "base" if row["condition"] == "repeat" else row["condition"]
            case = root / "cases" / row["case_id"] / condition
        raw = folder / "raw-plan.txt"
        receipt = read(folder / "raw-output.json")
        if receipt["content_sha256"] != sha(raw) or receipt["content"] != raw.read_text():
            raise ValueError("raw plan/receipt mismatch")
        if read(folder / "case-metrics.json") != row:
            raise ValueError("run index and individual result disagree")
        refs = {
            **common,
            **table.refs(
                input=[folder / "task.json", folder / "context.json", folder / "bindings.json"],
                raw=[raw, folder / "raw-output.json"],
                trace=[folder / "traces.jsonl", folder / "model-traces.jsonl"],
                reference=[case / "case-reference.json"],
                evaluation=[
                    folder / "validation.json",
                    folder / "case-metrics.json",
                    folder / "metrics.json",
                ],
            ),
        }
        metrics = read(folder / "metrics.json")
        table.add(
            experiment,
            root.name,
            "development-unreviewed",
            "plan_method_run",
            row["case_id"],
            row["method"],
            f"{index}:line-{number}",
            row,
            refs,
            model_attempts=metrics["invocations"]["model"]["attempted"],
            tool_attempts=metrics["invocations"]["tool"]["attempted"],
            input_tokens=metrics["token_usage"]["input"],
            output_tokens=metrics["token_usage"]["output"],
            source_group=read(case / "case-reference.json")["source_group"],
            structure_family=read(case / "case-reference.json")["structure_family"],
        )
    summary = read(root / "summary.json")
    if len(source_rows) != (summary["method_runs"] if experiment == "E1" else summary["completed"]):
        raise ValueError("plan run denominator mismatch")
    for method in methods:
        group = [r for r in source_rows if r["method"] == method]
        scores = summary["summaries"][method] if experiment == "E1" else None
        if scores and sum(r["reference_pass"] for r in group) != scores["reference_pass_count"]:
            raise ValueError("plan reference aggregate mismatch")


def e2_rows(table, root, supplement=False, primary=None):
    observations = read(root / "observations.json")
    if not supplement:
        table.pins(root, "input-hashes.json")
    common = batch_refs(table, root)
    for number, row in enumerate(observations):
        query = f"query-{row['query']:03}"
        qroot = (primary if supplement else root) / "queries" / query
        reference = qroot / "query-reference.json"
        if supplement:
            folder = root / ("sensitivity" if row["scope"] == "sensitivity" else "pilot") / query
            files = (
                list(folder.glob(f"alpha-{row['alpha']}.json"))
                if row["scope"] == "sensitivity"
                else list(folder.glob(f"{row['method']}.json"))
            )
            if not files:
                raise ValueError(f"missing supplemental retrieval: {folder}/{row['method']}")
        else:
            files = [root / "results" / query / f"{row['method']}.json"]
        table.add(
            "E2",
            root.name,
            row.get("scope", "development-unreviewed"),
            "query_method_top_k",
            query,
            row["method"],
            f"observations.json#/{number}",
            row,
            {
                **common,
                **table.refs(
                    input=[reference, qroot / "graph.json"],
                    reference=[reference],
                    trace=files,
                    evaluation=[root / "observations.json"],
                ),
            },
            structure_family=f"controlled-query-{row['kind']}",
        )
    if not supplement:
        summary = read(root / "summary.json")
        if len(observations) != summary["top_k_observations"]:
            raise ValueError("retrieval denominator mismatch")
        for method, cutoffs in summary["groups"].items():
            for k, aggregate in cutoffs.items():
                rows = [r for r in observations if r["method"] == method and r["top_k"] == int(k)]
                valid = [
                    r["development_recall"] for r in rows if r["development_recall"] is not None
                ]
                if len(rows) != aggregate["observations"] or not math.isclose(
                    sum(valid) / len(valid), aggregate["macro_recall"]
                ):
                    raise ValueError("retrieval macro recall mismatch")


def e3_rows(table, root):
    table.pins(root, "pre-evaluation-input-hashes.json")
    references = {r["case_id"]: r for r in read(root / "references.json")}
    results = []
    for path in sorted((root / "runs").glob("*/*/result.json")):
        row = read(path)
        results.append(row)
        folder = path.parent
        refs = {
            **batch_refs(table, root),
            **table.refs(
                input=[
                    folder / "task.json",
                    folder / "contract.json",
                    folder / "publication-catalog.json",
                ],
                reference=[root / "references.json"],
                evaluation=[path],
                trace=list(folder.glob("*trace*.json*"))
                + list(folder.glob("*dispatch*.json*"))
                + available(folder, "data/v8/ledger.sqlite3"),
            ),
        }
        table.add(
            "E3",
            root.name,
            "development-unreviewed",
            "supplement_method_run",
            row["case_id"],
            row["method"],
            str(path.relative_to(root)),
            row,
            refs,
            source_group=references[row["case_id"]]["source_family"],
            structure_family=references[row["case_id"]]["family"],
            solvable=references[row["case_id"]]["solvable"],
        )
    summary = read(root / "summary.json")
    if len(results) != summary["runs"]:
        raise ValueError("supplement denominator mismatch")
    for method, values in summary["per_method"].items():
        rows = [r for r in results if r["method"] == method]
        if (
            sum(r["all_closed"] for r in rows) != values["all_closed"]
            or sum(r["tool_calls"] for r in rows) != values["tool_calls"]
        ):
            raise ValueError("supplement aggregate mismatch")


def e4_rows(table, root):
    summary = read(root / "summary.json")
    common = batch_refs(table, root)
    total = 0
    for group, aggregate in sorted(summary["groups"].items()):
        path = root / group / "batches.csv"
        refs = {
            **common,
            **table.refs(
                input=available(root / group, "protocol.json"),
                evaluation=[path, root / "summary.json"],
            ),
        }
        with path.open() as stream:
            rows = list(csv.DictReader(stream))
        identities = {(r["seed"], r["batch"], r["method"]) for r in rows}
        if len(identities) != len(rows):
            raise ValueError("duplicate update batch")
        for number, row in enumerate(rows, 2):
            metrics = {k: v for k, v in row.items() if k not in {"batch", "method"}}
            metrics["consistent"] = row["consistent"] == "True"
            table.add(
                "E4",
                root.name,
                "historical-single-worker" if summary["workers"] == 1 else "four-worker-throughput",
                "update_method_batch",
                row["batch"],
                row["method"],
                f"{group}/batches.csv:line-{number}",
                metrics,
                refs,
                update_id=row["batch"],
                group=group,
                workers=summary["workers"],
                source_group=f"{group}/seed-{row['seed']}",
            )
        total += len(rows)
        for method, values in aggregate["methods"].items():
            subset = [r for r in rows if r["method"] == method]
            if (
                len(subset) != values["batches"]
                or sum(r["consistent"] == "True" for r in subset) != values["consistent"]
            ):
                raise ValueError("update consistency count mismatch")
    if total != summary["method_batches"]:
        raise ValueError("update denominator mismatch")


def e5_rows(table, root):
    table.pins(root, "input-hashes.json")
    candidates = {read(p / "reference.json")["case_id"]: p for p in (root / "cases").iterdir()}
    rows = read(root / "decisions.json")
    for number, row in enumerate(rows):
        folder = candidates[row["case_id"]]
        refs = {
            **batch_refs(table, root),
            **table.refs(
                input=[folder / "input.json"],
                reference=[folder / "reference.json"],
                raw=[folder / "candidate.txt"],
                trace=available(folder, f"{row['layer']}-trace.json"),
                evaluation=available(folder, f"{row['layer']}-validation.json")
                + [root / "decisions.json"],
            ),
        }
        table.add(
            "E5",
            root.name,
            "development-unreviewed",
            "candidate_gate_layer",
            row["case_id"],
            row["layer"],
            f"decisions.json#/{number}",
            row,
            refs,
            source_group=row["task_specification"],
            structure_family=row["fixture_lineage"],
        )
    if len(rows) != read(root / "summary.json")["decisions"]:
        raise ValueError("gate denominator mismatch")


def e7_rows(table, runtime):
    for root in sorted((runtime / "wp11").glob("e7-diagnostic-*")):
        if not (root / "summary.json").exists():
            continue
        summary = read(root / "summary.json")
        for number, row in enumerate(summary["rows"]):
            folder = root / "rounds" / f"round-{row['round']:03}"
            agent = folder / "agent"
            private = root / "private" / f"round-{row['round']:03}"
            refs = {
                **batch_refs(table, root),
                **table.refs(
                    input=available(folder, "input/snapshot.json"),
                    raw=available(agent, "raw-model-output.json"),
                    trace=available(agent, "model-traces.json", "model-metrics.json"),
                    evaluation=available(agent, "root-cause-report.json") + [root / "summary.json"],
                    reference=available(
                        private, "truth.json", "external-verification.json", "health-after.json"
                    ),
                ),
            }
            if root.name == "e7-diagnostic-full-002" and not all(
                refs.get(k) for k in ["input", "raw", "trace", "reference"]
            ):
                raise ValueError("final E7 original artifacts missing")
            scope = (
                "development-final-model"
                if root.name == "e7-diagnostic-full-002"
                else "development-model-history"
            )
            table.add(
                "E7-model",
                root.name,
                scope,
                "injected_diagnostic_round",
                f"round-{row['round']:03}",
                "limited-RootCause-model",
                f"summary.json#/rows/{number}",
                row,
                refs,
                source_group=row["condition"],
                structure_family=row["condition"],
            )
        if len(summary["rows"]) != summary["completed"]:
            raise ValueError("diagnostic denominator mismatch")
    remaining = runtime / "remaining-experiments-20261010"
    paths = [remaining / "e7-development-paired-replay-001"] + [
        remaining / name
        for name in [
            "e7-evidence-pilot-001",
            "e7-evidence-full-001",
            "e7-window-pilot-001",
            "e7-window-full-001",
        ]
    ]
    for root in paths:
        replay = "paired-replay" in root.name
        rows = (
            read(root / "rows-organizer-only.json")
            if replay
            else read(root / "summary.json")["rows"]
        )
        for number, row in enumerate(rows):
            folder = root / "rounds" / f"round-{row['round']:03}"
            original = (
                runtime / "wp11/e7-diagnostic-full-002/rounds" / folder.name if replay else folder
            )
            snapshot = original / "input/snapshot.json"
            if replay and sha(snapshot) != row["snapshot_sha256"]:
                raise ValueError("paired replay input changed")
            for mode, score in row["modes"].items():
                report = folder / (f"{mode}.json" if replay else f"agent/{mode}.json")
                scope = (
                    "known-development-replay"
                    if replay
                    else "posthoc-window-sensitivity"
                    if "window" in root.name
                    else "fresh-controlled-observations"
                )
                refs = {
                    **batch_refs(table, root),
                    **table.refs(
                        input=[snapshot],
                        raw=[report],
                        trace=[report],
                        evaluation=[
                            root / ("rows-organizer-only.json" if replay else "summary.json")
                        ],
                        reference=available(
                            (runtime / "wp11/e7-diagnostic-full-002" if replay else root)
                            / "private"
                            / folder.name,
                            "truth.json",
                            "external-verification.json",
                            "health-after.json",
                        ),
                    ),
                }
                report_body = read(report)
                location = "rows-organizer-only.json" if replay else "summary.json#/rows"
                table.add(
                    "E7-rules",
                    root.name,
                    scope,
                    "injected_round_method",
                    folder.name,
                    mode,
                    f"{location}#/{number}/{mode}",
                    {
                        **score,
                        "condition": row["condition"],
                        "healthy": row["condition"] == "healthy",
                        "diagnosis_seconds": report_body["diagnosis_seconds"],
                        "model_attempts": 0,
                    },
                    refs,
                    source_group=row["condition"],
                    structure_family=row["condition"],
                )


def export(project, output):
    table = EvidenceTable(project)
    runtime = project / "runtime/v8-next"
    plan_rows(table, runtime / "phase2/review-closure-full-001", "E1")
    primary = runtime / "phase3/review-e2-full-001"
    e2_rows(table, primary)
    e2_rows(table, runtime / "phase3/review-e2-supplement-001", True, primary)
    e3_rows(table, runtime / "phase3/review-e3-full-001")
    for name in [
        "e4-full-single-001",
        "review-e4-small-001",
        "review-e4-throughput-small-001",
        "review-e4-stress-001",
        "review-e4-full-throughput-001",
    ]:
        e4_rows(table, runtime / "phase3" / name)
    e5_rows(table, runtime / "phase3/review-e5-full-001")
    plan_rows(table, runtime / "phase3/review-e6-full-001", "E6")
    e7_rows(table, runtime)
    return table.write(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(export(args.project.resolve(), args.output), ensure_ascii=False))
