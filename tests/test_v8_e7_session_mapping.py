"""Normal wire identities must not join across UE, SEID, transaction or time."""

import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location(
    "e7_session_mapping", SCRIPTS / "v8_e7_session_mapping.py"
)
mapping = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mapping)
sys.path.pop(0)


def fixture():
    snapshot = {
        "core": {
            "logs_and_config": {
                "smf.yaml": "smf: {pfcp: {server: [{address: 127.0.0.4}]}}",
                "upf.yaml": (
                    "upf: {pfcp: {server: [{address: 127.0.0.7}]}, "
                    "gtpu: {server: [{address: 127.0.0.7}]}}"
                ),
                "gnb.yaml": "gtpIp: 127.0.0.1",
            }
        },
        "ue": {
            "interfaces": {
                "stdout": json.dumps(
                    [
                        {
                            "ifname": "uesimtun0",
                            "addr_info": [{"family": "inet", "local": "10.45.0.2"}],
                        }
                    ]
                )
            }
        },
    }
    packets = [
        {
            "packet_index": 0,
            "src": "127.0.0.4",
            "dst": "127.0.0.7",
            "timestamp_utc_epoch": 100,
            "pfcp": {
                "message_type": 50,
                "sequence": 42,
                "header_seid": 0,
                "ies": [{"type": 57, "seid": 11, "ipv4": "127.0.0.4"}],
            },
        },
        {
            "packet_index": 1,
            "src": "127.0.0.7",
            "dst": "127.0.0.4",
            "timestamp_utc_epoch": 101,
            "pfcp": {
                "message_type": 51,
                "sequence": 42,
                "header_seid": 11,
                "ies": [
                    {"type": 19, "cause": 1},
                    {"type": 57, "seid": 22, "ipv4": "127.0.0.7"},
                    {"type": 8, "children": [{"type": 21, "teid": 99, "ipv4": "127.0.0.7"}]},
                ],
            },
        },
        {
            "packet_index": 2,
            "src": "127.0.0.4",
            "dst": "127.0.0.7",
            "timestamp_utc_epoch": 102,
            "pfcp": {
                "message_type": 52,
                "sequence": 43,
                "header_seid": 22,
                "ies": [{"type": 10, "children": [{"type": 84, "ipv4": "127.0.0.1", "teid": 1}]}],
            },
        },
        {
            "packet_index": 3,
            "src": "127.0.0.7",
            "dst": "127.0.0.4",
            "timestamp_utc_epoch": 103,
            "pfcp": {
                "message_type": 53,
                "sequence": 43,
                "header_seid": 11,
                "ies": [{"type": 19, "cause": 1}],
            },
        },
        {
            "packet_index": 4,
            "src": "127.0.0.1",
            "dst": "127.0.0.7",
            "timestamp_utc_epoch": 104,
            "gtp_type_numeric": 255,
            "dst_port": 2152,
            "teid": 99,
            "inner_src": "10.45.0.2",
        },
        {
            "packet_index": 5,
            "src": "127.0.0.7",
            "dst": "127.0.0.1",
            "timestamp_utc_epoch": 105,
            "gtp_type_numeric": 255,
            "dst_port": 2152,
            "teid": 1,
            "inner_dst": "10.45.0.2",
        },
    ]
    return snapshot, [{"evidence_id": "f001", "value": {"packets": packets}}]


def test_complete_normal_wire_join_is_explicitly_not_application_acceptance(monkeypatch):
    snapshot, facts = fixture()
    monkeypatch.setattr(mapping, "enriched_facts", lambda _: facts)
    result = mapping.map_sessions(snapshot)["mappings"][0]
    assert result["observed_bidirectional_n3_mapping"]
    assert not result["application_acceptance_proven"]
    assert result["ran_bound_advertised_consistent"]


@pytest.mark.parametrize(
    "change",
    [
        "old_mod",
        "wrong_up_seid",
        "wrong_cp_seid",
        "wrong_seq",
        "early_data",
        "wrong_ue",
        "wrong_teid",
        "wrong_peer",
        "two_ues",
    ],
)
def test_session_mapping_rejects_cross_session_and_premature_data(monkeypatch, change):
    snapshot, facts = fixture()
    packets = facts[0]["value"]["packets"]
    if change == "old_mod":
        packets[2]["timestamp_utc_epoch"] = 99
    elif change == "wrong_up_seid":
        packets[2]["pfcp"]["header_seid"] = 999
    elif change == "wrong_cp_seid":
        packets[3]["pfcp"]["header_seid"] = 999
    elif change == "wrong_seq":
        packets[3]["pfcp"]["sequence"] = 999
    elif change == "early_data":
        packets[5]["timestamp_utc_epoch"] = 102
    elif change == "wrong_ue":
        packets[5]["inner_dst"] = "10.45.0.3"
    elif change == "wrong_teid":
        packets[5]["teid"] = 999
    elif change == "wrong_peer":
        packets[5]["dst"] = "127.0.0.8"
    else:
        addresses = json.loads(snapshot["ue"]["interfaces"]["stdout"])
        extra = deepcopy(addresses[0]["addr_info"][0])
        extra["local"] = "10.45.0.3"
        addresses[0]["addr_info"].append(extra)
        snapshot["ue"]["interfaces"]["stdout"] = json.dumps(addresses)
    monkeypatch.setattr(mapping, "enriched_facts", lambda _: facts)
    assert not mapping.map_sessions(snapshot)["mappings"][0]["observed_bidirectional_n3_mapping"]
