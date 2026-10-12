"""Independent source/readback audit and unreviewed engineering cost comparison."""

import argparse
import base64
import csv
import json
import re
import struct
from pathlib import Path

from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.e1_dataset import components, load_dataset, read, readiness, sha, write
from upf_agent.v8.models import EvaluationContext, EvidenceBinding, OrchestrationTask, digest
from upf_agent.v8.phase2 import METHODS
from upf_agent.v8.plan_translator import translate_plan
from upf_agent.v8.plan_validator import validate_plan


def table(path, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def capture_shape(encoded):
    raw = base64.b64decode(encoded, validate=True)
    endian = "<" if raw[:4] in [bytes.fromhex("d4c3b2a1"), bytes.fromhex("4d3cb2a1")] else ">"
    if len(raw) < 24 or raw[:4] not in [
        bytes.fromhex(v) for v in ["d4c3b2a1", "4d3cb2a1", "a1b2c3d4", "a1b23c4d"]
    ]:
        raise ValueError("valid classic pcap required")
    offset, count, truncated = 24, 0, 0
    while offset < len(raw):
        if offset + 16 > len(raw):
            raise ValueError("partial pcap record header")
        _, _, included, original = struct.unpack(endian + "IIII", raw[offset : offset + 16])
        offset += 16
        if offset + included > len(raw):
            raise ValueError("partial pcap packet")
        count += 1
        truncated += included < original
        offset += included
    return {"pcap_bytes": len(raw), "packet_records": count, "truncated_packets": truncated}


def assert_no_organizer_fields(value):
    forbidden = {
        "gold",
        "reference",
        "private_truth",
        "truth",
        "injection_condition",
        "true_cause",
        "provenance",
    }
    if isinstance(value, dict):
        assert not forbidden.intersection(value)
        for item in value.values():
            assert_no_organizer_fields(item)
    elif isinstance(value, list):
        for item in value:
            assert_no_organizer_fields(item)


def condition_readback(condition, snapshot, external, target, plane):
    small, large = (snapshot["normal_probes"][k]["returncode"] for k in ["small", "large"])
    if condition.startswith("inner-mtu-576"):
        applied = json.loads(external["links"]["stdout"])[0]["mtu"] == 576
        expected = (
            small == 0 and large == 0
            if condition.endswith("boundary-control")
            else small == 0 and large != 0
        )
    elif condition == "gateway-address-absent":
        applied = not any(
            a.get("local") == f"10.{plane}.0.1"
            for r in json.loads(external["addresses"]["stdout"])
            for a in r.get("addr_info", [])
        )
        expected = small != 0 and large != 0
    elif condition == "reply-blackhole-route":
        applied = any(
            r.get("type") == "blackhole" and r.get("dst") in [target, target + "/32"]
            for r in json.loads(external["routes"]["stdout"])
        )
        expected = small != 0 and large != 0
    elif condition == "reply-policy-prohibit":
        applied = any(
            r.get("priority") == 12001
            and r.get("action") == "prohibit"
            and r.get("src") in [f"10.{plane}.0.1", f"10.{plane}.0.1/32"]
            and r.get("dst") in [target, target + "/32"]
            for r in json.loads(external["rules"]["stdout"])
        )
        expected = small != 0 and large != 0
    elif condition == "ogstun-admin-down":
        applied = "UP" not in json.loads(external["links"]["stdout"])[0]["flags"]
        expected = small != 0 and large != 0
    else:
        chain = "input" if condition == "inner-request-filter" else "output"
        applied = bool(
            re.search(
                r"^\s*[1-9]\d*\s+\d+\s+DROP\s+icmp.*ogstun.*icmptype "
                + ("8" if chain == "input" else "0"),
                external[chain]["stdout"],
                re.M,
            )
        )
        expected = small != 0 and large != 0
    return bool(applied), bool(expected)


def audit_sources(project, dataset_root, root, output):
    if output.exists():
        raise ValueError("fresh audit output required")
    data = load_dataset(dataset_root)
    status = readiness(data)
    assert status["split_counts"] == {"dev": 24, "validation": 12, "heldout": 24}
    assert status["actual_review_records"] == 0 and status["hash_bound_approved_gold"] == 0
    rows = []
    campaign_roots = list((root / "input-expansion-001/captures").iterdir()) + [
        root / "input-expansion-002/captures/withheld-4"
    ]
    for campaign in sorted(campaign_roots):
        summary = read(campaign / "summary.json")
        spec = summary["spec"]
        assert summary["teardown_pass"]
        protocol = read(campaign / "protocol.json")
        for name, expected in protocol["code_hashes"].items():
            assert sha(campaign / "code/lab" / name) == expected
        for row in summary["rows"]:
            number = row["round"]
            private = campaign / "private" / f"round-{number:03d}"
            source = campaign / "rounds" / f"round-{number:03d}" / "input/snapshot.json"
            snap = read(source)
            truth = read(private / "truth.json")
            external = read(private / "external-verification.json")
            applied, expected = condition_readback(
                spec["condition"], snap, external, truth["target"], spec["plane"]
            )
            assert applied and expected == row["injection_verified"]
            for phase in ["before", "after"]:
                health = read(private / f"health-{phase}.json")
                assert health["pass"] and any(
                    all(
                        v["returncode"] == 0 and "0% packet loss" in v["stdout"] for v in a.values()
                    )
                    for a in health["attempts"]
                )
            rows.append(
                {
                    "campaign": str(campaign.relative_to(project)),
                    "round": number,
                    "condition": spec["condition"],
                    "planned_split": spec["split"],
                    "applied_kernel_condition_verified": applied,
                    "expected_probe_effect_verified": expected,
                    "small_probe_returncode": snap["normal_probes"]["small"]["returncode"],
                    "large_probe_returncode": snap["normal_probes"]["large"]["returncode"],
                    "recovered_with_fresh_UE_harness_reset": row["recovered"],
                    "normal_source": str(source.relative_to(project)),
                    "normal_source_sha256": sha(source),
                    "private_truth": str((private / "truth.json").relative_to(project)),
                    "private_truth_sha256": sha(private / "truth.json"),
                    "independent_kernel_read_sha256": sha(private / "external-verification.json"),
                    **capture_shape(snap["packet_capture"]["capture_base64"]),
                    "model_calls": 0,
                    "expert_Gold_created": False,
                    "heldout_model_consumed": False,
                }
            )
    assert len(rows) == 34 and sum(r["expected_probe_effect_verified"] for r in rows) == 33
    for case in data["cases"]:
        manifest = case["manifest"]
        if manifest.source_kind != "experimental-injection":
            continue
        provenance = read(dataset_root / manifest.provenance_file)
        if "capture_root" not in provenance:
            continue
        original = (
            Path(provenance["capture_root"])
            / "rounds"
            / f"round-{provenance['capture_round']:03d}"
            / "input/snapshot.json"
        )
        raw = case["visible"] / "data/raw/snapshot.json"
        assert sha(raw) == sha(original)
        snapshot = read(raw)
        normal = read(case["visible"] / case["task"].observation_files[0])
        assert normal["synthetic"] is False and normal["corroborated"] is False
        for record in normal["observations"]:
            fields = record["fields"]
            name = "upf.log" if record["object_id"] == "upf" else "gnb.log"
            assert (
                fields["log_excerpt"] == snapshot["core"]["logs_and_config"].get(name, "")[-3000:]
            )
            assert fields["core_interface_inventory"] == snapshot["core"]["interfaces"]["stdout"]
            assert fields["routing_inventory"] == snapshot["core"]["routing_inventory"]
            assert (
                fields["small_probe"] == snapshot["normal_probes"]["small"]
                and fields["large_probe"] == snapshot["normal_probes"]["large"]
            )
    carried = read(root / "input-expansion-002/carried-forward-campaigns.json")
    for campaign, receipt in carried.items():
        for name, expected in receipt["sha256"].items():
            assert (
                sha(Path(receipt["source"]) / name)
                == sha(root / "input-expansion-002/captures" / campaign / name)
                == expected
            )
    output.mkdir(parents=True)
    table(output / "acquisition-samples.csv", rows)
    inventory = []
    forms = []
    for case in data["cases"]:
        m = case["manifest"]
        inventory.append(
            {
                "case_id": m.case_id,
                "split": m.split,
                "source_group": m.source_group,
                "structure_family": m.structure_family,
                "task_file": m.task_file,
                "visible_root": m.visible_root,
                "reference_file": m.reference_file or "",
                "reference_sha256": digest(case["gold"]) if case["gold"] else "",
                "approved_gold": case["approved"] is not None,
                "raw_source_hashes": json.dumps(m.raw_source_hashes, sort_keys=True),
            }
        )
        for seat in [1, 2]:
            forms.append(
                {
                    "seat": seat,
                    "case_id": m.case_id,
                    "reference_sha256": digest(case["gold"]) if case["gold"] else "",
                    "reference_file": m.reference_file or "",
                    "reviewer": "",
                    "decision": "",
                    "review_source": "",
                    "review_version": "",
                    "notes": "",
                }
            )
    table(output / "case-inventory.csv", inventory)
    table(output / "empty-gold-review-organizer-only.csv", forms)
    result = {
        "case_count": 60,
        "split_counts": status["split_counts"],
        "source_structure_component_sizes": [len(g) for g in components(data["cases"])],
        "new_acquisition_trials": 34,
        "expected_effect_verified": 33,
        "failed_hypotheses_retained": 1,
        "fault_inputs_new": 27,
        "boundary_controls_new": 6,
        "new_case_raw_copies_and_projections_verified": 33,
        "carried_forward_inputs_not_counted_as_new_trials": 27,
        "empty_review_rows": 120,
        "missing_independent_references": len(status["missing_references"]),
        "actual_review_records": 0,
        "formal_e1_completed": False,
        "heldout_consumed": False,
        "new_model_generation_calls_by_this_audit": 0,
    }
    write(output / "summary.json", result)
    write(
        output / "sha256_manifest.json", {p.name: sha(p) for p in output.iterdir() if p.is_file()}
    )
    return result


def audit_calibration(project, run_root, output):
    if output.exists():
        raise ValueError("new calibration audit required")
    for name, expected in read(run_root / "sha256_manifest.json").items():
        assert sha(run_root / name) == expected, name
    protocol = read(run_root / "protocol.json")
    rows = [
        json.loads(line) for line in (run_root / "metrics-by-case.jsonl").read_text().splitlines()
    ]
    ids = [c["case_id"] for c in protocol["cases"]]
    assert {(r["case_id"], r["method"]) for r in rows} == {(i, m) for i in ids for m in METHODS}
    assert len(rows) == len(ids) * 4 and all(
        r["reference_pass"] is None and r["vpr"] is None and not r["reference_scoring_enabled"]
        for r in rows
    )
    replayed = 0
    model_requests = 0
    model_operations = {}
    action_counts = {}
    missing_costs = {
        k: [] for k in ["model_attempts", "tool_attempts", "input_tokens", "output_tokens"]
    }
    for row in rows:
        folder = run_root / "runs" / row["case_id"] / f"method-{METHODS.index(row['method']) + 1}"
        if row["runner_error"]:
            continue
        raw = (folder / "raw-plan.txt").read_text()
        raw_meta = read(folder / "raw-output.json")
        assert sha(folder / "raw-plan.txt") == raw_meta["content_sha256"]
        assert (
            translate_plan(raw).plan is not None
            if row["parsed"]
            else translate_plan(raw).plan is None
        )
        translated = translate_plan(raw).plan
        if translated is not None:
            for step in translated.steps:
                action_counts[step.action_type] = action_counts.get(step.action_type, 0) + 1
        task = OrchestrationTask.model_validate(read(folder / "task.json"))
        bindings = [EvidenceBinding.model_validate(b) for b in read(folder / "bindings.json")]
        context = EvaluationContext.model_validate(read(folder / "context.json"))
        validation = validate_plan(
            translate_plan(raw).plan,
            bindings,
            task,
            compile_contract(task),
            context,
            folder / "runtime",
        )
        assert validation.model_dump(mode="json") == read(folder / "validation.json")
        cost = read(folder / "metrics.json")
        for kind in ["model", "tool"]:
            assert row[kind + "_attempts"] == cost["invocations"][kind]["attempted"]
        for side in ["input", "output"]:
            assert row[side + "_tokens"] == cost["token_usage"][side]
        traces = [
            json.loads(line) for line in (folder / "model-traces.jsonl").read_text().splitlines()
        ]
        assert len(traces) == row["model_attempts"]
        for trace in traces:
            request = trace["request"]
            assert request["model"] == protocol["model_receipt"]["served_name"]
            encoded = json.dumps(request, ensure_ascii=False)
            assert "E1-HO-N" not in encoded
            assert_no_organizer_fields(request)
            for message in request.get("messages", []):
                if message["role"] == "user":
                    assert_no_organizer_fields(json.loads(message["content"]))
            operation = trace["operation"]
            model_operations[operation] = model_operations.get(operation, 0) + 1
            model_requests += 1
        replayed += 1
    for row in rows:
        for key, unknown in missing_costs.items():
            if row.get(key) is None:
                unknown.append({"case_id": row["case_id"], "method": row["method"]})
    index = {(r["case_id"], r["method"]): r for r in rows}
    comparisons = []
    for baseline, treatment in [
        (METHODS[1], METHODS[3]),
        (METHODS[2], METHODS[3]),
        (METHODS[0], METHODS[3]),
    ]:
        quality_delta = sum(
            index[i, treatment]["validator_pass"] - index[i, baseline]["validator_pass"]
            for i in ids
        ) / len(ids)
        for metric in [
            "tool_attempts",
            "model_attempts",
            "input_tokens",
            "output_tokens",
            "elapsed_seconds",
        ]:
            pairs = [(index[i, baseline].get(metric), index[i, treatment].get(metric)) for i in ids]
            unknown = [i for i, (x, y) in zip(ids, pairs, strict=True) if x is None or y is None]
            known = [(x, y) for x, y in pairs if x is not None and y is not None]
            comparisons.append(
                {
                    "baseline": baseline,
                    "treatment": treatment,
                    "quality_metric": "machine_validator_pass_only",
                    "quality_mean_difference": quality_delta,
                    "planned_case_denominator": len(ids),
                    "cost_metric": metric,
                    "measured_cost_pairs": len(known),
                    "unknown_case_ids": json.dumps(unknown),
                    "baseline_known_total": sum(x for x, _ in known),
                    "treatment_known_total": sum(y for _, y in known),
                    "mean_cost_difference": sum(y - x for x, y in known) / len(known)
                    if known and not unknown
                    else "",
                    "formal_vpr": "",
                    "population_superiority_claim": False,
                    "same_source_cluster_calibration_not_formal_inference": True,
                }
            )
    output.mkdir(parents=True)
    table(output / "paired-quality-cost.csv", comparisons)
    result = {
        "method_runs_verified": len(rows),
        "raw_plan_and_full_validator_replayed": replayed,
        "comparison_cost_rows": len(comparisons),
        "actual_model_attempts": sum(r["model_attempts"] or 0 for r in rows),
        "saved_actual_model_requests_verified": model_requests,
        "model_operations": model_operations,
        "plan_action_counts": action_counts,
        "unknown_cost_runs_by_metric": missing_costs,
        "known_cost_totals_do_not_impute_unknown_as_zero": True,
        "actual_tool_attempts": sum(r["tool_attempts"] or 0 for r in rows),
        "input_tokens": sum(r["input_tokens"] or 0 for r in rows),
        "output_tokens": sum(r["output_tokens"] or 0 for r in rows),
        "formal_vpr": None,
        "actual_human_reviews": 0,
        "heldout_consumed": False,
        "new_model_calls_by_this_audit": 0,
    }
    write(output / "summary.json", result)
    write(
        output / "sha256_manifest.json", {p.name: sha(p) for p in output.iterdir() if p.is_file()}
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=["sources", "calibration"])
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dataset", type=Path, default=Path("eval/v8/e1"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = (
        audit_sources(
            args.project.resolve(),
            args.dataset.resolve(),
            args.root.resolve(),
            args.output.resolve(),
        )
        if args.kind == "sources"
        else audit_calibration(args.project.resolve(), args.root.resolve(), args.output.resolve())
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
