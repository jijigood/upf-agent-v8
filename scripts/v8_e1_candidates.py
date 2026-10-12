"""Collect three new calibration candidates without model answers or manufactured Gold."""

import argparse
import json
import re
import shutil
import time
from datetime import UTC, datetime
from pathlib import Path

from v8_e7_evidence_runner import assert_owned, command, visible_delta

from upf_agent.v8.e1_dataset import CaseManifest, DatasetIndex, load_dataset, read, sha, write
from upf_agent.v8.models import ObjectProfile, OrchestrationTask, PermissionScope

CONDITIONS = ("inner-request-filter", "inner-reply-filter", "ogstun-admin-down")
IMAGE = "sha256:0298b2faf2810793b7d21ee61fd9f0189c35e22e3e3565b8dcfd615f78c04a3d"


def control(container, action, role="core", condition=None):
    argv = [
        "docker",
        "exec",
        container,
        "python3",
        "/control/candidate_control.py",
        action,
        "--role",
        role,
    ]
    if condition:
        argv.extend(["--condition", condition])
    receipt = command(argv)
    if receipt["returncode"]:
        raise RuntimeError(json.dumps(receipt))
    return json.loads(receipt["stdout"])


def health(container):
    attempts = []
    for _ in range(30):
        receipt = control(container, "health", "ue")
        attempts.append(receipt)
        if receipt["returncode"] == 0 and "0% packet loss" in receipt["stdout"]:
            return {"pass": True, "attempts": attempts}
        time.sleep(1)
    return {"pass": False, "attempts": attempts}


def verified(condition, impaired, external):
    if impaired["returncode"] == 0:
        return False
    if condition == "ogstun-admin-down":
        body = json.loads(external["ogstun"]["stdout"])
        return len(body) == 1 and "UP" not in body[0]["flags"]
    chain = "input" if condition == "inner-request-filter" else "output"
    return bool(re.search(r"^\s*[1-9]\d*\s+\d+\s+DROP\s+icmp", external[chain]["stdout"], re.M))


def register(dataset_root, capture_root):
    index = DatasetIndex.model_validate(read(dataset_root / "dataset.json"))
    for row in read(capture_root / "summary.json")["rows"]:
        if not row["injection_verified"] or not row["recovered"]:
            continue
        case_id = f"E1-CAL-N{row['round']:03d}"
        folder = dataset_root / "validation" / case_id
        if folder.exists():
            raise ValueError("new candidate ID required")
        visible = folder / "visible"
        raw = visible / "data/raw/snapshot.json"
        raw.parent.mkdir(parents=True)
        source = capture_root / "rounds" / f"round-{row['round']:03d}" / "input/snapshot.json"
        shutil.copy2(source, raw)
        snapshot = read(raw)
        # No state/MTU/config value is inferred from injection truth. Projection is unapproved.
        observations = [
            {
                "object_id": obj,
                "category": "R",
                "fields": {"event_type": "captured_runtime_and_probe_inventory"},
                "product": product,
                "version": version,
                "observed": {
                    "start": snapshot["window_start"],
                    "end": snapshot["window_end"],
                    "timezone_source": "UTC controller capture interval",
                },
                "raw_source_sha256": sha(raw),
            }
            for obj, product, version in [("upf", "Open5GS", "2.7.6"), ("ran", "UERANSIM", "3.2.7")]
        ]
        relative = "data/normalized/observations.json"
        write(
            visible / relative,
            {
                "source_id": case_id + "-normal-capture",
                "synthetic": False,
                "corroborated": False,
                "observations": observations,
                "raw_sources": {"data/raw/snapshot.json": sha(raw)},
                "projection_status": "candidate; requires expert validation before formal freeze",
            },
        )
        task = OrchestrationTask(
            question=(
                "新采集的受控5GC中，UE会话建立后到核心侧的ICMP探针异常。"
                "根据提供的正常日志、接口和抓包资料给出UPF与RAN的只读调查方案；"
                "说明还需哪些资料，证据不足时停止，不推断已知根因或已执行修复。"
            ),
            template="log_observation",
            objects=["upf", "ran"],
            product="Open5GS",
            version="2.7.6",
            object_profiles={
                "upf": ObjectProfile(role="upf", product="Open5GS", version="2.7.6"),
                "ran": ObjectProfile(role="ran", product="UERANSIM", version="3.2.7"),
            },
            as_of=snapshot["window_end"],
            synthetic=False,
            observation_files=[relative],
            permission=PermissionScope(objects=["upf", "ran"], readable_fields=["event_type"]),
            retrieval_device="cpu",
            model_enabled=False,
        )
        write(visible / "case-task.json", task.model_dump(mode="json"))
        provenance = f"gold/provenance/{case_id}.json"
        truth = read(capture_root / "private" / f"round-{row['round']:03d}" / "truth.json")
        write(
            dataset_root / provenance,
            {
                "case_id": case_id,
                "actual_capture": str(capture_root),
                "normal_capture_sha256": sha(raw),
                "truth": truth,
                "independent_Gold_available": False,
                "expert_review_received": False,
            },
        )
        manifest = CaseManifest(
            case_id=case_id,
            split="validation",
            visible_root=str(visible.relative_to(dataset_root)),
            task_file=str((visible / "case-task.json").relative_to(dataset_root)),
            reference_file=None,
            source_group="new-e1-inner-dataplane-campaign-001",
            structure_family="ogstun-administrative-state"
            if row["condition"] == "ogstun-admin-down"
            else "inner-icmp-directional-filter",
            source_kind="experimental-injection",
            previously_evaluated=False,
            raw_source_hashes={"data/raw/snapshot.json": sha(raw)},
            provenance_file=provenance,
        )
        name = str((folder / "case.json").relative_to(dataset_root))
        write(dataset_root / name, manifest.model_dump(mode="json"))
        index.cases.append(name)
    write(dataset_root / "dataset.json", index.model_dump(mode="json"))
    return load_dataset(dataset_root)


