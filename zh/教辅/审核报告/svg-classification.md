# SVG 分类审查报告 (zh/images/)

总计:115 张
- REDO_REQUIRED:115 / 115
- MINOR_FIX:0 / 115
- NO_CHANGE:0 / 115

分章:ch19=13、ch20=23、ch21=18、ch22=18、ch23=16、ch24=14、ch25=13 (合计 115)

> 所有 115 张原 SVG 均为占位骨架(仅标题文字、"概念A/B/C/D"占位条或简单通用方框),完全未传达原 markdown 上下文描述的概念,因此全部归为 REDO_REQUIRED 整张重画。

> 本报告由 7 个并行子代理按章节产出,每个子代理负责自己章节的文件。

## 章节分布
- ch19 应用 AI:13 张
- ch20 前沿 AI:23 张
- ch21 对齐、安全与可解释性:18 张
- ch22 LLM Evaluation 方法学:18 张
- ch23 AI Agent 与工具使用:16 张
- ch24 数值分析与凸优化补遗:14 张
- ch25 AI 系统实战面试指南:13 张

## ch25 AI 系统实战面试指南 (13 张)

### REDO_REQUIRED

| 文件 | 上下文引用 | 当前问题 | 重画建议 |
|---|---|---|---|
| ch25_01_radar.svg | `01. 面试全景与准备心法.md:167` — 五维能力雷达 Coding/ML/SD/Research/Behavior | 原图仅有标题文字, 无雷达图本体 | 画五边形雷达 + 5 层网格 + MLE/DS/Research 三条对比折线 + 图例 |
| ch25_02_drift_detection.svg | `02. ML 系统设计 8 步框架.md:543` — PSI/KS/MMD 三大漂移方法 | 仅"概念A/B/C/D"占位条, 无方法对比 | 画 3 列方法卡片: PSI (分桶占比) / KS (累计分布) / MMD (高维 embedding), 各含公式+阈值 |
| ch25_02_eight_step_ring.svg | `02. ML 系统设计 8 步框架.md:22` — 8 步圆环图, 用户在中心 | 实际只 6 个节点, 缺 Clarify/Training | 改 8 节点圆环: Clarify→Metrics→Data→Features→Model→Training→Deploy→Monitor, 中心"用户" |
| ch25_02_eight_step_loop.svg | `02. ML 系统设计 8 步框架.md:43` — 8 步框架圆环, 数据→特征→...→反馈 | 7 个节点, 缺 Training 步骤; 文字"反馈,持续迭代,用户在中心"挤在第 7 块 | 改 8 节点圆环: 1数据→2特征→3模型→4评估→5部署→6监控→7反馈→8迭代, 中心"用户" |
| ch25_02_feature_store.svg | `02. ML 系统设计 8 步框架.md:212` — 离线 (Spark+数据仓库) 与在线 (Redis/DynamoDB) 共用特征代码 | 仅一行标题文字, 无架构图 | 画分层: 顶部"特征定义 (feature_repo/)"→左右两路离线/在线仓库, 含 Feast API 调用 |
| ch25_02_two_tower.svg | `02. ML 系统设计 8 步框架.md:295` — 用户塔 + 物品塔 + 点积 | 仅一个占位 box, 无塔结构 | 画左右双塔: 用户特征→DNN→u-vec / 物品特征→DNN→v-vec, 中心点积→相似度 |
| ch25_03_douyin_traffic_pool.svg | `03. 典型题深度演练.md:1085` — 200→1000→5000→50000→500000 五级 | 节点内容仅数字, 缺阶段名+升级条件+降级说明 | 画 5 个池 + 阶段名 + 升级门槛 + 降级提示 |
| ch25_03_four_questions_map.svg | `03. 典型题深度演练.md:22` — 4 类 ML 系统设计场景 | 仅文字重复标题, 无图 | 画 2×2 矩阵: 内容推荐/社交 Feed/搜索排序/短视频流, 各含原型+关键+中文圈变体 |
| ch25_03_lambdamart_gradient.svg | `03. 典型题深度演练.md:333` — Lambda 梯度直观示意 | "概念A/B/C/D"占位, 与 LambdaMART 无关 | 画 5 文档排序 + lambda 反序对箭头 (粗细代表梯度大小), 标注反序对获得大梯度 |
| ch25_03_multitask_ranking.svg | `03. 典型题深度演练.md:331` — 共享底层 + 多个塔 + 任务权重 | 仅一行文字占位 | 画底部共享 MLP, 顶部 3 个塔 (Watch/Like/Share), 各带 α 权重 |
| ch25_03_realtime_vs_offline.svg | `03. 典型题深度演练.md:24` — 抖音实时 vs YouTube 离线对比 | "概念A/B/C/D"占位条, 无对比 | 画 3 列对比表: 维度/抖音实时/YouTube 离线, 5-6 行 (频率/延迟/部署/主指标/推理/探索) |
| ch25_04_fraud_three_questions.svg | `04. 反欺诈-风控-异常检测.md:21` — 三道题 + 极不平衡 | 仅文字重复标题 | 画顶部 3 类场景 (支付/网络/Spam) + 底部 4 大不平衡处理技术 |
| ch25_04_risk_vs_recommend.svg | `04. 反欺诈-风控-异常检测.md:23` — 镜像关系 | 仅文字重复标题 | 画对比表 6 行: 优化目标/Top-K/多样性/比例/反馈延迟/误判代价, 推荐 vs 风控 |

## ch24 数值分析与凸优化补遗 (14 张)

### REDO_REQUIRED

