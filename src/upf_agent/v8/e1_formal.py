"""Frozen file-backed validation/heldout execution; references never enter generation inputs."""

import csv
import random
import shutil
from functools import partial
from pathlib import Path

import httpx

from upf_agent.config import load_model_config
from upf_agent.v8.common_tools import CommonEvidenceTools
from upf_agent.v8.e1_dataset import components, load_dataset, read, readiness, sha, write
from upf_agent.v8.experiment_manifest import source_manifest
from upf_agent.v8.models import canonical, digest
from upf_agent.v8.phase2 import METHODS, append_jsonl, run_method
from upf_agent.v8.plan_generator import ObservedPlanClient, generation_manifest
from upf_agent.v8.plan_metrics import summarize_cases


def model_identity(response):
    """Compare service capabilities, excluding per-GET card/permission creation metadata."""
    rows = []
    for model in response["data"]:
        if not model.get("id"):
            raise ValueError("model card identity missing")
        row = {k: v for k, v in model.items() if k not in {"created", "permission"}}
        row["permission"] = [
            {k: v for k, v in permission.items() if k not in {"id", "created"}}
            for permission in model.get("permission", [])
        ]
        rows.append(row)
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("duplicate model card identity")
    return {"object": response.get("object"), "data": sorted(rows, key=lambda row: row["id"])}


def deployment_snapshot(project, receipt_file):
    if receipt_file is None:
        raise ValueError("actual model deployment receipt required before formal freeze")
    receipt = read(receipt_file)
    model = load_model_config(project / "config/models.yaml").generation["baseline"]
    if (
        receipt.get("served_name") != model.served_name
        or receipt.get("endpoint") != model.endpoint
        or not receipt.get("server_command")
    ):
        raise ValueError("deployment receipt/config mismatch or missing actual launch command")
    hashes = receipt.get("model_files", {})
    required = {
        str(p.relative_to(model.path))
        for p in model.path.rglob("*")
        if p.is_file() and (p.suffix in {".safetensors", ".json", ".model"})
    }
    if "config.json" not in required or not any(n.endswith(".safetensors") for n in required):
        raise ValueError("local model files unavailable")
    if not required.issubset(hashes):
        raise ValueError("deployment receipt does not pin all weights/tokenizer/config files")
    for name, expected in hashes.items():
        path = model.path / name
        if Path(name).is_absolute() or ".." in Path(name).parts or sha(path) != expected:
            raise ValueError("frozen model file mismatch")
    response = httpx.get(model.endpoint + "/models", timeout=15, trust_env=False)
    response.raise_for_status()
    models = response.json()
    if model.served_name not in {m["id"] for m in models["data"]}:
        raise ValueError("actual model service identity mismatch")
    return {
        "configuration": model.model_dump(mode="json"),
        "receipt": receipt,
        "receipt_sha256": sha(receipt_file),
        "models_response": models,
        "models_identity": model_identity(models),
    }


def code_snapshot(project):
    code = source_manifest(project)
    for name in ["scripts/v8_e1_formal.py", "config/models.yaml"]:
        code["files"][name] = sha(project / name)
    code["sha256"] = digest(code["files"])
    return code


def heldout_registry(project):
    return project / "runtime/v8-next/e1-heldout-consumption"


def heldout_keys(dataset, case_ids):
    result = []
    for case in dataset["cases"]:
        manifest = case["manifest"]
        if manifest.case_id in case_ids:
            sources = sorted(manifest.raw_source_hashes.values()) or sorted(
                sha(case["visible"] / name) for name in case["task"].observation_files
            )
            result.append(digest(sources))
    if len(result) != len(set(result)):
        raise ValueError("duplicate heldout physical input sets")
    return result


