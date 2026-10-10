"""Hash-based blank review seats for E2/E3/E6 outputs and real E7 investigations."""

import argparse
import csv
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export(project, output):
    if output.exists():
        raise ValueError("fresh output required")
    output.mkdir(parents=True)
    runtime = project / "runtime/v8-next"
    entries, hashes = [], {}

    def add(kind, key, files):
        pinned = {}
        for path in files:
            name = str(path.relative_to(project))
            pinned[name] = hashes[name] = sha(path)
        digest = hashlib.sha256(json.dumps(pinned, sort_keys=True).encode()).hexdigest()
        entries.append(
            {
                "kind": kind,
                "item_id": key,
                "input_sha256": digest,
                "material_files": list(pinned),
                "reviewed": False,
            }
        )

    for folder in sorted((runtime / "phase3/review-e2-full-001/queries").iterdir()):
        add("E2", folder.name, sorted(p for p in folder.rglob("*") if p.is_file()))
    for folder in sorted((runtime / "phase3/review-e3-full-001/inputs").iterdir()):
        add("E3", folder.name, sorted(p for p in folder.rglob("*") if p.is_file()))
    # Retain all 540 outputs in the index; prioritize disagreements without selecting
    # away failures from the experimental denominator or rewriting any raw material.
    for folder in sorted((runtime / "phase3/review-e6-full-001/runs").glob("*/*/*/*")):
        if (folder / "raw-plan.txt").exists():
            add(
                "E6-output",
                str(folder.relative_to(runtime / "phase3/review-e6-full-001/runs")),
                [
                    folder / n
                    for n in [
                        "raw-plan.txt",
                        "task.json",
                        "bindings.json",
                        "case-metrics.json",
                        "traces.jsonl",
                    ]
                ]
                + sorted(p for p in (folder / "runtime/data").rglob("*") if p.is_file()),
            )
    e7 = runtime / "wp11/e7-diagnostic-full-002"
    summary = json.loads((e7 / "summary.json").read_text())
    assert summary["completed"] == summary["planned"] == 60
    for folder in sorted((e7 / "rounds").iterdir()):
        add(
            "E7",
            folder.name,
            [
                folder / n
                for n in [
                    "input/snapshot.json",
                    "agent/facts.json",
                    "agent/model-visible-facts.json",
                    "agent/raw-model-output.json",
                    "agent/root-cause-report.json",
                ]
            ],
        )
    counts = {
        kind: sum(e["kind"] == kind for e in entries) for kind in ["E2", "E3", "E6-output", "E7"]
    }
    assert counts == {"E2": 96, "E3": 32, "E6-output": 540, "E7": 60}
    (output / "input-index.json").write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n"
    )
    (output / "source-sha256.json").write_text(
        json.dumps(hashes, ensure_ascii=False, indent=2) + "\n"
    )
    manifest_sha = sha(output / "source-sha256.json")
    fields = [
        "kind",
        "item_id",
        "input_sha256",
        "source_manifest_sha256",
        "reviewer",
        "reviewed_at",
        "decision",
        "source_locators",
        "rationale",
    ]
    for seat in (1, 2):
        with (output / f"reviewer-{seat}.csv").open(
            "w", encoding="utf-8-sig", newline=""
        ) as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            for entry in entries:
                writer.writerow(
                    {k: entry[k] for k in fields if k in entry}
                    | {"source_manifest_sha256": manifest_sha}
                )
    result = {
        "counts": counts,
        "records_per_seat": len(entries),
        "reviewers": 2,
        "source_files": len(hashes),
        "source_manifest_sha256": manifest_sha,
        "human_decisions": 0,
        "formal_acceptance": False,
        "E7_first_pass": "visible sources only; private injection truth excluded",
        "scope": "local material locator index; not anonymous or a Gold approval",
    }
    (output / "export-summary.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(export(Path(__file__).resolve().parents[1], args.output), ensure_ascii=False))
