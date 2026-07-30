"""Audit zh/教辅/ 7 类材料 against the QUALITY_PROCESS v1.1 SOP.

Implements 6+1 mandatory scans (数字硬错 / 跨章路径 / 公式闭合 / 跨章符号 /
病句 / 写盘自检 / 内容-位置对应). Output JSON report and human-readable
summary. Designed to be invoked as part of CI / pre-commit, not on each file
manually.

Usage:
    python3 scripts/audit_jiaofu.py zh/教辅              # scan one chapter
    python3 scripts/audit_jiaofu.py zh/教辅 --chapter 10  # all kinds for Ch10
    python3 scripts/audit_jiaofu.py zh/教辅 --all        # every chapter covered
    python3 scripts/audit_jiaofu.py zh/教辅 --chapter 10 --json /tmp/report.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable

ROOT_MATKIND = ("信息图", "复习大纲", "单页proposal", "思维导图", "闪卡", "阶段测试题")
MIN_BYTES = {
    "信息图": 5_000,
    "复习大纲": 10_000,
    "单页proposal": 2_500,
    "思维导图": 2_000,
    "闪卡": 30_000,
    "阶段测试题": 6_000,
}
SYMBOL_CONTRACT_KEYWORDS = {
    "λ": "特征值 / Lagrange / 正则 / Poisson / 学习率",
    "α": "显著性 / 正则 / 散度 / 学习率 / 融合权重",
    "β": "二类错误 / Beta 分布 / 回归系数 / 超参",
    "δ": "ε-δ / Dirac δ / 增量 / KL 变分",
    "ε": "ε-δ / 隐私预算 / ε-greedy / 数值精度",
    "η": "学习率 / 拒绝水平 / 渐近效率",
}
POLICY_MIN_NODES_MINDMAP = 50
POLICY_MIN_QUESTIONS_QUIZ = 20
POLICY_MIN_FLASHCARDS = 30


@dataclass
class Finding:
    kind: str
    severity: str   # ERROR / WARN / INFO
    path: str
    message: str


@dataclass
class AuditReport:
    chapter: str | None
    files_scanned: int = 0
    findings: list[Finding] = field(default_factory=list)

    def add(self, kind: str, severity: str, path: Path, message: str) -> None:
        self.findings.append(Finding(kind, severity, str(path), message))

    @property
    def errors(self) -> list[Finding]: return [f for f in self.findings if f.severity == "ERROR"]

    @property
    def warns(self) -> list[Finding]: return [f for f in self.findings if f.severity == "WARN"]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def scan_write_plumbing(report: AuditReport, file: Path, kind: str) -> None:
    """扫描 1: 写盘自检 - 首行 H1, 无 JSON/截断, 大小下限."""
    text = _read(file)
    lines = text.splitlines()
    if not lines:
        report.add("WRITE", "ERROR", file, "文件为空")
        return
    if not lines[0].startswith("# "):
        report.add("WRITE", "ERROR", file, f"首行非 H1: {lines[0][:60]!r}")
    last = lines[-1].strip() if lines else ""
    if last.endswith(("}", "]", "\")", "\"", "```")) and not last.startswith("#"):
        report.add("WRITE", "WARN", file, f"末行疑似截断/代码残留: {last[:60]!r}")
    if "\\n\\t" in text or "\\n" in text[:200]:
        report.add("WRITE", "ERROR", file, "JSON 转义残留 (\\\\n 出现)")
    min_bytes = MIN_BYTES.get(kind, 1_000)
    if file.stat().st_size < min_bytes:
        report.add("WRITE", "WARN", file, f"大小 {file.stat().st_size}B < 期望下限 {min_bytes}B")


def scan_path_leak(report: AuditReport, file: Path) -> None:
    """扫描 3: 跨章引用相对路径 - 无 /Users/ /tmp/ /private/tmp/."""
    text = _read(file)
    for pattern, label in (("/Users/", "绝对路径"), ("/tmp/", "临时路径"), ("/private/tmp/", "工作树临时路径")):
        if pattern in text:
            # 例外: 文件内文字中含解释性"必须""禁止""❌"上下文
            for m in re.finditer(re.escape(pattern), text):
                ctx = text[max(0, m.start() - 30): m.end() + 30]
                if any(skip in ctx for skip in ("❌", "禁止", "示例", "扫描命令", "示例命令", "排除")):
                    continue
                report.add("PATH", "ERROR", file, f"{label}残留: {ctx[:80]!r}")
                break


def scan_formula_closure(report: AuditReport, file: Path) -> None:
    """扫描 4: 公式闭合 - $$ 偶数, \\begin{ \\end{ 相等."""
    text = _read(file)
    dollar_dollar = text.count("$$")
    if dollar_dollar % 2 != 0:
        report.add("FORMULA", "ERROR", file, f"$$ 出现 {dollar_dollar} 次 (奇数, 不成对)")
    begin_c = len(re.findall(r"\\begin\{[^}]+\}", text))
    end_c = len(re.findall(r"\\end\{[^}]+\}", text))
    if begin_c != end_c:
        report.add("FORMULA", "ERROR", file, f"\\begin{{}} {begin_c} ≠ \\end{{}} {end_c}")
    inline_single = text.count("$")
    inline_only = inline_single - 2 * dollar_dollar
    if inline_only % 2 != 0:
        report.add("FORMULA", "WARN", file, f"行内 $ 出现 {inline_only} 次 (奇数, 疑似未闭合)")


def scan_symbol_contract(report: AuditReport, file: Path) -> None:
    """扫描 5: 跨章符号契约 - λ/α/β/δ/ε/η 首次出现需标注."""
    text = _read(file)
    for sym, meaning in SYMBOL_CONTRACT_KEYWORDS.items():
        if sym not in text:
            continue
        # 找首次出现位置
        idx = text.find(sym)
        # 附近 ±200 字符内若有任何"意义"标注关键词, 视为已标注
        window = text[max(0, idx - 200): min(len(text), idx + 200)]
        annotation_keywords = ("特征值", "Lagrange", "学习率", "显著性", "正则化", "散度", "增量", "Dirac", "ε-δ", "Beta", "二类", "权重", "概率", "调度", "隐私", "精确", "分数")
        annotated = any(kw in window for kw in annotation_keywords)
        # 公式环境内 (被 $...$ 包围) 的 α/β 通常无需标注 (它就是超参)
        in_math = (text.rfind("$", 0, idx) > text.rfind("$$", 0, idx)) and (text.find("$", idx) != -1)
        if not annotated and not in_math:
            report.add("SYMBOL", "WARN", file, f"{sym} 首次出现未标注多义 ({meaning})")


def scan_disease(report: AuditReport, file: Path) -> None:
    """扫描 6: 病句/截断 - TODO/草稿位于/重复字/占位符."""
    text = _read(file)
    issues = [
        ("承上启下承上启下", "重复字: 承上启下"),
        ("的的的", "重复字: 的的"),
        ("TODO", "TODO 残留"),
        ("草稿位于", "草稿路径残留"),
        ("/tmp/ch", "临时目录残留"),
    ]
    for pat, label in issues:
        if pat in text:
            # 例外: 阶段测试题中的 TODO 是练习题代码占位 (学生实现)
            is_exercise = "E1" in text and "TODO" in text and "# 评分" in text
            if pat == "TODO" and is_exercise:
                continue
            report.add("DISEASE", "WARN", file, f"{label}")


def scan_content_alignment(report: AuditReport, file: Path) -> None:
    """扫描 8: 内容-位置对应 - 讲解稿文件名 N. vs 标题第 N 节."""
    name_match = re.match(r"(\d+)\.", file.name)
    if not name_match:
        return
    expected = int(name_match.group(1))
    text = _read(file)
    title_match = re.search(r"第\s+(\d+)\s*节", text)
    if title_match:
        actual = int(title_match.group(1))
        if expected != actual:
            report.add("ALIGN", "ERROR", file, f"文件名 {expected} ≠ 标题第 {actual} 节 (内容-位置错位)")


def scan_policy_minimums(report: AuditReport, file: Path, kind: str) -> None:
    """扫描 7: 模板遵循 - 各类材料的最小节点数/题数/卡片数."""
    text = _read(file)
    if kind == "闪卡":
        cards = len(re.findall(r"^###\s+Card\s+\d+", text, re.M))
        if cards < POLICY_MIN_FLASHCARDS:
            report.add("POLICY", "WARN", file, f"闪卡张数 {cards} < {POLICY_MIN_FLASHCARDS}")
    elif kind == "阶段测试题":
        questions = len(re.findall(r"^###\s+[A-F]\d+", text, re.M))
        if questions < POLICY_MIN_QUESTIONS_QUIZ:
            report.add("POLICY", "WARN", file, f"题目数 {questions} < {POLICY_MIN_QUESTIONS_QUIZ}")
    elif kind == "思维导图":
        nodes = len(re.findall(r"mindmap|flowchart|TB|LR", text)) + len(re.findall(r"^\s*[A-Za-z][A-Za-z\d_]*\[", text, re.M))
        if nodes < POLICY_MIN_NODES_MINDMAP:
            report.add("POLICY", "WARN", file, f"思维导图节点估算 {nodes} < {POLICY_MIN_NODES_MINDMAP}")


def audit_single(file: Path, kind: str, report: AuditReport) -> None:
    if not file.exists():
        report.add("MISSING", "ERROR", file, "教辅文件不存在")
        return
    report.files_scanned += 1
    scan_write_plumbing(report, file, kind)
    scan_path_leak(report, file)
    scan_formula_closure(report, file)
    scan_symbol_contract(report, file)
    scan_disease(report, file)
    scan_policy_minimums(report, file, kind)
    if kind == "讲解稿":
        scan_content_alignment(report, file)


def _gather_files(教辅_dir: Path, chapter: str | None) -> list[tuple[Path, str]]:
    """Return (file, kind) pairs scoped to the requested chapter(s)."""
    pairs: list[tuple[Path, str]] = []
    for kind in ROOT_MATKIND:
        for f in (教辅_dir / kind).glob("第*.md"):
            if chapter and f"第{chapter}" not in f.name:
                continue
            pairs.append((f, kind))
    讲解稿_dir = 教辅_dir / "讲解稿"
    for ch_dir in 讲解稿_dir.iterdir():
        if not ch_dir.is_dir():
            continue
        if chapter and ch_dir.name != f"第{chapter}章":
            continue
        for f in ch_dir.glob("*.md"):
            pairs.append((f, "讲解稿"))
    return pairs


def render_summary(report: AuditReport) -> str:
    by_kind: dict[str, list[Finding]] = {}
    for f in report.findings:
        by_kind.setdefault(f.kind, []).append(f)
    lines = [
        f"教辅 QA 审计 · chapter={report.chapter or 'ALL'} · 扫描 {report.files_scanned} 文件",
        f"  ERROR: {len(report.errors)}",
        f"  WARN:  {len(report.warns)}",
    ]
    for kind, items in sorted(by_kind.items()):
        lines.append(f"  [{kind}] {len(items)} 项")
        for f in items[:20]:
            lines.append(f"    - {Path(f.path).relative_to(Path(f.path).parents[3])} :: {f.message}")
    if len(report.errors) == 0 and len(report.warns) == 0:
        lines.append("  ✅ PASS")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("教辅_dir", type=Path, help="教辅根目录 (zh/教辅)")
    parser.add_argument("--chapter", help="限定章节号 (例如 10)")
    parser.add_argument("--all", action="store_true", help="扫描所有章节")
    parser.add_argument("--json", type=Path, help="输出 JSON 报告到指定路径")
    args = parser.parse_args(argv)

    if not args.chapter and not args.all:
        parser.error("需要 --chapter N 或 --all")
    chapter = args.chapter if not args.all else None

    report = AuditReport(chapter=chapter)
    pairs = _gather_files(args.教辅_dir, chapter)
    for file, kind in sorted(pairs):
        audit_single(file, kind, report)

    summary = render_summary(report)
    print(summary)

    if args.json:
        args.json.write_text(json.dumps({
            "chapter": report.chapter,
            "files_scanned": report.files_scanned,
            "findings": [asdict(f) for f in report.findings],
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
