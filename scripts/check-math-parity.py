#!/usr/bin/env python3
"""Parity gate: report lines whose unescaped '$' count is odd.
Escaped currency ('\\$') is ignored. Code fences skipped."""
import sys

path = sys.argv[1]
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
            print(i, line[:90].rstrip())
print("odd-dollar lines:", bad)
sys.exit(1 if bad else 0)
