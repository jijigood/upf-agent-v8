"""RCA direction ambiguity, protocol truncation, and session identity negative controls."""

import importlib.util
import struct
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("e7_evidence_rca", SCRIPTS / "v8_e7_evidence_rca.py")
rca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rca)
sys.path.pop(0)


def ie(kind, body):
    return struct.pack("!HH", kind, len(body)) + body


def message(kind, sequence, ies=b"", seid=None):
    rest = (
        (struct.pack("!Q", seid) if seid is not None else b"")
        + sequence.to_bytes(3, "big")
        + b"\0"
        + ies
    )
    return struct.pack("!BBH", 0x21 if seid is not None else 0x20, kind, len(rest)) + rest


@pytest.mark.parametrize("cut", [0, 1, 4, 7, 10, 15, 18])
def test_pfcp_truncation_never_becomes_successful_session_mapping(cut):
    full = message(51, 42, ie(19, b"\1"), seid=123)
    with pytest.raises(ValueError, match="truncated"):
        rca.decode_pfcp(full[:cut])


def test_sequence_and_endpoint_seid_are_not_interchangeable():
    decoded = rca.decode_pfcp(message(51, 0xABCDEF, ie(19, b"\1"), seid=123))
    assert decoded["sequence"] == 0xABCDEF and decoded["header_seid"] == 123
    assert decoded["ies"][0]["cause"] == 1


def test_unknown_ie_is_retained_and_nested_ie_not_silently_skipped():
    decoded = rca.decode_pfcp(message(50, 42, ie(1, ie(65000, b"unknown"))))
    child = decoded["ies"][0]["children"][0]
    assert child["type"] == 65000 and child["length"] == 7 and len(child["sha256"]) == 64
    with pytest.raises(ValueError, match="truncated"):
        rca.decode_ies(ie(1, struct.pack("!HH", 21, 100)))


def test_fteid_choose_and_outer_header_ipv4_layout():
    assert rca.decode_ies(ie(21, b"\x0c\x07"))[0]["choose_id"] == 7
    fteid = rca.decode_ies(ie(21, b"\1" + struct.pack("!I", 99) + bytes([127, 0, 0, 7])))[0]
    outer = rca.decode_ies(ie(84, b"\1\0" + struct.pack("!I", 13) + bytes([127, 0, 0, 1])))[0]
    assert (fteid["ipv4"], fteid["teid"]) == ("127.0.0.7", 99)
    assert (outer["ipv4"], outer["teid"]) == ("127.0.0.1", 13)


def session_facts():
    cp, up = "127.0.0.4", "127.0.0.7"
    return [
        {
            "evidence_id": "f001",
            "value": {
                "packets": [
                    {
                        "packet_index": 0,
                        "src": cp,
                        "dst": up,
                        "timestamp_utc_epoch": 100,
                        "pfcp": {
                            "message_type": 50,
                            "sequence": 42,
                            "header_seid": 0,
                            "ies": [{"type": 57, "seid": 11, "ipv4": cp}],
                        },
                    },
                    {
                        "packet_index": 1,
                        "src": up,
                        "dst": cp,
                        "timestamp_utc_epoch": 101,
                        "pfcp": {
                            "message_type": 51,
                            "sequence": 42,
                            "header_seid": 11,
                            "ies": [{"type": 19, "cause": 1}, {"type": 57, "seid": 22, "ipv4": up}],
                        },
                    },
                ]
            },
        }
    ]


def test_pair_requires_both_local_seids_and_preserves_capture_only_scope():
    paired = rca.session_pairs(session_facts(), "127.0.0.4", "127.0.0.7")
    assert len(paired) == 1
    assert paired[0]["cp"]["seid"] == 11 and paired[0]["up"]["seid"] == 22
    assert not paired[0]["application_acceptance_proven"]


@pytest.mark.parametrize(
    "mutation",
    [
        "sequence",
        "header_seid",
        "endpoint",
        "rejected",
        "early",
        "late",
        "missing_cp",
        "duplicate_up",
    ],
)
def test_session_pair_rejects_cross_transaction_and_incomplete_identity(mutation):
    facts = session_facts()
    req, resp = facts[0]["value"]["packets"]
    if mutation in {"sequence", "header_seid"}:
        resp["pfcp"][mutation] = 999
    elif mutation == "endpoint":
        resp["src"] = "127.0.0.8"
    elif mutation == "rejected":
        resp["pfcp"]["ies"][0]["cause"] = 64
    elif mutation == "early":
        resp["timestamp_utc_epoch"] = 99
    elif mutation == "late":
        resp["timestamp_utc_epoch"] = 111
    elif mutation == "missing_cp":
        req["pfcp"]["ies"] = []
    else:
        resp["pfcp"]["ies"].append(resp["pfcp"]["ies"][-1])
    assert not rca.session_pairs(facts, "127.0.0.4", "127.0.0.7")


def minimal_snapshot(state="S (sleeping)", successful=False):
    ping = (
        "5 packets transmitted, 5 received, 0% packet loss"
        if successful
        else "5 packets transmitted, 0 received, 100% packet loss"
    )
    return {
        "window_start": "2026-10-10T00:00:00+00:00",
        "window_end": "2026-10-10T00:00:10+00:00",
        "core": {
            "process_states": {name: "State:\t" + state for name in ("upf", "smf", "gnb")},
            "logs_and_config": {},
        },
        "ue": {"process_states": {"ue": "State:\tS (sleeping)"}, "logs_and_config": {}},
        "packet_captures": {},
        "diagnostic_probes": {
            name: {"returncode": 0 if successful else 1, "stdout": ping}
            for name in ("uplink", "downlink")
        },
    }


def test_sleeping_and_no_packets_do_not_prove_a_specific_direction_or_cause():
    snapshot = minimal_snapshot()
    for mode in ("flat", "graph"):
        result = rca.diagnose(snapshot, mode, "0" * 64)
        assert result["hypotheses"][0]["cause"] == "unknown"
        assert not result["execute_authorized"] and not result["formal_quality"]


def test_healthy_requires_normal_processes_and_both_business_probes():
    result = rca.diagnose(minimal_snapshot(successful=True), "graph", "0" * 64)
    assert result["hypotheses"][0]["cause"] == "no_fault_observed"
    assert result["graph_query"]["nodes"] and result["graph_query"]["edges"]
    bad = minimal_snapshot(successful=True)
    bad["diagnostic_probes"]["downlink"]["returncode"] = 1
    assert rca.diagnose(bad, "graph", "0" * 64)["hypotheses"][0]["cause"] == "unknown"


def test_stopped_process_remains_a_candidate_even_if_probe_counter_is_healthy():
    result = rca.diagnose(minimal_snapshot("T (stopped)", True), "graph", "0" * 64)
    assert "no_fault_observed" not in [h["cause"] for h in result["hypotheses"]]
    assert result["hypotheses"][0]["cause"].endswith("process_suspended")
