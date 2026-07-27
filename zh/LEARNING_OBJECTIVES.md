# 学习目标与先修知识 (Learning Objectives)

> 本文件为全书 25 章提供**学习目标**与**先修知识**清单, 方便读者按图索骥、按需跳读.
>
> - **Prerequisites (先修)**: 阅读本章前建议掌握的知识.
> - **Learning Objectives (学习目标)**: 读完本章后你应当能够做到的事.
>
> 建议路径:
> - **数学地基** (第 01-05 章) → **ML/DL 核心** (第 06 章) → **模态专章** (第 07-12 章) → **系统与工程** (第 13-18 章) → **前沿与实战** (第 19-25 章).

---

## 第 01 章 — 向量

**Prerequisites**: 高中数学 (代数、三角、坐标系).

**Learning Objectives (读完本章你能:)**:
1. 用向量表示位置、方向、特征, 并解释欧氏空间与坐标系的几何直观.
2. 熟练计算向量加减、数乘、点积、叉积, 并说明其几何含义 (投影、夹角、面积).
3. 计算向量的 L1 / L2 / L∞ 范数, 并解释各自在 ML 中的用途 (正则化、距离度量).
4. 用余弦相似度衡量高维向量的相似性, 理解词向量、Embedding 的几何基础.
5. 使用 NumPy 完成常见向量运算, 并识别广播 (broadcasting) 带来的形状陷阱.

---

## 第 02 章 — 矩阵

**Prerequisites**: 第 01 章 (向量运算).

**Learning Objectives (读完本章你能:)**:
1. 用矩阵表示线性映射, 完成矩阵乘法、转置、逆、行列式的计算.
2. 解释特征值与特征向量的几何意义, 并计算 2×2 / 3×3 矩阵的特征分解.
3. 掌握 SVD 分解及其在 PCA、推荐系统、低秩近似中的应用.
4. 判断矩阵的秩、正定性与条件数, 并说明其对数值稳定性的影响.
5. 在深度学习框架中辨析张量 (Tensor) 形状与矩阵操作, 避免维度错配 bug.

---

## 第 03 章 — 微积分

**Prerequisites**: 第 01-02 章; 高中函数与极限.

**Learning Objectives (读完本章你能:)**:
1. 计算一元/多元函数的导数、偏导、梯度、Jacobian 与 Hessian.
2. 用链式法则手工推导简单神经网络的反向传播 (Backpropagation).
3. 解释梯度下降、动量、自适应学习率 (Adam / AdamW) 背后的数学原理.
4. 使用 PyTorch autograd / JAX grad 进行自动微分, 并验证与手推梯度一致.
5. 理解泰勒展开、凸函数、Lipschitz 连续等概念在优化收敛性分析中的角色.

---

## 第 04 章 — 统计学

**Prerequisites**: 第 03 章 (积分); 基础数据处理经验.

**Learning Objectives (读完本章你能:)**:
1. 区分描述性统计与推断性统计, 计算均值、方差、分位数、相关系数.
2. 使用假设检验 (t 检验、卡方检验、ANOVA) 判断实验结果是否显著.
3. 构造置信区间, 解释 p 值与第一/二类错误, 避免常见误用 (p-hacking).
4. 应用 Bootstrap 与置换检验, 处理无参数假设的实际问题.
5. 用统计视角审视 A/B 测试与模型评测结果, 识别显著性 vs. 实际意义.

---

## 第 05 章 — 概率论

**Prerequisites**: 第 03-04 章.

**Learning Objectives (读完本章你能:)**:
1. 用样本空间、事件、概率测度描述随机现象, 掌握条件概率与贝叶斯公式.
2. 熟悉常见分布 (Bernoulli / Binomial / Poisson / Gaussian / Categorical) 的形状与用途.
3. 计算期望、方差、协方差, 应用大数定律与中心极限定理.
4. 用 MLE / MAP 推导常见模型 (线性回归、逻辑回归、朴素贝叶斯) 的参数.
5. 理解信息论基础 (熵、KL 散度、交叉熵), 并解释其在损失函数中的作用.

---

## 第 06 章 — 机器学习

**Prerequisites**: 第 01-05 章; Python 编程.

**Learning Objectives (读完本章你能:)**:
1. 区分监督、无监督、自监督、强化学习范式, 选择合适任务框架.
2. 实现线性回归、逻辑回归、决策树、随机森林、SVM、K-Means 等经典算法.
3. 用偏差-方差分解解释欠拟合与过拟合, 应用正则化 (L1 / L2 / Dropout).
4. 设计训练/验证/测试集划分, 使用交叉验证与网格搜索调参.
5. 用 scikit-learn / PyTorch 完成端到端 ML 项目, 并合理选择评估指标 (Accuracy / F1 / AUC / RMSE).

