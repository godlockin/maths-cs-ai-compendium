#!/usr/bin/env python3
"""扫教辅中 mermaid 块的可疑模式"""
import re
from pathlib import Path

def check_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        c = f.read()
    blocks = re.findall(r'```mermaid\n(.*?)\n```', c, re.DOTALL)
    issues = []
    for i, b in enumerate(blocks):
        if re.search(r'::', b):
            issues.append(f'块{i+1}: :: 语法 (Mermaid 11+)')
        # 中文括号
        if re.search(r'[（()].+?[）)]', b):
            issues.append(f'块{i+1}: 中文括号')
        # 双引号配对
        quotes = b.count('"')
        if quotes % 2:
            issues.append(f'块{i+1}: 引号不配对 ({quotes} 个)')
    return issues

base = Path("zh/教辅")
for f in sorted(base.rglob("*.md")):
    issues = check_file(f)
    if issues:
        print(f"{f}:")
        for x in issues[:3]:
            print(f"  {x}")
