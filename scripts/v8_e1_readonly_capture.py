"""One healthy, normal-read collector smoke test; not a new E1/Gold/model trial."""

import argparse
import json
import shutil
import time
from datetime import UTC, datetime
from pathlib import Path

from v8_e7_evidence_runner import assert_owned, command, visible_delta

from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.e1_dataset import read, sha, write
from upf_agent.v8.e1_domain_readonly import (
    SCOPE_VERSION,
    DomainEvidenceTools,
    DomainScope,
    NamespaceScope,
    capture_inventory,
    extract_normal_fields,
)
from upf_agent.v8.experiment_metrics import MetricCollector
from upf_agent.v8.models import OrchestrationTask, digest
from upf_agent.v8.plan_generator import PlanBudget

IMAGE = "sha256:0298b2faf2810793b7d21ee61fd9f0189c35e22e3e3565b8dcfd615f78c04a3d"
SUBNET = "10.209.14.0/24"


def collect(project, output, template):
    if output.exists():
        raise ValueError("fresh collection output required")
    output.mkdir(parents=True)
    owner = output.name
    suffix = str(time.time_ns())[-9:]
    network, core, ue = ["upf-e1-normal-" + suffix + tail for tail in ("-net", "-core", "-ue")]
    code = output / "code/lab"
    code.mkdir(parents=True)
    for name in ("control.py", "diagnostic_control.py"):
        (code / name).write_text(
            (project / "lab/e7" / name).read_text().replace("10.208.7.2", "10.209.14.2")
        )
    shutil.copy2(project / "lab/e1/readonly_control.py", code / "readonly_control.py")
    shutil.copy2(Path(__file__), output / "code/runner.py")
    write(
        output / "protocol.json",
        {
            "purpose": "healthy normal filter/independent-namespace PCAP collector integration",
            "image_id": IMAGE,
            "internal_subnet": SUBNET,
            "planned_captures": 1,
            "fault_injections": 0,
            "models": 0,
            "formal_cases_added": 0,
            "heldout_consumed": False,
            "Gold_created": False,
            "capture_controller_is_harness_not_agent": True,
            "source_admission_approval": False,
            "code_hashes": {
                str(p.relative_to(output / "code")): sha(p)
                for p in (output / "code").rglob("*")
                if p.is_file()
            },
        },
    )
    receipts, created, teardown = [], [], []

    def controlled(container, operation, role, *, setup=False):
        assert_owned(container, owner)
        script = "control.py" if setup else "readonly_control.py"
        receipt = command(
            [
                "docker",
                "exec",
                container,
                "python3",
                f"/control/{script}",
                operation,
                "--role",
                role,
            ]
        )
        receipts.append(receipt)
        if receipt["returncode"]:
            raise RuntimeError(f"normal collector {operation} failed")
        return json.loads(receipt["stdout"])

    def health():
        attempts = []
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            probe = controlled(ue, "health", "ue", setup=True)
            attempts.append(probe)
            if probe["returncode"] == 0 and " 0% packet loss" in probe["stdout"]:
                return {"pass": True, "attempts": attempts}
            time.sleep(1)
        return {"pass": False, "attempts": attempts}

    result = {
        "engineering_pass": False,
        "model_calls": 0,
        "fault_injections": 0,
        "formal_cases_added": 0,
        "Gold_created": False,
        "actual_human_reviews": 0,
        "heldout_inputs_read": 0,
    }
    try:
        receipt = command(
            [
                "docker",
                "network",
                "create",
                "--internal",
                "--subnet",
                SUBNET,
                "--label",
                "upf.e7.owner=" + owner,
                network,
            ]
        )
        receipts.append(receipt)
        if receipt["returncode"]:
            raise RuntimeError("normal collector internal network creation failed")
        created.append((network, True))
        for container, ip in ((core, "10.209.14.2"), (ue, "10.209.14.3")):
            receipt = command(
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
            receipts.append(receipt)
            if receipt["returncode"]:
                raise RuntimeError("owned normal collector container failed")
            created.append((container, False))
            inspection = assert_owned(container, owner)
            if (
                inspection["Image"] != IMAGE
                or inspection["HostConfig"]["Privileged"]
                or inspection["HostConfig"]["PortBindings"]
            ):
                raise ValueError("normal collector isolation/image mismatch")
        write(output / "harness-only/core-boot.json", controlled(core, "boot", "core", setup=True))
        write(output / "harness-only/ue-boot.json", controlled(ue, "boot", "ue", setup=True))
        before_health = health()
        write(output / "health-before.json", before_health)
        if not before_health["pass"]:
            raise RuntimeError("normal collector healthy baseline failed")
        before = {
            "core": controlled(core, "snapshot", "core"),
            "ue": controlled(ue, "snapshot", "ue"),
        }
        started = datetime.now(UTC).isoformat()
        for container, role in ((core, "core"), (ue, "ue")):
            controlled(container, "capture-start", role)
        probe = controlled(ue, "health", "ue", setup=True)
        core_capture = controlled(core, "capture-end", "core")
        ue_capture = controlled(ue, "capture-end", "ue")
        snapshot = visible_delta(
            before,
            {
                "core": controlled(core, "snapshot", "core"),
                "ue": controlled(ue, "snapshot", "ue"),
                "normal_probe": probe,
                "packet_capture": core_capture,
                "ue_packet_capture": ue_capture,
                "window_start": started,
                "window_end": datetime.now(UTC).isoformat(),
            },
        )
        root = output / "normal-input"
        write(root / "data/raw/snapshot.json", snapshot)
        common = ["event_type", "log_excerpt", "domain_namespace"]
        scope = DomainScope(
            raw_sha256=sha(root / "data/raw/snapshot.json"),
            objects={
                "upf": NamespaceScope(
                    namespace="core",
                    devices=["ogstun"],
                    captures=["core-any"],
                    readable_fields=common
                    + ["tun_inventory", "filter_inventory", "packet_inventory"],
                ),
                "ran": NamespaceScope(namespace="core", readable_fields=common),
                "ue": NamespaceScope(
                    namespace="ue",
                    devices=["uesimtun0"],
                    captures=["ue-any"],
                    probe_ids=["normal"],
                    readable_fields=common
                    + ["tun_inventory", "session_probe_inventory", "packet_inventory"],
                ),
            },
        )
        write(root / "data/domain-scope.json", scope.model_dump(mode="json"))
        task = OrchestrationTask.model_validate(read(template)).model_copy(deep=True)
        task.question = (
            "健康控制采集器联调：核对授权命名空间的正常只读资料完整性；"
            "未获领域准入和Gold审核，不判断根因或修复。"
        )
        task.as_of = datetime.fromisoformat(snapshot["window_end"])
        task.permission.revision = f"{SCOPE_VERSION}:{digest(scope)}"
        fields = extract_normal_fields(root, scope)
        write(root / "task.json", task.model_dump(mode="json"))
        write(
            root / "data/domain-observations.json",
            {
                "source_id": owner + "-healthy-normal-integration",
                "synthetic": False,
                "corroborated": False,
                "raw_sources": {scope.raw_path: scope.raw_sha256},
                "observations": [
                    {
                        "object_id": obj,
                        "category": "R",
                        "fields": fields[obj],
                        "product": task.object_profiles[obj].product,
                        "version": task.object_profiles[obj].version,
                        "observed": {
                            "start": snapshot["window_start"],
                            "end": snapshot["window_end"],
                            "timezone_source": "same-host UTC controller interval",
                        },
                    }
                    for obj in task.objects
                ],
            },
        )
        collector = MetricCollector(owner)
        tools = DomainEvidenceTools(root, task, compile_contract(task), PlanBudget(task, collector))
        metrics = collector.summary()
        write(output / "normal-read-tool-metrics.json", metrics)
        captures = [
            capture_inventory(core_capture, "core", "core-any"),
            capture_inventory(ue_capture, "ue", "ue-any"),
        ]
        write(output / "capture-inventories.json", captures)
        all_chains = fields["upf"]["filter_inventory"]
        after_health = health()
        write(output / "health-after.json", after_health)
        checks = {
            "normal_probe_success": probe["returncode"] == 0
            and " 0% packet loss" in probe["stdout"],
            "health_before_and_after": before_health["pass"] and after_health["pass"],
            "three_read_only_chains": set(all_chains) == {"INPUT", "OUTPUT", "FORWARD"}
            and all(
                v["returncode"] == 0 and v["argv"] == ["iptables", "-nvxL", c]
                for c, v in all_chains.items()
            ),
            "two_nonempty_nontruncated_namespace_captures": all(
                c["packet_records"] > 0 and c["truncated_packets"] == 0 for c in captures
            ),
            "different_capture_bytes": captures[0]["capture_sha256"]
            != captures[1]["capture_sha256"],
            "capture_windows_overlap": max(c["first_packet_epoch"] for c in captures)
            <= min(c["last_packet_epoch"] for c in captures),
            "captures_within_observation": all(
                datetime.fromisoformat(snapshot["window_start"]).timestamp()
                <= c["first_packet_epoch"]
                <= c["last_packet_epoch"]
                <= datetime.fromisoformat(snapshot["window_end"]).timestamp()
                for c in captures
            ),
            "only_two_charged_normal_reads": metrics["invocations"]["tool"]["attempted"] == 2,
            "source_not_auto_approved": all(
                not b.corroborated for b in tools.bindings.values() if b.category == "R"
            ),
        }
        result.update(
            engineering_pass=all(checks.values()),
            checks=checks,
            captures=captures,
            source_admission_approval=False,
            packet_matching_or_delivery_proved=False,
            actual_normal_read_attempts=metrics["invocations"]["tool"]["attempted"],
        )
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}:{exc}"
    finally:
        for resource, is_network in reversed(created):
            try:
                assert_owned(resource, owner, is_network)
                receipt = command(
                    ["docker", "network", "rm", resource]
                    if is_network
                    else ["docker", "rm", "-f", resource]
                )
                teardown.append(receipt)
            except Exception as exc:
                teardown.append({"resource": resource, "error": str(exc)})
        remaining = command(["docker", "ps", "-aq", "--filter", "label=upf.e7.owner=" + owner])
        nets = command(["docker", "network", "ls", "-q", "--filter", "label=upf.e7.owner=" + owner])
        write(
            output / "resources-closeout.json",
            {"teardown": teardown, "containers_remaining": remaining, "networks_remaining": nets},
        )
        result["owned_resources_removed"] = (
            remaining["returncode"] == nets["returncode"] == 0
            and not remaining["stdout"].strip()
            and not nets["stdout"].strip()
        )
        result["engineering_pass"] = (
            result["engineering_pass"] and result["owned_resources_removed"]
        )
        write(output / "command-receipts.json", receipts)
        write(output / "summary.json", result)
        write(
            output / "sha256_manifest.json",
            {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()},
        )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = collect(args.project.resolve(), args.output.resolve(), args.template.resolve())
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["engineering_pass"] else 1)
