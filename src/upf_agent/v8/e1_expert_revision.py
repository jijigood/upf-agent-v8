"""Opt-in revision of the readonly interface requested by the received expert opinions."""

import hashlib
from copy import deepcopy
from typing import Literal

import networkx as nx
from pydantic import Field, ValidationError, model_validator

from upf_agent.v8.e1_dataset import sha
from upf_agent.v8.e1_domain_head import domain_schema, generate_domain_plan
from upf_agent.v8.e1_domain_readonly import (
    CANDIDATE_ACTIONS,
    CapturePairParams,
    load_scope,
    validate_domain_plan,
)
from upf_agent.v8.e1_source_closure import verify_admission
from upf_agent.v8.e1_verified_head import HEAD_INSTRUCTIONS, compact_body, head_manifest
from upf_agent.v8.models import Model, object_product_version
from upf_agent.v8.plan_generator import visible_evidence
from upf_agent.v8.plan_ir import EvidenceReference, PlanIR, PlanStep, TranslationReceipt
from upf_agent.v8.plan_translator import translate_plan
from upf_agent.v8.plan_validator import PlanValidationReport, ValidationIssue

PROFILE = "expert-readonly-revision-1"
REGISTRY = "v8-e1-readonly-registry-candidate-2"
MAX_STEPS = 16
MAX_TOKENS = 3072
INSTRUCTIONS = HEAD_INSTRUCTIONS.replace("最多12步", "最多16步") + (
    "开头的身份前置由Schema保证存在；它们是未来核验计划，不是已完成身份认证。"
    "身份参数绑定正常版本回执与命名空间；版本不符停止。"
    "READ_MANUAL_REFERENCE核对对应产品版本的只读原文，必须引用给出的K条文。"
    "它不检查n4_enabled，不把配置示例当作现场配置。"
    "任务要求的运行日志与手册核对必须显式安排；人工核对不能代替已有资料读取。"
    "session_established=null、空日志和operstate=UNKNOWN不证明正常或故障；必要时补证。"
    "COMPARE_CAPTURE_WINDOWS的input_basis=frozen_capture_inventory，直接核对冻结库存；"
    "不消费未来抓包读取的执行产物，不声称报文匹配或应用送达。"
    "明确填写on_unknown与至少一条expected_observations；写待核验判据，勿编造结果。"
    "原生K/C状态仅表示资料需求，不表示技术一致、诊断完成或网络已恢复。"
    "每步text最多12字，expected_observations最多12字；使用Schema中的短step_id，一行紧凑JSON。"
    "citation_table明示全部原始引用；steps.evidence使用对应cN短键，不能补造引用。"
    "先用step_options查询短ID对应的动作/对象/参数，再自主选择；这些选项不是必需步骤槽位。"
)


class IdentityParams(Model):
    namespace: Literal["core", "ue"]
    product: str
    version: str


class ManualParams(Model):
    product: str
    version: str
    purpose: Literal["runtime_investigation"] = "runtime_investigation"


class CapturePairRevision(CapturePairParams):
    input_basis: Literal["frozen_capture_inventory"] = "frozen_capture_inventory"


ACTIONS = CANDIDATE_ACTIONS | {
    "CHECK_IDENTITY": (IdentityParams, "read", "read", ["domain_namespace"], False),
    "READ_MANUAL_REFERENCE": (ManualParams, "read", "read", ["instruction"], True),
    "COMPARE_CAPTURE_WINDOWS": (CapturePairRevision, "read", "read", ["packet_inventory"], False),
}


class RevisionPlan(PlanIR):
    registry_version: Literal["v8-e1-readonly-registry-candidate-2"] = REGISTRY
    identity_source_admission_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    citation_table: dict[str, EvidenceReference] = Field(min_length=1)

    @model_validator(mode="before")
    @classmethod
    def explicit_citation_table(cls, value):
        if not isinstance(value, dict):
            return value
        # Assignment validation also calls this hook with already typed steps.
        # Resolve wire aliases only during raw input parsing, preserving those
        # typed values when other validated fields are assigned.
        if not any(
            isinstance(step, dict) and any(isinstance(ref, str) for ref in step.get("evidence", []))
            for step in value.get("steps", [])
        ):
            return value
        table = value.get("citation_table", {})
        result = dict(value)
        steps = []
        for original in value.get("steps", []):
            if not isinstance(original, dict):
                steps.append(original)
                continue
            step = dict(original)
            refs = []
            for ref in step.get("evidence", []):
                if isinstance(ref, str):
                    if ref not in table:
                        raise ValueError("unknown citation key")
                    refs.append(table[ref])
                else:
                    refs.append(ref)
            step["evidence"] = refs
            steps.append(step)
        result["steps"] = steps
        return result