---

## 第 07 章 — 计算语言学

**Prerequisites**: 第 06 章; 基础语言学常识可选.

**Learning Objectives (读完本章你能:)**:
1. 完成文本预处理 (分词、词干化、BPE、SentencePiece) 并识别中英文差异.
2. 解释 Word2Vec、GloVe、FastText 等静态词向量的训练目标与几何性质.
3. 手推 Attention 与 Transformer 的核心公式 (QKV, Multi-Head, Positional Encoding).
4. 使用 Hugging Face Transformers 微调 BERT / GPT 类模型完成分类、生成、抽取任务.
5. 理解 LLM 的预训练-微调-对齐三阶段范式, 并解释 Scaling Law 的实际含义.

---

## 第 08 章 — 计算机视觉

**Prerequisites**: 第 02-03 章 (矩阵、梯度); 第 06 章.

**Learning Objectives (读完本章你能:)**:
1. 解释卷积、池化、感受野等 CNN 核心概念, 并手算简单卷积输出形状.
2. 使用 ResNet / EfficientNet / ViT 完成图像分类, 理解残差连接与注意力机制.
3. 实现目标检测 (YOLO / Faster R-CNN) 与分割 (U-Net / Mask R-CNN) 的训练与推理.
4. 应用数据增强、迁移学习、蒸馏, 在小数据场景取得可用效果.
5. 理解扩散模型 (Diffusion) 与 CLIP 的原理, 解释图文对齐的技术路线.

---

## 第 09 章 — 音频与语音

**Prerequisites**: 第 03 章 (傅立叶); 第 06 章.

**Learning Objectives (读完本章你能:)**:
1. 完成音频采样、STFT、梅尔频谱 (Mel-Spectrogram) 特征提取.
2. 使用 CTC / Attention 架构训练 ASR 模型, 解释 Whisper / Conformer 的设计.
3. 训练/使用 TTS 模型 (Tacotron / VITS / VALL-E), 生成自然语音.
4. 完成说话人识别、声纹验证、语音增强等下游任务.
5. 部署实时语音管线, 权衡延迟、吞吐量、模型大小三角约束.

---

## 第 10 章 — 多模态学习

**Prerequisites**: 第 07-09 章.

**Learning Objectives (读完本章你能:)**:
1. 解释多模态融合的三种范式: 早期融合、晚期融合、跨模态注意力.
2. 训练/使用 CLIP、BLIP、LLaVA 等图文对齐模型完成检索与 VQA.
3. 理解视频-文本、音频-文本联合建模的挑战 (时序对齐、模态缺失).
4. 用视觉-语言模型 (VLM) 完成 OCR、图表理解、UI Agent 等实际任务.
5. 评估多模态系统的能力边界, 识别幻觉 (Hallucination) 与模态偏见.

---

## 第 11 章 — 自主系统

**Prerequisites**: 第 05-06 章; 第 08 章; 控制论基础可选.

**Learning Objectives (读完本章你能:)**:
1. 用 MDP / POMDP 建模决策问题, 区分策略 (Policy) 与价值 (Value).
2. 实现 Q-Learning、DQN、PPO、SAC 等强化学习算法, 训练玩具环境 (CartPole / Atari).
3. 理解模仿学习、逆强化学习、RLHF 的思想与工程差异.
4. 解释自动驾驶感知-规划-控制的分层架构, 掌握 SLAM 与运动规划基础.
5. 分析机器人系统的安全边界, 识别 Sim-to-Real gap 与分布外 (OOD) 风险.

---

## 第 12 章 — 图神经网络

**Prerequisites**: 第 02 章 (矩阵、特征分解); 第 06 章.

**Learning Objectives (读完本章你能:)**:
1. 用邻接矩阵、拉普拉斯矩阵表示图, 计算基本图论量 (度、路径、聚类系数).
2. 推导 GCN、GraphSAGE、GAT 的消息传递 (Message Passing) 公式.
3. 使用 PyG / DGL 完成节点分类、链路预测、图分类任务.
4. 解释异构图、动态图、图 Transformer 的建模思路.
5. 识别 GNN 常见陷阱 (过平滑 Over-Smoothing、瓶颈 Bottleneck), 应用相应缓解手段.

---

## 第 13 章 — 计算与操作系统

**Prerequisites**: C / Python 基础编程.

