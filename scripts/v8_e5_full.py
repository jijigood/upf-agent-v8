"""Run actual cumulative E5 gates on 120 complete development plans."""

import argparse
from pathlib import Path

from upf_agent.v8.e5_full import run_e5_full

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_e5_full(Path(__file__).resolve().parents[1], args.output)
    print(
        {
            "candidates": result["candidate_count"],
            "A4_correct": result["A4_correct"],
            "pass": result["engineering_pass"],
        }
    )
