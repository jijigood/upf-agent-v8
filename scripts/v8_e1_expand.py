"""Preregister and acquire 9 calibration plus 24 withheld inputs without model answers."""

import argparse
import ipaddress
import json
import re
import shutil
import time
from datetime import UTC, datetime
from pathlib import Path

from v8_e1_candidates import CONDITIONS, IMAGE
from v8_e7_evidence_runner import assert_owned, command, visible_delta

from upf_agent.v8.e1_dataset import CaseManifest, DatasetIndex, load_dataset, read, sha, write
from upf_agent.v8.experiment_manifest import source_manifest
from upf_agent.v8.models import ObjectProfile, OrchestrationTask, PermissionScope, digest

HELDOUT = (
    "gateway-address-absent",
    "reply-blackhole-route",
    "reply-policy-prohibit",
    "inner-mtu-576-boundary-control",
)
CAMPAIGNS = [
    {
        "id": f"validation-{i + 1}",
        "split": "validation",
        "condition": c,
        "repetitions": 3,
        "bridge": 31 + i,
        "plane": 45,
    }
    for i, c in enumerate(CONDITIONS)
] + [
    {
        "id": f"withheld-{i + 1}",
        "split": "heldout",
        "condition": c,
        "repetitions": 6,
        "bridge": 41 + i,
        "plane": 46 + i,
    }
    for i, c in enumerate(HELDOUT)
]


def control(container, action, role="core", condition=None, target=None):
    argv = [
        "docker",
        "exec",
        container,
        "python3",
        "/control/expanded_control.py",
        action,
        "--role",
        role,
    ]
    if condition:
        argv += ["--condition", condition]
    if target:
        argv += ["--target", target]
    receipt = command(argv)
    if receipt["returncode"]:
        raise RuntimeError(json.dumps(receipt))
    return json.loads(receipt["stdout"])


def healthy(ue):
    attempts = []
    for _ in range(20):
        body = control(ue, "health", "ue")
        attempts.append(body)
        if all(v["returncode"] == 0 and "0% packet loss" in v["stdout"] for v in body.values()):
            return {"pass": True, "attempts": attempts}
        time.sleep(1)
    return {"pass": False, "attempts": attempts}


def ue_address(snapshot, plane):
    rows = json.loads(snapshot["interfaces"]["stdout"])
    addresses = [
        a["local"]
        for r in rows
        if r["ifname"] == "uesimtun0"
        for a in r.get("addr_info", [])
        if a["family"] == "inet"
    ]
    if len(addresses) != 1 or ipaddress.IPv4Address(addresses[0]) not in ipaddress.IPv4Network(
        f"10.{plane}.0.0/16"
    ):
        raise ValueError("fresh UE address unavailable or outside campaign scope")
    return addresses[0]


def verify_injection(condition, probes, external, target, plane):
    small_failed = probes["small"]["returncode"] != 0
    large_failed = probes["large"]["returncode"] != 0
    if condition == "inner-mtu-576-boundary-control":
        return (
            not small_failed
            and not large_failed
            and json.loads(external["links"]["stdout"])[0]["mtu"] == 576
        )
    if not large_failed:
        return False
    if condition == "inner-mtu-576":
        return not small_failed and json.loads(external["links"]["stdout"])[0]["mtu"] == 576
    if not small_failed:
        return False
    if condition == "ogstun-admin-down":
        return "UP" not in json.loads(external["links"]["stdout"])[0]["flags"]
    if condition == "gateway-address-absent":
        return all(
            a.get("local") != f"10.{plane}.0.1"
            for r in json.loads(external["addresses"]["stdout"])
            for a in r.get("addr_info", [])
        )
    if condition == "reply-blackhole-route":
        return any(
            r.get("type") == "blackhole" and r.get("dst") in {target, target + "/32"}
            for r in json.loads(external["routes"]["stdout"])
        )
    if condition == "reply-policy-prohibit":
        return any(
            r.get("priority") == 12001 and r.get("action") == "prohibit"
            for r in json.loads(external["rules"]["stdout"])
        )
    chain = "input" if condition == "inner-request-filter" else "output"
    direction = "8" if chain == "input" else "0"
    return bool(
        re.search(
            r"^\s*[1-9]\d*\s+\d+\s+DROP\s+icmp.*ogstun.*icmptype " + direction,
            external[chain]["stdout"],
            re.M,
        )
    )


