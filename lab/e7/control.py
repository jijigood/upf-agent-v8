"""Independent E7 controller. Run ONLY inside the dedicated lab containers."""

import argparse
import json
import os
import signal
import subprocess
import time
from pathlib import Path

import yaml
from pymongo import MongoClient

ROOT = Path("/work")
INSTALL = Path("/opt/open5gs")
UERAN = Path("/opt/src/UERANSIM")
NF = ("nrf", "scp", "amf", "smf", "upf", "ausf", "udm", "udr", "pcf", "nssf", "bsf")


def command(args, timeout=30):
    p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    return {"argv": args, "returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def start(name, argv):
    logs = ROOT / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    with (logs / (name + ".log")).open("ab") as stream:
        p = subprocess.Popen(argv, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
    (ROOT / (name + ".pid")).write_text(str(p.pid))
    return p.pid


def stop(name):
    p = ROOT / (name + ".pid")
    if not p.exists():
        return
    pid = int(p.read_text())
    try:
        os.kill(pid, signal.SIGCONT)
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    for _ in range(20):
        status = Path(f"/proc/{pid}/status")
        if not status.exists():
            break
        try:
            state = next(
                line.split()[1]
                for line in status.read_text().splitlines()
                if line.startswith("State:")
            )
        except (FileNotFoundError, StopIteration):
            break
        # A zombie has finished execution and cannot write a capture or serve a
        # socket. PID 1 in this isolated lab may leave it unreaped; waiting for
        # /proc disappearance adds no teardown assurance for these NF binaries.
        if state in {"Z", "X"}:
            break
        time.sleep(0.1)
    p.unlink(missing_ok=True)


def nf_start(name):
    return start(
        name,
        [
            str(INSTALL / "bin" / ("open5gs-" + name + "d")),
            "-c",
            str(INSTALL / "etc/open5gs" / (name + ".yaml")),
        ],
    )


def ue_start(apn="internet"):
    stop("ue")
    p = UERAN / "config/open5gs-ue.yaml"
    cfg = yaml.safe_load(p.read_text())
    cfg["gnbSearchList"] = ["10.208.7.2"]
    cfg["sessions"][0]["apn"] = apn
    (ROOT / "ue.yaml").write_text(yaml.safe_dump(cfg))
    return start("ue", [str(UERAN / "cmake-build-release/nr-ue"), "-c", str(ROOT / "ue.yaml")])


def gnb_start(advertise=None):
    stop("gnb")
    cfg = yaml.safe_load((UERAN / "config/open5gs-gnb.yaml").read_text())
    cfg["linkIp"] = "10.208.7.2"
    if advertise:
        cfg["gtpAdvertiseIp"] = advertise
    (ROOT / "gnb.yaml").write_text(yaml.safe_dump(cfg))
    return start("gnb", [str(UERAN / "cmake-build-release/nr-gnb"), "-c", str(ROOT / "gnb.yaml")])


def boot(role):
    ROOT.mkdir(exist_ok=True)
    if role == "ue":
        return {"ue_pid": ue_start()}
    (ROOT / "mongo").mkdir(exist_ok=True)
    start(
        "mongo",
        ["/opt/mongodb/bin/mongod", "--bind_ip", "127.0.0.1", "--dbpath", str(ROOT / "mongo")],
    )
    client = MongoClient("mongodb://127.0.0.1", serverSelectionTimeoutMS=1000)
    for _ in range(30):
        try:
            client.admin.command("ping")
            break
        except Exception:
            time.sleep(1)
    # Published UERANSIM example subscription, strictly local test credentials.
    rate = {"downlink": {"value": 1, "unit": 3}, "uplink": {"value": 1, "unit": 3}}
    client.open5gs.subscribers.replace_one(
        {"imsi": "999700000000001"},
        {
            "schema_version": 1,
            "imsi": "999700000000001",
            "msisdn": [],
            "security": {
                "k": "465B5CE8B199B49FAA5F0A2EE238A6BC",
                "opc": "E8ED289DEBA952E4283B54E88E6183CA",
                "op": None,
                "amf": "8000",
            },
            "ambr": rate,
            "slice": [
                {
                    "sst": 1,
                    "default_indicator": True,
                    "session": [
                        {
                            "name": "internet",
                            "type": 3,
                            "ambr": rate,
                            "pcc_rule": [],
                            "qos": {
                                "index": 9,
                                "arp": {
                                    "priority_level": 8,
                                    "pre_emption_capability": 1,
                                    "pre_emption_vulnerability": 2,
                                },
                            },
                        }
                    ],
                }
            ],
            "access_restriction_data": 32,
            "network_access_mode": 0,
            "subscriber_status": 0,
            "operator_determined_barring": 0,
            "subscribed_rau_tau_timer": 12,
        },
        upsert=True,
    )
    receipts = [
        command(["ip", "tuntap", "add", "name", "ogstun", "mode", "tun"]),
        command(["ip", "addr", "add", "10.45.0.1/16", "dev", "ogstun"]),
        command(["ip", "link", "set", "ogstun", "up"]),
    ]
    for n in NF:
        nf_start(n)
        time.sleep(0.2)
    time.sleep(4)
    return {"setup": receipts, "gnb_pid": gnb_start()}


def inject(condition):
    if condition in ("n3-ul-loss", "n3-dl-loss", "upf-n3-block"):
        args = ["iptables", "-I", "INPUT", "1", "-p", "udp", "--dport", "2152"]
        if condition != "upf-n3-block":
            args += ["-s", "127.0.0.1" if condition == "n3-ul-loss" else "127.0.0.7"]
        args += ["-j", "DROP"]
        return command(args)
    if condition == "upf-paused":
        pid = int((ROOT / "upf.pid").read_text())
        os.kill(pid, signal.SIGSTOP)
        return {"pid": pid, "signal": "SIGSTOP"}
    if condition == "gnb-gtp-mismatch":
        return {"gnb_pid": gnb_start("127.0.0.8")}
    if condition == "ue-dnn-mismatch":
        return {"ue_pid": ue_start("unsubscribed")}
    raise ValueError("unknown condition")


def cleanup(role):
    if role == "ue":
        return {"ue_pid": ue_start()}
    receipt = command(["iptables", "-F", "INPUT"])
    os.kill(int((ROOT / "upf.pid").read_text()), signal.SIGCONT)
    return {"firewall": receipt, "gnb_pid": gnb_start()}


def snapshot(role):
    # Normal investigation evidence only: no injector command, ID, Gold or firewall rules.
    files = {}
    for p in sorted((ROOT / "logs").glob("*.log")):
        if p.name != "mongo.log":
            files[p.name] = p.read_text(errors="replace")
    for name in ("gnb.yaml", "ue.yaml"):
        p = ROOT / name
        if p.exists():
            cfg = yaml.safe_load(p.read_text())
            for key in ("key", "op", "homeNetworkPublicKey"):
                cfg.pop(key, None)
            files[name] = yaml.safe_dump(cfg)
    for name in ("upf", "smf") if role == "core" else ():
        files[name + ".yaml"] = (INSTALL / "etc/open5gs" / (name + ".yaml")).read_text()
    return {
        "role": role,
        "logs_and_config": files,
        "interfaces": command(["ip", "-json", "address"]),
        "sockets": command(["ss", "-lnup"]),
        "synthetic": False,
    }


if __name__ == "__main__":
    if not Path("/.dockerenv").exists() or not Path("/control/control.py").exists():
        raise RuntimeError("controller must run in the dedicated mounted lab container")
    p = argparse.ArgumentParser()
    p.add_argument(
        "operation", choices=["boot", "inject", "cleanup", "snapshot", "health", "verify"]
    )
    p.add_argument("--role", choices=["core", "ue"], default="core")
    p.add_argument("--condition")
    a = p.parse_args()
    if a.operation == "boot":
        result = boot(a.role)
    elif a.operation == "inject":
        result = inject(a.condition)
    elif a.operation == "cleanup":
        result = cleanup(a.role)
    elif a.operation == "snapshot":
        result = snapshot(a.role)
    elif a.operation == "health":
        result = command(
            ["ping", "-n", "-I", "uesimtun0", "-c", "5", "-i", ".2", "-W", "1", "10.45.0.1"]
        )
    else:
        result = {
            "firewall": command(["iptables", "-nvxL", "INPUT"]),
            "upf_process": Path(
                "/proc/" + (ROOT / "upf.pid").read_text().strip() + "/status"
            ).read_text(),
            "gnb_process": Path(
                "/proc/" + (ROOT / "gnb.pid").read_text().strip() + "/status"
            ).read_text(),
        }
    print(json.dumps(result))
