"""Read-only verification of the ordered delivery, original evidence and prior freeze."""

import argparse
import hashlib
import json
from pathlib import Path

from upf_agent.v8.experiment_manifest import source_manifest


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"missing physical file or path escape: {relative}")
    return path


def verify(project, delivery):
    project, delivery = project.resolve(), delivery.resolve()
    freeze = delivery / "delivery-freeze-001"
    manifest = read(freeze / "manifest.json")
    for relative, meta in manifest["files"].items():
        original = inside(project, relative)
        frozen = inside(freeze / "worktree", relative)
        if sha(original) != meta["sha256"] or sha(frozen) != meta["sha256"]:
            raise ValueError(f"delivery snapshot/current file mismatch: {relative}")
    artifacts = read(delivery / "sample-tables-002/artifact-index.json")
    for meta in artifacts.values():
        if sha(inside(project, meta["path"])) != meta["sha256"]:
            raise ValueError(f"original evidence mismatch: {meta['path']}")
    prior = (project / manifest["prior_freeze"]).resolve()
    if not prior.is_relative_to(project):
        raise ValueError("prior freeze path escape")
    previous = read(prior / "manifest.json")
    for relative, meta in previous["files"].items():
        if sha(inside(prior / "worktree", relative)) != meta["sha256"]:
            raise ValueError(f"prior frozen file mismatch: {relative}")
    core = source_manifest(project)["sha256"]
    if core != manifest["core_source_sha256"]:
        raise ValueError("core source changed")
    return {
        "delivery_frozen_and_current_files_verified": len(manifest["files"]),
        "original_evidence_files_verified": len(artifacts),
        "prior_frozen_files_verified": len(previous["files"]),
        "hash_mismatches": 0,
        "core_source_sha256": core,
        "delivery_manifest_sha256": sha(freeze / "manifest.json"),
        "prior_freeze_manifest_sha256": sha(prior / "manifest.json"),
        "prior_snapshot_does_not_need_to_match_new_plan": True,
        "new_model_calls": 0,
        "formal_e1_completed": False,
        "actual_double_review": False,
        "heldout_consumed": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--delivery", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.project, args.delivery), ensure_ascii=False, indent=2))
