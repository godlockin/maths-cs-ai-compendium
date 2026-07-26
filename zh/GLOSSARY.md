# 中英术语对照表 · Glossary

> 本表为《maths-cs-ai-compendium》中译工程的**术语规范**。凡书中出现的名词、缩写、隐喻,一律以本表为准; 遇歧义, 采用**"备注"**列指定的首选译法。
>
> - 缩写(MLP/CNN/GPU 等)通常**不译**,直接沿用英文。
> - 大写专有名词(Transformer, ResNet, PyTorch)保留英文。
> - 数学符号、公式一律不译。
> - 有争议的译法在备注中列出,采用首选。

---

## 1. 数学基础 (Foundations of Math)

| 英文 | 中文 | 备注 |
|---|---|---|
| axiom | 公理 | |
| theorem | 定理 | |
| lemma | 引理 | |
| corollary | 推论 | |
| proof | 证明 | |
| field | 域 | 抽象代数意义, 非 "field of study" |
| set | 集合 | |
| subset | 子集 | |
| function | 函数 | |
| mapping | 映射 | 亦作 "变换" |
| domain | 定义域 | |
| range / codomain | 值域 / 陪域 | |
| identity element | 单位元 | |
| inverse element | 逆元 | |
| commutativity | 交换律 | |
| associativity | 结合律 | |
| distributivity | 分配律 | |
| closure | 封闭性 | |
| real numbers ($\mathbb{R}$) | 实数 | |
| integers ($\mathbb{Z}$) | 整数 | |
| rational numbers | 有理数 | |
| complex numbers | 复数 | |
| Euclidean space | 欧几里得空间 | 亦作 "欧氏空间" |

---

## 2. 线性代数 (Linear Algebra)

| 英文 | 中文 | 备注 |
|---|---|---|
| vector | 向量 | |
| vector space | 向量空间 | |
| subspace | 子空间 | |
| scalar | 标量 | |
| scalar multiplication | 标量乘法 | |
| linear combination | 线性组合 | |
| linear independence | 线性无关 | |
| span | 张成 | 亦作 "生成"; 采用 "张成" |
| basis | 基 | |
| dimension | 维度 | |
| coordinate | 坐标 | |
| matrix | 矩阵 | |
| matrix multiplication | 矩阵乘法 | |
| transpose | 转置 | |
| inverse (matrix) | 逆矩阵 | |
| identity matrix | 单位矩阵 | |
| determinant | 行列式 | |
| trace | 迹 | |
| rank | 秩 | |
| null space / kernel | 零空间 / 核 | |
| column space | 列空间 | |
| row space | 行空间 | |
| eigenvalue | 特征值 | |
| eigenvector | 特征向量 | |
| eigendecomposition | 特征分解 | |
| SVD (Singular Value Decomposition) | 奇异值分解 | 缩写不译 |
| PCA (Principal Component Analysis) | 主成分分析 | 缩写不译 |
| orthogonal | 正交 | |
| orthonormal | 单位正交 | |
| dot product / inner product | 点积 / 内积 | |
| cross product | 叉积 | |
| outer product | 外积 | |
| norm | 范数 | |
| L1 norm | L1 范数 | 亦作 "曼哈顿距离" |
| L2 norm | L2 范数 | 亦作 "欧几里得范数" |
| cosine similarity | 余弦相似度 | |
| projection | 投影 | |
| linear transformation | 线性变换 | |
| feature vector | 特征向量 | ML 语境; 与线代 eigenvector 区分 |
| tensor | 张量 | |
| broadcasting | 广播 | NumPy/PyTorch 语义 |

---

## 3. 微积分与优化 (Calculus & Optimization)

