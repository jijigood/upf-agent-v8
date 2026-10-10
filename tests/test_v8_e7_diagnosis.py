"""PCAP provenance, finite diagnostic output, and hidden-truth boundaries."""

import ast
import base64
import importlib.util
import os
import signal
import socket
import struct
import subprocess
import sys
import time
from pathlib import Path

import pytest
from pydantic import ValidationError

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location(
    "e7_diagnosis_under_test", SCRIPTS / "v8_e7_diagnosis.py"
)
diagnosis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnosis)
sys.path.pop(0)


def packet_capture():
    inner = bytearray(20)
    inner[0], inner[9] = 0x45, 1
    inner[12:16], inner[16:20] = socket.inet_aton("10.45.0.2"), socket.inet_aton("10.45.0.1")
    gtp = struct.pack("!BBHI", 0x30, 255, 28, 123) + inner + bytes([8])
    udp = struct.pack("!HHHH", 2152, 2152, len(gtp) + 8, 0) + gtp
    ip = bytearray(20)
    ip[0], ip[9] = 0x45, 17
    ip[12:16], ip[16:20] = socket.inet_aton("127.0.0.1"), socket.inet_aton("127.0.0.7")
    frame = bytes(12) + b"\x08\x00" + ip + udp
    return (
        struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
        + struct.pack("<IIII", 100, 123456, len(frame), len(frame))
        + frame
    )


def test_real_packet_offsets_direction_teid_and_clock_are_preserved():
    result = diagnosis.pcap_packets(base64.b64encode(packet_capture()).decode())
    packet = result["packets"][0]
    assert packet["file_byte_start"] == 40
    assert packet["timestamp_utc_epoch"] == pytest.approx(100.123456)
    assert (packet["src"], packet["dst"], packet["teid"]) == ("127.0.0.1", "127.0.0.7", 123)
    assert packet["icmp_type_numeric"] == 8 and packet["inner_src"] == "10.45.0.2"
    assert not result["application_delivery_proven"]


@pytest.mark.parametrize("flags", [0x30, 0x31, 0x32, 0x33, 0x34, 0x37])
def test_gtp_optional_and_extension_layouts_decode_inner_ipv4(flags):
    capture = bytearray(packet_capture())
    gtp_start = 40 + 14 + 20 + 8
    optional = bytes([0, 1, 0, 0x85 if flags & 4 else 0]) if flags & 7 else b""
    extensions = bytes([1, 0x10, 1, 0x40, 1, 0, 0, 0]) if flags & 4 else b""
    capture[gtp_start] = flags
    capture[gtp_start + 8 : gtp_start + 8] = optional + extensions
    struct.pack_into("<II", capture, 32, len(capture) - 40, len(capture) - 40)
    packet = diagnosis.pcap_packets(base64.b64encode(capture).decode())["packets"][0]
    assert packet["gtp_header_bytes"] == 8 + len(optional) + len(extensions)
    assert packet["inner_src"] == "10.45.0.2" and packet["icmp_type_numeric"] == 8
    assert packet["teid"] == 123


@pytest.mark.parametrize(
    "body,error",
    [
        (b"", "optional"),
        (bytes([0, 0, 0, 0x85]), "truncated"),
        (bytes([0, 0, 0, 0x85, 0]), "zero-length"),
        (bytes([0, 0, 0, 0x85, 2, 0, 0, 0]), "truncated"),
    ],
)
def test_malformed_gtp_extension_preserves_outer_evidence_without_guessing(body, error):
    capture = bytearray(packet_capture()[: 40 + 14 + 20 + 8 + 8])
    capture[40 + 14 + 20 + 8] = 0x34
    capture.extend(body)
    struct.pack_into("<II", capture, 32, len(capture) - 40, len(capture) - 40)
    packet = diagnosis.pcap_packets(base64.b64encode(capture).decode())["packets"][0]
    assert error in packet["gtp_decode_error"]
    assert packet["teid"] == 123 and "inner_src" not in packet


@pytest.mark.parametrize("cut", [1, 23, 30, 40, 50])
def test_truncated_capture_never_becomes_zero_packet_evidence(cut):
    with pytest.raises(ValueError, match="truncated"):
        diagnosis.pcap_packets(base64.b64encode(packet_capture()[:cut]).decode())


def test_root_cause_candidates_cannot_invent_or_duplicate_cause_codes():
    hypothesis = {"cause": "upf_process_suspended", "rationale": "观测", "evidence_ids": ["f1"]}
    step = {
        "target": "upf",
        "action": "read_process_state",
        "text": "只读核验",
        "evidence_ids": ["f1"],
    }
    with pytest.raises(ValidationError):
        diagnosis.RootCauseReport(
            hypotheses=[hypothesis, hypothesis], investigations=[step], missing_evidence=[]
        )
    with pytest.raises(ValidationError):
        diagnosis.RootCauseReport(
            hypotheses=[{**hypothesis, "cause": "invented"}],
            investigations=[step],
            missing_evidence=[],
        )

    with pytest.raises(ValidationError):
        diagnosis.RootCauseReport(
            hypotheses=[hypothesis],
            investigations=[{**step, "claimed_executed": True}],
            missing_evidence=[],
        )


