"""Explicit candidate profile shared by engineering and guarded formal entry."""

import hashlib
import json
import subprocess

import httpx

from upf_agent.models import LocalModelError
from upf_agent.v8.e1_domain_head import INSTRUCTIONS, generate_domain_plan, manifest
from upf_agent.v8.e1_source_closure import POLICY
from upf_agent.v8.p5_plan_runner import run_p5
from upf_agent.v8.plan_generator import ObservedPlanClient

PROFILE = "verified-runtime-candidate-1"
HEAD_INSTRUCTIONS = INSTRUCTIONS + (
    "本版来源准入是正常采集与原文投影的机器核验，不是专家因果批准。"
    "packet_inventory.plain_icmp只记录普通IPv4 ICMP报文的方向、标识、序号和载荷哈希；"
    "未解码GTP/PFCP、IPv6或分片；未见报文不等于丢包，报文对应不等于应用送达。"
    "手册是版本范围内的原文参考，示例配置不是本案例实际配置。"
    "选择足以调查所问故障的步骤；完整性未知时明确补证。"
)


def head_manifest():
    return manifest() | {
        "version": "v8-e1-verified-runtime-head-candidate-3",
        "instructions_sha256": hashlib.sha256(HEAD_INSTRUCTIONS.encode()).hexdigest(),
        "template": "runtime_investigation",
        "reference_scoring": "unreviewed draft match or separately approved reference",
        "shared_domain_preparation_reads": 0,
        "manual_chunks_per_object_per_query": 2,
        "source_policy": POLICY,
        "context_catalog": "parameter names; constraints stay in the actual decoding grammar",
        "context_document_deduplication": "same object/source SHA/locator only",
        "visible_manual_chunks_per_object": 3,
        "native_p5_scope": "explicit object profiles; no legacy single-product filter",
        "evidence_display": (
            "original fields/citation plus applicable scope; duplicate metadata omitted"
        ),
    }


def run_verified_p5(root, task, tools, client):
    # Both products remain in the backend's explicit object_profiles and the tools
    # enforce those profiles. Legacy AgentTask's scalar product cannot encode them.
    return run_p5(root, task, tools, client, profile_scoped=True)


def compact_body(body):
    body = dict(body)
    body["action_registry"] = {
        name: {
            "parameter_names": list(spec["parameters"].get("properties", {})),
            "permission_kind": spec["permission_kind"],
            "effect_kind": spec["effect_kind"],
        }
        for name, spec in body["action_registry"].items()
    }
    unique, seen, per_object = [], set(), {}
    for row in body["evidence"]:
        citation = row["citation"]
        key = (
            row.get("object_id"),
            row.get("category"),
            citation["source_sha256"],
            citation["locator"],
        )
        if key not in seen:
            if row["category"] == "K":
                obj = row["object_id"]
                if per_object.get(obj, 0) >= 3:
                    continue
                per_object[obj] = per_object.get(obj, 0) + 1
            display = {
                k: row[k]
                for k in (
                    "object_id",
                    "category",
                    "fields",
                    "citation",
                    "observed",
                    "valid",
                    "product",
                    "version",
                    "purposes",
                    "readable",
                    "source_verified",
                    "synthetic",
                    "corroborated",
                    "deleted",
                )
                if k in row
            }
            display["source_id"] = row["source"]["source_id"]
            display["knowledge_applicability"] = {
                k: row["knowledge_applicability"][k]
                for k in ("status", "purposes", "reviewed")
                if k in (row.get("knowledge_applicability") or {})
            }
            unique.append(display)
            seen.add(key)
    body["evidence"] = unique
    method_context = dict(body.get("method_context", {}))
    if "states" in method_context:
        method_context["states"] = {
            rid: {
                "code": state["code"],
                "reasons": state["reasons"],
                "supporting_count": len(state.get("supporting", [])),
            }
            for rid, state in method_context["states"].items()
        }
    body["method_context"] = method_context
    body["shared_domain_preparation"] = (
        "no forced domain reads; actual native tool reads are charged"
    )
    body["capture_limit"] = (
        "two independent namespace captures; bounded plain IPv4 ICMP inventory only; "
        "packet correspondence does not prove loss, application delivery or cause"
    )
    body["context_catalog_note"] = "完整约束保留在实际Schema/grammar；未改变证据字段或引用原文。"
    return body


def generate_verified_plan(method, task, context, bindings, client, **kwargs):
    # A common display budget applies to all methods, including graph-added material.
    # Keep real retrieval/cost receipts; constrain the actual schema to visible citations.
    selected, seen, count = [], set(), {}
    for binding in bindings:
        key = (binding.object_id, binding.category, binding.source.sha256, binding.source.locator)
        if key in seen:
            continue
        if binding.category == "K":
            if count.get(binding.object_id, 0) >= 3:
                continue
            count[binding.object_id] = count.get(binding.object_id, 0) + 1
        selected.append(binding)
        seen.add(key)
    return generate_domain_plan(
        method,
        task,
        context,
        selected,
        client,
        **kwargs,
        instructions=HEAD_INSTRUCTIONS,
        body_transform=compact_body,
    )


class VerifiedPlanClient(ObservedPlanClient):
    def __init__(self, *args, grammar_python, **kwargs):
        super().__init__(*args, **kwargs)
        self.grammar_python = grammar_python
        self.client.close()
        self.client = httpx.Client(timeout=180, trust_env=False)

    def compile_candidate_schema(self, schema):
        script = (
            "import sys,xgrammar; print(str(xgrammar.Grammar.from_json_schema("
            "sys.stdin.read(),any_whitespace=False,separators=(',',':'))))"
        )
        try:
            result = subprocess.run(
                [self.grammar_python, "-c", script],
                input=json.dumps(schema),
                text=True,
                capture_output=True,
                timeout=max(0.001, self.budget.remaining()),
                check=True,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            raise LocalModelError(f"candidate grammar compilation failed: {exc}") from exc
        return result.stdout.strip()
