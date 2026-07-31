#!/usr/bin/env python3
"""
v2 改进版: Mermaid mindmap → ASCII 树状图
- 根节点用章节真实名
- 用 last-child 风格分支符 (├─ / └─)
- 干净缩进, 无累积 │
"""
import re
from pathlib import Path


def parse_mermaid(content: str):
    """提取 mermaid mindmap 块中的节点,返回层级树"""
    pattern = re.compile(r'```mermaid\s*\nmindmap\s*\n(.*?)\n```', re.DOTALL)
    match = pattern.search(content)
    if not match:
        return None, None
    block = match.group(1)

    # 找 root 节点
    root_match = re.search(r'root\s*\(\(\s*(.+?)\s*<br/?>(.+?)\s*\)\)', block)
    if not root_match:
        # 简化 root
        root_match = re.search(r'root\s*\(\(\s*(.+?)\s*\)\)', block)
    if root_match:
        root_text = re.sub(r'<br\s*/?>', ' / ', root_match.group(1) + ' ' + (root_match.group(2) if root_match.lastindex >= 2 else '')).strip()
    else:
        root_text = "Chapter"

    # 解析所有节点
    items = []  # (indent, text)
    lines = block.split('\n')
    started = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if 'root' in stripped and 'root(((' not in stripped:
            started = True
            continue
        if not started:
            continue
        if stripped == 'mindmap':
            continue

        indent = (len(line) - len(line.lstrip())) // 2
        # 清理文本
        text = re.sub(r'\[.*?\]', '', stripped)  # 移除 [id]
        text = re.sub(r'\(.*?\)\s*$', '', text)  # 移除末尾 ()
        # 处理 (((text))) 包裹
        text = re.sub(r'^\(+\(+\s*', '', text)
        text = re.sub(r'\s*\)+\)+$', '', text)
        text = re.sub(r'<br\s*/?>', ' / ', text)
        # 清理 emoji 后残留
        text = re.sub(r'\s*🟢\s*$', ' 🟢', text)
        text = re.sub(r'\s*🟡\s*$', ' 🟡', text)
        text = re.sub(r'\s*🔴\s*$', ' 🔴', text)
        text = re.sub(r'\s*⭐\s*$', ' ⭐', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if text and text not in ('mindmap', 'root'):
            items.append((indent, text))

    return root_text, items


def indent_to_tree(root_text, items):
    """把 (indent, text) 列表转为 ASCII 树"""
    if not items:
        return f"🌳 {root_text}\n(无子节点)"

    lines = [f"🌳 {root_text}"]
    # 按层级组织
    prev_indent = items[0][0]

    # 用栈追踪每个层级的"是否最后一个"
    stack = []  # 栈: 每层剩余兄弟数

    for i, (indent, text) in enumerate(items):
        # 找本层后续兄弟数
        siblings_after = 0
        for j in range(i + 1, len(items)):
            if items[j][0] == indent:
                siblings_after += 1
            elif items[j][0] < indent:
                break
        is_last = (siblings_after == 0)

        # 计算前缀
        if indent == 0 or indent == items[0][0]:
            # 一级子
            prefix = "└─ " if is_last else "├─ "
        else:
            # 深层: 上层是 last → 缩进 4 空格, 否则 │  + 4 空格
            parts = []
            for d in range(indent - 1, 0, -1):
                # 这层是 last?
                if d < len(stack) and stack[d] == 0:
                    parts.append("    ")
                else:
                    parts.append("│   ")
            parts.reverse()
            parts.append("└─ " if is_last else "├─ ")
            prefix = "".join(parts)

        # 更新栈
        while len(stack) < indent:
            stack.append(0)
        if indent > 0:
            stack[indent] = siblings_after

        lines.append(f"{prefix}{text}")

    return '\n'.join(lines)


def convert_file(filepath: Path) -> bool:
    content = filepath.read_text(encoding='utf-8')
    pattern = re.compile(r'```mermaid\s*\nmindmap\s*\n(.*?)\n```', re.DOTALL)
    matches = list(pattern.finditer(content))
    if not matches:
        return False

    new_content = content
    for match in reversed(matches):
        block = match.group(1)
        # 找 root
        root_match = re.search(r'root\s*\(\(\s*(.+?)\s*<br/?>(.+?)\s*\)\)', block)
        if not root_match:
            root_match = re.search(r'root\s*\(\(\s*(.+?)\s*\)\)', block)
        if root_match:
            root_text = root_match.group(1).strip() + " " + (root_match.group(2).strip() if root_match.lastindex >= 2 else "")
            root_text = re.sub(r'\s+', ' ', root_text).strip()
        else:
            # 从文件名猜章节
            root_text = filepath.stem.replace('第', '第 ').replace('章', ' 章')

        # 解析节点
        items = []
        lines = block.split('\n')
        started = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if 'root' in stripped and started is False:
                started = True
                continue
            if not started:
                continue
            if stripped == 'mindmap':
                continue
            indent = (len(line) - len(line.lstrip())) // 2
            text = re.sub(r'\[.*?\]', '', stripped)
            text = re.sub(r'\(.*?\)\s*$', '', text)
            text = re.sub(r'^\(+\(+\s*', '', text)
            text = re.sub(r'\s*\)+\)+$', '', text)
            text = re.sub(r'<br\s*/?>', ' / ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            if text and text not in ('mindmap', 'root'):
                items.append((indent, text))

        tree = indent_to_tree(root_text, items)
        replacement = f"```\n{tree}\n```"
        new_content = new_content[:match.start()] + replacement + new_content[match.end():]

    filepath.write_text(new_content, encoding='utf-8')
    return True


def main():
    base = Path("zh/教辅/思维导图")
    files = sorted(base.glob("第*.md"))
    print(f"扫描 {len(files)} 个思维导图\n")

    converted = 0
    for f in files:
        if convert_file(f):
            print(f"✓ {f.name}")
            converted += 1

    print(f"\n✅ 转换 {converted} 个文件")


if __name__ == "__main__":
    main()
