# 翻译规范手册 (Translation Guide)

> 本手册面向全部译者 agent。**任何翻译动作前必须完整通读一次**，违规产出将被主编 reject。
> 目标：20+ 译者协作时，读者感受到"像一个人写的"。

---

## 0. 项目背景速览

- 原书：*Maths, CS & AI Compendium* by Henry Ndubuaku
- 风格：直觉先行、大量口语化比喻、公式与代码密集、面向"想真正搞懂"的实践者 (不是应试)
- 面向读者：有基础 Python + 高中数学的 AI/ML 从业者与学生
- 中文版定位：**不是学术翻译，是"让中文读者读得津津有味的技术散文"**

---

## 1. 信达雅三原则 (硬核心)

### 1.1 信 (Fidelity) — 技术零失真

- **数学公式 100% 原样保留**。`$...$` `$$...$$` 内的一切 LaTeX 源码不改一字符
  - 变量名不改 (不要把 $x$ 翻成 $x_{中文}$)
  - 符号不改 ($\mathbb{R}^n$, $\mathbf{a}$, $\nabla$ 都保留)
  - 公式内即使有英文单词 (如 $\text{softmax}$)，也**不动**
- **代码块 100% 原样保留**，变量名/函数名/字符串不译，**仅可翻译代码内注释**
- **数据/引用/公式编号**保持一致
- 事实性内容 (人名、年份、机构、论文标题) 严格照原文对齐，不"美化"、不添油加醋

### 1.2 达 (Clarity) — 中文顺畅

- **长英文从句必须拆**。一句英文 40+ 词的 relative clause，拆成 2-3 个短中文句
- 主动语态优先。"is called" → "叫做" / "被称为" 二选一，别用"其被称之为"
- 避免翻译腔 red flags:
  - ❌ "作为一个 X，我们..." → ✅ "作为 X，我们..." (删多余的"一个")
  - ❌ "这是一件非常重要的事情" → ✅ "这很重要"
  - ❌ "对于 X 来说，它是..." → ✅ "X 是..."
  - ❌ "让我们来看看..." → ✅ "来看..." / "我们看..."
- **一句一想法**。原文一句里塞了三个概念，中文分三句

### 1.3 雅 (Register) — 保住"作者的声音"

- 原作口语化，中文也**口语化**。作者写 "Think of a Vector Space as a specific kind of playground"，就要翻成"把向量空间想象成一个特别的乐园", **不要**翻成"向量空间可被视为一种特定的数学游乐场"
- 常用亲切语气词:
  - "我们..." (we) — 拉近距离，全书统一
  - "想象一下..." / "把它想成..." — 对应 "Think of / Imagine"
  - "现在..." — 对应 "Now" 起头
  - "注意..." / "别忘了..." — 对应 "Note that"
  - "就是..." / "无非就是..." — 对应 "just / simply"
- 允许保留原作个人化表达 (如 "我 14 岁时..." 这类叙事)，用第一人称直译
- 谚语/比喻：优先保留原味，加译注；只有直译完全不懂时才意译

---

## 2. 格式硬约束 (Zero Tolerance)

违反以下任一条 = 主编直接打回重译。

