"""Build and replay separately pinned synthetic and private E2 repair supplements."""

import argparse
import json
import shutil
import socket
from pathlib import Path

from v8_wp10_bundle import extract, pack, read, screen, sha, verify, write

SCRIPTS = [
    "v8_review_bundle.py",
    "v8_review_remediation.py",
    "v8_review_model_runs.py",
    "v8_review_materials.py",
    "v8_review_results.py",
    "v8_review_supplement_index.py",
    "v8_review_e3_runs.py",
    "v8_e7_diagnostic_audit.py",
    "v8_e8_domain.py",
    "v8_wp10_bundle.py",
    "v8_bundle_replay.py",
    "v8_phase3_matrix_review.py",
    "v8_e3_audit.py",
    "v8_e4_review.py",
    "v8_e2_supplement.py",
    "v8_e2_supplement_review.py",
]


def copy_tree(source, target, public):
    if source.is_file():
        screen(source, public)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        return
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if "__pycache__" in relative.parts or path.name == ".venv-retrieval":
            continue
        if path.is_symlink():
            raise ValueError(f"unapproved symlink: {relative}")
        if path.is_file():
            copy_tree(path, target / relative, public)


def build(project, output, specification):
    if output.exists():
        raise ValueError("new bundle output required")
    spec = read(specification)
    public = spec["kind"] == "synthetic"
    root = output / "bundle"
    root.mkdir(parents=True)
    for name in ["src", "pyproject.toml", "uv.lock", "config/models.yaml"]:
        copy_tree(project / name, root / name, public)
    for name in SCRIPTS:
        copy_tree(project / "scripts" / name, root / "scripts" / name, public)
    for dataset in spec["datasets"]:
        path = Path(dataset["project_relative"])
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("project-relative dataset required")
        copy_tree(project / path, root / "data" / dataset["name"], public)
    for index, relative in enumerate(spec.get("evidence", [])):
        copy_tree(
            project / relative, root / "evidence" / f"{index:02d}" / Path(relative).name, public
        )
    from upf_agent.v8.experiment_manifest import source_manifest

    write(root / "repair-protocol.json", spec)
    write(
        root / "provenance.json",
        {
            "source": source_manifest(project),
            "specification_sha256": sha(specification),
            "formal_acceptance": False,
            "human_approvals": 0,
            "old_bundles": spec["historical_bundles"],
            "old_bundle_payload_modified": False,
        },
    )
    files = {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob("*")) if p.is_file()}
    write(
        root / "bundle-manifest.json",
        {"schema": "review-repair-bundle-1", "kind": spec["kind"], "files": files},
    )
    count = verify(root)
    archive = output / f"review-repair-{spec['kind']}.tar.gz"
    pack(root, archive)
    result = {
        "files": count,
        "archive_sha256": sha(archive),
        "archive_bytes": archive.stat().st_size,
        "kind": spec["kind"],
        "formal_acceptance": False,
    }
    write(output / "bundle-summary.json", result)
    return result