class RevisionTranslation(TranslationReceipt):
    translator_version: str = "v8-e1-expert-revision-translator-2"
    plan: RevisionPlan | None = None


class RevisionValidation(PlanValidationReport):
    validator_version: str = "v8-e1-expert-revision-validator-1"
    published_plan: RevisionPlan | None = None


def translate_revision(raw):
    return translate_plan(raw, plan_type=RevisionPlan, receipt_type=RevisionTranslation)


def identity_parameters(root, task, scope, obj):
    product, version = object_product_version(task, obj)
    return {
        "namespace": scope.objects[obj].namespace,
        "product": product,
        "version": version,
    }


def revision_schema(task, context, bindings, root):
    verify_admission(root, task)
    schema, caps, scope, header = domain_schema(task, context, bindings, root)
    branches = schema["$defs"]["PlanStep"]["anyOf"]
    identity, ordinary = [], []
    for branch in branches:
        props = branch["properties"]
        if props["action_type"]["const"] == "CHECK_IDENTITY":
            params = identity_parameters(root, task, scope, props["target"]["const"])
            props["parameters"] = {
                "type": "object",
                "properties": {k: {"const": v} for k, v in params.items()},
                "required": list(params),
                "additionalProperties": False,
            }
            identity.append(branch)
        else:
            ordinary.append(branch)
            if props["action_type"]["const"] == "READ_LOG":
                props["evidence"]["minItems"] = 1
            if props["action_type"]["const"] == "COMPARE_CAPTURE_WINDOWS":
                p = props["parameters"]
                p["properties"]["input_basis"] = {"const": "frozen_capture_inventory"}
                p["required"].append("input_basis")
    for index, obj in enumerate(task.objects, 1):
        candidates = [
            b
            for b in bindings
            if b.object_id == obj and b.category == "K" and b.evidence_id in caps["admissible_ids"]
        ]
        for b in candidates:
            branch = deepcopy(PlanStep.model_json_schema())
            branch.pop("$defs", None)
            params = {
                "product": b.product,
                "version": b.version,
                "purpose": task.template,
            }
            p = branch["properties"]
            p.update(
                action_type={"const": "READ_MANUAL_REFERENCE"},
                target={"const": obj},
                step_id={"const": f"m{index}-manual-reference"},
                parameters={
                    "type": "object",
                    "properties": {k: {"const": v} for k, v in params.items()},
                    "required": list(params),
                    "additionalProperties": False,
                },
                depends_on={"const": [caps["identity_steps"][obj]]},
                evidence={
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 1,
                    "items": {"const": visible_evidence(b)["citation"]},
                },
                permission_kind={"const": "read"},
                effect_kind={"const": "read"},
                claimed_executed={"const": False},
                non_executable={"const": True},
            )
            branch["required"] = list(
                dict.fromkeys(
                    branch["required"]
                    + ["parameters", "depends_on", "evidence", "permission_kind", "effect_kind"]
                )
            )
            branch["properties"] = {
                k: p[k] for k in ("action_type", "target", "step_id", "text")
            } | {
                k: v for k, v in p.items() if k not in ("action_type", "target", "step_id", "text")
            }
            ordinary.append(branch)
    for branch in identity + ordinary:
        p = branch["properties"]
        p["text"] = {"type": "string", "minLength": 1, "maxLength": 12}
        p["on_unknown"] = {"const": "request_evidence"}
        p["expected_observations"] = {
            "type": "array",
            "minItems": 1,
            "maxItems": 1,
            "items": {"type": "string", "minLength": 1, "maxLength": 12},
        }
        branch["required"] = list(
            dict.fromkeys(branch["required"] + ["on_unknown", "expected_observations"])
        )
    # IDs have no domain meaning. Shorten them before decoding, including every
    # dependency occurrence, without changing actions, parameters or references.
    aliases = {
        name: f"a{i}"
        for i, name in enumerate(sorted({b["properties"]["step_id"]["const"] for b in ordinary}), 1)
    }

    def shorten(value):
        if isinstance(value, str):
            return aliases.get(value, value)
        if isinstance(value, list):
            return [shorten(v) for v in value]
        if isinstance(value, dict):
            return {k: shorten(v) for k, v in value.items()}
        return value

    ordinary = shorten(ordinary)
    table = citation_table(bindings, caps["admissible_ids"])
    by_reference = {tuple(sorted(ref.items())): key for key, ref in table.items()}

    def encode_citations(value):
        if isinstance(value, list):
            return [encode_citations(v) for v in value]
        if isinstance(value, dict):
            literal = value.get("const")
            if isinstance(literal, dict) and set(literal) == {
                "evidence_id",
                "revision",
                "source_sha256",
                "locator",
            }:
                return {"const": by_reference[tuple(sorted(literal.items()))]}
            return {k: encode_citations(v) for k, v in value.items()}
        return value

    schema = encode_citations(schema)
    ordinary = encode_citations(ordinary)
    identity = encode_citations(identity)
    schema["$defs"]["PlanStep"]["anyOf"] = ordinary
    schema["properties"]["registry_version"] = {"const": REGISTRY}
    schema["properties"]["identity_source_admission_sha256"] = {
        "const": sha(root / "data/source-admission.json")
    }
    schema["required"].append("identity_source_admission_sha256")
    schema["properties"]["citation_table"] = {"const": table}
    schema["required"].append("citation_table")
    schema["properties"]["steps"] = {
        "type": "array",
        "prefixItems": identity,
        "items": {"$ref": "#/$defs/PlanStep"},
        "minItems": len(identity),
        "maxItems": MAX_STEPS,
    }
    return schema, caps, scope, header


