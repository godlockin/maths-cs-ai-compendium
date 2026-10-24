#!/usr/bin/env python3
"""
check-publish-hygiene.py — 发布卫生门禁 (build 前自动跑, 失败即挡)

覆盖 2026-10 实战踩过的三类"靠记住会忘"的错误:
1. 控制字符 (\x07 bell 曾把 $\alpha 吃成 $lpha)
2. 编辑过程语泄漏 ("原增补称…已删"/"尚待核实"/"未直接核到" 等核查口吻进入发布文本)
3. 内部标记残留 (<!-- FIX / %% FIX / {{ 占位符 / __SENTINEL__)
4. 测试卷分值自检 (题型 分数×题数 之和 = 总分; 4×7=14 曾两轮审校漏网)

用法: python3 scripts/check-publish-hygiene.py <md>...
退出码: 0 = 干净; 1 = 有命中 (打印 文件:行号)
"""
import re
import sys

CONTROL_RE = re.compile(r'[\x00-\x08\x0b-\x1f\x7f]')  # 排除 \t(09) \n(0a)
PROCESS_LANG = re.compile(
    r'原增补|尚待核实|未直接核到|采信前|查无此模型|不确\)|已删。|核过但未写入'
)
MARKER_RE = re.compile(r'<!--\s*FIX|%%\s*FIX|__SENTINEL__|\{\{|TODO:?\s*发布前')
# 价格假公式: "$10/$50" 这类裸美元价格能通过奇偶门禁但会配对成垃圾公式 (Ch07 §05 事故)
# 要求 / 后紧跟 $ (即 $N/$M 形态); 数学分数 $1/8$ 不误报 (Ch08 §05 误报回填)
PRICE_RE = re.compile(r'(?<![\\\w])\$\d[\d.,]*/\s*\$')
# 测试卷: 题型行 "选择题 10 题（30 分）" 与节标题 "一、选择题（10 × 3 = 30 分）"
SCORE_ITEM = re.compile(r'([一二三四五六]、[^（(]*?)（?\(?(\d+)\s*[×x]\s*(\d+)\s*=\s*(\d+)\s*分')
SCORE_HEADER = re.compile(r'(\S+?)\s*(\d+)\s*题[（(]\s*(\d+)\s*分[）)]')
# 尾部总分声明: "**总评**: 100 分" / "**总分：100 分**" (半角或全角冒号)
TOTAL_SCORE = re.compile(r'\*\*(?:总分|总评)\*\*\s*[:：]?\s*(\d+)\s*分')
# "**分布**: 选择 10×3 + 填空 5×4 + ... = 30+20+30+20 = 100, 共 25 题" — 取最后一个 "=" 后的数
TOTAL_DIST = re.compile(r'\*\*分布\*\*[^\n]*?=\s*(\d+)\s*[,，]?\s*共')
# 分布行里的 "N×M" 分项
DIST_PAIR = re.compile(r'(\d+)\s*[×x]\s*(\d+)')


def check_file(path: str) -> list[str]:
    problems = []
    text = open(path, encoding='utf-8', errors='replace').read()
    in_fence = False
    for i, line in enumerate(text.split('\n'), 1):
        # 代码围栏内的 {{ (python f-string 转义) 与 $ 价格属合法内容, 跳过这两类检查
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
        if CONTROL_RE.search(line):
            problems.append(f'{path}:{i} 控制字符: {line[:60]!r}')
        if PROCESS_LANG.search(line):
            problems.append(f'{path}:{i} 编辑过程语泄漏: {line.strip()[:80]}')
        if not in_fence:
            if MARKER_RE.search(line):
                problems.append(f'{path}:{i} 内部标记残留: {line.strip()[:80]}')
            if PRICE_RE.search(line):
                problems.append(f'{path}:{i} 裸美元价格 (需 \\$ 转义): {line.strip()[:80]}')
    # 分值自检 (仅当文件像测试卷: 含 "总分/总评" 且含题型行)
    if '总分' in text or '总评' in text:
        claimed = {}   # 题型名 -> 声明分
        computed = {}  # 题型名 -> 题数×每题分
        for m in SCORE_HEADER.finditer(text):
            name, n, score = m.group(1), int(m.group(2)), int(m.group(3))
            claimed.setdefault(name, 0)
            claimed[name] += score
        for m in SCORE_ITEM.finditer(text):
            name, n, per, total = m.group(1).strip(), int(m.group(2)), int(m.group(3)), int(m.group(4))
            if n * per != total:
                problems.append(f'{path} 分值算术错: "{name}" {n}×{per}={n*per} ≠ 标称 {total}')
            computed[name] = n * per
        # 尾部声明的总分: "**总评**: 100 分" 或 "**分布**: ... = 30+20+30+20 = 100, 共 25 题"
        claims = []
        for m in TOTAL_SCORE.finditer(text):
            claims.append((int(m.group(1)), m.group(0)))
        for m in TOTAL_DIST.finditer(text):
            claims.append((int(m.group(1)), m.group(0)))
        for claimed_total, raw in claims:
            if computed:
                s_comp = sum(computed.values())
                if s_comp != claimed_total:
                    problems.append(
                        f'{path} 总分对不上: 尾部声明 {claimed_total} 分 vs 题型节标题合计 {s_comp} 分')
            # 分布行里的 N×M 分项也要自洽 (每个分项不得超过总分)
            for dm in DIST_PAIR.finditer(raw):
                a, b = int(dm.group(1)), int(dm.group(2))
                if a * b > claimed_total:
                    problems.append(f'{path} 分布行算术错: {a}×{b}={a*b} 已超总分 {claimed_total}')
        if claimed and computed:
            for name, c in computed.items():
                key = next((k for k in claimed if k[:2] in name or name[:2] in k), None)
                if key and claimed[key] != c:
                    problems.append(f'{path} 分值口径打架: 题型行 "{key}"={claimed[key]} 分 vs 节标题 "{name}"={c} 分')
            s_claim, s_comp = sum(claimed.values()), sum(computed.values())
            if s_claim != s_comp:
                problems.append(f'{path} 总分对不上: 题型行合计 {s_claim} vs 节标题合计 {s_comp}')
    return problems


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    all_problems: list[str] = []
    for path in sys.argv[1:]:
        all_problems.extend(check_file(path))
    if all_problems:
        print(f'✗ 发布卫生门禁: {len(all_problems)} 处命中')
        for p in all_problems:
            print(' ', p)
        return 1
    print('✓ 发布卫生门禁通过')
    return 0


if __name__ == '__main__':
    sys.exit(main())
