"""Normalise half-width punctuation and CJK/ASCII spacing across zh/**/*.md.

Behaviour: read each Chinese chapter file, apply transformations only to
prose characters (excluding fenced code, block/inline math, inline code,
image/link URLs), and print a unified diff. Original code, math, links, and
images are preserved verbatim. The script does not modify files unless
``--apply`` is passed.
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

REPLACEMENTS = [
    (re.compile(r"([一-鿿]),\s"), r"\1，"),
    (re.compile(r",\s*([一-鿿])"), r"，\1"),
    (re.compile(r"([一-鿿])\.(\s|$)"), r"\1。\2"),
    (re.compile(r"\.([一-鿿])"), r"。\1"),
    (re.compile(r"([一-鿿]):\s"), r"\1："),
    (re.compile(r":\s*([一-鿿])"), r"：\1"),
    (re.compile(r"([一-鿿]);\s"), r"\1；"),
    (re.compile(r";\s*([一-鿿])"), r"；\1"),
    (re.compile(r"([一-鿿])\?\s"), r"\1？"),
    (re.compile(r"\?([一-鿿])"), r"？\1"),
    (re.compile(r"([一-鿿])!\s"), r"\1！"),
    (re.compile(r"!([一-鿿])"), r"！\1"),
    (re.compile(r"([一-鿿])(\d)"), r"\1 \2"),
    (re.compile(r"(\d)([一-鿿])"), r"\1 \2"),
    (re.compile(r"([一-鿿])([A-Za-z])"), r"\1 \2"),
    (re.compile(r"([A-Za-z])([一-鿿])"), r"\1 \2"),
]

# Each placeholder is a unique sentinel unlikely to appear in prose.
PLACEHOLDER_PATTERN = re.compile(r"__PN_SENTINEL_(\d+)__")


def _is_prose_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if re.match(r"^\s*(```+|~~~+)", line):
        return False
    if stripped.startswith("$$"):
        return False
    return True


def _mask_protected(line: str, mask_state: dict[str, list[str]]) -> tuple[str, list[str]]:
    """Replace protected spans with sentinels, returning the masked line and
    the replacement tokens (in original order) so they can be restored after
    punctuation normalisation."""
    tokens: list[str] = []

    def stash(match: re.Match) -> str:
        token = match.group(0)
        tokens.append(token)
        index = len(tokens) - 1
        return f"__PN_SENTINEL_{index}__"

    masked = re.sub(r"```[\s\S]*?```", stash, line)
    masked = re.sub(r"`[^`\n]*`", stash, masked)
    masked = re.sub(r"\$\$[^$]*\$\$", stash, masked)
    masked = re.sub(r"\$[^$\n]*\$", stash, masked)
    masked = re.sub(r"!\[[^\]]*\]\([^)]*\)", stash, masked)
    masked = re.sub(r"\[[^\]]*\]\([^)]*\)", stash, masked)
    return masked, tokens


def _restore_placeholders(line: str, tokens: list[str]) -> str:
    def restore(match: re.Match) -> str:
        return tokens[int(match.group(1))]
    return PLACEHOLDER_PATTERN.sub(restore, line)


def _transform_line(line: str) -> str:
    masked, tokens = _mask_protected(line, {})
    for pattern, replacement in REPLACEMENTS:
        masked = pattern.sub(replacement, masked)
    return _restore_placeholders(masked, tokens)


def _transform(text: str) -> str:
    output: list[str] = []
    in_fence = False
    in_block_math = False
    for line in text.splitlines():
        stripped = line.strip()
        fence = re.match(r"^\s*(```+|~~~+)", line)
        if fence:
            in_fence = not in_fence
            output.append(line)
            continue
        if in_fence:
            output.append(line)
            continue
        if in_block_math:
            output.append(line)
            if "$$" in stripped:
                in_block_math = False
            continue
        if stripped.startswith("$$"):
            in_block_math = stripped.count("$$") < 2
            output.append(line)
            continue
        if not _is_prose_line(line):
            output.append(line)
            continue
        output.append(_transform_line(line))
    return "\n".join(output)


def _diff(original: str, updated: str) -> str:
    return "".join(difflib.unified_diff(
        original.splitlines(keepends=True),
        updated.splitlines(keepends=True),
        n=2,
    ))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="directories or files to scan")
    parser.add_argument("--apply", action="store_true", help="apply changes in place")
    args = parser.parse_args()
    total_changed = 0
    for root in args.paths:
        files = [root] if root.is_file() else sorted(root.rglob("*.md"))
        for path in files:
            original = path.read_text(encoding="utf-8")
            updated = _transform(original)
            if updated == original:
                continue
            total_changed += 1
            print(f"\n== {path} ==")
            print(_diff(original, updated)[:1500])
            if args.apply:
                path.write_text(updated, encoding="utf-8")
    print(f"\nFiles with changes: {total_changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())