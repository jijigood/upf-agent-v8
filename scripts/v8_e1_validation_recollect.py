"""Recapture the existing validation conditions with normal dual-namespace evidence.

The organizer alone sees injections. No original case, heldout or approval is changed.
"""

import argparse
import json
import shutil
import time
from datetime import UTC, datetime
from pathlib import Path

from v8_e1_validation_packet import private_round, validation_cases, verify_condition
from v8_e7_evidence_runner import assert_owned, command, visible_delta

from upf_agent.v8.e1_dataset import inside, read, sha, write
from upf_agent.v8.e1_source_closure import IMAGE, POLICY, admission_checks, policy_code_sha256
from upf_agent.v8.models import digest

CONDITIONS = ("inner-request-filter", "inner-reply-filter", "ogstun-admin-down")


def collect(project, dataset, output):
    if output.exists():
        raise ValueError("fresh recollection output required")
    cases, previous = [], {}
    for manifest, task, visible, task_path in validation_cases(dataset):
        provenance = read(inside(dataset, manifest.provenance_file))
        raw = visible / "data/raw/snapshot.json"
        private = private_round(project, provenance, sha(raw))
        truth = read(private / "truth.json")
        if truth["condition"] not in CONDITIONS:
            raise ValueError("validation condition outside the frozen recollection protocol")
        cases.append(
            {
                "case_id": manifest.case_id,
                "condition": truth["condition"],
                "source_group": manifest.source_group,
                "structure_family": manifest.structure_family,
                "original_raw_sha256": sha(raw),
                "task": task.model_dump(mode="json"),
            }
        )
        for path in (raw, task_path, dataset / manifest.provenance_file, private / "truth.json"):
            previous[str(path)] = sha(path)
    if len(cases) != 12:
        raise ValueError("the existing twelve validation parents are required")
    output.mkdir(parents=True)
    code = output / "code/lab"
    code.mkdir(parents=True)
    for folder, name in (
        ("e7", "control.py"),
        ("e7", "diagnostic_control.py"),
        ("e1", "candidate_control.py"),
        ("e1", "readonly_control.py"),
    ):
        text = (project / "lab" / folder / name).read_text().replace("10.208.7.2", "10.209.15.2")
        (code / name).write_text(text)
    shutil.copy2(Path(__file__), output / "code/runner.py")
    write(
        output / "organizer-only/protocol.json",
        {
            "version": "validation-normal-recollection-1",
            "cases": cases,
            "models": 0,
            "heldout_inputs_read": 0,
            "new_independent_cases": 0,
            "source_policy": POLICY,
            "policy_code_sha256": policy_code_sha256(),
            "code_hashes": {p.name: sha(p) for p in code.iterdir()},
            "Gold_approved": False,
            "human_reviews": 0,
        },
    )
    owner = "e1-recollect-" + output.name
    suffix = digest([str(output), time.time_ns()])[:10]
    network, core, ue = ["upf-e1r-" + suffix + tail for tail in ("-net", "-core", "-ue")]
    created, receipts, rows, closeout = [], [], [], []

    def controlled(container, op, role, *, reader=False, condition=None):
        assert_owned(container, owner)
        argv = [
            "docker",
            "exec",
            container,
            "python3",
            "/control/" + ("readonly_control.py" if reader else "candidate_control.py"),
            op,
            "--role",
            role,
        ]
        if condition:
            argv += ["--condition", condition]
        r = command(argv)
        receipts.append(r)
        if r["returncode"]:
            raise RuntimeError("owned capture operation failed: " + json.dumps(r))
        return json.loads(r["stdout"])

    def health():
        attempts = []
        for _ in range(20):
            r = controlled(ue, "health", "ue")
            attempts.append(r)
            if r["returncode"] == 0 and " 0% packet loss" in r["stdout"]:
                return {"pass": True, "attempts": attempts}
            time.sleep(1)
        return {"pass": False, "attempts": attempts}

    result = {
        "planned": 12,
        "complete": False,
        "actual_human_reviews": 0,
        "heldout_inputs_read": 0,
        "model_calls": 0,
        "formal_e1_completed": False,
    }
    try:
        r = command(
            [
                "docker",
                "network",
                "create",
                "--internal",
                "--subnet",
                "10.209.15.0/24",
                "--label",
                "upf.e7.owner=" + owner,
                network,
            ]
        )
        receipts.append(r)
        if r["returncode"]:
            raise RuntimeError("isolated recollection network failed")
        created.append((network, True))
        for container, ip in ((core, "10.209.15.2"), (ue, "10.209.15.3")):
            r = command(
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
                    str(code) + ":/control:ro",
                    IMAGE,
                ]
            )
            receipts.append(r)
            if r["returncode"]:
                raise RuntimeError("owned recollection container failed")
            created.append((container, False))
            inspected = assert_owned(container, owner)
            if (
                inspected["Image"] != IMAGE
                or inspected["HostConfig"]["Privileged"]
                or inspected["HostConfig"]["PortBindings"]
            ):
                raise ValueError("owned container isolation/image mismatch")
        deployment = {"image": IMAGE}
        for key, container, argv in (
            ("open5gs", core, ["/opt/open5gs/bin/open5gs-upfd", "-v"]),
            ("ueransim", ue, ["/opt/src/UERANSIM/cmake-build-release/nr-ue", "--version"]),
        ):
            r = command(["docker", "exec", container, *argv])
            receipts.append(r)
            deployment[key] = r
        write(output / "deployment.json", deployment)
        for container, role in ((core, "core"), (ue, "ue")):
            write(
                output / "organizer-only" / (role + "-boot.json"),
                controlled(container, "boot", role),
            )
        for case in cases:
            cid = case["case_id"]
            private = output / "organizer-only" / cid
            before_health = health()
            write(private / "health-before.json", before_health)
            if not before_health["pass"]:
                raise RuntimeError("recollection baseline unhealthy")
            before = {
                "core": controlled(core, "snapshot", "core", reader=True),
                "ue": controlled(ue, "snapshot", "ue", reader=True),
            }
            row = {"case_id": cid, "injection_verified": False, "recovery_verified": False}
            rows.append(row)
            try:
                write(
                    private / "inject.json",
                    controlled(core, "inject", "core", condition=case["condition"]),
                )
                started = datetime.now(UTC).isoformat()
                for container, role in ((core, "core"), (ue, "ue")):
                    controlled(container, "capture-start", role, reader=True)
                probe = controlled(ue, "health", "ue")
                captures = [
                    controlled(container, "capture-end", role, reader=True)
                    for container, role in ((core, "core"), (ue, "ue"))
                ]
                snapshot = visible_delta(
                    before,
                    {
                        "core": controlled(core, "snapshot", "core", reader=True),
                        "ue": controlled(ue, "snapshot", "ue", reader=True),
                        "normal_probe": probe,
                        "packet_capture": captures[0],
                        "ue_packet_capture": captures[1],
                        "window_start": started,
                        "window_end": datetime.now(UTC).isoformat(),
                    },
                )
                target = output / "normal-inputs" / cid / "snapshot.json"
                write(target, snapshot)
                external = controlled(core, "verify", "core")
                write(private / "external-verification.json", external)
                row["injection_verified"] = verify_condition(case["condition"], snapshot, external)
                checks = admission_checks(snapshot, deployment)
                write(
                    output / "normal-inputs" / cid / "source-admission.json",
                    {
                        "policy": POLICY,
                        "policy_sha256": digest(POLICY),
                        "policy_code_sha256": policy_code_sha256(),
                        "raw_sha256": sha(target),
                        "deployment": deployment,
                        "checks": checks,
                        "expert_reviewed": False,
                        "causal_approval": False,
                    },
                )
                row["provenance_checks_pass"] = all(checks.values())
                write(
                    private / "truth.json",
                    {
                        "condition": case["condition"],
                        "verified": row["injection_verified"],
                        "experimental_truth_only": True,
                        "expert_Gold": False,
                    },
                )
            finally:
                write(private / "cleanup.json", controlled(core, "cleanup", "core"))
                after_health = health()
                write(private / "health-after.json", after_health)
                row["recovery_verified"] = after_health["pass"]
            print(json.dumps(row), flush=True)
            if not all(
                row.get(k)
                for k in ("injection_verified", "recovery_verified", "provenance_checks_pass")
            ):
                raise RuntimeError("recollection failed; original failure retained")
        result["complete"] = len(rows) == 12
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}:{exc}"
    finally:
        for resource, is_network in reversed(created):
            try:
                assert_owned(resource, owner, is_network)
                closeout.append(
                    command(
                        ["docker", "network", "rm", resource]
                        if is_network
                        else ["docker", "rm", "-f", resource]
                    )
                )
            except Exception as exc:
                closeout.append({"resource": resource, "error": str(exc)})
        remaining = [
            command(["docker", "ps", "-aq", "--filter", "label=upf.e7.owner=" + owner]),
            command(["docker", "network", "ls", "-q", "--filter", "label=upf.e7.owner=" + owner]),
        ]
        result["resources_removed"] = all(
            r["returncode"] == 0 and not r["stdout"].strip() for r in remaining
        )
        result["original_validation_unchanged"] = all(
            sha(Path(name)) == expected for name, expected in previous.items()
        )
        result["complete"] &= (
            result["resources_removed"] and result["original_validation_unchanged"]
        )
        result["rows"] = rows
        write(output / "organizer-only/command-receipts.json", receipts)
        write(output / "resources-closeout.json", {"teardown": closeout, "remaining": remaining})
        write(output / "original-inputs-sha256.json", previous)
        write(output / "summary.json", result)
        write(
            output / "sha256_manifest.json",
            {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()},
        )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dataset", type=Path, default=Path("eval/v8/e1"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = collect(args.project.resolve(), args.dataset.resolve(), args.output.resolve())
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["complete"] else 1)
