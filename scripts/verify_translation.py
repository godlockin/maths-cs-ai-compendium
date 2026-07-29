from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    source_file: str
    target_file: str
    message: str


SUMMARY = re.compile(r"^> \*\*一句话总结\*\*:.*(?:\n>.*)*\n?", re.M)
NAV = re.compile(r"^## 🗺️ 本章导览\n(?:\n|[-*].*\n)+", re.M)
KEY_POINTS = re.compile(r"\n---\n\n## 📌 本节要点\n(?:\n|[-*].*\n)*$", re.M)
LABELLED_NOTE = re.compile(r"^> \*\*(?:补充说明|译注)\*\*:.*(?:\n>.*)*\n?", re.M)


# Kept as a separate operation so enhancement handling cannot accidentally remove
# ordinary translated prose or markdown structure.
def strip_enhancements(text: str) -> str:
    for pattern in (SUMMARY, NAV, KEY_POINTS, LABELLED_NOTE):
        text = pattern.sub("", text)
    return text


def markdown_files(directory: Path) -> list[Path]:
    return sorted(directory.glob("*.md"))


def map_files(source_dir: Path, target_dir: Path) -> list[tuple[Path, Path]]:
    source_files = markdown_files(source_dir)
    target_files = markdown_files(target_dir)
    if len(source_files) != len(target_files):
        raise ValueError(
            f"file count differs: source={len(source_files)} target={len(target_files)}"
        )
    return list(zip(source_files, target_files))


@dataclass(frozen=True)
class _Unit:
    kind: str
    value: str = ""


def _is_fence(line: str) -> bool:
    return bool(re.match(r"^\s*(```+|~~~+)", line))


def _flush_paragraph(units: list[_Unit], paragraph: list[str]) -> None:
    if paragraph:
        units.append(_Unit("prose", "\n".join(paragraph)))
        paragraph.clear()