| # | 约束 | 例子 |
|---|-----|------|
| F1 | `$...$` 与 `$$...$$` 内**一个字符都不能改** | `$\mathbf{a} = [a_1, a_2]$` 原样 |
| F2 | ` __PN_SENTINEL_0__ ` 代码块整块保留，只译**代码内注释** | Python `# compute norm` → `# 计算范数` |
| F3 | 图片语法 `![alt](../../images/xxx.svg)` **路径不改**, alt 文本译中文 | `![向量 a 在 3D 空间中的绘制](../../images/vector_3d.svg)` |
| F4 | Markdown 标题层级 `#`/`##`/`###` **完全对齐**原文数量（排除 F12 认可的学习增强块） | 原文 `## Overview` → 译文 `## 概览` (仍两个 `#`)；增强块中的标题不参与结构计数 |
| F5 | Admonition `!!! note` / `!!! warning` / `!!! tip` 标记保留，只译标题与内容 | `!!! note "关键点"` |
| F6 | 列表符号 `-` / `*` / `1.` 与缩进层级严格保持（排除 F12 认可的学习增强块） | 原缩进 4 空格，译文也 4 空格；增强块中的列表不参与结构计数 |
| F7 | 行内代码 `` `variable_name` `` 保留原文，不译 | `` `numpy.dot()` `` |
| F8 | 链接 `[text](url)` 中 URL 不改，文字可译 | `[点这里](https://example.com)` |
| F9 | 表格结构 (行数列数分隔线) 保持一致，仅译单元格内容 | |
| F10 | 空行数量与段落结构对齐原文 (影响 markdown 渲染) | |
| F11 | 章节文件名 (中文目录) 已按主编约定，译者**不新建/改名** | |

### F12 原文覆盖与中文扩展 — 一一对应是底线

中文版**可以比原文更丰富**：可增加帮助理解的解释、例子、章节导览、总结、要点与译注；但每个原文信息单元必须在译文中保留可追溯的一一对应。

- 原文标题、正文段落、列表项、表格项、admonition、公式、代码、图片与链接不得漏译、以概述替代、倒置或改变原意。
- 新增内容不得无依据杜撰事实，也不得伪装成原作译文。
- `一句话总结`、`本章导览`、`本节要点` 是本手册规定的学习增强块。
- 其他新增解释、例子或断言必须以 `> **补充说明**:` 或 `[译注:]` 标记。
- 验收以“增强块之外的原文信息单元按顺序一一对应、增强块内新增内容不替代原文”为准；标题和列表结构比较排除 F12 认可的学习增强块，不以中文与原文的行数、标题数或列表数完全相等为准。

**Verifier 规则 ID**：P0 阻断项为 `P0-FILE-MAP`、`P0-SOURCE-COVERAGE`、`P0-MATH`、`P0-CODE`、`P0-ASSET`、`P0-STRUCTURE`；P1 项为 `P1-SEMANTIC`、`P1-UNLABELLED-EXPANSION`；P2 项为 `P2-PUNCTUATION`、`P2-SPACING`。交付证据必须逐项报告这些 ID。

---

## 3. 术语一致性

### 3.1 必读：`zh/GLOSSARY.md`

- **翻译前先 `cat zh/GLOSSARY.md`** 查已有术语约定
- 遇到新术语 → 追加到 GLOSSARY.md (格式 `| English | 中文 | 首次出现章节 |`)
- 同一术语全书**必须**用同一中文译法，冲突时以 GLOSSARY.md 为准
- 如 GLOSSARY.md 尚不存在，创建之，使用下列表头:
  ```markdown
  # 术语表 (Glossary)

  | English | 中文 | 首次出现 | 备注 |
  |---------|------|---------|------|
  ```

### 3.2 首次出现规则

- **首次**出现：`中文译名 (English)` ，例："梯度下降 (gradient descent)"
- 之后统一用中文，除非：(a) 极短的缩写更通用 (如 `MoE`/`SVD`/`GPU`); (b) 代码/公式里
- 无标准中文译法 → 保留英文，段末加**译注脚注** `[译注: xxx 尚无统一中译, 保留原文]`

### 3.3 常见术语参考 (与 GLOSSARY.md 互补，后者为准)

