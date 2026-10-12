"""Packet and provenance negative controls; all inputs here are synthetic fixtures."""

import base64
import copy
import json
import struct
from datetime import UTC, datetime

import pytest

from upf_agent.v8.e1_packet_observations import compare, observations
from upf_agent.v8.e1_source_closure import IMAGE, admission_checks


def capture(*, link=276, payload=b"test", identifier=7, stamp=100, icmp_type=8, fragment=0):
    icmp = struct.pack("!BBHHH", icmp_type, 0, 0, identifier, 1) + payload
    ipv4 = (
        struct.pack(
            "!BBHHHBBH4s4s",
            0x45,
            0,
            20 + len(icmp),
            1,
            fragment,
            64,
            1,
            0,
            b"\x0a\x2d\x00\x02",
            b"\x0a\x2d\x00\x01",
        )
        + icmp
    )
    if link == 276:
        packet = struct.pack("!HHIHBB8s", 0x0800, 0, 2, 65534, 4, 0, b"\0" * 8) + ipv4
    elif link == 113:
        packet = struct.pack("!HHH8sH", 4, 65534, 0, b"\0" * 8, 0x0800) + ipv4
    elif link == 1:
        packet = b"\0" * 12 + struct.pack("!H", 0x0800) + ipv4
    else:
        packet = ipv4
    raw = struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, link)
    raw += struct.pack("<IIII", stamp, 0, len(packet), len(packet)) + packet
    return {"capture_base64": base64.b64encode(raw).decode()}


@pytest.mark.parametrize("link", [276, 113, 1, 101])
def test_supported_link_preserves_echo_identity(link):
    result = observations(capture(link=link))
    assert result["rows"][0]["identifier"] == 7
    assert result["rows"][0]["src"] == "10.45.0.2"
    assert result["delivery_or_cause_proved"] is False


@pytest.mark.parametrize(
    "change", [{"payload": b"different"}, {"identifier": 8}, {"stamp": 104}, {"icmp_type": 0}]
)
def test_partial_identity_or_time_does_not_match(change):
    result = compare(observations(capture()), observations(capture(**change)))
    assert result["matched_observations"] == 0
    assert result["unmatched_means_packet_loss"] is False


def test_matching_is_injective_and_does_not_prove_delivery():
    left = observations(capture())
    left["rows"].append(copy.deepcopy(left["rows"][0]))
    right = observations(capture(link=101))
    result = compare(left, right)
    assert result["matched_observations"] == 1 and result["left_unmatched"] == 1
    assert result["delivery_or_cause_proved"] is False
    with pytest.raises(ValueError, match="independent"):
        compare(left, left)


def test_fragments_and_unknown_links_remain_unknown():
    assert observations(capture(fragment=0x2000))["skipped"] == {"fragmented_ipv4": 1}
    assert not observations(capture(link=999))["rows"]


def test_incomplete_pcap_is_rejected():
    item = capture()
    item["capture_base64"] = base64.b64encode(
        base64.b64decode(item["capture_base64"])[:-1]
    ).decode()
    with pytest.raises(ValueError, match="record length"):
        observations(item)


def source():
    raw = {}
    for role, name in (("core", "ogstun"), ("ue", "uesimtun0")):
        raw[role] = {
            "role": role,
            "synthetic": False,
            "interfaces": {
                "argv": ["ip", "-json", "address"],
                "returncode": 0,
                "stdout": json.dumps([{"ifname": name}]),
            },
        }
    raw["core"]["filter_inventory"] = {
        c: {"argv": ["iptables", "-nvxL", c], "returncode": 0}
        for c in ("INPUT", "OUTPUT", "FORWARD")
    }
    for role, key, link in (("core", "packet_capture", 276), ("ue", "ue_packet_capture", 101)):
        raw[key] = capture(link=link)
        raw[key]["capture_position"] = f"owned {role} namespace any interface"
    raw["normal_probe"] = {
        "argv": ["ping", "-n", "-I", "uesimtun0", "-c", "5", "-i", ".2", "-W", "1", "10.45.0.1"],
        "returncode": 1,
    }
    raw["window_start"] = datetime.fromtimestamp(99, UTC).isoformat()
    raw["window_end"] = datetime.fromtimestamp(101, UTC).isoformat()
    deployment = {
        "image": IMAGE,
        "open5gs": {"returncode": 0, "stdout": "Open5GS v2.7.6"},
        "ueransim": {"returncode": 1, "stdout": "v3.2.7"},
    }
    return raw, deployment


