"""Requirement-specific graph inputs, with explicit permissions and frozen bounded budgets."""

from typing import Literal

from pydantic import Field

from upf_agent.v8.compiler import permitted
from upf_agent.v8.graph import GraphQueryPlan
from upf_agent.v8.models import (
    EvidenceContract,
    Model,
    OrchestrationTask,
    Requirement,
    digest,
    object_product_version,
)


class RequirementGraphQuery(Model):
    schema_version: Literal["v8-requirement-graph-1"] = "v8-requirement-graph-1"
    task: OrchestrationTask
    contract: EvidenceContract
    requirement: Requirement
    graph: GraphQueryPlan
    reseed_ids: list[str] = Field(default_factory=list, max_length=100)
    top_k: Literal[5, 10, 20] = 10
    alpha: float = Field(default=0.85, gt=0, lt=1)
    tolerance: float = Field(default=1e-8, gt=0, lt=1)
    max_iterations: int = Field(default=1000, ge=1, le=10000)
    denied_reasons: list[str] = Field(default_factory=list)


def compile_requirement_query(
    task,
    contract,
    requirement,
    seeds,
    *,
    reseed_ids=(),
    top_k=10,
    max_nodes=100,
    max_edges=200,
    max_hops=2,
    alpha=0.85,
    tolerance=1e-8,
    max_iterations=1000,
    relations=None,
):
    """Never drop a forbidden object/field to turn a denied requirement into a weaker query."""
    if contract.task_id != task.run_id or contract.task_fingerprint != digest(task):
        raise ValueError("contract does not match current task")
    declared = next(
        (r for r in contract.requirements if r.requirement_id == requirement.requirement_id), None
    )
    if declared != requirement or requirement.kind not in {"K", "R", "P"}:
        raise ValueError("query requires an exact declared K/R/P requirement")
    denied = []
    if not requirement.objects or any(
        not permitted(task, obj, requirement.fields) for obj in requirement.objects
    ):
        denied.append("requirement_permission_denied")
    domains = {p.domain for p in task.path.positions if p.object_id in requirement.objects}
    if requirement.domains and not domains <= set(requirement.domains):
        denied.append("requirement_domain_mismatch")
    profiles = [object_product_version(task, obj) for obj in requirement.objects]
    if requirement.version_required and any(not v or v == "unknown" for _, v in profiles):
        denied.append("unknown_required_version")
    if requirement.kind == "K" and (any(not p for p, _ in profiles) or not requirement.purpose):
        denied.append("unknown_knowledge_product_or_purpose")
    graph = GraphQueryPlan(
        seed_ids=list(dict.fromkeys(seeds)),
        objects=[] if denied else requirement.objects,
        domains=requirement.domains or task.permission.domains,
        relations=relations
        if relations is not None
        else [
            "CONTAINS",
            "DESCRIBES",
            "APPLIES_TO",
            "HAS_INTERFACE",
            "SUPPORTED_BY",
            "OBSERVED_ON",
            "RECEIPT_FOR",
        ],
        as_of=task.as_of,
        version=task.version,
        object_versions={obj: object_product_version(task, obj)[1] for obj in requirement.objects}
        if task.object_profiles
        else {},
        require_version=requirement.version_required,
        allow_synthetic=task.synthetic,
        max_hops=max_hops,
        max_nodes=max_nodes,
        max_edges=max_edges,
        contract_id=contract.contract_id,
    )
    # Freeze values so subsequent caller mutation cannot silently alter a compiled query.
    return RequirementGraphQuery(
        task=task.model_copy(deep=True),
        contract=contract.model_copy(deep=True),
        requirement=requirement.model_copy(deep=True),
        graph=graph,
        reseed_ids=list(dict.fromkeys(reseed_ids)),
        top_k=top_k,
        alpha=alpha,
        tolerance=tolerance,
        max_iterations=max_iterations,
        denied_reasons=denied,
    )
