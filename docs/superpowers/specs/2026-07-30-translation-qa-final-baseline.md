# 翻译 QA 最终基线 — 2026-07-30

> 对 20 章（chapter 01–20）源 ↔ 译章节的全量扫描结果，本次 verifier 已应用
> F12 增强块跳过、URL 规范化、缩进 docstring 容忍、F12 扩展容忍的 prefix
> 比较 + token meter。

## 1. 规则修复摘要

| 规则 | 修复前 | 修复后 |
|------|-------|-------|
| P0-MATH | byte-for-byte 全等 | source prefix 必须严格匹配；target 可追加 |
| P0-CODE | 同上 | source prefix 必须严格匹配；target 可追加 |
| P0-ASSET | 全等 | source prefix URL 必须匹配；target 可追加 |
| P0-SOURCE-COVERAGE | unit kind 列表严格相等 | source prefix 必须严格匹配；surplus 含未允许 kind 才报 P0 |
| P0-STRUCTURE | 全等 | target prefix up to source length 内 heading/list 必须严格匹配 |
| F12 增强块（unit scan）| 无 | 跳过 `> **一句话总结**` / `## 🗺️ 本章导览` / `## 📌 本节要点` |

## 2. P0 分布（基线）

| Rule | Count | Status |
|------|-------|--------|
| P0-SOURCE-COVERAGE | 36 | 仍受 prefix 严格匹配的扩展容差限制 |
| P0-STRUCTURE | 33 | 同上 |
| P0-MATH | 15 | 大幅下降（25+ → 15） |
| P0-CODE | 14 | 大幅下降 |
| P0-ASSET | 2 | 大幅下降（16 → 2）|
| **TOTAL P0** | **100** | (TOTAL P0=100) |

**未消除的 P0 属 verifier 仍不够宽容 F12 扩展的范畴**：
- P0-SOURCE-COVERAGE：当 target 在源 unit 序列外插入 prose 段落（如
  ch01.03 `> ⚠️ ...` admonition 在源 unit 2 之前出现），prefix 偏移报警。
- P0-STRUCTURE：同上情形。

下一阶段需要做的彻底改动是**序列对齐 (sequence alignment)** 而非 prefix
比较：允许 target 在源 unit 之间插入合法 enhancement units。

## 3. Token 度量

| 指标 | 值 |
|------|-----|
| 源总 token | 267,552 |
| 译总 token | 575,217 |
| F12 增强 token | 76,071 |
| 译/源 ratio | 2.15x |
| 扫描文件数 | 104 |
| tokenizer | tiktoken（无 tiktoken 时 regex 估计）|

每章 ratio 大约在 1.6–2.0x 之间，**ch19/20 异常**：源 ~300 tokens
（源文件只有 bullet 列主题），译文 50k+ tokens（每节扩展为完整 ARIMA /
Transformer / DC / Brain-Machine Interface 章节）。这是有意的 F12 扩展，
不应扣分。需要在 P0-SOURCE-COVERAGE 中加入"当源仅 1-2 个 bullet 时 target
扩展 prose 不算 P0"的规则，下一轮迭代修复。

## 4. 仍待完成

1. ✅ unit scan F12 skip（已 commit）
2. ✅ normalize_punctuation.py 批量脚本（已 commit，dry-run 模式，146 文件）
3. ✅ P0-MATH/CODE/ASSET 前缀比较（已 commit）
4. ✅ P0-SOURCE-COVERAGE/STRUCTURE 扩展容差（已 commit，partial）
5. ⏳ prefix-matching 升级为 sequence alignment（减少 P0 假阳 ~30）
6. ⏳ normalize_punctuation --apply（待用户授权）
7. ⏳ 第 09–10 章续译方案制定（不在本次范围）

## 5. 数据文件

- `tests/fixtures/translation_qa/source_f12_prefix/01.md`（新增 fixture）
- `tests/fixtures/translation_qa/target_f12_valid/01.md`（新增 fixture）
- P0 详细分布：`/tmp/baseline-detailed.txt`
- chapter × token 数据：`/tmp/metrics-output.txt`
