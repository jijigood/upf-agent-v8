"""Run synthetic same-candidate offline gate controls, never execute a suggestion."""

import argparse
import json
from pathlib import Path

from upf_agent.v8.e5 import run_e5

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_e5(Path(__file__).resolve().parents[1], args.output)
    print(json.dumps({k: v for k, v in result.items() if k != "source"}, ensure_ascii=False))