| 文件 | 上下文引用 | 当前问题 | 重画建议 |
|---|---|---|---|
| ch24_01_condition_number.svg | `01. 浮点与数值稳定性.md:189` — 输入扰动经良态/病态矩阵的放大对比 | 原图是 4 条 "概念A-D" 占位条, 完全无 κ 概念 | 左良态圆球 vs 右病态被拉长椭圆 + 公式 ‖δy‖/‖y‖ ≤ κ(A) × ‖δx‖/‖x‖ |
| ch24_01_float_formats.svg | `01. 浮点与数值稳定性.md:57` — FP32/FP16/BF16/FP8 位布局对比 | 4 条占位条, 无位布局 | 5 行位布局图: s/exp/mant 三色块按真实位数比例, 含精度与动态范围标签 |
| ch24_01_mixed_precision.svg | `01. 浮点与数值稳定性.md:374` — FP32 master + FP16/BF16 + Loss Scaling | 仅 2 行文字, 无流程 | FP32 master → cast → FP16/BF16 → loss → Loss Scaling → grads → unscale 回 master, 含 autocast API 框 |
| ch24_02_cg_vs_sd.svg | `02. 迭代法与稀疏线代.md:434` — CG 相对 SD 的路径对比 | 4 条占位条, 与 CG/SD 无关 | 左 SD 椭圆等高线上之字形路径 (zigzag), 右 CG 沿 A-共轭方向两步直达, 配 κ vs √κ 公式 |
| ch24_02_sparse_attention.svg | `02. 迭代法与稀疏线代.md:438` — Longformer 滑窗 vs BigBird 随机+全局 | 仅 1 行副标题文字 | 上 Longformer 16×16 网格紫色窗口带+橙色全局列; 下 BigBird 三色 (窗口+全局+红色随机点), 含复杂度标注 |
| ch24_02_sparse_formats.svg | `02. 迭代法与稀疏线代.md:436` — CSR / CSC / BSR 存储格式位布局对比 | 4 条占位条, 无存储格式 | 左 4×4 示例矩阵, 中 CSR (values+col_idx+row_ptr 数组), 右 CSC (对称按列), 底 BSR 块结构说明 |
| ch24_03_convex_set_examples.svg | `03. 凸集与凸函数.md:36` — 球凸/环和并集非凸 | 4 条占位条, 完全无关 | 上排凸集 (球/多面体/单纯形/半空间) 绿填充+弦段示例; 下排非凸 (环/两圆盘并/ℤ²/双峰次水平集) 红虚线穿洞 |
| ch24_03_epigraph.svg | `03. 凸集与凸函数.md:86` — 凸函数与它的 epigraph | 4 条占位条, 无几何 | 左 f(x)=x² 凸函数+弦段示例, 右 epi(f) 区域紫填充, 标注 f 凸 ⟺ epi(f) 凸集 |
| ch24_04_duality_gap.svg | `04. 对偶与 KKT.md:108` — 弱对偶/强对偶/Slater | 仅 1 行副标题文字 | 上排数轴: d* ≤ p* 间隙橙色阴影; 下排强对偶 d*=p* 合并点 + Slater 条件框 + 反例注 |
| ch24_04_fenchel_conjugate.svg | `04. 对偶与 KKT.md:476` — 切线截距成 f*(y) | 仅 1 行副标题文字 | 左 f(x)=½x² 配 3 条不同斜率切线, 右 f*(y)=½y² 标对应点; 底 Fenchel-Young 不等式 |
| ch24_05_newton_vs_gd.svg | `05. 二阶方法.md:25` — GD 之字下降 vs Newton 一步跨底 | 仅 1 行副标题文字 | 左 GD 在椭球等高线之字形 (红), 右 Newton 一步沿 H⁻¹∇f 直达 (蓝), 配 κ 复杂度对比 |
| ch24_05_second_order_landscape.svg | `05. 二阶方法.md:473` — 二阶方法生态 Newton→BFGS/LM/K-FAC | 仅 1 行文字 | 树状图: Newton 根 → Quasi-Newton (BFGS/L-BFGS) / Gauss-Newton (LM) / DL近似 (K-FAC/Shampoo/Sophia), 含使用场景条 |
| ch24_06_feasible_paths.svg | `06. 内点法与约束优化.md:26` — 障碍法/投影法/Frank-Wolfe | 仅 1 行文字 | 3 面板同可行多边形: 左紫中央路径(障碍), 中红之字折返(投影), 右橙顶点连线(FW) |
| ch24_06_ml_landscape.svg | `06. 内点法与约束优化.md:460` — LASSO/SVM/Portfolio/NN Verification/Adversarial | 仅 1 行文字 | 2×3 网格: 左经典 (LASSO/SVM/Portfolio), 右现代 (NN Verif/Adv/Phase Retr-MaxCut), 底 CVXPY 落地条 |

---

## ch23 AI Agent 与工具使用 (16 张)

### REDO_REQUIRED

