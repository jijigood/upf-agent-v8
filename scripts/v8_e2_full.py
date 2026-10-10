"""Run real P3 seed cache and all five E2 development controls."""

import argparse
from pathlib import Path

from upf_agent.v8.e2 import run_e2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cuda:1")
    parser.add_argument("--seed-cache", type=Path)
    args = parser.parse_args()
    result = run_e2(Path(__file__).resolve().parents[1], args.output, args.device, args.seed_cache)
    print(
        {
            "queries": result["queries"],
            "retrievals": result["method_retrievals"],
            "pass": result["engineering_pass"],
        }
    )