| 英文 | 中文 | 备注 |
|---|---|---|
| derivative | 导数 | |
| partial derivative | 偏导数 | |
| gradient | 梯度 | |
| Jacobian | 雅可比矩阵 | |
| Hessian | 海森矩阵 | 亦作 "黑塞矩阵" |
| chain rule | 链式法则 | |
| Taylor series | 泰勒级数 | |
| integral | 积分 | |
| limit | 极限 | |
| continuity | 连续性 | |
| differentiability | 可微性 | |
| convexity | 凸性 | |
| convex function | 凸函数 | |
| gradient descent | 梯度下降 | |
| stochastic gradient descent (SGD) | 随机梯度下降 | 缩写常保留 |
| learning rate | 学习率 | |
| optimizer | 优化器 | |
| momentum | 动量 | |
| Adam | Adam | 优化器名, 保留 |
| RMSProp | RMSProp | 保留 |
| weight decay | 权重衰减 | |
| loss function | 损失函数 | |
| cost function | 代价函数 | |
| objective function | 目标函数 | |
| minimum / maximum | 极小值 / 极大值 | |
| local minimum | 局部极小 | |
| global minimum | 全局极小 | |
| saddle point | 鞍点 | |
| convergence | 收敛 | |

---

## 4. 概率与统计 (Probability & Statistics)

| 英文 | 中文 | 备注 |
|---|---|---|
| probability | 概率 | |
| random variable | 随机变量 | |
| distribution | 分布 | |
| probability density function (PDF) | 概率密度函数 | |
| cumulative distribution function (CDF) | 累积分布函数 | |
| expectation / mean | 期望 / 均值 | |
| variance | 方差 | |
| standard deviation | 标准差 | |
| covariance | 协方差 | |
| correlation | 相关系数 | |
| Gaussian / normal distribution | 高斯分布 / 正态分布 | |
| Bernoulli distribution | 伯努利分布 | |
| binomial distribution | 二项分布 | |
| Poisson distribution | 泊松分布 | |
| uniform distribution | 均匀分布 | |
| conditional probability | 条件概率 | |
| Bayes' theorem | 贝叶斯定理 | |
| prior | 先验 | |
| posterior | 后验 | |
| likelihood | 似然 | |
| maximum likelihood estimation (MLE) | 极大似然估计 | 缩写常保留 |
| maximum a posteriori (MAP) | 最大后验估计 | 缩写常保留 |
| entropy | 熵 | |
| cross-entropy | 交叉熵 | |
| KL divergence | KL 散度 | 保留缩写 |
| mutual information | 互信息 | |
| hypothesis test | 假设检验 | |
| p-value | p 值 | |
| confidence interval | 置信区间 | |
| central limit theorem | 中心极限定理 | |
| law of large numbers | 大数定律 | |
| Markov chain | 马尔可夫链 | |
| Monte Carlo | 蒙特卡罗 | |

---

## 5. 经典机器学习 (Classical ML)

| 英文 | 中文 | 备注 |
|---|---|---|
| machine learning | 机器学习 | |
| supervised learning | 监督学习 | |
| unsupervised learning | 无监督学习 | |
| semi-supervised learning | 半监督学习 | |
| self-supervised learning | 自监督学习 | |
| reinforcement learning | 强化学习 | |
| training | 训练 | |
| inference | 推理 | 亦作 "推断"; 采用 "推理" |
| validation | 验证 | |
| test set | 测试集 | |
| overfitting | 过拟合 | |
| underfitting | 欠拟合 | |
| regularization | 正则化 | |
| bias-variance tradeoff | 偏差-方差权衡 | |
| cross-validation | 交叉验证 | |
| feature engineering | 特征工程 | |
| feature | 特征 | |
| label | 标签 | |
| linear regression | 线性回归 | |
| logistic regression | 逻辑回归 | 亦作 "对数几率回归" |
| decision tree | 决策树 | |
| random forest | 随机森林 | |
| gradient boosting | 梯度提升 | |
| XGBoost | XGBoost | 保留 |
| k-nearest neighbors (KNN) | k 近邻 | |
| k-means | k 均值 | |
| clustering | 聚类 | |
| classification | 分类 | |
| regression | 回归 | |
| SVM (Support Vector Machine) | 支持向量机 | 缩写常保留 |
| kernel trick | 核技巧 | |
| ensemble | 集成 | |
| bagging | 装袋 | 常保留英文 |
| boosting | 提升 | 常保留英文 |
| precision | 精确率 | |
| recall | 召回率 | |
| F1 score | F1 分数 | |
| accuracy | 准确率 | |
| ROC curve | ROC 曲线 | |
| AUC | AUC | 缩写不译 |
| confusion matrix | 混淆矩阵 | |

