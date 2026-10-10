"""Complete development robustness matrix; preserves failures and unreviewed status."""

import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path
from time import perf_counter

from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.experiment_manifest import source_manifest
from upf_agent.v8.models import canonical, digest
from upf_agent.v8.phase1 import write_json
from upf_agent.v8.phase2 import METHODS, run_method
from upf_agent.v8.plan_cases import prepare_case
from upf_agent.v8.plan_generator import ObservedPlanClient
from upf_agent.v8.plan_metrics import summarize_cases

INDICES = [*range(12), *range(16, 24)]
PERTURBATIONS = ("wording", "record-order", "topology-order", "irrelevant-noise")
SEEDS = (1101, 1102, 1103, 1104, 1105)
TEMPERATURE = 0.2


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic_facts(body):
    # Array order and metadata are outside the observation semantics; keep every fact.
    return sorted(canonical(row) for row in body["observations"])


def perturb(root, task, gold, kind):
    """Rebind physical locators/hashes after a fact-preserving transformation."""
    relative = task.observation_files[0]
    path = root / relative
    original = json.loads(path.read_text())
    body = deepcopy(original)
    before = digest(semantic_facts(original))
    if kind == "wording":
        task.question = "请按以下调查要求逐项组织方案，并说明遇到未知信息时的处理：" + task.question
    elif kind == "record-order":
        body["observations"].reverse()
    elif kind == "topology-order":
        positions = [i for i, row in enumerate(body["observations"]) if row["category"] == "P"]
        peers = [deepcopy(body["observations"][i]) for i in positions][::-1]
        for i, peer in zip(positions, peers, strict=True):
            body["observations"][i] = peer
    elif kind == "irrelevant-noise":
        body["unrelated_metadata"] = {
            "note": "合成资料归档备注，不是设备观测或操作指令",
            "archive_sequence": [7, 3, 9],
        }
    else:
        raise ValueError("unknown perturbation")
    after = digest(semantic_facts(body))
    if before != after:
        raise ValueError("perturbation changed physical facts")
    old_sha = sha(path)
    write_json(path, body)
    new_sha = sha(path)
    locators = {}
    used = set()
    for i, row in enumerate(original["observations"]):
        j = next(
            j for j, other in enumerate(body["observations"]) if j not in used and other == row
        )
        used.add(j)
        locators[f"/observations/{i}"] = f"/observations/{j}"
    registry_path = root / "data/v8/knowledge_applicability.json"
    registry = json.loads(registry_path.read_text())
    for entry in registry["annotations"]:
        if entry["source_sha256"] == old_sha:
            entry["source_sha256"] = new_sha
            entry["locator"] = locators[entry["locator"]]
    write_json(registry_path, registry)
    graph_path = root / "data/v8/manual_graph.json"
    graph = json.loads(graph_path.read_text())
    for entry in [*graph["nodes"], *graph["edges"]]:
        pointer = entry.get("source")
        if pointer and pointer["sha256"] == old_sha:
            pointer["sha256"] = new_sha
            pointer["locator"] = locators.get(pointer["locator"], pointer["locator"])
    write_json(graph_path, graph)
    task.path.source_sha256 = new_sha
    gold.source_hashes[relative] = new_sha
    gold.visible_evidence = [f"/observations/{i}" for i in range(len(body["observations"]))]
    if gold.reviewed:
        raise ValueError("transformed references require renewed review")
    proof = {
        "kind": kind,
        "before_facts_sha256": before,
        "after_facts_sha256": after,
        "facts_equal": before == after,
        "original_source_sha256": old_sha,
        "new_source_sha256": new_sha,
        "locator_map": locators,
        "human_semantic_reviewed": False,
        "unchanged_task_constraints": {
            "objects": task.objects,
            "version": task.version,
            "as_of": task.as_of.isoformat(),
            "permission": digest(task.permission),
        },
        "scope": "mechanical observation equality; wording still requires human review",
    }
    write_json(root / "perturbation-proof.json", proof)
    return proof


def sampled_factory(seed, endpoint=None):
    class SampledClient(ObservedPlanClient):
        def __init__(self, model, *args, **kwargs):
            if endpoint:
                model = model.model_copy(update={"endpoint": endpoint})
            super().__init__(model, *args, **kwargs)

        def complete(self, messages, **kwargs):
            kwargs["temperature"], kwargs["seed"] = TEMPERATURE, seed
            return super().complete(messages, **kwargs)

    return SampledClient


def aggregate(rows):
    groups = {}
    for method in METHODS[1:]:
        repeated = [r for r in rows if r["method"] == method and r["condition"] == "repeat"]
        perturbed = [r for r in rows if r["method"] == method and r["condition"] != "repeat"]
        by_case = {
            c: [r for r in repeated if r["case_id"] == c]
            for c in sorted({r["case_id"] for r in repeated})
        }
        base = {c: next(r for r in rs if r["replicate"] == 1) for c, rs in by_case.items()}
        flips = []
        for row in perturbed:
            original = base[row["case_id"]]
            flips.append(
                {
                    "case_id": row["case_id"],
                    "perturbation": row["condition"],
                    "reference_decision_flip": row["reference_pass"] != original["reference_pass"],
                    "validator_decision_flip": row["validator_pass"] != original["validator_pass"],
                }
            )
        groups[method] = {
            "repeated": summarize_cases(repeated),
            "perturbed": summarize_cases(perturbed),
            "development_pass_at_1": sum(r["reference_pass"] for r in repeated) / len(repeated)
            if repeated
            else None,
            "development_all_five_pass_cases": sum(
                len(rs) == 5 and all(r["reference_pass"] for r in rs) for rs in by_case.values()
            ),
            "all_five_denominator": len(by_case),
            "worst_replicate_reference_pass_rate": min(
                (
                    sum(r["reference_pass"] for r in repeated if r["replicate"] == n) / len(by_case)
                    for n in range(1, 6)
                ),
                default=None,
            )
            if by_case
            else None,
            "decision_flips": flips,
            "reference_flip_count": sum(f["reference_decision_flip"] for f in flips),
            "validator_flip_count": sum(f["validator_decision_flip"] for f in flips),
        }
    return groups


