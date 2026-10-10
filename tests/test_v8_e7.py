import importlib.util
import json
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest


def load(name):
    p = Path(__file__).resolve().parents[1] / "scripts" / (name + ".py")
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


agent = load("v8_e7_agent")
runner = load("v8_e7_runner")


def test_log_parser_retains_ansi_utf8_and_unmatched_bytes():
    text = "\x1b[32m10/10 10:00:00.123: [pfcp] INFO: 对端关联\x1b[0m\nunknown line\n"
    rows = agent.parse_log(text, "upf")
    assert rows[0]["parsed_header"] and rows[0]["message"] == "对端关联"
    assert rows[0]["severity"] == "INFO"
    assert not rows[1]["parsed_header"]
    assert rows[-1]["byte_end"] == len(text.encode())
    assert rows[1]["byte_start"] == rows[0]["byte_end"]
    assert all(r["timestamp_inference"] is None for r in rows)


def test_ueransim_header_and_unknown_kept():
    rows = agent.parse_log("[2026-10-10 10:00:00.123] [nas] [error] PDU reject\n?", "ue")
    assert rows[0]["severity"] == "error"
    assert rows[0]["message"] == "PDU reject"
    assert not rows[1]["parsed_header"]


def test_snapshot_only_keeps_current_epoch():
    before = {
        r: {"logs_and_config": {"a.log": "old\n", "gnb.yaml": "normal"}} for r in ("core", "ue")
    }
    after = {
        r: {"logs_and_config": {"a.log": "old\nnew\n", "gnb.yaml": "new config"}}
        for r in ("core", "ue")
    }
    result = runner.visible_delta(before, after)
    assert result["core"]["logs_and_config"] == {"a.log": "new\n", "gnb.yaml": "new config"}
    with pytest.raises(ValueError, match="rotation"):
        runner.visible_delta(before, after)


@pytest.mark.parametrize("condition", ["n3-ul-loss", "n3-dl-loss", "upf-n3-block"])
def test_packet_loss_requires_counter_not_only_failed_ping(condition):
    impaired = {"returncode": 1}
    external = {"firewall": {"stdout": " 0 0 DROP udp"}, "gnb_process": "State:\tS"}
    assert not runner.injection_verified(condition, impaired, external, {})
    external["firewall"]["stdout"] = " 3 360 DROP udp"
    assert runner.injection_verified(condition, impaired, external, {})
    assert not runner.injection_verified(condition, {"returncode": 0}, external, {})
    external["gnb_process"] = "State:\tZ"
    assert not runner.injection_verified(condition, impaired, external, {})


def test_paused_process_and_config_mismatch_truth():
    assert not runner.injection_verified(
        "upf-paused", {"returncode": 1}, {"upf_process": "State:\tS"}, {}
    )
    assert runner.injection_verified(
        "upf-paused", {"returncode": 1}, {"upf_process": "State:\tT"}, {}
    )
    snapshot = {"ue": {"logs_and_config": {"ue.yaml": "apn: unsubscribed", "ue.log": ""}}}
    assert not runner.injection_verified("ue-dnn-mismatch", {"returncode": 1}, {}, snapshot)
    snapshot["ue"]["logs_and_config"]["ue.log"] = "MM status DNN_NOT_SUPPORTED_OR_NOT_SUBSCRIBED"
    snapshot["core"] = {"logs_and_config": {"amf.log": ""}}
    assert not runner.injection_verified("ue-dnn-mismatch", {"returncode": 1}, {}, snapshot)
    snapshot["core"]["logs_and_config"]["amf.log"] = (
        'Ue requested DNN "unsubscribed" Not Supported OR Not Subscribed'
    )
    assert runner.injection_verified("ue-dnn-mismatch", {"returncode": 1}, {}, snapshot)


def test_resource_ownership_protection(monkeypatch):
    monkeypatch.setattr(
        runner,
        "command",
        lambda _: {
            "returncode": 0,
            "stdout": json.dumps([{"Config": {"Labels": {runner.LABEL: "someone-else"}}}]),
        },
    )
    with pytest.raises(ValueError, match="unowned"):
        runner.assert_owned("container", "ours")


