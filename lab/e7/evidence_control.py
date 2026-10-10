"""Owned lab capture with full snaplen; historical controller remains unchanged."""

import argparse
import ipaddress
import json
import time
from pathlib import Path

import diagnostic_control as original


def capture_start():
    original.legacy.stop("capture")
    path = original.legacy.ROOT / "diagnostic.pcap"
    path.unlink(missing_ok=True)
    pid = original.legacy.start(
        "capture",
        [
            "tcpdump",
            "-i",
            "lo",
            "-s",
            "65535",
            "-U",
            "-w",
            str(path),
            "udp port 2152 or udp port 8805",
        ],
    )
    time.sleep(0.3)
    return {"pid": pid, "snaplen": 65535}


if __name__ == "__main__":
    if not Path("/.dockerenv").exists():
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
        result = original.capture_end()
        result["snaplen"] = 65535
    elif args.operation == "downlink-probe":
        target = ipaddress.IPv4Address(args.target)
        if target not in ipaddress.IPv4Network("10.45.0.0/16"):
            raise ValueError("local observed UE address required")
        result = original.legacy.command(
            ["ping", "-n", "-I", "ogstun", "-c", "5", "-i", ".2", "-W", "1", str(target)]
        )
    elif args.operation == "snapshot":
        result = original.snapshot(args.role)
    elif args.operation == "inject":
        result = original.inject(args.condition)
    elif args.operation == "cleanup":
        result = original.cleanup(args.role)
    elif args.operation == "boot":
        result = original.legacy.boot(args.role)
    elif args.operation == "health":
        result = original.legacy.command(
            ["ping", "-n", "-I", "uesimtun0", "-c", "5", "-i", ".2", "-W", "1", "10.45.0.1"]
        )
    elif args.operation == "verify":
        result = {
            "firewall": original.legacy.command(["iptables", "-nvxL", "INPUT"]),
            "process_states": original.process_states(args.role),
        }
    else:
        raise ValueError("unknown operation")
    print(json.dumps(result))