def validate_revision(plan, bindings, task, contract, context, root):
    report = validate_domain_plan(
        plan,
        bindings,
        task,
        contract,
        context,
        root,
        action_registry=ACTIONS,
        report_type=RevisionValidation,
        registry_version=REGISTRY,
        conditional_capture_observations=True,
    )
    if plan is None:
        return report

    def issue(code, step):
        report.issues.append(ValidationIssue(code=code, step_id=step))

    try:
        verify_admission(root, task)
        if plan.identity_source_admission_sha256 != sha(root / "data/source-admission.json"):
            issue("identity_receipt_hash_mismatch", None)
        scope = load_scope(root, task)
    except (OSError, ValueError, KeyError, TypeError):
        issue("identity_version_receipt_invalid", None)
        scope = None
    graph = nx.DiGraph()
    graph.add_nodes_from(s.step_id for s in plan.steps)
    graph.add_edges_from((d, s.step_id) for s in plan.steps for d in s.depends_on)
    by_id = {b.evidence_id: b for b in bindings}
    for ref in plan.citation_table.values():
        bound = by_id.get(ref.evidence_id)
        if bound is None or ref.model_dump(mode="json") != visible_evidence(bound)["citation"]:
            issue("citation_table_binding_mismatch", None)
    for step in plan.steps:
        if any(ref not in plan.citation_table.values() for ref in step.evidence):
            issue("step_citation_absent_from_table", step.step_id)
        if step.action_type == "CHECK_IDENTITY":
            if scope is not None and (
                step.target not in scope.objects
                or step.parameters != identity_parameters(root, task, scope, step.target)
            ):
                issue("identity_profile_or_receipt_mismatch", step.step_id)
        else:
            ancestors = nx.ancestors(graph, step.step_id)
            if not any(
                s.action_type == "CHECK_IDENTITY"
                and s.target == step.target
                and s.step_id in ancestors
                for s in plan.steps
            ):
                issue("revision_identity_dependency_missing", step.step_id)
        if not step.expected_observations or step.on_unknown != "request_evidence":
            issue("explicit_observation_or_unknown_exit_missing", step.step_id)
        if step.action_type == "READ_LOG":
            cited_logs = [by_id.get(r.evidence_id) for r in step.evidence]
            if not cited_logs or any(
                b is None
                or b.category != "R"
                or b.object_id != step.target
                or "log_excerpt" not in b.fields
                for b in cited_logs
            ):
                issue("runtime_log_reference_missing", step.step_id)
        if step.action_type == "READ_MANUAL_REFERENCE":
            try:
                params = ManualParams.model_validate(step.parameters)
            except ValidationError:
                continue
            cited = [by_id.get(r.evidence_id) for r in step.evidence]
            if len(cited) != 1 or cited[0] is None:
                issue("manual_original_reference_missing", step.step_id)
            else:
                b = cited[0]
                if (
                    b.category != "K"
                    or b.object_id != step.target
                    or (params.product, params.version) != object_product_version(task, step.target)
                    or params.purpose != task.template
                ):
                    issue("manual_object_version_or_location_mismatch", step.step_id)
    if report.issues:
        report.raw_plan_validity = report.published_plan_validity = False
        report.published_plan = None
        report.retained_steps = 0
        report.rejected_steps = len(plan.steps)
    return report


