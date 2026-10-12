"""Opt-in, machine provenance policy for newly owned normal captures.

This certifies recorded observations, not diagnosis, human review or expert Gold.
Original sources and the formal default policy are never upgraded retrospectively.
"""

import hashlib
import json
from datetime import datetime

from upf_agent.v8.e1_dataset import read, sha
from upf_agent.v8.e1_domain_readonly import (
    DomainEvidenceTools,
    capture_inventory,
    extract_normal_fields,
    load_scope,
)
from upf_agent.v8.e1_packet_observations import observations
from upf_agent.v8.models import digest

IMAGE = "sha256:0298b2faf2810793b7d21ee61fd9f0189c35e22e3e3565b8dcfd615f78c04a3d"
POLICY = {
    "version": "v8-e1-owned-normal-provenance-candidate-2",
    "image": IMAGE,
    "allowed_raw_keys": [
        "core",
        "ue",
        "normal_probe",
        "packet_capture",
        "ue_packet_capture",
        "window_start",
        "window_end",
    ],
    "source_kind": "new owned collector observations; machine verified provenance",
    "human_review": False,
    "causal_or_expert_approval": False,
    "requires": [
        "image_and_runtime_versions",
        "role_and_read_commands",
        "window",
        "three_filter_chains",
        "two_namespace_pcaps",
        "exact_raw_projection",
    ],
}


def admission_checks(snapshot, deployment):
    start, end = (datetime.fromisoformat(snapshot[k]) for k in ("window_start", "window_end"))
    checks = {
        "only_normal_keys": set(snapshot) == set(POLICY["allowed_raw_keys"]),
        "fixed_image": deployment.get("image") == IMAGE,
        "actual_versions": (
            deployment.get("open5gs", {}).get("returncode") == 0
            and deployment["open5gs"].get("stdout", "").strip() == "Open5GS v2.7.6"
            and deployment.get("ueransim", {}).get("returncode") in {0, 1}
            and deployment["ueransim"].get("stdout", "").strip() == "v3.2.7"
        ),
        "bounded_utc_window": start.utcoffset() is not None
        and end.utcoffset() is not None
        and 0 < (end - start).total_seconds() <= 90,
    }
    for role, device in (("core", "ogstun"), ("ue", "uesimtun0")):
        body = snapshot[role]
        interfaces = body["interfaces"]
        checks[role + "_role"] = body.get("role") == role and body.get("synthetic") is False
        checks[role + "_read_interfaces"] = (
            interfaces.get("argv") == ["ip", "-json", "address"]
            and interfaces.get("returncode") == 0
        )
        checks[role + "_device"] = (
            sum(r.get("ifname") == device for r in json.loads(interfaces["stdout"])) == 1
        )
        capture = snapshot["packet_capture" if role == "core" else "ue_packet_capture"]
        inv = capture_inventory(capture, role, role + "-any")
        checks[role + "_pcap"] = (
            inv["truncated_packets"] == 0
            and inv["packet_records"] > 0
            and capture.get("capture_position") == f"owned {role} namespace any interface"
        )
        checks[role + "_packet_times"] = (
            start.timestamp()
            <= inv["first_packet_epoch"]
            <= inv["last_packet_epoch"]
            <= end.timestamp()
        )
        observations(capture)  # Independent bounded framing/packet parser, including unknowns.
    chains = snapshot["core"].get("filter_inventory", {})
    checks["normal_filter_reads"] = set(chains) == {"INPUT", "OUTPUT", "FORWARD"} and all(
        r.get("argv") == ["iptables", "-nvxL", c] and r.get("returncode") == 0
        for c, r in chains.items()
    )
    probe = snapshot["normal_probe"]
    checks["normal_probe_record"] = probe.get("argv") == [
        "ping",
        "-n",
        "-I",
        "uesimtun0",
        "-c",
        "5",
        "-i",
        ".2",
        "-W",
        "1",
        "10.45.0.1",
    ] and probe.get("returncode") in {0, 1}
    checks["independent_capture_bytes"] = (
        capture_inventory(snapshot["packet_capture"], "core", "core-any")["capture_sha256"]
        != capture_inventory(snapshot["ue_packet_capture"], "ue", "ue-any")["capture_sha256"]
    )
    return checks


def verify_admission(root, task):
    scope = load_scope(root, task)
    receipt = read(root / "data/source-admission.json")
    if receipt.get("policy") != POLICY or receipt.get("policy_sha256") != digest(POLICY):
        raise ValueError("unknown or changed source admission policy")
    if receipt.get("raw_sha256") != scope.raw_sha256 or receipt.get("expert_reviewed") is not False:
        raise ValueError("source admission raw hash or review status mismatch")
    checks = admission_checks(read(root / scope.raw_path), receipt["deployment"])
    if checks != receipt.get("checks") or not all(checks.values()):
        raise ValueError("normal collection provenance checks failed")
    fields = extract_normal_fields(root, scope)
    body = read(root / "data/domain-observations.json")
    if body.get("corroborated") is not True or body.get("raw_sources") != {
        scope.raw_path: scope.raw_sha256
    }:
        raise ValueError("new normal source does not bind the admitted raw capture")
    if body.get("admission_sha256") != sha(root / "data/source-admission.json"):
        raise ValueError("normal source admission receipt changed")
    if {r["object_id"]: r["fields"] for r in body["observations"]} != fields:
        raise ValueError("normal projection differs from raw capture")
    return receipt


