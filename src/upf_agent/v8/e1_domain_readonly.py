"""Opt-in E1 namespace observations and bounded actions; never an execution backend.

Old tasks, registry and Gold remain untouched. Real projections are unapproved.
The only tool reads frozen normal captures; it never reads injector/private files.
"""

import base64
import hashlib
import json
import struct
from pathlib import Path
from typing import Literal

import networkx as nx
from pydantic import Field, ValidationError, model_validator

from upf_agent.agent_contracts import ToolPacket
from upf_agent.agent_tools import evidence, failure
from upf_agent.contracts import ResultStatus, ToolResult
from upf_agent.v8.action_registry import ACTIONS
from upf_agent.v8.adapters import source_path
from upf_agent.v8.common_tools import CommonEvidenceTools
from upf_agent.v8.compiler import permitted
from upf_agent.v8.models import Model, digest, object_product_version
from upf_agent.v8.plan_ir import PlanIR, TranslationReceipt
from upf_agent.v8.plan_source_verifier import verify_plan_source
from upf_agent.v8.plan_translator import translate_plan
from upf_agent.v8.plan_validator import PlanValidationReport, ValidationIssue, validate_plan

REGISTRY_VERSION = "v8-e1-readonly-registry-candidate-1"
SCOPE_VERSION = "v8-e1-namespace-scope-candidate-1"
DOMAIN_FIELDS = ("tun_inventory", "filter_inventory", "session_probe_inventory", "packet_inventory")


class NamespaceScope(Model):
    namespace: Literal["core", "ue"]
    devices: list[Literal["ogstun", "uesimtun0"]] = Field(default_factory=list)
    captures: list[Literal["core-any", "ue-any"]] = Field(default_factory=list)
    readable_fields: list[str]
    probe_ids: list[Literal["normal", "small", "large"]] = Field(default_factory=list)


class DomainScope(Model):
    version: Literal["v8-e1-namespace-scope-candidate-1"] = SCOPE_VERSION
    raw_path: Literal["data/raw/snapshot.json"] = "data/raw/snapshot.json"
    raw_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    objects: dict[str, NamespaceScope]

    @model_validator(mode="after")
    def registered_namespaces(self):
        ordinary = {"event_type", "log_excerpt", "domain_namespace"}
        limits = {
            "upf": (
                "core",
                {"ogstun"},
                {"core-any"},
                ordinary | {"tun_inventory", "filter_inventory", "packet_inventory"},
            ),
            "ran": ("core", set(), set(), ordinary),
            "ue": (
                "ue",
                {"uesimtun0"},
                {"ue-any"},
                ordinary | {"tun_inventory", "session_probe_inventory", "packet_inventory"},
            ),
        }
        for obj, allowed in self.objects.items():
            if obj not in limits:
                raise ValueError("object outside registered E1 namespace scope")
            namespace, devices, captures, fields = limits[obj]
            if (
                allowed.namespace != namespace
                or not set(allowed.devices) <= devices
                or not set(allowed.captures) <= captures
                or not set(allowed.readable_fields) <= fields
            ):
                raise ValueError("registered namespace/device/field scope mismatch")
            if obj != "ue" and allowed.probe_ids:
                raise ValueError("probe records belong to the explicit UE scope")
        return self


class ReadBasis(Model):
    namespace: Literal["core", "ue"]
    basis: Literal["inspect_existing", "collect_then_check"]
    pending: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def mode(self):
        if (self.basis == "inspect_existing" and self.pending) or (
            self.basis == "collect_then_check" and not self.pending
        ):
            raise ValueError("basis and pending information disagree")
        return self


class TunParams(ReadBasis):
    device: Literal["ogstun", "uesimtun0"]


class FilterParams(ReadBasis):
    table: Literal["filter"] = "filter"
    chain: Literal["INPUT", "OUTPUT", "FORWARD"]


class ProbeParams(ReadBasis):
    device: Literal["uesimtun0"] = "uesimtun0"
    probe_id: Literal["normal", "small", "large"]


class CaptureParams(ReadBasis):
    capture_id: Literal["core-any", "ue-any"]