def runner_options(profile):
    if profile == "legacy":
        return {"tools_factory": NormalizedEvidenceTools}, generation_manifest()
    if profile == "task-covered-readonly-1":
        from upf_agent.v8.e1_covered_head import (
            ReservedHeadBudget,
            covered_manifest,
            generate_covered,
            translate_covered,
            validate_covered,
        )
        from upf_agent.v8.e1_source_closure import VerifiedDomainTools
        from upf_agent.v8.e1_verified_head import run_verified_p5

        return {
            "tools_factory": VerifiedDomainTools,
            "p5_runner": run_verified_p5,
            "plan_generator": generate_covered,
            "plan_translator": translate_covered,
            "plan_validator": validate_covered,
            "budget_factory": ReservedHeadBudget,
        }, covered_manifest()
    if profile == "expert-readonly-revision-1":
        from upf_agent.v8.e1_expert_revision import (
            generate_revision,
            revision_manifest,
            translate_revision,
            validate_revision,
        )
        from upf_agent.v8.e1_source_closure import VerifiedDomainTools
        from upf_agent.v8.e1_verified_head import run_verified_p5

        return {
            "tools_factory": VerifiedDomainTools,
            "p5_runner": run_verified_p5,
            "plan_generator": generate_revision,
            "plan_translator": translate_revision,
            "plan_validator": validate_revision,
        }, revision_manifest()
    if profile != "verified-runtime-candidate-1":
        raise ValueError("unknown formal runner profile")
    from upf_agent.v8.e1_domain_readonly import translate_domain_plan, validate_domain_plan
    from upf_agent.v8.e1_source_closure import VerifiedDomainTools
    from upf_agent.v8.e1_verified_head import generate_verified_plan, head_manifest, run_verified_p5

    return {
        "tools_factory": VerifiedDomainTools,
        "p5_runner": run_verified_p5,
        "plan_generator": generate_verified_plan,
        "plan_translator": translate_domain_plan,
        "plan_validator": validate_domain_plan,
    }, head_manifest()


def freeze(
    project,
    dataset_root,
    output,
    *,
    stage="validation",
    scale=60,
    validation_result=None,
    deployment_file=None,
    runner_profile="legacy",
):
    project, dataset_root, output = project.resolve(), dataset_root.resolve(), output.resolve()
    if (
        stage not in {"validation", "heldout"}
        or output.exists()
        or output.is_relative_to(dataset_root)
    ):
        raise ValueError("valid stage and new output outside dataset required")
    dataset = load_dataset(dataset_root)
    status = readiness(dataset, scale)
    if not status["data_ready"]:
        raise ValueError("formal data not ready: " + "; ".join(status["problems"]))
    _, profile_head = runner_options(runner_profile)
    if runner_profile != "legacy":
        from upf_agent.v8.e1_source_closure import verify_admission

        for case in dataset["cases"]:
            if case["manifest"].split == stage:
                if case["task"].template != "runtime_investigation":
                    raise ValueError("verified runtime profile requires explicit runtime tasks")
                verify_admission(case["visible"], case["task"])
    if stage == "heldout":
        ids = [c["manifest"].case_id for c in dataset["cases"] if c["manifest"].split == stage]
        if any(
            (heldout_registry(project) / (key + ".json")).exists()
            for key in heldout_keys(dataset, ids)
        ):
            raise ValueError("heldout physical inputs previously consumed/reserved")
    code = code_snapshot(project)
    validation = None
    if stage == "heldout":
        if validation_result is None:
            raise ValueError("completed frozen validation result required before heldout")
        validation = read(validation_result / "summary.json")
        previous = read(validation_result / "freeze.json")
        hashes = read(validation_result / "sha256_manifest.json")
        if any(sha(validation_result / name) != expected for name, expected in hashes.items()):
            raise ValueError("validation output changed")
        if (
            validation["stage"] != "validation"
            or not validation["execution_pass"]
            or not validation.get("natural_language_output_review_completed", False)
            or validation["heldout_consumed"]
            or previous["code"] != code
            or previous["dataset_files"] != dataset["files"]
            or previous.get("runner_profile", "legacy") != runner_profile
        ):
            raise ValueError("validation incomplete or code/dataset changed since calibration")
    deployment = deployment_snapshot(project, deployment_file)
    if stage == "heldout" and {k: v for k, v in deployment.items() if k != "models_response"} != {
        k: v for k, v in previous["deployment"].items() if k != "models_response"
    }:
        raise ValueError("deployment changed after validation")
    selected = [c for c in dataset["cases"] if c["manifest"].split == stage]
    rng = random.Random(20261010)
    base = list(METHODS)
    rng.shuffle(base)
    order = {
        c["manifest"].case_id: base[i % 4 :] + base[: i % 4]
        for i, c in enumerate(sorted(selected, key=lambda c: c["manifest"].case_id))
    }
    frozen = {
        "schema_version": "v8-e1-formal-freeze-1",
        "stage": stage,
        "scale": scale,
        "methods": METHODS,
        "primary_comparison": [METHODS[1], METHODS[3]],
        "secondary_comparisons": [[METHODS[2], METHODS[3]], [METHODS[0], METHODS[3]]],
        "budget": {"tools": 8, "models": 8, "rounds": 3, "seconds": 180},
        "head": profile_head,
        "runner_profile": runner_profile,
        "tool_adapter": NormalizedEvidenceTools.version,
        "code": code,
        "dataset_files": dataset["files"],
        "deployment": deployment,
        "selected_cases": sorted(order),
        "method_order": order,
        "method_order_design": "seeded balanced Latin rotation; same frozen inputs",
        "statistics": {
            "primary_metric": "approved-solvable-case VPR",
            "cluster_fields": ["source_group", "structure_family"],
            "bootstrap_repetitions": 2000,
            "seed": 20261010,
            "failure_in_denominator": True,
            "superiority_assumed": False,
        },
        "validation_summary_sha256": sha(validation_result / "summary.json")
        if validation_result
        else None,
        "heldout_consumed": False,
        "limitations": [
            "bounded existing IR and common workflow head",
            "physical receipts cannot establish human independence",
            "shared service latency is descriptive",
        ],
    }
    output.mkdir(parents=True)
    shutil.copytree(dataset_root, output / "dataset")
    for name, expected in frozen["dataset_files"].items():
        if sha(output / "dataset" / name) != expected or sha(dataset_root / name) != expected:
            raise ValueError("dataset changed during freeze")
    for name, expected in code["files"].items():
        path = output / "code" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(project / name, path)
        if sha(path) != expected:
            raise ValueError("code changed during freeze")
    write(output / "readiness.json", status)
    write(output / "freeze.json", frozen)
    write(
        output / "sha256_manifest.json",
        {str(p.relative_to(output)): sha(p) for p in sorted(output.rglob("*")) if p.is_file()},
    )
    return frozen


