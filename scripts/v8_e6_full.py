"""Execute all 300 repeats and 240 fact-preserving development perturbations."""

import argparse
from pathlib import Path

from upf_agent.v8.e6 import run_e6

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--endpoint")
    args = parser.parse_args()
    result = run_e6(args.project, args.output, args.workers, args.endpoint)
    print({"completed": result["completed"], "fatal_errors": len(result["fatal_errors"])})
