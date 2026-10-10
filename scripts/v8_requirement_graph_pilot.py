"""Run WP08's 24-query synthetic engineering control package; not formal E2 Gold."""

import argparse
from pathlib import Path

from upf_agent.v8.wp08 import run_wp08

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_wp08(args.project.resolve(), args.output.resolve())
    print({"pass": result["pass"], "method_runs": result["method_runs"], "formal_e2": False})
    raise SystemExit(0 if result["pass"] else 1)
