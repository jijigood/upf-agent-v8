import importlib.util
import io
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest


def load_script(name):
    path = Path(__file__).resolve().parents[1] / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bundle = load_script("v8_wp10_bundle")
matrix = load_script("v8_phase3_matrix_review")


def test_pinned_archive_roundtrip_and_tamper(tmp_path):
    root = tmp_path / "source"
    root.mkdir()
    (root / "raw.txt").write_text("original failed output")
    bundle.write(
        root / "bundle-manifest.json", {"files": {"raw.txt": bundle.sha(root / "raw.txt")}}
    )
    archive = tmp_path / "bundle.tar.gz"
    bundle.pack(root, archive)
    target = tmp_path / "relocated"
    assert bundle.extract(archive, target) == 1
    (target / "raw.txt").write_text("replaced by successful output")
    with pytest.raises(ValueError, match="hash mismatch"):
        bundle.verify(target)


@pytest.mark.parametrize("name", ["../outside", "/absolute", "a/../../outside", "a\\outside"])
def test_archive_rejects_path_escape(tmp_path, name):
    archive = tmp_path / "bad.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        info = tarfile.TarInfo(name)
        info.size = 1
        tar.addfile(info, io.BytesIO(b"x"))
    with pytest.raises(ValueError, match="unsafe"):
        bundle.extract(archive, tmp_path / "target")


def test_archive_rejects_link_and_duplicate_member(tmp_path):
    for kind in ["link", "duplicate"]:
        archive = tmp_path / f"{kind}.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            info = tarfile.TarInfo("raw.txt")
            if kind == "link":
                info.type = tarfile.SYMTYPE
                info.linkname = "/tmp/outside"
                tar.addfile(info)
            else:
                info.size = 1
                tar.addfile(info, io.BytesIO(b"x"))
                tar.addfile(info, io.BytesIO(b"y"))
        with pytest.raises(ValueError, match="non-regular or duplicate"):
            bundle.extract(archive, tmp_path / kind)


def test_manifest_cannot_follow_directory_symlink(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "raw.txt").write_text("raw")
    root = tmp_path / "bundle"
    root.mkdir()
    (root / "data").symlink_to(outside, target_is_directory=True)
    bundle.write(
        root / "bundle-manifest.json", {"files": {"data/raw.txt": bundle.sha(outside / "raw.txt")}}
    )
    with pytest.raises(ValueError, match="symlink"):
        bundle.verify(root)


def test_public_screen_rejects_private_document_and_populated_auth(tmp_path):
    doc = tmp_path / "manual.docx"
    doc.write_bytes(b"private")
    with pytest.raises(ValueError, match="private/binary"):
        bundle.screen(doc, public=True)
    bundle.screen(doc, public=False)
    config = tmp_path / "models.yaml"
    config.write_text(
        "generation:\n  endpoint: http://127.0.0.1:18000/v1\n  api_key: secret-value\n"
    )
    with pytest.raises(ValueError, match="auth field"):
        bundle.screen(config, public=True)


def test_credential_screen_does_not_mistake_task_revision_label_for_key(tmp_path):
    path = tmp_path / "protocol.json"
    path.write_text('{"revision": "task-required-two-sided-mapping-1"}')
    bundle.screen(path, public=True)
    path.write_text('"' + "sk-" + "a" * 24 + '"')
    with pytest.raises(ValueError, match="credential pattern"):
        bundle.screen(path, public=True)


def test_relocated_seed_cache_preserves_hash_without_original(tmp_path):
    cache = tmp_path / "cache"
    cache.mkdir()
    path = cache / "query-001.json"
    path.write_text('{"raw": "frozen P3 result"}')
    pins = {"/nonexistent/original/query-001.json": bundle.sha(path)}
    assert matrix.seed_cache_paths(pins, cache) == {path.name: path}
    path.write_text("changed")
    with pytest.raises(ValueError, match="hash mismatch"):
        matrix.seed_cache_paths(pins, cache)


def test_original_cache_compatibility_and_ambiguous_relocation(tmp_path):
    path = tmp_path / "query-001.json"
    path.write_text("original")
    pins = {str(path): bundle.sha(path)}
    assert matrix.seed_cache_paths(pins) == {path.name: path}
    pins["/other/query-001.json"] = bundle.sha(path)
    with pytest.raises(ValueError, match="ambiguous"):
        matrix.seed_cache_paths(pins, tmp_path)


def test_relocated_cache_rejects_symlink(tmp_path):
    cache = tmp_path / "cache"
    cache.mkdir()
    original = tmp_path / "query-001.json"
    original.write_text("original")
    (cache / original.name).symlink_to(original)
    with pytest.raises(ValueError, match="escaped"):
        matrix.seed_cache_paths({str(original): bundle.sha(original)}, cache)


def test_offline_guard_blocks_calls_and_original_reads_in_child(tmp_path):
    original = tmp_path / "original"
    original.mkdir()
    (original / "pyproject.toml").write_text("old project")
    script_root = Path(__file__).resolve().parents[1] / "scripts"
    code = f"""
import socket, sys, subprocess
from pathlib import Path
sys.path.insert(0, {str(script_root)!r})
from v8_bundle_replay import install_guard
from v8_bundle_replay import replay
try:
    replay(Path({str(tmp_path)!r}), Path({str(tmp_path / 'runtime/reproduce')!r}), fresh_cpu=True)
except ValueError as error:
    assert 'runtime/v8-next/phase3' in str(error)
else:
    raise AssertionError('E5 namespace mismatch must fail before copying/evaluating')
counts = install_guard([Path({str(original)!r})])
operations = [
    lambda: socket.socket().connect(('127.0.0.1', 1)),
    lambda: Path({str(original / 'pyproject.toml')!r}).read_text(),
    lambda: subprocess.run([sys.executable, '-c', 'print(1)']),
]
for operation in operations:
    try:
        operation()
    except PermissionError:
        pass
    else:
        raise AssertionError('guard failed')
assert counts['blocked_connections'] == 1, counts
assert counts['blocked_original_reads'] == 1, counts
assert counts['blocked_processes'] == 1, counts
subprocess.run(['uname', '-p'], check=True, capture_output=True)
assert counts['allowed_metadata_processes'] == 1, counts
try:
    subprocess.run(['uname', '-a'], capture_output=True)
except PermissionError:
    pass
else:
    raise AssertionError('different command must remain blocked')
assert counts['blocked_processes'] == 2, counts
"""
    subprocess.run([sys.executable, "-c", code], check=True, capture_output=True, text=True)