---

## 6. 深度学习 (Deep Learning)

| 英文 | 中文 | 备注 |
|---|---|---|
| deep learning | 深度学习 | |
| neural network | 神经网络 | |
| neuron | 神经元 | |
| hidden layer | 隐藏层 | |
| MLP (Multi-Layer Perceptron) | 多层感知机 | 缩写常保留 |
| fully connected layer / dense layer | 全连接层 | |
| forward pass | 前向传播 | |
| backpropagation | 反向传播 | |
| backward pass | 反向传播 | 同上 |
| activation function | 激活函数 | |
| ReLU | ReLU | 保留;释义时说"修正线性单元" |
| sigmoid | Sigmoid | 保留 |
| tanh | tanh | 保留 |
| GELU | GELU | 保留;高斯误差线性单元 |
| Swish | Swish | 保留 |
| softmax | Softmax | 保留 |
| weight | 权重 | |
| bias | 偏置 | 与 statistical bias(偏差) 区分 |
| parameter | 参数 | |
| hyperparameter | 超参数 | |
| epoch | 轮次 | 常保留英文 |
| batch | 批 / 批次 | |
| mini-batch | 小批 | |
| batch size | 批大小 | |
| initialization | 初始化 | |
| Xavier initialization | Xavier 初始化 | 亦作 "Glorot 初始化" |
| He initialization | He 初始化 | 亦作 "Kaiming 初始化" |
| batch normalization | 批归一化 | 亦作 "批量标准化"; 首选 "批归一化" |
| layer normalization | 层归一化 | |
| instance normalization | 实例归一化 | |
| group normalization | 组归一化 | |
| dropout | Dropout | 保留;释义时说"随机丢弃" |
| vanishing gradient | 梯度消失 | |
| exploding gradient | 梯度爆炸 | |
| skip connection / residual connection | 跳跃连接 / 残差连接 | |
| universal approximation theorem | 万能逼近定理 | |
| representation learning | 表征学习 | |
| embedding | 嵌入 / 嵌入向量 | 首选 "嵌入" |
| latent space | 潜空间 | 亦作 "隐空间" |
| feature map | 特征图 | |
| receptive field | 感受野 | |
| convolution | 卷积 | |
| CNN (Convolutional Neural Network) | 卷积神经网络 | 缩写常保留 |
| kernel / filter | 卷积核 / 滤波器 | |
| stride | 步长 | |
| padding | 填充 | |
| dilation | 膨胀 / 空洞 | 首选 "膨胀"; 亦作 "空洞卷积" (dilated conv) |
| pooling | 池化 | |
| max pooling | 最大池化 | |
| average pooling | 平均池化 | |
| global average pooling (GAP) | 全局平均池化 | |
| depthwise separable convolution | 深度可分离卷积 | |
| RNN (Recurrent Neural Network) | 循环神经网络 | 缩写常保留 |
| LSTM | LSTM | 长短期记忆网络, 缩写常保留 |
| GRU | GRU | 门控循环单元, 缩写常保留 |
| forget gate | 遗忘门 | |
| input gate | 输入门 | |
| output gate | 输出门 | |
| cell state | 细胞状态 | 亦作 "元胞状态" |
| hidden state | 隐藏状态 | |
| autoencoder | 自编码器 | |
| VAE (Variational Autoencoder) | 变分自编码器 | 缩写常保留 |
| GAN (Generative Adversarial Network) | 生成对抗网络 | 缩写常保留 |
| generator | 生成器 | |
| discriminator | 判别器 | |
| diffusion model | 扩散模型 | |
| denoising | 去噪 | |
| reparameterization trick | 重参数化技巧 | |
| ResNet | ResNet | 保留 |
| DenseNet | DenseNet | 保留 |
| Inception | Inception | 保留;释义"Inception 模块" |
| VGG | VGG | 保留 |
| AlexNet / LeNet | AlexNet / LeNet | 保留 |
| MobileNet | MobileNet | 保留 |
| EfficientNet | EfficientNet | 保留 |
| compound scaling | 复合缩放 | |
| Grad-CAM | Grad-CAM | 保留 |
| neural style transfer | 神经风格迁移 | |

