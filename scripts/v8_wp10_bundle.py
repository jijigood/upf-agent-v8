"""Build pinned, local WP10 bundles from an explicit dataset allowlist."""

import argparse
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import tarfile
from pathlib import Path, PurePosixPath

SCRIPTS = [
    "v8_wp10_bundle.py",
    "v8_bundle_replay.py",
    "v8_wp10_results.py",
    "v8_phase2_audit.py",
    "v8_phase2_reference_revision.py",
    "v8_phase3_matrix_review.py",
    "v8_e3_audit.py",
    "v8_e4_review.py",
    "v8_requirement_graph_engine_probe.py",
    "v8_e2_supplement.py",
    "v8_e2_supplement_review.py",
]
SYNTHETIC = {
    "phase2": ["pilot-final-001", "closure-full-004", "reference-revision-002"],
    "phase3": [
        "wp08-pilot-004",
        "e3-public-four-methods-002",
        "e4-full-single-001",
        "e5-full-002",
        "e6-full-002",
        "e3-four-methods-002",
        "e3-public-four-methods-001",
        "e6-full-001",
        "e6-full-001-interruption.json",
        "e3-four-methods-audit-002.json",
        "e3-public-four-methods-audit-001.json",
    ],
}
PRIVATE_E2 = {
    "phase3": [
        "e2-full-003",
        "e2-mixed-pilot-and-sensitivity-003",
        "e2-full-001.log",
        "e2-full-002.log",
        "e2-mixed-pilot-and-sensitivity-001.log",
        "e2-mixed-pilot-and-sensitivity-002.log",
    ],
}
PRIVATE_SUFFIXES = {".docx", ".doc", ".pdf", ".xlsx", ".pptx", ".safetensors", ".gguf"}
SECRET = re.compile(
    rb"(?:(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_path(root, name):
    p = PurePosixPath(name)
    if p.is_absolute() or not p.parts or ".." in p.parts or "\\" in name:
        raise ValueError(f"unsafe bundle path: {name}")
    path = root / name
    # Reject directory symlinks as well as file symlinks, even when they point inside.
    if any((root / Path(*p.parts[:i])).is_symlink() for i in range(1, len(p.parts) + 1)):
        raise ValueError(f"bundle symlink: {name}")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"bundle path escape: {name}")
    return path


def screen(path, public):
    if path.is_symlink():
        raise ValueError("source symlink")
    if path.name == ".env" or path.name.startswith(".env."):
        raise ValueError("environment file forbidden")
    if public and path.suffix.lower() in PRIVATE_SUFFIXES:
        raise ValueError(f"private/binary asset forbidden in synthetic bundle: {path.name}")
    if path.suffix in {".json", ".jsonl", ".yaml", ".txt", ".md", ".log", ".py"}:
        if SECRET.search(path.read_bytes()):
            raise ValueError(f"credential pattern found: {path.name}")
    if path.name == "models.yaml":
        # Frozen historical model metadata is preserved byte for byte. It is never loaded
        # by the offline runner. Reject populated auth fields instead of rewriting hashes.
        import yaml

        def inspect(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if (
                        str(key).lower().replace("-", "_")
                        in {"api_key", "password", "access_token", "secret", "authorization"}
                        and item
                    ):
                        raise ValueError("populated historical auth field")
                    inspect(item)
            elif isinstance(value, list):
                for item in value:
                    inspect(item)

        inspect(yaml.safe_load(path.read_text()))


def verify(root):
    manifest = read(root / "bundle-manifest.json")
    for name, expected in manifest["files"].items():
        path = safe_path(root, name)
        if not path.is_file() or sha(path) != expected:
            raise ValueError(f"bundle hash mismatch: {name}")
    return len(manifest["files"])


def pack(root, archive):
    # Deterministic member metadata and gzip timestamp; no links or special files.
    with (
        archive.open("xb") as raw,
        gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, compresslevel=3) as zipped,
    ):
        with tarfile.open(fileobj=zipped, mode="w") as tar:
            for path in sorted(root.rglob("*")):
                if not path.is_file():
                    continue
                name = str(path.relative_to(root))
                safe_path(root, name)
                info = tar.gettarinfo(str(path), arcname=name)
                info.uid = info.gid = info.mtime = 0
                info.uname = info.gname = ""
                info.mode = 0o644
                with path.open("rb") as stream:
                    tar.addfile(info, stream)


def extract(archive, target):
    if target.exists():
        raise ValueError("choose a new extraction directory")
    target.mkdir(parents=True)
    with tarfile.open(archive, "r:gz") as tar:
        seen = set()
        for member in tar:
            path = safe_path(target, member.name)
            if not member.isfile() or member.name in seen:
                raise ValueError("non-regular or duplicate archive member")
            seen.add(member.name)
            path.parent.mkdir(parents=True, exist_ok=True)
            stream = tar.extractfile(member)
            with path.open("xb") as dest:
                shutil.copyfileobj(stream, dest)
    return verify(target)


