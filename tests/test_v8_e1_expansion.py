"""Acquisition gates and unreviewed calibration must preserve provenance and evaluation limits."""

import base64
import importlib
import json
import struct
from pathlib import Path

import httpx
import pytest

from upf_agent.v8.e1_dataset import CaseManifest, DatasetIndex, write
from upf_agent.v8.e1_formal import model_identity
from upf_agent.v8.plan_cases import prepare_case
from upf_agent.v8.plan_generator import ObservedPlanClient
from upf_agent.v8.plan_ir import CaseGold, PlanIR, PlanStep

PROJECT = Path(__file__).resolve().parents[1]


def test_capture_audit_counts_snaplen_truncation_and_rejects_partial_record(monkeypatch):
    monkeypatch.syspath_prepend(str(PROJECT / "scripts"))
    audit = importlib.import_module("v8_e1_followup_audit")
    header = bytes.fromhex("d4c3b2a1") + struct.pack("<HHIIII", 2, 4, 0, 0, 16, 1)
    raw = header + struct.pack("<IIII", 1, 0, 4, 8) + b"unit"
    assert audit.capture_shape(base64.b64encode(raw)) == {
        "pcap_bytes": 44,
        "packet_records": 1,
        "truncated_packets": 1,
    }
    with pytest.raises(ValueError, match="partial pcap packet"):
        audit.capture_shape(base64.b64encode(raw[:-1]))


def test_calibration_request_audit_rejects_nested_private_truth(monkeypatch):
    monkeypatch.syspath_prepend(str(PROJECT / "scripts"))
    audit = importlib.import_module("v8_e1_followup_audit")
    audit.assert_no_organizer_fields({"evidence": [{"fields": {"observed_state": "down"}}]})
    with pytest.raises(AssertionError):
        audit.assert_no_organizer_fields({"evidence": [{"fields": {"private_truth": "unit"}}]})


def test_model_get_creation_fields_are_volatile_but_capability_changes_are_not():
    before = {
        "object": "list",
        "data": [
            {
                "id": "unit-model",
                "created": 1,
                "root": "/unit/weights",
                "max_model_len": 16384,
                "permission": [{"id": "modelperm-before", "created": 1, "allow_view": True}],
            }
        ],
    }
    after = json.loads(json.dumps(before))
    after["data"][0]["created"] = 2
    after["data"][0]["permission"][0].update(id="modelperm-after", created=2)
    assert model_identity(before) == model_identity(after)
    after["data"][0]["max_model_len"] = 8192
    assert model_identity(before) != model_identity(after)
    after["data"][0]["max_model_len"] = 16384
    after["data"][0]["permission"][0]["allow_view"] = False
    assert model_identity(before) != model_identity(after)


@pytest.fixture
def modules(monkeypatch):
    monkeypatch.syspath_prepend(str(PROJECT / "scripts"))
    return importlib.import_module("v8_e1_expand"), importlib.import_module("v8_e1_calibration")


def test_acquisition_preregistered_counts_and_disjoint_failure_families(modules):
    expand, _ = modules
    assert sum(s["repetitions"] for s in expand.CAMPAIGNS if s["split"] == "validation") == 9
    assert sum(s["repetitions"] for s in expand.CAMPAIGNS if s["split"] == "heldout") == 24
    validation = {s["condition"] for s in expand.CAMPAIGNS if s["split"] == "validation"}
    heldout = {s["condition"] for s in expand.CAMPAIGNS if s["split"] == "heldout"}
    assert not validation.intersection(heldout)


@pytest.mark.parametrize(
    "large_returncode,small_returncode,mtu,passed",
    [(1, 0, 576, True), (0, 0, 576, False), (1, 1, 576, False), (1, 0, 1500, False)],
)
def test_mtu_gate_needs_failed_large_healthy_small_and_actual_mtu(
    modules, large_returncode, small_returncode, mtu, passed
):
    expand, _ = modules
    assert (
        expand.verify_injection(
            "inner-mtu-576",
            {"small": {"returncode": small_returncode}, "large": {"returncode": large_returncode}},
            {"links": {"stdout": json.dumps([{"mtu": mtu}])}},
            "10.49.0.2",
            49,
        )
        is passed
    )


def test_wrong_observed_ue_scope_or_ambiguous_interface_cannot_be_injected(modules):
    expand, _ = modules
    body = {
        "interfaces": {
            "stdout": json.dumps(
                [{"ifname": "uesimtun0", "addr_info": [{"family": "inet", "local": "192.0.2.9"}]}]
            )
        }
    }
    with pytest.raises(ValueError, match="outside campaign scope"):
        expand.ue_address(body, 46)


def test_low_mtu_boundary_control_requires_both_probes_healthy(modules):
    expand, _ = modules
    external = {"links": {"stdout": json.dumps([{"mtu": 576}])}}
    probes = {"small": {"returncode": 0}, "large": {"returncode": 0}}
    assert expand.verify_injection(
        "inner-mtu-576-boundary-control", probes, external, "10.49.0.2", 49
    )
    probes["large"]["returncode"] = 1
    assert not expand.verify_injection(
        "inner-mtu-576-boundary-control", probes, external, "10.49.0.2", 49
    )