def selected_bindings(bindings):
    selected, seen, manual_objects = [], set(), set()
    for b in bindings:
        key = (b.object_id, b.category, b.source.sha256, b.source.locator)
        if key in seen or b.category == "K" and b.object_id in manual_objects:
            continue
        seen.add(key)
        if b.category == "K":
            manual_objects.add(b.object_id)
        selected.append(b)
    return selected


def citation_table(bindings, admissible_ids):
    eligible = sorted(
        (b for b in bindings if b.evidence_id in admissible_ids),
        key=lambda b: (b.object_id, b.category, b.source.sha256, b.source.locator, b.evidence_id),
    )
    return {f"c{i}": visible_evidence(b)["citation"] for i, b in enumerate(eligible, 1)}


def revision_body(body):
    body = compact_body(body)
    body["action_registry"] = {
        name: {
            "parameter_names": list(spec[0].model_json_schema()["properties"]),
            "permission_kind": spec[1],
            "effect_kind": spec[2],
        }
        for name, spec in ACTIONS.items()
    }
    for row in body["evidence"]:
        if row["category"] == "R" and "packet_inventory" in row["fields"]:
            row["fields"] = deepcopy(row["fields"])
            capture = row["fields"]["packet_inventory"]
            if "plain_icmp" in capture:
                plain = capture["plain_icmp"]
                plain["displayed_record_count"] = len(plain.pop("rows", []))
                plain["rows_omitted_from_display"] = True
    body["comparison_input"] = "frozen_capture_inventory; no consumption of future step output"
    body["unknown_catalog"] = [
        "session_established=null:补证",
        "空日志:缺证而非正常",
        "operstate=UNKNOWN:不能独立判故障",
        "仅本地网关10.45.0.1，不证明DN/应用送达",
        "instruction资料集合可用，不证明技术事实一致",
    ]
    return body


def generate_revision(method, task, context, bindings, client, **kwargs):
    def transform(body):
        root = kwargs["source_root"]
        scope = load_scope(root, task)
        body["identity_receipt"] = {
            "meaning": "normal version provenance; identity checks are future planned checks",
            "identity_source_admission_sha256": sha(root / "data/source-admission.json"),
            "parameters": {
                obj: identity_parameters(root, task, scope, obj) for obj in task.objects
            },
        }
        table = citation_table(
            selected_bindings(bindings), body["generation_capabilities"]["admissible_ids"]
        )
        by_id = {ref["evidence_id"]: key for key, ref in table.items()}
        body = revision_body(body)
        for row in body["evidence"]:
            row["citation_key"] = by_id.get(row["citation"]["evidence_id"])
        return body

    return generate_domain_plan(
        method,
        task,
        context,
        selected_bindings(bindings),
        client,
        **kwargs,
        schema_factory=revision_schema,
        registry_version=REGISTRY,
        action_registry=ACTIONS,
        instructions=INSTRUCTIONS,
        body_transform=transform,
        max_tokens=MAX_TOKENS,
        schema_catalog_factory=public_step_options,
    )


def public_step_options(schema):
    branches = schema["properties"]["steps"]["prefixItems"] + schema["$defs"]["PlanStep"]["anyOf"]
    return [
        {
            **{k: b["properties"][k]["const"] for k in ("step_id", "action_type", "target")},
            "fixed_parameters": {
                k: v["const"]
                for k, v in b["properties"]["parameters"].get("properties", {}).items()
                if "const" in v
            },
        }
        for b in branches
    ]


def revision_manifest():
    return head_manifest() | {
        "version": "v8-e1-expert-readonly-head-4",
        "profile": PROFILE,
        "registry_version": REGISTRY,
        "max_steps": MAX_STEPS,
        "max_tokens": MAX_TOKENS,
        "instructions_sha256": hashlib.sha256(INSTRUCTIONS.encode()).hexdigest(),
        "identity_prior": (
            "mandatory source-scoped identity anchors; investigation actions selected"
        ),
        "visible_manual_chunks_per_object": 1,
        "post_generation_repair": False,
        "step_id_encoding": "short aN aliases fixed before generation; identity IDs unchanged",
        "citation_encoding": "explicit raw citation_table; no external enrichment or output repair",
        "parameter_choice_catalog": (
            "public schema-derived short-ID/action/object/parameter choices"
        ),
        "capture_comparison_input": "frozen_capture_inventory",
        "incomplete_capture_exit": "explicit request_evidence, not proof of completeness",
        "budget": {"models": 8, "tools": 8, "rounds": 3, "seconds": 180},
    }
