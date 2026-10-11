#!/usr/bin/env python3
"""Join inline-math formulas broken across lines in jiaofu markdown files.

Rule: if a line ends with '$' (possibly followed by trailing whitespace) and
the count of '$' on that line is ODD, the trailing '$' opens an inline formula
whose body continues on the next line -> merge next line into this one.
Display-math '$$' lines have even counts and are left alone.
Index-based loop (no for/pointer divergence).
"""
import sys, glob

def fix_file(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    out, merged = [], 0
    i, n = 0, len(lines)
    in_code = False
    while i < n:
        line = lines[i]
        if line.lstrip().startswith("```"):
            in_code = not in_code
            out.append(line)
            i += 1
            continue
        if in_code:
            out.append(line)
            i += 1
            continue
        cur = line
        while (
            cur.rstrip().endswith("$")
            and cur.count("$") % 2 == 1
            and i + 1 < n
        ):
            nxt = lines[i + 1]
            if nxt.strip() == "$$" or nxt.lstrip().startswith(("#", "```")):
                break
            cur = cur.rstrip() + nxt
            merged += 1
            i += 1
        out.append(cur)
        i += 1
    if merged:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out))
    return merged

paths = sys.argv[1:] or sorted(glob.glob("zh/教辅/**/*.md", recursive=True))
total = 0
for p in paths:
    m = fix_file(p)
    if m:
        print(f"{p}: {m} joins")
    total += m
print(f"TOTAL merged joins: {total}")