| English | 中文 (推荐) | 语境提醒 |
|---------|-----------|---------|
| vector space | 向量空间 | |
| scalar | 标量 | |
| dot product | 点积 | 不用"内积" (inner product 另用) |
| inner product | 内积 | 抽象空间 |
| norm | 范数 | |
| gradient descent | 梯度下降 | |
| loss function | 损失函数 | 不用"代价函数" |
| feature | 特征 | ML 语境 |
| feature vector | 特征向量 | ⚠️ 数学的 eigenvector 也叫特征向量，见 §8 |
| eigenvector / eigenvalue | 特征向量 / 特征值 | 与 ML feature 同名，用上下文区分，必要时加原文 |
| embedding | 嵌入 | 名词；embedding vector = 嵌入向量 |
| attention | 注意力 | self-attention = 自注意力 |
| transformer | Transformer | 不译，首字母大写 |
| convolution | 卷积 | |
| kernel (CNN) | 卷积核 | |
| kernel (OS) | 内核 | |
| kernel (SVM/method) | 核 (kernel) | 首次出现附原文 |
| pooling | 池化 | |
| backpropagation | 反向传播 | |
| overfitting | 过拟合 | |
| regularisation | 正则化 | |
| MoE (Mixture of Experts) | MoE (专家混合) | MoE 不译；内部 "expert" 译"专家" |
| SSM (State Space Model) | 状态空间模型 (SSM) | |
| RNN / CNN / LLM / VLM | 保留缩写 | 首次出现给全称中文 |
| tensor | 张量 | |
| batch | 批 / 批次 | batch size = 批大小 |
| epoch | epoch | 不译，已成技术黑话 |
| pipeline | 流水线 | 分布式训练语境 |
| playground (数学) | 乐园 | |
| playground (代码调试) | 沙盒 | |
| ablation | 消融 (ablation) | 首次加英文 |

---

## 4. 中文标点规范

### 4.1 正文用全角

| 用法 | 用 | 不用 |
|-----|----|----|
| 句号 | 。 | . |
| 逗号 | , | , (半角) ← ⚠️注意，本手册作者习惯半角，**译者一律用全角 `，`** |
| 冒号 | : | : (半角) → **正文用全角 `：`** |
| 分号 | ; → **`；`** | |
| 问号 | ? → **`？`** | |
| 感叹号 | ! → **`！`** | |
| 引号 | "..." "..." (中文弯引号) | "..." |
| 括号 | (行文) 用半角 `()` 更整齐；但整段中文括号可 `（）` | 团队统一：**半角 `()` 前后加空格** |
| 破折号 | —— (双 em dash) | -- / – |
| 省略号 | …… | ... (若原文强调技术省略如代码则保留 `...`) |

> **例外 — 保留英文标点的位置**:
> - LaTeX 公式内部一切标点 (逗号句号等)
> - 代码块 / 行内代码 `` `...` `` 内部
> - 文件路径 / URL / 命令行
> - 数字序列 (1,000 vs 1000；本书统一**不加千分位**)

### 4.2 中英文/数字混排 — **加半角空格**

- ✅ "梯度下降 gradient descent 是一种优化方法"
- ✅ "我们训练了 100 个 epoch"
- ✅ "使用 PyTorch 2.0 版本"
- ❌ "梯度下降 gradient descent 是一种..."
- ❌ "训练 100 个 epoch"

**规则**：中文字符 与 (英文单词 / 阿拉伯数字 / 行内代码) 相邻时，**加一个半角空格**。

**例外**：全角标点前后**不加**空格 (中文标点已含视觉空间)。

---

## 5. 专有名词处理

### 5.1 人名

- **首次**: `中文译名 (English Full Name)`
  - Charles Darwin → 查尔斯·达尔文 (Charles Darwin)
  - Henry Ndubuaku → 亨利·恩杜布阿库 (Henry Ndubuaku)
- **之后**：仅用中文
- 姓名之间的分隔用**中间点 `·`**，不用小圆点或半角句号
- **知名度极高且中文圈更常直接用英文的**，可保留英文：Alan Turing (可译"艾伦·图灵"，也可保留)，团队约定**保留英文形式**减少误译，除非有绝对通用中译 (如爱因斯坦、达尔文、牛顿)

### 5.2 机构 / 产品 / 公司

