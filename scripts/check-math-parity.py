#!/usr/bin/env python3
"""Parity gate: report lines whose unescaped '$' count is odd.
Escaped currency ('\\$') is ignored. Code fences skipped.

用法: python3 scripts/check-math-parity.py <md> [<md> ...]
逐个文件检查, 全部通过才退出 0 (build-chapter.sh 传的是整目录通配符,
早期版本只取 argv[1] 导致只检查第一个文件, 已修)。
"""
import sys


def check(path: str) -> int:
    bad = 0
    in_code = False
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        n = 0
        j = 0
        while j < len(line):
            if line[j] == "\\" and j + 1 < len(line) and line[j + 1] == "$":
                j += 2
                continue
            if line[j] == "$":
                n += 1
            j += 1
        if n % 2 == 1:
            bad += 1
            if bad <= 5:
                print(f"{path}:{i}", line[:90].rstrip())
    print(f"{path}: odd-dollar lines: {bad}")
    return bad


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    total = 0
    for path in sys.argv[1:]:
        total += check(path)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
