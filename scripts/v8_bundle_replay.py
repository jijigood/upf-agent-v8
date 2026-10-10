"""Verify and replay a relocated WP10 bundle, with network access disabled."""

import argparse
import json
import os
import shutil
import socket
import sys
from pathlib import Path
from urllib.parse import unquote

from v8_wp10_bundle import read, verify, write


def install_guard(denied_roots):
    """Python audit guard for accidental external reads/calls, not an OS sandbox."""
    roots = [p.resolve() for p in denied_roots]
    counts = {
        "blocked_connections": 0,
        "blocked_original_reads": 0,
        "blocked_processes": 0,
        "allowed_metadata_processes": 0,
    }

    def guard(event, args):
        if event == "socket.connect":
            counts["blocked_connections"] += 1
            raise PermissionError("WP10 offline replay: socket connection denied")
        if event in {"subprocess.Popen", "os.system", "os.exec", "os.posix_spawn"}:
            # platform.platform() uses this exact standard-library query on Linux.
            # It reads kernel CPU metadata, with no file/model/network arguments.
            if (
                event == "subprocess.Popen"
                and args[0] == "uname"
                and args[1] == ["uname", "-p"]
                and shutil.which("uname") == "/usr/bin/uname"
                and args[2] is None
                and args[3] is None
            ):
                counts["allowed_metadata_processes"] += 1
                return
            counts["blocked_processes"] += 1
            raise PermissionError("WP10 offline replay: child process denied")
        if event not in {"open", "os.listdir", "os.scandir", "sqlite3.connect"} or not args:
            return
        value = args[0]
        if not isinstance(value, (str, bytes, os.PathLike)):
            return
        name = os.fsdecode(value)
        if name.startswith("file:"):
            name = unquote(name[5:].split("?", 1)[0])
        path = Path(name).resolve()
        if any(path.is_relative_to(root) for root in roots):
            counts["blocked_original_reads"] += 1
            raise PermissionError("WP10 relocated replay: original directory read denied")
        if str(path).startswith("/dev/nvidia"):
            raise PermissionError("WP10 CPU replay: GPU device denied")

    sys.addaudithook(guard)
    return counts


