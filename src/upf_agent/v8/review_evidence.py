"""Physical JSON-to-binding review, including both recorded and binding time windows."""

import hashlib
import json

from upf_agent.contracts import TimeWindow
from upf_agent.v8.adapters import source_path
from upf_agent.v8.models import canonical, object_product_version


def source_review(root, binding, task):
    findings = []
    source = binding.source
    try:
        path = source_path(root, source.relative_path)
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != source.sha256:
            findings.append("source_hash_mismatch")
        if path.suffix != ".json":
            from upf_agent.v8.plan_source_verifier import verify_plan_source

            if not verify_plan_source(root, binding, task):
                findings.append("unverified_native_document")
            return sorted(set(findings))
        body = json.loads(raw)
        record = body
        for part in source.locator.strip("/").split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            if isinstance(record, list):
                if not part.isascii() or not part.isdigit() or str(int(part)) != part:
                    raise ValueError("invalid array pointer")
                record = record[int(part)]
            else:
                record = record[part]
        if body.get("source_id") != source.source_id:
            findings.append("source_id_mismatch")
        for name in ("category", "product", "version"):
            if record.get(name) != getattr(binding, name):
                findings.append(f"source_{name}_mismatch")
        if task.aliases.get(record.get("object_id"), record.get("object_id")) != binding.object_id:
            findings.append("source_object_id_mismatch")
        if (
            binding.category in {"R", "P"}
            and record.get("config_version") != binding.config_version
        ):
            findings.append("source_config_version_mismatch")
        if any(
            k not in record.get("fields", {}) or canonical(record["fields"][k]) != canonical(v)
            for k, v in binding.fields.items()
        ):
            findings.append("source_fields_mismatch")
        for flag in ("synthetic", "corroborated"):
            if (body.get(flag) is True) != getattr(binding, flag):
                findings.append(f"source_{flag}_mismatch")
        windows = ["valid"]
        if binding.category in {"R", "P"} or binding.observed is not None:
            windows.append("observed")
        for name in windows:
            value = record.get(name)
            window = TimeWindow.model_validate_json(json.dumps(value)) if value else None
            if window != getattr(binding, name):
                findings.append(f"source_{name}_mismatch")
        product, version = object_product_version(task, binding.object_id)
        if binding.version != version or not version:
            findings.append("binding_version_mismatch")
        if binding.category == "K" and binding.product != product:
            findings.append("binding_product_mismatch")
        # Judge binding time independently of the source; neither may overwrite the other.
        if binding.valid and not binding.valid.start <= task.as_of < binding.valid.end:
            findings.append("binding_outside_validity")
        if binding.category in {"R", "P"}:
            if binding.observed is None:
                findings.append("binding_unknown_window")
            elif binding.observed.end > task.as_of:
                findings.append("binding_future_observation")
            elif (task.as_of - binding.observed.end).total_seconds() > 300:
                findings.append("binding_stale_observation")
        return sorted(set(findings))
    except (OSError, ValueError, KeyError, TypeError, IndexError):
        return sorted(set(findings + ["unresolvable_source"]))
