"""Fixed normal observations inside an owned E1 lab; no fault/write operation."""

import argparse
import base64
import json
import time
from pathlib import Path

import diagnostic_control as observed

legacy = observed.legacy


def operation(name, role):
    if name == "snapshot":
        result = observed.snapshot(role)
        if role == "core":
            result["filter_inventory"] = {
                chain: legacy.command(["iptables", "-nvxL", chain])
                for chain in ("INPUT", "OUTPUT", "FORWARD")
            }
        return result
    if name == "capture-start":
        legacy.stop("e1-normal-capture")
        path = legacy.ROOT / "e1-normal-capture.pcap"
        path.unlink(missing_ok=True)
        pid = legacy.start(
            "e1-normal-capture",
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
        return {"pid": pid, "snaplen": 65535, "namespace": role}
    if name == "capture-end":
        legacy.stop("e1-normal-capture")
        return {
            "capture_base64": base64.b64encode(
                (legacy.ROOT / "e1-normal-capture.pcap").read_bytes()
            ).decode(),
            "capture_position": f"owned {role} namespace any interface",
            "packet_matching_or_delivery_proved": False,
        }
    raise ValueError("unregistered normal observation")


if __name__ == "__main__":
    if not Path("/.dockerenv").exists() or not Path("/control/readonly_control.py").exists():
        raise RuntimeError("dedicated mounted lab container required")
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("snapshot", "capture-start", "capture-end"))
    parser.add_argument("--role", choices=("core", "ue"), required=True)
    args = parser.parse_args()
    print(json.dumps(operation(args.operation, args.role)))