| 文件 | 上下文引用 | 当前问题 | 重画建议 |
|---|---|---|---|
| ch23_01_agent_four_pillars.svg | `01. 什么是 AI Agent.md:73` — LLM Agent 经典四要素 (LLM 大脑 + 工具 + 记忆 + 规划) | 仅一行"大脑+工具+记忆+规划"占位, 无拓扑 | 画中心 LLM 大脑 + 上下左右四要素 (工具/规划/记忆/环境反馈), 含 MDP 闭环 |
| ch23_01_autonomy_spectrum.svg | `01. 什么是 AI Agent.md:119` — Level 0→4 自主性光谱, 能力与失败风险递增 | 仅"Level 0"和"Level 4"两个空框 | 画 5 个 Level 横轴渐变 (绿→红) + 能力/失败风险双轴标签 + Anthropic 铁律卡 |
| ch23_01_ch_relations.svg | `01. 什么是 AI Agent.md:439` — Ch21 对齐 ↔ Ch22 评测 → Ch23 Agent | 仅标题文字 | 画 Ch21/22 顶部双圆, Ch23 底部汇流, 双向箭头, Agent 是放大器注释 |
| ch23_02_reasoning_landscape.svg | `02. Prompt-based 推理与规划.md:36` — CoT → SC → ToT → GoT 全景 | "概念A/B/C/D"占位条, 与推理方法无关 | 画 7 种方法 (CoT/SC/ToT/GoT/L2M/ReAct/PoT) 行 + 各自拓扑可视化 + P(y\|x) 公式 |
| ch23_02_tot_24game.svg | `02. Prompt-based 推理与规划.md:367` — ToT 在 24 点问题上的搜索树 | 仅标题文字占位 | 画 root→3 一级分支 (13-9=4/10-4=6/9+4=13) → 展开二级, 标注 V 分数与剪枝, GPT-4 4%→74% |
| ch23_02_reason_step_composition.svg | `02. Prompt-based 推理与规划.md:572` — Agent Loop 中 reason 步的组合 | "概念A/B/C/D"占位, 无 reason/组合 | 画 ReAct 中心循环 (Thought/Action/Obs) + 上方 6 种 reason 方法卡片 + 实战模板 |
| ch23_03_llm_needs_tools.svg | `03. 工具使用与函数调用.md:26` — LLM 只会说 vs 用工具会做 | 仅一行文字占位 | 画左红框"LLM 4 大短板" + 右绿框"工具 3 大收益" + 中间数学公式 P_tool 确定性 |
| ch23_03_tool_retrieval.svg | `03. 工具使用与函数调用.md:357` — embedding 空间 top-k 选工具 | "概念A/B/C/D"占位, 无 embedding 空间 | 画椭圆 embedding 空间 + v_q 中心 + top-k 圈 + 近 3 工具 (绿) + 远 ~10 工具 (灰) + 5 步流程 |
| ch23_04_mcp_architecture.svg | `04. 模型上下文协议 MCP.md:85` — Host 内嵌 Client, Client 连 Server | "Host 内嵌多个 Client..."文字截断 | 画 Host 容器框 + LLM 圆 + 3 个 Client + 3 个 Server (filesystem/github/postgres), 1:1 虚线, JSON-RPC 标签 |
| ch23_04_mcp_nxm_vs_npm.svg | `04. 模型上下文协议 MCP.md:25` — N×M (Function Calling) vs N+M (MCP) 复杂度对比 | "概念A/B/C/D"占位 | 画左红框 4×4 网格 16 adapter, 右绿框 N Client + M Server + MCP 协议总线 |
| ch23_05_mas_topologies.svg | `05. Multi-Agent 编排系统.md:57` — Sequential/Hierarchical/P2P/Debate 四模式 | 4 个错位叠加框, "Debate"挤在 P2P 内 | 画 2×2 网格: Sequential (3 节点箭头) / Hierarchical (Manager→3 Workers) / P2P (4 节点网状) / Debate (3 节点→投票) |
| ch23_06_prod_arch.svg | `06. Agent 生产落地.md:490` — FastAPI + Redis + Postgres + Vector DB + Celery + K8s + Observability | "FastAPI+Redis+Postgre"截断文字 | 画分层架构: 客户端→网关→Agent Runtime→(LLM/Embed/Rerank)→(Redis/PG/Vector)→(Celery/沙箱/MCP)→(K8s/Observability) |
| ch23_06_prod_pillars.svg | `06. Agent 生产落地.md:30` — Demo→Production 九座桥梁 | 仅一行文字占位 | 画 Demo(蓝)/Production(红)双圆 + 9 卡片桥 (状态/记忆/沙盒/成本/延迟/可观测/错误/测试/部署), 含底部心法条 |
| ch23_07_voyager.svg | `07. 前沿方向.md:60` — Voyager 三大机制 (自动课程/技能库/迭代 prompting) | 仅一行文字占位 | 画左侧 GPT-4 大脑 + 右侧三大机制框 (紫课程/橙技能库/青迭代) + 底部公式 |
| ch23_07_computer_use.svg | `07. 前沿方向.md:221` — 截图→VLM→坐标→执行→新截图 | 5 个空矩形平铺, 无 Computer Use 细节 | 画 5 步骤流程 (青/蓝/紫/橙/绿) + ReAct 循环回到底部 + JSON tool_call 代码 + 三大短板 |
| ch23_07_embodiment_ladder.svg | `07. 前沿方向.md:336` — 沙盒→浏览器→桌面→机器人阶梯 | 4 个相同框平铺, 缺 text-only 与 mobile | 画 6 级阶梯 (text-only→沙盒→Web→桌面→Mobile→机器人 VLA), 渐变底色, 顶部升级箭头 |

---

## ch19 应用 AI (13 张)

### REDO_REQUIRED

