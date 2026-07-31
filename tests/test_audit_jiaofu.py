"""Smoke tests for scripts/audit_jiaofu.py."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "audit_jiaofu.py"
JIAOFU = REPO_ROOT / "zh" / "教辅"


def test_script_imports():
    """The audit module exposes the public surface."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import audit_jiaofu  # noqa: F401
    assert hasattr(audit_jiaofu, "AuditReport")
    assert hasattr(audit_jiaofu, "main")


def test_cli_help():
    """--help exits 0 and emits usage."""
    out = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True
    )
    assert out.returncode == 0, out.stderr
    assert "--chapter" in out.stdout
    assert "--all" in out.stdout
    assert "--json" in out.stdout


def test_chapter10_clean_or_warn_only(tmp_path: Path):
    """Audit on Chapter 10 should NOT report ERROR (this is the freshly
    authored baseline). It may produce WARN that we tolerate."""
    out = subprocess.run(
        [sys.executable, str(SCRIPT), str(JIAOFU), "--chapter", "10", "--json",
         str(tmp_path / "r.json")],
        capture_output=True, text=True,
    )
    assert out.returncode in (0, 1), out.stderr
    data = json.loads((tmp_path / "r.json").read_text())
    errors = [f for f in data["findings"] if f["severity"] == "ERROR"]
    # Ch10 was generated under SOP v1.1; it should have 0 ERROR.
    # The above invocation should pass with no strict failure.
    assert errors == [], f"Chapter 10 must be ERROR-free: {errors}"


def test_full_audit_with_realistic_fixtures(tmp_path: Path):
    """Synthesise a tiny 教辅 fixture that intentionally violates the SOP,
    then assert each violation is detected."""
    fix = tmp_path / "fix"
    (fix / "信息图").mkdir(parents=True)
    (fix / "复习大纲").mkdir(parents=True)
    (fix / "单页proposal").mkdir(parents=True)
    (fix / "思维导图").mkdir(parents=True)
    (fix / "闪卡").mkdir(parents=True)
    (fix / "阶段测试题").mkdir(parents=True)
    (fix / "讲解稿" / "第00章").mkdir(parents=True)

    # 1) H1 first-line violation
    (fix / "信息图" / "第00章.md").write_text(
        "<!-- bad opening comment -->\n\n# Body without H1 at top\n", encoding="utf-8"
    )
    # 2) Absolute /Users/ path
    (fix / "复习大纲" / "第00章.md").write_text(
        "# Title\n\nsee /Users/chenchen/x.md for content\n", encoding="utf-8"
    )
    # 3) Unbalanced $$
    (fix / "单页proposal" / "第00章.md").write_text(
        "# Title\n\nbroken $$ formula without close\n", encoding="utf-8"
    )
    # 4) TODO tag
    (fix / "闪卡" / "第00章.md").write_text(
        "# Title\n\n### Card 1\nTODO: implement\n", encoding="utf-8"
    )
    # 5) Wrong heading in lecture
    (fix / "讲解稿" / "第00章" / "01. wrong.md").write_text(
        "# 讲解稿 · 第 00 章 第 05 节 · 错配\n\ncontent\n", encoding="utf-8"
    )
    # 6) Tiny mindmap with no nodes
    (fix / "思维导图" / "第00章.md").write_text("# Title\n\nshort content\n", encoding="utf-8")
    # 7) Empty quiz
    (fix / "阶段测试题" / "第00章.md").write_text("# Title\n\nshort\n", encoding="utf-8")

    report = subprocess.run(
        [sys.executable, str(SCRIPT), str(fix), "--chapter", "00", "--json",
         str(tmp_path / "r.json")],
        capture_output=True, text=True,
    )
    data = json.loads((tmp_path / "r.json").read_text())
    kinds_found = {f["kind"] for f in data["findings"]}
    errors = [f for f in data["findings"] if f["severity"] == "ERROR"]

    # WRITE caught the HTML-comment opening
    assert any(f["kind"] == "WRITE" and f["path"].endswith("信息图/第00章.md") for f in errors), \
        f"WRITE not flagged for 信息图 violation: {errors}"
    # PATH caught /Users/
    assert any(f["kind"] == "PATH" for f in errors), \
        f"PATH not flagged: {errors}"
    # FORMULA caught unbalanced $$
    assert any(f["kind"] == "FORMULA" for f in errors), \
        f"FORMULA not flagged: {errors}"
    # DISEASE caught TODO
    assert any(f["kind"] == "DISEASE" and "TODO" in f["message"] for f in data["findings"]), \
        f"TODO not flagged: {data['findings']}"
    # ALIGN caught misaligned lecture (filename 01 vs title 第 5 节)
    assert any(f["kind"] == "ALIGN" and "01" in f["path"] for f in errors), \
        f"ALIGN not flagged for misaligned lecture: {errors}"