---

## 7. 注意力机制与 Transformer (Attention & Transformers)

| 英文 | 中文 | 备注 |
|---|---|---|
| attention | 注意力 | |
| self-attention | 自注意力 | |
| cross-attention | 交叉注意力 | |
| multi-head attention | 多头注意力 | |
| scaled dot-product attention | 缩放点积注意力 | |
| query / key / value (Q, K, V) | 查询 / 键 / 值 | |
| Transformer | Transformer | 保留 |
| encoder | 编码器 | |
| decoder | 解码器 | |
| encoder-only | 仅编码器 | |
| decoder-only | 仅解码器 | |
| encoder-decoder | 编码器-解码器 | |
| positional encoding | 位置编码 | |
| sinusoidal encoding | 正弦位置编码 | |
| RoPE (Rotary Position Embedding) | 旋转位置编码 | 缩写常保留 |
| ALiBi | ALiBi | 保留;释义"带线性偏置的注意力" |
| causal mask | 因果掩码 | |
| masked language modelling (MLM) | 掩码语言建模 | 缩写常保留 |
| causal language modelling (CLM) | 因果语言建模 | 缩写常保留 |
| next sentence prediction (NSP) | 下一句预测 | |
| pre-training | 预训练 | |
| fine-tuning | 微调 | |
| prompt | 提示 / 提示词 | 首选 "提示词" |
| prompt engineering | 提示工程 | |
| zero-shot | 零样本 | |
| few-shot | 少样本 | |
| in-context learning (ICL) | 上下文学习 | |
| chain-of-thought (CoT) | 思维链 | |
| BERT | BERT | 保留 |
| GPT | GPT | 保留 |
| T5 | T5 | 保留 |
| BART | BART | 保留 |
| LLM (Large Language Model) | 大语言模型 | 缩写常保留 |
| tokenization | 分词 / 分词化 | |
| token | Token | 保留 (亦作 "词元") |
| subword | 子词 | |
| BPE (Byte Pair Encoding) | 字节对编码 | |
| WordPiece | WordPiece | 保留 |
| SentencePiece | SentencePiece | 保留 |
| scaling laws | 缩放律 | 亦作 "扩展律" |
| Chinchilla scaling | Chinchilla 缩放 | 保留 |
| MoE (Mixture of Experts) | 专家混合模型 | 缩写常保留 |
| expert | 专家 | |
| router / gating network | 路由 / 门控网络 | |
| load balancing loss | 负载均衡损失 | |
| PEFT (Parameter-Efficient Fine-Tuning) | 参数高效微调 | 缩写常保留 |
| LoRA (Low-Rank Adaptation) | 低秩适配 | 缩写常保留 |
| adapter | 适配器 | |
| prefix tuning | 前缀微调 | |
| prompt tuning | 提示微调 | |
| RLHF | RLHF | 基于人类反馈的强化学习, 缩写常保留 |
| SFT (Supervised Fine-Tuning) | 有监督微调 | 缩写常保留 |
| DPO | DPO | 直接偏好优化, 缩写常保留 |
| perplexity | 困惑度 | |
| BLEU / ROUGE / METEOR | BLEU / ROUGE / METEOR | 保留 |