| 文件 | 上下文引用 | 当前问题 | 重画建议 |
|---|---|---|---|
| ch19_01_finance_map.svg | `01. AI 在金融.md:413` — 整体场景地图 | 仅"概念A/B/C/D"占位条, 不反映金融 AI 场景 | 中心"金融 AI"圆 + 6 个卫星域: 风控/量化/信贷/智能投顾/NLP-BloombergGPT·FinGPT/RegTech |
| ch19_03_generation.svg | `03. 药物发现.md:143` — 分子生成四种范式 | 标题对了, 但 4 个概念条全部占位 | 画 4 卡片: VAE潜空间/GAN图生成/Diffusion去噪/Transformer自回归, 各含代表论文+视觉示意+优劣 |
| ch19_03_leverage.svg | `03. 药物发现.md:400` — 研发漏斗 x1000 / x10 / 几乎无 | 仅标题+副标题文字, 无漏斗 | 画 4 段漏斗: 前期候选生成×1000 (绿) → ADMET×10 (蓝) → 临床前×1.5 (橙) → 临床试验≈1× (红) |
| ch19_03_pipeline.svg | `03. 药物发现.md:21` — 靶点→命中→先导→临床前→临床+ AI 加速点标注 | 5 个方框只写名称, 无 AI 加速标注 | 5 节点流水线 (绿/绿/橙/灰/红 颜色随 AI 杠杆递减), 顶部 AI 大/中/小/几乎无 标签 |
| ch19_03_retrosynthesis.svg | `03. 药物发现.md:282` — 目标分子→MCTS→起始原料, 反应模板与可行性得分 | 三方框线性, 无 MCTS 树/分数/可购性 | 画 MCTS 树: 根=目标分子, 3 反应分支 (含 score), 每分支再展开反应物, 右侧 Stock 库存表 (✓可购/✗难获取/⚠反应不可行) |
| ch19_04_agent_landscape.svg | `04. 智能体系统.md:524` — 上/中/下三层生态 | 仅 1 中心节点+1 下层节点, 完全不反映三层生态 | 画三层: 上 (GPTs/Claude Desktop/Apple Intelligence/Computer Use), 中 (Agentforce/Copilot/通义/百度), 下 (MCP/LangGraph/CrewAI/AutoGen) |
| ch19_04_agent_loop.svg | `04. 智能体系统.md:27` — ReAct 推理-行动-观察闭环 | 仅标题文字, 无循环结构 | 中心 LLM 圆 + Thought/Action/Observation 三个气泡 + Tools 外部, 闭环箭头标注 (Thought→Action→Observation→回到 LLM) |
| ch19_04_rag_agent_pipeline.svg | `04. 智能体系统.md:396` — RAG 检索 + Agent 工具调用 | 仅标题文字重复 | 画两大区块: 左 RAG (用户问题→Embedding→向量库→Top-K), 右 Agent (LLM 脑→get_order/initiate_refund 工具), 中间连接"注入" |
| ch19_05_chest_xray_pipeline.svg | `05. 医疗健康.md:30` — X 光 → DenseNet-121 → 14 类 + Grad-CAM | 3 个方框仅文字, 无 DenseNet/14 类/热图 | 4 阶段: X 光缩略图 → DenseNet-121 密集块+论文 → 14 类标签+概率条 → Grad-CAM 热图叠加右下肺野 |
| ch19_05_da_vinci.svg | `05. 医疗健康.md:223` — 主控台→主控电脑→床旁 4 臂 + AI 子任务 | 3 个方框仅文字, 缺主控台/4 臂/AI 子任务 | 主控台 (医生+3D 视觉+主手柄) → 主控电脑 (视频处理/抖动过滤/缩放) → 4 臂机械臂 (含 7-DoF 腕式器械 + 病人床) + 底部 AI 子任务模块 (缝合/打结/STAR) |
| ch19_05_dice_iou.svg | `05. 医疗健康.md:69` — Dice 公式 + IoU 对比 | 4 个概念条占位, 与 Dice/IoU 无关 | 左 Venn (P ∩ G 交集高亮) + 中 Dice 公式 (2·\|P∩G\|/(\|P\|+\|G\|)) + 右 IoU 公式 (\|P∩G\|/\|P∪G\|) + 底部关系式 |
| ch19_05_ehr_multitask.svg | `05. 医疗健康.md:185` — 共享 backbone → 4 个任务头 + 加权联合损失 | 2 方框仅文字, 缺 4 个任务头/加权损失 | EHR 输入 → 共享 Backbone → 4 任务头 (死亡 0.93/再入院 0.75/长住 0.85/诊断 0.86), 含各自 AUROC + 底部 ℒ=Σλₖℒₖ 公式 + 外部验证警告 |
| ch19_05_gradcam.svg | `05. 医疗健康.md:463` — 最后卷积层→GAP→加权回传→热图 | 仅 1 个占位框 + 截断文字 | 左胸片+右下肺野红色热斑 + 右 6 步流水线: 输入→前向传播→类别分数→回传求梯度→GAP→加权求和→ReLU 上采样, 含 Lᶜ_GradCAM 公式 |

---

## ch21 对齐、安全与可解释性 (18 张)

### REDO_REQUIRED

