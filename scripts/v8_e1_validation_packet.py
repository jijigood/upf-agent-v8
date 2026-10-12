"""Prepare source-bound validation authoring drafts; never approve Gold or evidence."""

import argparse
import csv
import json
import re
import shutil
from collections import Counter
from pathlib import Path

from upf_agent.v8.e1_dataset import CaseManifest, inside, read, sha, write
from upf_agent.v8.models import OrchestrationTask

REQUIREMENTS = [
    ("identity_and_scope", "核对对象、产品版本、采集时窗和只读权限", "CHECK_IDENTITY"),
    ("session_and_probe", "核对UE会话及探针的源、目的、大小、时间和返回码", None),
    ("linux_tun_state", "核对核心侧ogstun的管理状态、地址与UPF配置一致性", None),
    ("packet_direction", "结合两侧抓包区分请求到达、响应生成及返回路径", None),
    ("linux_filter_counters", "只读核对INPUT/OUTPUT规则及方向对应的计数", None),
    ("logs_and_unknowns", "核对日志实际内容和缺失资料，不从空窗口推断正常", "READ_LOG"),
    ("stop_and_escalate", "证据、权限或动作表达不足时补证或转人工", "REQUEST_EVIDENCE"),
]


def validation_cases(dataset):
    """Visit validation only; do not load the dataset-wide Gold/heldout tree."""
    result = []
    for folder in sorted((dataset / "validation").iterdir()):
        if not folder.is_dir():
            continue
        manifest = CaseManifest.model_validate(read(folder / "case.json"))
        if manifest.split != "validation" or manifest.case_id != folder.name:
            raise ValueError("validation folder and case split disagree")
        visible = inside(dataset, manifest.visible_root, directory=True)
        task_path = inside(dataset, manifest.task_file)
        if not visible.is_relative_to(folder.resolve()) or not task_path.is_relative_to(visible):
            raise ValueError("validation source outside its declared case")
        task = OrchestrationTask.model_validate(read(task_path))
        for relative, expected in manifest.raw_source_hashes.items():
            if sha(inside(visible, relative)) != expected:
                raise ValueError("validation raw source hash mismatch")
        result.append((manifest, task, visible, task_path))
    if not result:
        raise ValueError("no validation cases; heldout cannot be used as fallback")
    return result


def private_round(project, provenance, raw_hash):
    capture = Path(provenance.get("capture_root", provenance.get("actual_capture", "")))
    if not capture.is_absolute() or not capture.resolve().is_relative_to(project):
        raise ValueError("capture must be inside this project")
    if "capture_round" in provenance:
        number = provenance["capture_round"]
    else:
        matches = [
            p
            for p in (capture / "rounds").glob("round-*/input/snapshot.json")
            if sha(p) == raw_hash
        ]
        if len(matches) != 1:
            raise ValueError("normal snapshot must identify exactly one original round")
        number = int(matches[0].parents[1].name.removeprefix("round-"))
    raw = capture / "rounds" / f"round-{number:03d}" / "input/snapshot.json"
    if sha(raw) != raw_hash:
        raise ValueError("raw snapshot and original capture differ")
    return capture / "private" / f"round-{number:03d}"


def verify_condition(condition, snapshot, external):
    probes = snapshot.get("normal_probes", {"normal": snapshot.get("normal_probe")})
    if not probes or any(p is None or p["returncode"] == 0 for p in probes.values()):
        return False
    if condition == "ogstun-admin-down":
        link = external.get("links", external.get("ogstun"))
        return bool(
            link and link["returncode"] == 0 and "UP" not in json.loads(link["stdout"])[0]["flags"]
        )
    if condition not in {"inner-request-filter", "inner-reply-filter"}:
        raise ValueError("condition outside this validation authoring protocol")
    chain = "input" if condition == "inner-request-filter" else "output"
    direction = "8" if chain == "input" else "0"
    if external[chain]["returncode"] != 0:
        return False
    return bool(
        re.search(
            r"^\s*[1-9]\d*\s+\d+\s+DROP\s+icmp.*ogstun.*icmptype " + direction,
            external[chain]["stdout"],
            re.M,
        )
    )


