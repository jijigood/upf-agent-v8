"""Owned-container-only acquisition of fresh calibration and withheld fault inputs."""

import argparse
import ipaddress
import json
from pathlib import Path

import candidate_control as candidate

legacy = candidate.legacy
GATEWAY = "10.45.0.1"
CIDR = "10.45.0.0/16"
STATE = legacy.ROOT / "expanded-private-state.json"
HELDOUT_CONDITIONS = (
    "gateway-address-absent",
    "reply-blackhole-route",
    "reply-policy-prohibit",
    "inner-mtu-576-boundary-control",
)


def probe(size=56):
    return legacy.command(
        [
            "ping",
            "-n",
            "-I",
            "uesimtun0",
            "-c",
            "3",
            "-i",
            ".2",
            "-W",
            "1",
            "-M",
            "do",
            "-s",
            str(size),
            GATEWAY,
        ]
    )


def inventory():
    return {
        "addresses": legacy.command(["ip", "-json", "address", "show", "ogstun"]),
        "links": legacy.command(["ip", "-json", "link", "show", "ogstun"]),
        "routes": legacy.command(["ip", "-json", "route", "show", "table", "all"]),
        "rules": legacy.command(["ip", "-json", "rule", "show"]),
        **candidate.operation("verify", "core"),
    }


def checked(result):
    if result["returncode"]:
        raise RuntimeError(json.dumps(result))
    return result


def inject(condition, target):
    address = ipaddress.IPv4Address(target)
    if address not in ipaddress.IPv4Network(CIDR) or str(address) == GATEWAY:
        raise ValueError("injection target must be the observed owned UE address")
    previous = inventory()
    STATE.write_text(json.dumps({"condition": condition, "target": target, "before": previous}))
    if condition in candidate.CONDITIONS:
        return checked(candidate.inject(condition))
    commands = {
        "gateway-address-absent": ["ip", "address", "del", GATEWAY + "/16", "dev", "ogstun"],
        "reply-blackhole-route": ["ip", "route", "add", "blackhole", target + "/32"],
        "reply-policy-prohibit": [
            "ip",
            "rule",
            "add",
            "priority",
            "12001",
            "from",
            GATEWAY + "/32",
            "to",
            target + "/32",
            "prohibit",
        ],
        "inner-mtu-576": ["ip", "link", "set", "ogstun", "mtu", "576"],
        "inner-mtu-576-boundary-control": ["ip", "link", "set", "ogstun", "mtu", "576"],
    }
    if condition not in commands:
        raise ValueError("unknown acquisition condition")
    return checked(legacy.command(commands[condition]))


def cleanup():
    state = json.loads(STATE.read_text())
    condition, target = state["condition"], state["target"]
    if condition in candidate.CONDITIONS:
        result = candidate.operation("cleanup", "core")
    else:
        mtu = json.loads(state["before"]["links"]["stdout"])[0]["mtu"]
        commands = {
            "gateway-address-absent": ["ip", "address", "add", GATEWAY + "/16", "dev", "ogstun"],
            "reply-blackhole-route": ["ip", "route", "del", "blackhole", target + "/32"],
            "reply-policy-prohibit": ["ip", "rule", "del", "priority", "12001"],
            "inner-mtu-576": ["ip", "link", "set", "ogstun", "mtu", str(mtu)],
            "inner-mtu-576-boundary-control": ["ip", "link", "set", "ogstun", "mtu", str(mtu)],
        }
        result = checked(legacy.command(commands[condition]))
    STATE.unlink()
    return result


def operation(action, role, condition=None, target=None):
    if action == "boot":
        if role == "core" and GATEWAY != "10.45.0.1":
            for name in ["smf", "upf"]:
                path = legacy.INSTALL / "etc/open5gs" / (name + ".yaml")
                path.write_text(
                    path.read_text().replace("10.45.0.", GATEWAY.rsplit(".", 1)[0] + ".")
                )
        return legacy.boot(role)
    if action == "restart-ue":
        return {"pid": legacy.ue_start()}
    if action == "health":
        return {"small": probe(), "large": probe(1200)}
    if action == "inject":
        return inject(condition, target)
    if action == "cleanup":
        return cleanup()
    if action == "verify":
        return inventory()
    if action == "snapshot":
        result = candidate.operation("snapshot", role)
        if role == "core":
            result["routing_inventory"] = {
                "routes": legacy.command(["ip", "-json", "route", "show", "table", "all"]),
                "rules": legacy.command(["ip", "-json", "rule", "show"]),
            }
        return result
    return candidate.operation(action, role)


if __name__ == "__main__":
    if not Path("/.dockerenv").exists() or not Path("/control/expanded_control.py").exists():
        raise RuntimeError("explicitly owned mounted lab container required")
    parser = argparse.ArgumentParser()
    parser.add_argument("action")
    parser.add_argument("--role", choices=["core", "ue"], default="core")
    parser.add_argument("--condition")
    parser.add_argument("--target")
    args = parser.parse_args()
    print(json.dumps(operation(args.action, args.role, args.condition, args.target)))
