"""Finite bilateral source coverage and consistency; future collection is never evidence."""

from itertools import product

from upf_agent.v8.models import canonical

PAIR_FIELDS = ("service_id", "local_endpoint", "peer_endpoint", "direction", "mapping_version")
DIRECTIONS = {("tx", "rx"), ("rx", "tx"), ("egress", "ingress"), ("ingress", "egress")}


def pair_gaps(task, bindings, target, peer):
    """Bindings must already pass independent eligibility; do not choose away conflicts."""
    gaps = set()
    sides = {
        obj: [b for b in bindings if b.category == "P" and b.object_id == obj]
        for obj in (target, peer)
    }
    for obj, rows in sides.items():
        if not rows:
            gaps.add(f"{obj}:P:missing_or_inadmissible")
        for field in PAIR_FIELDS:
            values = {canonical(b.fields[field]) for b in rows if b.fields.get(field) is not None}
            if rows and not values:
                gaps.add(f"{obj}:P:{field}:missing")
            elif len(values) > 1:
                gaps.add(f"{obj}:P:{field}:conflicting_observations")
        for row in rows:
            if not row.config_version:
                gaps.add(f"{obj}:P:config_version:missing")
            if row.observed is None:
                gaps.add(f"{obj}:P:observed_window:missing")
            runtime = [b for b in bindings if b.category == "R" and b.object_id == obj]
            if any(b.config_version != row.config_version for b in runtime):
                gaps.add(f"{obj}:runtime_pair_config_version:mismatch")
    prefix = f"{target}/{peer}"
    for left, right in product(sides[target], sides[peer]):
        a, b = left.fields, right.fields
        checks = {
            "service_id": bool(task.path.service_id)
            and a.get("service_id") == b.get("service_id") == task.path.service_id,
            "mapping_version": bool(task.path.version)
            and a.get("mapping_version") == b.get("mapping_version") == task.path.version,
            "endpoints": bool(a.get("local_endpoint"))
            and bool(a.get("peer_endpoint"))
            and a.get("local_endpoint") == b.get("peer_endpoint")
            and a.get("peer_endpoint") == b.get("local_endpoint"),
            "direction": (a.get("direction"), b.get("direction")) in DIRECTIONS,
            "config_version": bool(left.config_version)
            and left.config_version == right.config_version,
            "observed_window": bool(left.observed and right.observed)
            and max(left.observed.start, right.observed.start)
            < min(left.observed.end, right.observed.end),
        }
        for name, ok in checks.items():
            if not ok:
                gaps.add(f"{prefix}:{name}:mismatch")
    return sorted(gaps)


def mapping_role_valid(task, target, peer):
    if not task.object_profiles:
        return True  # Historical tasks did not declare object roles; do not infer from names.
    if target not in task.object_profiles or peer not in task.object_profiles:
        return False
    expected = {"upf_n3_fault": {"upf", "ran"}, "upf_n4_fault": {"upf", "smf"}}
    return (
        task.template not in expected
        or {task.object_profiles[target].role, task.object_profiles[peer].role}
        == expected[task.template]
    )