- 一般**保留原文**: DeepMind, OpenAI, Nvidia, Y Combinator, Google, Meta, Anthropic, GitHub
- 通用中译已牢固的可用中文：谷歌 (Google) — 首次给英文即可，但技术书籍中**建议全书保留英文**以避免歧义
- 硬件/框架名保留原文：PyTorch, TensorFlow, CUDA, Triton, ARM NEON, AVX

### 5.3 创始人 / 名人引言

- 直接引言 (带引号 "...")，中文译文 + **译注 (脚注)** 附原文:
  ```markdown
  达尔文形容自己"不算机灵, 像一个需要时间才能吸收数据的慢处理器"[^darwin-quote]。

  [^darwin-quote]: 原文: "not being quick-witted, feeling like a 'slow processor' who needed time to soak in data."
  ```

---

## 6. 文化梗 / 隐喻 / 幽默处理

- **默认策略**：直译 → 若不通再意译 → 段末加**脚注**说明原文
- 常见坑:
  - `playground` — 数学语境 = "乐园" (原作反复用)；编程 = "沙盒"；儿童场景 = "游乐场"
  - `dark magic` / `black box` — 直译 "黑魔法" / "黑箱" 中文都通
  - `just` / `merely` — 常译"不过是" / "无非" / "就是"，保留轻描淡写口吻
  - `hand-waving` — "含糊带过" / "拍脑袋"，加脚注解释亦可
  - `soak in` (作者原句) — "慢慢吸收"，保留生活化感
- **文化梗** (梗如美国电视剧、体育、政治笑话)：意译 + 脚注
- **谚语**：若中文有对应，用中文谚语 + 脚注附原文

**脚注格式** (统一 `[^tag]` + 段尾定义，每章脚注 tag 独立编号):
```markdown
...原文这里有个双关[^pun-1]。

[^pun-1]: 译注: 原文 "kernel of truth" 一语双关, 既指真相内核也暗指 CNN 卷积核。
```

---

## 7. 每章翻译流程 Checklist (Translator Agent 必执行)

按顺序执行，**每一步都是硬门**。

### 步骤 1：预读 (5-10 min)
- [ ] `cat zh/TRANSLATION_GUIDE.md` (本文件，每次都要重读一遍)
- [ ] `cat zh/GLOSSARY.md` (查已有术语)
- [ ] 通读整章原文一次，标出所有:
  - 未在 GLOSSARY 的新术语
  - 数学公式 / 代码块 / 图片位置 (确认不动)
  - 文化梗 / 隐喻 / 引言

### 步骤 2：术语落地
- [ ] 新术语先追加到 `zh/GLOSSARY.md` (若已有条目则复用)
- [ ] 若与已有译法冲突，**停止翻译**，到 GLOSSARY 讨论区留 issue 待主编裁定

### 步骤 3：逐段翻译
- [ ] 逐段处理，不跳段，不合并段
- [ ] 每段翻完立刻自检：公式动了没？代码动了没？图片路径动了没?
- [ ] 长句 (> 30 中文字) 考虑拆句
- [ ] 保持原文空行 / 缩进

### 步骤 4：自检 (硬门)
- [ ] `diff` 结构：**增强块之外**的标题层级/数量、列表符号/缩进、代码块数量、公式数量、图片数量与原文**完全一致**；F12 认可的学习增强块不计入标题和列表结构比较
  - 可用：`grep -c '^#' src.md` 与 `grep -c '^#' zh/dst.md`
  - `grep -c '```' src.md` 计数代码块围栏 (应为偶数且相等)
  - `grep -oc '!\[' src.md` 计数图片
  - `grep -oc '\$\$' src.md` 计数块公式围栏
