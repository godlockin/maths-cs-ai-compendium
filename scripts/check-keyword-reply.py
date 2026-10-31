#!/usr/bin/env python3
"""
check-keyword-reply.py — 公众号「关键词自动回复」文案门禁

用法: python3 scripts/check-keyword-reply.py <txt> [<txt> ...]

规则 (来自 Ch01-Ch09 实战):
  1. 长度 ≤ 600 字符 (后台文本回复的可读性上限; 超出后手机端折叠严重)
  2. 必须是纯文本: 禁止 markdown 标记 (# / ** / ``` / ![](...))
  3. 公式只能用 Unicode (不得出现 \\frac / \\sum / $...$ LaTeX 语法)
  4. 必须含下一章引导句 "回复 \"NN\" ...下一章" (连载钩子)
  5. 卡片编号 1..N 连续 (【1】【2】... 不跳号)
"""
import re
import sys

MAX_CHARS = 600
MD_RE = re.compile(r"(#{1,6}\s|\*\*|```|!\[.*?\]\(|\[.+\]\(https?)")
LATEX_RE = re.compile(r"\\[a-zA-Z]+|\$[^\s$]")
CARD_RE = re.compile(r"【(\d+)】")
NEXT_HOOK_RE = re.compile(r"回复\s*[\"\"']?\s*\d{1,2}\s*[\"\"']?")


def check(path: str) -> list[str]:
    problems: list[str] = []
    text = open(path, encoding="utf-8").read()
    n = len(text)
    if n > MAX_CHARS:
        problems.append(f"{path}: {n} 字 > {MAX_CHARS} 上限 ({n - MAX_CHARS} 字超长)")
    for i, line in enumerate(text.splitlines(), 1):
        if MD_RE.search(line):
            problems.append(f"{path}:{i}: 含 markdown 标记, 关键词回复必须纯文本: {line[:60]}")
        if LATEX_RE.search(line):
            problems.append(f"{path}:{i}: 含 LaTeX 语法, 公式必须改 Unicode: {line[:60]}")
    nums = sorted(int(x) for x in CARD_RE.findall(text))
    if nums:
        expected = list(range(1, len(nums) + 1))
        if nums != expected:
            problems.append(f"{path}: 卡片编号不连续: {nums} (期望 {expected})")
        if not NEXT_HOOK_RE.search(text):
            problems.append(f"{path}: 缺下一章引导句 (形如 回复 \"10\" 预订下章闪卡)")
    else:
        problems.append(f"{path}: 未检出任何 【N】 卡片标记")
    return problems


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    allp: list[str] = []
    for p in sys.argv[1:]:
        allp.extend(check(p))
    if allp:
        print("\n".join(allp))
        return 1
    print(f"✓ keyword-reply 门禁通过 ({len(sys.argv) - 1} 份回复文案)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
