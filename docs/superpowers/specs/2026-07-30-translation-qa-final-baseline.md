# 翻译 QA 最终基线 — 2026-07-30

> 对 20 章（chapter 01–20）源 ↔ 译章节的全量扫描结果，本次 verifier 已应用
> F12 增强块跳过、URL 规范化、缩进 docstring 容忍、LCS sequence alignment。
> 中文章节已批量通过 `normalize_punctuation.py --apply zh/` 完成全角标点。

## 1. 规则修复摘要

| 规则 | 修复前 | 修复后 |
|------|-------|-------|
| P0-MATH | byte-for-byte 全等 | source prefix 必须严格匹配；target 可追加 |
| P0-CODE | 同上 | source prefix 必须严格匹配；target 可追加 |
| P0-ASSET | 全等 | source prefix URL 必须匹配；target 可追加 |
| P0-SOURCE-COVERAGE | unit kind 列表严格相等 | LCS alignment — 仅当 source unit 不可被 target 匹配才报 |
| P0-STRUCTURE | 全等 | LCS alignment on heading+list 子集 |
| F12 增强块（unit scan）| 无 | 跳过 `> **一句话总结**` / `## 🗺️ 本章导览` / `## 📌 本节要点` |

## 2. P0 分布 — 2026-07-30 LCS 升级后

| Rule | Count |
|------|-------|
| P0-SOURCE-COVERAGE | 18 |
| P0-STRUCTURE | 17 |
| P0-MATH | 15 |
| P0-CODE | 14 |
| P0-ASSET | 2 |
| **TOTAL P0** | **66** |

**对比**：134 (改进前) → 100 (F12 前缀容差) → 66 (LCS alignment)。

**剩余 P0 多数源自重复 list 项**——同一 `(kind=list, value=0)` 在
多处出现时，LCS 把后出现项认作"丢失"。下一轮迭代需要 fuzzy
cost-based alignment。

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
Transformer / DC / Brain-Machine Interface 章节）。这是有意的 F12 扩展。

## 4. 完成状态

| 任务 | 状态 |
|------|------|
| unit scan F12 skip | ✅ 65dc9b7 |
| normalize_punctuation.py | ✅ 65dc9b7 (dry-run) |
| normalize_punctuation --apply | ✅ 62531b7 (146 files) |
| P0-MATH/CODE/ASSET 前缀比较 | ✅ e741641 |
| P0-SOURCE-COVERAGE/STRUCTURE LCS | ✅ 84b2752 |
| F12 增强块跳过测试 fixture | ✅ 8be7f0b |
| LCS missing-section fixture | ✅ 84b2752 |
| 第 09–10 章续译方案 | ⏳ 后续会话 |

## 5. 数据文件

- `tests/fixtures/translation_qa/source_f12_prefix/01.md`
- `tests/fixtures/translation_qa/target_f12_valid/01.md`
- `tests/fixtures/translation_qa/source_lcs_missing/01.md`
- `tests/fixtures/translation_qa/target_lcs_missing_section/01.md`
- P0 详细分布：`/tmp/baseline-detailed.txt`
- chapter × token 数据：`/tmp/metrics-output.txt`
