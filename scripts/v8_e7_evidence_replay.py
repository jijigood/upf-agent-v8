"""Paired development replay; worker reads normal snapshots before organizer scoring."""

import argparse
import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from v8_e7_diagnostic_runner import CAUSE_MAP
from v8_e7_evidence_rca import write


def run(dataset, output):
    if output.exists():
        raise ValueError("fresh replay output required")
    output.mkdir(parents=True)
    original = json.loads((dataset / "summary.json").read_text())
    worker = Path(__file__).with_name("v8_e7_evidence_rca.py")
    hashes = {}

    def replay(row):
        number = row["round"]
        inputs = dataset / "rounds" / f"round-{number:03}" / "input"
        target = output / "rounds" / f"round-{number:03}"
        raw = inputs / "snapshot.json"
        expected_sha = hashlib.sha256(raw.read_bytes()).hexdigest()
        command = [
            sys.executable,
            str(worker),
            "--input",
            str(inputs),
            "--output",
            str(target),
            "--private-root",
            str(dataset / "private"),
        ]
        proc = subprocess.run(command, capture_output=True, text=True, timeout=60)
        receipt = {
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "argv": command,
            "round": number,
            "snapshot_sha256": expected_sha,
        }
        # Scoring outside the worker: these labels never enter diagnostic invocation.
        if proc.returncode == 0:
            results = json.loads((target / "diagnosis.json").read_text())
            if results["physical_capture_sha256"] != expected_sha:
                raise ValueError("input changed during replay")
            receipt["modes"] = {
                mode: {
                    "hypotheses": hypotheses,
                    "top1_correct": hypotheses[0] == CAUSE_MAP[row["condition"]],
                    "top3_correct": CAUSE_MAP[row["condition"]] in hypotheses,
                }
                for mode, hypotheses in results["hypotheses"].items()
            }
            receipt["old_model_top1_correct"] = row.get("top1_correct", False)
            receipt["old_model_top3_correct"] = row.get("top3_correct", False)
        receipt["condition"] = row["condition"]
        return receipt

    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(replay, original["rows"]))
    for row in rows:
        hashes[str(dataset / "rounds" / f"round-{row['round']:03}" / "input/snapshot.json")] = row[
            "snapshot_sha256"
        ]
    write(output / "rows-organizer-only.json", rows)
    write(output / "input-hashes.json", hashes)
    summary = {
        "scope": "development snapshots used in method design; not unbiased validation/heldout",
        "rounds": len(rows),
        "diagnostic_invocations": 3 * len(rows),
        "new_model_calls": 0,
        "method_failures": sum(r["returncode"] != 0 for r in rows),
        "modes": {
            mode: {
                "top1_correct": sum(
                    r.get("modes", {}).get(mode, {}).get("top1_correct", False) for r in rows
                ),
                "top3_correct": sum(
                    r.get("modes", {}).get(mode, {}).get("top3_correct", False) for r in rows
                ),
            }
            for mode in ("flat", "joined", "graph")
        },
        "old_model": {
            "top1_correct": sum(r.get("old_model_top1_correct", False) for r in rows),
            "top3_correct": sum(r.get("old_model_top3_correct", False) for r in rows),
        },
        "formal_quality": False,
        "pass": all(r["returncode"] == 0 for r in rows),
    }
    write(output / "summary.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.dataset.resolve(), args.output.resolve())))
