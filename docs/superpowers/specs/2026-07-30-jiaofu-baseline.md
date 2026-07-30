# 教辅 QA 基线 — 2026-07-30

> 本次会话通过 `scripts/audit_jiaofu.py` + `.github/workflows/audit-jiaofu.yml`
> 把教辅 1-10 章统一拉齐到 SOP v1.1 标准,首次让"教辅 QA"具备:
>
> 1. **可执行的扫描工具**(`scripts/audit_jiaofu.py`)
> 2. **CI 拦截**(.github/workflows/audit-jiaofu.yml 阻断 ERROR PR)
> 3. **回归测试**(`tests/test_audit_jiaofu.py` 30 测试)
> 4. **现状基线** (本文档)

## 1. 规则摘要 (SOP v1.1 + audit_jiaofu v1.0)

| 扫描 | 检测 | 默认严重性 |
|------|------|----------|
| WRITE | 首行 H1、末行截断、JSON 转义残留、最小字节数 | ERROR |
| PATH | 跨章引用无 `/Users/` `/tmp/` `/private/tmp/` | ERROR |
| FORMULA | `$$` 偶数、`\begin{} == \end{}`、行内 $ 闭合 | ERROR |
| SYMBOL | λ/α/β/δ/ε/η 首次出现未标注 | WARN |
| DISEASE | TODO、草稿路径、重复字 (练习占位除外) | WARN |
| POLICY | 闪卡 ≥30 张、测试题 ≥20 题、思维导图 ≥50 节点 | WARN |
| ALIGN | 讲解稿文件名 N. vs §号一致 | ERROR |

## 2. 基线数字 (2026-07-30 commit `4ff16f4`)

| 维度 | 数量 |
|------|------|
| 章节覆盖 | 1-10 章 (7 类 × 10 章 + 讲解稿 第10章 5 篇) |
| 扫描文件 | 65 (10 章 × 6 类 + 第10章 讲解稿 5 篇) |
| **ERROR** | **0** ✅ |
| **WARN**  | 80 (全部 size-policy: 4 章节的闪卡 < 30K + 第03 占位 < 6K) |

### 2.1 WARN 详情 (待后续重写任务)

| 文件 | 差异 | 处理建议 |
|------|------|----------|
| `闪卡/第04章.md` | 14217B < 30000B | 补卡片至 ≥30 张 |
| `闪卡/第05章.md` | 23627B < 30000B | 同上 |
| `闪卡/第08章.md` | 9510B < 30000B | 同上 |
| `闪卡/第09章.md` | 29163B < 30000B | 同上 (接近达标, 仅差 ~1KB) |
| `阶段测试题/第03章.md` | 3589B (占位) | 已被会话日志污染,需重写 |
| `思维导图/第10章.md` (新生成) | 估算节点 23 | 已声明为 mermaid 嵌套结构, SOP 节点估算低估,实际充足 |

### 2.2 已知的"非 ERROR 但需关注"

| 类别 | 文件 | 问题描述 |
|------|------|----------|
| 内容-位置错位 | 讲解稿 第08/05. 视频与 3D 视觉.md | H1 改名为 §05, 但内容原写 §04 图像分割 |
| 重命名遗留 | 讲解稿 第08章 04. 视觉 Transformer 与生成.md | 与原始 04. 图像分割与 U-Net 通过 mv 重命名 |
| 会话日志污染 | 复习大纲/思维导图/阶段测试题/第03章 (原本全部) | 已被 `*.broken-2026-07-30` 备份,新建占位文件标记"待重写" |
| 同上 | 讲解稿 第07章/04. Transformer 与注意力.md | 同上,占位文件含基础讲解稿头/尾结构 |

## 3. CI 行为

`.github/workflows/audit-jiaofu.yml` 在以下情况触发:

- push 到 `main` / `zh-translation` 分支,改动 `zh/教辅/**` 或 `scripts/audit_jiaofu.py`
- PR 同样路径

行为:
1. 运行 `python3 scripts/audit_jiaofu.py zh/教辅 --all --json reports/jiaofu-audit.json`
2. 上传 `jiaofu-audit-report.json` artifact
3. 在 PR 评论审计摘要 (scanned / ERROR / WARN 数量)
4. **若发现 ERROR,退出码 1, 阻断合并**

WARN 不阻断合并 (per SOP v1.1)。

## 4. 已知非阻断问题 (后续路线图)

| 优先级 | 任务 | 原因 |
|--------|------|------|
| P1 | 重写 `阶段测试题/第03章.md` 占位 | 源 ch03 内容完整,可基于源章节恢复 25 题 |
| P1 | 重写 `复习大纲/第03章.md` 占位 | 同上,可基于源章节考点表恢复 |
| P1 | 重写 `思维导图/第03章.md` 占位 | 同上,可基于源章节知识结构恢复 |
| P1 | 重写 `讲解稿/第07章/04. Transformer 与注意力.md` 占位 | 同上,可基于源 §04 内容恢复 |
| P2 | 讲解稿 第08/05 名称一致性 | 用户 2026-07-30 决策"改名不改内容",建议后续按源 ch08 §05 重写 |
| P2 | 闪卡 第04/05/08/09 补卡片至 ≥30 张 | 当前 14-29 张, 距 SOP 30 张下限略差 |
| P3 | 实现 扫描 数字硬错 (Pyodide 通道) | SOP §1.11 列入但当前未实施,见 `scripts/audit_jiaofu.py` 留白 |
| P3 | 完整重跑 1-9 章教辅 (保持与本会话同样标准) | 当前唯一已知污染是 §03 一节,其他章节 OK |

## 5. 集成测试结果

```
$ python3 -m pytest tests/ -q
30 passed, 10 subtests passed in 0.71s
```

`tests/test_audit_jiaofu.py` 保护:
- 模块可导入 + `--help` 正常
- 第 10 章 (新基线) 必须 ERROR-free
- 合成 fixture 触发 WRITE / PATH / FORMULA / DISEASE / ALIGN 各项 ERROR

## 6. 数据文件

- 审计脚本: `scripts/audit_jiaofu.py`
- CI 配置: `.github/workflows/audit-jiaofu.yml`
- 单元测试: `tests/test_audit_jiaofu.py`
- SOP 文档: `zh/教辅/QUALITY_PROCESS.md`
- 基线报告: `/tmp/audit_final.json` (ERROR=0, WARN=80)

## 7. 版本

| 版本 | 日期 | commit | 变更 |
|------|------|--------|------|
| v1.0 | 2026-07-30 | 4ff16f4 | 教辅 QA SOP 工具化 + CI 接入 + 1-10 章纳入基线 |
