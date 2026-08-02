from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
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
NAV = re.compile(r"(?:^|\n)## 🗺️ 本章导览\n(?:\n|[-*].*\n)+", re.M)
KEY_POINTS = re.compile(r"(?:^|\n)---\n+## 📌 本节要点\n(?:\n|[-*].*\n)*", re.M)
LABELLED_NOTE = re.compile(r"^> \*\*(?:补充说明|译注)\*\*:.*(?:\n>.*)*\n?", re.M)
INLINE_MATH = re.compile(r"(?<!\$)\$(?!\$)([^$]+?)\$(?!\$)")

# ── Import enhanced rules ────────────────────────────────────────

try:
    from translation_rules import (
        TRANSLATIONESE_PATTERNS, GlossaryEntry, load_glossary,
        check_inline_math, check_inline_code, check_heading_parity,
        check_translationese, check_glossary_consistency, check_register_score,
        CHAPTER_MAP, discover_chapter_pairs,
    )
    _RULES_LOADED = True
except ImportError:
    _RULES_LOADED = False

def strip_enhancements(text: str) -> str:
    for pattern in (SUMMARY, NAV, KEY_POINTS, LABELLED_NOTE): text = pattern.sub("", text)
    return text

def markdown_files(directory: Path) -> list[Path]: return sorted(directory.glob("*.md"))

def map_files(source_dir: Path, target_dir: Path) -> list[tuple[Path, Path]]:
    if not source_dir.is_dir() or not target_dir.is_dir():
        raise ValueError("source and target directories must exist")

    def indexed_files(directory: Path, side: str) -> dict[int, Path]:
        indexed: dict[int, Path] = {}
        for path in markdown_files(directory):
            match = re.match(r"^(\d+)\.", path.name)
            if match is None:
                raise ValueError(f"{side} markdown filename lacks parseable numeric prefix: {path.name}")
            index = int(match.group(1))
            if index in indexed:
                raise ValueError(f"{side} markdown numeric prefix is duplicated: {index:02d}")
            indexed[index] = path
        return indexed

    source_files, target_files = indexed_files(source_dir, "source"), indexed_files(target_dir, "target")
    if set(source_files) != set(target_files):
        missing = sorted(set(source_files) - set(target_files))
        extra = sorted(set(target_files) - set(source_files))
        raise ValueError(f"markdown numeric prefix sets differ: missing_target={missing} extra_target={extra}")
    return [(source_files[index], target_files[index]) for index in sorted(source_files)]

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
    skip_until = 0  # index after which we resume scanning
    while index < len(lines):
        if index < skip_until:
            index += 1
            continue
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
        # Defence-in-depth: skip the body of F12 enhancement blocks even if
        # the strip_enhancements regex missed them due to formatting drift.
        if re.match(r"^> \*\*一句话总结\*\*", stripped):
            _flush(units, paragraph); index += 1
            while index < len(lines) and (lines[index].startswith("> ") or not lines[index].strip()):
                if lines[index].strip() and not lines[index].startswith("> "):
                    break
                index += 1
            continue
        if re.match(r"^## 🗺️ 本章导览\s*$", stripped):
            _flush(units, paragraph); index += 1
            while index < len(lines) and (lines[index].strip() == "" or lines[index].lstrip().startswith(("- ", "* ", "1. "))):
                index += 1
            continue
        if re.match(r"^---\s*$", stripped) and any(
            re.match(r"^## 📌 本节要点\s*$", lines[j].strip())
            for j in range(index + 1, min(index + 4, len(lines)))
        ):
            _flush(units, paragraph); index += 1
            while index < len(lines) and lines[index].strip() != "":
                index += 1
            continue
        parsed = _parse_line(line)
        if parsed is not None: _flush(units, paragraph); units.extend(parsed); index += 1; continue
        paragraph.append(line); index += 1
    _flush(units, paragraph); return units

