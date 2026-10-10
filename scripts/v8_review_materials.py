"""Export corrected reference, plan and perturbation material with blank human review seats."""

import argparse
import csv
import json
import shutil
from pathlib import Path

from v8_review_remediation import sha

from upf_agent.v8.models import digest
from upf_agent.v8.phase1 import write_json


def export(phase2, e6, output):
    if output.exists():
        raise ValueError("new review package required")
    output.mkdir(parents=True)
    entries, private = [], []

    def item(kind, key, original, files, data):
        token = digest([kind, key, [sha(p) for p in files.values()]])[:20]
        folder = output / "public" / kind / token
        folder.mkdir(parents=True)
        for name, path in files.items():
            shutil.copy2(path, folder / name)
        if data:
            shutil.copytree(data, folder / "data")
        entries.append(
            {
                "kind": kind,
                "anonymous_id": token,
                "material": str(folder.relative_to(output / "public")),
                "input_sha256": digest({n: sha(p) for n, p in files.items()}),
                "reviewed": False,
            }
        )
        private.append({"anonymous_id": token, "original": str(original)})
        return folder

    for folder in sorted((phase2 / "cases").iterdir()):
        item(
            "references",
            folder.name,
            folder,
            {
                "case-reference.json": folder / "case-reference.json",
                "case-spec.json": folder / "case-spec.json",
                "case-task.json": folder / "case-task.json",
            },
            folder / "data",
        )
    for folder in sorted((phase2 / "runs").glob("pilot-*/method-*")):
        item(
            "plans",
            str(folder.relative_to(phase2)),
            folder,
            {
                "raw-plan.txt": folder / "raw-plan.txt",
                "task.json": folder / "task.json",
                "bindings.json": folder / "bindings.json",
            },
            folder / "runtime/data",
        )
    for folder in sorted((e6 / "cases").glob("*/*")):
        proof = folder / "perturbation-proof.json"
        if not proof.exists():
            continue
        base = folder.parent / "base"
        target = item(
            "perturbations",
            str(folder.relative_to(e6)),
            folder,
            {
                "changed-task.json": folder / "task.json",
                "base-task.json": base / "task.json",
                "mechanical-proof.json": proof,
            },
            folder / "data",
        )
        shutil.copytree(base / "data", target / "base-data")
    counts = {
        kind: sum(r["kind"] == kind for r in entries)
        for kind in ["references", "plans", "perturbations"]
    }
    assert counts == {"references": 24, "plans": 96, "perturbations": 80}
    write_json(output / "public" / "input-index.json", entries)
    write_json(output / "organizer-only" / "source-map.json", private)
    write_json(
        output / "public" / "review-protocol.json",
        {
            "source_revision": "review-remediation-20261010-1",
            "review_order": "approve references separately; judge raw plans from visible facts",
            "reference_reviewer_focus": (
                "role/product/version, complete steps, conditional gap outlet"
            ),
            "plan_reviewer_focus": (
                "both P citations or explicit pending gaps; identity DAG; safe wording"
            ),
            "perturbation_focus": "task goal, scope, roles, time, permissions and physical facts",
            "prior_reviews": (
                "previous version opinions retained by organizers, not new-hash approval"
            ),
            "two_independent_reviewers_completed": False,
            "arbitration_completed": False,
            "formal_acceptance": False,
            "strict_blind_review_completed": False,
            "anonymization_limit": "styles and task fingerprints may reveal methods",
        },
    )
    for seat in [1, 2]:
        with (output / "public" / f"reviewer-{seat}.csv").open(
            "w", encoding="utf-8-sig", newline=""
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "kind",
                    "anonymous_id",
                    "input_sha256",
                    "reviewer",
                    "decision",
                    "source_locators",
                    "rationale",
                ],
            )
            writer.writeheader()
            writer.writerows({k: r.get(k, "") for k in writer.fieldnames} for r in entries)
    hashes = {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()}
    write_json(output / "sha256_manifest.json", hashes)
    return {"counts": counts, "files": len(hashes), "formal_approval": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase2", type=Path, required=True)
    parser.add_argument("--e6", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = export(args.phase2, args.e6, args.output)
    write_json(args.output / "export-summary.json", result)
    print(json.dumps(result, ensure_ascii=False))