class NormalizedEvidenceTools(CommonEvidenceTools):
    version = "v8-common-normalized-tools-1"

    def __init__(self, root, task, contract, budget):
        super().__init__(root, task, contract, budget, allow_real=True)


def paired_statistics(dataset, rows, frozen):
    cost_case_ids = list(frozen["selected_cases"])
    selected = [
        c
        for c in dataset["cases"]
        if c["manifest"].case_id in frozen["selected_cases"]
        and c["approved"].solvability == "solvable"
    ]
    clusters = components(selected)
    index = {(r["case_id"], r["method"]): r for r in rows}
    results = []
    for baseline, treatment in [frozen["primary_comparison"], *frozen["secondary_comparisons"]]:
        costs = {}
        for metric in [
            "tool_attempts",
            "model_attempts",
            "input_tokens",
            "output_tokens",
            "elapsed_seconds",
        ]:
            pairs, missing = [], []
            for case_id in cost_case_ids:
                x, y = index[case_id, baseline].get(metric), index[case_id, treatment].get(metric)
                if x is None or y is None:
                    missing.append(case_id)
                else:
                    pairs.append((x, y))
            complete = bool(cost_case_ids) and not missing
            costs[metric] = {
                "planned_case_denominator": len(cost_case_ids),
                "measured_pairs": len(pairs),
                "unknown_case_ids": missing,
                "baseline_known_total": sum(x for x, _ in pairs),
                "treatment_known_total": sum(y for _, y in pairs),
                "mean_difference": sum(y - x for x, y in pairs) / len(pairs) if complete else None,
                "complete_measurement": complete,
                "scope": "all frozen cases, including failures and nonsolvable cases",
                "cost_superiority_claim": False,
            }
        values = [
            (
                bool(index[c["manifest"].case_id, baseline]["vpr"]),
                bool(index[c["manifest"].case_id, treatment]["vpr"]),
            )
            for c in selected
        ]
        interval = None
        if len(clusters) >= 2:
            rng = random.Random(frozen["statistics"]["seed"])
            samples = []
            for _ in range(frozen["statistics"]["bootstrap_repetitions"]):
                ids = [
                    case_id for _ in clusters for case_id in clusters[rng.randrange(len(clusters))]
                ]
                samples.append(
                    sum(index[i, treatment]["vpr"] - index[i, baseline]["vpr"] for i in ids)
                    / len(ids)
                )
            samples.sort()
            interval = [
                samples[int(0.025 * (len(samples) - 1))],
                samples[int(0.975 * (len(samples) - 1))],
            ]
        results.append(
            {
                "baseline": baseline,
                "treatment": treatment,
                "solvable_case_denominator": len(values),
                "clusters": len(clusters),
                "mean_difference": sum(y - x for x, y in values) / len(values) if values else None,
                "improved": sum(y > x for x, y in values),
                "regressed": sum(y < x for x, y in values),
                "cluster_bootstrap95": interval,
                "paired_costs": costs,
                "superiority_claim": False,
            }
        )
    return results