class CapturePairParams(CaptureParams):
    peer_object_id: str
    peer_capture_id: Literal["core-any", "ue-any"]


DOMAIN_ACTIONS = {
    "READ_TUN_INTERFACE": (TunParams, "read", "read", ["tun_inventory"], False),
    "READ_FILTER_COUNTERS": (FilterParams, "read", "read", ["filter_inventory"], False),
    "READ_SESSION_PROBE": (ProbeParams, "read", "read", ["session_probe_inventory"], False),
    "READ_PACKET_CAPTURE": (CaptureParams, "read", "read", ["packet_inventory"], False),
    # Only capture location, time overlap and completeness, not packet/causal matching.
    "COMPARE_CAPTURE_WINDOWS": (CapturePairParams, "read", "read", ["packet_inventory"], False),
}
CANDIDATE_ACTIONS = {**ACTIONS, **DOMAIN_ACTIONS}


class DomainPlanIR(PlanIR):
    registry_version: Literal["v8-e1-readonly-registry-candidate-1"] = REGISTRY_VERSION


class DomainTranslationReceipt(TranslationReceipt):
    translator_version: str = "v8-e1-domain-json-translator-candidate-1"
    plan: DomainPlanIR | None = None


class DomainValidationReport(PlanValidationReport):
    validator_version: str = "v8-e1-domain-validator-candidate-2"
    published_plan: DomainPlanIR | None = None


def translate_domain_plan(raw):
    return translate_plan(raw, plan_type=DomainPlanIR, receipt_type=DomainTranslationReceipt)