**Learning Objectives (读完本章你能:)**:
1. 解释冯·诺依曼架构、CPU 流水线、缓存层级 (L1/L2/L3/DRAM) 与内存墙.
2. 理解进程、线程、协程的差异, 编写正确的同步/异步并发代码.
3. 掌握虚拟内存、文件系统、系统调用的基本原理.
4. 分析程序性能瓶颈 (CPU-bound / Memory-bound / IO-bound), 选择合适优化方向.
5. 读懂 top / htop / perf / strace 等诊断工具输出, 定位真实生产问题.

---

## 第 14 章 — 数据结构与算法

**Prerequisites**: 第 13 章; 基础编程.

**Learning Objectives (读完本章你能:)**:
1. 熟练使用数组、链表、栈、队列、哈希表、堆、树、图, 并分析其时空复杂度.
2. 掌握排序、查找、递归、动态规划、贪心、回溯、图搜索等经典算法范式.
3. 用大 O 记号分析算法复杂度, 权衡时间 vs. 空间.
4. 识别 ML/AI 场景下常见数据结构选型问题 (向量检索、KV 存储、流处理).
5. 独立完成中等难度算法题, 并写出可读、健壮的实现代码.

---

## 第 15 章 — 生产级软件工程

**Prerequisites**: 第 13-14 章; 至少一门主力语言.

**Learning Objectives (读完本章你能:)**:
1. 设计清晰的模块边界与接口, 遵循 SOLID / DRY / YAGNI 等原则.
2. 编写单元测试、集成测试、端到端测试, 理解 TDD 与测试金字塔.
3. 熟练使用 Git 分支模型、Code Review、CI/CD, 保障团队协作质量.
4. 应用可观测性三大支柱 (Logs / Metrics / Traces) 定位分布式系统故障.
5. 从需求评审、技术设计、上线、复盘完整走通一次生产级迭代.

---

## 第 16 章 — SIMD 与 GPU 编程

**Prerequisites**: 第 13 章; C / C++ 基础.

**Learning Objectives (读完本章你能:)**:
1. 解释 SIMD、SIMT、MIMD 并行模型, 说明 CPU AVX 与 GPU Warp 的差异.
2. 用 CUDA / Triton 编写基础 Kernel (向量加法、矩阵乘法、Reduction、Softmax).
3. 分析 GPU 内存层级 (Register / Shared / L2 / HBM) 对性能的影响.
4. 使用 Roofline 模型判断算子是 Compute-bound 还是 Memory-bound.
5. 使用 Nsight Systems / Compute 剖析 Kernel, 优化 Occupancy 与 Bank Conflict.

---

## 第 17 章 — AI 推理

**Prerequisites**: 第 06-07 章; 第 16 章.

**Learning Objectives (读完本章你能:)**:
1. 解释推理引擎的核心指标: 延迟 (P50/P99)、吞吐量、QPS、TTFT、TPOT.
2. 应用量化 (INT8 / INT4 / FP8)、剪枝、蒸馏, 压缩模型且保精度.
3. 理解 KV Cache、PagedAttention、Continuous Batching 的工程价值.
4. 使用 vLLM / TensorRT-LLM / SGLang 部署 LLM 推理服务.
5. 设计推理网关, 处理限流、路由、负载均衡与多模型编排.

---

## 第 18 章 — 机器学习系统设计

**Prerequisites**: 第 06 章; 第 15 章; 第 17 章.

**Learning Objectives (读完本章你能:)**:
1. 从业务需求出发, 完成端到端 ML 系统设计 (数据、特征、训练、评估、部署、监控).
2. 设计特征平台 (Feature Store), 解决在线/离线一致性问题.
3. 构建训练-推理管线, 应用 MLOps 工具 (MLflow / Airflow / Kubeflow).
4. 设计 A/B 测试与影子发布 (Shadow) 机制, 安全上线新模型.
5. 建立数据/模型漂移 (Drift) 监控与自动化再训练闭环.

---

## 第 19 章 — 应用 AI

**Prerequisites**: 第 06-10 章; 第 17-18 章.

**Learning Objectives (读完本章你能:)**:
1. 使用 RAG (检索增强生成) 构建企业知识问答系统, 权衡召回 vs. 精度.
2. 设计 Prompt Engineering / Few-shot / CoT / ReAct 模式解决复杂任务.
3. 构建代码生成、文档摘要、客服机器人等常见 LLM 应用.
4. 集成向量数据库 (Pinecone / Milvus / Qdrant) 完成语义检索.
5. 评估应用效果, 建立离线基准与在线反馈闭环.