def failure_catalog():
    return {
        "schema": "wp10-failure-catalog-1",
        "reviewed": False,
        "heldout_consumed": False,
        "items": [
            {
                "id": "phase2-pilot-final-001",
                "payload": "data/phase2/pilot-final-001",
                "denominator": 96,
                "meaning": "original development failures retained",
            },
            {
                "id": "phase2-reference-mismatch",
                "payload": "data/phase2/reference-revision-002",
                "reference_cases": 20,
                "rescored_runs": 96,
                "meaning": "R07/R09 post-output reference correction, approval pending",
            },
            {
                "id": "e3-four-methods-002",
                "payload": "data/phase3/e3-four-methods-002",
                "denominator": 128,
                "audit": "data/phase3/e3-four-methods-audit-002.json",
                "meaning": "historical protocol/tool-error mismatch; not final result",
            },
            {
                "id": "e3-public-four-methods-001",
                "payload": "data/phase3/e3-public-four-methods-001",
                "denominator": 128,
                "audit": "data/phase3/e3-public-four-methods-audit-001.json",
                "meaning": "prior public-tool budget/protocol revision; not final result",
            },
            {
                "id": "e3-final-unclosed",
                "payload": "data/phase3/e3-public-four-methods-002",
                "per_method_denominator": 32,
                "meaning": "all unclosed tasks retained",
            },
            {
                "id": "e4-negative-groups",
                "payload": "data/phase3/e4-full-single-001",
                "denominator": 64000,
                "meaning": "all CSV rows, including slower Local groups",
            },
            {
                "id": "e5-ablations",
                "payload": "data/phase3/e5-full-002",
                "decisions": 720,
                "meaning": "unsafe lower layers and reject-all losses retained",
            },
            {
                "id": "e6-full-001",
                "payload": "data/phase3/e6-full-001",
                "interruption": "data/phase3/e6-full-001-interruption.json",
                "expected": 540,
                "completed": 27,
                "pending": 2,
                "meaning": "interrupted batch; never merged into complete 540-run denominator",
            },
        ],
        "excluded_private_history": "E2 raw handbook experiments/logs in separate local attachment",
        "scope": "final software matrices and listed failed predecessors; not every scratch run",
    }


