"""Independent isolated E7 lifecycle: real 5GC health, injection, capture, cleanup.

The existing Engine is exercised as a log-observation integration probe only.
Root-cause quality and formal human-approved semantic scoring remain separate.
"""

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

CONDITIONS = (
    "n3-ul-loss",
    "n3-dl-loss",
    "upf-paused",
    "upf-n3-block",
    "gnb-gtp-mismatch",
    "ue-dnn-mismatch",
)
LABEL = "upf.e7.owner"


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def command(argv, timeout=60):
    started = time.perf_counter()
    p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    return {
        "argv": argv,
        "returncode": p.returncode,
        "stdout": p.stdout,
        "stderr": p.stderr,
        "seconds": time.perf_counter() - started,
    }


def control(container, operation, role="core", condition=None):
    argv = [
        "docker",
        "exec",
        container,
        "python3",
        "/control/control.py",
        operation,
        "--role",
        role,
    ]
    if condition:
        argv += ["--condition", condition]
    receipt = command(argv)
    if receipt["returncode"]:
        raise RuntimeError(json.dumps(receipt))
    return json.loads(receipt["stdout"])


def wait_health(ue, timeout=45):
    deadline = time.monotonic() + timeout
    receipts = []
    while time.monotonic() < deadline:
        r = control(ue, "health", "ue")
        receipts.append(r)
        if r["returncode"] == 0 and "0% packet loss" in r["stdout"]:
            return {"pass": True, "attempts": receipts}
        time.sleep(1)
    return {"pass": False, "attempts": receipts}


def assert_owned(name, owner, network=False):
    kind = ["network", "inspect"] if network else ["inspect"]
    r = command(["docker", *kind, name])
    if r["returncode"]:
        raise RuntimeError("cannot inspect owned lab resource")
    body = json.loads(r["stdout"])[0]
    labels = body.get("Labels", {}) if network else body["Config"].get("Labels", {})
    if labels.get(LABEL) != owner:
        raise ValueError("refuse to mutate unowned Docker resource")
    return body


def visible_delta(before, after):
    """Keep normal config, retain only new log bytes within this capture interval."""
    for role in ("core", "ue"):
        for name, text in after[role]["logs_and_config"].items():
            if name.endswith(".log"):
                old = before[role]["logs_and_config"].get(name, "")
                if not text.startswith(old):
                    raise ValueError("log rotation/truncation requires a new capture epoch")
                after[role]["logs_and_config"][name] = text[len(old) :]
    return after


def injection_verified(condition, impaired, external, snapshot):
    if impaired["returncode"] == 0:
        return False
    if condition in {"n3-ul-loss", "n3-dl-loss", "upf-n3-block"}:
        import re

        return "State:\tZ" not in external["gnb_process"] and bool(
            re.search(r"^\s*[1-9]\d*\s+\d+\s+DROP\s+udp", external["firewall"]["stdout"], re.M)
        )
    if condition == "upf-paused":
        return "State:\tT" in external["upf_process"]
    if condition == "gnb-gtp-mismatch":
        return "gtpAdvertiseIp: 127.0.0.8" in snapshot["core"]["logs_and_config"]["gnb.yaml"]
    if condition == "ue-dnn-mismatch":
        return (
            "apn: unsubscribed" in snapshot["ue"]["logs_and_config"]["ue.yaml"]
            and "DNN_NOT_SUPPORTED_OR_NOT_SUBSCRIBED"
            in snapshot["ue"]["logs_and_config"].get("ue.log", "")
            and 'Ue requested DNN "unsubscribed" Not Supported OR Not Subscribed'
            in snapshot["core"]["logs_and_config"].get("amf.log", "")
        )
    return False


