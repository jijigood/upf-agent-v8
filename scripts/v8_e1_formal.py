"""Prepare, audit, freeze and run file-backed E1 validation/heldout datasets."""

import argparse
import json
from pathlib import Path

from upf_agent.v8.e1_dataset import initialize, load_dataset, readiness, write
from upf_agent.v8.e1_formal import freeze, run
from upf_agent.v8.e1_output_review import finalize


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["init", "audit", "freeze", "run", "finalize"])
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dataset", type=Path, default=Path("eval/v8/e1"))
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--legacy-cases",
        type=Path,
        default=Path("runtime/v8-next/phase2/review-closure-full-001/cases"),
    )
    parser.add_argument("--scale", type=int, choices=[60, 150], default=60)
    parser.add_argument("--stage", choices=["validation", "heldout"], default="validation")
    parser.add_argument(
        "--runner-profile", choices=["legacy", "verified-runtime-candidate-1"], default="legacy"
    )
    parser.add_argument("--validation-result", type=Path)
    parser.add_argument("--deployment", type=Path)
    parser.add_argument("--frozen-input", type=Path)
    parser.add_argument("--run-result", type=Path)
    parser.add_argument("--output-reviews", type=Path)
    parser.add_argument("--review-root", type=Path)
    args = parser.parse_args()
    if args.command == "init":
        result = initialize(args.project.resolve(), args.dataset, args.legacy_cases)
    elif args.command == "audit":
        result = readiness(load_dataset(args.dataset), args.scale)
        if args.output:
            if args.output.exists():
                raise ValueError("new audit output required")
            write(args.output / "summary.json", result)
    elif args.command == "freeze":
        if args.output is None:
            parser.error("freeze requires --output")
        result = freeze(
            args.project,
            args.dataset,
            args.output,
            stage=args.stage,
            scale=args.scale,
            validation_result=args.validation_result,
            deployment_file=args.deployment,
            runner_profile=args.runner_profile,
        )
    elif args.command == "run":
        if args.output is None or args.frozen_input is None:
            parser.error("run requires --frozen-input and --output")
        result = run(args.project, args.frozen_input, args.output)
    else:
        if any(
            value is None
            for value in [
                args.frozen_input,
                args.run_result,
                args.output_reviews,
                args.review_root,
                args.output,
            ]
        ):
            parser.error(
                "finalize requires frozen input, run result, output reviews, review root and output"
            )
        result = finalize(
            args.frozen_input, args.run_result, args.output_reviews, args.review_root, args.output
        )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