---

## 8. 计算机视觉 (Computer Vision)

| 英文 | 中文 | 备注 |
|---|---|---|
| image classification | 图像分类 | |
| object detection | 目标检测 | |
| semantic segmentation | 语义分割 | |
| instance segmentation | 实例分割 | |
| panoptic segmentation | 全景分割 | |
| bounding box | 边界框 | |
| IoU (Intersection over Union) | 交并比 | |
| anchor box | 锚框 | |
| NMS (Non-Maximum Suppression) | 非极大值抑制 | 缩写常保留 |
| feature pyramid network (FPN) | 特征金字塔网络 | |
| ViT (Vision Transformer) | 视觉 Transformer | 缩写常保留 |
| MLP-Mixer | MLP-Mixer | 保留 |
| CLS token | CLS Token | 保留 |
| patch | 图块 / Patch | 首选 "图块" |
| data augmentation | 数据增强 | |
| Mixup / CutMix / RandAugment | Mixup / CutMix / RandAugment | 保留 |
| transfer learning | 迁移学习 | |
| feature extraction | 特征提取 | |
| ImageNet | ImageNet | 保留 |
| pixel | 像素 | |
| channel | 通道 | |
| edge detection | 边缘检测 | |
| Sobel / Canny | Sobel / Canny | 保留 |
| Gaussian blur | 高斯模糊 | |
| histogram | 直方图 | |
| optical flow | 光流 | |

---

## 9. 音频与语音 (Audio & Speech)

| 英文 | 中文 | 备注 |
|---|---|---|
| waveform | 波形 | |
| sample rate | 采样率 | |
| spectrogram | 频谱图 | |
| mel-spectrogram | 梅尔频谱图 | |
| MFCC | MFCC | 梅尔频率倒谱系数, 缩写常保留 |
| Fourier transform | 傅里叶变换 | |
| FFT (Fast Fourier Transform) | 快速傅里叶变换 | |
| STFT | 短时傅里叶变换 | 缩写常保留 |
| ASR (Automatic Speech Recognition) | 自动语音识别 | 缩写常保留 |
| TTS (Text-to-Speech) | 文本转语音 | 缩写常保留 |
| speaker diarization | 说话人分离 | |
| voice activity detection (VAD) | 语音活动检测 | |
| Whisper | Whisper | 保留 |
| wav2vec | wav2vec | 保留 |

---

## 10. 多模态学习 (Multimodal Learning)

| 英文 | 中文 | 备注 |
|---|---|---|
| multimodal | 多模态 | |
| modality | 模态 | |
| vision-language model (VLM) | 视觉-语言模型 | 缩写常保留 |
| CLIP | CLIP | 保留 |
| contrastive learning | 对比学习 | |
| InfoNCE loss | InfoNCE 损失 | 保留 |
| image-text pair | 图文对 | |
| joint embedding | 联合嵌入 | |
| cross-modal | 跨模态 | |
| captioning | 图像描述 / 字幕生成 | |
| VQA (Visual Question Answering) | 视觉问答 | |

---

## 11. 图神经网络与自主系统 (GNN & Robotics)

| 英文 | 中文 | 备注 |
|---|---|---|
| GNN (Graph Neural Network) | 图神经网络 | 缩写常保留 |
| node | 节点 | |
| edge | 边 | |
| graph | 图 | |
| adjacency matrix | 邻接矩阵 | |
| message passing | 消息传递 | |
| GCN (Graph Convolutional Network) | 图卷积网络 | |
| GAT (Graph Attention Network) | 图注意力网络 | |
| GraphSAGE | GraphSAGE | 保留 |
| pooling (graph) | 图池化 | |
| autonomous system | 自主系统 | |
| SLAM | SLAM | 同步定位与建图, 缩写常保留 |
| Kalman filter | 卡尔曼滤波 | |
| PID controller | PID 控制器 | 缩写不译 |
| policy | 策略 | |
| reward | 奖励 | |
| Q-learning | Q 学习 | |
| actor-critic | 演员-评论家 | |
| MDP (Markov Decision Process) | 马尔可夫决策过程 | 缩写常保留 |