def _unit_scan(text: str) -> list[_Unit]:
    lines = text.splitlines()
    units: list[_Unit] = []
    paragraph: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            _flush_paragraph(units, paragraph)
            index += 1
            continue
        fence = re.match(r"^\s*(```+|~~~+)(.*)$", line)
        if fence:
            _flush_paragraph(units, paragraph)
            marker, info = fence.groups()
            body = [line]
            index += 1
            while index < len(lines):
                body.append(lines[index])
                if re.match(r"^\s*" + re.escape(marker[0]) + r"{3,}\s*$", lines[index]):
                    index += 1
                    break
                index += 1
            units.append(_Unit("fence", "\n".join(body)))
            continue
        heading = re.match(r"^\s*(#{1,6})\s+", line)
        if heading:
            _flush_paragraph(units, paragraph)
            units.append(_Unit("heading", str(len(heading.group(1)))))
            index += 1
            continue
        formula = stripped == "$$" or stripped.startswith("$$")
        if formula:
            _flush_paragraph(units, paragraph)
            body = [line]
            if stripped != "$$" and stripped.endswith("$$"):
                index += 1
            else:
                index += 1
                while index < len(lines):
                    body.append(lines[index])
                    if lines[index].strip().endswith("$$"):
                        index += 1
                        break
                    index += 1
            units.append(_Unit("formula", "\n".join(body)))
            continue
        list_item = re.match(r"^(\s*)(?:[-*+] |\d+[.)] )", line)
        if list_item:
            _flush_paragraph(units, paragraph)
            units.append(_Unit("list", str(len(list_item.group(1).replace("\t", "    ")) // 2)))
            index += 1
            continue
        if re.match(r"^\s*>", line):
            _flush_paragraph(units, paragraph)
            units.append(_Unit("admonition"))
            index += 1
            continue
        if re.match(r"^\s*\|.*\|\s*$", line):
            _flush_paragraph(units, paragraph)
            units.append(_Unit("table"))
            index += 1
            continue
        links = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", line)
        if links:
            _flush_paragraph(units, paragraph)
            prose = re.sub(r"!?\[[^\]]*\]\(([^)]+)\)", "", line)
            if prose.strip():
                units.append(_Unit("prose", line))
            units.extend(_Unit("asset", url.strip()) for url in links)
            index += 1
            continue
        paragraph.append(line)
        index += 1
    _flush_paragraph(units, paragraph)
    return units


def _urls(text: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", text)]


def _math_blocks(text: str) -> list[str]:
    return re.findall(r"\$\$(?:.|\n)*?\$\$", text)


def _fenced_blocks(text: str) -> list[str]:
    return [unit.value for unit in _unit_scan(text) if unit.kind == "fence"]


def _code_equal(source: str, target: str) -> bool:
    source_lines = source.splitlines()
    target_lines = target.splitlines()
    if len(source_lines) != len(target_lines):
        return False
    for source_line, target_line in zip(source_lines, target_lines):
        # Only Python-style comments are ignorable; delimiters and code remain exact.
        source_code, source_hash, _ = source_line.partition("#")
        target_code, target_hash, _ = target_line.partition("#")
        if source_hash and target_hash:
            if source_code != target_code:
                return False
        elif source_line != target_line:
            return False
    return True


def _finding(rule: str, source: Path, target: Path, message: str) -> Finding:
    return Finding(rule, "P0", str(source), str(target), message)


def verify_file(source: Path, target: Path) -> list[Finding]:
    source_text = strip_enhancements(source.read_text(encoding="utf-8"))
    target_text = strip_enhancements(target.read_text(encoding="utf-8"))
    findings: list[Finding] = []

    source_math, target_math = _math_blocks(source_text), _math_blocks(target_text)
    if source_math != target_math:
        findings.append(_finding("P0-MATH", source, target, "ordered $$ blocks differ byte-for-byte"))

    source_code, target_code = _fenced_blocks(source_text), _fenced_blocks(target_text)
    if len(source_code) != len(target_code) or any(
        not _code_equal(left, right) for left, right in zip(source_code, target_code)
    ):
        findings.append(_finding("P0-CODE", source, target, "ordered fenced code blocks differ"))

    if _urls(source_text) != _urls(target_text):
        findings.append(_finding("P0-ASSET", source, target, "image or link URL sequence differs"))

    source_units, target_units = _unit_scan(source_text), _unit_scan(target_text)
    source_types = [unit.kind for unit in source_units]
    target_types = [unit.kind for unit in target_units]
    if source_types != target_types:
        findings.append(_finding("P0-SOURCE-COVERAGE", source, target, "source unit count/order/type cannot be matched"))

    source_structure = [(unit.kind, unit.value) for unit in source_units if unit.kind in {"heading", "list"}]
    target_structure = [(unit.kind, unit.value) for unit in target_units if unit.kind in {"heading", "list"}]
    if source_structure != target_structure:
        findings.append(_finding("P0-STRUCTURE", source, target, "heading level or list nesting sequence differs"))
    return findings


def verify_chapter(source_dir: Path, target_dir: Path, strict: bool = False) -> dict:
    findings: list[Finding] = []
    try:
        pairs = map_files(source_dir, target_dir)
    except ValueError as error:
        findings.append(Finding("P0-FILE-MAP", "P0", str(source_dir), str(target_dir), str(error)))
        return {"status": "FAIL", "findings": [asdict(f) for f in findings], "metrics": {}}
    for source, target in pairs:
        findings.extend(verify_file(source, target))
    blocked = any(f.severity == "P0" or (strict and f.severity == "P2") for f in findings)
    return {"status": "FAIL" if blocked else "PASS", "findings": [asdict(f) for f in findings], "metrics": {}}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify translated markdown structure")
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--target-dir", type=Path, required=True)
    parser.add_argument("--chapter")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--metrics-only", action="store_true")
    args = parser.parse_args(argv)
    source_dir = args.source_dir / args.chapter if args.chapter else args.source_dir
    target_dir = args.target_dir / args.chapter if args.chapter else args.target_dir
    report = verify_chapter(source_dir, target_dir, strict=args.strict)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
