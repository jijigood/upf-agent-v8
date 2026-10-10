"""Read-only formal E1 readiness audit; never relabel development or consume heldout."""

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from upf_agent.v8.plan_ir import CaseGold
from upf_agent.v8.plan_review import GoldReview, apply_reviews, validate_splits


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assess(case_root, review_records=(), minimum_cases=60):
    files = sorted(case_root.glob("*/case-reference.json"))
    golds = [(p, CaseGold.model_validate_json(p.read_text())) for p in files]
    problems, inventory = [], []
    reviews_by_case = defaultdict(list)
    for record in review_records:
        reviews_by_case[record.case_id].append(record)
    if len({g.case_id for _, g in golds}) != len(golds):
        problems.append("duplicate_case_identity")
    # Union both source and structure identities; neither may cross the split.
    parent = list(range(len(golds)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    groups = {}
    approved = 0
    for i, (path, gold) in enumerate(golds):
        for field in ("source_group", "structure_family"):
            key = (field, getattr(gold, field))
            if key in groups:
                parent[find(i)] = find(groups[key])
            groups[key] = i
        source_checks = {}
        for relative, expected in gold.source_hashes.items():
            candidate = (path.parent / relative).resolve()
            valid_path = candidate.is_relative_to(path.parent.resolve())
            ok = valid_path and candidate.is_file() and sha(candidate) == expected
            source_checks[relative] = ok
            if not ok:
                problems.append(f"source_integrity:{gold.case_id}:{relative}")
        rs = reviews_by_case[gold.case_id]
        bound_approval = False
        if not gold.reviewed:
            try:
                apply_reviews(gold, rs)
                bound_approval = True
            except ValueError:
                pass
        # reviewed:true metadata alone is not a verifiable original review receipt.
        approved += int(bound_approval)
        inventory.append(
            {
                "case_id": gold.case_id,
                "reference_path": str(path),
                "reference_sha256": sha(path),
                "source_group": gold.source_group,
                "structure_family": gold.structure_family,
                "source_level": gold.source_level,
                "split": gold.split,
                "synthetic": gold.synthetic,
                "reviewed_metadata": gold.reviewed,
                "hash_bound_double_approval": bound_approval,
                "review_record_count": len(rs),
                "source_integrity": source_checks,
            }
        )
    components = defaultdict(list)
    for i, (_, g) in enumerate(golds):
        components[find(i)].append(g.case_id)
    if len(golds) < minimum_cases:
        problems.append("insufficient_independent_case_inventory")
    if len(components) < 3:
        problems.append("fewer_than_three_disjoint_source_structure_components")
    if approved != len(golds) or not golds:
        problems.append("missing_hash_bound_independent_gold_double_approval")
    splits = Counter(g.split for _, g in golds)
    if any(not splits[name] for name in ("dev", "validation", "heldout")):
        problems.append("missing_formal_split")
    try:
        validate_splits([g for _, g in golds])
    except ValueError as exc:
        problems.append(str(exc))
    return {
        "case_count": len(golds),
        "minimum_scale_candidate": minimum_cases,
        "source_groups": len({g.source_group for _, g in golds}),
        "structure_families": len({g.structure_family for _, g in golds}),
        "connected_components": list(components.values()),
        "split_counts": dict(splits),
        "hash_bound_approved_gold": approved,
        "problems": sorted(set(problems)),
        "data_ready": not problems,
        "formal_experiment_completed": False,
        "heldout_consumed": False,
        "new_model_calls": 0,
        "formal_vpr": None,
        "inventory": inventory,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--reviews", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--minimum-cases", type=int, choices=[60, 150], default=60)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("new audit output required")
    records = (
        [GoldReview.model_validate(r) for r in json.loads(args.reviews.read_text())]
        if args.reviews
        else []
    )
    result = assess(args.cases, records, args.minimum_cases)
    args.output.mkdir(parents=True)
    (args.output / "summary.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps({k: v for k, v in result.items() if k != "inventory"}, ensure_ascii=False))