- [ ] 中英文/数字之间是否加空格？(spot check 5 处)
- [ ] 中文标点是否全角？(`grep -n ' , ' zh/dst.md` 检查游离半角逗号)
- [ ] 术语是否统一？(grep 新术语关键词，确认全章唯一译法)
- [ ] 首次出现术语是否带英文原文?
- [ ] 脚注是否闭合？(`[^tag]` 与 `[^tag]:` 数量相等)
- [ ] 按原文顺序核对每个原文信息单元，确认**增强块之外**仍按顺序一一对应；增强块只能新增内容，不得替代、重排或省略原文信息单元；不得以行数、标题数或列表数相等代替覆盖核验
- [ ] 所有新增解释、例子或断言均有可见的 `> **补充说明**:` 或 `[译注:]` 标记；`一句话总结`、`本章导览`、`本节要点` 可作为本手册规定的学习增强块
- [ ] 记录 Translation QA verifier 的 P0/P1/P2 结果；任一 P0 失败不得交付，P1/P2 结果必须随交付证据保留

### 步骤 5：交付
- [ ] 输出文件命名规则：`zh/第XX章 - 中文章节名/序号. 中文小节名.md` (与已建目录结构对齐)
- [ ] 提交前跑 markdown lint (若配置)
- [ ] 在 commit message 注明：`translate(chXX): <小节名>`

---

## 8. 常见坑清单 (Recurring Traps)

| 坑 | 说明 | 正解 |
|----|-----|------|
| **MoE 里的 expert** | "expert" 在 MoE 上下文是术语 | 译"专家" (专家网络 / 专家路由) |
| **kernel 三义** | CNN / OS / kernel method | CNN=卷积核，OS=内核，method=核 (首次加英文) |
| **feature 两义** | ML 特征 vs 数学 eigen-* | 严格区分，eigen-* 加原文 |
| **normal 三义** | 正态分布 / 法向量 / 一般的 | 分布 → 正态；几何 → 法；日常 → 普通/一般 |
| **regular** | regularisation vs regular expression | 前者 = 正则化，后者 = 正则表达式 |
| **model** | 数学模型 / ML 模型 / 建模 | 统一"模型"；动词 "modeling" 译"建模" |
| **training** | 训练 (ML)，不译"培训" | |
| **inference** | 推理 (ML)，不译"推断"；但概率统计的 statistical inference = 统计推断 | 区分领域 |
| **prior/posterior** | 先验/后验 (概率) | 别译"前置/后置" |
| **greedy** | 贪心 (算法)，不译"贪婪的" | |
| **naive** | 朴素 (如 Naive Bayes = 朴素贝叶斯) | 别译"天真的" |
| **online/offline** | 上下文相关 | ML=在线/离线学习；网页=线上/线下 |
| **channel** | CNN=通道；通信=信道 | |
| **stream** | 数据流 / 流式 | 别混用 |
| **head** (attention) | 注意力头 | 不译"头部" |
| **layer** | 层 | Transformer 一层 = 一个 block |
| **block** | 块 / 模块 | 视上下文 |
| **just / simply** | 不过是 / 无非 / 就是 | 保留轻语气 |
| **note / notice** | 注意 / 请注意 | 不用"值得注意的是" (太正式) |
| **for instance / e.g.** | 例如 / 比如 | 别用"举个例子来说" |
| **so-called** | 所谓 (中性) | 别用"所谓的" (含贬义) |
| **arbitrary** | 任意 (数学) | 别译"随意" |
| **almost surely** | 几乎必然 (概率) | 术语，别口语化 |
| **一/1** | 数字上下文用阿拉伯数字，成语/俗语用中文 | "1 维空间" vs "一举两得" |
| **单位** | cm/kg/GB/GHz 前后加空格 | "185 cm" 而非 "185cm" |
| **括号内的英文原文** | 首次：中文 (English)，括号内**不加**空格 | ✅ "梯度下降 (gradient descent)"; ❌ "梯度下降 ( gradient descent )" |
| **~ 与 ~ 的破折号** | 数值范围 (1~10) 用 `~` 或 `–`；语义停顿用 `——` | 别混 |

### 版式微坑
- Alt 文本内不要放公式 (屏幕阅读器不友好)，用自然语言描述
- 中文冒号后紧跟英文/公式时**不加空格**: ✅ `例如：$x = 1$`
- 表格内单元格不加末尾句号，保持简洁
- Admonition 内部块级公式仍用 `$$` (不能缩进破坏渲染)

