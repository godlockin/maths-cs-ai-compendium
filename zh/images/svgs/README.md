# P20-A 原创 SVG 插图 · 索引与说明

> **位置**: `zh/images/svgs/`
> **总数**: 5 张核心插图 (示范集)
> **格式**: SVG (矢量, 任何尺寸不失真, 可直接嵌入 Markdown)

---

## 一 · 已完成插图 (5 张)

| 文件 | 主题 | 用途章节 |
|------|------|----------|
| `chapters_map.svg` | 25 章全景地图 | 整本书前言 + 全局概览 |
| `llm_inference_arch.svg` | LLM 推理部署全景架构 | Ch17 / Ch18 / Ch25 |
| `attention_complexity.svg` | Attention 复杂度演进曲线 | Ch07 / Ch17 |
| `agent_protocols_stack.svg` | AI Agent 5 大协议栈 | Ch23 |
| `rlhf_pipeline.svg` | RLHF 三阶段 + DPO/GRPO 对比 | Ch07 / Ch21 |
| `l1_l2_linf_norm.svg` | L1/L2/L∞ 范数等值面 | Ch01 / Ch03 |
| `gradient_descent.svg` | 梯度下降示意 | Ch03 / Ch06 |
| `normal_dist_clt.svg` | 正态分布 + 中心极限定理 | Ch04 / Ch05 |
| `transformer_arch.svg` | Transformer Encoder-Decoder | Ch07 / Ch25 |
| `bpe_tokenization.svg` | BPE Token 化流程 | Ch07 |
| `cnn_convolution.svg` | CNN 卷积操作 | Ch08 / Ch11 |
| `vit_arch.svg` | ViT 架构 | Ch08 / Ch10 |
| `mfcc_pipeline.svg` | MFCC 特征提取 | Ch09 |
| `matrix_multiplication.svg` | 矩阵乘法 GEMM | Ch02 / Ch16 |
| `cap_theorem.svg` | CAP 定理 | Ch18 |
| `bayesian_network.svg` | 贝叶斯网络 | Ch05 / Ch19 |
| `whisper_asr_pipeline.svg` | Whisper ASR 流程 | Ch09 |
| `stable_diffusion_arch.svg` | SD 潜在扩散 | Ch08 / Ch10 |
| `av_levels_sae.svg` | 自动驾驶分级 | Ch11 |
| `gnn_fraud_detection.svg` | GNN 团伙欺诈 | Ch12 / Ch19 |
| `cuda_thread_model.svg` | CUDA 线程模型 | Ch16 |
| `rag_architecture.svg` | RAG 架构 | Ch23 / Ch25 |
| `moe_architecture.svg` | MoE 架构 | Ch07 / Ch17 |
| `paged_attention.svg` | KV Cache + PagedAttention | Ch17 |
| `alphafold_arch.svg` | AlphaFold 2 架构 | Ch19 |
| `mamba2_arch.svg` | Mamba-2 状态空间模型 | Ch07 / Ch17 |
| `federated_learning.svg` | FedAvg 联邦学习 | Ch20 |
| `tree_of_thoughts.svg` | ToT 树状推理 | Ch23 |
| `flash_attention_3_tricks.svg` | FA 3 大技巧 | Ch07 / Ch17 |
| `quantization_comparison.svg` | 量化精度对比 | Ch17 |
| `recommender_3stage.svg` | 推荐 3 段式 | Ch18 / Ch25 |

---

## 二 · 风格指南

### 2.1 配色

- **数学**: `#4a90e2` 蓝
- **ML**: `#7ed321` 绿
- **DL**: `#f5a623` 橙
- **应用**: `#bd10e0` 紫
- **前沿**: `#e74c3c` 红

### 2.2 字体

- 中文: `sans-serif` (默认)
- 标题: `bold 24px`
- 正文: `13-14px`
- 小字: `11-12px`

### 2.3 嵌入方式

```markdown
![LLM 推理架构](../images/svgs/llm_inference_arch.svg)
```

或 HTML:

```html
<img src="../images/svgs/llm_inference_arch.svg" width="800">
```

---

## 三 · 推荐新增插图 (95 张候选)

> 全部 25 章 × 4 张 = 100 张目标, 已完成 5 张, 剩余 95 张可选。

### 3.1 高优先级 (建议先做, 每章 1-2 张)

| 章节 | 插图主题 |
|------|----------|
| Ch01 向量 | 向量空间几何示意 + 范数等值面 (L1/L2/L∞) |
| Ch02 矩阵 | 矩阵乘法示意 + SVD 几何 |
| Ch03 微积分 | 梯度下降示意 + 凸函数 |
| Ch04 统计 | 正态分布 + 中心极限定理 |
| Ch05 概率 | 贝叶斯网络 + 信息熵 |
| Ch06 ML | 决策树 + 神经网络对比 |
| Ch07 NLP | Transformer 架构 + BPE 流程 |
| Ch08 CV | CNN 卷积示意 + ViT Patch |
| Ch09 语音 | MFCC 提取 + 端到端 ASR |
| Ch10 多模态 | CLIP 训练 + VLM 架构 |
| Ch11 自主系统 | VLA 模型架构 |
| Ch12 GNN | 图卷积示意 |
| Ch13 系统 | 进程 / 内存 / IO |
| Ch14 算法 | 排序 / 搜索复杂度对比 |
| Ch15 工程 | Git 工作流 + CI/CD |
| Ch16 GPU | CUDA 线程模型 + 内存层次 |
| Ch17 推理 | 量化方案对比 + 引擎对比 |
| Ch18 系统 | ML Pipeline 架构 |
| Ch19 应用 | AlphaFold 架构 |
| Ch20 前沿 | 量子比特可视化 + BCI 流程 |
| Ch21 对齐 | 对齐层次 + 治理框架 |
| Ch22 Eval | Benchmark 体系 + LLM-as-Judge |
| Ch23 Agent | ReAct / Reflexion 流程 |
| Ch24 优化 | 凸优化 + 分布式 SGD |
| Ch25 面试 | 系统设计框架 + Offer 博弈 |

### 3.2 中优先级 (锦上添花)

- 流程图: 数据流 / 训练 pipeline / 推理 pipeline
- 对比表: 各模型 / 各算法性能
- 时序图: 模型演进 / 协议时间线
- 架构图: 微服务 / 分布式系统

### 3.3 低优先级 (可选)

- 封面图 / 章节装饰
- 概念图 (抽象)

---

## 四 · 创建方式

### 4.1 模板

参考已完成 5 张, 主要元素:
- `<rect>` + `<circle>` + `<path>`: 几何
- `<text>`: 标签
- `<marker>` + `<path>`: 箭头
- `<defs>` + `<style>`: 统一样式

### 4.2 工具

- **Inkscape** (开源)
- **Figma** (在线)
- **draw.io** (免费)
- **Mermaid** (Markdown 内嵌, 自动 SVG)
- **D3.js** (编程生成)

### 4.3 验证

- 在 Chrome 打开 .svg 文件
- 检查标签不重叠
- 检查配色协调
- 检查跨平台兼容

---

## 五 · 工作量估算

- **每张原创 SVG**: 30-60 分钟
- **95 张剩余**: ~80-150 小时
- **外包成本** (按 $30/h): $2.4k-4.5k
- **建议**: 每章 2 张核心 = 50 张 = ~25-50 小时

---

## 六 · 一句话总结

> **5 张原创 SVG + 索引文档 + 配色规范 + 候选清单** 已就位。
> **剩余 95 张按需扩展**, 是出版级别视觉的"长尾工作"。
> **当前已显著提升教材可读性, 接近数字出版水准**。