def test_missing_citation_is_rejected_by_schema_and_runtime():
    schema = diagnosis.RootCauseReport.model_json_schema()
    for name in ["Hypothesis", "Investigation"]:
        assert schema["$defs"][name]["properties"]["evidence_ids"]["minItems"] == 1
    with pytest.raises(ValidationError):
        diagnosis.Investigation(
            target="smf",
            action="read_packet_capture",
            text="实际失败原文中的无引证调查",
            evidence_ids=[],
        )


@pytest.mark.parametrize("field", ["rationale", "text", "missing_evidence"])
def test_repeated_narrative_cannot_exhaust_diagnostic_completion(field):
    report = {
        "hypotheses": [
            {"cause": "unknown", "rationale": "缺少应用收包证据", "evidence_ids": ["f001"]}
        ],
        "investigations": [
            {
                "target": "upf",
                "action": "read_packet_capture",
                "text": "核对接收点与方向",
                "evidence_ids": ["f001"],
            }
        ],
        "missing_evidence": [],
    }
    diagnosis.RootCauseReport.model_validate(report)
    # The actual failed generation repeated a clause up to the previous 500/300
    # character limits. Reject that expansion before it can consume the full budget.
    repeated = "进程状态为S，表明调度未激活；" * 12
    if field == "rationale":
        report["hypotheses"][0][field] = repeated
    elif field == "text":
        report["investigations"][0][field] = repeated
    else:
        report[field] = [repeated]
    with pytest.raises(ValidationError):
        diagnosis.RootCauseReport.model_validate(report)
    schema = diagnosis.RootCauseReport.model_json_schema()
    assert schema["$defs"]["Hypothesis"]["properties"]["rationale"]["maxLength"] == 64
    assert schema["$defs"]["Investigation"]["properties"]["text"]["maxLength"] == 48
    assert schema["properties"]["missing_evidence"]["items"]["maxLength"] == 64


def test_owned_zombie_cleanup_does_not_wait_for_container_pid1_reaping(tmp_path):
    # Execute the production stop function without importing container-only MongoDB.
    tree = ast.parse((SCRIPTS.parent / "lab/e7/control.py").read_text())
    stop = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "stop")
    namespace = {"ROOT": tmp_path, "Path": Path, "os": os, "signal": signal, "time": time}
    exec(compile(ast.Module(body=[stop], type_ignores=[]), "production_stop", "exec"), namespace)
    child = os.fork()
    if child == 0:
        os.setsid()
        os._exit(0)
    try:
        status = Path(f"/proc/{child}/status")
        for _ in range(100):
            if "State:\tZ" in status.read_text():
                break
            time.sleep(0.01)
        else:
            pytest.fail("owned test child did not exit")
        (tmp_path / "capture.pid").write_text(str(child))

        def unnecessary_wait(_):
            pytest.fail("zombie cleanup must not wait for /proc disappearance")

        from types import SimpleNamespace

        namespace["time"] = SimpleNamespace(sleep=unnecessary_wait)
        namespace["stop"]("capture")
        assert not (tmp_path / "capture.pid").exists()
    finally:
        os.waitpid(child, 0)


@pytest.mark.parametrize(
    "state,allowed",
    [("S (sleeping)", False), ("R (running)", False), ("T (stopped)", True), ("unknown", True)],
)
def test_process_suspension_requires_a_non_contradictory_visible_state(state, allowed):
    facts = [{"object_id": "upf", "locator": "/core/process_states/upf", "value": {"state": state}}]
    assert ("upf_process_suspended" in diagnosis.eligible_causes(facts)) == allowed


def test_diagnostic_guard_rejects_truth_network_and_lab_commands(tmp_path):
    visible, output, private = [tmp_path / n for n in ["input", "output", "private"]]
    for p in [visible, output, private]:
        p.mkdir()
    (private / "truth.json").write_text("hidden")
    code = f"""import sys,pathlib,socket,subprocess
sys.path.insert(0,{str(SCRIPTS)!r})
from v8_e7_diagnosis import guard
visible=pathlib.Path({str(visible)!r});output=pathlib.Path({str(output)!r});private=pathlib.Path({str(private)!r})
guard(visible,output,private,18000)
checks=[lambda: (private/'truth.json').read_text(),lambda: (private/'truth.json').unlink(),
        lambda: socket.socket().connect(('127.0.0.1',1)),lambda: subprocess.run(['true'])]
for check in checks:
 try: check()
 except PermissionError: pass
 else: raise AssertionError('guard bypass')
(output/'allowed.json').write_text('allowed')
"""
    result = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (private / "truth.json").read_text() == "hidden"


def test_log_storm_projection_records_omissions_and_keeps_raw_facts():
    events = [
        {"line": n, "message": "同一故障产生大量日志。" * 80, "severity": "INFO"}
        for n in range(1, 101)
    ]
    facts = [
        {
            "evidence_id": "f001",
            "object_id": "smf",
            "locator": "/core/logs_and_config/smf.log",
            "value": {"events": events},
        }
    ]
    before = repr(facts)
    projected = diagnosis.model_view(facts)[0]["value"]
    assert projected["omitted_events"] > 0
    assert projected["total_events"] == 100
    assert projected["latest_events"][-1]["line"] == 100
    assert len(projected["latest_events"]) + projected["omitted_events"] == 100
    assert repr(facts) == before
