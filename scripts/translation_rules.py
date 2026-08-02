#!/usr/bin/env python3
"""Translation QA rules — injectable into verify_translation.py via import.
New checks: inline math, inline code, translationese, glossary consistency, register.
"""
import json, os, re, sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

# ═══════════════════════════════════════════════════════════════════
# 1. Translationese pattern bank
# ═══════════════════════════════════════════════════════════════════

TRANSLATIONESE_PATTERNS = [
    # (regex, suggestion, severity)
    (r"作为一个\b", "删掉多余的'一个'，改为'作为'", "P2"),
    (r"对于.{1,20}来说", "删掉'对于...来说'，直接写主语", "P2"),
    (r"让我们来看看", "改为'来看' 或 '我们来看'", "P2"),
    (r"被称之为", "改为'叫做' 或 '被称为'", "P2"),
    (r"这是一件非常重要的事情", "精简为'这很重要'", "P2"),
    (r"其被", "主动语态优先，避免'其被'", "P2"),
    (r"人们通常", "简化或省略", "P2"),
    (r"实际上，我们可以", "改为'其实可以' 或删除", "P2"),
    (r"值得注意的是", "改为'注意'", "P2"),
    (r"\b等等\b", "检查是否必要，中文少用省略", "P2"),
    (r"呢\b", "检查是否翻译腔语气词", "P2"),
    (r"的的", "重复'的'——合并或删除", "P2"),
    (r"被\w{2,4}所", "避免'被...所'的文言残留", "P2"),
    (r"进行\w{2,6}(?:处理|操作|分析|研究|实验|训练|推理|优化)", "删掉虚动词'进行'，直接用实义动词", "P2"),
    (r"东西", "改为更准确的名词", "P2"),
]

# ═══════════════════════════════════════════════════════════════════
# 2. Glossary loader
# ═══════════════════════════════════════════════════════════════════

@dataclass
class GlossaryEntry:
    en: str
    zh_preferred: str
    zh_variants: list[str]
    notes: str = ""

def load_glossary(glossary_path: Path) -> dict[str, GlossaryEntry]:
    """Parse GLOSSARY.md into {en_term: GlossaryEntry} dict."""
    if not glossary_path.exists():
        return {}

    text = glossary_path.read_text(encoding="utf-8")
    entries: dict[str, GlossaryEntry] = {}

    for line in text.split('\n'):
        line = line.strip()
        if not line.startswith('|') or line.startswith('|--') or line.startswith('|---'):
            continue
        parts = [p.strip() for p in line.split('|')]
        # Columns: | # | EN | ZH | Notes |
        if len(parts) < 4:
            continue
        en_idx = 2 if len(parts) >= 4 else 1
        zh_idx = 3 if len(parts) >= 4 else 2
        en = parts[en_idx] if en_idx < len(parts) else ""
        zh = parts[zh_idx] if zh_idx < len(parts) else ""
        notes = parts[4] if len(parts) > 4 else ""

        if not en or not zh or en in ('EN', 'English'):
            continue

        # Split ZH variants: "嵌入 / 嵌入向量" → ["嵌入", "嵌入向量"]
        zh_variants = [v.strip() for v in re.split(r'[\s]*[/／][\s]*', zh)]
        preferred = zh_variants[0] if zh_variants else zh

        entries[en.lower()] = GlossaryEntry(
            en=en, zh_preferred=preferred,
            zh_variants=zh_variants, notes=notes.strip()
        )

    return entries

# ═══════════════════════════════════════════════════════════════════
# 3. New check functions
# ═══════════════════════════════════════════════════════════════════

def check_inline_math(source_text: str, target_text: str) -> tuple[bool, list[str]]:
    """Verify $...$ inline math from EN is preserved in ZH. ZH can add math (F12)."""
    src_math = set(re.findall(r'(?<!\$)\$(?!\$)([^$\n]+?)\$(?!\$)', source_text))
    tgt_math = set(re.findall(r'(?<!\$)\$(?!\$)([^$\n]+?)\$(?!\$)', target_text))
    # Only flag EN math that is MISSING from ZH (deletions only, additions OK)
    missing = src_math - tgt_math
    return len(missing) == 0, sorted(missing)[:10]

def check_inline_code(source_text: str, target_text: str) -> tuple[bool, list[str]]:
    """Verify inline `code` spans are unchanged. Returns (ok, changed_items)."""
    # Only match single-token inline code (single word, no spaces, no newlines)
    src_codes = set(re.findall(r'`([^`\s\n]+?)`', source_text))
    tgt_codes = set(re.findall(r'`([^`\s\n]+?)`', target_text))
    changed = sorted(src_codes - tgt_codes)
    return len(changed) == 0, changed[:10]

def check_heading_parity(source_text: str, target_text: str) -> tuple[bool, dict]:
    """Verify heading count and depth match between source and target."""
    src_headings = re.findall(r'^(#{1,6})\s', source_text, re.MULTILINE)
    tgt_headings = re.findall(r'^(#{1,6})\s', target_text, re.MULTILINE)
    src_counts = {h: src_headings.count(h) for h in set(src_headings)}
    tgt_counts = {h: tgt_headings.count(h) for h in set(tgt_headings)}
    ok = (len(src_headings) == len(tgt_headings) and src_counts == tgt_counts)
    return ok, {"src_total": len(src_headings), "tgt_total": len(tgt_headings),
                "src_by_depth": src_counts, "tgt_by_depth": tgt_counts}

