"""Export per-invocation E7 controls without mixing development and fresh denominators."""

import argparse
import csv
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export(root, output):
    if output.exists():
        raise ValueError("fresh result export required")
    output.mkdir(parents=True)
    rows = []
    replay = root / "e7-development-paired-replay-001"
    for r in read(replay / "rows-organizer-only.json"):
        for mode, score in r["modes"].items():
            report = replay / "rounds" / f"round-{r['round']:03}" / (mode + ".json")
            rows.append(
                {
                    "scope": "known-development-replay",
                    "batch": replay.name,
                    "round": r["round"],
                    "condition_organizer_only": r["condition"],
                    "mode": mode,
                    "top1_correct": score["top1_correct"],
                    "top3_correct": score["top3_correct"],
                    "healthy": False,
                    "false_positive": None,
                    "snapshot_sha256": r["snapshot_sha256"],
                    "report_sha256": sha(report),
                    "model_calls": 0,
                    "diagnosis_seconds": read(report)["diagnosis_seconds"],
                    "formal_vpr": None,
                }
            )
    for name in (
        "e7-evidence-pilot-001",
        "e7-evidence-full-001",
        "e7-window-pilot-001",
        "e7-window-full-001",
    ):
        dataset = root / name
        if not (dataset / "summary.json").exists():
            continue
        if not read(dataset / "summary.json")["pass"]:
            raise ValueError("dataset engineering incomplete")
        for r in read(dataset / "summary.json")["rows"]:
            inputs = dataset / "rounds" / f"round-{r['round']:03}" / "input/snapshot.json"
            for mode, score in r["modes"].items():
                report = inputs.parent.parent / "agent" / (mode + ".json")
                rows.append(
                    {
                        "scope": "posthoc-window-sensitivity"
                        if "window" in name
                        else "fresh-controlled-observations",
                        "batch": name,
                        "round": r["round"],
                        "condition_organizer_only": r["condition"],
                        "mode": mode,
                        "top1_correct": score["top1_correct"],
                        "top3_correct": score["top3_correct"],
                        "healthy": r["condition"] == "healthy",
                        "false_positive": score["false_positive"]
                        if r["condition"] == "healthy"
                        else None,
                        "snapshot_sha256": sha(inputs),
                        "report_sha256": sha(report),
                        "model_calls": 0,
                        "diagnosis_seconds": read(report)["diagnosis_seconds"],
                        "formal_vpr": None,
                    }
                )
    fields = list(rows[0])
    with (output / "results-organizer-only.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    summaries = []
    for batch in sorted({r["batch"] for r in rows}):
        for mode in ("flat", "joined", "graph"):
            group = [r for r in rows if r["batch"] == batch and r["mode"] == mode]
            faults = [r for r in group if not r["healthy"]]
            summaries.append(
                {
                    "batch": batch,
                    "mode": mode,
                    "fault_denominator": len(faults),
                    "top1_correct": sum(r["top1_correct"] for r in faults),
                    "top3_correct": sum(r["top3_correct"] for r in faults),
                    "healthy_denominator": len(group) - len(faults),
                    "false_positives": sum(bool(r["false_positive"]) for r in group),
                    "formal_vpr": None,
                }
            )
    (output / "summary.json").write_text(
        json.dumps(
            {
                "rows": len(rows),
                "summaries": summaries,
                "csv_sha256": sha(output / "results-organizer-only.csv"),
                "formal_quality": False,
            },
            indent=2,
        )
        + "\n"
    )
    return {"rows": len(rows), "formal_quality": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(export(args.root, args.output)))
