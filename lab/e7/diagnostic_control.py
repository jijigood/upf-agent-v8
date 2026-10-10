"""Read-only diagnostic capture and additional independent E7 injection controls.

Only executed inside the owned lab container; injection receipts stay private.
"""

import argparse
import base64
import ipaddress
import json
import os
import signal
import time
from pathlib import Path

import control as legacy


def capture_start():
    legacy.stop("capture")
    path = legacy.ROOT / "diagnostic.pcap"
    path.unlink(missing_ok=True)
    pid = legacy.start(
        "capture",
        [
            "tcpdump",
            "-i",
            "lo",
            "-s",
            "256",
            "-U",
            "-w",
            str(path),
            "udp port 2152 or udp port 8805",
        ],
    )
    time.sleep(0.3)
    return {"pid": pid}


def capture_end():
    legacy.stop("capture")
    path = legacy.ROOT / "diagnostic.pcap"
    return {
        "capture_base64": base64.b64encode(path.read_bytes()).decode(),
        "capture_position": "core loopback wire capture before INPUT filtering",
        "scope": "packet presence is not proof of application delivery",
    }


def process_states(role):
    states = {}
    for name in ("upf", "smf", "gnb") if role == "core" else ("ue",):
        pid_file = legacy.ROOT / (name + ".pid")
        if pid_file.exists():
            pid = int(pid_file.read_text())
            path = Path(f"/proc/{pid}/status")
            states[name] = path.read_text() if path.exists() else "process absent"
    return states


def inject(condition):
    if condition in {"smf-paused", "gnb-paused", "ue-paused"}:
        name = condition.split("-", 1)[0]
        pid = int((legacy.ROOT / (name + ".pid")).read_text())
        os.kill(pid, signal.SIGSTOP)
        return {"pid": pid, "signal": "SIGSTOP"}
    if condition.startswith("pfcp-"):
        args = ["iptables", "-I", "INPUT", "1", "-p", "udp", "--dport", "8805"]
        if condition != "pfcp-bilateral-loss":
            args += ["-s", "127.0.0.4" if condition == "pfcp-request-loss" else "127.0.0.7"]
        return legacy.command(args + ["-j", "DROP"])
    return legacy.inject(condition)


def cleanup(role):
    for name in ("smf", "gnb", "upf") if role == "core" else ("ue",):
        pid_file = legacy.ROOT / (name + ".pid")
        if pid_file.exists():
            try:
                os.kill(int(pid_file.read_text()), signal.SIGCONT)
            except ProcessLookupError:
                pass
    if role == "ue":
        return legacy.cleanup(role)
    # Paused SMF/PFCP loss can leave pending sessions in AMF/SMF. Resume alone
    # does not restore them. Reset all owned NFs before starting a fresh UE.
    # This is harness reset, never an agent-selected repair or measured MTTR.
    firewall = legacy.command(["iptables", "-F", "INPUT"])
    legacy.stop("gnb")
    for name in reversed(legacy.NF):
        legacy.stop(name)
    restarted = {}
    for name in legacy.NF:
        restarted[name] = legacy.nf_start(name)
        time.sleep(0.2)
    time.sleep(4)
    return {
        "firewall": firewall,
        "restarted_owned_nfs": restarted,
        "gnb_pid": legacy.gnb_start(),
        "kind": "independent harness reset; not agent repair or MTTR",
    }


def snapshot(role):
    return {**legacy.snapshot(role), "process_states": process_states(role)}


if __name__ == "__main__":
    if not Path("/.dockerenv").exists() or not Path("/control/diagnostic_control.py").exists():
        raise RuntimeError("dedicated owned lab container required")
    parser = argparse.ArgumentParser()
    parser.add_argument("operation")
    parser.add_argument("--role", choices=["core", "ue"], default="core")
    parser.add_argument("--condition")
    parser.add_argument("--target")
    args = parser.parse_args()
    if args.operation == "capture-start":
        result = capture_start()
    elif args.operation == "capture-end":
        result = capture_end()
    elif args.operation == "downlink-probe":
        target = ipaddress.IPv4Address(args.target)
        if target not in ipaddress.IPv4Network("10.45.0.0/16"):
            raise ValueError("downlink target must be an observed local UE address")
        result = legacy.command(
            ["ping", "-n", "-I", "ogstun", "-c", "5", "-i", ".2", "-W", "1", str(target)]
        )
    elif args.operation == "snapshot":
        result = snapshot(args.role)
    elif args.operation == "inject":
        result = inject(args.condition)
    elif args.operation == "cleanup":
        result = cleanup(args.role)
    elif args.operation == "boot":
        result = legacy.boot(args.role)
    elif args.operation == "health":
        result = legacy.command(
            ["ping", "-n", "-I", "uesimtun0", "-c", "5", "-i", ".2", "-W", "1", "10.45.0.1"]
        )
    elif args.operation == "verify":
        result = {
            "firewall": legacy.command(["iptables", "-nvxL", "INPUT"]),
            "process_states": process_states(args.role),
        }
    else:
        raise ValueError("unknown diagnostic operation")
    print(json.dumps(result))
