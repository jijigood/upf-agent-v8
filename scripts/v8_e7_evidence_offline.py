"""Relocated CPU-only replay of finite E7 evidence bundles, without network or original reads."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

from v8_bundle_replay import install_guard
from v8_e7_evidence_audit import audit
from v8_e7_session_mapping import run as mapping_run

from upf_agent.v8.experiment_manifest import source_manifest


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root, output, deny):
    if output.exists() or not output.resolve().is_relative_to((root / "runtime").resolve()):
        raise ValueError("fresh relocated runtime output required")
    manifest = json.loads((root / "bundle-manifest.json").read_text())
    if any(sha(root / name) != expected for name, expected in manifest["files"].items()):
        raise ValueError("bundle SHA mismatch")
    import upf_agent

    if not Path(upf_agent.__file__).resolve().is_relative_to(root / "src"):
        raise ValueError("must import relocated core source")
    counters = install_guard(deny)
    if source_manifest(root) != manifest["core_source"]:
        raise ValueError("wrong core source")
    output.mkdir(parents=True)
    results = []
    for dataset in sorted((root / "datasets").iterdir()):
        replay = audit(dataset, output / (dataset.name + "-audit"))
        mapping = mapping_run(dataset, output / (dataset.name + "-mapping"))
        original_audits = [
            p
            for p in (root / "supplements").glob("*/summary.json")
            if json.loads(p.read_text()).get("dataset", "").endswith(dataset.name)
        ]
        matches = []
        for path in original_audits:
            original = json.loads(path.read_text())
            matches.append(
                all(
                    replay[key] == original[key]
                    for key in (
                        "metrics",
                        "comparisons",
                        "per_round_checks",
                        "pfcp_observed_establishment_pairs",
                        "truncated_packets",
                        "pfcp_decode_errors",
                        "pass",
                    )
                )
            )
        mapping_baselines = [
            p
            for p in (root / "supplements").glob("*/summary.json")
            if "mapping" in p.parent.name
            and json.loads(p.read_text()).get("rounds") == mapping["rounds"]
        ]
        mapping_matches = []
        for path in mapping_baselines:
            original = json.loads(path.read_text())
            mapping_matches.append(
                all(
                    original[k] == mapping[k]
                    for k in (
                        "rows",
                        "establishments",
                        "bidirectional_n3_mappings",
                        "ran_config_mismatches",
                        "method_sha256",
                    )
                )
            )
        results.append(
            {
                "dataset": dataset.name,
                "rounds": replay["rounds"],
                "method_recomputations": 3 * replay["rounds"],
                "audit_pass": replay["pass"],
                "original_score_matches": bool(matches) and all(matches),
                "mapping_matches": bool(mapping_matches) and any(mapping_matches),
                "mapping_establishments": mapping["establishments"],
            }
        )
    final_hashes = all(sha(root / name) == expected for name, expected in manifest["files"].items())
    result = {
        "datasets": results,
        "pinned_files_checked_twice": len(manifest["files"]),
        "original_hashes_unchanged": final_hashes,
        "guard_counts": counters,
        "core_source_sha256": manifest["core_source"]["sha256"],
        "python": sys.version,
        "new_model_calls": 0,
        "agent_repairs": 0,
        "guard_scope": "Python audit protection against accidental access, not an OS sandbox",
        "formal_quality": False,
        "pass": final_hashes
        and all(
            r["audit_pass"] and r["original_score_matches"] and r["mapping_matches"]
            for r in results
        )
        and not any(
            counters[k]
            for k in ("blocked_connections", "blocked_original_reads", "blocked_processes")
        ),
    }
    (output / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--deny-root", type=Path, nargs="+", required=True)
    args = parser.parse_args()
    result = run(args.root.resolve(), args.output.resolve(), args.deny_root)
    print(json.dumps(result))
    raise SystemExit(0 if result["pass"] else 1)
