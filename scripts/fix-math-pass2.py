#!/usr/bin/env python3
"""Pass 2: character-stream repair — remove newlines that sit inside an
unclosed inline formula. '$' toggles math state; '\$' escaped; ``` toggles
code blocks (newlines preserved there). '$$' toggles twice (display), so
newlines inside display blocks stay untouched."""
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    lines = f.read().split("\n")

out, joined = [], 0
in_code = False
buf = ""
in_math = False
for line in lines:
    if line.lstrip().startswith("```"):
        # flush any dangling math state conservatively (shouldn't happen)
        in_code = not in_code
        out.append(buf + line)
        buf, in_math = "", False
        continue
    j = 0
    while j < len(line):
        ch = line[j]
        if ch == "\\" and j + 1 < len(line) and line[j + 1] == "$":
            buf += "\\$"
            j += 2
            continue
        if ch == "$":
            in_math = not in_math
            buf += ch
            j += 1
            continue
        buf += ch
        j += 1
    if in_math:
        # formula continues on next line -> swallow the newline
        joined += 1
        continue
    out.append(buf)
    buf = ""

if buf:
    out.append(buf)

with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"{path}: {joined} newline joins inside math")