def run(project, frozen_root, output, *, client_factory=ObservedPlanClient, probe=True):
    project, frozen_root, output = project.resolve(), frozen_root.resolve(), output.resolve()
    if output.exists() or output.is_relative_to(frozen_root):
        raise ValueError("new run directory outside frozen input required")
    frozen = read(frozen_root / "freeze.json")
    profile_options, _ = runner_options(frozen.get("runner_profile", "legacy"))
    if frozen.get("runner_profile", "legacy") != "legacy" and client_factory is ObservedPlanClient:
        from upf_agent.v8.e1_verified_head import VerifiedPlanClient

        client_factory = partial(
            VerifiedPlanClient,
            grammar_python=frozen["deployment"]["receipt"]["server_command"][0],
        )
    for name, expected in read(frozen_root / "sha256_manifest.json").items():
        if sha(frozen_root / name) != expected:
            raise ValueError("frozen input changed")
    if code_snapshot(project) != frozen["code"]:
        raise ValueError("code/model configuration differs from formal freeze")
    dataset = load_dataset(frozen_root / "dataset")
    if not readiness(dataset, frozen["scale"])["data_ready"]:
        raise ValueError("frozen dataset is not ready")
    if probe:
        # Probe before reserving the stage; no task is sent by this model identity GET.
        model = load_model_config(project / "config/models.yaml").generation["baseline"]
        for name, expected in frozen["deployment"]["receipt"]["model_files"].items():
            if sha(model.path / name) != expected:
                raise ValueError("model changed since freeze")
        response = httpx.get(model.endpoint + "/models", timeout=15, trust_env=False)
        response.raise_for_status()
        if model_identity(response.json()) != frozen["deployment"]["models_identity"]:
            raise ValueError("actual model service changed since freeze")
    # Reserve the entire frozen stage once; crashes/failures never make heldout reusable.
    marker = frozen_root / "consumption.json"
    if frozen["stage"] == "heldout":
        registry = heldout_registry(project)
        keys = heldout_keys(dataset, frozen["selected_cases"])
        if any((registry / (key + ".json")).exists() for key in keys):
            raise ValueError("heldout physical inputs previously consumed/reserved")
        registry.mkdir(parents=True, exist_ok=True)
        for key in keys:
            with (registry / (key + ".json")).open("x") as stream:
                stream.write(
                    canonical(
                        {
                            "freeze_sha256": sha(frozen_root / "freeze.json"),
                            "output": str(output),
                            "state": "reserved-before-model-request",
                        }
                    )
                    + "\n"
                )
    with marker.open("x") as stream:
        stream.write(
            canonical(
                {
                    "stage": frozen["stage"],
                    "output": str(output),
                    "freeze_sha256": sha(frozen_root / "freeze.json"),
                }
            )
            + "\n"
        )
    output.mkdir(parents=True)
    write(output / "freeze.json", frozen)
    write(output / "run-plan.json", frozen["method_order"])
    rows = []
    selected = {
        c["manifest"].case_id: c
        for c in dataset["cases"]
        if c["manifest"].case_id in frozen["selected_cases"]
    }
    for case_id in frozen["selected_cases"]:
        case = selected[case_id]
        for method in frozen["method_order"][case_id]:
            folder = output / "runs" / case_id / f"method-{METHODS.index(method) + 1}"
            folder.mkdir(parents=True)
            try:
                row = run_method(
                    project,
                    case["visible"],
                    folder,
                    case["task"],
                    case["approved"],
                    method,
                    client_factory,
                    **profile_options,
                    calibration_candidate=frozen["stage"] == "validation",
                )
                row["runner_error"] = None
                cost = read(folder / "metrics.json")
                row.update(
                    model_attempts=cost["invocations"]["model"]["attempted"],
                    tool_attempts=cost["invocations"]["tool"]["attempted"],
                    input_tokens=cost["token_usage"]["input"],
                    output_tokens=cost["token_usage"]["output"],
                )
            except Exception as error:
                row = {
                    "case_id": case_id,
                    "method": method,
                    "reviewed": True,
                    "solvability": case["approved"].solvability,
                    "parsed": False,
                    "validator_pass": False,
                    "reference_pass": False,
                    "vpr": False if case["approved"].solvability == "solvable" else None,
                    "hard_constraint_violation": False,
                    "unscorable": True,
                    "runner_error": f"{type(error).__name__}:{error}",
                }
                write(folder / "runner-error.json", row)
            row.update(
                source_group=case["manifest"].source_group,
                structure_family=case["manifest"].structure_family,
                split=frozen["stage"],
            )
            rows.append(row)
            write(folder / "case-metrics.json", row)
            append_jsonl(output / "metrics-by-case.jsonl", row)
    fields = sorted(set().union(*(row.keys() for row in rows)))
    with (output / "metrics-by-case.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(
            {k: canonical(v) if isinstance(v, (dict, list, bool)) else v for k, v in row.items()}
            for row in rows
        )
    review_fields = [
        "seat",
        "case_id",
        "method",
        "raw_plan_sha256",
        "reference_sha256",
        "reviewer",
        "role",
        "semantic_valid",
        "review_version",
        "review_source",
        "notes",
    ]
    with (output / "empty-output-review-organizer-only.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=review_fields)
        writer.writeheader()
        for row in rows:
            raw = (
                output
                / "runs"
                / row["case_id"]
                / f"method-{METHODS.index(row['method']) + 1}"
                / "raw-plan.txt"
            )
            for seat in [1, 2]:
                writer.writerow(
                    {
                        "seat": seat,
                        "case_id": row["case_id"],
                        "method": row["method"],
                        "raw_plan_sha256": sha(raw) if raw.exists() else "",
                        "reference_sha256": digest(selected[row["case_id"]]["gold"]),
                    }
                )
    statistics = paired_statistics(dataset, rows, frozen)
    summaries = {
        method: summarize_cases([r for r in rows if r["method"] == method]) for method in METHODS
    }
    for summary in summaries.values():
        summary.pop("vpr_wilson95")
    unchanged = code_snapshot(project) == frozen["code"] and all(
        sha(frozen_root / "dataset" / name) == expected
        for name, expected in frozen["dataset_files"].items()
    )
    failed = [
        row
        for row in rows
        if row["runner_error"]
        or row.get("method_failure")
        or row.get("generation_error")
        or row.get("finish_reason") == "length"
    ]
    summary = {
        "schema_version": "v8-e1-formal-run-1",
        "stage": frozen["stage"],
        "cases": len(selected),
        "planned_method_runs": len(selected) * len(METHODS),
        "recorded_method_runs": len(rows),
        "summaries": summaries,
        "runner_errors": sum(bool(r["runner_error"]) for r in rows),
        "method_or_generation_errors": len(failed),
        "source_unchanged": unchanged,
        "execution_pass": unchanged and not failed,
        "formal_e1_execution_completed": frozen["stage"] == "heldout" and unchanged and not failed,
        "formal_e1_completed": False,
        "formal_statistics_completed": False,
        "reference_statistics_completed": frozen["stage"] == "heldout"
        and not failed
        and all(r["cluster_bootstrap95"] is not None for r in statistics),
        "heldout_consumed": frozen["stage"] == "heldout",
        "real_network_writes": 0,
        "approved_reference_count": len(selected),
        "superiority_claim": False,
        "natural_language_output_review_completed": False,
        "formal_vpr": None,
        "workflow_scope": frozen["head"]["generation_prior"],
    }
    write(output / "summary.json", summary)
    write(output / "paired-statistics.json", statistics)
    write(
        output / "failures.json",
        [row for row in rows if not row["reference_pass"] or row in failed],
    )
    write(
        output / "sha256_manifest.json",
        {str(p.relative_to(output)): sha(p) for p in sorted(output.rglob("*")) if p.is_file()},
    )
    return summary
