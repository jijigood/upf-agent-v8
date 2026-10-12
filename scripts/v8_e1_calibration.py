"""Unreviewed validation engineering runs; never score absent Gold or consume heldout."""

import argparse
import csv
import json
import random
import re
import shutil
import subprocess
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlparse

import httpx

from upf_agent.config import load_model_config
from upf_agent.v8.e1_dataset import load_dataset, read, sha, write
from upf_agent.v8.e1_formal import NormalizedEvidenceTools, code_snapshot, model_identity
from upf_agent.v8.models import canonical, digest
from upf_agent.v8.phase2 import METHODS, append_jsonl, run_method
from upf_agent.v8.plan_generator import ObservedPlanClient


def prepare_model_receipt(project, output):
    if output.exists():
        raise ValueError("new physical model receipt required")
    model = load_model_config(project / "config/models.yaml").generation["baseline"]
    endpoint = urlparse(model.endpoint)
    if endpoint.hostname != "127.0.0.1":
        raise ValueError("this lab uses the configured loopback baseline only")
    response = httpx.get(model.endpoint + "/models", timeout=15, trust_env=False)
    response.raise_for_status()
    identity = response.json()
    if model.served_name not in {row["id"] for row in identity["data"]}:
        raise ValueError("baseline service identity mismatch")
    socket = subprocess.check_output(["ss", "-ltnp", f"sport = :{endpoint.port}"], text=True)
    pid_match = re.search(r"pid=(\d+)", socket)
    if pid_match is None:
        raise ValueError("actual local serving process unavailable")
    pid = int(pid_match[1])
    command = [
        b.decode() for b in (Path("/proc") / str(pid) / "cmdline").read_bytes().split(b"\0") if b
    ]
    for i, value in enumerate(command):
        if value in {"--api-key", "--hf-token"} and i + 1 < len(command):
            command[i + 1] = "[redacted]"
    start_ticks = (Path("/proc") / str(pid) / "stat").read_text().split(") ", 1)[1].split()[19]
    files = sorted(
        p
        for p in model.path.rglob("*")
        if p.is_file() and p.suffix in {".safetensors", ".json", ".model"}
    )
    hashes = {}
    for path in files:
        hashes[str(path.relative_to(model.path))] = sha(path)
        print("pinned " + path.name, flush=True)
    if "config.json" not in hashes or not any(n.endswith(".safetensors") for n in hashes):
        raise ValueError("actual model weights/config missing")
    receipt = {
        "served_name": model.served_name,
        "endpoint": model.endpoint,
        "server_command": command,
        "server_pid": pid,
        "server_start_ticks": start_ticks,
        "models_response": identity,
        "model_files": hashes,
        "loopback_identity_probe_bypasses_proxy": True,
        "new_model_generation_requests": 0,
    }
    write(output, receipt)
    return receipt


def verify_model(project, receipt):
    model = load_model_config(project / "config/models.yaml").generation["baseline"]
    if receipt["served_name"] != model.served_name or receipt["endpoint"] != model.endpoint:
        raise ValueError("actual deployment receipt/config mismatch")
    required = {
        str(p.relative_to(model.path))
        for p in model.path.rglob("*")
        if p.is_file() and p.suffix in {".safetensors", ".json", ".model"}
    }
    if not required or not required.issubset(receipt["model_files"]):
        raise ValueError("all model weights/tokenizer/config must be pinned")
    for name, expected in receipt["model_files"].items():
        if (
            Path(name).is_absolute()
            or ".." in Path(name).parts
            or sha(model.path / name) != expected
        ):
            raise ValueError("actual deployment weight hash mismatch")
    response = httpx.get(model.endpoint + "/models", timeout=15, trust_env=False)
    response.raise_for_status()
    if model_identity(response.json()) != model_identity(receipt["models_response"]):
        raise ValueError("actual baseline model service changed")
    pid = receipt["server_pid"]
    stat = (Path("/proc") / str(pid) / "stat").read_text().split(") ", 1)[1].split()[19]
    socket = subprocess.check_output(
        ["ss", "-ltnp", f"sport = :{urlparse(model.endpoint).port}"], text=True
    )
    if stat != receipt["server_start_ticks"] or f"pid={pid}," not in socket:
        raise ValueError("actual baseline serving process changed")


