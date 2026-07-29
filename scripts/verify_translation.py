from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Sequence

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

def strip_enhancements(text: str) -> str:
    for pattern in (SUMMARY, NAV, KEY_POINTS, LABELLED_NOTE): text = pattern.sub("", text)
    return text

def markdown_files(directory: Path) -> list[Path]: return sorted(directory.glob("*.md"))

def map_files(source_dir: Path, target_dir: Path) -> list[tuple[Path, Path]]:
    if not source_dir.is_dir() or not target_dir.is_dir(): raise ValueError("source and target directories must exist")
    source_files, target_files = markdown_files(source_dir), markdown_files(target_dir)
    if len(source_files) != len(target_files): raise ValueError(f"file count differs: source={len(source_files)} target={len(target_files)}")
    if [p.name for p in source_files] != [p.name for p in target_files]: raise ValueError("source and target markdown filename mapping differs")
    return list(zip(source_files, target_files))

@dataclass(frozen=True)
class _Unit:
    kind: str
    value: str = ""

def _flush(units: list[_Unit], paragraph: list[str]) -> None:
    if paragraph: units.append(_Unit("prose", "\n".join(paragraph))); paragraph.clear()

def _line_structure(line: str) -> tuple[str, str, str] | None:
    item = re.match(r"^(\s*)(?:[-*+] |\d+[.)] )(.*)$", line)
    if item:
        indent, body = item.groups(); return "list", str(len(indent.replace("\t", "    ")) // 2), body
    quote = re.match(r"^\s*>\s?(.*)$", line)
    if quote: return "admonition", "", quote.group(1)
    if re.match(r"^\s*\|.*\|\s*$", line): return "table", "", line.strip()[1:-1]
    return None

def _normalized_prose(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"!?\[[^\]]*\]\(([^)]+)\)", "", text)).strip()

def _parse_line(line: str) -> list[_Unit] | None:
    links = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", line); structure = _line_structure(line)
    if not links and structure is None: return None
    units: list[_Unit] = []; prose = line
    if structure:
        kind, metadata, prose = structure; units.append(_Unit(kind, metadata))
    normalized = _normalized_prose(prose)
    if normalized: units.append(_Unit("prose", normalized))
    units.extend(_Unit("asset", url.strip()) for url in links); return units

def _unit_scan(text: str) -> list[_Unit]:
    lines, units, paragraph = text.splitlines(), [], []; index = 0
    while index < len(lines):
        line, stripped = lines[index], lines[index].strip()
        if not stripped: _flush(units, paragraph); index += 1; continue
        fence = re.match(r"^\s*(```+|~~~+)(.*)$", line)
        if fence:
            _flush(units, paragraph); marker, _ = fence.groups(); body = [line]; index += 1
            while index < len(lines):
                body.append(lines[index])
                if re.match(r"^\s*" + re.escape(marker[0]) + r"{3,}\s*$", lines[index]): index += 1; break
                index += 1
            units.append(_Unit("fence", "\n".join(body))); continue
        heading = re.match(r"^\s*(#{1,6})\s+", line)
        if heading: _flush(units, paragraph); units.append(_Unit("heading", str(len(heading.group(1))))); index += 1; continue
        if stripped == "$$" or stripped.startswith("$$"):
            _flush(units, paragraph); body = [line]; index += 1
            if not (stripped != "$$" and stripped.endswith("$$")):
                while index < len(lines):
                    body.append(lines[index])
                    if lines[index].strip().endswith("$$"): index += 1; break
                    index += 1
            units.append(_Unit("formula", "\n".join(body))); continue
        parsed = _parse_line(line)
        if parsed is not None: _flush(units, paragraph); units.extend(parsed); index += 1; continue
        paragraph.append(line); index += 1
    _flush(units, paragraph); return units