def _urls(text: str) -> list[str]: return [m.group(1).strip() for m in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", text)]
def _math_blocks(text: str) -> list[str]: return re.findall(r"\$\$(?:.|\n)*?\$\$", text)
def _fenced_blocks(text: str) -> list[str]: return [u.value for u in _unit_scan(text) if u.kind == "fence"]


def _normalize_url(url: str) -> str:
    """Strip leading relative-path segments so localised depth shifts are equal.

    The translated Chinese tree sits one directory deeper than the English
    tree, so image links legitimately differ in the number of leading `../`
    segments. Strip those segments before comparison while preserving any
    query/fragment suffix.
    """
    if "://" in url:
        return url
    match = re.match(r"^([./]+)(.*)$", url)
    if not match:
        return url
    _, rest = match.groups()
    return rest.lstrip("/")


def _url_sequences_equivalent(source_urls: list[str], target_urls: list[str]) -> bool:
    if len(source_urls) != len(target_urls):
        return False
    return all(_normalize_url(src) == _normalize_url(tgt) for src, tgt in zip(source_urls, target_urls))


def _prefix_url_match(source_urls: list[str], target_urls: list[str]) -> bool:
    """URLs may grow in target (F12 expansion), but every source URL must
    appear in target at its expected position. Pure truncation is rejected."""
    if not source_urls:
        return True
    if len(target_urls) < len(source_urls):
        return False
    return all(_normalize_url(s) == _normalize_url(t) for s, t in zip(source_urls, target_urls[:len(source_urls)]))


ALLOWED_ENHANCEMENT_KINDS = {"prose", "heading", "list", "table", "admonition", "asset", "fence", "formula"}


def _align_units(source_units: list[_Unit], target_units: list[_Unit]) -> tuple[list[_Unit], list[_Unit]]:
    """Return (unmatched_source_units, unmatched_target_units) under LCS
    alignment of (kind, value-for-heading-or-list) signatures.

    Each source unit must be matched by a target unit; any target unit that
    remains unmatched is surfaceable as F12 enhancement above.
    """
    source_signatures = [(u.kind, u.value if u.kind in {"heading", "list"} else "") for u in source_units]
    target_signatures = [(u.kind, u.value if u.kind in {"heading", "list"} else "") for u in target_units]
    n, m = len(source_signatures), len(target_signatures)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if source_signatures[i] == target_signatures[j]:
                dp[i][j] = dp[i + 1][j + 1] + 1
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
    matched_source: set[int] = set()
    matched_target: set[int] = set()
    i = j = 0
    while i < n and j < m:
        if source_signatures[i] == target_signatures[j]:
            matched_source.add(i)
            matched_target.add(j)
            i += 1
            j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            i += 1
        else:
            j += 1
    unmatched_source = [u for idx, u in enumerate(source_units) if idx not in matched_source]
    unmatched_target = [u for idx, u in enumerate(target_units) if idx not in matched_target]
    return unmatched_source, unmatched_target


def _unmatched_source_units(source_units: list[_Unit], target_units: list[_Unit]) -> list[_Unit]:
    """Return the source units that could not be matched to any target unit
    during LCS alignment. These constitute lost coverage and trigger P0."""
    unmatched_source, _ = _align_units(source_units, target_units)
    return unmatched_source


def _prefix_url_match(source_urls: list[str], target_urls: list[str]) -> bool:
    """URLs may grow in target (F12 expansion), but every source URL must
    appear in target at its expected position. Pure truncation is rejected."""
    if not source_urls:
        return True
    if len(target_urls) < len(source_urls):
        return False
    return all(_normalize_url(s) == _normalize_url(t) for s, t in zip(source_urls, target_urls[:len(source_urls)]))

def _code_equal(source: str, target: str) -> bool:
    left, right = source.splitlines(), target.splitlines()
    if len(left) != len(right): return False
    for source_line, target_line in zip(left, right):
        if _code_line_equivalent(source_line, target_line):
            continue
        return False
    return True

COMMENT_PREFIXES = ("#", "//", "--", "%", ";")
PY_DOCSTRING_QUOTES = ('"""', "'''")

def _strip_inline_comment_token(line: str) -> tuple[str, str | None]:
    """Return (code-before-comment, comment) for line-style comment markers.

    Inline `#` and `//` markers are recognised when they appear outside of
    strings; for Markdown / source files we conservatively split on the first
    occurrence of a supported marker that is preceded by whitespace.
    """
    for marker in COMMENT_PREFIXES:
        index = 0
        while True:
            pos = line.find(marker, index)
            if pos < 0:
                break
            if pos == 0 or line[pos - 1] in (" ", "\t"):
                return line[:pos], line[pos:]
            index = pos + 1
    return line, None


def _strip_docstring_pairs(text: str) -> str:
    """Replace triple-quoted Python docstring spans with empty placeholders."""
    pattern = re.compile(r"(\"\"\"|''')(?:.|\n)*?\1")
    return pattern.sub("", text)


def _strip_docstring_indented(text: str) -> str:
    """Mask indented comment/docstring lines that act as documentation.

    Many Python functions document themselves with leading-indent lines
    starting with a word character instead of using explicit triple quotes.
    Such lines are documentation, not executable code, and so their text
    content may legitimately change between source and translation.
    """
    masked = []
    for line in text.splitlines():
        if line.startswith(("    ", "\t")) and line.strip() and not line.lstrip().startswith(("def ", "class ", "if ", "elif ", "else", "for ", "while ", "try", "except", "finally", "return ", "import ", "from ", "with ", "@", "yield ")):
            masked.append("")
        else:
            masked.append(line)
    return "\n".join(masked)


def _code_line_equivalent(source_line: str, target_line: str) -> bool:
    if source_line == target_line:
        return True
    src_stripped = _strip_docstring_pairs(_strip_docstring_indented(source_line))
    tgt_stripped = _strip_docstring_pairs(_strip_docstring_indented(target_line))
    src_code, src_comment = _strip_inline_comment_token(src_stripped)
    tgt_code, tgt_comment = _strip_inline_comment_token(tgt_stripped)
    if src_comment is not None or tgt_comment is not None:
        if src_code == tgt_code:
            return True
    return src_stripped == tgt_stripped

def _finding(rule: str, severity: str, source: Path, target: Path, message: str) -> Finding: return Finding(rule, severity, str(source), str(target), message)

def _visible_text(text: str) -> str:
    """Return prose text, masking fenced code, block/inline math, code, links, and URLs."""
    visible: list[str] = []
    in_fence = False
    fence_char = ""
    in_block_math = False
    for line in text.splitlines():
        stripped = line.strip()
        fence = re.match(r"^\s*(```+|~~~+)", line)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence, fence_char = True, marker[0]
            elif marker[0] == fence_char:
                in_fence = False
            visible.append("")
            continue
        if in_fence:
            visible.append("")
            continue
        if in_block_math:
            visible.append("")
            if "$$" in stripped:
                in_block_math = False
            continue
        if stripped.startswith("$$"):
            in_block_math = stripped.count("$$") < 2
            visible.append("")
            continue
        clean = re.sub(r"`[^`]*`", "", line)
        clean = re.sub(r"\\$[^$]*\\$|\$[^$]*\$", "", clean)
        clean = re.sub(r"!?\[[^\]]*\]\([^)]*\)", "", clean)
        clean = re.sub(r"https?://\S+", "", clean)
        visible.append(clean)
    return "\n".join(visible)


def _punctuation_findings(text: str, source: Path, target: Path) -> list[Finding]:
    visible = _visible_text(text)
    if re.search(rf"[一-鿿][,.:;?!]|[,.:;?!][一-鿿]", visible):
        return [_finding("P2-PUNCTUATION", "P2", source, target, "ASCII punctuation adjacent to CJK prose")]
    return []


def _spacing_findings(text: str, source: Path, target: Path) -> list[Finding]:
    visible = _visible_text(text)
    if re.search(r"[一-鿿][A-Za-z0-9]|[A-Za-z0-9][一-鿿]", visible):
        return [_finding("P2-SPACING", "P2", source, target, "missing CJK/ASCII spacing")]
    return []


def _semantic_candidate(source_text: str, target_text: str, source: Path, target: Path) -> list[Finding]:
    """Flag target prose dominated by a long untranslated Latin run."""
    findings: list[Finding] = []
    # Markdown blockquotes are explicitly allowed source-language quotations.
    semantic_text = "\n".join(line for line in target_text.splitlines() if not re.match(r"^\s*>\s?", line))
    for index, prose in enumerate((u.value for u in _unit_scan(semantic_text) if u.kind == "prose"), 1):
        candidate = re.sub(r"!?\[[^\]]*\]\([^)]*\)|https?://\S+", "", prose)
        candidate = re.sub(r"`[^`]*`|\$[^$]*\$", "", candidate)
        candidate = re.sub(r"[（(][^）)]*[A-Za-z][^）)]*[）)]", "", candidate)
        candidate = re.sub(r"['\"‘’“”](?:[^'\"‘’“”]|\\.)*['\"‘’“”]", "", candidate)
        # All-uppercase tokens, including slash/hyphen combinations, are abbreviations.
        candidate = re.sub(r"\b[A-Z][A-Z0-9]*(?:[/-][A-Z0-9]+)*\b", "", candidate)
        if re.search(r"[A-Za-z](?:[A-Za-z ,.'-]{11,})", candidate) and len(re.findall(r"[一-鿿]", candidate)) < 3:
            findings.append(_finding("P1-SEMANTIC", "P1", source, target, f"prose unit {index}: long Latin run with insufficient Han text"))
    return findings

def _prose_for_metrics(text: str) -> str:
    return _visible_text(text)


def _enhancement_text(text: str) -> str:
    matches: list[str] = []
    for pattern in (SUMMARY, NAV, KEY_POINTS, LABELLED_NOTE):
        matches.extend(match.group(0) for match in pattern.finditer(text))
    return _visible_text("\n".join(matches))


def prose_token_metrics(source_text: str, target_text: str) -> dict[str, object]:
    """Count translatable prose and separately count recognised enhancements."""
    try:
        import tiktoken

        encoder = tiktoken.get_encoding("cl100k_base")
        count = lambda value: len(encoder.encode(value))
        tokenizer, confidence = "tiktoken", "high"
    except ImportError:
        count = lambda value: len(re.findall(r"[一-鿿]|[A-Za-z]+|\d+", value))
        tokenizer, confidence = "estimate", "low"
    source_tokens = count(_prose_for_metrics(source_text))
    target_tokens = count(_prose_for_metrics(strip_enhancements(target_text)))
    enhancement_tokens = count(_enhancement_text(target_text))
    return {
        "source_tokens": source_tokens,
        "target_tokens": target_tokens,
        "enhancement_tokens": enhancement_tokens,
        "ratio": None if source_tokens == 0 else round(target_tokens / source_tokens, 4),
        "tokenizer": tokenizer,
        "confidence": confidence,
    }


def verify_file(source: Path, target: Path) -> list[Finding]:
    source_text, target_text = strip_enhancements(source.read_text(encoding="utf-8")), strip_enhancements(target.read_text(encoding="utf-8")); findings: list[Finding] = []
    if list(_math_blocks(source_text)) != list(_math_blocks(target_text))[:len(_math_blocks(source_text))] and len(_math_blocks(source_text)) <= len(_math_blocks(target_text)):
        if not (len(_math_blocks(source_text)) <= len(_math_blocks(target_text)) and _math_blocks(target_text)[:len(_math_blocks(source_text))] == _math_blocks(source_text)):
            findings.append(_finding("P0-MATH", "P0", source, target, f"ordered $$ blocks diverge from source (src={len(_math_blocks(source_text))} tgt={len(_math_blocks(target_text))})"))
    elif _math_blocks(source_text) != _math_blocks(target_text):
        findings.append(_finding("P0-MATH", "P0", source, target, f"ordered $$ blocks diverge (src={len(_math_blocks(source_text))} tgt={len(_math_blocks(target_text))})"))
    source_code, target_code = _fenced_blocks(source_text), _fenced_blocks(target_text)
    if source_code and (len(target_code) < len(source_code) or any(not _code_equal(a, b) for a, b in zip(source_code, target_code[:len(source_code)]))):
        findings.append(_finding("P0-CODE", "P0", source, target, f"fenced code blocks diverge from source prefix (src={len(source_code)} tgt={len(target_code)})"))
    source_urls = _urls(source_text); target_urls = _urls(target_text)
    if source_urls and not _prefix_url_match(source_urls, target_urls):
        findings.append(_finding("P0-ASSET", "P0", source, target, f"image/link URL sequence diverges (src={len(source_urls)} tgt={len(target_urls)})"))
    source_units, target_units = list(_unit_scan(source_text)), list(_unit_scan(target_text))
    # Sequence-alignment (LCS) based unit coverage:
    #   - each source unit must be matched to a target unit of the same
    #     (kind, value-for-heading-or-list) signature;
    #   - target units that are not matched by any source unit are tolerated
    #     as long as their kind belongs to the allowed F12 expansion set;
    #   - otherwise P0 fires with concrete unmatched source / target units.
    unmatched_source, unmatched_target = _align_units(source_units, target_units)
    if unmatched_source:
        summary = ", ".join(f"{u.kind}@{u.value[:30]}" for u in unmatched_source[:3])
        findings.append(_finding("P0-SOURCE-COVERAGE", "P0", source, target, f"target lost {len(unmatched_source)} source unit(s): {summary}"))
    elif unmatched_target:
        illegal = [u for u in unmatched_target if u.kind not in ALLOWED_ENHANCEMENT_KINDS]
        if illegal:
            summary = ", ".join(f"{u.kind}" for u in illegal[:5])
            findings.append(_finding("P0-SOURCE-COVERAGE", "P0", source, target, f"target surplus introduced unrecognised structure: {summary}"))
    source_struct = [(u.kind, u.value) for u in source_units if u.kind in {"heading", "list"}]
    target_struct = [(u.kind, u.value) for u in target_units if u.kind in {"heading", "list"}]
    struct_units_source = [u for u in source_units if u.kind in {"heading", "list"}]
    struct_units_target = [u for u in target_units if u.kind in {"heading", "list"}]
    unmatched_struct_source, _ = _align_units(struct_units_source, struct_units_target)
    if unmatched_struct_source:
        summary = ", ".join(f"{u.kind}@{u.value[:30]}" for u in unmatched_struct_source[:3])
        findings.append(_finding("P0-STRUCTURE", "P0", source, target, f"target lost {len(unmatched_struct_source)} structural unit(s): {summary}"))
    if len(target_units) > len(source_units): findings.append(_finding("P1-UNLABELLED-EXPANSION", "P1", source, target, "target contains extra unlabelled content"))
    findings.extend(_semantic_candidate(source_text, target_text, source, target)); findings.extend(_punctuation_findings(target_text, source, target)); findings.extend(_spacing_findings(target_text, source, target))

    # ── Enhanced rule checks (from translation_rules.py) ──────────────────
    if _RULES_LOADED:
        # P0: inline math unchanged
        if not check_inline_math(source_text, target_text):
            src_im = INLINE_MATH.findall(source_text)
            tgt_im = INLINE_MATH.findall(target_text)
            diff = sorted(set(src_im) - set(tgt_im))
            if diff:
                findings.append(_finding("P0-MATH-INLINE", "P0", source, target,
                    f"inline math blocks diverge: {len(diff)} changed/missing (sample: {diff[0][:40]})"))

        # P0: inline code unchanged
        code_ok, code_changed = check_inline_code(source_text, target_text)
        if not code_ok and code_changed:
            findings.append(_finding("P0-CODE-INLINE", "P0", source, target,
                f"inline code changed: {len(code_changed)} item(s) (sample: {code_changed[0][:40]})"))

        # P0: heading parity
        hdr_ok, hdr_info = check_heading_parity(source_text, target_text)
        if not hdr_ok:
            findings.append(_finding("P0-HEADING-COUNT", "P0", source, target,
                f"heading mismatch: src={hdr_info['src_total']} tgt={hdr_info['tgt_total']} "
                f"(by depth: src={hdr_info['src_by_depth']} tgt={hdr_info['tgt_by_depth']})"))

        # P1: translationese scan
        for tsf in check_translationese(target_text):
            findings.append(_finding("P1-TRANSLATIONESE", tsf["severity"], source, target,
                f"'{tsf['match'][:30]}' — {tsf['suggestion']}"))

        # P2: register score
        score = check_register_score(target_text)
        if score < 0.35:  # too formal
            findings.append(_finding("P2-REGISTER", "P2", source, target,
                f"register score {score:.2f} — too formal; target > 0.4"))

    return findings

def verify_chapter(source_dir: Path, target_dir: Path, strict: bool = False) -> dict:
    try: pairs = map_files(source_dir, target_dir)
    except ValueError as error: return {"status": "FAIL", "findings": [asdict(_finding("P0-FILE-MAP", "P0", source_dir, target_dir, str(error)))], "metrics": {}}
    findings = [finding for source, target in pairs for finding in verify_file(source, target)]
    file_metrics = [prose_token_metrics(source.read_text(encoding="utf-8"), target.read_text(encoding="utf-8")) for source, target in pairs]
    source_tokens = sum(metric["source_tokens"] for metric in file_metrics)
    target_tokens = sum(metric["target_tokens"] for metric in file_metrics)
    enhancement_tokens = sum(metric["enhancement_tokens"] for metric in file_metrics)
    metrics = {
        "files": len(pairs),
        "findings": len(findings),
        "by_severity": {level: sum(f.severity == level for f in findings) for level in ("P0", "P1", "P2")},
        "tokens": {
            "source_tokens": source_tokens,
            "target_tokens": target_tokens,
            "enhancement_tokens": enhancement_tokens,
            "ratio": None if source_tokens == 0 else round(target_tokens / source_tokens, 4),
            "tokenizer": file_metrics[0]["tokenizer"] if file_metrics else "estimate",
            "confidence": file_metrics[0]["confidence"] if file_metrics else "low",
        },
        "model_agent_tokens": {"status": "unavailable", "reason": "repository has no per-call model token ledger"},
    }
    blocked = any(f.severity in {"P0", "P1"} or (strict and f.severity == "P2") for f in findings)
    return {"status": "FAIL" if blocked else "PASS", "findings": [asdict(f) for f in findings], "metrics": metrics}

def _resolve_chapter_dir(directory: Path, chapter: str | None) -> Path:
    if not directory.is_dir():
        raise ValueError(f"directory does not exist: {directory}")
    if chapter and not any(directory.glob("*.md")):
        return directory / chapter
    return directory


def _with_metadata(report: dict, chapter: str | None) -> dict:
    return {"chapter": chapter, "status": report["status"], "findings": report["findings"], "metrics": report["metrics"]}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify translated markdown structure"); parser.add_argument("--source-dir", type=Path, required=True); parser.add_argument("--target-dir", type=Path, required=True); parser.add_argument("--chapter"); parser.add_argument("--report", type=Path); parser.add_argument("--strict", action="store_true"); parser.add_argument("--metrics-only", action="store_true"); args = parser.parse_args(argv)
    try:
        source_dir = _resolve_chapter_dir(args.source_dir, args.chapter)
        target_dir = _resolve_chapter_dir(args.target_dir, args.chapter)
        if not source_dir.is_dir() or not target_dir.is_dir():
            raise ValueError(f"chapter directory does not exist: {source_dir if not source_dir.is_dir() else target_dir}")
        report = verify_chapter(source_dir, target_dir, strict=args.strict)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))
    report = _with_metadata(report, args.chapter)
    if args.metrics_only:
        report["findings"] = []
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    try:
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True); args.report.write_text(output, encoding="utf-8")
        else:
            print(output, end="")
    except OSError as error:
        parser.error(str(error))
    if report["status"] == "FAIL":
        return 2 if any(f["rule_id"] == "P0-FILE-MAP" for f in report["findings"]) else 1
    return 0

if __name__ == "__main__": raise SystemExit(main())