---

## 9. 主编终审要点 (Reviewer Cheatsheet)

主编 review 时按以下清单快速扫描:

1. 公式/代码/图片路径**未动**
2. 增强块之外的标题/列表/空行结构对齐；增强块不计入标题与列表结构比较
3. 中英文空格规范，全角标点
4. 术语与 GLOSSARY 一致，首次出现带英文
5. 语气亲切 (读起来像作者本人在讲，不像论文摘要)
6. 长句已拆，无翻译腔
7. 脚注闭合，引言原文可追溯
8. 目录结构与命名合规
9. 按原文顺序逐单元核对覆盖，确认每个原文信息单元均有可追溯的一一对应；不得以行数、标题数或列表数相等作为替代
10. 新增内容均有可见标记：`一句话总结`、`本章导览`、`本节要点`，或 `> **补充说明**:`、`[译注:]`
11. 附 Translation QA verifier 的完整 P0/P1/P2 结果与 JSON 证据；重点确认 `P0-SOURCE-COVERAGE`、`P1-UNLABELLED-EXPANSION`

---

## 11. 缩写处理 (v1.1 强化)

### 11.1 缩写首现三段式

任何缩写 (MLP / CNN / RNN / BPE / NER / POS / SVD / PCA / GAN / VAE / RLHF / MoE / SSM / DP / BFS / DFS / SIMD / CUDA / TPU / GPU / LLM / VLM / TF-IDF / NFC / NFD / OCR / ASR / TTS / SLAM / RTX ...) 首次出现时**必须**给出:

**格式**: `中文常见译法 (English Full Name, ABBR)`

- ✅ "字节对编码 (Byte-Pair Encoding, BPE)"
- ✅ "循环神经网络 (Recurrent Neural Network, RNN)"
- ✅ "命名实体识别 (Named Entity Recognition, NER)"
- ✅ "混合专家 (Mixture of Experts, MoE)"
- ✅ "自动语音识别 (Automatic Speech Recognition, ASR)"
- ❌ "BPE" (直接用，无全称)
- ❌ "字节对编码 (BPE)" (缺 Full Name)

**之后**：仅用缩写 ABBR (如 "BPE 算法…")，不重复全称。

### 11.2 无中文常见译法的处理

- 若技术圈**约定俗成不译** (SIMD / CUDA / GPU / TPU)：首现仍要给全称
  - ✅ "单指令多数据 (Single Instruction Multiple Data, SIMD)"
  - ✅ "统一计算设备架构 (Compute Unified Device Architecture, CUDA)"
  - 之后正文用 SIMD / CUDA
- 若中文有多种译法，取 GLOSSARY.md 首选:
  - GPU：图形处理器 (Graphics Processing Unit, GPU)
  - TPU：张量处理单元 (Tensor Processing Unit, TPU)

### 11.3 章内首现 vs 全书首现

- **每一节** (即每一个 .md 文件) 各自独立处理：该节首次出现的缩写都要展开
- 理由：读者可能从任一节切入，不能假设已读上文
- GLOSSARY.md 记录**全书统一译法**，但正文按节展开

### 11.4 缩写全称核对清单 (常见错案例)

