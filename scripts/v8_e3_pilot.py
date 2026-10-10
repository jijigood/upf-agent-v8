"""Run E3 staged-source development controls; opt in to actual native P5 model runs."""

import argparse
import json
from pathlib import Path

from upf_agent.v8.e3 import run_e3

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--native-p5", action="store_true")
    parser.add_argument("--shared-public-tools", action="store_true")
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = run_e3(
        args.project,
        args.output,
        native_p5=args.native_p5,
        shared_public_tools=args.shared_public_tools,
    )
    print(json.dumps({k: v for k, v in result.items() if k != "source"}, ensure_ascii=False))