| 文件 | 上下文引用 | 当前问题 | 重画建议 |
|---|---|---|---|
| ch21_01_alignment_layers.svg | `01. 什么是对齐.md:39` — 对齐三层次: 意图/价值/能力 | 仅 3 个空方框, 无层级语义和注释 | 画 3 块堆叠层 (意图/价值/能力), 各带解释 + 右侧"层层递进"虚线箭头 |
| ch21_01_goodhart_variants.svg | `01. 什么是对齐.md:114` — 古德哈特四种变体: 回归/极端/因果/对抗 | 仅 1 总览 + 4 子框, 子框均仅文字 | 画 4 列卡片 (回归/极端/因果/对抗), 各含迷你示意: 散点图回归 / 曲线分叉 / 因果 DAG / 优化器搜索漏洞, 顶部"破坏强度递增"箭头 |
| ch21_01_outer_inner.svg | `01. 什么是对齐.md:63` — 外对齐 vs 内对齐 | 仅标题+副标题文字, 无结构 | 上下两区: 上外对齐 (训练目标 L_outer) → 下内对齐 (mesa-objective) → 底部左右对比 (训练分布 vs 分布外发散) |
| ch21_02_bradley_terry.svg | `02. RLHF-DPO 深入.md:37` — Bradley-Terry 从比较重建奖励 | 仅标题+副标题 | 左公式卡片 (P(y_w≻y_l\|x)=σ(r_w-r_l) + RM loss) + 右 Sigmoid 曲线图 (y_w/y_l 标注 + Δr 箭头) + 平移/尺度性质注 |
| ch21_02_rlhf_pipeline.svg | `02. RLHF-DPO 深入.md:137` — SFT→RM→PPO 三步流水线 | 仅 3 个空方框 SFT/RM/PPO | 3 步骤彩色框 + 数据流说明框 (提示-回复/偏好对/KL约束目标) + 底部汇聚"对齐模型 π_θ" |
| ch21_02_dpo_family.svg | `02. RLHF-DPO 深入.md:268` — DPO/IPO/KTO/SimPO loss 形状对比 | "概念A/B/C/D"占位条, 与 DPO 无关 | 4 行 loss 曲线: DPO −logσ 饱和 / IPO MSE with margin / KTO 不对称 / SimPO 长度归一化无 ref, 含轴与标注 |
| ch21_03_threat_model.svg | `03. 对抗攻击与越狱.md:21` — 威胁模型三维分类 | 仅总览+子框, 严重缺失 | 三维立方体轴 (信息可见性/介入阶段/攻击目标) + 右侧 6 类典型威胁模型卡片 (FGSM/GCG/backdoor/data leak/steal/DoS) |
| ch21_03_visual_adv.svg | `03. 对抗攻击与越狱.md:92` — FGSM/PGD/C&W 三种视觉对抗样本 | "概念A/B/C/D"占位, 与对抗无关 | 三列: 原图熊猫/对抗样本长臂猿/扰动 δ 放大显示 + 底部 3 方法对比卡片 (单步/迭代优化/最小 L2) |
| ch21_03_gcg.svg | `03. 对抗攻击与越狱.md:201` — GCG 攻击 4 步流程 | 仅 3 个空方框 (缺 Step 4) | 2 步 (反向传播 + Top-K/抽样) 上排 + Step 4 前向验证下排 + 反馈回环箭头 + 底部目标公式 |
| ch21_03_prompt_injection.svg | `03. 对抗攻击与越狱.md:255` — 间接提示注入 4 阶段流程 | 仅 4 个空方框 (用户/Agent/恶意文档/工具链) | 4 节点流程 + 中间黄色背景框显示"隐藏恶意内容" + 右侧"信任边界模糊"警告 |
| ch21_04_three_gens.svg | `04. 机制可解释性入门.md:32` — 三代可解释性范式演化 | 仅 3 个空方框, 文字截断 | 3 卡片横向: 第一代 saliency / 第二代 probing / 第三代 circuit mech interp, 含代表方法+局限注释 |
| ch21_04_superposition.svg | `04. 机制可解释性入门.md:187` — n 个特征方向在 d 维空间叠加 | "概念A/B/C/D"占位, 与叠加无关 | 中心 12 条彩色特征向量呈辐射状嵌入 2D 单位圆 (投影) + 底部 JL 引理 + 多义神经元后果说明 |
| ch21_04_ioi_circuit.svg | `04. 机制可解释性入门.md:302` — IOI 电路 7 类头协作 | "概念A/B/C/D"占位 | 5 节点主流 (Token Embed→Duplicate→Prev Token/S-Inhibition→Name Mover→Mary) + 旁挂 Backup/Negative + 底部层分布轴 + ablate 验证条 |
| ch21_05_ioi_heatmap.svg | `05. 可解释性工具与实战.md:126` — 12×12 head grid 中 name mover 亮点 | 仅标题+副标题 | 12×12 热力图 (高亮 L9-L10 + 部分 L7-8) + 右侧图例 (颜色梯度 + 4 类头标注) + 复现脚注 |
| ch21_05_sae_pareto.svg | `05. 可解释性工具与实战.md:233` — SAE 变体 Pareto 曲线 | "概念A/B/C/D"占位, 与 SAE 无关 | 折线图: X=L₀, Y=variance explained, 3 曲线 (vanilla L1 虚线灰 / Top-K 绿 / JumpReLU 红最高) + 甜点区 + 图例 |
| ch21_06_cai_pipeline.svg | `06. AI 安全治理与前沿.md:167` — Constitutional AI 两阶段流水线 | 仅标题+副标题 | 左右两区: SL-CAI (红队 prompt→生成→批评→改写→SFT M₁) + RL-CAI (双采样→评审→AI偏好训 R_φ→PPO→M₂) + 跨阶段箭头 |
| ch21_06_scalable_oversight.svg | `06. AI 安全治理与前沿.md:94` — Debate/RRM/IDA 结构差异 | 3 错位叠加框, 文字截断 | 3 列对比卡: Debate (2 debater + 1 裁判) / RRM (递归塔 R₂→R₁→R₀) / IDA (人协调→放大→蒸馏) + 共用底部天花板警告 |
| ch21_06_sleeper_agent.svg | `06. AI 安全治理与前沿.md:249` — Sleeper Agent 训练/部署对比 | "概念A/B/C/D"占位 | 左右两阶段: 训练 (year=2024 正常 / year=2023 含漏洞 → SFT+RLHF+CAI 学到条件性行为) + 部署 (正常触发正常 / 真实用户 2023 → 触发漏洞) + 红色警戒条 |

## ch22 LLM Evaluation 方法学 (18 张)

### REDO_REQUIRED