def replay(root, output, denied):
    from v8_bundle_replay import install_guard

    from upf_agent.v8.experiment_manifest import source_manifest

    # Check before the guard, then import all evaluations exclusively from this relocated src.
    count = verify(root)
    import upf_agent.v8.models as imported

    assert Path(imported.__file__).resolve().is_relative_to(root.resolve() / "src")
    assert source_manifest(root) == read(root / "provenance.json")["source"]
    if output.exists() or not output.resolve().is_relative_to(root.resolve() / "runtime"):
        raise ValueError("new output inside relocated runtime required")
    output.mkdir(parents=True)
    guards = install_guard(denied)
    with socket.socket() as probe:
        try:
            probe.connect(("127.0.0.1", 1))
        except PermissionError:
            pass
        else:
            raise AssertionError("offline guard did not block connection")
    initial = dict(guards)
    from v8_e2_supplement_review import review as review_supplement
    from v8_e3_audit import audit as review_e3
    from v8_e4_review import review as review_e4
    from v8_e7_diagnostic_audit import audit as review_e7
    from v8_e8_domain import audit as review_e8
    from v8_phase3_matrix_review import review_e2, review_e5, review_e6
    from v8_review_remediation import audit_phase2, fresh_e5_source_checks

    operations = {
        "phase2": lambda p: audit_phase2(p),
        "E2": lambda p: review_e2(p),
        "E3": lambda p: review_e3(p, output / ("E3-" + p.name + ".json")),
        "E4": lambda p: review_e4(p, output / ("E4-" + p.name + ".json")),
        "E5": lambda p: review_e5(p),
        "E6": lambda p: review_e6(p),
        "source-E5": lambda p: fresh_e5_source_checks(p),
        "E7": lambda p: review_e7(p, output / ("E7-" + p.name + ".json")),
        "E8": lambda p: review_e8(p),
    }
    results = {}
    spec = read(root / "repair-protocol.json")
    for item in spec["datasets"]:
        if not item.get("audit"):
            continue
        path = root / "data" / item["name"]
        # SQLite audit readers can write SHM. Replay disposable verified copies.
        if item["audit"] == "E3":
            copied = output / "sqlite-working-copy" / item["name"]
            shutil.copytree(path, copied)
            path = copied
        result = operations[item["audit"]](path)
        results[item["name"]] = result
        write(output / f"audit-{item['name']}.json", result)
        if item["audit"] == "E5":
            checks = operations["source-E5"](path)
            write(output / "source-E5.json", checks)
        if item["audit"] == "E2":
            supplement = root / "data" / spec["e2_supplement_name"]
            results["E2_supplement"] = review_supplement(path, supplement)
            write(output / "E2-supplement.json", results["E2_supplement"])
    cpu_reexecution = {}
    if spec["kind"] == "synthetic":
        from upf_agent.v8.e3 import run_e3
        from upf_agent.v8.e4 import run_matrix
        from upf_agent.v8.e5_full import run_e5_full

        fresh_e3 = run_e3(root, output / "fresh-E3", shared_public_tools=True)
        fresh_e4 = run_matrix(root, output / "fresh-E4", "small", 1)
        fresh_e5 = run_e5_full(root, output / "fresh-E5")
        assert fresh_e3["pass"] and fresh_e4["pass"] and fresh_e5["engineering_pass"]
        cpu_reexecution = {
            "E3_runs": fresh_e3["runs"],
            "E4_method_batches": fresh_e4["method_batches"],
            "E5_decisions": fresh_e5["decisions"],
            "new_model_calls": 0,
        }
    assert verify(root) == count
    result = {
        "verified_files": count,
        "rechecked_files": count,
        "new_model_calls": 0,
        "human_reviews_imported": 0,
        "guard_activity": {k: guards[k] - initial[k] for k in guards},
        "datasets": {
            k: {
                "audit_pass": r.get("integrity_pass", r.get("audit_pass", r.get("pass", True))),
                "engineering_pass": r.get("engineering_pass"),
                "development_pass": r.get("development_pass"),
            }
            for k, r in results.items()
        },
        "source_unchanged": source_manifest(root) == read(root / "provenance.json")["source"],
        "formal_acceptance": False,
        "fresh_cpu_reexecution": cpu_reexecution,
    }
    assert all(r["audit_pass"] for r in result["datasets"].values())
    assert all(
        result["guard_activity"][k] == 0
        for k in ["blocked_connections", "blocked_original_reads", "blocked_processes"]
    )
    write(output / "replay-summary.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["build", "extract", "replay"])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--spec", type=Path)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--deny-root", type=Path, action="append", default=[])
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    if args.action == "build":
        result = build(project, args.output, args.spec)
    elif args.action == "extract":
        result = {"files": extract(args.archive, args.output)}
    else:
        result = replay(project, args.output, args.deny_root)
    print(json.dumps(result, ensure_ascii=False))
