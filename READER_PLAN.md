# 反向纠错专家团 v2 · 按领域细分

主公批 v2: 入门通用 1 人, 中级/资深/科技作者**按文章领域**分多组, 每组配专属 tools 与 skills. 总计 ~15 个专家并行 review.

## 角色分组 (按章节领域)

### 通用入门组 (1 人)
- **R0 · 高中生入门读者** — 通用视角, 看任何章节, 无前置背景. 抽样 8 篇横跨全书.

### 数学与统计领域 (2 人)
- **R1-MATH · 应用数学博士/教授** — 审 Ch01-05 (向量/矩阵/微积分/统计/概率)
  - tools: WebSearch (查论文/教科书引用), WebFetch (Springer/arXiv 摘要)
  - skills: 严格公式推导, 符号约定一致 (列向量 vs 行向量), 实分析基础
- **R2-CONVEX · 凸优化研究员** — 审 Ch24 (数值/凸优化)
  - tools: WebSearch (Boyd/Nocedal/Trefethen), arXiv look-up
  - skills: KKT, 强凸性, 算法收敛率严谨性, 文献引用准确性

### 经典 ML 与深度学习领域 (2 人)
- **R3-CLASSICML · 资深 ML 工程师** — 审 Ch06 (经典 ML/深度学习)
  - tools: WebSearch (经典算法), GitHub 查 sklearn/XGBoost 实现细节
  - skills: 公式 vs 实现一致性, 工程坑点
- **R4-DL-RESEARCH · 顶级 DL 研究科学家** — 审 Ch06 (深度学习部分), Ch22 (Eval)
  - tools: WebSearch (顶会论文), arXiv 摘要, NeurIPS/ICML 论文引用核验
  - skills: 数学严谨, 引用真实, 与 SOTA 对齐

### NLP 与 LLM 领域 (2 人)
- **R5-NLP · NLP 研究科学家 (高校)** — 审 Ch07 (NLP), Ch22/05 (LLM eval)
  - tools: WebSearch (ACL/EMNLP/NAACL), HuggingFace 文档
  - skills: BPE/WordPiece 准确性, LM 训练细节, 学术引用规范
- **R6-LLM-OPS · LLM 应用工程师** — 审 Ch07/05 (高级文本生成), Ch23 (Agent)
  - tools: WebSearch (OpenAI/Anthropic/Google API 文档), GitHub 查 vLLM/SGLang/TGI
  - skills: API/库名称准确, 工程实战, 与社区共识对齐

### 计算机视觉与多模态 (2 人)
- **R7-CV · 资深 CV 研究员** — 审 Ch08 (CV), Ch10 (多模态)
  - tools: WebSearch (CVPR/ECCV/ICCV), HuggingFace Transformers
  - skills: CNN/Transformer 细节, 多模态架构, SOTA benchmark
- **R8-ROBOT · 机器人 + 视觉定位工程师** — 审 Ch11 (自主系统), Ch12 (GNN)
  - tools: WebSearch (RSS/CoRL/ICRA), 自动驾驶/机器人论文
  - skills: SLAM/VLA/具身智能, BEV 感知, GNN 应用

### 音频语音领域 (1 人)
- **R9-ASR · 语音 AI 工程师** — 审 Ch09 (音频与语音)
  - tools: WebSearch (Interspeech/ICASSP), ESPnet/HuggingFace 文档
  - skills: ASR/TTS/声码器, 梅尔频谱公式, Wav2Vec/Whisper 准确性

### 计算机基础与系统 (3 人)
- **R10-OS · OS 教授** — 审 Ch13 (计算与操作系统)
  - tools: WebSearch (OS 教科书 OSTEP/OSTEP 2018), Arpaci-Dusseau
  - skills: 进程调度/内存管理/文件系统, 严格性
- **R11-ALGO · 算法竞赛选手 + 业界工程师** — 审 Ch14 (DSA)
  - tools: WebSearch (CLRS 算法导论), LeetCode/CF 题号真实性
  - skills: 复杂度分析, 跳表/红黑树/B 树细节, 入门到资深分级
- **R12-SDE · 资深 SRE/后端工程师** — 审 Ch15 (软工), Ch16 (GPU 编程)
  - tools: WebSearch (Linux/PTX/SASS/NVIDIA 文档), GitHub 查 NVIDIA/cuBLAS
  - skills: 工程实践, CUDA 优化, Docker/CI/CD, warp/SM 架构版本

### MLOps 与分布式系统 (2 人)
- **R13-MLOPS · 资深 MLOps 工程师** — 审 Ch17 (推理), Ch18 (系统设计)
  - tools: WebSearch (VLLM/TGI/Triton 文档), Anyscale/MosaicML 博客
  - skills: KV cache, continuous batching, 模型服务工程
