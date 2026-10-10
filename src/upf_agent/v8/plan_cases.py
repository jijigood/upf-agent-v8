"""Synthetic cases and unreviewed reference branches frozen before model outputs."""

import hashlib
import json
from datetime import timedelta
from pathlib import Path

from upf_agent.v8.builders import task_graph
from upf_agent.v8.fixtures import example
from upf_agent.v8.graph import GraphEdge, GraphNode, MemoryGraphStore
from upf_agent.v8.knowledge_applicability import KnowledgeAnnotation, KnowledgeRegistry
from upf_agent.v8.models import ObjectProfile, SourcePointer, digest
from upf_agent.v8.phase1 import write_json
from upf_agent.v8.plan_ir import ActionPattern, CaseGold, GoldBranch
from upf_agent.v8.reference_revision import revise_peer_mapping

SPECS = [
    ("upf_n4_fault", "normal"),
    ("upf_n4_fault", "disabled"),
    ("upf_n4_fault", "down"),
    ("upf_n4_fault", "conflict"),
    ("upf_n4_fault", "unknown_purpose"),
    ("upf_n4_fault", "wrong_version"),
    ("upf_n4_fault", "missing_runtime"),
    ("upf_n4_fault", "missing_pair"),
    ("upf_n3_fault", "normal"),
    ("upf_n3_fault", "small_mtu"),
    ("upf_n3_fault", "down"),
    ("upf_n3_fault", "unknown_purpose"),
    ("manual_operation", "normal"),
    ("manual_operation", "wrong_version"),
    ("manual_operation", "unknown_purpose"),
    ("manual_operation", "missing_knowledge"),
    ("upf_n4_fault", "unknown_version"),
    ("upf_n4_fault", "missing_window"),
    ("upf_n4_fault", "stale"),
    ("upf_n4_fault", "field_denied"),
    ("upf_n4_fault", "peer_conflict"),
    ("upf_n3_fault", "missing_pair"),
    ("upf_n4_fault", "mapping_conflict"),
    ("upf_n3_fault", "pair_config_conflict"),
]


