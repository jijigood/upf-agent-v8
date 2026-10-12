"""Candidate head checks on saved validation inputs and preregistered development cases."""

import argparse
import json
import shutil
import subprocess
from functools import partial
from pathlib import Path

import httpx
from v8_e1_calibration import verify_model
from v8_e1_validation_packet import validation_cases

from upf_agent.models import LocalModelError
from upf_agent.v8.bounded_plan_generator import (
    candidate_manifest,
    candidate_schema,
    generate_bounded_plan,
)
from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.e1_dataset import CaseManifest, inside, read, sha, write
from upf_agent.v8.e1_formal import code_snapshot
from upf_agent.v8.models import EvaluationContext, EvidenceBinding, OrchestrationTask, digest
from upf_agent.v8.phase2 import METHODS, append_jsonl, run_method
from upf_agent.v8.plan_capabilities import compile_capabilities
from upf_agent.v8.plan_generator import ObservedPlanClient
from upf_agent.v8.plan_ir import CaseGold
from upf_agent.v8.plan_translator import translate_plan
from upf_agent.v8.plan_validator import validate_plan

DEV_IDS = ["pilot-01", "pilot-05", "pilot-13"]


class LoopbackClient(ObservedPlanClient):
    def __init__(self, *args, grammar_python, **kwargs):
        super().__init__(*args, **kwargs)
        self.grammar_python = grammar_python
        self.client.close()
        self.client = httpx.Client(timeout=180, trust_env=False)

    def compile_candidate_schema(self, schema):
        script = (
            "import sys,xgrammar; "
            "print(str(xgrammar.Grammar.from_json_schema("
            "sys.stdin.read(),any_whitespace=False,separators=(',',':'))))"
        )
        try:
            result = subprocess.run(
                [self.grammar_python, "-c", script],
                input=json.dumps(schema),
                text=True,
                capture_output=True,
                timeout=max(0.001, self.budget.remaining()),
                check=True,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
            raise LocalModelError(f"compact grammar compilation failed: {error}") from error
        return result.stdout.strip()


def schema_audit(project, dataset, saved_run, output):
    if output.exists():
        raise ValueError("fresh schema audit required")
    selected = validation_cases(dataset.resolve())
    output.mkdir(parents=True)
    rows = []
    for manifest, _, _, _ in selected:
        for method in METHODS:
            folder = saved_run / "runs" / manifest.case_id / f"method-{METHODS.index(method) + 1}"
            task = OrchestrationTask.model_validate(read(folder / "task.json"))
            context = EvaluationContext.model_validate(read(folder / "context.json"))
            bindings = [EvidenceBinding.model_validate(b) for b in read(folder / "bindings.json")]
            caps = compile_capabilities(task, context, bindings, folder / "runtime")
            header = {
                "context_fingerprint": context.fingerprint,
                "scope_fingerprint": digest(task.permission),
                "batch_id": context.batch_id,
                "evaluation_as_of": context.as_of.isoformat(),
                "target_objects": task.objects,
            }
            schema = candidate_schema(bindings, header, capabilities=caps, task=task)
            branches = schema["$defs"]["PlanStep"]["anyOf"]
            row = {
                "case_id": manifest.case_id,
                "method": method,
                "schema_sha256": digest(schema),
                "fixed_step_slots": False,
                "min_steps": schema["properties"]["steps"]["minItems"],
                "max_steps": schema["properties"]["steps"]["maxItems"],
                "admitted_evidence": len(caps["admissible_ids"]),
                "allowed_actions": sorted(
                    {b["properties"]["action_type"]["const"] for b in branches}
                ),
            }
            rows.append(row)
            write(
                output / manifest.case_id / f"method-{METHODS.index(method) + 1}-schema.json",
                schema,
            )
    write(output / "rows.json", rows)
    result = {
        "cases": len(selected),
        "schemas_verified": len(rows),
        "all_variable_1_to_8_steps": all(r["min_steps"] == 1 and r["max_steps"] == 8 for r in rows),
        "source_evidence_still_unapproved": all(r["admitted_evidence"] == 0 for r in rows),
        "new_model_calls": 0,
        "heldout_inputs_read": 0,
        "formal_e1_completed": False,
        "candidate": candidate_manifest(),
    }
    write(output / "summary.json", result)
    write(
        output / "sha256_manifest.json",
        {str(p.relative_to(output)): sha(p) for p in sorted(output.rglob("*")) if p.is_file()},
    )
    return result


def dev_run(project, dataset, output, deployment, *, client_factory=None, probe=True):
    project, dataset, output = (p.resolve() for p in [project, dataset, output])
    if output.exists() or output.is_relative_to(dataset):
        raise ValueError("fresh development run outside the source dataset required")
    cases = []
    for case_id in DEV_IDS:
        path = dataset / "development" / case_id / "case.json"
        manifest = CaseManifest.model_validate(read(path))
        if manifest.split != "dev" or manifest.case_id != case_id:
            raise ValueError("candidate preflight requires the explicit development cases")
        task = OrchestrationTask.model_validate(read(inside(dataset, manifest.task_file)))
        gold = CaseGold.model_validate(read(inside(dataset, manifest.reference_file)))
        if gold.reviewed or gold.split != "dev":
            raise ValueError("development draft reference required; no formal scoring")
        cases.append((manifest, task, gold, inside(dataset, manifest.visible_root, directory=True)))
    receipt = read(deployment)
    if client_factory is None:
        client_factory = partial(LoopbackClient, grammar_python=receipt["server_command"][0])
    if probe:
        print("verifying existing physical model and service", flush=True)
        verify_model(project, receipt)
    code = code_snapshot(project)
    for name in [
        "scripts/v8_e1_planning_candidate.py",
        "scripts/v8_e1_validation_packet.py",
        "scripts/v8_e1_calibration.py",
    ]:
        code["files"][name] = sha(project / name)
    code["sha256"] = digest(code["files"])
    output.mkdir(parents=True)
    for name in code["files"]:
        target = output / "code" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(project / name, target)
    order = [METHODS[0], METHODS[2], METHODS[1], METHODS[3]]
    metas = []
    for i, (m, task, gold, visible) in enumerate(cases):
        frozen = output / "frozen-inputs" / m.case_id
        shutil.copytree(visible, frozen)
        write(
            output / "organizer-only" / m.case_id / "unreviewed-dev-reference.json",
            gold.model_dump(mode="json"),
        )
        metas.append(
            {
                "case_id": m.case_id,
                "template": task.template,
                "task": task.model_dump(mode="json"),
                "reference_is_unreviewed_development_only": True,
                "method_order": order[i % 4 :] + order[: i % 4],
            }
        )
    inputs = {
        str(p.relative_to(output / "frozen-inputs")): sha(p)
        for p in (output / "frozen-inputs").rglob("*")
        if p.is_file()
    }
    write(
        output / "protocol.json",
        {
            "kind": "bounded-head-development-preflight",
            "head": candidate_manifest(),
            "cases": metas,
            "code": code,
            "input_hashes": inputs,
            "model_receipt": receipt,
            "model_receipt_sha256": sha(deployment),
            "budget": {"models": 8, "tools": 8, "rounds": 3, "seconds": 180},
            "method_order": "preregistered Latin rotation",
            "planned_method_runs": 12,
            "Gold_used_for_generation": False,
            "post_generation_repair": False,
            "formal_vpr_enabled": False,
            "heldout_consumed": False,
        },
    )
    rows = []
    for (_, task, gold, _), meta in zip(cases, metas, strict=True):
        for method in meta["method_order"]:
            folder = output / "runs" / gold.case_id / f"method-{METHODS.index(method) + 1}"
            folder.mkdir(parents=True)
            try:
                row = run_method(
                    project,
                    output / "frozen-inputs" / gold.case_id,
                    folder,
                    task,
                    gold,
                    method,
                    client_factory,
                    calibration_candidate=True,
                    plan_generator=generate_bounded_plan,
                )
                parsed = translate_plan((folder / "raw-plan.txt").read_text()).plan
                cost = read(folder / "metrics.json")
                row.update(
                    {
                        "model_attempts": cost["invocations"]["model"]["attempted"],
                        "tool_attempts": cost["invocations"]["tool"]["attempted"],
                        "input_tokens": cost["token_usage"]["input"],
                        "output_tokens": cost["token_usage"]["output"],
                        "actions": [(s.action_type, s.target) for s in parsed.steps]
                        if parsed
                        else [],
                        "runner_error": None,
                    }
                )
                frozen_task = OrchestrationTask.model_validate(read(folder / "task.json"))
                bindings = [
                    EvidenceBinding.model_validate(b) for b in read(folder / "bindings.json")
                ]
                context = EvaluationContext.model_validate(read(folder / "context.json"))
                actual = validate_plan(
                    parsed,
                    bindings,
                    frozen_task,
                    compile_contract(frozen_task),
                    context,
                    folder / "runtime",
                )
                assert actual.model_dump(mode="json") == read(folder / "validation.json")
            except Exception as exc:
                row = {
                    "case_id": gold.case_id,
                    "method": method,
                    "parsed": False,
                    "validator_pass": False,
                    "reference_pass": False,
                    "actions": [],
                    "model_attempts": None,
                    "tool_attempts": None,
                    "input_tokens": None,
                    "output_tokens": None,
                    "runner_error": f"{type(exc).__name__}:{exc}",
                }
            row.update(
                vpr=None,
                split="dev",
                reviewed=False,
                head=candidate_manifest()["version"],
                evaluation_scope="unreviewed development reference match; not technical VPR",
            )
            write(folder / "case-metrics.json", row)
            append_jsonl(output / "metrics-by-case.jsonl", row)
            rows.append(row)
            print(
                json.dumps(
                    {
                        k: row.get(k)
                        for k in [
                            "case_id",
                            "method",
                            "parsed",
                            "validator_pass",
                            "reference_pass",
                            "runner_error",
                        ]
                    }
                ),
                flush=True,
            )
    unchanged = all(sha(output / "frozen-inputs" / n) == v for n, v in inputs.items()) and all(
        sha(project / n) == v for n, v in code["files"].items()
    )
    result = {
        "cases": len(cases),
        "planned_method_runs": 12,
        "recorded_method_runs": len(rows),
        "parsed": sum(r["parsed"] for r in rows),
        "validator_passes": sum(r["validator_pass"] for r in rows),
        "dev_reference_matches": sum(bool(r["reference_pass"]) for r in rows),
        "distinct_action_target_sequences": len({digest(r["actions"]) for r in rows}),
        "actual_model_attempts_known": sum(r["model_attempts"] or 0 for r in rows),
        "unknown_cost_runs": sum(r["model_attempts"] is None for r in rows),
        "runner_errors": sum(bool(r["runner_error"]) for r in rows),
        "source_unchanged": unchanged,
        "formal_vpr": None,
        "formal_e1_completed": False,
        "heldout_inputs_read": 0,
        "actual_human_reviews": 0,
    }
    write(output / "summary.json", result)
    write(
        output / "sha256_manifest.json",
        {str(p.relative_to(output)): sha(p) for p in sorted(output.rglob("*")) if p.is_file()},
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["schema-audit", "dev-run"])
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dataset", type=Path, default=Path("eval/v8/e1"))
    parser.add_argument("--saved-run", type=Path)
    parser.add_argument("--deployment", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "schema-audit":
        if args.saved_run is None:
            parser.error("schema-audit requires --saved-run")
        result = schema_audit(args.project, args.dataset, args.saved_run, args.output)
    else:
        if args.deployment is None:
            parser.error("dev-run requires --deployment")
        result = dev_run(args.project, args.dataset, args.output, args.deployment)
    print(json.dumps(result, ensure_ascii=False))
