"""Finalize reference-matched E1 results only with real, raw-hash-bound semantic reviews."""

import csv
import json
from pathlib import Path
from typing import Literal

from pydantic import Field

from upf_agent.v8.e1_dataset import load_dataset, read, sha, write
from upf_agent.v8.e1_formal import paired_statistics
from upf_agent.v8.models import Model, canonical, digest
from upf_agent.v8.phase2 import METHODS
from upf_agent.v8.plan_metrics import summarize_cases


class OutputReview(Model):
    case_id: str
    method: str
    raw_plan_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    reference_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    reviewer: str = Field(min_length=1)
    role: Literal["reviewer", "adjudicator"] = "reviewer"
    semantic_valid: bool
    review_version: str = Field(min_length=1)
    review_source: str = Field(min_length=1)
    notes: list[str] = Field(min_length=1)


def finalize(frozen_root, run_root, reviews_file, review_root, output):
    frozen_root, run_root, review_root, output = (
        p.resolve() for p in [frozen_root, run_root, review_root, output]
    )
    if output.exists() or output.is_relative_to(run_root) or output.is_relative_to(frozen_root):
        raise ValueError("new finalization output outside original run/freeze required")
    for root in [frozen_root, run_root]:
        for name, expected in read(root / "sha256_manifest.json").items():
            if sha(root / name) != expected:
                raise ValueError("original frozen/run artifact changed")
    frozen = read(frozen_root / "freeze.json")
    run_summary = read(run_root / "summary.json")
    if read(run_root / "freeze.json") != frozen or not run_summary["source_unchanged"]:
        raise ValueError("run and frozen protocol mismatch")
    dataset = load_dataset(frozen_root / "dataset")
    cases = {c["manifest"].case_id: c for c in dataset["cases"]}
    rows = [
        json.loads(line) for line in (run_root / "metrics-by-case.jsonl").read_text().splitlines()
    ]
    identities = {(row["case_id"], row["method"]) for row in rows}
    expected = {(case_id, method) for case_id in frozen["selected_cases"] for method in METHODS}
    if len(identities) != len(rows) or identities != expected:
        raise ValueError("complete planned case/method denominator required")
    records = [OutputReview.model_validate(row) for row in read(reviews_file)]
    keys = [(r.case_id, r.method, r.reviewer.strip().casefold()) for r in records]
    if len(keys) != len(set(keys)) or any(not k[2] for k in keys):
        raise ValueError("duplicate/blank output reviewer identity")
    receipts, by_pair = {}, {}
    for record in records:
        key = (record.case_id, record.method)
        if key not in expected:
            raise ValueError("output review refers to a run outside this frozen stage")
        raw = (
            run_root
            / "runs"
            / record.case_id
            / f"method-{METHODS.index(record.method) + 1}"
            / "raw-plan.txt"
        )
        if (
            not raw.is_file()
            or sha(raw) != record.raw_plan_sha256
            or digest(cases[record.case_id]["gold"]) != record.reference_sha256
        ):
            raise ValueError("output review/raw plan/reference hash mismatch")
        source = (review_root / record.review_source).resolve(strict=True)
        if (
            Path(record.review_source).is_absolute()
            or not source.is_relative_to(review_root)
            or not source.is_file()
        ):
            raise ValueError("output review_source must be physical and inside review_root")
        receipts[record.review_source] = sha(source)
        by_pair.setdefault(key, []).append(record)
    for row in rows:
        row["reference_based_vpr"] = row["vpr"]
        if not row["parsed"]:
            row["semantic_review_status"] = "unscorable machine failure retained"
            row["vpr"] = False if row["solvability"] == "solvable" else None
            continue
        reviews = by_pair.get((row["case_id"], row["method"]), [])
        pair = [r for r in reviews if r.role == "reviewer"]
        adjudication = [r for r in reviews if r.role == "adjudicator"]
        if len(pair) != 2:
            raise ValueError("every parsed raw plan needs two actual semantic review records")
        if pair[0].semantic_valid == pair[1].semantic_valid:
            if adjudication:
                raise ValueError("unneeded adjudication must not override agreeing reviews")
            semantic_valid = pair[0].semantic_valid
            row["semantic_review_status"] = "two matching supplied semantic decisions"
        else:
            if len(adjudication) != 1:
                raise ValueError(
                    "semantic disagreement requires actual third-reviewer adjudication"
                )
            semantic_valid = adjudication[0].semantic_valid
            row["semantic_review_status"] = "supplied adjudication of original disagreement"
        row["semantic_valid"] = semantic_valid
        row["vpr"] = (
            bool(row["reference_based_vpr"] and semantic_valid)
            if row["solvability"] == "solvable"
            else None
        )
    statistics = paired_statistics(dataset, rows, frozen)
    summaries = {m: summarize_cases([r for r in rows if r["method"] == m]) for m in METHODS}
    for value in summaries.values():
        value.pop("vpr_wilson95")
    output.mkdir(parents=True)
    write(output / "freeze.json", frozen)
    write(output / "received-output-reviews.json", [r.model_dump(mode="json") for r in records])
    write(output / "review-source-receipts.json", receipts)
    write(output / "paired-statistics.json", statistics)
    with (output / "formal-results.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        fields = sorted(set().union(*(r.keys() for r in rows)))
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(
            {k: canonical(v) if isinstance(v, (dict, list, bool)) else v for k, v in row.items()}
            for row in rows
        )
    summary = {
        "stage": frozen["stage"],
        "recorded_method_runs": len(rows),
        "source_unchanged": run_summary["source_unchanged"],
        "execution_pass": run_summary["execution_pass"],
        "natural_language_output_review_completed": True,
        "actual_output_review_records": len(records),
        "summaries": summaries,
        "formal_vpr": {method: value["vpr"] for method, value in summaries.items()},
        "formal_e1_completed": frozen["stage"] == "heldout",
        "formal_statistics_completed": frozen["stage"] == "heldout"
        and all(r["cluster_bootstrap95"] is not None for r in statistics),
        "heldout_consumed": frozen["stage"] == "heldout",
        "superiority_claim": False,
        "review_authenticity": (
            "supplied physical records checked; actual expertise/independence is a human fact"
        ),
        "original_run_manifest_sha256": sha(run_root / "sha256_manifest.json"),
        "new_model_calls": 0,
    }
    write(output / "summary.json", summary)
    write(
        output / "sha256_manifest.json", {p.name: sha(p) for p in output.iterdir() if p.is_file()}
    )
    return summary