| 文件 | 上下文引用 | 当前问题 | 重画建议 |
|---|---|---|---|
| ch22_01_benchmark_saturation.svg | `01. 为什么 Eval 是 LLM 的圣杯.md:139` — 随模型能力提升, benchmark 从高区分度→饱和→污染 | 4 条"概念A-D"占位条 | 画 2D 折线图 (横轴时间/世代, 纵轴分数), MMLU reported 蓝实线 + 含污染 reported 红虚线 + 90% 饱和横线 + 三段色块标注 (高区分度绿/逼近饱和橙/污染主导红), 底部 Goodhart 注 |
| ch22_01_three_uses.svg | `01. 为什么 Eval 是 LLM 的圣杯.md:34` — 诊断/决策/信任的目标与冲突 | 仅 1 行副标题文字 | 3 列彩色卡片: 诊断(蓝·信号灵敏)/决策(绿·可比较)/信任(橙·可审计防作弊), 每列含目标/要求/常见形态 + 底部"灵敏→防作弊"张力箭头 |
| ch22_02_bertscore_vs_bleu.svg | `02. 传统 NLP 指标.md:300` — BERTScore 保住相似度, BLEU 在同义替换下崩塌 | 4 条概念条占位 | 顶参考/候选对 ("小猫在垫子上"vs"猫咪坐在毯子上"), 下方双面板 BERTScore F=0.92 绿 vs BLEU-4 ≈ 0.00 红, 各含方法简述与优缺 |
| ch22_02_perplexity.svg | `02. 传统 NLP 指标.md:91` — 模型在几个候选 token 之间的平均"摇摆度" | 4 条概念条占位 | 左右两柱状图 (10 候选 token): 左绿色集中分布 PPL≈8, 右红色平摊 PPL≈320 + 底部公式框 exp(−1/N·Σ log p) + "跨模型不可比, 同模型不同数据可纵比" |
| ch22_03_benchmark_timeline.svg | `03. 现代 Benchmark 体系.md:44` — GLUE→MMLU→SWE-Bench 范式演进时间线 | 仅 1 行副标题文字 | 横向时间线 (2018-2025), 6 个 benchmark 节点 (GLUE蓝/SuperGLUE青/MMLU紫/HumanEval绿/MT-Bench橙/SWE-Bench红), 顶部阶段标注 (分类→推理→agent) + 底部 3 范式阶段卡片 |
| ch22_03_pass_at_k_variance.svg | `03. 现代 Benchmark 体系.md:384` — pass@k 无偏估计 vs 直接采样方差对比 | 4 条概念条占位 | 左绿面板: n=100,k=10 无偏估计 → 方差≈0.012, 5 次重复窄带; 右红面板: n=k=10 朴素估计 → 方差≈0.21, 5 次重复散开; 底部紫色提示框"n ≥ 10k" |
| ch22_04_benchmark_vs_arena.svg | `04. 竞技场与人类偏好.md:33` — 从 benchmark 分数到 pairwise 偏好投票的范式对比 | 4 条概念条占位 | 左蓝面板 benchmark (MMLU/GPT-4-class): 流程+leaderboard 模拟 + 优(-)可复现/离真实用户远; 右橙面板 Arena: 匿名对局+投票+BT-MLE → rating, 优(-)真用户/慢/匿名易被猜 |
| ch22_04_chatbot_arena_flow.svg | `04. 竞技场与人类偏好.md:222` — 匿名 pairwise 投票 UI 与 rating 拟合流程 | 4 条概念条占位 | 4 阶段流程: 用户 prompt → 后端随机路由 → 匿名并排 UI (A/B 候选 + 3 投票按钮) → BT-MLE 拟合 + Leaderboard (GPT-4o 1287 / Claude 3.5 1265) |
| ch22_04_internal_arena_pipeline.svg | `04. 竞技场与人类偏好.md:414` — 内部 Arena 采集→BT-MLE→leaderboard 端到端流水线 | 4 个错位蓝框, 文字"leaderboard 展示的端到端"挤在第 3 块 | 5 阶段彩框 (青/紫/蓝/绿+5a Style Control 回归/5b 红 Leaderboard) 配底部 pitfall 注释 (匿名/卫生/不报 CI) |
| ch22_05_human_vs_llm_judge.svg | `05. LLM-as-Judge.md:36` — 人类 vs LLM 判分的成本/一致性/速度三维对比 | 4 条概念条占位 | 表格 4 行 (单人类/$3/MT-Bench 3 人/$9/GPT-4 2024/$0.03/GPT-4o 2024末/$0.01), 每行含一致性色条 + 综合判定 + 底部 3D 轴向图 (成本↓/一致性↑/速度↑) |
| ch22_05_judge_biases.svg | `05. LLM-as-Judge.md:271` — 五大偏差 (position/verbosity/self/family/phrasing) 与校正 | 1 行副标题 + 标题截断 | 5 行彩色卡片: position 红 (swap-avg) / verbosity 紫 (LC-AlpacaEval) / self 橙 (跨家族) / family 青 (异族集) / phrasing 灰 (锁版本), 每行含现象+校正 |
| ch22_05_multi_judge_jury.svg | `05. LLM-as-Judge.md:419` — 多 LLM 集成 judge (jury) 的架构 | 4 个错位蓝框 | 3 阶段彩框: 输入 → 独立判分 (3 judge + swap-and-average, AB/BA×2) → 加权投票 (w ∝ κ) → 最终裁决; 底部集成收益上限表 (Verga 2024: 1→3 +4%, 3→5 +1%, 5→10 ≈0) |
| ch22_06_contamination_types.svg | `06. Contamination.md:25` — 三种污染形式 (exact/near-dup/web scrape), 严重度递减/检测难度递增 | 4 条概念条占位 | 3 列卡片 (exact 红 ⭐⭐⭐⭐⭐ + n-gram 易 / near-dup 橙 ⭐⭐⭐ + 嵌入中 / web-scrape 紫 ⭐⭐⭐⭐ + cutoff 对比极难) |
| ch22_06_five_defenses.svg | `06. Contamination.md:450` — 五道防线 (held-out/时间戳/canary/rephrase/动态) | 仅 1 行副标题文字 | 5 行堆叠卡片 (蓝/青/紫/橙/绿), 每行编号 + 名称 + 简述 + 校正手段, 底部"5 道防线叠加才够" |
| ch22_06_static_vs_live_benchmark.svg | `06. Contamination.md:308` — 静态 vs 活体 benchmark 污染风险时间演化 | 仅 1 行副标题文字 | 双折线图 (横轴时间): 红实线静态 reported 飙升至 100% + 紫虚线含污染 reported 更高 + 绿平线活体真能力恒定; 区域标注污染扩张区, 旁注 LiveCodeBench 实测差 20pp |
| ch22_07_agent_eval_landscape.svg | `07. 前沿方向.md:237` — 从 SWE-Bench 到 WebArena/OSWorld/GAIA 的能力面覆盖 | 5 个错位蓝框, 文字"GAIA 通用助手的能力面覆盖"挤在第 4 块 | 4 列彩卡 (SWE-Bench 蓝代码/WebArena 绿浏览器/OSWorld 紫桌面/GAIA 橙通用), 每列含来源/题数/验证/代表模型数字, 底部"每一列代表一种环境, AgentBench 综合" |
| ch22_07_helm_radar.svg | `07. 前沿方向.md:39` — HELM 42 场景 × 7 维度雷达图, 单一 leaderboard 转多维权衡 | 4 条概念条占位 | 中央 7 轴雷达图 (accuracy/robust/fairness/bias/toxicity/efficiency/calibration), 双折线 (GPT-4o 蓝实线 vs Claude 3.5 红虚线) + 右侧图例盒 + 底部加权平均公式 |
| ch22_07_multimodal_ladder.svg | `07. 前沿方向.md:370` — 多模态评测能力层级 (MMBench→MathVista→MMMU→Video-MME) | 5 个错位蓝框, 文字"Video-MME 时序推理"挤在第 4 块 | 4 阶梯彩卡 (低到高): MMBench 蓝识别 (矮) → MathVista 绿视觉数学 → MMMU 紫专业推理 → Video-MME 红视频时序 (最高), 每级含数字示例 + 箭头升级 + 底部"模态演化阶梯" |

