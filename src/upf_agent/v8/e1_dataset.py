"""File-backed E1 cases: visible sources, independent references and real review receipts."""

import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Literal

from pydantic import Field

from upf_agent.agent_contracts import AgentBudget
from upf_agent.v8.models import Model, OrchestrationTask, digest
from upf_agent.v8.plan_ir import CaseGold
from upf_agent.v8.plan_review import GoldReview, apply_reviews, calibration_report, validate_splits

SPLIT_FOLDERS = {"dev": "development", "validation": "validation", "heldout": "heldout"}
SCALES = {
    60: {"dev": 24, "validation": 12, "heldout": 24},
    150: {"dev": 60, "validation": 30, "heldout": 60},
}


def sha(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def inside(root, relative, *, directory=False):
    if Path(relative).is_absolute():
        raise ValueError("dataset paths must be relative")
    path = (root / relative).resolve(strict=True)
    if not path.is_relative_to(root.resolve()) or not (
        path.is_dir() if directory else path.is_file()
    ):
        raise ValueError("dataset source path escape or wrong file kind")
    return path


class CaseManifest(Model):
    schema_version: Literal["v8-e1-file-case-1"] = "v8-e1-file-case-1"
    case_id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]{0,79}$")
    split: Literal["dev", "validation", "heldout"]
    visible_root: str
    task_file: str
    reference_file: str | None = None
    source_group: str = Field(min_length=1)
    structure_family: str = Field(min_length=1)
    source_kind: Literal[
        "legacy-development", "experimental-injection", "manual-log", "benchmark", "new-synthetic"
    ]
    previously_evaluated: bool
    raw_source_hashes: dict[str, str] = Field(default_factory=dict)
    provenance_file: str


class DatasetIndex(Model):
    schema_version: Literal["v8-e1-file-dataset-1"] = "v8-e1-file-dataset-1"
    cases: list[str]
    reviews_file: str = "reviews/received-reviews.json"
    history_file: str = "history-index.json"
    status: Literal["draft"] = "draft"


def components(cases):
    parent = {c["manifest"].case_id: c["manifest"].case_id for c in cases}

    def find(key):
        while parent[key] != key:
            parent[key] = parent[parent[key]]
            key = parent[key]
        return key

    labels = {}
    for case in cases:
        manifest = case["manifest"]
        for field in ["source_group", "structure_family"]:
            key = (field, getattr(manifest, field))
            if key in labels:
                parent[find(manifest.case_id)] = find(labels[key])
            labels[key] = manifest.case_id
    groups = defaultdict(list)
    for case_id in parent:
        groups[find(case_id)].append(case_id)
    return sorted(sorted(ids) for ids in groups.values())