def build(project, output, kind):
    from upf_agent.v8.experiment_manifest import source_manifest

    project, output = project.resolve(), output.resolve()
    if output.exists():
        raise ValueError("choose a new bundle ID")
    public = kind == "synthetic"
    output.mkdir(parents=True)
    root = output / "bundle"
    root.mkdir()
    source = source_manifest(project)
    provenance = {}
    excluded = []
    snapshots = {}

    def copy_file(path, name):
        if not path.is_file():
            raise ValueError(f"missing/nonregular input: {path}")
        screen(path, public)
        target = safe_path(root, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        before = sha(path)
        shutil.copyfile(path, target)
        if sha(target) != before or sha(path) != before:
            raise ValueError("source changed during copy")
        provenance[name] = {"original": str(path.relative_to(project)), "sha256": before}

    for path in sorted((project / "src/upf_agent").rglob("*.py")):
        copy_file(path, str(path.relative_to(project)))
    for name in ["pyproject.toml", "uv.lock", *[f"scripts/{s}" for s in SCRIPTS]]:
        copy_file(project / name, name)
    for phase, names in (SYNTHETIC if public else PRIVATE_E2).items():
        for name in names:
            path = project / "runtime/v8-next" / phase / name
            if path.is_file():
                copy_file(path, f"data/{phase}/{name}")
            else:
                if not path.is_dir() or path.is_symlink():
                    raise ValueError(f"missing/symlink dataset: {name}")
                for file in sorted(path.rglob("*")):
                    if file.is_symlink():
                        if not public and file.name == ".venv-retrieval" and file.is_dir():
                            excluded.append(
                                {
                                    "original": str(file.relative_to(project)),
                                    "reason": "old virtual-environment link; no experiment input",
                                }
                            )
                            continue
                        raise ValueError("dataset symlink")
                    if file.is_file():
                        copy_file(file, f"data/{phase}/{name}/{file.relative_to(path)}")
    if not public:
        cache = project / "runtime/v8-next/phase3/e2-full-002/seed-cache"
        for file in sorted(cache.glob("query-*.json")):
            copy_file(file, f"data/phase3/e2-original-seed-cache/{file.name}")
    # Historical source is recovered only by byte hash from original frozen worktrees.
    # No generated/regenerated implementation is presented as the historical source.
    candidates = [project, *sorted((project / "runtime/v8-next").glob("*/*/worktree"))]
    if public:
        expected_snapshots = {
            "phase2": read(root / "data/phase2/closure-full-004/source_manifest.json"),
            "E3": read(root / "data/phase3/e3-public-four-methods-002/summary.json")["source"],
            "E4": read(root / "data/phase3/e4-full-single-001/summary.json")["source"],
            "E5": read(root / "data/phase3/e5-full-002/protocol.json")["source"],
            "E6": read(root / "data/phase3/e6-full-002/protocol.json")["source"],
        }
    else:
        expected_snapshots = {"E2": read(root / "data/phase3/e2-full-003/summary.json")["source"]}
    for label, expected in expected_snapshots.items():
        for name, expected_sha in expected["files"].items():
            matching = next(
                (
                    candidate / name
                    for candidate in candidates
                    if (candidate / name).is_file() and sha(candidate / name) == expected_sha
                ),
                None,
            )
            if matching is None:
                raise ValueError(f"historical source unavailable: {label}/{name}")
            copy_file(matching, f"history/code/{label}/{name}")
        if source_manifest(root / "history/code" / label) != expected:
            raise ValueError(f"historical source manifest mismatch: {label}")
        snapshots[label] = expected
    if public:
        write(root / "failure-catalog.json", failure_catalog())
    readme = """# WP10 本地复现包

Python 3.11；依赖由 uv.lock 固定。先安装依赖：`uv sync --locked --no-dev`。
依赖已缓存时使用 `uv sync --locked --offline --no-dev`，安装环境不包含模型权重。

在包根目录执行：

```bash
.venv/bin/python scripts/v8_bundle_replay.py --output runtime/v8-next/phase3/wp10-reproduce-001
```

synthetic 包另可追加 `--fresh-cpu` 执行图检索 72 控制、3 次真实 Engine/Ledger、
E3 的 T0/T1/T3 共 96 次、E4 720 更新、E5 720 判定。使用相同合成开发输入设计；
这些新执行不增加独立样本数。真实模型方法只回放存储原文，不重新请求模型。
E3 原数据库在工作副本中读，原始 bytes 与 SHA 保持不变。

默认仅复算历史输出和完整分母；禁用 socket 连接，无 GPU/模型服务依赖。
所有参考仍未获得独立双评；VPR 为 null，未消费正式 heldout。
历史 models.yaml 和 trace 中路径/服务地址仅为冻结元数据，离线 runner 不加载这些配置。
审查表、人工批准、模型权重、环境密钥、仓库 .git 均不包含。

本包只在本机生成，没有对外发布。仓库未提供 LICENSE；本包不授予新的分发许可，
对外发布前仍需明确代码与材料许可，并完成相应的质量审查。
"""
    if public:
        readme += (
            "\n本包只含 synthetic 软件数据。实际手册 E2 不包含，WP08 不能替代 E2 正式质量结论。\n"
        )
    else:
        readme += (
            "\n**PRIVATE E2：本地实际手册材料附件，含真实 DOCX/检索输出，"
            "禁止混入 synthetic 分发包。**\n"
        )
    (root / "README.md").write_text(readme)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=project, capture_output=True, text=True, check=True
    ).stdout.strip()
    write(
        root / "provenance.json",
        {
            "head": head,
            "source": source,
            "copied": provenance,
            "excluded": excluded,
            "historical_sources": snapshots,
        },
    )
    files = {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob("*")) if p.is_file()}
    write(
        root / "bundle-manifest.json",
        {
            "schema": "wp10-bundle-1",
            "kind": kind,
            "synthetic_only": public,
            "files": files,
            "reviewed": False,
            "formal_acceptance": False,
            "heldout_consumed": False,
            "original_code_source": source,
            "secret_screen": "known credential patterns and nonempty model auth fields",
            "public_filter": "explicit synthetic dataset allowlist; no private document binaries",
            "screen_is_not_general_declassification": True,
        },
    )
    assert source_manifest(project) == source
    count = verify(root)
    archive = output / f"wp10-{kind}.tar.gz"
    pack(root, archive)
    receipt = {
        "kind": kind,
        "files": count,
        "archive": str(archive.relative_to(project)),
        "archive_sha256": sha(archive),
        "archive_bytes": archive.stat().st_size,
        "copied_bytes": sum((root / n).stat().st_size for n in files),
        "source_unchanged": True,
        "original_files_changed": False,
        "externally_published": False,
        "human_reviews_imported": 0,
    }
    write(output / "build-receipt.json", receipt)
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--kind", choices=["synthetic", "private-e2"], default="synthetic")
    parser.add_argument("--extract", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.extract:
        if args.output is None:
            parser.error("--extract requires --output")
        print({"verified_files": extract(args.extract, args.output)})
    elif args.verify:
        print({"verified_files": verify(args.verify)})
    else:
        if args.output is None:
            parser.error("--output required")
        print(build(args.project, args.output, args.kind))