def collect(project, output, spec):
    if output.exists():
        raise ValueError("fresh campaign output required")
    output.mkdir(parents=True)
    code = output / "code/lab"
    code.mkdir(parents=True)
    bridge, plane = spec["bridge"], spec["plane"]
    for folder, name in [
        ("e7", "control.py"),
        ("e7", "diagnostic_control.py"),
        ("e1", "candidate_control.py"),
        ("e1", "expanded_control.py"),
    ]:
        raw = (project / "lab" / folder / name).read_text()
        if name == "expanded_control.py":
            # Preserve the original installed-YAML search string and branch comparison.
            raw = raw.replace('GATEWAY = "10.45.0.1"', f'GATEWAY = "10.{plane}.0.1"').replace(
                'CIDR = "10.45.0.0/16"', f'CIDR = "10.{plane}.0.0/16"'
            )
        else:
            raw = raw.replace("10.208.7.2", f"10.210.{bridge}.2").replace(
                "10.45.0.", f"10.{plane}.0."
            )
        (code / name).write_text(raw)
    write(
        output / "protocol.json",
        {
            **spec,
            "image": IMAGE,
            "code_hashes": {p.name: sha(p) for p in code.iterdir()},
            "new_model_calls": 0,
            "heldout_model_consumed": False,
            "replicates_are_correlated": True,
        },
    )
    owner = "e1-expand-" + output.name
    suffix = digest([str(output), time.time_ns()])[:10]
    network, core, ue = ["upf-e1x-" + suffix + tail for tail in ["-net", "-core", "-ue"]]
    created, rows, startup = [], [], []
    try:
        receipt = command(
            [
                "docker",
                "network",
                "create",
                "--internal",
                "--subnet",
                f"10.210.{bridge}.0/24",
                "--label",
                "upf.e7.owner=" + owner,
                network,
            ]
        )
        startup.append(receipt)
        if receipt["returncode"]:
            raise RuntimeError("campaign network creation failed")
        created.append(network)
        for name, last in [(core, 2), (ue, 3)]:
            receipt = command(
                [
                    "docker",
                    "run",
                    "-d",
                    "--runtime",
                    "runc",
                    "--name",
                    name,
                    "--label",
                    "upf.e7.owner=" + owner,
                    "--network",
                    network,
                    "--ip",
                    f"10.210.{bridge}.{last}",
                    "--cap-add",
                    "NET_ADMIN",
                    "--device",
                    "/dev/net/tun",
                    "--memory",
                    "2g",
                    "--cpus",
                    "2",
                    "-v",
                    str(code.resolve()) + ":/control:ro",
                    IMAGE,
                ]
            )
            startup.append(receipt)
            if receipt["returncode"]:
                raise RuntimeError("campaign container creation failed")
            created.append(name)
            inspected = assert_owned(name, owner)
            if inspected["HostConfig"]["Privileged"] or inspected["HostConfig"]["PortBindings"]:
                raise ValueError("campaign isolation violated")
            write(output / "private" / (name.rsplit("-", 1)[1] + "-inspection.json"), inspected)
        write(output / "private/core-boot.json", control(core, "boot"))
        write(output / "private/ue-boot.json", control(ue, "boot", "ue"))
        for number in range(1, spec["repetitions"] + 1):
            private = output / "private" / f"round-{number:03d}"
            row = {"round": number, "injection_verified": False, "recovered": False}
            rows.append(row)
            if number > 1:
                write(private / "fresh-ue-process.json", control(ue, "restart-ue", "ue"))
            before_health = healthy(ue)
            write(private / "health-before.json", before_health)
            if not before_health["pass"]:
                raise RuntimeError("baseline probes failed before injection")
            before = {"core": control(core, "snapshot"), "ue": control(ue, "snapshot", "ue")}
            target = ue_address(before["ue"], plane)
            started = datetime.now(UTC).isoformat()
            try:
                write(
                    private / "inject.json",
                    control(core, "inject", condition=spec["condition"], target=target),
                )
                control(core, "capture-start")
                probes = control(ue, "health", "ue")
                capture = control(core, "capture-end")
                external = control(core, "verify")
                write(private / "external-verification.json", external)
                row["injection_verified"] = verify_injection(
                    spec["condition"], probes, external, target, plane
                )
                snapshot = {
                    "core": control(core, "snapshot"),
                    "ue": control(ue, "snapshot", "ue"),
                    "packet_capture": capture,
                    "normal_probes": probes,
                    "window_start": started,
                    "window_end": datetime.now(UTC).isoformat(),
                }
                write(
                    output / "rounds" / f"round-{number:03d}" / "input/snapshot.json",
                    visible_delta(before, snapshot),
                )
                write(
                    private / "truth.json",
                    {
                        "condition": spec["condition"],
                        "target": target,
                        "verified": row["injection_verified"],
                        "basis": (
                            "actual controller receipt, separate kernel-state read "
                            "and small/large probe results"
                        ),
                        "expert_Gold": False,
                    },
                )
            finally:
                write(private / "cleanup.json", control(core, "cleanup"))
                write(private / "recovery-ue-harness-reset.json", control(ue, "restart-ue", "ue"))
                after_health = healthy(ue)
                write(private / "health-after.json", after_health)
                row["recovered"] = after_health["pass"]
            print(json.dumps({"campaign": spec["id"], **row}), flush=True)
            if not row["injection_verified"] or not row["recovered"]:
                raise RuntimeError("injection/recovery gate failed; retain failure and stop")
    finally:
        teardown = []
        for resource in reversed(created):
            assert_owned(resource, owner, resource == network)
            teardown.append(
                command(
                    ["docker", "network", "rm", resource]
                    if resource == network
                    else ["docker", "rm", "-f", resource]
                )
            )
        write(output / "startup.json", startup)
        write(output / "teardown.json", teardown)
        write(
            output / "summary.json",
            {
                "spec": spec,
                "planned_rounds": spec["repetitions"],
                "rows": rows,
                "injections_verified": sum(r["injection_verified"] for r in rows),
                "recoveries_verified": sum(r["recovered"] for r in rows),
                "teardown_pass": all(r["returncode"] == 0 for r in teardown),
                "new_model_calls": 0,
                "heldout_consumed": False,
            },
        )
    return read(output / "summary.json")