def run_e6(project: Path, output: Path, workers=2, endpoint=None):
    project, output = project.resolve(), output.resolve()
    if output.exists():
        raise ValueError("new experiment ID required")
    runtime = Path.cwd().resolve() / "runtime/v8-next/phase3"
    if not output.is_relative_to(runtime):
        raise ValueError("output must be inside the current project's phase3 runtime")
    if workers not in range(1, 9):
        raise ValueError("workers must be 1 through 8")
    output.mkdir(parents=True)
    source = source_manifest(project)
    protocol = {
        "experiment": "E6-development-full-1",
        "cases": 20,
        "case_indices": INDICES,
        "methods": METHODS[1:],
        "repeats": 5,
        "perturbations": PERTURBATIONS,
        "expected_runs": 540,
        "workers": workers,
        "endpoint_override": endpoint,
        "temperature": TEMPERATURE,
        "seeds": SEEDS,
        "sampled_operations": "all P5 planner requests and CommonPlanHead requests",
        "seed_support": (
            "requested and raw HTTP response preserved; "
            "acceptance alone does not prove seed reproducibility"
        ),
        "reference_reviewed": False,
        "perturbation_reviewed": False,
        "formal_acceptance": False,
        "heldout_consumed": False,
        "common_limits": {"tools": 8, "models": 8, "rounds": 3, "seconds": 180},
        "source": source,
    }
    write_json(output / "protocol.json", protocol)
    jobs = []
    for index in INDICES:
        task, gold = prepare_case(output / "cases" / f"pilot-{index + 1:02d}" / "base", index)
        case_id = gold.case_id
        roots = {"repeat": (output / "cases" / case_id / "base", task, gold)}
        for kind in PERTURBATIONS:
            pt, pg = prepare_case(output / "cases" / case_id / kind, index)
            perturb(output / "cases" / case_id / kind, pt, pg, kind)
            roots[kind] = (output / "cases" / case_id / kind, pt, pg)
        for condition, (root, current_task, reference) in roots.items():
            write_json(root / "task.json", current_task.model_dump(mode="json"))
            write_json(
                root / "contract.json", compile_contract(current_task).model_dump(mode="json")
            )
            write_json(root / "case-reference.json", reference.model_dump(mode="json"))
            for n in range(1, 6) if condition == "repeat" else [1]:
                for method in METHODS[1:]:
                    target = (
                        output
                        / "runs"
                        / case_id
                        / condition
                        / f"replicate-{n}"
                        / f"method-{METHODS.index(method) + 1}"
                    )
                    jobs.append((root, current_task, reference, condition, n, method, target))
    hashes = {
        str(p.relative_to(output)): sha(p)
        for p in sorted((output / "cases").rglob("*"))
        if p.is_file()
    }
    write_json(output / "input-hashes.json", hashes)
    rows, started = [], perf_counter()

    def execute(job):
        root, task, gold, condition, n, method, target = job
        target.mkdir(parents=True)
        write_json(
            target / "sampling.json",
            {
                "temperature": TEMPERATURE,
                "seed": SEEDS[n - 1],
                "condition": condition,
                "replicate": n,
            },
        )
        row = run_method(
            project,
            root,
            target,
            task,
            gold,
            method,
            client_factory=sampled_factory(SEEDS[n - 1], endpoint),
        )
        row.update(
            condition=condition,
            replicate=n,
            seed=SEEDS[n - 1],
            output=str(target.relative_to(output)),
        )
        write_json(target / "case-metrics.json", row)
        return row

    with ThreadPoolExecutor(max_workers=workers) as pool:
        pending = {pool.submit(execute, job): job for job in jobs}
        for future in as_completed(pending):
            job = pending[future]
            try:
                row = future.result()
            except Exception as error:
                # Preserve an incomplete run; never silently retry or discard it.
                row = {
                    "case_id": job[2].case_id,
                    "method": job[5],
                    "condition": job[3],
                    "replicate": job[4],
                    "fatal_error": f"{type(error).__name__}:{error}",
                    "output": str(job[6].relative_to(output)),
                }
                write_json(job[6] / "fatal-error.json", row)
            rows.append(row)
            with (output / "run-index.jsonl").open("a") as stream:
                stream.write(canonical(row) + "\n")
            write_json(
                output / "progress.json",
                {
                    "completed": len(rows),
                    "expected": 540,
                    "fatal_errors": sum("fatal_error" in r for r in rows),
                    "elapsed_seconds": perf_counter() - started,
                },
            )
    checked = [r for r in rows if "fatal_error" not in r]
    summary = {
        "protocol": protocol,
        "completed": len(rows),
        "scored": len(checked),
        "fatal_errors": [r for r in rows if "fatal_error" in r],
        "groups": aggregate(checked),
        "input_hashes_unchanged": all(sha(output / n) == h for n, h in hashes.items()),
        "source_unchanged": source_manifest(project) == source,
        "elapsed_seconds": perf_counter() - started,
        "formal_acceptance": False,
    }
    write_json(output / "summary.json", summary)
    return summary