def load_dataset(root):
    root = root.resolve()
    index = DatasetIndex.model_validate(read(root / "dataset.json"))
    if len(index.cases) != len(set(index.cases)):
        raise ValueError("duplicate case manifest path")
    files = {"dataset.json": sha(root / "dataset.json")}

    def pin(path):
        files[str(path.relative_to(root))] = sha(path)

    review_file = inside(root, index.reviews_file)
    history_path = inside(root, index.history_file)
    history = read(history_path)
    pin(history_path)
    records = [GoldReview.model_validate(row) for row in read(review_file)]
    pin(review_file)
    keys = [(r.case_id, r.reviewer.strip().casefold()) for r in records]
    if len(keys) != len(set(keys)) or any(not identity for _, identity in keys):
        raise ValueError("duplicate or blank reviewer identity")
    for record in records:
        source = inside(root, record.review_source)
        if not source.is_relative_to(root / "reviews"):
            raise ValueError("review receipts must remain outside visible cases, inside reviews")
        pin(source)
    cases, ids = [], set()
    for relative in index.cases:
        path = inside(root, relative)
        manifest = CaseManifest.model_validate(read(path))
        if manifest.case_id in ids:
            raise ValueError("duplicate case ID")
        ids.add(manifest.case_id)
        if Path(relative).parts[0] != SPLIT_FOLDERS[manifest.split]:
            raise ValueError("case split and directory disagree")
        if manifest.source_kind == "legacy-development" and manifest.split != "dev":
            raise ValueError("legacy development cannot be reassigned to formal splits")
        if manifest.split != "dev" and manifest.structure_family in history["structure_families"]:
            raise ValueError("known development/E7 family cannot be renamed into a new split")
        pin(path)
        visible = inside(root, manifest.visible_root, directory=True)
        if (root / "gold").resolve().is_relative_to(visible):
            raise ValueError("Gold cannot be inside visible root")
        for entry in visible.rglob("*"):
            if entry.is_symlink():
                raise ValueError("visible source symlinks are not permitted")
            if entry.is_file():
                if re.search(r"(^|[-_.])(gold|truth|private|reference)([-_.]|$)", entry.name, re.I):
                    raise ValueError("organizer reference/truth cannot enter visible sources")
                pin(entry)
        task_path = inside(root, manifest.task_file)
        if not task_path.is_relative_to(visible):
            raise ValueError("task must be inside visible root")
        task = OrchestrationTask.model_validate(read(task_path))
        if (
            task.budget != AgentBudget()
            or task.model_enabled
            or task.graph_backend != "memory"
            or task.retrieval_device != "cpu"
            or task.model_profile != "baseline"
            or task.interrupt_before_collect
        ):
            raise ValueError("four-method common 8/8/3/180 budget and offline MemoryGraph required")
        if task.permission.execute or set(task.permission.objects) != set(task.objects):
            raise ValueError("case requires exact declared read-only scope")
        if not task.observation_files:
            raise ValueError("normal visible observations required")
        for source in task.observation_files:
            observation = inside(visible, source)
            if not observation.is_relative_to(visible / "data"):
                raise ValueError("observations must be inside visible data")
            body = read(observation)
            if body.get("synthetic") is not task.synthetic:
                raise ValueError("task/observation provenance mismatch")
            forbidden = {"any_of", "root_cause_truth", "expected_answer", "reference_pass", "vpr"}

            def guard(value, forbidden=forbidden):
                if isinstance(value, dict):
                    if forbidden.intersection(value):
                        raise ValueError("organizer answers found in normal observations")
                    for item in value.values():
                        guard(item)
                elif isinstance(value, list):
                    for item in value:
                        guard(item)

            guard(body)
            if manifest.split != "dev" and sha(observation) in history["visible_source_hashes"]:
                raise ValueError("previously evaluated normal source reused in formal split")
        for source, expected in manifest.raw_source_hashes.items():
            if sha(inside(visible, source)) != expected:
                raise ValueError("raw physical source hash mismatch")
            if manifest.split != "dev" and expected in history["visible_source_hashes"]:
                raise ValueError("previously evaluated raw capture reused in formal split")
        pin(inside(root, manifest.provenance_file))
        gold = None
        approved = None
        if manifest.reference_file:
            gold_path = inside(root, manifest.reference_file)
            if gold_path.is_relative_to(visible):
                raise ValueError("Gold cannot be visible to model")
            pin(gold_path)
            gold = CaseGold.model_validate(read(gold_path))
            for field in ["case_id", "split", "source_group", "structure_family"]:
                if getattr(gold, field) != getattr(manifest, field):
                    raise ValueError("case manifest/reference mismatch")
            if (
                gold.objects != task.objects
                or gold.as_of != task.as_of
                or gold.version != task.version
                or gold.synthetic != task.synthetic
                or gold.permission_fingerprint != digest(task.permission)
            ):
                raise ValueError("reference/task scope, version, time or provenance mismatch")
            if not gold.source_hashes or any(
                source not in gold.source_hashes for source in task.observation_files
            ):
                raise ValueError("reference must pin every normal observation")
            for source, expected in gold.source_hashes.items():
                if sha(inside(visible, source)) != expected:
                    raise ValueError("Gold physical source hash mismatch")
            pair = [r for r in records if r.case_id == manifest.case_id]
            if any(r.reference_sha256 != digest(gold) for r in pair):
                raise ValueError("review reference hash mismatch")
            try:
                approved = apply_reviews(gold, pair)
            except ValueError:
                pass
        cases.append(
            {
                "manifest": manifest,
                "visible": visible,
                "task": task,
                "gold": gold,
                "approved": approved,
            }
        )
    if set(r.case_id for r in records) - ids:
        raise ValueError("review refers to a case outside this dataset")
    validate_splits([c["manifest"] for c in cases])
    # Identical physical observation blobs cannot be renamed into another split.
    seen = defaultdict(set)
    for case in cases:
        for name in case["task"].observation_files:
            seen[sha(case["visible"] / name)].add(case["manifest"].split)
        for value in case["manifest"].raw_source_hashes.values():
            seen[value].add(case["manifest"].split)
    if any(len(splits) > 1 for splits in seen.values()):
        raise ValueError("identical normal raw source crosses splits")
    return {"root": root, "cases": cases, "files": files, "reviews": records}


