"""Generation-time admissibility, derived from visible sources, never reference answers.

This compiler is a shared generation prior, not an evaluator. The offline Validator
rechecks the untouched output and physical sources independently.
"""

from upf_agent.v8.compiler import compile_contract, permitted
from upf_agent.v8.knowledge_applicability import annotate_knowledge
from upf_agent.v8.models import canonical, object_product_version
from upf_agent.v8.peer_mapping import pair_gaps
from upf_agent.v8.plan_source_verifier import verify_plan_source

VERSION = "v8-plan-capabilities-2"


def compile_capabilities(task, context, bindings, root):
    admissible, rejected = [], {}
    contract_id = compile_contract(task).contract_id
    for original in bindings:
        b = original.model_copy(deep=True)
        reasons = []
        if b.deleted or b.task_id != task.run_id or b.contract_id != contract_id:
            reasons.append("deleted_or_cross_task")
        if not verify_plan_source(root, b, task) or not b.corroborated:
            reasons.append("source_unverified")
        if not b.readable or not permitted(task, b.object_id, list(b.fields)):
            reasons.append("permission_denied")
        if b.synthetic and not task.synthetic:
            reasons.append("synthetic_source")
        expected_product, expected_version = object_product_version(task, b.object_id)
        if not b.version or b.version != expected_version:
            reasons.append("version_unknown_or_mismatched")
        if b.valid and not b.valid.start <= context.as_of < b.valid.end:
            reasons.append("outside_validity")
        if b.category in {"R", "P"}:
            if not b.observed or b.observed.end > context.as_of:
                reasons.append("observation_window_unknown_or_future")
            elif (context.as_of - b.observed.end).total_seconds() > 300:
                reasons.append("stale_observation")
        if b.category == "K":
            # Re-read the registered mapping, including revocation; a cached receipt is not trust.
            annotate_knowledge(root, b)
            if b.product != expected_product or task.template not in b.purposes:
                reasons.append("knowledge_applicability_unknown")
        if reasons:
            rejected[b.evidence_id] = reasons
        else:
            admissible.append(b)

    fault = task.template in {"upf_n3_fault", "upf_n4_fault"}
    field = "mtu" if task.template == "upf_n3_fault" else "n4_enabled"
    required_kinds = ["K", "R", "P"] if fault else ["R"]
    if task.template == "runtime_investigation":
        required_kinds = ["K", "R"]
    if task.template == "manual_operation":
        required_kinds = ["K"]
    unresolved = []
    for obj in task.objects:
        for kind in required_kinds:
            rows = [b for b in admissible if b.object_id == obj and b.category == kind]
            if not rows:
                unresolved.append(f"{obj}:{kind}:missing_or_inadmissible")
            if kind == "R":
                fields = ["interface", "state", field] if fault else ["event_type"]
                for name in fields:
                    values = {canonical(b.fields[name]) for b in rows if name in b.fields}
                    if not permitted(task, obj, [name]):
                        unresolved.append(f"{obj}:{name}:permission_denied")
                    elif not values:
                        unresolved.append(f"{obj}:{name}:missing")
                    elif len(values) > 1:
                        unresolved.append(f"{obj}:{name}:conflicting_observations")
    mapping_gaps = {}
    if fault:
        for left, right in zip(task.path.positions, task.path.positions[1:], strict=False):
            gaps = pair_gaps(task, admissible, left.object_id, right.object_id)
            mapping_gaps[f"{left.object_id}/{right.object_id}"] = gaps
            unresolved.extend(gaps)
    return {
        "version": VERSION,
        "admissible_ids": [b.evidence_id for b in admissible],
        "rejected": rejected,
        "unresolved": sorted(set(unresolved)),
        "mapping_gaps": mapping_gaps,
        "identity_steps": {obj: f"id{i + 1}" for i, obj in enumerate(task.objects)},
        "interface": "N3" if task.template == "upf_n3_fault" else "N4",
        "configuration_field": field,
        "fault_investigation": fault,
        "manual_investigation": task.template == "manual_operation",
        "post_generation_repair": False,
        "uses_gold_or_contract_states": False,
    }