def check_translationese(text: str) -> list[dict]:
    """Scan target text for translationese patterns."""
    findings = []
    for pattern, suggestion, severity in TRANSLATIONESE_PATTERNS:
        for m in re.finditer(pattern, text):
            findings.append({
                "pattern": pattern, "match": m.group(0),
                "position": m.start(), "suggestion": suggestion,
                "severity": severity
            })
    return findings

def check_glossary_consistency(text: str, glossary: dict[str, 'GlossaryEntry']) -> list[dict]:
    """Check that glossary terms are used consistently in target text.
    For each EN term, verify only one ZH variant appears in any given file.
    """
    findings = []
    for en_term, entry in glossary.items():
        variants_used = set()
        for variant in entry.zh_variants:
            if variant in text:
                variants_used.add(variant)
        if len(variants_used) > 1:
            findings.append({
                "en_term": en_term,
                "variants_found": sorted(variants_used),
                "preferred": entry.zh_preferred,
                "message": f"'{en_term}' translated inconsistently: {sorted(variants_used)}"
            })
    return findings

def check_register_score(text: str) -> float:
    """Score text on a 'conversational vs formal' scale. Higher = more conversational."""
    conversational = len(re.findall(r'我们|想象|注意|就是|其实|比如|不过|当然|对吧', text))
    formal = len(re.findall(r'其|该|之|所|者|并非|及其|予以|进行', text))
    total = conversational + formal
    if total == 0:
        return 0.5  # neutral
    return conversational / total

# ═══════════════════════════════════════════════════════════════════
# 4. Chapter mapping: EN dir → ZH dir
# ═══════════════════════════════════════════════════════════════════

CHAPTER_MAP = [
    ("chapter 01 - vectors", "zh/第01章 - 向量"),
    ("chapter 02 - matrices", "zh/第02章 - 矩阵"),
    ("chapter 03 - calculus", "zh/第03章 - 微积分"),
    ("chapter 04 - statistics", "zh/第04章 - 统计学"),
    ("chapter 05 - probability", "zh/第05章 - 概率论"),
    ("chapter 06 - machine learning", "zh/第06章 - 机器学习"),
    ("chapter 07 - computational linguistics", "zh/第07章 - 计算语言学"),
    ("chapter 08 - computer vision", "zh/第08章 - 计算机视觉"),
    ("chapter 09 - audio and speech", "zh/第09章 - 音频与语音"),
    ("chapter 10 - multimodal learning", "zh/第10章 - 多模态学习"),
    ("chapter 11 - autonomous systems", "zh/第11章 - 自主系统"),
    ("chapter 12 - graph neural networks", "zh/第12章 - 图神经网络"),
    ("chapter 13 - computing and OS", "zh/第13章 - 计算与操作系统"),
    ("chapter 14 - data structures and algorithms", "zh/第14章 - 数据结构与算法"),
    ("chapter 15 - production software engineering", "zh/第15章 - 生产级软件工程"),
    ("chapter 16 - SIMD and GPU programming", "zh/第16章 - SIMD 与 GPU 编程"),
    ("chapter 17 - AI inference", "zh/第17章 - AI 推理"),
    ("chapter 18 - ML systems design", "zh/第18章 - 机器学习系统设计"),
    ("chapter 19 - applied AI", "zh/第19章 - 应用 AI"),
    ("chapter 20 - bleeding edge AI", "zh/第20章 - 前沿 AI"),
    ("chapter 21 - alignment, safety & interpretability", "zh/第21章 - 对齐、安全与可解释性"),
    ("chapter 22 - llm evaluation methodology", "zh/第22章 - LLM Evaluation 方法学"),
    ("chapter 23 - ai agent and tool use", "zh/第23章 - AI Agent 与工具使用"),
    ("chapter 24 - numerical analysis and convex optimisation", "zh/第24章 - 数值分析与凸优化补遗"),
    ("chapter 25 - ai system interview guide", "zh/第25章 - AI 系统实战面试指南"),
]


def discover_chapter_pairs(repo_root: Path) -> list[tuple[Path, Path]]:
    """Auto-discover EN+ZH chapter pairs from repo root."""
    pairs = []
    for en_name, zh_name in CHAPTER_MAP:
        en_path = repo_root / en_name
        zh_path = repo_root / zh_name
        if en_path.is_dir() and zh_path.is_dir():
            pairs.append((en_path, zh_path))
    return pairs


# ═══════════════════════════════════════════════════════════════════
# 5. Export for verify_translation.py injection
# ═══════════════════════════════════════════════════════════════════

__all__ = [
    "TRANSLATIONESE_PATTERNS", "GlossaryEntry", "load_glossary",
    "check_inline_math", "check_inline_code", "check_heading_parity",
    "check_translationese", "check_glossary_consistency", "check_register_score",
    "CHAPTER_MAP", "discover_chapter_pairs",
]