---

## 12. 计算与操作系统 (Computing & OS)

| 英文 | 中文 | 备注 |
|---|---|---|
| operating system (OS) | 操作系统 | |
| process | 进程 | |
| thread | 线程 | |
| context switch | 上下文切换 | |
| scheduler | 调度器 | |
| system call | 系统调用 | |
| kernel (OS) | 内核 | 与 CNN 的 kernel(卷积核) 区分 |
| user space | 用户态 | |
| memory management | 内存管理 | |
| virtual memory | 虚拟内存 | |
| paging | 分页 | |
| cache | 缓存 | |
| L1 / L2 / L3 cache | L1 / L2 / L3 缓存 | |
| RAM | 内存 (RAM) | |
| register | 寄存器 | |
| instruction | 指令 | |
| pipeline | 流水线 | |
| interrupt | 中断 | |
| file system | 文件系统 | |
| mutex / lock | 互斥锁 / 锁 | |
| semaphore | 信号量 | |
| deadlock | 死锁 | |
| race condition | 竞态条件 | |

---

## 13. 数据结构与算法 (DSA)

| 英文 | 中文 | 备注 |
|---|---|---|
| algorithm | 算法 | |
| data structure | 数据结构 | |
| Big O notation | 大 O 记号 | |
| time complexity | 时间复杂度 | |
| space complexity | 空间复杂度 | |
| array | 数组 | |
| linked list | 链表 | |
| stack | 栈 | |
| queue | 队列 | |
| deque | 双端队列 | |
| hash table / hash map | 哈希表 / 哈希映射 | |
| tree | 树 | |
| binary tree | 二叉树 | |
| BST (Binary Search Tree) | 二叉搜索树 | |
| heap | 堆 | |
| priority queue | 优先队列 | |
| trie | 字典树 | 亦作 "前缀树" |
| graph (DSA) | 图 | |
| BFS | 广度优先搜索 | 缩写常保留 |
| DFS | 深度优先搜索 | 缩写常保留 |
| recursion | 递归 | |
| iteration | 迭代 | |
| divide and conquer | 分治 | |
| dynamic programming (DP) | 动态规划 | 缩写常保留 |
| memoization | 记忆化 | |
| greedy algorithm | 贪心算法 | |
| backtracking | 回溯 | |
| two pointers | 双指针 | |
| sliding window | 滑动窗口 | |
| binary search | 二分查找 | |
| sorting | 排序 | |
| merge sort | 归并排序 | |
| quick sort | 快速排序 | |
| heap sort | 堆排序 | |
| topological sort | 拓扑排序 | |
| Dijkstra | Dijkstra 算法 | 保留人名 |
| union-find | 并查集 | |
| optimal substructure | 最优子结构 | |
| overlapping subproblems | 重叠子问题 | |

---

## 14. SIMD 与 GPU 硬件 (SIMD & GPU Hardware)