def case_dataset(root, splits):
    entries = []
    for i, split in enumerate(splits):
        case_id = f"UNIT-{split}-{i}"
        folder = root / ({"validation": "validation", "heldout": "heldout"}[split]) / case_id
        visible = folder / "visible"
        task, _ = prepare_case(visible, 0)
        observation = visible / task.observation_files[0]
        body = json.loads(observation.read_text())
        body["source_id"] = case_id
        write(observation, body)
        from upf_agent.v8.e1_dataset import sha

        task.path.source_id = case_id
        task.path.source_sha256 = sha(observation)
        write(visible / "case-task.json", task.model_dump(mode="json"))
        (visible / "case-reference.json").unlink()
        provenance = f"gold/provenance/{case_id}.json"
        write(root / provenance, {"unit_fixture_only": True})
        manifest = CaseManifest(
            case_id=case_id,
            split=split,
            visible_root=str(visible.relative_to(root)),
            task_file=str((visible / "case-task.json").relative_to(root)),
            reference_file=None,
            source_group=case_id,
            structure_family=split + "-unit-family",
            source_kind="new-synthetic",
            previously_evaluated=False,
            provenance_file=provenance,
        )
        name = str((folder / "case.json").relative_to(root))
        write(root / name, manifest.model_dump(mode="json"))
        entries.append(name)
    write(root / "dataset.json", DatasetIndex(cases=entries).model_dump(mode="json"))
    write(root / "reviews/received-reviews.json", [])
    write(root / "history-index.json", {"visible_source_hashes": [], "structure_families": []})


def fake_client(model, collector, budget, **kwargs):
    def response(request):
        context = json.loads(json.loads(request.content)["messages"][1]["content"])
        if "trusted_header" in context:
            header = context["trusted_header"]
            plan = PlanIR(
                **header,
                steps=[
                    PlanStep(
                        step_id="id" + str(i),
                        text="核对身份",
                        action_type="CHECK_IDENTITY",
                        target=obj,
                    )
                    for i, obj in enumerate(header["target_objects"])
                ],
                stop_conditions=["缺证停止"],
            )
            content = plan.model_dump_json()
        else:
            content = json.dumps({"actions": [], "done": True, "questions": [], "candidates": []})
        return httpx.Response(
            200,
            json={
                "choices": [{"message": {"content": content}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 20},
            },
        )

    return ObservedPlanClient(
        model, collector, budget, transport=httpx.MockTransport(response), **kwargs
    )


def test_unreviewed_calibration_keeps_all_methods_but_no_gold_or_heldout(
    modules, tmp_path, monkeypatch
):
    _, calibration = modules
    root = tmp_path / "dataset"
    case_dataset(root, ["validation", "validation", "heldout"])
    receipt = tmp_path / "unit-deployment.json"
    write(receipt, {"fixture_only": True})
    from upf_agent.v8 import phase2

    monkeypatch.setattr(
        phase2, "prepare_case", lambda *a: pytest.fail("fixed SPECS fallback forbidden")
    )
    output = tmp_path / "run"
    result = calibration.run_calibration(
        PROJECT, root, output, receipt, client_factory=fake_client, probe=False
    )
    assert (
        result["cases"] == 2 and result["recorded_method_runs"] == 8 and result["source_unchanged"]
    )
    assert not result["heldout_consumed"] and not result["formal_e1_completed"]
    assert result["formal_vpr"] is None and not result["reference_scoring_enabled"]
    from upf_agent.v8.models import digest

    protocol = json.loads((output / "protocol.json").read_text())
    assert protocol["code"]["sha256"] == digest(protocol["code"]["files"])
    assert not any("UNIT-heldout" in p.name for p in (output / "frozen-inputs").iterdir())
    rows = [
        json.loads(line) for line in (output / "metrics-by-case.jsonl").read_text().splitlines()
    ]
    assert all(r["reference_pass"] is None and r["vpr"] is None for r in rows)
    for raw in output.glob("runs/*/*/raw-plan.txt"):
        metrics = json.loads((raw.parent / "case-metrics.json").read_text())
        assert metrics["reference_pass"] is None and metrics["solvability"] is None
    assert not isinstance(calibration.absent_reference("unit"), CaseGold)
    with pytest.raises(ValueError, match="new calibration output"):
        calibration.run_calibration(
            PROJECT, root, output, receipt, client_factory=fake_client, probe=False
        )


def test_heldout_never_used_as_calibration_fallback(modules, tmp_path):
    _, calibration = modules
    root = tmp_path / "dataset"
    case_dataset(root, ["heldout"])
    receipt = tmp_path / "unit-deployment.json"
    write(receipt, {"fixture_only": True})
    output = tmp_path / "run"
    with pytest.raises(ValueError, match="never a calibration fallback"):
        calibration.run_calibration(
            PROJECT, root, output, receipt, client_factory=fake_client, probe=False
        )
    assert not output.exists()
