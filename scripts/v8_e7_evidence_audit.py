"""Independent raw-file rescoring and graph/session replay for E7 evidence controls."""

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

from upf_agent.v8.plan_metrics import wilson


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def equivalent(a, b):
    a, b = dict(a), dict(b)
    a.pop("diagnosis_seconds", None)
    b.pop("diagnosis_seconds", None)
    return a == b


def analyze(rows):
    metrics, conditions = {}, defaultdict(list)
    for row in rows:
        conditions[row["condition"]].append(row)
    for mode in ("flat", "joined", "graph"):
        faults = [r for r in rows if r["condition"] != "healthy" and r["injection_verified"]]
        healthy = [r for r in rows if r["condition"] == "healthy" and r["injection_verified"]]
        correct = sum(r.get("modes", {}).get(mode, {}).get("top1_correct", False) for r in faults)
        correct3 = sum(r.get("modes", {}).get(mode, {}).get("top3_correct", False) for r in faults)
        fp = sum(r.get("modes", {}).get(mode, {}).get("false_positive", False) for r in healthy)
        metrics[mode] = {
            "fault_denominator": len(faults),
            "top1_correct": correct,
            "top3_correct": correct3,
            "top1": correct / len(faults) if faults else None,
            "unknown_faults": sum(
                r.get("modes", {}).get(mode, {}).get("hypotheses", ["unknown"])[0] == "unknown"
                for r in faults
            ),
            "healthy_denominator": len(healthy),
            "false_positives": fp,
            "healthy_recognized": sum(
                r.get("modes", {}).get(mode, {}).get("healthy_recognized", False) for r in healthy
            ),
            "false_positive_wilson95_descriptive": wilson(fp, len(healthy)),
            "interval_scope": "repeated same-lab controls, not independent natural incidents",
        }
    comparisons = {}
    for baseline in ("flat", "joined"):
        improvements = regressions = 0
        by_condition = {}
        for condition, group in conditions.items():
            if condition == "healthy":
                continue
            delta = sum(
                int(r.get("modes", {}).get("graph", {}).get("top1_correct", False))
                - int(r.get("modes", {}).get(baseline, {}).get("top1_correct", False))
                for r in group
            )
            by_condition[condition] = delta
            improvements += delta > 0
            regressions += delta < 0
        discordant = improvements + regressions
        exact_sign = (
            min(
                1.0,
                2
                * sum(math.comb(discordant, k) for k in range(min(improvements, regressions) + 1))
                / 2**discordant,
            )
            if discordant
            else 1.0
        )
        comparisons[baseline + "_vs_graph"] = {
            "improved_fault_families": improvements,
            "regressed_fault_families": regressions,
            "correct_count_delta_by_condition": by_condition,
            "family_sign_test_two_sided_descriptive": exact_sign,
            "inferential_limit": "reused controlled fault families; no population claim",
        }
    return {"metrics": metrics, "comparisons": comparisons}