def test_source_checks_are_provenance_only():
    raw, deployment = source()
    assert all(admission_checks(raw, deployment).values())
    raw["condition"] = "organizer answer must not be visible"
    assert not admission_checks(raw, deployment)["only_normal_keys"]


def test_candidate_formal_profile_is_explicit_and_keeps_legacy_default():
    from upf_agent.v8.e1_formal import NormalizedEvidenceTools, runner_options
    from upf_agent.v8.e1_source_closure import VerifiedDomainTools

    legacy, old_head = runner_options("legacy")
    candidate, new_head = runner_options("verified-runtime-candidate-1")
    assert legacy["tools_factory"] is NormalizedEvidenceTools
    assert candidate["tools_factory"] is VerifiedDomainTools
    assert old_head["version"] != new_head["version"]
    with pytest.raises(ValueError, match="unknown"):
        runner_options("arbitrary-schema-from-input")


def test_compact_context_preserves_facts_and_citations_without_changing_original():
    from upf_agent.v8.e1_verified_head import compact_body

    row = {
        "object_id": "upf",
        "category": "K",
        "fields": {"instruction": "original"},
        "citation": {"source_sha256": "1" * 64, "locator": "chars:0:8"},
        "source": {"source_id": "original-source"},
        "knowledge_applicability": {"status": "mapped", "reviewed": False},
    }
    original = {
        "evidence": [row, copy.deepcopy(row)],
        "action_registry": {
            "CHECK": {
                "parameters": {"properties": {"field": {"type": "string"}}},
                "permission_kind": "read",
                "effect_kind": "read",
            }
        },
    }
    result = compact_body(original)
    assert len(result["evidence"]) == 1 and len(original["evidence"]) == 2
    assert result["evidence"][0]["fields"] == row["fields"]
    assert result["evidence"][0]["citation"] == row["citation"]
    assert result["evidence"][0]["knowledge_applicability"]["reviewed"] is False


@pytest.mark.parametrize(
    "fault", ["image", "version", "role", "write_command", "missing_chain", "future_capture"]
)
def test_bad_source_never_admitted(fault):
    raw, deployment = source()
    if fault == "image":
        deployment["image"] = "different"
    elif fault == "version":
        deployment["ueransim"]["stdout"] = "v3.2.6"
    elif fault == "role":
        raw["ue"]["role"] = "core"
    elif fault == "write_command":
        raw["core"]["filter_inventory"]["INPUT"]["argv"] = ["iptables", "-F", "INPUT"]
    elif fault == "missing_chain":
        del raw["core"]["filter_inventory"]["OUTPUT"]
    else:
        raw["window_end"] = datetime.fromtimestamp(99.5, UTC).isoformat()
    assert not all(admission_checks(raw, deployment).values())


@pytest.mark.parametrize("profile_scoped", [False, True])
def test_p5_profile_uses_object_products_without_a_global_product_filter(
    monkeypatch, tmp_path, profile_scoped
):
    from upf_agent.v8 import p5_plan_runner
    from upf_agent.v8.models import ObjectProfile, OrchestrationTask

    captured = []
    monkeypatch.setattr(
        p5_plan_runner, "run_agent", lambda root, task, backend: captured.append(task)
    )
    task = OrchestrationTask(
        question="只读故障排查，核对手册和日志计数",
        template="runtime_investigation",
        objects=["upf", "ue"],
        product="Open5GS",
        version="2.7.6",
        object_profiles={
            "upf": ObjectProfile(role="upf", product="Open5GS", version="2.7.6"),
            "ue": ObjectProfile(role="unspecified", product="UERANSIM", version="3.2.7"),
        },
    )
    original = task.model_dump(mode="json")
    p5_plan_runner.run_p5(tmp_path, task, None, None, profile_scoped=profile_scoped)
    assert captured[0].product == (None if profile_scoped else "Open5GS")
    assert captured[0].version == (None if profile_scoped else "2.7.6")
    assert captured[0].mode == "agent"
    assert task.model_dump(mode="json") == original