| 英文 | 中文 | 备注 |
|---|---|---|
| Moore's Law | 摩尔定律 | |
| clock speed / clock frequency | 时钟频率 | |
| transistor | 晶体管 | |
| core | 核心 | |
| multi-core | 多核 | |
| superscalar | 超标量 | |
| out-of-order execution | 乱序执行 | |
| branch prediction | 分支预测 | |
| speculative execution | 推测执行 | |
| instruction-level parallelism (ILP) | 指令级并行 | |
| data-level parallelism | 数据级并行 | |
| SIMD | SIMD | 单指令多数据, 缩写不译 |
| SIMT | SIMT | 单指令多线程, 缩写不译 |
| vector register | 向量寄存器 | |
| SSE / AVX / AVX-512 | SSE / AVX / AVX-512 | x86 指令集, 保留 |
| NEON / SVE | NEON / SVE | ARM 指令集, 保留 |
| intrinsic | 内建函数 | 亦作 "内置函数" |
| GPU | GPU | 缩写不译 |
| CUDA | CUDA | 保留 |
| CPU | CPU | 缩写不译 |
| TPU | TPU | 缩写不译 |
| ASIC | ASIC | 缩写不译 |
| FPGA | FPGA | 缩写不译 |
| FLOPS | FLOPS | 每秒浮点运算数, 缩写不译 |
| bandwidth | 带宽 | |
| latency | 延迟 | |
| throughput | 吞吐量 | |
| roofline model | Roofline 模型 | 保留 |
| arithmetic intensity | 算术强度 | 亦作 "计算强度" |
| memory-bound | 内存受限 | |
| compute-bound | 计算受限 | |
| kernel (GPU) | 核函数 | GPU 语境; 与 OS kernel 区分 |
| kernel fusion | 算子融合 | 亦作 "核融合" |
| warp | Warp | 保留;CUDA 术语 |
| block / grid | 块 / 网格 | CUDA 术语 |
| shared memory | 共享内存 | |
| global memory | 全局内存 | |
| tensor core | Tensor Core | 保留 |
| FMA (Fused Multiply-Add) | 融合乘加 | |
| BLAS | BLAS | 保留 |
| GEMM | GEMM | 通用矩阵乘, 保留 |

---

## 15. AI 推理与部署 (Inference & Deployment)

| 英文 | 中文 | 备注 |
|---|---|---|
| inference | 推理 | |
| latency (inference) | 推理延迟 | |
| throughput (serving) | 服务吞吐 | |
| quantization | 量化 | |
| INT8 / FP16 / BF16 / FP32 | INT8 / FP16 / BF16 / FP32 | 保留 |
| pruning | 剪枝 | |
| distillation | 蒸馏 | |
| knowledge distillation | 知识蒸馏 | |
| KV cache | KV 缓存 | 保留 |
| speculative decoding | 推测解码 | |
| batching | 批处理 | |
| continuous batching | 连续批处理 | |
| paged attention | PagedAttention | 保留 (vLLM 术语) |
| flash attention | FlashAttention | 保留 |
| ONNX | ONNX | 保留 |
| TensorRT | TensorRT | 保留 |
| vLLM / TGI / SGLang | vLLM / TGI / SGLang | 保留 |
| serving | 服务化 | |
| edge deployment | 边缘部署 | |
| model registry | 模型仓库 | |

---

## 16. 系统设计与工程 (Systems Design & Engineering)

| 英文 | 中文 | 备注 |
|---|---|---|
| scalability | 可扩展性 | |
| horizontal scaling | 水平扩展 | |
| vertical scaling | 垂直扩展 | |
| load balancer | 负载均衡器 | |
| microservice | 微服务 | |
| API | API | 缩写不译 |
| REST | REST | 保留 |
| gRPC | gRPC | 保留 |
| database | 数据库 | |
| SQL / NoSQL | SQL / NoSQL | 保留 |
| indexing | 索引 | |
| sharding | 分片 | |
| replication | 复制 | |
| caching (systems) | 缓存 | |
| queue (message) | 消息队列 | |
| Kafka | Kafka | 保留 |
| Redis | Redis | 保留 |
| CI/CD | CI/CD | 缩写不译 |
| containerization | 容器化 | |
| Docker / Kubernetes | Docker / Kubernetes (K8s) | 保留 |
| observability | 可观测性 | |
| logging | 日志 | |
| metrics | 指标 | |
| tracing | 链路追踪 | |
| DAG | DAG | 有向无环图, 缩写常保留 |
| dataflow | 数据流 | |
| MLOps | MLOps | 保留 |
| feature store | 特征仓库 | |
| A/B test | A/B 测试 | |
| model drift | 模型漂移 | |
| data drift | 数据漂移 | |

---

## 17. 应用 AI 与前沿 (Applied & Frontier AI)