def replay(root, output, fresh_cpu=False, denied_roots=()):
    root, output = root.resolve(), output.resolve()
    if output.exists() or not output.is_relative_to(root / "runtime"):
        raise ValueError("choose a new output inside this bundle's runtime directory")
    if fresh_cpu and not output.is_relative_to(root / "runtime/v8-next/phase3"):
        raise ValueError("fresh CPU output must belong to runtime/v8-next/phase3")
    if any(root.is_relative_to(p.resolve()) for p in denied_roots):
        raise ValueError("bundle root cannot itself be denied")
    checked = verify(root)
    manifest = read(root / "bundle-manifest.json")
    if manifest["kind"] != "synthetic" and fresh_cpu:
        raise ValueError("fresh CPU controls apply only to synthetic bundle")
    output.mkdir(parents=True)
    guard_counts = install_guard(denied_roots)
    # Prove the guard works before reading datasets; subtract these intentional probes
    # from the experiment counters. No connection reaches the network.
    with socket.socket() as probe:
        try:
            probe.connect(("127.0.0.1", 1))
        except PermissionError:
            pass
        else:
            raise AssertionError("offline guard failed")
    for path in denied_roots:
        try:
            (path / "pyproject.toml").read_bytes()
        except PermissionError:
            pass
        else:
            raise AssertionError("original-root guard failed")
    self_probes = dict(guard_counts)
    import upf_agent
    from upf_agent.v8.experiment_manifest import source_manifest

    imported_source = Path(upf_agent.__file__).resolve()
    if not imported_source.is_relative_to(root / "src/upf_agent"):
        raise ValueError("imported original/foreign editable package")
    assert source_manifest(root) == manifest["original_code_source"]
    historical_sources = read(root / "provenance.json")["historical_sources"]
    for label, expected in historical_sources.items():
        assert source_manifest(root / "history/code" / label) == expected
    from v8_phase3_matrix_review import review_e2, review_e5, review_e6

    results = {}
    if manifest["kind"] == "private-e2":
        from v8_e2_supplement_review import review as supplement_review

        batch = root / "data/phase3/e2-full-003"
        results["E2"] = review_e2(batch, root / "data/phase3/e2-original-seed-cache")
        results["E2_supplement"] = supplement_review(
            batch, root / "data/phase3/e2-mixed-pilot-and-sensitivity-003"
        )
        for key, result in results.items():
            write(output / f"{key}.json", result)
    else:
        from v8_e3_audit import audit as e3_audit
        from v8_e4_review import review as e4_review
        from v8_phase2_audit import audit as phase2_audit
        from v8_phase2_reference_revision import revise_batch

        phase2 = root / "data/phase2"
        phase3 = root / "data/phase3"
        results["phase2"] = phase2_audit(
            phase2 / "closure-full-004", phase2 / "pilot-final-001", output / "phase2.json"
        )
        # The legacy auditor signals integrity failures by raising and has no pass field.
        results["phase2"]["pass"] = results["phase2"]["runs_recomputed"] == 96
        results["phase2_revision"] = revise_batch(
            root,
            phase2 / "closure-full-004",
            output / "reference-recomputed",
            phase2 / "reference-revision-002/supplied-audit-summary.json",
        )
        for path in (phase2 / "reference-revision-002/cases").glob("*/case-reference.json"):
            assert (
                path.read_bytes()
                == (
                    output / "reference-recomputed/cases" / path.parent.name / path.name
                ).read_bytes()
            )
        for name in ["metrics-by-case.jsonl", "reference-negative-controls.json"]:
            assert read_records(phase2 / "reference-revision-002" / name) == read_records(
                output / "reference-recomputed" / name
            )
        # SQLite readers can create/change WAL/SHM. Use a disposable, byte-identical copy;
        # the originals and their frozen receipts are verified again afterwards.
        e3_copy = output / "sqlite-working-copy/e3"
        shutil.copytree(phase3 / "e3-public-four-methods-002", e3_copy)
        results["E3"] = e3_audit(e3_copy, output / "E3.json")
        results["E4"] = e4_review(phase3 / "e4-full-single-001", output / "E4.json")
        results["E5"] = review_e5(phase3 / "e5-full-002")
        results["E6"] = review_e6(phase3 / "e6-full-002")
        for key in ["E5", "E6"]:
            write(output / f"{key}.json", results[key])
        catalog = read(root / "failure-catalog.json")
        for item in catalog["items"]:
            assert (root / item["payload"]).exists()
        old_audit = read(root / "data/phase3/e3-four-methods-audit-002.json")
        assert not old_audit["pass"] and old_audit["runs"] == 128
        interruption = read(root / "data/phase3/e6-full-001-interruption.json")
        assert interruption["progress"]["completed"] == 27
        assert len(interruption["pending_runs"]) == 2
        results["history"] = {
            "catalog_items": len(catalog["items"]),
            "old_E3_failure_preserved": True,
            "E6_interrupted_completed": 27,
            "E6_pending": 2,
            "merged_into_final_denominator": False,
            "pass": True,
        }
    fresh = {}
    if fresh_cpu:
        from v8_requirement_graph_engine_probe import run as engine_probe

        from upf_agent.v8.e3 import run_e3
        from upf_agent.v8.e4 import run_matrix
        from upf_agent.v8.e5_full import run_e5_full
        from upf_agent.v8.wp08 import run_wp08

        fresh_root = output / "fresh-cpu"
        operations = [
            ("graph", lambda: run_wp08(root, fresh_root / "graph")),
            ("engine", lambda: engine_probe(root, fresh_root / "engine")),
            ("E3", lambda: run_e3(root, fresh_root / "e3", shared_public_tools=True)),
            ("E4", lambda: run_matrix(root, fresh_root / "e4", "small", workers=1)),
            ("E5", lambda: run_e5_full(root, fresh_root / "e5")),
        ]
        for key, operation in operations:
            print(f"fresh CPU {key}: start", flush=True)
            result = operation()
            passed = result.get("pass", result.get("engineering_pass", False))
            fresh[key] = {"pass": passed}
            if not passed:
                raise AssertionError(f"fresh CPU {key} failed")
            print(f"fresh CPU {key}: pass", flush=True)
        graph = read(fresh_root / "graph/summary.json")
        e3 = read(fresh_root / "e3/summary.json")
        e4 = read(fresh_root / "e4/summary.json")
        e5 = read(fresh_root / "e5/summary.json")
        assert graph["method_runs"] == 72 and graph["model_calls"] == 0
        assert e3["runs"] == 96 and not e3["native_p5_enabled"]
        assert sum(r["model_calls"] for r in e3["per_method"].values()) == 0
        assert e4["method_batches"] == 720 and e4["model_calls"] == 0
        assert e5["decisions"] == 720
        fresh["counts"] = {
            "graph_controls": 72,
            "engine_ledger_runs": 3,
            "E3_runs": 96,
            "E4_method_batches": 720,
            "E5_decisions": 720,
            "new_model_calls": 0,
            "new_independent_samples_claimed": False,
        }
        results["fresh_E3_audit"] = e3_audit(fresh_root / "e3", output / "fresh-E3-audit.json")
        results["fresh_E5_audit"] = review_e5(fresh_root / "e5")
        write(output / "fresh-E5-audit.json", results["fresh_E5_audit"])
    rechecked = verify(root)
    experiment_guard = {key: value - self_probes[key] for key, value in guard_counts.items()}
    passed = all(r.get("pass", False) for r in results.values()) and not any(
        experiment_guard[key]
        for key in ["blocked_connections", "blocked_original_reads", "blocked_processes"]
    )
    report = {
        "schema": "wp10-relocated-replay-1",
        "kind": manifest["kind"],
        "bundle_root": str(root),
        "imported_source": str(imported_source),
        "historical_source_hashes_verified": {
            label: expected["sha256"] for label, expected in historical_sources.items()
        },
        "files_verified_before": checked,
        "files_verified_after": rechecked,
        "original_files_unchanged": checked == rechecked,
        "network_guard": True,
        "guard_self_probes": self_probes,
        "experiment_guard_events": experiment_guard,
        "guard_scope": "Python audit events; not an OS sandbox",
        "allowed_process": "exact standard-library uname -p kernel metadata query only",
        "denied_roots": [str(p) for p in denied_roots],
        "new_model_calls": 0,
        "human_reviews_imported": 0,
        "formal_acceptance": False,
        "heldout_consumed": False,
        "results": results,
        "fresh": fresh,
        "pass": passed,
    }
    write(output / "summary.json", report)
    print(json.dumps({k: v for k, v in report.items() if k not in {"results", "fresh"}}))
    return report


def read_records(path):
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in path.read_text().splitlines()]
    return read(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fresh-cpu", action="store_true")
    parser.add_argument("--deny-root", type=Path, action="append", default=[])
    args = parser.parse_args()
    result = replay(
        Path(__file__).resolve().parents[1], args.output, args.fresh_cpu, args.deny_root
    )
    raise SystemExit(0 if result["pass"] else 1)