---

## 第 20 章 — 前沿 AI

**Prerequisites**: 第 06-07 章; 第 10 章.

**Learning Objectives (读完本章你能:)**:
1. 跟踪最新 LLM / VLM / 世界模型的架构演进 (MoE、Mamba、状态空间模型).
2. 理解合成数据、自我改进 (Self-Improve)、Test-Time Compute 的研究前沿.
3. 分析多模态推理、具身智能 (Embodied AI)、科学 AI (AI4Science) 的发展方向.
4. 阅读顶会论文 (NeurIPS / ICML / ICLR / ACL / CVPR), 提炼核心贡献.
5. 判断技术趋势的成熟度, 避免盲目跟风或过早唱衰.

---

## 第 21 章 — 对齐、安全与可解释性

**Prerequisites**: 第 06-07 章; 第 19 章.

**Learning Objectives (读完本章你能:)**:
1. 解释 RLHF、DPO、Constitutional AI 等对齐 (Alignment) 方法的差异.
2. 识别常见 AI 风险: 偏见、幻觉、越狱、隐私泄露、供应链攻击.
3. 应用红队测试 (Red Teaming)、对抗样本、成员推断等安全评估手段.
4. 使用可解释性工具 (SHAP / LIME / Attention 可视化 / 电路分析) 分析模型行为.
5. 遵循 AI 治理框架 (NIST AI RMF / EU AI Act) 完成合规审查.

---

## 第 22 章 — LLM Evaluation 方法学

**Prerequisites**: 第 04 章 (统计); 第 07 章; 第 19 章.

**Learning Objectives (读完本章你能:)**:
1. 区分基准测试 (Benchmark)、人工评测、LLM-as-Judge 三类评估范式.
2. 设计任务特定的评测集, 避免数据污染 (Data Contamination).
3. 应用 Elo / Bradley-Terry / Arena 等成对比较方法.
4. 识别评测偏差 (位置偏差、长度偏差、风格偏差), 应用校准手段.
5. 构建持续评估管线, 支撑模型迭代与 Regression 检测.

---

## 第 23 章 — AI Agent 与工具使用

**Prerequisites**: 第 07 章; 第 19 章; 第 21 章.

**Learning Objectives (读完本章你能:)**:
1. 解释 ReAct、Plan-and-Execute、Reflexion 等 Agent 架构范式.
2. 设计工具调用 (Function Calling / Tool Use) 接口, 处理错误与重试.
3. 构建多 Agent 协作系统 (Supervisor / Swarm / Debate), 解决复杂任务.
4. 集成 MCP (Model Context Protocol) / OpenAPI 工具生态.
5. 评估 Agent 的成功率、成本、延迟, 建立 Agent-specific 观测体系.

---

## 第 24 章 — 数值分析与凸优化补遗

**Prerequisites**: 第 02-03 章; 第 06 章.

**Learning Objectives (读完本章你能:)**:
1. 分析浮点表示 (FP32 / FP16 / BF16 / FP8) 的精度、范围与数值稳定性.
2. 掌握 LU / QR / Cholesky / SVD 等数值线性代数分解算法.
3. 解释凸集、凸函数、拉格朗日对偶、KKT 条件, 判断优化问题的凸性.
4. 熟悉 SGD、Newton、L-BFGS、共轭梯度、ADMM 等优化算法的收敛性.
5. 识别病态问题 (Ill-Conditioned), 应用预处理 (Preconditioning) 与正则化.

---

## 第 25 章 — AI 系统实战面试指南

**Prerequisites**: 完成第 01-24 章的相应部分.

**Learning Objectives (读完本章你能:)**:
1. 拆解 ML System Design 面试题 (推荐系统、搜索、Feed 排序、LLM 应用) 的通用框架.
2. 在 45 分钟内完成需求澄清、方案设计、数据建模、模型选型、评估设计的完整表达.
3. 应答 LLM/RAG/Agent 类新题, 展示对最新技术栈的理解.
4. 处理开放式 trade-off 问题 (精度 vs. 延迟, 成本 vs. 效果, 定制 vs. 通用).
5. 复盘面试表现, 建立个人技术叙事 (Tech Narrative) 与项目案例库.

---

> **使用建议**:
> - 初学者按章顺序推进, 每章完成"Learning Objectives"自测再进入下一章.
> - 有基础的读者可从"Prerequisites"反查缺口, 定点补齐.
> - 团队学习可按目标拆分为周计划, 每周聚焦 1-2 个 objective.