def absent_reference(case_id):
    # Only the legacy scorer's case metadata interface; not a CaseGold, not persisted as Gold.
    # An empty reference cannot have a matching branch. All reference results are suppressed.
    return SimpleNamespace(
        case_id=case_id, reviewed=False, solvability="human_review", any_of=[], forbidden_actions=[]
    )


def run_calibration(
    project, dataset_root, output, receipt_file, *, client_factory=ObservedPlanClient, probe=True
):
    project, dataset_root, output = (p.resolve() for p in [project, dataset_root, output])
    if output.exists() or output.is_relative_to(dataset_root):
        raise ValueError("new calibration output outside original cases required")
    dataset = load_dataset(dataset_root)
    selected = sorted(
        (c for c in dataset["cases"] if c["manifest"].split == "validation"),
        key=lambda c: c["manifest"].case_id,
    )
    if not selected:
        raise ValueError("no validation cases; heldout is never a calibration fallback")
    receipt = read(receipt_file)
    if probe:
        verify_model(project, receipt)
    code = code_snapshot(project)
    code["files"]["scripts/v8_e1_calibration.py"] = sha(project / "scripts/v8_e1_calibration.py")
    code["sha256"] = digest(code["files"])
    output.mkdir(parents=True)
    frozen = output / "frozen-inputs"
    base = list(METHODS)
    random.Random(20261011).shuffle(base)
    case_receipts = []
    for i, item in enumerate(selected):
        name = item["manifest"].case_id
        shutil.copytree(item["visible"], frozen / name)
        case_receipts.append(
            {
                "case_id": name,
                "task": item["task"].model_dump(mode="json"),
                "source_group": item["manifest"].source_group,
                "structure_family": item["manifest"].structure_family,
                "method_order": base[i % 4 :] + base[: i % 4],
            }
        )
    input_hashes = {
        str(p.relative_to(frozen)): sha(p) for p in sorted(frozen.rglob("*")) if p.is_file()
    }
    write(
        output / "protocol.json",
        {
            "kind": "unreviewed-validation-engineering-only",
            "cases": case_receipts,
            "code": code,
            "model_receipt": receipt,
            "model_receipt_sha256": sha(receipt_file),
            "input_hashes": input_hashes,
            "reference_scoring_enabled": False,
            "formal_e1_completed": False,
            "heldout_consumed": False,
            "budget": {"tools": 8, "models": 8, "rounds": 3, "seconds": 180},
            "method_order": "seeded balanced Latin rotation",
            "model_inputs_exclude_organizer_truth": True,
        },
    )
    for name in code["files"]:
        target = output / "code" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(project / name, target)
    rows = []
    for item, meta in zip(selected, case_receipts, strict=True):
        case_id = meta["case_id"]
        for method in meta["method_order"]:
            folder = output / "runs" / case_id / f"method-{METHODS.index(method) + 1}"
            folder.mkdir(parents=True)
            try:
                row = run_method(
                    project,
                    frozen / case_id,
                    folder,
                    item["task"],
                    absent_reference(case_id),
                    method,
                    client_factory,
                    tools_factory=NormalizedEvidenceTools,
                    calibration_candidate=True,
                )
                cost = read(folder / "metrics.json")
                row.update(
                    model_attempts=cost["invocations"]["model"]["attempted"],
                    tool_attempts=cost["invocations"]["tool"]["attempted"],
                    input_tokens=cost["token_usage"]["input"],
                    output_tokens=cost["token_usage"]["output"],
                    runner_error=None,
                )
            except Exception as error:
                row = {
                    "case_id": case_id,
                    "method": method,
                    "parsed": False,
                    "validator_pass": False,
                    "hard_constraint_violation": None,
                    "runner_error": f"{type(error).__name__}:{error}",
                    "model_attempts": None,
                    "tool_attempts": None,
                    "input_tokens": None,
                    "output_tokens": None,
                }
                write(folder / "runner-error.json", row)
            row.update(
                reference_pass=None,
                vpr=None,
                branch=None,
                reviewed=False,
                solvability=None,
                reference_scoring_enabled=False,
                split="validation",
                evaluation_scope="unreviewed engineering calibration",
                source_group=meta["source_group"],
                structure_family=meta["structure_family"],
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
                            "model_attempts",
                            "runner_error",
                        ]
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
    fields = sorted(set().union(*(r.keys() for r in rows)))
    with (output / "metrics-by-case.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(
            {k: canonical(v) if isinstance(v, (dict, list, bool)) else v for k, v in row.items()}
            for row in rows
        )
    review_rows = []
    for row in rows:
        raw = (
            output
            / "runs"
            / row["case_id"]
            / f"method-{METHODS.index(row['method']) + 1}"
            / "raw-plan.txt"
        )
        for seat in [1, 2]:
            review_rows.append(
                {
                    "seat": seat,
                    "case_id": row["case_id"],
                    "method": row["method"],
                    "raw_plan_sha256": sha(raw) if raw.exists() else "",
                    "reference_sha256": "",
                    "reviewer": "",
                    "decision": "",
                    "review_source": "",
                    "notes": "",
                }
            )
    with (output / "empty-output-review-organizer-only.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=list(review_rows[0]))
        writer.writeheader()
        writer.writerows(review_rows)
    summaries = {
        method: {
            "planned_cases": len(selected),
            "recorded_runs": sum(r["method"] == method for r in rows),
            "parsed": sum(r["parsed"] for r in rows if r["method"] == method),
            "validator_pass": sum(r["validator_pass"] for r in rows if r["method"] == method),
            "formal_vpr": None,
            "reference_pass_count": None,
        }
        for method in METHODS
    }
    unchanged = all(
        sha(frozen / name) == expected for name, expected in input_hashes.items()
    ) and all(sha(project / name) == expected for name, expected in code["files"].items())
    result = {
        "cases": len(selected),
        "planned_method_runs": len(selected) * 4,
        "recorded_method_runs": len(rows),
        "summaries": summaries,
        "source_unchanged": unchanged,
        "new_model_attempts_known": sum(r["model_attempts"] or 0 for r in rows),
        "unknown_cost_runs": sum(r["model_attempts"] is None for r in rows),
        "runner_errors": sum(bool(r["runner_error"]) for r in rows),
        "reference_scoring_enabled": False,
        "formal_vpr": None,
        "formal_e1_completed": False,
        "heldout_consumed": False,
        "actual_human_review_records": 0,
        "real_network_writes": 0,
        "engineering_execution_completed": len(rows) == len(selected) * 4 and unchanged,
        "calibration_cannot_be_relabelled_as_formal_E1": True,
    }
    write(output / "summary.json", result)
    write(
        output / "sha256_manifest.json",
        {str(p.relative_to(output)): sha(p) for p in sorted(output.rglob("*")) if p.is_file()},
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare-model", "run"])
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dataset", type=Path, default=Path("eval/v8/e1"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--deployment", type=Path)
    args = parser.parse_args()
    if args.command == "prepare-model":
        receipt = prepare_model_receipt(args.project.resolve(), args.output)
        print(
            json.dumps(
                {
                    "served_name": receipt["served_name"],
                    "pinned_files": len(receipt["model_files"]),
                    "server_pid": receipt["server_pid"],
                }
            )
        )
    else:
        if args.deployment is None:
            parser.error("run requires actual --deployment receipt")
        print(
            json.dumps(
                run_calibration(args.project, args.dataset, args.output, args.deployment),
                ensure_ascii=False,
            )
        )
