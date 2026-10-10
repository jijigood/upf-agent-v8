"""Task-derived reference correction; never infer requirements from generated plans."""

from upf_agent.v8.models import digest
from upf_agent.v8.plan_ir import ActionPattern, CaseGold, GoldBranch


def revise_peer_mapping(task, gold: CaseGold):
    """Require one two-sided mapping check in every N3/N4 allowed branch.

    A human escalation remains an alternative to interface/configuration checks,
    but includes the stated identity and conditional mapping investigation.
    No source, task, solvability or review approval is changed here.
    """
    if task.template not in {"upf_n3_fault", "upf_n4_fault"}:
        return gold.model_copy(deep=True)
    if (
        gold.objects != task.objects
        or gold.permission_fingerprint != digest(task.permission)
        or gold.version != task.version
        or gold.as_of != task.as_of
    ):
        raise ValueError("reference does not match task scope/time/version/permission")
    positions = task.path.positions
    if len(positions) != 2 or {p.object_id for p in positions} != set(task.objects):
        raise ValueError("this development reference requires an explicit two-object path")
    left, right = (p.object_id for p in positions)
    branches = []
    for branch in gold.any_of:
        required = [p.model_copy(deep=True) for p in branch.required]
        identities = []
        for obj in [left, right]:
            matches = [p for p in required if p.action_type == "CHECK_IDENTITY" and p.target == obj]
            if len(matches) > 1:
                raise ValueError("ambiguous identity anchors in reference")
            if not matches:
                pattern = ActionPattern(
                    pattern_id=f"id-{digest(obj)[:8]}", action_type="CHECK_IDENTITY", target=obj
                )
                required.insert(len(identities), pattern)
            else:
                pattern = matches[0]
            identities.append(pattern.pattern_id)
        mappings = [p for p in required if p.action_type == "VERIFY_PEER_MAPPING"]
        if mappings:
            if len(mappings) != 1 or (
                mappings[0].target != left
                or mappings[0].parameters != {"peer_object_id": right}
                or set(mappings[0].depends_on) != set(identities)
            ):
                raise ValueError("existing mapping pattern requires explicit adjudication")
        else:
            required.append(
                ActionPattern(
                    pattern_id="peer-mapping",
                    action_type="VERIFY_PEER_MAPPING",
                    target=left,
                    parameters={"peer_object_id": right},
                    depends_on=identities,
                )
            )
        branches.append(
            GoldBranch(branch_id=branch.branch_id, required=required, optional=branch.optional)
        )
    result = gold.model_dump(mode="json")
    result["any_of"] = [b.model_dump(mode="json") for b in branches]
    # A changed reference requires approval of its new hash; old approvals do not transfer.
    if result["any_of"] != gold.model_dump(mode="json")["any_of"]:
        result.update(reviewed=False, reviewers=[], review_version="unreviewed")
    return CaseGold.model_validate(result)