def register(dataset_root, root):
    index = DatasetIndex.model_validate(read(dataset_root / "dataset.json"))
    registered = []
    for spec in CAMPAIGNS:
        capture = root / "captures" / spec["id"]
        summary = read(capture / "summary.json")
        if len(summary["rows"]) != spec["repetitions"] or not all(
            r["injection_verified"] and r["recovered"] for r in summary["rows"]
        ):
            raise ValueError("incomplete campaign cannot enter dataset")
        for row in summary["rows"]:
            ordinal = (
                (spec["bridge"] - 31) * 3 + row["round"] + 3
                if spec["split"] == "validation"
                else (spec["bridge"] - 41) * 6 + row["round"]
            )
            case_id = (
                f"E1-CAL-N{ordinal:03d}"
                if spec["split"] == "validation"
                else f"E1-HO-N{ordinal:03d}"
            )
            folder = dataset_root / spec["split"] / case_id
            if folder.exists():
                raise ValueError("new file case ID required")
            visible = folder / "visible"
            raw = visible / "data/raw/snapshot.json"
            raw.parent.mkdir(parents=True)
            shutil.copy2(
                capture / "rounds" / f"round-{row['round']:03d}" / "input/snapshot.json", raw
            )
            snap = read(raw)
            observations = []
            for obj, product, version in [
                ("upf", "Open5GS", "2.7.6"),
                ("ran", "UERANSIM", "3.2.7"),
            ]:
                log = "upf.log" if obj == "upf" else "gnb.log"
                fields = {
                    "event_type": "captured_runtime_and_probe_inventory",
                    "log_excerpt": snap["core"]["logs_and_config"].get(log, "")[-3000:],
                    "core_interface_inventory": snap["core"]["interfaces"]["stdout"],
                    "routing_inventory": snap["core"]["routing_inventory"],
                    "small_probe": snap["normal_probes"]["small"],
                    "large_probe": snap["normal_probes"]["large"],
                }
                observations.append(
                    {
                        "object_id": obj,
                        "category": "R",
                        "product": product,
                        "version": version,
                        "fields": fields,
                        "observed": {
                            "start": snap["window_start"],
                            "end": snap["window_end"],
                            "timezone_source": "UTC controller capture interval",
                        },
                        "raw_source_sha256": sha(raw),
                    }
                )
            normal = "data/normalized/observations.json"
            write(
                visible / normal,
                {
                    "source_id": case_id + "-normal-capture",
                    "synthetic": False,
                    "corroborated": False,
                    "observations": observations,
                    "raw_sources": {"data/raw/snapshot.json": sha(raw)},
                    "projection_status": "unreviewed actual runtime projection",
                },
            )
            task = OrchestrationTask(
                question=(
                    "受控5GC的UE会话建立后收到核心侧ICMP连通性调查请求。"
                    "根据正常日志、接口、路由和探针资料提出UPF与RAN的只读调查方案；"
                    "先核验资料是否支持异常，核对适用范围，资料不足或超出能力时请求资料／转人工，"
                    "不宣称已执行修复。"
                ),
                template="log_observation",
                objects=["upf", "ran"],
                product="Open5GS",
                version="2.7.6",
                as_of=snap["window_end"],
                synthetic=False,
                object_profiles={
                    "upf": ObjectProfile(role="upf", product="Open5GS", version="2.7.6"),
                    "ran": ObjectProfile(role="ran", product="UERANSIM", version="3.2.7"),
                },
                observation_files=[normal],
                permission=PermissionScope(
                    objects=["upf", "ran"], readable_fields=list(observations[0]["fields"])
                ),
                retrieval_device="cpu",
                model_enabled=False,
            )
            write(visible / "case-task.json", task.model_dump(mode="json"))
            provenance = f"gold/provenance/{case_id}.json"
            write(
                dataset_root / provenance,
                {
                    "case_id": case_id,
                    "capture_root": str(capture),
                    "capture_round": row["round"],
                    "source_sha256": sha(raw),
                    "truth": read(capture / "private" / f"round-{row['round']:03d}" / "truth.json"),
                    "independent_Gold_available": False,
                    "expert_review_received": False,
                    "correlation": (
                        "fresh UE process after first round; "
                        "same campaign binaries and failure mechanism"
                    ),
                },
            )
            family = {
                "inner-request-filter": "inner-icmp-directional-filter",
                "inner-reply-filter": "inner-icmp-directional-filter",
                "ogstun-admin-down": "ogstun-administrative-state",
            }.get(spec["condition"], spec["condition"])
            manifest = CaseManifest(
                case_id=case_id,
                split=spec["split"],
                visible_root=str(visible.relative_to(dataset_root)),
                task_file=str((visible / "case-task.json").relative_to(dataset_root)),
                reference_file=None,
                source_group="e1-expanded-" + spec["id"],
                structure_family=family,
                source_kind="experimental-injection",
                previously_evaluated=False,
                raw_source_hashes={"data/raw/snapshot.json": sha(raw)},
                provenance_file=provenance,
            )
            name = str((folder / "case.json").relative_to(dataset_root))
            write(dataset_root / name, manifest.model_dump(mode="json"))
            index.cases.append(name)
            registered.append(case_id)
    write(dataset_root / "dataset.json", index.model_dump(mode="json"))
    load_dataset(dataset_root)
    return registered


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dataset", type=Path, default=Path("eval/v8/e1"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--register-only", action="store_true")
    parser.add_argument("--resume-from", type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    root = args.output.resolve()
    if args.register_only:
        print(
            json.dumps({"registered": register(args.dataset.resolve(), root)}, ensure_ascii=False)
        )
        return
    if root.exists():
        raise ValueError("fresh expansion directory required")
    root.mkdir(parents=True)
    write(
        root / "preregistration.json",
        {
            "campaigns": CAMPAIGNS,
            "additional_validation": 9,
            "withheld_candidates": 24,
            "before_any_model_answer": True,
            "core": source_manifest(project),
            "collector_sha256": sha(Path(__file__)),
            "controller_sha256": sha(project / "lab/e1/expanded_control.py"),
            "shared_platform_and_replicates_are_correlated": True,
            "expert_Gold_created": False,
            "heldout_model_consumed": False,
        },
    )
    shutil.copytree(args.dataset, root / "before-dataset")
    reused = {}
    for spec in CAMPAIGNS:
        if args.resume_from:
            previous = args.resume_from / "captures" / spec["id"]
            if (previous / "summary.json").exists():
                summary = read(previous / "summary.json")
                if (
                    summary["spec"] == spec
                    and len(summary["rows"]) == spec["repetitions"]
                    and all(r["injection_verified"] and r["recovered"] for r in summary["rows"])
                    and summary["teardown_pass"]
                ):
                    shutil.copytree(previous, root / "captures" / spec["id"])
                    reused[spec["id"]] = {
                        "source": str(previous.resolve()),
                        "sha256": {
                            str(p.relative_to(previous)): sha(p)
                            for p in previous.rglob("*")
                            if p.is_file()
                        },
                    }
                    print("verified existing completed campaign " + spec["id"], flush=True)
                    continue
        collect(project, root / "captures" / spec["id"], spec)
    write(root / "carried-forward-campaigns.json", reused)
    print(json.dumps({"registered": register(args.dataset.resolve(), root)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