def prepare(project, dataset, output, knowledge):
    project, dataset, output = (p.resolve() for p in [project, dataset, output])
    if output.exists() or output.is_relative_to(dataset):
        raise ValueError("fresh packet outside original dataset required")
    cases = validation_cases(dataset)
    sources = read(knowledge / "index.json")
    for source in sources:
        if sha(knowledge.parent / source["file"]) != source["sha256"]:
            raise ValueError("pinned knowledge source mismatch")
    output.mkdir(parents=True)
    shutil.copytree(knowledge, output / "organizer-only/knowledge-sources")
    rows, reviews, original_hashes = [], [], {}
    for m, task, visible, task_path in cases:
        raw_path = inside(visible, "data/raw/snapshot.json")
        snapshot = read(raw_path)
        provenance_path = inside(dataset, m.provenance_file)
        provenance = read(provenance_path)
        private = private_round(project, provenance, sha(raw_path))
        truth, external = read(private / "truth.json"), read(private / "external-verification.json")
        if not verify_condition(truth["condition"], snapshot, external):
            raise ValueError("private injection readback and visible probe disagree")
        target = output / "organizer-only" / m.case_id
        target.mkdir(parents=True)
        shutil.copytree(visible, output / "normal-inputs" / m.case_id)
        for name in [
            "truth.json",
            "external-verification.json",
            "inject.json",
            "health-before.json",
            "health-after.json",
        ]:
            shutil.copy2(private / name, target / name)
            original_hashes[str((private / name).relative_to(project))] = sha(private / name)
        shutil.copy2(provenance_path, target / "provenance.json")
        for path in [task_path, provenance_path, *visible.rglob("*")]:
            if path.is_file():
                original_hashes[str(path.relative_to(project))] = sha(path)
        normal = read(inside(visible, task.observation_files[0]))
        logs = snapshot["core"]["logs_and_config"]
        row = {
            "case_id": m.case_id,
            "condition": truth["condition"],
            "normal_snapshot_sha256": sha(raw_path),
            "source_group": m.source_group,
            "structure_family": m.structure_family,
            "upf_window_log_chars": len(logs.get("upf.log", "")),
            "ran_window_log_chars": len(logs.get("gnb.log", "")),
            "physical_condition_readback_pass": True,
            "corroborated": normal.get("corroborated") is True,
            "shared_core_inventory_on_ran_binding": any(
                o["object_id"] == "ran" and "core_interface_inventory" in o["fields"]
                for o in normal["observations"]
            ),
            "missing_typed_action_requirements": sum(
                action is None for _, _, action in REQUIREMENTS
            ),
            "independent_Gold_approved": False,
        }
        rows.append(row)
        write(
            target / "reference-authoring-draft.json",
            {
                "case_id": m.case_id,
                "status": "automatically prepared authoring draft; unreviewed",
                "not_a_CaseGold": True,
                "reviewed": False,
                "actual_human_reviews": 0,
                "facts": row,
                "task": task.model_dump(mode="json"),
                "requirements_to_review": [
                    {
                        "id": name,
                        "description": text,
                        "existing_typed_action": action,
                        "required": None,
                        "depends_on": None,
                        "acceptable_alternatives": None,
                    }
                    for name, text, action in REQUIREMENTS
                ],
                "injection_truth_is_not_model_visible": True,
                "root_cause_from_model_visible_data": "not adjudicated",
                "task_solvability": None,
                "natural_language_reference": None,
                "permission_and_action_gaps_must_not_be_deleted_to_fit_current_system": True,
                "forbidden_claims_to_review": [
                    "已执行修复",
                    "由空日志证明业务正常",
                    "未经证据确认根因",
                ],
                "stop_conditions_to_review": ["缺少适用知识或双侧证据", "操作超出权限或动作表"],
                "knowledge_sources": sources,
                "unresolved_source_questions": [
                    "空窗口日志是否符合采集时段，是否还需其他日志文件",
                    "RAN绑定中的核心侧接口／UE探针应作为共享背景还是对象事实",
                    "Open5GS手册如何对应本案例版本、拓扑与目标；UERANSIM适用知识仍需补充",
                    "只读调查任务与完整故障定位／修复的成功定义应分别制定",
                ],
            },
        )
        for seat in [1, 2]:
            reviews.append(
                {
                    "case_id": m.case_id,
                    "seat": seat,
                    "reviewer": "",
                    "qualification": "",
                    "facts_and_projection_decision": "",
                    "knowledge_applicability_decision": "",
                    "Gold_draft_decision": "",
                    "solvability": "",
                    "reference_sha256": "",
                    "review_source": "",
                    "notes": "",
                }
            )
    for name, table_rows in [
        ("organizer-source-facts.csv", rows),
        ("empty-expert-review.csv", reviews),
    ]:
        with (output / name).open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(table_rows[0]))
            writer.writeheader()
            writer.writerows(table_rows)
    write(output / "original-inputs-sha256.json", original_hashes)
    result = {
        "validation_cases": len(cases),
        "condition_counts": dict(Counter(r["condition"] for r in rows)),
        "physical_readbacks_verified": len(rows),
        "empty_UPF_log_windows": sum(r["upf_window_log_chars"] == 0 for r in rows),
        "empty_RAN_log_windows": sum(r["ran_window_log_chars"] == 0 for r in rows),
        "shared_core_inventory_on_ran_bindings": sum(
            r["shared_core_inventory_on_ran_binding"] for r in rows
        ),
        "expert_review_rows": len(reviews),
        "actual_human_reviews": 0,
        "approved_Gold": 0,
        "evidence_admission_flags_changed": False,
        "heldout_inputs_read": 0,
        "new_model_calls": 0,
    }
    assert all(sha(project / name) == expected for name, expected in original_hashes.items())
    write(output / "summary.json", result)
    write(
        output / "README.md.json",
        {
            "order": [
                "先阅读normal-inputs并独立形成调查结论，再对照organizer-only注入真值与参考草稿",
                "分别审核来源投影、知识适用性和Gold；两名实际评审独立记录，分歧另存仲裁",
                "编制完整自然语言参考后再映射CaseGold；缺少动作要保留为表达缺口，不删除必要步骤",
                "空表和自动草稿均不是批准，不能上传organizer-only为模型上下文",
            ]
        },
    )
    write(
        output / "sha256_manifest.json",
        {str(p.relative_to(output)): sha(p) for p in sorted(output.rglob("*")) if p.is_file()},
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dataset", type=Path, default=Path("eval/v8/e1"))
    parser.add_argument("--knowledge", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            prepare(args.project, args.dataset, args.output, args.knowledge), ensure_ascii=False
        )
    )