| 常见错 | 正确全称 |
|-------|---------|
| CNN = "Convolutional Neural Networks" | ✅ **Convolutional Neural Network** (单数) |
| RNN | Recurrent Neural Network |
| LSTM | Long Short-Term Memory |
| GRU | Gated Recurrent Unit |
| GAN | Generative Adversarial Network |
| VAE | Variational Autoencoder |
| BERT | Bidirectional Encoder Representations from Transformers |
| GPT | Generative Pre-trained Transformer |
| T5 | Text-to-Text Transfer Transformer |
| BPE | Byte-Pair Encoding |
| POS | Part-of-Speech |
| NER | Named Entity Recognition |
| TF-IDF | Term Frequency-Inverse Document Frequency |
| SVD | Singular Value Decomposition |
| PCA | Principal Component Analysis |
| ICA | Independent Component Analysis |
| MoE | Mixture of Experts |
| SSM | State Space Model |
| RLHF | Reinforcement Learning from Human Feedback |
| DPO | Direct Preference Optimization |
| KL | Kullback-Leibler (divergence) |
| MLE | Maximum Likelihood Estimation |
| MAP | Maximum A Posteriori |
| MSE | Mean Squared Error |
| CE | Cross-Entropy |
| SGD | Stochastic Gradient Descent |
| BFS / DFS | Breadth-First Search / Depth-First Search |
| DP | Dynamic Programming |
| SIMD | Single Instruction Multiple Data |
| CUDA | Compute Unified Device Architecture |
| GPU / TPU / CPU | Graphics / Tensor / Central Processing Unit |
| ARM | Advanced RISC Machine |
| AVX | Advanced Vector Extensions |
| ASR | Automatic Speech Recognition |
| TTS | Text-to-Speech |
| OCR | Optical Character Recognition |
| SLAM | Simultaneous Localization and Mapping |
| GNN | Graph Neural Network |
| GAT | Graph Attention Network |
| VLM | Vision-Language Model |
| VLA | Vision-Language-Action model |
| CLIP | Contrastive Language-Image Pre-training |
| LoRA | Low-Rank Adaptation |
| MLP | Multi-Layer Perceptron |
| ReLU | Rectified Linear Unit |
| GELU | Gaussian Error Linear Unit |
| BN / LN | Batch Normalization / Layer Normalization |
| API | Application Programming Interface |
| OS | Operating System |
| IPC | Inter-Process Communication |
| RTOS | Real-Time Operating System |
| NFC / NFD | Normalization Form Canonical Composition / Decomposition |

⚠️ 若不确定全称，**查 Wikipedia 或 GLOSSARY.md**，不要凭记忆。

---

## 12. 括号对齐规范 (v1.1 强化)

### 12.1 括号类型对照

| 场景 | 用哪种括号 | 前后空格 | 内部空格 |
|------|----------|---------|---------|
| **术语首现** `中文 (English)` | 半角 `()` | 中文与 `(` 之间 **1 空格** | 内部**紧贴**，无空格 |
| **缩写全称** `中文 (Full Name, ABBR)` | 半角 `()` | 中文与 `(` 之间 **1 空格** | 内部无空格 |
| **公式内部** | 保持 LaTeX 原样 | — | — |
| **代码/URL** | 保留原样 | — | — |
| **中文补充说明**(纯中文) | 全角 `（）` | 无空格 | — |
| **单位/数字附注** | 半角 `()` | 数字前有空格 | 内部无空格 |

### 12.2 例

- ✅ 反向传播 (backpropagation) 是训练神经网络的核心算法
- ✅ 循环神经网络 (Recurrent Neural Network, RNN) 处理序列数据
- ✅ 我们训练了 100 个 epoch (相当于遍历数据集 100 遍)
- ✅ 张三（作者本人）在书中提到 ← 纯中文补充说明用全角
- ❌ 反向传播( backpropagation )是... ← 括号内有多余空格
- ❌ 反向传播 (backpropagation)是... ← 右括号后缺空格
- ❌ 反向传播(backpropagation) 是... ← 左括号前缺空格

### 12.3 嵌套括号

- 术语 + 附加缩写：`中文 (English Full Name, ABBR)` — 用逗号分隔，**不要**嵌套
- ❌ "字节对编码 (Byte-Pair Encoding (BPE))"
- ✅ "字节对编码 (Byte-Pair Encoding, BPE)"

### 12.4 自动检查

grep 排查常见错误:
```bash
# 找中文与半角左括号紧贴(缺空格)
grep -nP '[\p{Han}]\(' zh/**/*.md

# 找半角右括号后紧跟中文(缺空格)
grep -nP '\)[\p{Han}]' zh/**/*.md

# 找括号内首尾空格
grep -nP '\( | \)' zh/**/*.md
```

