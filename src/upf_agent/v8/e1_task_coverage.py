"""Explicit user-task obligations, independent of Gold and source admissibility.

This gate checks whether a proposed plan addresses the requested investigation.
It does not approve domain correctness, execution, a cause, or a reference answer.
"""

from pathlib import Path

from pydantic import Field, model_validator

from upf_agent.v8.e1_dataset import read
from upf_agent.v8.models import Model, digest


class TaskAction(Model):
    action_type: str
    target: str
    parameters: dict = Field(default_factory=dict)
    required_fields: list[str] = Field(default_factory=list)


class TaskObligation(Model):
    requirement_id: str
    description: str
    any_of: list[TaskAction] = Field(min_length=1)


class TaskRequest(Model):
    version: str = "v8-explicit-readonly-task-request-1"
    question_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    permission_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    object_profiles_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    obligations: list[TaskObligation] = Field(min_length=1)
    scope: str = "readonly investigation plan; no diagnosis or execution approval"
    authoring_basis: str = "explicit public task question; author proposal awaiting expert review"

    @model_validator(mode="after")
    def unique_ids(self):
        ids = [r.requirement_id for r in self.obligations]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate task obligation IDs")
        return self


def load_task_request(root, task):
    request = TaskRequest.model_validate(read(Path(root) / "data/task-request.json"))
    if (
        request.question_sha256 != digest(task.question)
        or request.permission_sha256 != digest(task.permission)
        or request.object_profiles_sha256 != digest(task.object_profiles)
    ):
        raise ValueError("task request question, permission or product version changed")
    if any(a.target not in task.objects for r in request.obligations for a in r.any_of):
        raise ValueError("task request contains an unauthorized object")
    return request


def action_matches(step, action):
    return (
        step.action_type == action.action_type
        and step.target == action.target
        and all(step.parameters.get(k) == v for k, v in action.parameters.items())
    )


def has_field(fields, path):
    value = fields
    for name in path.split("."):
        if not isinstance(value, dict) or name not in value:
            return False
        value = value[name]
    return True


def covered_obligations(plan, request, bindings, *, require_declaration=True):
    """Check actual steps and required cited fields, never trust a model's coverage claim."""
    by_id = {b.evidence_id: b for b in bindings}
    steps = {s.step_id: s for s in plan.steps} if plan else {}
    claims = getattr(plan, "task_coverage", {}) if plan else {}
    rows = []
    for obligation in request.obligations:
        matched = []
        for step in steps.values():
            for alternative in obligation.any_of:
                if not action_matches(step, alternative):
                    continue
                sources = [by_id.get(ref.evidence_id) for ref in step.evidence]
                if alternative.required_fields and not any(
                    b is not None
                    and b.object_id == alternative.target
                    and all(has_field(b.fields, f) for f in alternative.required_fields)
                    for b in sources
                ):
                    continue
                matched.append(step.step_id)
                break
        declared = claims.get(obligation.requirement_id)
        covered = declared in matched if require_declaration else bool(matched)
        rows.append(
            {
                "requirement_id": obligation.requirement_id,
                "actual_matching_steps": matched,
                "declared_step": declared,
                "covered": covered,
                "status": "covered" if covered else "missing_or_misdeclared",
            }
        )
    return rows
