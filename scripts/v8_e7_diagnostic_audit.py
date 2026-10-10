"""Independent physical-capture, raw-model, cost and injection-truth replay for E7."""

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

from upf_agent.v8.models import EvidenceBinding, OrchestrationTask
from upf_agent.v8.phase1 import write_json
from upf_agent.v8.review_evidence import source_review


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_frozen(root, name):
    directory = root / "code/scripts"
    sys.path.insert(0, str(directory))
    spec = importlib.util.spec_from_file_location("frozen_" + name, directory / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def audit(root, output):
    if output.exists():
        raise ValueError("new independent audit required")
    hashes = read(root / "code-hashes.json")
    assert all(sha(root / "code" / name) == expected for name, expected in hashes.items())
    runner = load_frozen(root, "v8_e7_diagnostic_runner")
    diagnosis = load_frozen(root, "v8_e7_diagnosis")
    summary, protocol = read(root / "summary.json"), read(root / "protocol.json")
    if (root / "source_manifest.json").exists():
        from upf_agent.v8.experiment_manifest import source_manifest

        assert source_manifest(Path(__file__).resolve().parents[1]) == read(
            root / "source_manifest.json"
        )
        assert summary["source_unchanged"]
    assert summary["planned"] == len(protocol["conditions"]) * protocol["repetitions"]
    rows = summary["rows"]
    assert len({(r["condition"], r["repeat"]) for r in rows}) == len(rows)
    records, inferred_failed_requests = [], 0
    for row in rows:
        number = f"round-{row['round']:03d}"
        folder = root / "rounds" / number
        private = root / "private" / number
        if row["health_error"]:
            records.append({"round": number, "health_error": True})
            continue
        snapshot_path = folder / "input/snapshot.json"
        snapshot = read(snapshot_path)
        truth = read(private / "truth.json")
        verification = read(private / "external-verification.json")
        verified = runner.injection_verified(
            row["condition"], verification["probe"], verification["independent_state"], snapshot
        )
        assert truth["condition"] == truth["expected_answer"] == row["condition"]
        assert truth["verified"] == row["injection_verified"] == verified
        assert read(private / "health-after.json")["pass"] == row["recovered"]
        record = {
            "round": number,
            "injection_verified": verified,
            "recovered": row["recovered"],
            "method_failure": row["method_failure"],
            "source_sha256": sha(snapshot_path),
        }
        agent = folder / "agent"
        if not row["integration_pass"]:
            process = (
                read(private / "agent-process.json")
                if (private / "agent-process.json").exists()
                else {}
            )
            # Old transport failures did not persist a trace. Record this lower bound
            # from the observed HTTP exception, not an invented request or token count.
            if (
                "HTTPStatusError" in process.get("stderr", "")
                and not (agent / "model-metrics.json").exists()
            ):
                inferred_failed_requests += 1
            record["failure_preserved"] = True
            metrics = agent / "model-metrics.json"
            if metrics.exists():
                failed_cost = read(metrics)
                record["actual_model_calls"] = failed_cost["invocations"]["model"]["attempted"]
                record["model_token_usage"] = failed_cost["token_usage"]
                assert record["actual_model_calls"] == row.get("actual_model_calls", 0)
                raw = agent / "raw-model-output.json"
                trace = agent / "model-traces.json"
                if raw.exists() and trace.exists():
                    saved_traces = read(trace)
                    assert (
                        saved_traces[-1]["response"]["choices"][0]["message"]["content"]
                        == read(raw)["content"]
                    )
            native_metrics = list((agent / "runs/v8").glob("*/metrics.json"))
            if len(native_metrics) == 1:
                native_cost = read(native_metrics[0])
                record["actual_native_tool_calls"] = native_cost["invocations"]["tool"]["attempted"]
                record["native_tool_committed"] = native_cost["invocations"]["tool"]["committed"]
            records.append(record)
            continue
        facts = diagnosis.build_facts(snapshot)
        for fact in facts:
            fact["source_sha256"] = sha(snapshot_path)
        assert facts == read(agent / "facts.json")
        assert diagnosis.model_view(facts) == read(agent / "model-visible-facts.json")
        traces = read(agent / "model-traces.json")
        assert len(traces) == 1 and traces[0]["operation"] == "e7_root_cause"
        config = root / "code/config/models.yaml"
        if config.exists():
            import yaml

            expected_model = yaml.safe_load(config.read_text())["generation"]["baseline"]
            assert traces[0]["request"]["model"] == expected_model["served_name"]
        content = traces[0]["response"]["choices"][0]["message"]["content"]
        assert content == read(agent / "raw-model-output.json")["content"]
        report = diagnosis.RootCauseReport.model_validate_json(content)
        assert report.model_dump(mode="json") == read(agent / "root-cause-report.json")
        ids = {f["evidence_id"] for f in facts}
        assert all(ref in ids for h in report.hypotheses for ref in h.evidence_ids)
        assert all(ref in ids for s in report.investigations for ref in s.evidence_ids)
        assert all(h.cause in diagnosis.eligible_causes(facts) for h in report.hypotheses)
        measurement = read(agent / "diagnosis.json")
        assert measurement["physical_capture_sha256"] == sha(snapshot_path)
        assert not report.execute_authorized and not report.goal_achieved
        assert measurement["diagnosis_seconds"] <= 180
        native = read(agent / "native.json")
        assert all(not a["execute_authorized"] for a in native["actions"])
        assert not native["task"]["synthetic"] and len(native["bindings"]) == 4
        assert native["task"]["object_profiles"]["ran"]["version"] == "3.2.7"
        assert native["task"]["object_profiles"]["upf"]["version"] == "2.7.6"
        task = OrchestrationTask.model_validate(native["task"])
        assert all(
            not source_review(agent, EvidenceBinding.model_validate(b), task)
            for b in native["bindings"]
        )
        observations = read(agent / "data/e7/observations.json")
        assert observations["raw_capture_sha256"] == sha(snapshot_path)
        assert not observations["synthetic"] and not observations["corroborated"]
        for observation in observations["observations"]:
            assert observation["raw_fact_ids"] == [
                f["evidence_id"] for f in facts if f["object_id"] == observation["object_id"]
            ]
            assert observation["observed"]["start"] == snapshot["window_start"]
            assert observation["observed"]["end"] == snapshot["window_end"]
        native_metrics = list((agent / "runs/v8").glob("*/metrics.json"))
        assert len(native_metrics) == 1
        native_cost = read(native_metrics[0])
        assert native_cost["invocations"]["model"]["attempted"] == 0
        assert native_cost["invocations"]["tool"]["attempted"] <= 8
        correct1 = report.hypotheses[0].cause == runner.CAUSE_MAP[row["condition"]]
        correct3 = runner.CAUSE_MAP[row["condition"]] in [h.cause for h in report.hypotheses]
        assert row["top1_correct"] == correct1 and row["top3_correct"] == correct3
        cost = read(agent / "model-metrics.json")["invocations"]["model"]["attempted"]
        assert cost == row["actual_model_calls"] == 1
        record.update(
            top1_correct=correct1,
            top3_correct=correct3,
            actual_model_calls=cost,
            actual_native_tool_calls=native_cost["invocations"]["tool"]["attempted"],
            native_tool_committed=native_cost["invocations"]["tool"]["committed"],
            model_token_usage=read(agent / "model-metrics.json")["token_usage"],
            fact_count=len(facts),
            captured_packets=sum(
                len(f["value"].get("packets", [])) for f in facts if isinstance(f["value"], dict)
            ),
        )
        records.append(record)
    verified_count = sum(r["injection_verified"] for r in rows)
    if verified_count:
        assert (
            summary["root_cause_top1"]
            == sum(r.get("top1_correct", False) for r in rows) / verified_count
        )
        assert (
            summary["root_cause_top3"]
            == sum(r.get("top3_correct", False) for r in rows) / verified_count
        )
    assert all(r["returncode"] == 0 for r in read(root / "private/teardown.json"))
    artifact_hashes = {
        str(p.relative_to(root)): sha(p) for p in sorted(root.rglob("*")) if p.is_file()
    }
    result = {
        "rounds": len(rows),
        "planned": summary["planned"],
        "verified_injections": verified_count,
        "root_cause_top1": summary["root_cause_top1"],
        "root_cause_top3": summary["root_cause_top3"],
        "truth_scope": "experimental injection family; not independent natural incidents",
        "actual_recorded_model_calls": summary["model_calls"],
        "old_untraced_failed_request_lower_bound": inferred_failed_requests,
        "formal_step_approval": False,
        "new_model_calls": 0,
        "records": records,
        "artifact_hashes": artifact_hashes,
        "integrity_pass": True,
        "engineering_pass": summary["pass"],
    }
    write_json(output, result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.root, args.output)
    print({k: v for k, v in result.items() if k not in {"records", "artifact_hashes"}})