class VerifiedDomainTools(DomainEvidenceTools):
    version = "v8-e1-verified-owned-normal-tools-candidate-1"

    def __init__(self, root, task, contract, budget):
        from upf_agent.v8.common_tools import CommonEvidenceTools

        self.admission = verify_admission(root, task)
        self.scope = load_scope(root, task)
        # Normal native log reads already return the domain fields. No forced reads:
        # Direct/P5/v8 can all obtain them through the same existing public catalog.
        CommonEvidenceTools.__init__(self, root, task, contract, budget, allow_real=True)
        self.shared_readbacks = []

    def tool(self, task, call, known, timeout):
        if call.name not in {"search_manual", "read_manual_block"}:
            packet = super().tool(task, call, known, timeout)
            entries = []
            for entry in packet.evidence:
                record = entry.metadata.get("record")
                try:
                    repeated = record is not None and json.loads(entry.excerpt) == record
                except (TypeError, ValueError):
                    repeated = False
                if repeated:
                    entry = entry.model_copy(
                        update={
                            "metadata": {k: v for k, v in entry.metadata.items() if k != "record"}
                            | {"full_normal_record_in_excerpt": True}
                        }
                    )
                entries.append(entry)
            return packet.model_copy(update={"evidence": entries})
        from upf_agent.agent_contracts import ToolPacket
        from upf_agent.agent_tools import evidence, failure, validate_call
        from upf_agent.contracts import ResultStatus, ToolResult
        from upf_agent.p3_index import load_active_index, load_chunks
        from upf_agent.p3_lexical import TechnicalTokenizer, search_bm25
        from upf_agent.v8.compiler import permitted
        from upf_agent.v8.knowledge_applicability import annotate_knowledge
        from upf_agent.v8.models import EvidenceBinding, SourcePointer, object_product_version

        # This adapter validates against explicit object profiles, including UERANSIM.
        # Legacy AgentTask's one product field cannot represent this multi-product scope.
        scoped = task.model_copy(update={"product": None, "version": None})
        args, error = validate_call(scoped, call, known)
        if error:
            return failure(error, error)
        request = call.model_dump(mode="json")
        self.budget.check("tool", request)
        with self.budget.collector.measure("tool", call.name, request):
            directory, manifest = load_active_index(self.root)
            if sha(directory / "chunks.jsonl") != manifest["chunks_sha256"]:
                return failure("corrupt_source", "manual chunk archive hash changed")
            chunks = load_chunks(directory)
            objects = task.device_ids or self.task.objects
            tokenizer = TechnicalTokenizer(self.root / "data/p3/telecom_dictionary.txt")
            entries = []
            for obj in objects:
                if not permitted(self.task, obj, ["instruction"]):
                    continue
                product, version = object_product_version(self.task, obj)
                if call.name == "search_manual":
                    if (
                        args.product
                        and args.product != product
                        or args.version
                        and args.version != version
                    ):
                        continue
                    hits = search_bm25(
                        directory / "bm25",
                        chunks,
                        tokenizer,
                        args.query,
                        product,
                        version,
                        min(args.top_k, 2),
                    )
                else:
                    c = chunks.get(args.chunk_id)
                    hits = (
                        [(c.chunk_id, 1)]
                        if c
                        and c.product == product
                        and c.version == version
                        and (not args.source_id or c.source_id == args.source_id)
                        else []
                    )
                for cid, _ in hits:
                    chunk = chunks[cid]
                    source = self.root / "data/raw" / chunk.relative_path
                    _, start, stop = chunk.locators[0].split(":")
                    if (
                        sha(source) != chunk.source_sha256
                        or source.read_text()[int(start) : int(stop)] != chunk.text
                    ):
                        return failure("corrupt_source", "manual original text projection changed")
                    entry = evidence(
                        task,
                        cid,
                        chunk.source_id,
                        chunk.source_sha256,
                        chunk.locators[0],
                        "manual",
                        chunk.text,
                        {
                            "device_id": obj,
                            "relative_path": "data/raw/" + chunk.relative_path,
                            "product": product,
                            "version": version,
                            "knowledge_generation": manifest["index_generation"],
                        },
                    )
                    entry = entry.model_copy(update={"evidence_id": entry.evidence_id + ":" + obj})
                    entries.append(entry)
                    for req in self.contract.requirements:
                        if req.kind != "K" or obj not in req.objects:
                            continue
                        b = EvidenceBinding(
                            evidence_id=f"{entry.evidence_id}:{req.requirement_id}",
                            native_id=cid,
                            task_id=self.task.run_id,
                            contract_id=self.contract.contract_id,
                            requirement_id=req.requirement_id,
                            object_id=obj,
                            category="K",
                            fields={"instruction": chunk.text},
                            source=SourcePointer(
                                source_id=chunk.source_id,
                                sha256=chunk.source_sha256,
                                relative_path="data/raw/" + chunk.relative_path,
                                locator=chunk.locators[0],
                            ),
                            product=product,
                            version=version,
                            receipt_id=entry.evidence_id,
                            synthetic=False,
                            corroborated=True,
                        )
                        annotate_knowledge(self.root, b)
                        self.bindings[b.evidence_id] = b
            return ToolPacket(
                result=ToolResult(
                    status=ResultStatus.COMPLETED if entries else ResultStatus.MISSING_SOURCE,
                    elapsed_ms=0,
                    evidence_ids=[e.evidence_id for e in entries],
                ),
                evidence=entries,
                gaps=[] if entries else ["no applicable pinned original manual block"],
            )


def policy_code_sha256():
    return hashlib.sha256(open(__file__, "rb").read()).hexdigest()