def prepare_case(root: Path, index: int):
    if root.exists():
        raise ValueError("case root exists")
    root.mkdir(parents=True)
    template, mutation = SPECS[index]
    case_id = f"pilot-{index + 1:02d}"
    task = example(root, name=case_id, template=template)
    peer = "RAN-B" if template == "upf_n3_fault" else "SMF-B"
    if peer != "SMF-B":
        task.objects = ["UPF-A", peer]
        task.permission.objects = task.objects
        task.path.positions[1].object_id = peer
    task.object_profiles = {
        "UPF-A": ObjectProfile(role="upf", product="UPF", version="5.0"),
        peer: ObjectProfile(
            role="ran" if template == "upf_n3_fault" else "smf",
            product="SyntheticRAN" if template == "upf_n3_fault" else "SyntheticSMF",
            version="dev-1",
        ),
    }
    task.run_id = digest([case_id, "phase2-role-aware-dev-2"])[:32]
    task.retrieval_device = "cpu"
    task.model_enabled = False
    relative = task.observation_files[0]
    body = json.loads((root / relative).read_text())
    body["path"]["objects"] = task.objects
    for row in body["observations"]:
        if row["object_id"] == "SMF-B":
            row["object_id"] = peer
        profile = task.object_profiles[row["object_id"]]
        row["product"], row["version"] = profile.product, profile.version
        if row["category"] == "K":
            row["fields"]["instruction"] = (
                f"合成{profile.role}对象专用只读规程：检查声明接口配置和状态；"
                "仅用于本开发fixture，不是厂商操作手册"
            )
    runtime = next(r for r in body["observations"] if r["category"] == "R")
    pair = next(r for r in body["observations"] if r["category"] == "P")
    if mutation == "disabled":
        runtime["fields"]["n4_enabled"] = False
    if mutation == "down":
        runtime["fields"]["state"] = "down"
    if mutation == "small_mtu":
        runtime["fields"]["mtu"] = 576
    if mutation == "conflict":
        other = json.loads(json.dumps(runtime))
        other["fields"]["n4_enabled"] = False
        body["observations"].append(other)
    if mutation == "wrong_version":
        for row in body["observations"]:
            row["version"] = "4.0"
    if mutation == "unknown_version":
        for row in body["observations"]:
            row["version"] = None
    if mutation == "missing_window":
        for row in body["observations"]:
            if row["category"] in {"R", "P"}:
                row.pop("observed", None)
    if mutation == "stale":
        for row in body["observations"]:
            if row["category"] in {"R", "P"}:
                row["observed"]["end"] = (task.as_of - timedelta(hours=1)).isoformat()
                row["observed"]["start"] = (task.as_of - timedelta(hours=2)).isoformat()
    if mutation == "field_denied":
        task.permission.readable_fields.remove("n4_enabled")
    if mutation in {"missing_runtime", "missing_pair", "missing_knowledge"}:
        kind = {"missing_runtime": "R", "missing_pair": "P", "missing_knowledge": "K"}[mutation]
        body["observations"] = [
            r for r in body["observations"] if r["category"] != kind or r["object_id"] != "UPF-A"
        ]
    if mutation == "peer_conflict":
        pair["fields"]["peer_endpoint"] = "192.0.2.99"
    if mutation == "mapping_conflict":
        pair["fields"]["mapping_version"] = "map-other"
    if mutation == "pair_config_conflict":
        pair["config_version"] = "cfg-other"
    # Every case is a development scenario, with shared fixture families explicitly recorded.
    investigation = (
        "先核对身份，再查阅适用手册并检查手册指定配置；本任务不要求双侧映射调查；"
        if template == "manual_operation"
        else "先核对身份，再调查声明接口/配置及双侧映射；"
    )
    task.question = (
        f"合成开发案例{case_id}：{template}。为UPF-A与{peer}给出只读调查方案，"
        f"{investigation}缺少适用证据时补证或转人工，"
        "不得声称根因已确定或任何网络变更已执行。"
    )
    write_json(root / relative, body)
    sha = hashlib.sha256((root / relative).read_bytes()).hexdigest()
    task.path.source_sha256 = sha
    annotations = []
    store = MemoryGraphStore()
    nodes, edges = task_graph(task, [])
    for idx, row in enumerate(body["observations"]):
        if row["category"] != "K":
            continue
        text = row["fields"]["instruction"]
        source = SourcePointer(
            source_id=body["source_id"],
            sha256=sha,
            locator=f"/observations/{idx}",
            relative_path=relative,
        )
        if mutation != "unknown_purpose" and row.get("version"):
            annotations.append(
                KnowledgeAnnotation(
                    annotation_id=f"{case_id}-k-{idx}",
                    source_sha256=sha,
                    locator=source.locator,
                    content_sha256=hashlib.sha256(text.encode()).hexdigest(),
                    product=row["product"],
                    version=row["version"],
                    object_ids=[row["object_id"]],
                    purposes=[template],
                    basis_kind="trusted_rule",
                    basis_source="explicit synthetic fixture specification",
                    basis_version="1",
                    rule_id="synthetic-purpose-exact-match-1",
                    reviewed=False,
                )
            )
        node_id = f"{case_id}-document-{idx}"
        nodes.append(
            GraphNode(
                node_id=node_id,
                kind="DocumentBlock",
                layer="knowledge",
                source=source,
                object_ids=[row["object_id"]],
                version=row.get("version"),
                synthetic=True,
                attributes={"text": text, "product": row["product"]},
            )
        )
        edges.append(
            GraphEdge(
                edge_id=f"{node_id}-object",
                source_id=f"object:{row['object_id']}",
                target_id=node_id,
                relation="DESCRIBES",
                source=source,
                synthetic=True,
            )
        )
    registry = KnowledgeRegistry(version=f"{case_id}-registry-1", annotations=annotations)
    write_json(root / "data/v8/knowledge_applicability.json", registry.model_dump(mode="json"))
    store.build(nodes, edges)
    write_json(root / "data/v8/manual_graph.json", store.snapshot())
    unknown = mutation in {
        "unknown_purpose",
        "wrong_version",
        "missing_runtime",
        "missing_pair",
        "missing_knowledge",
        "unknown_version",
        "missing_window",
        "stale",
        "field_denied",
        "conflict",
        "peer_conflict",
        "mapping_conflict",
        "pair_config_conflict",
    }
    required = []
    for obj in task.objects:
        suffix = digest(obj)[:8]
        identity = f"id-{suffix}"
        required.append(
            ActionPattern(pattern_id=identity, action_type="CHECK_IDENTITY", target=obj)
        )
        if template != "manual_operation":
            required.append(
                ActionPattern(
                    pattern_id=f"interface-{suffix}",
                    action_type="CHECK_INTERFACE",
                    target=obj,
                    parameters={"interface": "N3" if template == "upf_n3_fault" else "N4"},
                    depends_on=[identity],
                )
            )
        knowledge_available = mutation not in {
            "unknown_purpose",
            "wrong_version",
            "unknown_version",
        }
        knowledge_available &= not (mutation == "missing_knowledge" and obj == "UPF-A")
        field = "mtu" if template == "upf_n3_fault" else "n4_enabled"
        if knowledge_available and field in task.permission.readable_fields:
            required.append(
                ActionPattern(
                    pattern_id=f"config-{suffix}",
                    action_type="CHECK_CONFIGURATION",
                    target=obj,
                    parameters={"field": field},
                    depends_on=[identity],
                )
            )
    branches = [GoldBranch(branch_id="read-only-investigation", required=required)]
    if unknown:
        required.append(
            ActionPattern(pattern_id="gap", action_type="REQUEST_EVIDENCE", target="UPF-A")
        )
        branches[0] = GoldBranch(branch_id="investigate-and-request", required=required)
        branches.append(
            GoldBranch(
                branch_id="review",
                required=[p.model_copy(deep=True) for p in required if p.pattern_id != "gap"]
                + [ActionPattern(pattern_id="review", action_type="HUMAN_REVIEW", target="UPF-A")],
            )
        )
    # References derive from the case specification before model outputs, never Contract states.
    gold = CaseGold(
        case_id=case_id,
        source_group=case_id,
        structure_family="example-v8-role-aware-2",
        source_level="D1",
        synthetic=True,
        reviewed=False,
        solvability="needs_evidence" if unknown else "solvable",
        objects=task.objects,
        version=task.version,
        as_of=task.as_of,
        permission_fingerprint=digest(task.permission),
        visible_evidence=[f"/observations/{i}" for i in range(len(body["observations"]))],
        source_hashes={relative: sha},
        any_of=branches,
        stop_conditions=[
            "unknown evidence: stop or request evidence",
            "no automatic network write",
        ],
    )
    gold = revise_peer_mapping(task, gold)
    write_json(root / "case-task.json", task.model_dump(mode="json"))
    write_json(root / "case-reference.json", gold.model_dump(mode="json"))
    write_json(
        root / "case-spec.json",
        {
            "case_id": case_id,
            "template": template,
            "mutation": mutation,
            "calibration_candidate": index < 10,
            "fixture_generator_family": "example-v8-role-aware-2",
            "input_revision": "review-remediation-20261010-1",
            "object_profiles": {
                k: v.model_dump(mode="json") for k, v in task.object_profiles.items()
            },
            "synthetic": True,
            "reviewed": False,
            "independent_fault_count_claim": False,
        },
    )
    return task, gold