## ch20 前沿 AI (23 张)

### REDO_REQUIRED

| 文件 | 上下文引用 | 当前问题 | 重画建议 |
|---|---|---|---|
| ch20_01_bloch_sphere.svg | `01. 量子机器学习.md:34` — 单 qubit 在 Bloch 球上的几何 (北极 \|0⟩, 赤道叠加, 任意门 = 旋转) | 仅标题重复, 无球体/轴/向量 | 中心半径 120 单位球 + 3 正交轴 (x/y/z 灰) + 态向量 \|ψ⟩ 红色箭头从球心出发指向 |θ,φ| + θ/φ 角弧 + 极轴标签 \|0⟩/\|1⟩ + 右侧参数化公式与几何直觉列表 |
| ch20_01_bell_circuit.svg | `01. 量子机器学习.md:140` — Bell 态制备电路 \|00⟩ → H → CNOT → M | 仅标题文字, 无电路图 | 两条 qubit 横线 (q₀/q₁), H 蓝盒 + CNOT (控制点+靶 X+圆) + 两个 M 测量 + 末态 Φ⁺ = (\|00⟩+\|11⟩)/√2 + 底部采样直方图 (00=49.8, 11=50.2, 01≈10=0 纠缠证据) |
| ch20_01_barren_plateau.svg | `01. 量子机器学习.md:333` — 损失函数景观高维几乎平坦, 梯度消失 | 4 条"概念A-D"占位条, 与 barren plateau 无关 | 左"浅电路 (n 小)" 显示带极小点的波浪损失面 + "梯度有信号", 右"深/宽电路" 几乎平坦红色损失面 + "梯度≈0" + 底部公式 Var[∂L/∂θᵢ] ~ O(b⁻ⁿ) |
| ch20_02_neuron_dynamics.svg | `02. 神经形态计算.md:85` — 膜电位动力学: 接收输入 → 积分 → 阈值触发 spike → 重置 | 仅 4 个方框+箭头, 无电位曲线 | 顶部膜电位曲线 (绿色 rest 线 + 红色阈值线 + 蓝色积分曲线 + 3 个红色 spike 标注) + 底部 4 阶段流程框 (I→V→spike→reset) |
| ch20_02_izhikevich_modes.svg | `02. 神经形态计算.md:137` — LIF 只能 regular spiking, Izhikevich 可复现 bursting/chattering 等 | "概念A-D"占位条 | 顶 LIF 单条 regular 轨迹; 下 Izhikevich 4 模式小图: regular (蓝) / fast (青) / bursting (橙) / chattering (紫) + 底部公式 + 低阈值/适应模式 |
| ch20_02_rate_coding.svg | `02. 神经形态计算.md:211` — 输入值越大, 神经元 spike 越密 | 仅标题+副标题文字 | 顶部斜坡输入信号 + 4 个神经元 row (低/中/高/最高), spike 数 5→9→15→55, 视觉上 spike 密度递增 |
| ch20_02_stdp_window.svg | `02. 神经形态计算.md:222` — Δt>0 → LTP, Δt<0 → LTD (Bi & Poo 1998) | 3 方框文字截断 | 上行 pre/post 时序示意 (Δt>0 与 Δt<0 各自 spike 对); 下行 Δw vs Δt 曲线 (右侧 LTP 绿指数衰减, 左侧 LTD 红指数衰减); 底部公式 |
| ch20_02_surrogate_gradient.svg | `02. 神经形态计算.md:332` — 前向硬 spike, 反向平滑替代梯度 | "概念A-D"占位 | 坐标系 x=V-V_th, y=S/∂S, 蓝色硬阶跃 + 橙色 arc-tan 平滑替代曲线 (Neftci 2019) + 底部前向/反向 BPTT 流程框 |
| ch20_02_hardware_timeline.svg | `02. 神经形态计算.md:453` — Mead 1990 → NorthPole 2023 神经形态芯片时间线 | 仅标题+副标题 | 横向时间轴 (1990→2023), 7 个节点上下交替: Mead 1990 模拟 / BrainScaleS 2010 / TrueNorth 2011 / Loihi 1 2017 / Tianjic 2019 / Loihi 2 2021 / NorthPole 2023, 各带颜色框 + 底部 3 时代标注 |
| ch20_02_event_vs_frame.svg | `02. 神经形态计算.md:477` — 静止场景下传统相机反复输出相同画面, 事件相机完全静默 | 仅标题+副标题 | 顶部"静止场景"剪影; 下半双栏: 左传统相机 30-120 fps 全帧 (11 个重复方块) + 摘要; 右 DVS 完全静默虚线 + 摘要; 底部比较条 (1µs / 120dB / <10mW) |
| ch20_03_orbit_dc_architecture.svg | `03. 太空数据中心.md:374` — 太阳能板、辐射板、星间激光链路、地面站 | 1 个矩形占位框 | 黑色太空背景 + 中央卫星 (主体+左右太阳板+底部辐射板) + 右上地球+地面站 + 左上太阳+通量箭头 + 左侧另一卫星连激光束 (红色 ISL) + 底部系统要素摘要 |
| ch20_03_seu_tmr.svg | `03. 太空数据中心.md:376` — 单粒子翻转 1→0 + TMR 三副本多数表决 | 仅标题+副标题 | 左 SEU: 粒子射线紫色斜线射入存储单元, 数字翻转 1→0, 标注"1→0 翻转!"; 右 TMR: 3 副本 A=1/B=0/C=1 → 投票器三角形 → 输出 1, 底部 LEO 翻转率公式 |
| ch20_03_radiator_curve.svg | `03. 太空数据中心.md:378` — Stefan-Boltzmann P~AT⁴ | "概念A-D"占位 | 坐标系 x=温度°/y=功率W/m², 三条 T⁴ 曲线 (A=0.25/0.5/1.0 m² 蓝/绿/红), 右侧标签 + 底部公式 P=εσA(T⁴-T_env⁴) |
| ch20_04_decentralised_ai_motivation.svg | `04. 去中心化 AI.md:42` — 四大动机: 数据垄断/隐私/数据孤岛/反集权 | 仅标题+副标题 | 2×2 四宫格彩卡: ①数据垄断(红) ②隐私合规(橙) ③数据孤岛(紫) ④反集权(绿), 各含一行现象与一行斜体解释 |
| ch20_04_fedavg_round.svg | `04. 去中心化 AI.md:95` — FedAvg: 本地训练→上传梯度→服务器聚合→下发新模型 | 4 占位框扁平 | 上排 3 客户端 (A/B/C 蓝/绿/橙) + 中部紫色协调服务器带加权公式 + 上下箭头 (灰色上传/绿色下发) + 底部红条"原始数据 D_A,B,C 从不出本地" |
| ch20_04_crypto_tech_compare.svg | `04. 去中心化 AI.md:186` — PoW/PoS/DPoS/BFT 共识机制对比 | "概念A-D"占位条 | 5 行对比表: 表头深灰, 4 行共识 (黄PoW极高算力 / 绿PoS低 / 蓝DPoS联盟 / 紫BFT许可), 列含 TPS/出块/特点 |
| ch20_04_blockchain_ai_stack.svg | `04. 去中心化 AI.md:250` — 区块链 × AI 数据/计算/共识/应用分层 | 4 占位框错位 | 自下而上 4 层梯形: 数据(蓝)→计算(绿)→共识(红)→应用(紫), 左侧竖条标签, 每层带代表性项目 (FATE/Bittensor 等) + 右侧"用户/合规/算力/数据"四问 |
| ch20_04_china_ecosystem.svg | `04. 去中心化 AI.md:289` — BSN/长安链/蚂蚁链 + FATE/KubeFATE + 隐语等 | 仅标题+副标题 | 三列 (基础设施蓝/联邦框架绿/隐私计算橙), 各 3 卡片 (BSN/长安链/蚂蚁链, FATE/KubeFATE/云厂商 PAI, 隐语/瑶光/行业联盟), 底部"路径"总结条 |
| ch20_05_bci_taxonomy.svg | `05. 脑机接口.md:36` — BCI 三大门派: 侵入/半侵入/非侵入 | "概念A-D"占位 | 侧视大脑剪影 (颅骨+头皮+沟回) + 红色 Utah Array 针刺入皮层 + 橙色 ECoG 网格贴在皮层 + 绿色 EEG 电极在头皮外 + 三色引线 (侵入/半侵入/非侵入) + 底部 3 卡片总结 |
| ch20_05_eeg_1020.svg | `05. 脑机接口.md:116` — EEG 10-20 标准电极分布 | "概念A-D"占位 | 头顶俯视圆: Fp1/Fp2 红(额极)/F3 Fz F4 蓝/ C3 Cz C4 绿 / P3 Pz P4 紫 / O1 O2 橙 / T3 T4 青 (10-20 坐标), 加鼻根/枕骨标签 |
| ch20_05_snr_comparison.svg | `05. 脑机接口.md:75` — Utah Array / ECoG / EEG / MEG SNR 对比 | "概念A-D"占位 | 对数横轴 -10~30 dB, 5 横条: 皮层内 LFP/SUA 红(~20dB) / ECoG 橙(~12dB) / fNIRS 紫(~3dB) / MEG 青(~5dB) / EEG 绿(~0dB), 底部 SNR 公式与"非侵入式需三维滤波"提示 |
| ch20_05_stentrode_path.svg | `05. 脑机接口.md:99` — Stentrode 经颈静脉→上矢状窦→运动皮层 | 3 方框文字截断 | 4 阶段流程卡: ①颈静脉入路(红) ②经锁骨下静脉导管(橙) ③上矢状窦(蓝脑+血管) ④撑开在血管壁(绿含 16 电极触点), 底部传统开颅 vs Stentrode 微创对比卡 |
| ch20_05_bci_llm_pipeline.svg | `05. 脑机接口.md:272` — 神经→RNN 解码→beam search→LLM 纠错 | 标题重复文字 | 5 阶段彩框流水线: ①神经采集(蓝) ②预处理(绿) ③神经编码器(橙) ④Beam search(红) ⑤LLM 纠错(紫), 含公式与 CER/WER + 中部"TAR WAHTER BOTEL → The water bottle"示例 + 底部"LLM 承担语言先验"注 |

---