- **R14-DIST-SYS · 分布式系统研究员** — 审 Ch18 (系统设计)
  - tools: WebSearch (Google/AWS/Microsoft 论文), DDIA/Kleppmann
  - skills: 分布式一致性, RDMA/NCCL, 3D 并行 (TP/PP/DP)

### 应用 AI 行业专家 (3 人)
- **R15-FIN · 量化基金经理** — 审 Ch19/01 (金融)
  - tools: WebSearch (公开年报/SSRN/QuantConnect), BloombergGPT/FinGPT
  - skills: 时序预测/组合优化, 业界真实术语 (TWAP/VWAP/VaR), 监管 (Basel III)
- **R16-BIO · 计算生物学博士** — 审 Ch19/02-05 (蛋白/药物/医疗)
  - tools: WebSearch (AlphaFold 论文/Nature/Science), PDB/UniProt 数据库
  - skills: AlphaFold 家族/ESM 准确性, ADMET 术语, FDA/NMPA 监管
- **R17-QUANTUM · 量子计算研究员** — 审 Ch20/01-02 (量子/神经形态)
  - tools: WebSearch (IBM Quantum/PennyLane/Qiskit), Nature Quantum Info
  - skills: VQE/QAOA 推导严谨, Loihi/SpiNNaker 真实硬件, NISQ era 现状

### 前沿主题专家 (2 人)
- **R18-BCI · 神经工程/BCI 研究员** — 审 Ch20/05 (脑机接口)
  - tools: WebSearch (Neuralink/BrainGate/Synchron 论文), Nature Neuroscience
  - skills: BCI 硬件细节, 神经解码算法, 临床试验状态
- **R19-FED · 联邦学习/隐私计算专家** — 审 Ch20/04 (去中心化 AI), Ch23 (Agent 安全)
  - tools: WebSearch (FATE/PaddleFL/OpenFL 文档), 微众银行/阿里论文
  - skills: FedAvg 变体, DP/SMPC 严谨性, 中国/海外生态

### LLM 安全与评估 (2 人)
- **R20-AI-SAFETY · AI 对齐研究员** — 审 Ch21 (对齐/安全/可解释性)
  - tools: WebSearch (Anthropic/OpenAI 论文), arXiv cs.AI
  - skills: RLHF/DPO 数学, mech interp 电路概念, sleeper agents
- **R21-LLM-EVAL · LLM 评测基准开发者** — 审 Ch22 (Eval), Ch22/06 (Contamination)
  - tools: WebSearch (HELM/MMLU/LMSYS 论文), HuggingFace leaderboards
  - skills: benchmark 设计原则, contamination 检测, Elo 评分

### Agent 与 Agentic 系统 (1 人)
- **R22-AGENT · Multi-Agent 系统工程师** — 审 Ch23 (Agent), Ch19/04 (智能体应用)
  - tools: WebSearch (AutoGen/LangGraph/MetaGPT/MCP 文档), GitHub
  - skills: 多框架对比, MCP 协议准确性, Voyager/SWE-Agent 真实进展

### 出版/编辑/教学视角 (3 人)
- **R23-EDITOR · 技术图书资深编辑 (O'Reilly/Manning 级别)** — 审 **全书所有章节**
  - tools: Read, 抽样比照行业标准 (出版的 ML 教材)
  - skills: 章节结构, 风格统一, 表述清晰, 教材化
- **R24-AI-COLUMNIST · AI 专栏作家 (机器之心/新智元级别)** — 审全书
  - tools: Read
  - skills: **AI 味检测专家** (主责), 找出所有"凭据"无信息短语
- **R25-PROF · 高校 CS 教授** — 审全书
  - tools: WebSearch (CS 课程大纲/CS 教育论文)
  - skills: 教学节奏, 习题设计, 先修链, 课程编排

### 总数: 26 个专家

---

## 启动策略

**第一批**: 26 个 agent 同时启动 (单批, 一次性). 由于每个 agent 只看自己领域 5-7 篇, 总工作量:
- 每 agent 8 分钟上限
- 26 agent 并行
- 总 8-15 分钟完成

每个 agent 启动前, 必须 WebSearch/WebFetch 验证自己领域的引用真实性, 不靠记忆.

完成后汇总: 主编 agent 把 26 份报告整合成 `zh/READER_REPORT_v2.md`, 列:
- 总问题清单 (按严重性 P0/P1/P2)
- AI 味高频段 (用于批量重写)
- 各领域特殊反馈 (供专业修复 agent 应对)

---

## 关键参数

- 入门读者 1 人 (R0) — 抽样广, 看**易读性**
- 24 个领域专家 — 抽样专, 看**专业准确性**
- 1 个全章节编辑 (R23) + 1 个全章节 AI 味检测 (R24) + 1 个全章节教学 (R25) — 横切视角

总计 **26 位专家**.

待 P5 (wf_f07b5b29-298) 完成通知到来, 我立即启动.