def _urls(text: str) -> list[str]: return [m.group(1).strip() for m in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", text)]
def _math_blocks(text: str) -> list[str]: return re.findall(r"\$\$(?:.|\n)*?\$\$", text)
def _fenced_blocks(text: str) -> list[str]: return [u.value for u in _unit_scan(text) if u.kind == "fence"]

def _code_equal(source: str, target: str) -> bool:
    left, right = source.splitlines(), target.splitlines()
    if len(left) != len(right): return False
    for source_line, target_line in zip(left, right):
        source_code, source_hash, _ = source_line.partition("#"); target_code, target_hash, _ = target_line.partition("#")
        if source_hash and target_hash:
            if source_code != target_code: return False
        elif source_line != target_line: return False
    return True

def _finding(rule: str, severity: str, source: Path, target: Path, message: str) -> Finding: return Finding(rule, severity, str(source), str(target), message)

def _protected_line(line: str) -> str:
    line = re.sub(r"`[^`]*`", "", line); line = re.sub(r"!?\[[^\]]*\]\([^)]+\)", "", line); return re.sub(r"https?://\S+", "", line)

def _punctuation_findings(text: str, source: Path, target: Path) -> list[Finding]:
    for number, line in enumerate(text.splitlines(), 1):
        if re.match(r"^\s*(?:```|~~~|\$\$)", line): continue
        if re.search(r"[一-鿿][,!?;:]|[,!?;:][一-鿿]", _protected_line(line)):
            return [_finding("P2-PUNCTUATION", "P2", source, target, f"line {number}: ASCII punctuation adjacent to CJK prose")]
    return []

def _spacing_findings(text: str, source: Path, target: Path) -> list[Finding]:
    for number, line in enumerate(text.splitlines(), 1):
        if re.match(r"^\s*(?:```|~~~|\$\$)", line): continue
        clean = _protected_line(line)
        for word in re.findall(r"[A-Za-z][A-Za-z0-9+.#-]{2,}", clean):
            if word.isupper() or re.fullmatch(r"[A-Za-z]{1,3}\d+", word): continue
            if re.search(rf"[一-鿿]{re.escape(word)}|{re.escape(word)}[一-鿿]", clean):
                return [_finding("P2-SPACING", "P2", source, target, f"line {number}: missing CJK/Latin word spacing")]
    return []

def _semantic_candidate(source_text: str, target_text: str, source: Path, target: Path) -> list[Finding]:
    source_prose = [u.value for u in _unit_scan(source_text) if u.kind == "prose"]; target_prose = [u.value for u in _unit_scan(target_text) if u.kind == "prose"]; findings = []
    for index, (left, right) in enumerate(zip(source_prose, target_prose), 1):
        latin_left, latin_right = re.findall(r"[A-Za-z]{3,}", left.lower()), re.findall(r"[A-Za-z]{3,}", right.lower())
        if len(latin_left) >= 4 and len(latin_right) >= 4:
            score = SequenceMatcher(None, " ".join(latin_left), " ".join(latin_right)).ratio()
            if score < 0.25: findings.append(_finding("P1-SEMANTIC", "P1", source, target, f"prose unit {index}: low lexical similarity candidate ({score:.2f})"))
    return findings

def verify_file(source: Path, target: Path) -> list[Finding]:
    source_text, target_text = strip_enhancements(source.read_text(encoding="utf-8")), strip_enhancements(target.read_text(encoding="utf-8")); findings: list[Finding] = []
    if _math_blocks(source_text) != _math_blocks(target_text): findings.append(_finding("P0-MATH", "P0", source, target, "ordered $$ blocks differ byte-for-byte"))
    source_code, target_code = _fenced_blocks(source_text), _fenced_blocks(target_text)
    if len(source_code) != len(target_code) or any(not _code_equal(a, b) for a, b in zip(source_code, target_code)): findings.append(_finding("P0-CODE", "P0", source, target, "ordered fenced code blocks differ"))
    if _urls(source_text) != _urls(target_text): findings.append(_finding("P0-ASSET", "P0", source, target, "image or link URL sequence differs"))
    source_units, target_units = _unit_scan(source_text), _unit_scan(target_text)
    if [u.kind for u in source_units] != [u.kind for u in target_units]: findings.append(_finding("P0-SOURCE-COVERAGE", "P0", source, target, "source unit count/order/type cannot be matched"))
    if [(u.kind, u.value) for u in source_units if u.kind in {"heading", "list"}] != [(u.kind, u.value) for u in target_units if u.kind in {"heading", "list"}]: findings.append(_finding("P0-STRUCTURE", "P0", source, target, "heading level or list nesting sequence differs"))
    if len(target_units) > len(source_units): findings.append(_finding("P1-UNLABELLED-EXPANSION", "P1", source, target, "target contains extra unlabelled content"))
    findings.extend(_semantic_candidate(source_text, target_text, source, target)); findings.extend(_punctuation_findings(target_text, source, target)); findings.extend(_spacing_findings(target_text, source, target)); return findings

def verify_chapter(source_dir: Path, target_dir: Path, strict: bool = False) -> dict:
    try: pairs = map_files(source_dir, target_dir)
    except ValueError as error: return {"status": "FAIL", "findings": [asdict(_finding("P0-FILE-MAP", "P0", source_dir, target_dir, str(error)))], "metrics": {}}
    findings = [finding for source, target in pairs for finding in verify_file(source, target)]
    metrics = {"files": len(pairs), "findings": len(findings), "by_severity": {level: sum(f.severity == level for f in findings) for level in ("P0", "P1", "P2")}}
    blocked = any(f.severity in {"P0", "P1"} or (strict and f.severity == "P2") for f in findings)
    return {"status": "FAIL" if blocked else "PASS", "findings": [asdict(f) for f in findings], "metrics": metrics}

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify translated markdown structure"); parser.add_argument("--source-dir", type=Path, required=True); parser.add_argument("--target-dir", type=Path, required=True); parser.add_argument("--chapter"); parser.add_argument("--report", type=Path); parser.add_argument("--strict", action="store_true"); parser.add_argument("--metrics-only", action="store_true"); args = parser.parse_args(argv)
    source_dir, target_dir = (args.source_dir / args.chapter if args.chapter else args.source_dir), (args.target_dir / args.chapter if args.chapter else args.target_dir)
    try: report = verify_chapter(source_dir, target_dir, strict=args.strict)
    except (OSError, UnicodeError, ValueError) as error: parser.error(str(error))
    if report["findings"] and report["findings"][0]["rule_id"] == "P0-FILE-MAP":
        output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.report:
            try:
                args.report.parent.mkdir(parents=True, exist_ok=True); args.report.write_text(output, encoding="utf-8")
            except OSError as error: parser.error(str(error))
        else: print(output, end="")
        return 2
    if args.metrics_only: report = {"status": report["status"], "metrics": report["metrics"]}
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    try:
        if args.report: args.report.parent.mkdir(parents=True, exist_ok=True); args.report.write_text(output, encoding="utf-8")
        else: print(output, end="")
    except OSError as error: parser.error(str(error))
    return 1 if report["status"] == "FAIL" else 0

if __name__ == "__main__": raise SystemExit(main())