def readiness(dataset, scale=60):
    cases = dataset["cases"]
    counts = Counter(c["manifest"].split for c in cases)
    problems = []
    for split, minimum in SCALES[scale].items():
        if counts[split] != minimum:
            problems.append(f"split_count:{split}:{counts[split]}:required:{minimum}")
    missing = [c["manifest"].case_id for c in cases if c["gold"] is None]
    unapproved = [c["manifest"].case_id for c in cases if c["approved"] is None]
    reused = [
        c["manifest"].case_id
        for c in cases
        if c["manifest"].split != "dev" and c["manifest"].previously_evaluated
    ]
    if missing:
        problems.append("missing_independent_reference")
    if unapproved:
        problems.append("missing_hash_bound_real_double_reviews")
    if reused:
        problems.append("nondevelopment_cases_previously_evaluated")
    return {
        "scale": scale,
        "case_count": len(cases),
        "split_counts": dict(counts),
        "source_structure_components": components(cases),
        "missing_references": missing,
        "unapproved_cases": unapproved,
        "reused_nondevelopment_cases": reused,
        "actual_review_records": len(dataset["reviews"]),
        "hash_bound_approved_gold": len(cases) - len(unapproved),
        "calibration": calibration_report(dataset["reviews"]),
        "problems": problems,
        "data_ready": not problems,
        "formal_e1_completed": False,
        "heldout_consumed": False,
        "formal_vpr": None,
        "review_independence_is_a_human_fact": True,
    }


def initialize(project, root, legacy):
    project, root, legacy = project.resolve(), root.resolve(), legacy.resolve()
    if root.exists():
        raise ValueError("new E1 dataset directory required")
    entries = []
    for original in sorted(legacy.glob("*/case-reference.json")):
        gold = CaseGold.model_validate(read(original))
        if gold.split != "dev" or gold.reviewed:
            raise ValueError("legacy intake only imports unapproved development drafts")
        folder = root / "development" / gold.case_id
        visible = folder / "visible"
        visible.mkdir(parents=True)
        shutil.copytree(original.parent / "data", visible / "data")
        shutil.copy2(original.parent / "case-task.json", visible / "case-task.json")
        reference = f"gold/development/{gold.case_id}.json"
        write(root / reference, gold.model_dump(mode="json"))
        provenance = f"gold/provenance/{gold.case_id}.json"
        write(
            root / provenance,
            {
                "source_kind": "legacy-development",
                "previously_evaluated": True,
                "original_bundle": str(original.parent.relative_to(project)),
                "original_reference_sha256": sha(original),
            },
        )
        manifest = CaseManifest(
            case_id=gold.case_id,
            split="dev",
            visible_root=str(visible.relative_to(root)),
            task_file=str((visible / "case-task.json").relative_to(root)),
            reference_file=reference,
            source_group=gold.source_group,
            structure_family=gold.structure_family,
            source_kind="legacy-development",
            previously_evaluated=True,
            provenance_file=provenance,
        )
        entry = str((folder / "case.json").relative_to(root))
        write(root / entry, manifest.model_dump(mode="json"))
        entries.append(entry)
    if not entries:
        raise ValueError("no legacy development cases supplied")
    for folder in ["validation", "heldout", "gold/validation", "gold/heldout", "reviews/records"]:
        (root / folder).mkdir(parents=True, exist_ok=True)
        (root / folder / ".gitkeep").write_text("")
    write(root / "reviews/received-reviews.json", [])
    history_hashes, history_families = set(), set()
    for name in entries:
        entry = CaseManifest.model_validate(read(root / name))
        gold = CaseGold.model_validate(read(root / entry.reference_file))
        history_hashes.update(gold.source_hashes.values())
        history_families.add(gold.structure_family)
    for pattern in [
        "wp11/e7-diagnostic-*/rounds/*/input/snapshot.json",
        "remaining-experiments-20261010/e7-*/rounds/*/input/snapshot.json",
    ]:
        for path in (project / "runtime/v8-next").glob(pattern):
            history_hashes.add(sha(path))
    for path in (project / "runtime/v8-next/remaining-experiments-20261010").glob(
        "e7-*/protocol.json"
    ):
        history_families.update(read(path).get("conditions", []))
    write(
        root / "history-index.json",
        {
            "visible_source_hashes": sorted(history_hashes),
            "structure_families": sorted(history_families),
            "scope": (
                "known development observations and already used E7 captures/families; "
                "metadata novelty still needs human review"
            ),
        },
    )
    write(root / "dataset.json", DatasetIndex(cases=entries).model_dump(mode="json"))
    for name, model in [
        ("case-manifest", CaseManifest),
        ("dataset", DatasetIndex),
        ("case-gold", CaseGold),
        ("gold-review", GoldReview),
        ("task", OrchestrationTask),
    ]:
        write(root / "schemas" / f"{name}.schema.json", model.model_json_schema())
    return readiness(load_dataset(root))