def run(project, output, image, repetitions):
    if output.exists() or repetitions != 3:
        raise ValueError("new output ID and preregistered 3 repeats required")
    output.mkdir(parents=True)
    owner = output.name
    suffix = hashlib.sha256(str(output).encode()).hexdigest()[:10]
    network, core, ue = ("upf-e7-" + suffix + n for n in ("-net", "-core", "-ue"))
    private = output / "private"
    private.mkdir()
    write(
        output / "protocol.json",
        {
            "conditions": CONDITIONS,
            "repetitions": repetitions,
            "pilot_rounds": 18,
            "image": image,
            "synthetic": False,
            "reviewed": False,
            "method": "v8-log-observation-integration",
            "root_cause_top1": None,
            "root_cause_top3": None,
            "formal_quality": False,
            "health_target": "UE TUN to core ogstun, 5 ICMP echo requests, zero loss",
            "external_network": False,
            "agent_execution": False,
            "failure_denominators": [
                "health_error",
                "harness_error",
                "method_failure",
                "cleanup_failure",
            ],
        },
    )
    # Freeze exact helper bytes before any network mutation.
    helper_names = [
        "lab/e7/Dockerfile",
        "lab/e7/control.py",
        "scripts/v8_e7_runner.py",
        "scripts/v8_e7_agent.py",
    ]
    hashes = {}
    for name in helper_names:
        raw = (project / name).read_bytes()
        p = output / "code" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
    write(output / "code-hashes.json", hashes)
    created = []
    rows = []
    startup, teardown = [], []
    try:
        r = command(
            [
                "docker",
                "network",
                "create",
                "--internal",
                "--subnet",
                "10.208.7.0/24",
                "--label",
                LABEL + "=" + owner,
                network,
            ]
        )
        startup.append(r)
        if r["returncode"]:
            raise RuntimeError("isolated network create failed")
        created.append(network)
        for name, ip in ((core, "10.208.7.2"), (ue, "10.208.7.3")):
            r = command(
                [
                    "docker",
                    "run",
                    "-d",
                    "--runtime",
                    "runc",
                    "--name",
                    name,
                    "--label",
                    LABEL + "=" + owner,
                    "--network",
                    network,
                    "--ip",
                    ip,
                    "--cap-add",
                    "NET_ADMIN",
                    "--device",
                    "/dev/net/tun",
                    "--memory",
                    "2g",
                    "--cpus",
                    "2",
                    "-v",
                    str(output / "code/lab/e7") + ":/control:ro",
                    image,
                ]
            )
            startup.append(r)
            if r["returncode"]:
                raise RuntimeError("isolated container create failed")
            created.append(name)
            inspected = assert_owned(name, owner)
            if inspected["HostConfig"]["Privileged"] or inspected["HostConfig"]["PortBindings"]:
                raise ValueError("lab isolation violated")
            write(private / (name + "-inspect.json"), inspected)
        write(private / "core-boot.json", control(core, "boot"))
        write(private / "ue-boot.json", control(ue, "boot", "ue"))
        baseline = wait_health(ue)
        write(output / "baseline-health.json", baseline)
        write(private / "baseline-core.json", control(core, "snapshot"))
        write(private / "baseline-ue.json", control(ue, "snapshot", "ue"))
        if not baseline["pass"]:
            raise RuntimeError("healthy 5GC baseline failed; no injection rounds started")
        for condition in CONDITIONS:
            for repeat in range(1, repetitions + 1):
                number = len(rows) + 1
                round_root = output / "rounds" / f"round-{number:03d}"
                round_private = private / f"round-{number:03d}"
                row = {
                    "round": number,
                    "condition": condition,
                    "repeat": repeat,
                    "health_error": False,
                    "harness_error": False,
                    "method_failure": False,
                    "cleanup_failure": False,
                    "injection_verified": False,
                    "integration_pass": False,
                    "recovered": False,
                }
                health = wait_health(ue)
                write(round_private / "health-before.json", health)
                if not health["pass"]:
                    row["health_error"] = True
                    rows.append(row)
                    break
                start = datetime.now(UTC).isoformat()
                before = {"core": control(core, "snapshot"), "ue": control(ue, "snapshot", "ue")}
                role, target = ("ue", ue) if condition == "ue-dnn-mismatch" else ("core", core)
                try:
                    write(round_private / "inject.json", control(target, "inject", role, condition))
                    if condition == "gnb-gtp-mismatch":
                        control(ue, "boot", "ue")
                    time.sleep(3)
                    impaired = control(ue, "health", "ue")
                    external = control(core, "verify")
                    write(
                        round_private / "external-verification.json",
                        {"probe": impaired, "independent_state": external},
                    )
                    snapshot = {
                        "core": control(core, "snapshot"),
                        "ue": control(ue, "snapshot", "ue"),
                        "window_start": start,
                        "window_end": datetime.now(UTC).isoformat(),
                    }
                    snapshot = visible_delta(before, snapshot)
                    row["injection_verified"] = injection_verified(
                        condition, impaired, external, snapshot
                    )
                    row["harness_error"] = not row["injection_verified"]
                    public_input = round_root / "input"
                    write(public_input / "snapshot.json", snapshot)
                    write(
                        round_private / "truth.json",
                        {
                            "condition": condition,
                            "synthetic": False,
                            "verified": row["injection_verified"],
                            "expected_answer": condition,
                            "recovery_truth_source": "independent UE ping after controller cleanup",
                        },
                    )
                    if row["injection_verified"]:
                        p = command(
                            [
                                sys.executable,
                                str(output / "code/scripts/v8_e7_agent.py"),
                                "--input",
                                str(public_input),
                                "--output",
                                str(round_root / "agent"),
                                "--private-root",
                                str(private),
                            ],
                            timeout=60,
                        )
                        write(round_private / "agent-process.json", p)
                        row["method_failure"] = p["returncode"] != 0
                        if not row["method_failure"]:
                            integration = json.loads(
                                (round_root / "agent/integration.json").read_text()
                            )
                            row["integration_pass"] = integration["pass"]
                            row["method_failure"] = not integration["pass"]
                finally:
                    write(round_private / "cleanup-core.json", control(core, "cleanup"))
                    time.sleep(1)
                    write(round_private / "cleanup-ue.json", control(ue, "cleanup", "ue"))
                    recovered = wait_health(ue)
                    write(round_private / "health-after.json", recovered)
                    row["recovered"] = recovered["pass"]
                    row["cleanup_failure"] = not recovered["pass"]
                    rows.append(row)
                    write(output / "progress.json", rows)
                if row["cleanup_failure"]:
                    break
            if rows and (rows[-1]["health_error"] or rows[-1]["cleanup_failure"]):
                break
    except Exception as exc:
        write(output / "runner-error.json", {"type": type(exc).__name__, "message": str(exc)})
    finally:
        for name in reversed(created):
            is_network = name == network
            assert_owned(name, owner, is_network)
            teardown.append(
                command(
                    ["docker", "network", "rm", name]
                    if is_network
                    else ["docker", "rm", "-f", name]
                )
            )
        write(private / "startup.json", startup)
        write(private / "teardown.json", teardown)
    summary = {
        "rows": rows,
        "planned": 18,
        "completed": len(rows),
        "synthetic": False,
        "reviewed": False,
        "model_calls": 0,
        "root_cause_top1": None,
        "root_cause_top3": None,
        "formal_quality": False,
        "controlled_recovery_experiment": False,
        "injection_verified": sum(r["injection_verified"] for r in rows),
        "integration_pass": sum(r["integration_pass"] for r in rows),
        "recovered": sum(r["recovered"] for r in rows),
        "teardown_pass": bool(teardown) and all(r["returncode"] == 0 for r in teardown),
        "pass": len(rows) == 18
        and all(r["injection_verified"] and r["integration_pass"] and r["recovered"] for r in rows),
    }
    summary["pass"] &= summary["teardown_pass"]
    write(output / "summary.json", summary)
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--image", required=True, help="immutable sha256 Docker image ID")
    p.add_argument("--repetitions", type=int, default=3)
    a = p.parse_args()
    if not a.image.startswith("sha256:") or len(a.image) != 71:
        p.error("pin the built image by SHA256 ID")
    import signal

    def interrupted(signum, frame):
        raise RuntimeError("experiment interrupted; preserve all evidence and tear down owned lab")

    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    result = run(a.project.resolve(), a.output.resolve(), a.image, a.repetitions)
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}))
    raise SystemExit(0 if result["pass"] else 1)
