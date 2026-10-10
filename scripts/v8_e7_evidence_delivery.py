"""Local E7 supplement bundle and blank real-review seats; no external publication."""

import argparse
import csv
import hashlib
import json
import shutil
import tarfile
from pathlib import Path

from upf_agent.v8.experiment_manifest import source_manifest


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def reviews(datasets, output):
    if output.exists():
        raise ValueError("fresh review export required")
    public = output / "public"
    public.mkdir(parents=True)
    index, source_map = [], []
    for dataset in datasets:
        summary = json.loads((dataset / "summary.json").read_text())
        if not summary["pass"]:
            raise ValueError("export only finalized engineering-passing batches")
        for row in summary["rows"]:
            source = dataset / "rounds" / f"round-{row['round']:03}"
            item_id = hashlib.sha256(
                (dataset.name + ":" + sha(source / "input/snapshot.json")).encode()
            ).hexdigest()[:20]
            target = public / ("case-" + item_id)
            target.mkdir()
            pairs = [(source / "input/snapshot.json", target / "snapshot.json")]
            pairs += [
                (source / "agent" / f"{mode}.json", target / f"{mode}-report.json")
                for mode in ("flat", "joined", "graph")
            ]
            for a, b in pairs:
                shutil.copyfile(a, b)
                if sha(a) != sha(b):
                    raise ValueError("review copy changed bytes")
            file_hashes = {str(b.relative_to(public)): sha(b) for _, b in pairs}
            material_sha = hashlib.sha256(
                json.dumps(file_hashes, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()
            index.append(
                {
                    "item_id": item_id,
                    "snapshot": str((target / "snapshot.json").relative_to(public)),
                    "files": file_hashes,
                    "material_sha256": material_sha,
                    "synthetic": False,
                    "reviewed": False,
                }
            )
            source_map.append(
                {
                    "item_id": item_id,
                    "dataset": str(dataset),
                    "round": row["round"],
                    "condition": row["condition"],
                }
            )
    write(public / "input-index.json", index)
    write(output / "organizer-only/source-map.json", source_map)
    fields = [
        "item_id",
        "input_sha256",
        "material_sha256",
        "reviewer",
        "reviewed_at",
        "decision",
        "evidence_locations",
        "rationale",
        "review_source",
    ]
    for seat in (1, 2):
        with (public / f"reviewer-{seat}.csv").open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(
                {
                    "item_id": r["item_id"],
                    "input_sha256": r["files"][r["snapshot"]],
                    "material_sha256": r["material_sha256"],
                }
                for r in index
            )
    hashes = {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()}
    write(output / "sha256_manifest.json", hashes)
    result = {
        "records_per_seat": len(index),
        "reviewers_recorded": 0,
        "formal_quality": False,
        "scope": "copied normal inputs/outputs; not anonymous; first pass withholds truth",
    }
    write(output / "summary.json", result)
    return result


def bundle(project, datasets, extras, output):
    if output.exists():
        raise ValueError("fresh bundle output required")
    package = output / "package"
    package.mkdir(parents=True)
    for path in (project / "src/upf_agent").rglob("*.py"):
        target = package / path.relative_to(project)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    for name in ("pyproject.toml", "uv.lock"):
        shutil.copyfile(project / name, package / name)
    for path in (project / "scripts").glob("v8_e7*.py"):
        target = package / "scripts" / path.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    for name in ("v8_formal_readiness.py", "v8_bundle_replay.py", "v8_wp10_bundle.py"):
        shutil.copyfile(project / "scripts" / name, package / "scripts" / name)
    for dataset in datasets:
        shutil.copytree(
            dataset,
            package / "datasets" / dataset.name,
            ignore=shutil.ignore_patterns("__pycache__"),
        )
    for extra in extras:
        if extra.is_symlink():
            raise ValueError("no linked supplementary source")
        target = package / "supplements" / extra.name
        if extra.is_dir():
            shutil.copytree(extra, target, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(extra, target)
    files = {str(p.relative_to(package)): sha(p) for p in package.rglob("*") if p.is_file()}
    write(
        package / "bundle-manifest.json",
        {
            "schema": "e7-evidence-local-supplement-1",
            "files": files,
            "core_source": source_manifest(project),
            "private_truth_included": True,
            "formal_quality": False,
            "external_publication": False,
        },
    )
    archive = output / "e7-evidence-local-supplement.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(
            package,
            arcname="package",
            filter=lambda info: None if "__pycache__" in info.name else info,
        )
    result = {
        "archive": str(archive),
        "archive_sha256": sha(archive),
        "archive_bytes": archive.stat().st_size,
        "files": len(files),
        "manifest_sha256": sha(package / "bundle-manifest.json"),
        "formal_quality": False,
        "private_local_only": True,
    }
    write(output / "summary.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["reviews", "bundle"])
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--datasets", type=Path, nargs="+", required=True)
    parser.add_argument("--extras", type=Path, nargs="*", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = (
        reviews(args.datasets, args.output)
        if args.operation == "reviews"
        else bundle(args.project, args.datasets, args.extras, args.output)
    )
    print(json.dumps(result))