---

## 13. 章节结构规范 (v1.1 新增) — 一句话总结 + 重点归纳

本节规定的 `一句话总结`、`本章导览`、`本节要点` 均是 F12 认可的学习增强块：它们可不计入 F4/F6 的标题与列表结构比较，但不得替代、重排或省略增强块之外的原文信息单元；增强块之外仍须按原文顺序一一对应。

**每一节 .md 文件的输出结构 (硬性):**

```markdown
# <节标题>

> **一句话总结**: <1 句, 30-50 字, 高度浓缩本节讲什么>

*<原作 italic 引言的中文翻译, 若原作有 italic 概述则保留>*

<正文...>

---

## 📌 本节要点

- **<关键概念 1>**: <10-20 字解释>
- **<关键概念 2>**: <10-20 字解释>
- ...
- (5-8 条为宜, 覆盖本节所有需要读者记住的东西)

<可选: 与下一节的衔接>
```

### 13.1 "一句话总结" 规则

- 位置：标题正下方 blockquote 形式 `> **一句话总结**: xxx`
- 长度：30-50 中文字
- 内容：回答"这一节到底讲什么，为什么重要"
- 例:
  - > **一句话总结**：向量空间是一切 AI/ML 表示的数学舞台，它保证向量间的加法与缩放不会"逃出空间"，由此支撑起线性代数的整套理论。
  - > **一句话总结**：分词是把连续文本切成模型能处理的离散 token 的关键预处理步骤；BPE / WordPiece / Unigram 是三种主流子词切分算法。

### 13.2 "本节要点" 规则

- 位置：文件末尾，用 `---` 与正文分隔，用 `## 📌 本节要点` 作二级标题
- 条目：5-8 条，每条一行 `- **术语**: 解释`
- 目的：读者读完后**只看要点**就能回忆全节
- 若原节内容极短 (< 100 行 markdown): 3-5 条即可
- 若极长 (> 500 行)：可扩到 10 条
- 术语部分用中文加粗，解释用**陈述句**，不用问号

### 13.3 章首页 (每章第一个 .md 文件) 额外要求

- 除本节的"一句话总结"与"本节要点"之外，额外在**顶部**加一段 `## 🗺️ 本章导览`, 5-8 行 bullet，概述整章 5 节的关系与阅读顺序建议
- 例 (Chapter 01 - Vectors 首节):

```markdown
# 向量空间

> **一句话总结**: ...

## 🗺️ 本章导览

- 本章覆盖向量的一切: 空间 → 性质 → 度量 → 运算 → 高级结构
- **01. 向量空间** (本节): 定义向量与它们生活的空间, 引入公理
- **02. 向量的性质**: 长度、方向、单位化、正交
- **03. 范数与度量**: 各种距离与相似度
- **04. 向量积**: 点积、叉积、外积
- **05. 基与对偶**: 换基、对偶空间, 通往矩阵一章的桥梁

*<原作 italic 引言中译>*

<正文>
```

### 13.4 空章节处理

若原文文件为空 (如 Ch20 若干节)，中文版**同样保留空文件**，内容为:
```markdown
# <节标题>

> **一句话总结**: 本节内容尚待作者补充 (原文亦为空).

*占位符 — 待原作者更新原文后同步翻译.*
```

---

## 14. 联系与升级

- 手册版本：v1.1 (2026-07 update：缩写全称、括号对齐、章节归纳)
- 遇到手册未覆盖的新问题 → 在 `zh/TRANSLATION_QA.md` 追加 (若无则创建)，主编周期性合并到本手册
- **不要**擅自修改本手册主体，手册变更由主编统一 gate

---

> **一句话**：保住公式与代码，保住作者的语气，剩下的就是"让一个懂技术的中文朋友，用中文把这段讲明白"。