def audit(dataset, output):
    if output.exists():
        raise ValueError("new audit output required")
    output.mkdir(parents=True)
    code = dataset / "code/scripts"
    sys.path.insert(0, str(code))
    spec = importlib.util.spec_from_file_location(
        "frozen_evidence_rca", code / "v8_e7_evidence_rca.py"
    )
    method = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(method)
    summary, protocol = read(dataset / "summary.json"), read(dataset / "protocol.json")
    code_checks = {
        n: sha(dataset / "code" / n) == expected
        for n, expected in read(dataset / "code-hashes.json").items()
    }
    rows, checks, mapping_count, errors, packet_truncations = [], [], 0, [], 0
    expected_order = [
        (condition, repeat)
        for condition in protocol["conditions"]
        for repeat in range(1, protocol["repetitions"] + 1)
    ]
    labels = dict(
        zip(
            (
                "healthy",
                "n3-ul-loss",
                "n3-dl-loss",
                "upf-paused",
                "upf-n3-block",
                "gnb-gtp-mismatch",
                "ue-dnn-mismatch",
                "smf-paused",
                "pfcp-request-loss",
                "pfcp-response-loss",
                "pfcp-bilateral-loss",
                "gnb-paused",
                "ue-paused",
            ),
            (
                "no_fault_observed",
                "n3_uplink_transport_loss",
                "n3_downlink_transport_loss",
                "upf_process_suspended",
                "n3_bidirectional_transport_loss",
                "gnb_gtp_endpoint_mismatch",
                "ue_dnn_not_subscribed",
                "smf_process_suspended",
                "pfcp_smf_to_upf_loss",
                "pfcp_upf_to_smf_loss",
                "pfcp_bidirectional_loss",
                "ran_process_suspended",
                "ue_process_suspended",
            ),
            strict=True,
        )
    )
    for row in summary["rows"]:
        number, condition = row["round"], row["condition"]
        root = dataset / "rounds" / f"round-{number:03}"
        private = dataset / "private" / f"round-{number:03}"
        snapshot_path = root / "input/snapshot.json"
        snapshot = read(snapshot_path)
        external = read(private / "external-verification.json")
        state = external["independent_state"]
        actual_verified = False
        if condition == "healthy":
            actual_verified = all(
                p["returncode"] == 0 and "5 packets transmitted, 5 received" in p["stdout"]
                for p in snapshot["diagnostic_probes"].values()
            )
        elif condition.endswith("paused"):
            obj = condition.split("-")[0]
            states = state["ue_process_states"] if obj == "ue" else state["process_states"]
            actual_verified = "State:\tT" in states[obj] and external["probe"]["returncode"] != 0
        elif condition in {"gnb-gtp-mismatch", "ue-dnn-mismatch"}:
            cfg = snapshot["core" if condition.startswith("gnb") else "ue"]["logs_and_config"]
            expected_text = (
                "gtpAdvertiseIp: 127.0.0.8" if condition.startswith("gnb") else "apn: unsubscribed"
            )
            actual_verified = (
                expected_text in cfg["gnb.yaml" if condition.startswith("gnb") else "ue.yaml"]
                and external["probe"]["returncode"] != 0
            )
        else:
            import re

            actual_verified = (
                bool(
                    re.search(r"^\s*[1-9]\d*\s+\d+\s+DROP\s+udp", state["firewall"]["stdout"], re.M)
                )
                and external["probe"]["returncode"] != 0
            )
        recovered = read(private / "health-after.json")
        recovery_ok = (
            recovered["pass"]
            and recovered["attempts"][-1]["returncode"] == 0
            and "5 packets transmitted, 5 received" in recovered["attempts"][-1]["stdout"]
        )
        truth = read(private / "truth.json")
        copied = dict(row)
        copied["modes"] = {}
        round_checks = {
            "round": number,
            "protocol_order": expected_order[number - 1] == (condition, row["repeat"]),
            "verified_independently": actual_verified and row["injection_verified"],
            "truth_binding": truth["condition"] == condition
            and truth["verified"] == actual_verified,
            "independent_recovery": recovery_ok and row["recovered"],
            "method_process_success": read(private / "agent-process.json")["returncode"] == 0,
        }
        for mode in ("flat", "joined", "graph"):
            actual = read(root / "agent" / f"{mode}.json")
            replay = method.diagnose(snapshot, mode, sha(snapshot_path))
            round_checks[mode + "_deterministic_replay"] = equivalent(actual, replay)
            hypotheses = [h["cause"] for h in actual["hypotheses"]]
            rescored = {
                "hypotheses": hypotheses,
                "top1_correct": hypotheses[0] == labels[condition],
                "top3_correct": labels[condition] in hypotheses,
                "false_positive": condition == "healthy"
                and hypotheses[0] not in {"no_fault_observed", "unknown"},
                "healthy_recognized": condition == "healthy"
                and hypotheses[0] == "no_fault_observed",
            }
            round_checks[mode + "_scoring"] = row["modes"][mode] == rescored
            copied["modes"][mode] = rescored
            if mode == "graph":
                mapping_count += len(actual["session_pairs"])
                packet_truncations += sum(
                    p["captured_bytes"] < p["wire_bytes"]
                    for f in actual["facts"]
                    if isinstance(f["value"], dict) and "packets" in f["value"]
                    for p in f["value"]["packets"]
                )
                errors.extend(
                    {
                        "round": number,
                        "fact": f["evidence_id"],
                        "packet": p["packet_index"],
                        "error": p["pfcp_decode_error"],
                    }
                    for f in actual["facts"]
                    if isinstance(f["value"], dict) and "packets" in f["value"]
                    for p in f["value"]["packets"]
                    if "pfcp_decode_error" in p
                )
                round_checks["actual_graph_query"] = not actual["graph_query"]["truncated"]
                round_checks["joined_graph_equivalence"] = hypotheses == [
                    h["cause"] for h in read(root / "agent/joined.json")["hypotheses"]
                ]
        checks.append(round_checks)
        rows.append(copied)
    teardown = read(dataset / "private/teardown.json")
    hashes = {str(p.relative_to(dataset)): sha(p) for p in dataset.rglob("*") if p.is_file()}
    result = {
        "dataset": str(dataset),
        "planned": len(expected_order),
        "rounds": len(rows),
        **analyze(rows),
        "code_integrity": code_checks,
        "per_round_checks": checks,
        "pfcp_observed_establishment_pairs": mapping_count,
        "pfcp_decode_errors": errors,
        "truncated_packets": packet_truncations,
        "actual_new_model_calls": 0,
        "agent_repairs": 0,
        "formal_quality": False,
        "domain_rules_approved": False,
        "teardown_pass": bool(teardown) and all(r["returncode"] == 0 for r in teardown),
        "pass": len(rows) == len(expected_order)
        and all(code_checks.values())
        and all(all(v for k, v in c.items() if k != "round") for c in checks)
        and bool(teardown)
        and all(r["returncode"] == 0 for r in teardown),
    }
    (output / "source-sha256.json").write_text(json.dumps(hashes, indent=2) + "\n")
    (output / "rows-organizer-only.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    )
    (output / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.dataset.resolve(), args.output.resolve())
    print(
        json.dumps(
            {k: v for k, v in result.items() if k not in {"per_round_checks", "code_integrity"}}
        )
    )
    raise SystemExit(0 if result["pass"] else 1)