def enrich_visible_candidates(dataset_root):
    """Keep revision 001; expose only measured normal capture facts in revision 002."""
    dataset = load_dataset(dataset_root)
    updated = []
    for item in dataset["cases"]:
        manifest = item["manifest"]
        if manifest.source_kind != "experimental-injection":
            continue
        if item["gold"] is not None or manifest.previously_evaluated:
            raise ValueError("only unreviewed, unevaluated candidate projections can be revised")
        visible = item["visible"]
        snapshot = read(visible / "data/raw/snapshot.json")
        original = read(visible / item["task"].observation_files[0])
        relative = "data/normalized/observations-002.json"
        if (visible / relative).exists():
            raise ValueError("candidate projection revision 002 already exists")
        for record in original["observations"]:
            name = "upf.log" if record["object_id"] == "upf" else "gnb.log"
            record["fields"].update(
                log_excerpt=snapshot["core"]["logs_and_config"].get(name, "")[-3000:],
                core_interface_inventory=snapshot["core"]["interfaces"]["stdout"],
                normal_probe_returncode=snapshot["normal_probe"]["returncode"],
                normal_probe_output=snapshot["normal_probe"]["stdout"],
            )
        original["projection_revision"] = "002; actual logs/probe/interfaces; no injector truth"
        write(visible / relative, original)
        task = item["task"].model_copy(deep=True)
        task.observation_files = [relative]
        task.permission.readable_fields = [
            "event_type",
            "log_excerpt",
            "core_interface_inventory",
            "normal_probe_returncode",
            "normal_probe_output",
        ]
        new_task = visible / "case-task-002.json"
        write(new_task, task.model_dump(mode="json"))
        manifest.task_file = str(new_task.relative_to(dataset_root))
        folder = dataset_root / "validation" / manifest.case_id
        shutil.copy2(folder / "case.json", folder / "case-manifest-revision-001.json")
        write(folder / "case.json", manifest.model_dump(mode="json"))
        updated.append(manifest.case_id)
    load_dataset(dataset_root)
    return {
        "updated_candidates": updated,
        "projection_revision": "002",
        "original_projection_preserved": True,
        "new_model_calls": 0,
        "Gold_created": False,
        "heldout_consumed": False,
    }