def load_scope(root, task):
    scope = DomainScope.model_validate_json(source_path(root, "data/domain-scope.json").read_text())
    if task.permission.revision != f"{SCOPE_VERSION}:{digest(scope)}":
        raise ValueError("namespace scope does not match the trusted permission revision")
    if set(scope.objects) != set(task.objects):
        raise ValueError("namespace scope must cover exactly the task objects")
    for obj, allowed in scope.objects.items():
        if not permitted(task, obj, allowed.readable_fields):
            raise ValueError("namespace field scope exceeds task permission")
    raw = source_path(root, scope.raw_path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != scope.raw_sha256:
        raise ValueError("frozen normal capture hash mismatch")
    return scope


def capture_inventory(capture, namespace, capture_id):
    if not capture or "capture_base64" not in capture:
        return None
    raw = base64.b64decode(capture["capture_base64"], validate=True)
    magic = raw[:4].hex()
    if len(raw) < 24 or magic not in {"d4c3b2a1", "4d3cb2a1", "a1b2c3d4", "a1b23c4d"}:
        raise ValueError("classic pcap required")
    endian = "<" if magic in {"d4c3b2a1", "4d3cb2a1"} else ">"
    scale = 1_000_000_000 if magic in {"4d3cb2a1", "a1b23c4d"} else 1_000_000
    offset, count, truncated, times = 24, 0, 0, []
    while offset < len(raw):
        if offset + 16 > len(raw):
            raise ValueError("partial pcap record header")
        sec, fraction, included, original = struct.unpack(
            endian + "IIII", raw[offset : offset + 16]
        )
        offset += 16
        if fraction >= scale or included > original or offset + included > len(raw):
            raise ValueError("invalid or partial pcap record")
        count += 1
        truncated += included < original
        times.append(sec + fraction / scale)
        offset += included
    result = {
        "namespace": namespace,
        "capture_id": capture_id,
        "capture_position": capture.get("capture_position", "unknown"),
        "capture_sha256": hashlib.sha256(raw).hexdigest(),
        "pcap_bytes": len(raw),
        "packet_records": count,
        "truncated_packets": truncated,
        "link_type": struct.unpack(endian + "I", raw[20:24])[0],
        "first_packet_epoch": min(times) if times else None,
        "last_packet_epoch": max(times) if times else None,
        "packet_matching_or_delivery_proved": False,
    }
    # New parser adds explicit observations, never silently upgrades window comparison.
    from upf_agent.v8.e1_packet_observations import observations

    result["plain_icmp"] = observations(capture)
    return result


def extract_normal_fields(root, scope):
    raw = json.loads(source_path(root, scope.raw_path).read_text())
    output = {}
    for obj, allowed in scope.objects.items():
        namespace = raw[allowed.namespace]
        fields = {
            "event_type": "frozen_namespace_observation",
            "domain_namespace": allowed.namespace,
        }
        logs = namespace.get("logs_and_config", {})
        # Scope deliberately separates UPF, gNB and UE windows in a shared core namespace.
        filename = "upf.log" if obj == "upf" else "gnb.log" if obj == "ran" else "ue.log"
        fields["log_excerpt"] = logs.get(filename, "")
        interfaces = namespace.get("interfaces")
        if (
            "tun_inventory" in allowed.readable_fields
            and interfaces
            and interfaces["returncode"] == 0
        ):
            items = json.loads(interfaces["stdout"])
            if not isinstance(items, list):
                raise ValueError("interface inventory must be a list")
            fields["tun_inventory"] = [
                {
                    k: item[k]
                    for k in ["ifname", "flags", "mtu", "operstate", "addr_info"]
                    if k in item
                }
                for item in items
                if item.get("ifname") in allowed.devices
            ]
        # Never copy private/external-verification rules into a normal observation.
        filters = namespace.get("filter_inventory")
        if "filter_inventory" in allowed.readable_fields and filters is not None:
            expected = {c: ["iptables", "-nvxL", c] for c in ["INPUT", "OUTPUT", "FORWARD"]}
            if any(c not in expected or v.get("argv") != expected[c] for c, v in filters.items()):
                raise ValueError("unregistered filter read command")
            fields["filter_inventory"] = filters
        if "session_probe_inventory" in allowed.readable_fields:
            probes = raw.get("normal_probes", {"normal": raw.get("normal_probe")})
            fields["session_probe_inventory"] = {
                "namespace": allowed.namespace,
                "session_log_excerpt": logs.get("ue.log", ""),
                "probe_records": {k: v for k, v in probes.items() if k in allowed.probe_ids and v},
                "session_established": None,
                "session_applicability_or_cause_verified": False,
            }
        if "packet_inventory" in allowed.readable_fields:
            capture = (
                raw.get("packet_capture")
                if allowed.namespace == "core"
                else raw.get("ue_packet_capture")
            )
            result = (
                capture_inventory(capture, allowed.namespace, allowed.captures[0])
                if allowed.captures
                else None
            )
            if result is not None:
                fields["packet_inventory"] = result
        output[obj] = {k: v for k, v in fields.items() if k in allowed.readable_fields}
    return output


def verify_domain_binding(root, b, task, scope):
    if (
        not verify_plan_source(root, b, task)
        or b.category != "R"
        or b.object_id not in scope.objects
    ):
        return False
    expected = extract_normal_fields(root, scope)[b.object_id]
    return all(k in expected and expected[k] == v for k, v in b.fields.items())


class DomainReadArgs(Model):
    object_id: str
    fields: list[str] = Field(min_length=1)


class DomainEvidenceTools(CommonEvidenceTools):
    version = "v8-e1-frozen-readonly-tools-candidate-1"

    def __init__(self, root, task, contract, budget):
        self.scope = load_scope(root, task)
        super().__init__(root, task, contract, budget, allow_real=not task.synthetic)
        # Shared, preregistered preparation for every method, charged before native work.
        self.shared_readbacks = []
        for obj, allowed in self.scope.objects.items():
            fields = [f for f in DOMAIN_FIELDS if f in allowed.readable_fields]
            if fields:
                packet = self.read_domain_snapshot({"object_id": obj, "fields": fields})
                self.shared_readbacks.append(
                    {"object_id": obj, "status": packet.result.status.value, "gaps": packet.gaps}
                )

    def _rows(self):
        for relative, body, index, record, sha in super()._rows():
            allowed = self.scope.objects[record["object_id"]].readable_fields
            record = {
                **record,
                "fields": {k: v for k, v in record["fields"].items() if k in allowed},
            }
            yield relative, body, index, record, sha

    def read_domain_snapshot(self, request):
        self.budget.check("tool", request)
        with self.budget.collector.measure("tool", "read_domain_snapshot", request):
            try:
                args = DomainReadArgs.model_validate(request)
            except ValidationError:
                return failure("invalid_arguments", "invalid bounded read request")
            allowed = self.scope.objects.get(args.object_id)
            if not allowed or not set(args.fields) <= set(allowed.readable_fields):
                return failure("scope_denied", "object or field outside namespace scope")
            # Actual source reads, independent of plan generation and organizer material.
            fields = extract_normal_fields(self.root, self.scope)[args.object_id]
            if any(f not in fields for f in args.fields):
                gaps = [
                    f"{args.object_id}:{f}:not_in_normal_capture"
                    for f in args.fields
                    if f not in fields
                ]
            else:
                gaps = []
            entries = []
            # Use the same provenance-preserving binder as the public native backend.
            from upf_agent.agent_contracts import AgentTask
            from upf_agent.contracts import TaskType

            agent = AgentTask(
                run_id=self.task.run_id,
                question=self.task.question,
                task_type=TaskType.DIAGNOSE,
                log_generation=digest([self.task.observation_files, "public-synthetic-generation"])[
                    :20
                ],
                device_ids=[args.object_id],
                product=self.task.product,
                version=self.task.version,
            )
            # The nested read is deliberately not counted as a second public invocation.
            for relative, body, index, record, sha in self._rows():
                if record["object_id"] != args.object_id or record["category"] != "R":
                    continue
                from upf_agent.v8.models import EvidenceBinding, SourcePointer

                native = f"{Path(relative).stem}:observation:{index}"
                entry = evidence(
                    agent,
                    native,
                    body["source_id"],
                    sha,
                    f"/observations/{index}",
                    "tool",
                    json.dumps(record, ensure_ascii=False),
                    {"device_id": args.object_id, "relative_path": relative, "record": record},
                )
                entries.append(entry)
                for req in self.contract.requirements:
                    if req.kind != "R" or args.object_id not in req.objects:
                        continue
                    b = EvidenceBinding(
                        evidence_id=f"{entry.evidence_id}:{req.requirement_id}",
                        native_id=native,
                        task_id=self.task.run_id,
                        contract_id=self.contract.contract_id,
                        requirement_id=req.requirement_id,
                        object_id=args.object_id,
                        category="R",
                        fields=record["fields"],
                        source=SourcePointer(
                            source_id=body["source_id"],
                            sha256=sha,
                            locator=f"/observations/{index}",
                            relative_path=relative,
                        ),
                        observed=record.get("observed"),
                        product=record.get("product"),
                        version=record.get("version"),
                        receipt_id=entry.evidence_id,
                        synthetic=body["synthetic"],
                        source_verified=True,
                        corroborated=body.get("corroborated") is True,
                    )
                    if not verify_domain_binding(self.root, b, self.task, self.scope):
                        return failure(
                            "corrupt_source", "normal projection does not match raw capture"
                        )
                    self.bindings[b.evidence_id] = b
            return ToolPacket(
                result=ToolResult(
                    status=ResultStatus.COMPLETED if entries else ResultStatus.MISSING_SOURCE,
                    elapsed_ms=0,
                    evidence_ids=[e.evidence_id for e in entries],
                    data={"source_admission_changed": False, "field_gaps": gaps},
                ),
                evidence=entries,
                gaps=gaps,
            )


def selector(params):
    for name in ["chain", "probe_id", "capture_id", "device"]:
        if hasattr(params, name):
            return getattr(params, name)
    return None


def field_gap(obj, field, selected=None):
    suffix = f":{selected}" if selected else ""
    return f"{obj}:{field}{suffix}:missing_or_inadmissible"


def supports_fields(b, fields, params, *, peer=False):
    if not all(f in b.fields and b.fields[f] is not None for f in fields):
        return False
    if "filter_inventory" in fields:
        receipt = b.fields["filter_inventory"].get(params.chain)
        return (
            isinstance(receipt, dict)
            and receipt.get("returncode") == 0
            and isinstance(receipt.get("stdout"), str)
        )
    if "session_probe_inventory" in fields:
        return params.probe_id in b.fields["session_probe_inventory"]["probe_records"]
    if "packet_inventory" in fields:
        return b.fields["packet_inventory"]["capture_id"] == (
            params.peer_capture_id if peer else params.capture_id
        )
    return True


def domain_eligible(root, b, task, contract, context, scope):
    """Independent field evidence eligibility, not the generation capability mask."""
    if b.deleted or b.task_id != task.run_id or b.contract_id != contract.contract_id:
        return False
    if not b.corroborated or not b.readable or not permitted(task, b.object_id, list(b.fields)):
        return False
    if b.synthetic and not task.synthetic:
        return False
    product, version = object_product_version(task, b.object_id)
    if not version or b.version != version or b.product != product:
        return False
    if b.valid and not b.valid.start <= context.as_of < b.valid.end:
        return False
    if (
        not b.observed
        or b.observed.end > context.as_of
        or (context.as_of - b.observed.end).total_seconds() > 300
    ):
        return False
    return verify_domain_binding(root, b, task, scope)


def validate_domain_plan(
    plan,
    bindings,
    task,
    contract,
    context,
    root,
    *,
    action_registry=None,
    report_type=DomainValidationReport,
    registry_version=REGISTRY_VERSION,
    conditional_capture_observations=False,
):
    actions = CANDIDATE_ACTIONS if action_registry is None else action_registry
    report = validate_plan(
        plan,
        bindings,
        task,
        contract,
        context,
        root,
        action_registry=actions,
        report_type=report_type,
        peer_reference_categories={"VERIFY_PEER_MAPPING": {"P"}, "COMPARE_CAPTURE_WINDOWS": {"R"}},
    )
    if plan is None:
        return report

    def issue(code, step=None):
        report.issues.append(ValidationIssue(code=code, step_id=step))

    if plan.registry_version != registry_version:
        issue("domain_registry_mismatch")
    try:
        scope = load_scope(root, task)
    except (OSError, ValueError, KeyError, TypeError):
        issue("domain_scope_or_normal_source_invalid")
        scope = None
    admissible = {
        b.evidence_id: b
        for b in bindings
        if scope is not None and domain_eligible(root, b, task, contract, context, scope)
    }
    originals = {b.evidence_id: b for b in bindings}
    if scope is not None:
        for step in plan.steps:
            for ref in step.evidence:
                b = originals.get(ref.evidence_id)
                if (
                    b is not None
                    and b.category == "R"
                    and not verify_domain_binding(root, b, task, scope)
                ):
                    issue("domain_raw_projection_mismatch", step.step_id)
    graph = nx.DiGraph()
    graph.add_nodes_from(s.step_id for s in plan.steps)
    graph.add_edges_from((d, s.step_id) for s in plan.steps for d in s.depends_on)
    for step in plan.steps:
        spec = actions.get(step.action_type) if step.action_type in DOMAIN_ACTIONS else None
        if spec is None or scope is None:
            continue
        try:
            params = spec[0].model_validate(step.parameters)
        except ValidationError:
            continue
        allowed = scope.objects.get(step.target)
        if not allowed or params.namespace != allowed.namespace:
            issue("domain_namespace_denied", step.step_id)
            continue
        if hasattr(params, "device") and params.device not in allowed.devices:
            issue("domain_device_denied", step.step_id)
        if hasattr(params, "capture_id") and params.capture_id not in allowed.captures:
            issue("domain_capture_scope_denied", step.step_id)
        if hasattr(params, "probe_id") and params.probe_id not in allowed.probe_ids:
            issue("domain_probe_scope_denied", step.step_id)
        targets = [step.target]
        peer = getattr(params, "peer_object_id", None)
        if peer is not None:
            peer_scope = scope.objects.get(peer)
            if (
                peer == step.target
                or not peer_scope
                or params.peer_capture_id not in peer_scope.captures
            ):
                issue("domain_peer_capture_denied", step.step_id)
            else:
                targets.append(peer)
                if peer_scope.namespace == allowed.namespace:
                    issue("independent_capture_positions_missing", step.step_id)
        ancestors = nx.ancestors(graph, step.step_id)
        for obj in targets:
            if not any(
                s.action_type == "CHECK_IDENTITY" and s.target == obj and s.step_id in ancestors
                for s in plan.steps
            ):
                issue("domain_identity_dependency_missing", step.step_id)
            if not set(spec[3]) <= set(scope.objects[obj].readable_fields):
                issue("domain_field_permission_denied", step.step_id)
        fields = spec[3]
        available = {}
        for obj in targets:
            available[obj] = [
                b
                for b in admissible.values()
                if b.object_id == obj
                and supports_fields(b, fields, params, peer=obj != step.target)
            ]
        gaps = sorted(
            field_gap(obj, f, params.peer_capture_id if obj != step.target else selector(params))
            for obj in targets
            for f in fields
            if not available[obj]
        )
        if params.basis == "collect_then_check":
            if not gaps or sorted(set(params.pending)) != gaps or step.evidence:
                issue("domain_pending_gap_mismatch", step.step_id)
        else:
            cited = [admissible.get(r.evidence_id) for r in step.evidence]
            if gaps or any(
                not any(b is not None and b in available[obj] for b in cited) for obj in targets
            ):
                issue("domain_existing_basis_incomplete", step.step_id)
            if any(b is None or not any(b in available[obj] for obj in targets) for b in cited):
                issue("domain_unrelated_citation", step.step_id)
            if len({r.evidence_id for r in step.evidence}) != len(step.evidence):
                issue("domain_duplicate_citation", step.step_id)
            for b in cited:
                if b is not None and "packet_inventory" in b.fields:
                    capture = b.fields["packet_inventory"]
                    for key in ["first_packet_epoch", "last_packet_epoch"]:
                        when = capture[key]
                        if (
                            when is not None
                            and not b.observed.start.timestamp()
                            <= when
                            <= b.observed.end.timestamp()
                        ):
                            issue("capture_time_outside_observation_window", step.step_id)
        if (
            step.action_type == "COMPARE_CAPTURE_WINDOWS"
            and params.basis == "inspect_existing"
            and not gaps
        ):
            captures = [available[obj][0].fields["packet_inventory"] for obj in targets]
            if len(captures) != 2 or captures[0]["capture_sha256"] == captures[1]["capture_sha256"]:
                issue("independent_capture_sources_missing", step.step_id)
            elif any(c["first_packet_epoch"] is None or c["truncated_packets"] for c in captures):
                if conditional_capture_observations and step.on_unknown in {
                    "request_evidence",
                    "human_review",
                }:
                    report.preconditions.append(
                        {
                            "step_id": step.step_id,
                            "predicate": "capture_nonempty_complete",
                            "value": "unknown",
                            "on_unknown": step.on_unknown,
                        }
                    )
                else:
                    issue("capture_empty_or_truncated", step.step_id)
            elif max(c["first_packet_epoch"] for c in captures) > min(
                c["last_packet_epoch"] for c in captures
            ):
                issue("capture_windows_do_not_overlap", step.step_id)
    if report.issues:
        report.raw_plan_validity = report.published_plan_validity = False
        report.published_plan = None
        report.retained_steps = 0
        report.rejected_steps = len(plan.steps)
    return report


def domain_score(plan, validation, gold):
    return {
        "case_id": gold.case_id,
        "reviewed": False,
        "solvability": None,
        "parsed": plan is not None,
        "unscorable": plan is None,
        "validator_pass": validation.raw_plan_validity,
        "published_validator_pass": validation.published_plan_validity,
        "reference_pass": None,
        "vpr": None,
        "branch": None,
        "forbidden_action": any(s.effect_kind == "network_write" for s in plan.steps)
        if plan
        else False,
        "hard_constraint_violation": any(i.severity == "hard" for i in validation.issues),
        "issues": [i.code for i in validation.issues],
        "retained_steps": validation.retained_steps,
        "rejected_steps": validation.rejected_steps,
        "rewritten_steps": validation.rewritten_steps,
    }