| 英文 | 中文 | 备注 |
|---|---|---|
| agent | 智能体 / Agent | 首选 "智能体"; 高频语境保留 "Agent" |
| tool use / function calling | 工具调用 / 函数调用 | |
| RAG (Retrieval-Augmented Generation) | 检索增强生成 | 缩写常保留 |
| retriever | 检索器 | |
| vector database | 向量数据库 | |
| ANN (Approximate Nearest Neighbor) | 近似最近邻 | 缩写常保留 |
| HNSW / FAISS | HNSW / FAISS | 保留 |
| hallucination | 幻觉 | |
| alignment | 对齐 | |
| red teaming | 红队测试 | |
| jailbreak | 越狱 | |
| SSM (State Space Model) | 状态空间模型 | 缩写常保留 |
| Mamba | Mamba | 保留 |
| world model | 世界模型 | |
| foundation model | 基础模型 | |
| emergence | 涌现 | |
| grokking | Grokking | 保留;释义"顿悟式泛化" |
| test-time compute | 测试时计算 | |
| reasoning model | 推理模型 | |
| Mixture of Depths | 深度混合 | 参照 MoE |

---

## 18. 文风与隐喻处理 (Style & Metaphor)

> 本书大量使用比喻、玩笑与文化梗以提升可读性。翻译时**保留其风格张力**,不必逐字直译, 而是给出等效的中文表达。

| 英文原句 / 说法 | 中文对照 | 备注 |
|---|---|---|
| mathematical playground | 数学乐园 | 见第 01 章开头 |
| the space where ML lives | ML 栖身之所 / ML 生活的空间 | 拟人化保留 |
| without leaving the space | 不逃出这个空间 | 强调封闭性 |
| the Darwins of the world | 像达尔文那样反应慢却坚韧的学习者 | 文化梗需铺垫说明 |
| the bedrock of the field | 领域的基石 | |
| conveyor belt (of cell state) | 传送带 (指 LSTM 细胞状态) | |
| gradient highway | 梯度高速公路 | 指残差连接 |
| dying ReLU | 死亡 ReLU | 保留隐喻 |
| curse of dimensionality | 维度诅咒 | 亦作 "维数灾难" |
| free lunch | 免费午餐 | 常与 "No Free Lunch Theorem" 一并出现 |
| a bug caught at compile time costs \$1 | 编译期抓到一个 bug 花你 \$1 | 谚语式保留 |
| out of the box | 开箱即用 | |
| under the hood | 底层机制 / 引擎盖下 | |
| ignite the deep learning revolution | 点燃深度学习革命 | AlexNet 语境 |
| hit a wall | 撞上了墙 | 时钟频率停滞语境 |
| the era ended | 那个时代结束了 | |
| garbage in, garbage out | 垃圾进, 垃圾出 (GIGO) | 缩写常保留 |
| toy example | 玩具示例 | |
| bells and whistles | 花里胡哨的功能 | 视语境亦可译 "附加功能" |
| syntactic sugar | 语法糖 | |
| ninja / hacker (colloquial) | 高手 / 极客 | 视语境 |
| a picture is worth a thousand words | 一图胜千言 | |

---

## 使用说明

1. **一致性优先**: 同一术语在全书内保持单一译法, 参见本表 "备注" 列的首选项。
2. **首次出现**: 首次出现时使用 "**中文译名 (English)**" 形式, 后续可只用中文或缩写。
3. **缩写规则**: 缩写 (MLP/CNN/GPU/RLHF 等) 一律保留英文, 不译。
4. **公式与代码**: 数学符号、变量名、代码标识符一律不译。
5. **专有名词**: 模型/架构/框架名 (Transformer/BERT/PyTorch/CUDA 等) 保留英文。
6. **争议裁决**: 遇到多译法, 以本表为准; 本表未覆盖的, 参照《人工智能名词》(全国科学技术名词审定委员会) 与常见中文教材惯例。

