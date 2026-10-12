"""New inner-dataplane calibration captures, only inside explicitly owned lab containers."""

import argparse
import base64
import json
import time
from pathlib import Path

import diagnostic_control as observed

legacy = observed.legacy
CONDITIONS = ("inner-request-filter", "inner-reply-filter", "ogstun-admin-down")


def inject(condition):
    if condition == "ogstun-admin-down":
        return legacy.command(["ip", "link", "set", "ogstun", "down"])
    if condition not in CONDITIONS:
        raise ValueError("unknown calibration injection")
    request = condition == "inner-request-filter"
    return legacy.command(
        [
            "iptables",
            "-I",
            "INPUT" if request else "OUTPUT",
            "1",
            "-i" if request else "-o",
            "ogstun",
            "-p",
            "icmp",
            "--icmp-type",
            "echo-request" if request else "echo-reply",
            "-j",
            "DROP",
        ]
    )


def operation(name, role, condition=None):
    if name == "boot":
        return legacy.boot(role)
    if name == "health":
        return legacy.command(
            ["ping", "-n", "-I", "uesimtun0", "-c", "5", "-i", ".2", "-W", "1", "10.45.0.1"]
        )
    if name == "snapshot":
        return observed.snapshot(role)
    if name == "inject":
        return inject(condition)
    if name == "verify":
        return {
            "input": legacy.command(["iptables", "-nvxL", "INPUT"]),
            "output": legacy.command(["iptables", "-nvxL", "OUTPUT"]),
            "ogstun": legacy.command(["ip", "-json", "link", "show", "ogstun"]),
        }
    if name == "cleanup":
        return {
            "input": legacy.command(["iptables", "-F", "INPUT"]),
            "output": legacy.command(["iptables", "-F", "OUTPUT"]),
            "ogstun": legacy.command(["ip", "link", "set", "ogstun", "up"]),
        }
    if name == "capture-start":
        legacy.stop("capture")
        path = legacy.ROOT / "e1-candidate.pcap"
        path.unlink(missing_ok=True)
        pid = legacy.start(
            "capture",
            [
                "tcpdump",
                "-i",
                "any",
                "-s",
                "65535",
                "-U",
                "-w",
                str(path),
                "udp port 2152 or udp port 8805 or icmp",
            ],
        )
        time.sleep(0.3)
        return {"pid": pid, "snaplen": 65535}
    if name == "capture-end":
        legacy.stop("capture")
        return {
            "capture_base64": base64.b64encode(
                (legacy.ROOT / "e1-candidate.pcap").read_bytes()
            ).decode(),
            "capture_position": "owned core any interface; ingress presence is not delivery proof",
        }
    raise ValueError("unknown operation")


if __name__ == "__main__":
    if not Path("/.dockerenv").exists() or not Path("/control/candidate_control.py").exists():
        raise RuntimeError("dedicated mounted lab container required")
    parser = argparse.ArgumentParser()
    parser.add_argument("operation")
    parser.add_argument("--role", choices=["core", "ue"], default="core")
    parser.add_argument("--condition")
    args = parser.parse_args()
    print(json.dumps(operation(args.operation, args.role, args.condition)))
