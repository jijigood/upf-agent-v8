"""Independent negative controls for namespace permissions, source proof and candidate isolation."""

import base64
import json
import struct
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from upf_agent.v8.compiler import compile_contract
from upf_agent.v8.e1_dataset import sha, write
from upf_agent.v8.e1_domain_head import domain_schema
from upf_agent.v8.e1_domain_readonly import (
    SCOPE_VERSION,
    DomainEvidenceTools,
    DomainPlanIR,
    DomainScope,
    NamespaceScope,
    capture_inventory,
    domain_score,
    extract_normal_fields,
    field_gap,
    load_scope,
    translate_domain_plan,
    validate_domain_plan,
)
from upf_agent.v8.experiment_metrics import MetricCollector
from upf_agent.v8.models import (
    EvaluationContext,
    ObjectProfile,
    OrchestrationTask,
    PermissionScope,
    digest,
)
from upf_agent.v8.plan_generator import PlanBudget
from upf_agent.v8.plan_ir import PlanStep
from upf_agent.v8.plan_translator import translate_plan
from upf_agent.v8.plan_validator import validate_plan


def fixture(root, *, approved=False, filters=False, dual_capture=None):
    at = datetime(2026, 10, 11, tzinfo=UTC)

    def interface(name):
        return {
            "returncode": 0,
            "stdout": json.dumps(
                [
                    {
                        "ifname": name,
                        "flags": ["UP"],
                        "mtu": 1400,
                        "operstate": "UNKNOWN",
                        "addr_info": [],
                    }
                ]
            ),
        }

    packet = struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
    packet += struct.pack("<IIII", int(at.timestamp()), 0, 4, 4) + b"test"
    raw = {
        "core": {
            "interfaces": interface("ogstun"),
            "logs_and_config": {"upf.log": "", "gnb.log": ""},
        },
        "ue": {"interfaces": interface("uesimtun0"), "logs_and_config": {"ue.log": ""}},
        "normal_probe": {
            "argv": ["ping", "-n", "-I", "uesimtun0"],
            "returncode": 1,
            "stdout": "timeout",
        },
        "packet_capture": {
            "capture_base64": base64.b64encode(packet).decode(),
            "capture_position": "core any",
        },
        "window_start": (at - timedelta(seconds=1)).isoformat(),
        "window_end": (at + timedelta(seconds=1)).isoformat(),
    }
    if filters:
        raw["core"]["filter_inventory"] = {
            "INPUT": {"argv": ["iptables", "-nvxL", "INPUT"], "returncode": 0, "stdout": "no rule"}
        }
    if dual_capture is not None:
        ue_packet = packet
        if dual_capture != "same_bytes":
            second = struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
            fraction = 500000 if dual_capture == "nonoverlap" else 0
            original = 8 if dual_capture == "truncated" else 4
            second += struct.pack("<IIII", int(at.timestamp()), fraction, 4, original) + b"ue!!"
            ue_packet = second
        raw["ue_packet_capture"] = {
            "capture_base64": base64.b64encode(ue_packet).decode(),
            "capture_position": "independent ue any",
        }
    path = root / "data/raw/snapshot.json"
    write(path, raw)
    common = ["event_type", "log_excerpt", "domain_namespace"]
    scope = DomainScope(
        raw_sha256=sha(path),
        objects={
            "upf": NamespaceScope(
                namespace="core",
                devices=["ogstun"],
                captures=["core-any"],
                readable_fields=common + ["tun_inventory", "filter_inventory", "packet_inventory"],
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
    task = OrchestrationTask(
        question="unit control, no expert or model result",
        template="log_observation",
        objects=list(scope.objects),
        product="Open5GS",
        version="2.7.6",
        synthetic=True,
        as_of=at + timedelta(seconds=2),
        object_profiles={
            "upf": ObjectProfile(role="upf", product="Open5GS", version="2.7.6"),
            "ran": ObjectProfile(role="ran", product="UERANSIM", version="3.2.7"),
            "ue": ObjectProfile(role="unspecified", product="UERANSIM", version="3.2.7"),
        },
        permission=PermissionScope(
            objects=list(scope.objects),
            readable_fields=sorted({f for s in scope.objects.values() for f in s.readable_fields}),
            revision=f"{SCOPE_VERSION}:{digest(scope)}",
        ),
        observation_files=["data/domain-observations.json"],
    )
    values = extract_normal_fields(root, scope)
    write(
        root / task.observation_files[0],
        {
            "source_id": "synthetic-unit-control",
            "synthetic": True,
            "corroborated": approved,
            "observations": [
                {
                    "category": "R",
                    "object_id": obj,
                    "fields": values[obj],
                    "product": task.object_profiles[obj].product,
                    "version": task.object_profiles[obj].version,
                    "observed": {
                        "start": raw["window_start"],
                        "end": raw["window_end"],
                        "timezone_source": "unit",
                    },
                }
                for obj in task.objects
            ],
        },
    )
    contract = compile_contract(task)
    collector = MetricCollector(task.run_id)
    tools = DomainEvidenceTools(root, task, contract, PlanBudget(task, collector))
    context = EvaluationContext.from_task(task, contract, "unit-domain")
    return task, contract, context, tools, collector


def plan_for(task, context, params, refs=(), action="READ_TUN_INTERFACE", target="upf"):
    steps = [
        PlanStep(step_id="id1", action_type="CHECK_IDENTITY", target="upf", text="核对UPF身份"),
        PlanStep(step_id="id3", action_type="CHECK_IDENTITY", target="ue", text="核对UE身份"),
    ]
    steps.append(
        PlanStep(
            step_id="check",
            action_type=action,
            target=target,
            text="取得授权资料后检查",
            parameters=params,
            depends_on=["id1"] if target == "upf" else ["id3"],
            evidence=list(refs),
        )
    )
    return DomainPlanIR(
        context_fingerprint=context.fingerprint,
        scope_fingerprint=digest(task.permission),
        batch_id=context.batch_id,
        evaluation_as_of=context.as_of,
        target_objects=task.objects,
        steps=steps,
        stop_conditions=["缺证时停止"],
        goal_achieved=False,
    )


def reference(b):
    return {
        "evidence_id": b.evidence_id,
        "revision": b.revision,
        "source_sha256": b.source.sha256,
        "locator": b.source.locator,
    }


def test_candidate_registry_cannot_enter_default_translator_or_validator(tmp_path):
    task, contract, context, tools, _ = fixture(tmp_path)
    plan = plan_for(
        task,
        context,
        {
            "namespace": "core",
            "device": "ogstun",
            "basis": "collect_then_check",
            "pending": [field_gap("upf", "tun_inventory", "ogstun")],
        },
    )
    raw = plan.model_dump_json()
    assert translate_plan(raw).plan is None
    assert translate_domain_plan(raw).plan == plan
    assert validate_domain_plan(
        plan, list(tools.bindings.values()), task, contract, context, tmp_path
    ).raw_plan_validity
    old = validate_plan(plan, list(tools.bindings.values()), task, contract, context, tmp_path)
    assert not old.raw_plan_validity and "unknown_action" in [i.code for i in old.issues]


@pytest.mark.parametrize(
    "mutation,expected",
    [
        ("namespace", "domain_namespace_denied"),
        ("device", "domain_device_denied"),
        ("dependency", "domain_identity_dependency_missing"),
        ("pending", "domain_pending_gap_mismatch"),
        ("write", "execution_claim_or_write"),
    ],
)
def test_independent_domain_gates_reject_invalid_future_checks(tmp_path, mutation, expected):
    task, contract, context, tools, _ = fixture(tmp_path)
    plan = plan_for(
        task,
        context,
        {
            "namespace": "core",
            "device": "ogstun",
            "basis": "collect_then_check",
            "pending": [field_gap("upf", "tun_inventory", "ogstun")],
        },
    )
    s = plan.steps[-1]
    if mutation == "namespace":
        s.parameters["namespace"] = "ue"
    if mutation == "device":
        s.parameters["device"] = "uesimtun0"
    if mutation == "dependency":
        s.depends_on = []
    if mutation == "pending":
        s.parameters["pending"] = ["invented unrelated gap"]
    if mutation == "write":
        s.effect_kind = "network_write"
    result = validate_domain_plan(
        plan, list(tools.bindings.values()), task, contract, context, tmp_path
    )
    assert not result.raw_plan_validity and expected in [i.code for i in result.issues]


def test_existing_basis_requires_approved_raw_matching_field_and_selector(tmp_path):
    task, contract, context, tools, _ = fixture(tmp_path, approved=True, filters=True)
    b = next(b for b in tools.bindings.values() if b.object_id == "upf")
    plan = plan_for(
        task,
        context,
        {"namespace": "core", "device": "ogstun", "basis": "inspect_existing", "pending": []},
        [reference(b)],
    )
    assert validate_domain_plan(
        plan, list(tools.bindings.values()), task, contract, context, tmp_path
    ).raw_plan_validity
    no_cite = plan.model_copy(deep=True)
    no_cite.steps[-1].evidence = []
    assert not validate_domain_plan(
        no_cite, list(tools.bindings.values()), task, contract, context, tmp_path
    ).raw_plan_validity
    absent = plan_for(
        task,
        context,
        {"namespace": "core", "chain": "FORWARD", "basis": "inspect_existing", "pending": []},
        [reference(b)],
        action="READ_FILTER_COUNTERS",
    )
    result = validate_domain_plan(
        absent, list(tools.bindings.values()), task, contract, context, tmp_path
    )
    assert not result.raw_plan_validity and "domain_existing_basis_incomplete" in [
        i.code for i in result.issues
    ]


def test_unapproved_binding_cannot_become_existing_evidence(tmp_path):
    task, contract, context, tools, _ = fixture(tmp_path)
    b = next(b for b in tools.bindings.values() if b.object_id == "upf")
    plan = plan_for(
        task,
        context,
        {"namespace": "core", "device": "ogstun", "basis": "inspect_existing", "pending": []},
        [reference(b)],
    )
    result = validate_domain_plan(
        plan, list(tools.bindings.values()), task, contract, context, tmp_path
    )
    assert {"unverified_source", "domain_existing_basis_incomplete"} <= {
        i.code for i in result.issues
    }
    assert not result.raw_plan_validity


def test_scope_hash_and_raw_capture_tamper_are_rejected(tmp_path):
    task, _, _, _, _ = fixture(tmp_path)
    path = tmp_path / "data/domain-scope.json"
    d = json.loads(path.read_text())
    d["objects"]["ue"]["namespace"] = "core"
    write(path, d)
    with pytest.raises(ValueError, match="scope|permission revision"):
        load_scope(tmp_path, task)
    task, _, _, _, _ = fixture(tmp_path / "second")
    raw = tmp_path / "second/data/raw/snapshot.json"
    raw.write_text(raw.read_text() + " ")
    with pytest.raises(ValueError, match="capture hash"):
        load_scope(tmp_path / "second", task)


def test_tool_counts_real_reads_and_does_not_open_private_filter_material(tmp_path):
    task, _, _, tools, collector = fixture(tmp_path)
    write(
        tmp_path / "private/external-verification.json",
        {"input": {"stdout": "injected secret cause"}},
    )
    scope = load_scope(tmp_path, task)
    fields = extract_normal_fields(tmp_path, scope)
    assert "filter_inventory" not in fields["upf"] and "packet_inventory" not in fields["ue"]
    assert not any(
        k in fields["ran"] for k in ["tun_inventory", "session_probe_inventory", "packet_inventory"]
    )
    assert collector.summary()["invocations"]["tool"]["attempted"] == 2
    denied = tools.read_domain_snapshot({"object_id": "ran", "fields": ["tun_inventory"]})
    assert denied.error_code == "scope_denied"
    assert collector.summary()["invocations"]["tool"]["attempted"] == 3
    invalid = tools.read_domain_snapshot(
        {"object_id": "upf", "fields": ["tun_inventory"], "command": "iptables -F INPUT"}
    )
    assert invalid.error_code == "invalid_arguments"


def test_single_capture_cannot_support_existing_bilateral_comparison(tmp_path):
    task, contract, context, tools, _ = fixture(tmp_path, approved=True)
    b = next(b for b in tools.bindings.values() if b.object_id == "upf")
    plan = plan_for(
        task,
        context,
        {
            "namespace": "core",
            "capture_id": "core-any",
            "peer_object_id": "ue",
            "peer_capture_id": "ue-any",
            "basis": "inspect_existing",
            "pending": [],
        },
        [reference(b)],
        action="COMPARE_CAPTURE_WINDOWS",
    )
    plan.steps[-1].depends_on = ["id1", "id3"]
    result = validate_domain_plan(
        plan, list(tools.bindings.values()), task, contract, context, tmp_path
    )
    assert not result.raw_plan_validity and "domain_existing_basis_incomplete" in [
        i.code for i in result.issues
    ]


def test_schema_expresses_namespaced_future_reads_without_reference_or_slot_coverage(tmp_path):
    task, _, context, tools, _ = fixture(tmp_path)
    schema, caps, _, _ = domain_schema(task, context, list(tools.bindings.values()), tmp_path)
    assert caps["admissible_ids"] == []
    assert (
        "prefixItems" not in schema["properties"]["steps"]
        and schema["properties"]["steps"]["maxItems"] == 12
    )
    actions = {
        b["properties"]["action_type"]["const"] for b in schema["$defs"]["PlanStep"]["anyOf"]
    }
    assert {
        "READ_TUN_INTERFACE",
        "READ_FILTER_COUNTERS",
        "READ_SESSION_PROBE",
        "READ_PACKET_CAPTURE",
        "COMPARE_CAPTURE_WINDOWS",
    } <= actions
    for b in schema["$defs"]["PlanStep"]["anyOf"]:
        if b["properties"]["action_type"]["const"].startswith(
            ("READ_TUN", "READ_FILTER", "READ_SESSION", "READ_PACKET", "COMPARE_CAPTURE")
        ):
            assert b["properties"]["parameters"]["properties"]["basis"] == {
                "const": "collect_then_check"
            }
            assert b["properties"]["evidence"]["maxItems"] == 0


def test_corrupt_pcap_and_missing_reference_keep_failure_and_unknown_metrics(tmp_path):
    with pytest.raises(ValueError, match="classic pcap"):
        capture_inventory(
            {"capture_base64": base64.b64encode(b"incomplete").decode()}, "core", "core-any"
        )
    task, contract, context, tools, _ = fixture(tmp_path)
    validation = validate_domain_plan(
        None, list(tools.bindings.values()), task, contract, context, tmp_path
    )
    score = domain_score(None, validation, SimpleNamespace(case_id="unit-only"))
    assert score["reference_pass"] is None and score["vpr"] is None and score["solvability"] is None
    assert not score["validator_pass"] and score["issues"] == ["parse_failure"]


def test_self_consistent_forged_projection_does_not_override_pinned_raw_capture(tmp_path):
    task, contract, context, tools, _ = fixture(tmp_path, approved=True)
    b = next(b for b in tools.bindings.values() if b.object_id == "upf").model_copy(deep=True)
    path = tmp_path / task.observation_files[0]
    doc = json.loads(path.read_text())
    doc["observations"][0]["fields"]["tun_inventory"][0]["mtu"] = 9999
    write(path, doc)
    b.fields = doc["observations"][0]["fields"]
    b.source.sha256 = sha(path)
    plan = plan_for(
        task,
        context,
        {"namespace": "core", "device": "ogstun", "basis": "inspect_existing", "pending": []},
        [reference(b)],
    )
    result = validate_domain_plan(plan, [b], task, contract, context, tmp_path)
    assert not result.raw_plan_validity
    assert "domain_raw_projection_mismatch" in {i.code for i in result.issues}
    _, caps, _, _ = domain_schema(task, context, [b], tmp_path)
    assert b.evidence_id not in caps["admissible_ids"]
    assert "normal_projection_mismatch" in caps["rejected"][b.evidence_id]


def test_all_action_branches_select_semantic_action_before_identifier(tmp_path):
    task, _, context, tools, _ = fixture(tmp_path)
    schema, _, _, _ = domain_schema(task, context, list(tools.bindings.values()), tmp_path)
    # The actual compact decoder follows property order, although JSON Schema
    # itself is unordered. Different first keys silently exclude other actions.
    for branch in schema["$defs"]["PlanStep"]["anyOf"]:
        assert list(branch["properties"])[:4] == ["action_type", "target", "step_id", "text"]


@pytest.mark.parametrize(
    "capture_mode,expected_issue",
    [
        ("independent", None),
        ("same_bytes", "independent_capture_sources_missing"),
        ("nonoverlap", "capture_windows_do_not_overlap"),
        ("truncated", "capture_empty_or_truncated"),
    ],
)
def test_capture_comparison_checks_independence_time_and_completeness_only(
    tmp_path, capture_mode, expected_issue
):
    task, contract, context, tools, _ = fixture(tmp_path, approved=True, dual_capture=capture_mode)
    rows = list(tools.bindings.values())
    refs = [reference(next(b for b in rows if b.object_id == obj)) for obj in ("upf", "ue")]
    plan = plan_for(
        task,
        context,
        {
            "namespace": "core",
            "capture_id": "core-any",
            "peer_object_id": "ue",
            "peer_capture_id": "ue-any",
            "basis": "inspect_existing",
            "pending": [],
        },
        refs,
        action="COMPARE_CAPTURE_WINDOWS",
    )
    plan.steps[-1].depends_on = ["id1", "id3"]
    result = validate_domain_plan(plan, rows, task, contract, context, tmp_path)
    if expected_issue is None:
        assert result.raw_plan_validity
        assert all(
            not b.fields["packet_inventory"]["packet_matching_or_delivery_proved"] for b in rows
        )
    else:
        assert not result.raw_plan_validity and expected_issue in {i.code for i in result.issues}


def test_failed_filter_read_is_a_gap_even_with_valid_raw_provenance(tmp_path):
    task, contract, context, _, _ = fixture(tmp_path, approved=True, filters=True)
    raw_path = tmp_path / "data/raw/snapshot.json"
    raw = json.loads(raw_path.read_text())
    raw["core"]["filter_inventory"]["INPUT"].update(returncode=1, stdout="", stderr="read denied")
    write(raw_path, raw)
    scope_path = tmp_path / "data/domain-scope.json"
    scope = DomainScope.model_validate_json(scope_path.read_text())
    scope.raw_sha256 = sha(raw_path)
    write(scope_path, scope.model_dump(mode="json"))
    task.permission.revision = f"{SCOPE_VERSION}:{digest(scope)}"
    source = json.loads((tmp_path / task.observation_files[0]).read_text())
    fields = extract_normal_fields(tmp_path, scope)
    source["raw_sources"] = {scope.raw_path: scope.raw_sha256}
    for row in source["observations"]:
        row["fields"] = fields[row["object_id"]]
    write(tmp_path / task.observation_files[0], source)
    contract = compile_contract(task)
    context = EvaluationContext.from_task(task, contract, "unit-failed-filter")
    tools = DomainEvidenceTools(
        tmp_path, task, contract, PlanBudget(task, MetricCollector(task.run_id))
    )
    bindings = list(tools.bindings.values())
    b = next(b for b in bindings if b.object_id == "upf")
    plan = plan_for(
        task,
        context,
        {"namespace": "core", "chain": "INPUT", "basis": "inspect_existing", "pending": []},
        [reference(b)],
        action="READ_FILTER_COUNTERS",
    )
    result = validate_domain_plan(plan, bindings, task, contract, context, tmp_path)
    assert not result.raw_plan_validity
    assert "domain_existing_basis_incomplete" in {i.code for i in result.issues}
    schema, _, _, _ = domain_schema(task, context, bindings, tmp_path)
    branch = next(
        b
        for b in schema["$defs"]["PlanStep"]["anyOf"]
        if b["properties"]["action_type"]["const"] == "READ_FILTER_COUNTERS"
        and b["properties"]["parameters"]["properties"]["chain"]["const"] == "INPUT"
    )
    assert branch["properties"]["parameters"]["properties"]["basis"] == {
        "const": "collect_then_check"
    }
