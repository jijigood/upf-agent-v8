"""Task/reference consistency and strict matching for the reported R07/R09 defect."""

import pytest

from upf_agent.v8.models import digest
from upf_agent.v8.plan_cases import SPECS, prepare_case
from upf_agent.v8.plan_ir import PlanIR, PlanStep
from upf_agent.v8.plan_metrics import score_case
from upf_agent.v8.plan_validator import PlanValidationReport
from upf_agent.v8.reference_revision import revise_peer_mapping


@pytest.mark.parametrize("index", range(24))
def test_case_branches_require_mapping_and_two_identities_only_for_faults(tmp_path, index):
    task, gold = prepare_case(tmp_path / "case", index)
    manual = SPECS[index][0] == "manual_operation"
    for branch in gold.any_of:
        mappings = [p for p in branch.required if p.action_type == "VERIFY_PEER_MAPPING"]
        if manual:
            assert not mappings
            assert "本任务不要求双侧映射调查" in task.question
            continue
        assert len(mappings) == 1
        mapping = mappings[0]
        identities = {
            p.target: p.pattern_id for p in branch.required if p.action_type == "CHECK_IDENTITY"
        }
        assert set(identities) == set(task.objects)
        assert mapping.target == task.path.positions[0].object_id
        assert mapping.parameters == {"peer_object_id": task.path.positions[1].object_id}
        assert set(mapping.depends_on) == set(identities.values())
    assert not gold.reviewed
    assert revise_peer_mapping(task, gold) == gold


@pytest.mark.parametrize("index", [0, 4])
@pytest.mark.parametrize("mutation", ["none", "missing", "wrong_peer", "one_dependency"])
def test_reference_matching_cannot_accept_missing_or_wrong_mapping_even_via_review_branch(
    tmp_path, index, mutation
):
    task, gold = prepare_case(tmp_path / "case", index)
    # Exercise every alternative independently; Validator validity is fixed to isolate matching.
    for branch in gold.any_of:
        steps = [
            PlanStep(
                step_id=p.pattern_id,
                text="reference matching control",
                action_type=p.action_type,
                target=p.target,
                parameters=p.parameters,
                depends_on=p.depends_on,
            )
            for p in branch.required
        ]
        mapping = next(s for s in steps if s.action_type == "VERIFY_PEER_MAPPING")
        if mutation == "missing":
            steps.remove(mapping)
        elif mutation == "wrong_peer":
            mapping.parameters = {"peer_object_id": mapping.target}
        elif mutation == "one_dependency":
            mapping.depends_on = mapping.depends_on[:1]
        plan = PlanIR(
            context_fingerprint="matching-control",
            scope_fingerprint=digest(task.permission),
            batch_id="matching-control",
            evaluation_as_of=task.as_of,
            target_objects=task.objects,
            steps=steps,
            stop_conditions=["stop on unknown"],
        )
        validation = PlanValidationReport(raw_plan_validity=True, published_plan_validity=True)
        result = score_case(plan, validation, gold)
        assert result["reference_pass"] is (mutation == "none")
        assert result["vpr"] is None


def test_changed_reference_cannot_inherit_old_approval(tmp_path):
    task, gold = prepare_case(tmp_path / "case", 0)
    body = gold.model_dump(mode="json")
    body.update(reviewed=True, reviewers=["reviewer-1", "reviewer-2"], review_version="old-hash")
    for branch in body["any_of"]:
        branch["required"] = [
            p for p in branch["required"] if p["action_type"] != "VERIFY_PEER_MAPPING"
        ]
    old = type(gold).model_validate(body)
    new = revise_peer_mapping(task, old)
    assert not new.reviewed and new.reviewers == [] and new.review_version == "unreviewed"
    assert old.reviewed  # No mutation of the original record.


def test_scope_mismatch_and_ambiguous_existing_mapping_require_explicit_resolution(tmp_path):
    task, gold = prepare_case(tmp_path / "case", 0)
    wrong = gold.model_copy(deep=True)
    wrong.permission_fingerprint = "wrong"
    with pytest.raises(ValueError, match="scope"):
        revise_peer_mapping(task, wrong)
    wrong = gold.model_copy(deep=True)
    mapping = next(p for p in wrong.any_of[0].required if p.action_type == "VERIFY_PEER_MAPPING")
    mapping.depends_on = mapping.depends_on[:1]
    with pytest.raises(ValueError, match="adjudication"):
        revise_peer_mapping(task, wrong)