def collect(project, output):
    if output.exists():
        raise ValueError("new capture output required")
    output.mkdir(parents=True)
    owner = output.name
    suffix = sha(project / "lab/e1/candidate_control.py")[:7] + str(time.time_ns())[-5:]
    network, core, ue = ("upf-e1-" + suffix + ending for ending in ["-net", "-core", "-ue"])
    code = output / "code/lab"
    code.mkdir(parents=True)
    for name in ["control.py", "diagnostic_control.py"]:
        raw = (project / "lab/e7" / name).read_text()
        # This only changes bridge discovery addresses in this batch's copied controller.
        (code / name).write_text(raw.replace("10.208.7.2", "10.209.11.2"))
    shutil.copy2(project / "lab/e1/candidate_control.py", code / "candidate_control.py")
    write(
        output / "protocol.json",
        {
            "conditions": CONDITIONS,
            "planned_rounds": 3,
            "candidate_split": "validation",
            "image_id": IMAGE,
            "internal_subnet": "10.209.11.0/24",
            "agent_or_model_execution": False,
            "Gold_generation": False,
            "source_scope": (
                "new injection mechanisms; same upstream binaries and core loopback layout"
            ),
            "source_group": (
                "one collection campaign; three observations are not independent source groups"
            ),
            "known_E7_condition_reused": False,
            "heldout_consumed": False,
            "code_hashes": {p.name: sha(p) for p in code.iterdir()},
        },
    )
    created, rows, receipts = [], [], []
    try:
        result = command(
            [
                "docker",
                "network",
                "create",
                "--internal",
                "--subnet",
                "10.209.11.0/24",
                "--label",
                "upf.e7.owner=" + owner,
                network,
            ]
        )
        receipts.append(result)
        if result["returncode"]:
            raise RuntimeError("isolated E1 network failed")
        created.append(network)
        for container, ip in [(core, "10.209.11.2"), (ue, "10.209.11.3")]:
            result = command(
                [
                    "docker",
                    "run",
                    "-d",
                    "--runtime",
                    "runc",
                    "--name",
                    container,
                    "--label",
                    "upf.e7.owner=" + owner,
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
                    str(code.resolve()) + ":/control:ro",
                    IMAGE,
                ]
            )
            receipts.append(result)
            if result["returncode"]:
                raise RuntimeError("owned E1 container failed")
            created.append(container)
            inspection = assert_owned(container, owner)
            if inspection["HostConfig"]["Privileged"] or inspection["HostConfig"]["PortBindings"]:
                raise ValueError("lab isolation violated")
        write(output / "private/core-boot.json", control(core, "boot"))
        write(output / "private/ue-boot.json", control(ue, "boot", "ue"))
        baseline = health(ue)
        write(output / "baseline-health.json", baseline)
        if not baseline["pass"]:
            raise RuntimeError("healthy baseline failed before candidate injections")
        for number, condition in enumerate(CONDITIONS, 1):
            private = output / "private" / f"round-{number:03d}"
            row = {
                "round": number,
                "condition": condition,
                "injection_verified": False,
                "recovered": False,
            }
            rows.append(row)
            before_health = health(ue)
            write(private / "health-before.json", before_health)
            if not before_health["pass"]:
                raise RuntimeError("baseline failed between candidate conditions")
            before = {"core": control(core, "snapshot"), "ue": control(ue, "snapshot", "ue")}
            started = datetime.now(UTC).isoformat()
            try:
                write(private / "inject.json", control(core, "inject", condition=condition))
                control(core, "capture-start")
                impaired = control(ue, "health", "ue")
                capture = control(core, "capture-end")
                external = control(core, "verify")
                write(private / "external-verification.json", external)
                row["injection_verified"] = verified(condition, impaired, external)
                snapshot = {
                    "core": control(core, "snapshot"),
                    "ue": control(ue, "snapshot", "ue"),
                    "packet_capture": capture,
                    "normal_probe": impaired,
                    "window_start": started,
                    "window_end": datetime.now(UTC).isoformat(),
                }
                snapshot = visible_delta(before, snapshot)
                write(output / "rounds" / f"round-{number:03d}" / "input/snapshot.json", snapshot)
                write(
                    private / "truth.json",
                    {
                        "condition": condition,
                        "verified": row["injection_verified"],
                        "basis": (
                            "owned injection receipt plus independent counter/interface read "
                            "and impaired UE probe"
                        ),
                        "expert_Gold": False,
                    },
                )
            finally:
                write(private / "cleanup.json", control(core, "cleanup"))
                recovered = health(ue)
                write(private / "health-after.json", recovered)
                row["recovered"] = recovered["pass"]
            if not row["injection_verified"] or not row["recovered"]:
                raise RuntimeError(
                    "candidate injection/recovery gate failed; remaining conditions not run"
                )
    finally:
        teardown = []
        for resource in reversed(created):
            is_network = resource == network
            assert_owned(resource, owner, is_network)
            result = command(
                ["docker", "network", "rm", resource]
                if is_network
                else ["docker", "rm", "-f", resource]
            )
            teardown.append(result)
        write(output / "startup.json", receipts)
        write(output / "teardown.json", teardown)
        write(
            output / "summary.json",
            {
                "planned_rounds": 3,
                "completed_rounds": len(rows),
                "rows": rows,
                "injections_verified": sum(r["injection_verified"] for r in rows),
                "recoveries_verified": sum(r["recovered"] for r in rows),
                "teardown_pass": all(r["returncode"] == 0 for r in teardown),
                "new_model_calls": 0,
                "expert_Gold_created": False,
                "heldout_consumed": False,
            },
        )
    return read(output / "summary.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dataset", type=Path)
    parser.add_argument("--enrich-only", action="store_true")
    args = parser.parse_args()
    if args.enrich_only:
        if args.dataset is None:
            parser.error("--enrich-only requires --dataset")
        result = enrich_visible_candidates(args.dataset.resolve())
    else:
        if args.output is None:
            parser.error("capture requires --output")
        result = collect(args.project.resolve(), args.output.resolve())
        if args.dataset:
            register(args.dataset.resolve(), args.output.resolve())
            enrich_visible_candidates(args.dataset.resolve())
    print(json.dumps(result, ensure_ascii=False))
