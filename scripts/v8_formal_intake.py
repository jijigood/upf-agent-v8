"""Prepare version-bound formal E1 intake; missing human facts remain missing."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from v8_formal_readiness import assess
from v8_sample_export import encoded, read, sha

from upf_agent.v8.models import digest
from upf_agent.v8.phase2 import METHODS
from upf_agent.v8.plan_ir import CaseGold
from upf_agent.v8.plan_review import GoldReview, apply_reviews, calibration_report


def intake(project, cases, output, reviews_file=None, review_root=None):
    project, cases, output = project.resolve(), cases.resolve(), output.resolve()
    if output.exists() or not output.is_relative_to(project / "runtime/v8-next"):
        raise ValueError("new formal intake directory required")
    paths = sorted(cases.glob("*/case-reference.json"))
    golds = {p.parent.name: CaseGold.model_validate_json(p.read_text()) for p in paths}
    by_id = {g.case_id: g for g in golds.values()}
    if not paths or len(by_id) != len(paths):
        raise ValueError("nonempty references with unique case IDs required")
    records = (
        [] if reviews_file is None else [GoldReview.model_validate(r) for r in read(reviews_file)]
    )
    keys = [(r.case_id, r.reviewer.strip().casefold()) for r in records]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate case/reviewer identity")
    root = (review_root or project).resolve()
    source_receipts = {}
    invalid_sources = []
    for record in records:
        if record.case_id not in by_id or digest(by_id[record.case_id]) != record.reference_sha256:
            raise ValueError("review hash/case does not match supplied reference")
        source = Path(record.review_source)
        source = (source if source.is_absolute() else root / source).resolve()
        if not source.is_relative_to(root) or not source.is_file():
            invalid_sources.append(
                {
                    "case_id": record.case_id,
                    "reviewer": record.reviewer,
                    "reason": "review_source is not a physical file inside review_root",
                }
            )
        else:
            source_receipts[record.review_source] = {"path": str(source), "sha256": sha(source)}
    source_files = {str(p.relative_to(cases)): sha(p) for p in paths}
    status = assess(cases, [] if invalid_sources else records)
    status.pop("inventory")
    status.update(
        actual_review_records=len(records),
        review_source_receipts=source_receipts,
        invalid_review_sources=invalid_sources,
        review_authenticity=(
            "physical receipts and distinct supplied identities checked; "
            "humans establish expertise and independence"
        ),
        approval_is_not_inferred_from_AI_or_old_version=True,
        formal_protocol_frozen=False,
        formal_execution_allowed=False,
    )
    inventory = []
    empty = []
    approved = {}
    for path in paths:
        gold = golds[path.parent.name]
        pair = [r for r in records if r.case_id == gold.case_id]
        bound = False
        if not invalid_sources:
            try:
                approved[gold.case_id] = apply_reviews(gold, pair)
                bound = True
            except ValueError:
                pass
        inventory.append(
            {
                "case_id": gold.case_id,
                "reference_path": str(path.relative_to(project))
                if path.is_relative_to(project)
                else str(path),
                "reference_file_sha256": sha(path),
                "reference_canonical_digest": digest(gold),
                "source_group": gold.source_group,
                "structure_family": gold.structure_family,
                "source_level": gold.source_level,
                "split": gold.split,
                "hash_bound_double_approval": bound,
                "actual_review_records": len(pair),
            }
        )
        for seat in [1, 2]:
            empty.append(
                {
                    "seat": seat,
                    "case_id": gold.case_id,
                    "reference_sha256": digest(gold),
                    "reference_file_sha256": sha(path),
                    "reviewer": "",
                    "decision": "",
                    "review_version": "",
                    "review_source": "",
                    "notes": "",
                }
            )
    draft = {
        "schema": "formal-e1-intake-protocol-1",
        "status": "draft-awaiting-data-and-review",
        "methods": METHODS,
        "primary_comparison": [METHODS[1], METHODS[3]],
        "secondary_comparisons": [[METHODS[2], METHODS[3]], [METHODS[0], METHODS[3]]],
        "common_budget": {"tools": 8, "models": 8, "rounds": 3, "seconds": 180},
        "scale_options": {
            "60": {"dev": 24, "validation": 12, "heldout": 24},
            "150": {"dev": 60, "validation": 30, "heldout": 60},
        },
        "scale_chosen": None,
        "required_before_freeze": [
            "independent grouped case inventory",
            "hash-bound real double reviews",
            "validation revisions completed",
            "approved protocol and model deployment",
            "code/prompt/registry/evaluator and heldout hashes",
        ],
        "formal_vpr": None,
        "heldout_consumed": False,
    }
    output.mkdir(parents=True)
    for name, value in [
        ("status.json", status),
        ("protocol-draft.json", draft),
        ("received-reviews.json", [r.model_dump(mode="json") for r in records]),
        ("calibration.json", calibration_report(records)),
        ("source-hashes.json", source_files),
    ]:
        (output / name).write_text(encoded(value) + "\n")
    for name, rows in [("reference-inventory.csv", inventory), ("empty-double-review.csv", empty)]:
        with (output / name).open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    (output / "approved-references").mkdir()
    for case_id, gold in approved.items():
        (output / "approved-references" / f"{digest(case_id)[:20]}.json").write_text(
            gold.model_dump_json() + "\n"
        )
    (output / "case-gold.schema.json").write_text(encoded(CaseGold.model_json_schema()) + "\n")
    (output / "gold-review.schema.json").write_text(encoded(GoldReview.model_json_schema()) + "\n")
    (output / "README.md").write_text(
        "# 正式 E1 接收入口\n\n"
        "该包接收实际材料，不产生专家批准。reference_sha256 使用 reference_canonical_digest，"
        "不是 reference_file_sha256。填写两个真实独立评审及实际 review_source 文件，"
        "以 GoldReview JSON 数组重新运行 --reviews；有分歧保留双方意见、修订参考后重新双评。\n\n"
        "空表不能导入为审核。已收到的旧单人意见保留，新 hash 不继承旧批准。"
        "status.json 的 data_ready 只判断数据条件；它不完成正式协议、模型冻结、"
        "validation 修订或新 heldout 消费。当前 formal_execution_allowed 始终为 false。\n"
    )
    if any(sha(cases / relative) != expected for relative, expected in source_files.items()):
        raise ValueError("reference changed during intake")
    (output / "sha256_manifest.json").write_text(
        encoded(
            {str(p.relative_to(output)): sha(p) for p in sorted(output.rglob("*")) if p.is_file()}
        )
        + "\n"
    )
    return {
        k: v
        for k, v in status.items()
        if k not in {"connected_components", "review_source_receipts"}
    }


def candidate_inventory(project, output):
    if output.exists():
        raise ValueError("new candidate inventory file required")
    rows = []
    for relative in [
        "eval/p6/business_v4/reviewed_suite.jsonl",
        "eval/p6/business_v5_replacement/candidate_suite.jsonl",
    ]:
        path = project / relative
        if not path.exists():
            continue
        manifest = read(path.parent / "manifest.json")
        # Export provenance metadata; keep questions, answers and label content out.
        for number, line in enumerate(path.read_text().splitlines(), 1):
            row = json.loads(line)
            new = "replacement" in relative and row["split"] == "heldout"
            rows.append(
                {
                    "suite": relative,
                    "suite_sha256": sha(path),
                    "line": number,
                    "case_id": row["id"],
                    "category": row["category"],
                    "split_in_original_suite": row["split"],
                    "source_groups": encoded(row["source_groups"]),
                    "label_status_in_original_suite": row["label_status"],
                    "new_unexecuted_candidate": new
                    and manifest.get("new_heldout_executed") is False,
                    "E1_PlanIR_Gold_available": False,
                    "E1_double_approval_available": False,
                    "required_work": (
                        "physical task/evidence/PlanIR Gold transfer and real independent review; "
                        "do not relabel old heldout"
                    ),
                }
            )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return {
        "candidate_rows": len(rows),
        "counts_by_suite": dict(Counter(r["suite"] for r in rows)),
        "new_unexecuted_P6_candidates": sum(r["new_unexecuted_candidate"] for r in rows),
        "E1_approved_gold": 0,
        "heldout_evaluated_by_this_inventory": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reviews", type=Path)
    parser.add_argument("--review-root", type=Path)
    args = parser.parse_args()
    print(
        json.dumps(
            intake(args.project, args.cases, args.output, args.reviews, args.review_root),
            ensure_ascii=False,
        )
    )