def test_agent_ingests_runtime_windows_and_does_not_hide_tool_failures(tmp_path):
    """Contract test using declared test fixtures, outside experimental denominators."""
    visible, private = tmp_path / "input", tmp_path / "private"
    visible.mkdir()
    private.mkdir()
    now = datetime.now(UTC)
    body = {
        "core": {
            "logs_and_config": {
                "upf.log": "10/10 10:00:00.123: [upf] INFO: Runtime fixture\n",
                "smf.log": "10/10 10:00:00.123: [smf] INFO: Runtime fixture\n",
            }
        },
        "ue": {"logs_and_config": {}},
        "window_start": (now - timedelta(seconds=1)).isoformat(),
        "window_end": now.isoformat(),
    }
    (visible / "snapshot.json").write_text(json.dumps(body))
    script = Path(__file__).resolve().parents[1] / "scripts/v8_e7_agent.py"
    p = subprocess.run(
        [
            sys.executable,
            str(script),
            "--input",
            str(visible),
            "--output",
            str(tmp_path / "result"),
            "--private-root",
            str(private),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert p.returncode == 0, p.stderr
    result = json.loads(p.stdout)
    assert result["binding_count"] == result["expected_runtime_observations"] == 2
    assert not result["tool_errors"] and result["pass"]


def test_agent_guard_blocks_truth_mutation_network_and_commands(tmp_path):
    output, private = tmp_path / "output", tmp_path / "private"
    output.mkdir()
    private.mkdir()
    (private / "truth.json").write_text("hidden")
    script = f"""import sys, pathlib, socket, subprocess
sys.path.insert(0, {str(Path(__file__).resolve().parents[1] / "scripts")!r})
from v8_e7_agent import guard
out=pathlib.Path({str(output)!r})
truth=pathlib.Path({str(private / "truth.json")!r})
guard(out, out, truth.parent)
checks=[lambda: truth.read_text(), lambda: truth.unlink(),
        lambda: socket.socket().connect(('127.0.0.1', 1)), lambda: subprocess.run(['true'])]
for check in checks:
    try: check()
    except PermissionError: pass
    else: raise AssertionError('guard bypass')
(out/'result.json').write_text('allowed')
"""
    p = subprocess.run([sys.executable, "-B", "-c", script], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert (private / "truth.json").read_text() == "hidden"
    assert (output / "result.json").read_text() == "allowed"


@pytest.mark.parametrize("baseline_ok", [False, True])
def test_lifecycle_cleans_owned_resources_and_stops_after_failed_recovery(
    tmp_path, monkeypatch, baseline_ok
):
    project = tmp_path / "project"
    for name in (
        "lab/e7/Dockerfile",
        "lab/e7/control.py",
        "scripts/v8_e7_runner.py",
        "scripts/v8_e7_agent.py",
    ):
        p = project / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("test helper\n")
    output = tmp_path / "experiment"
    calls = []

    def fake_command(argv, timeout=60):
        calls.append(argv)
        if argv[:1] != ["docker"]:
            return {"returncode": 1, "stdout": "", "stderr": "method failed"}
        return {"returncode": 0, "stdout": "resource", "stderr": ""}

    monkeypatch.setattr(runner, "command", fake_command)
    monkeypatch.setattr(
        runner,
        "assert_owned",
        lambda *args: {"HostConfig": {"Privileged": False, "PortBindings": {}}},
    )
    snapshot = {"logs_and_config": {}}
    monkeypatch.setattr(runner, "control", lambda *args: snapshot if args[1] == "snapshot" else {})
    health = iter([{"pass": baseline_ok}, {"pass": True}, {"pass": False}])
    monkeypatch.setattr(runner, "wait_health", lambda _: next(health))
    monkeypatch.setattr(runner, "injection_verified", lambda *args: True)
    monkeypatch.setattr(runner.time, "sleep", lambda _: None)
    result = runner.run(project, output, "sha256:" + "a" * 64, 3)
    assert not result["pass"] and result["teardown_pass"]
    assert sum(c[:3] == ["docker", "rm", "-f"] for c in calls) == 2
    assert sum(c[:3] == ["docker", "network", "rm"] for c in calls) == 1
    if baseline_ok:
        assert result["completed"] == 1
        assert result["rows"][0]["cleanup_failure"]
        assert result["rows"][0]["method_failure"]
    else:
        assert result["completed"] == 0
