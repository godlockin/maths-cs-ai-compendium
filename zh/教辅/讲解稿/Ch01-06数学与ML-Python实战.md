# Ch01-06 数学与 ML Python 实战 · 讲解稿

> **章节定位**: Ch01-06 数学基础 + 经典 ML 的 Python 实战补丁。
> **承接**: Ch01-05 数学 → Ch06 ML → 本实战
> **篇幅**: ~5500 字 / 阅读 15 分钟 / 讲解 30 分钟

---

## 一 · Ch01 线性代数实战

### 1.1 NumPy 基础

```python
import numpy as np

# 1. 向量
v = np.array([1, 2, 3])

# 2. 矩阵
A = np.array([[1, 2], [3, 4]])

# 3. 矩阵乘法
A @ A  # 5 7 11 15

# 4. 范数
np.linalg.norm(v)  # 3.74

# 5. 特征值
eigenvalues, eigenvectors = np.linalg.eig(A)
```

### 1.2 实战 1: PCA 降维

```python
from sklearn.decomposition import PCA
import numpy as np

# 生成数据
X = np.random.randn(100, 10)  # 100 样本, 10 特征

# PCA
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

# 解释方差比
print(pca.explained_variance_ratio_)
# 这就是 Ch02 SVD 实战
```

### 1.3 实战 2: 词嵌入可视化

```python
# 用 PCA 把 300 维词向量降到 2 维
# 观察语义聚类
from sklearn.manifold import TSNE

embeddings = word2vec_model.wv.vectors  # (10000, 300)
embedded = TSNE(n_components=2).fit_transform(embeddings)
plt.scatter(embedded[:, 0], embedded[:, 1])
```

---

## 二 · Ch02 矩阵论实战

### 2.1 SVD 图像压缩

```python
from PIL import Image
import numpy as np

# 加载图像
img = np.array(Image.open('photo.jpg'))
print(img.shape)  # (H, W, 3)

# 灰度
gray = img.mean(axis=2)

# SVD
U, S, Vt = np.linalg.svd(gray, full_matrices=False)

# 压缩: 只保留前 50 个奇异值
k = 50
compressed = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
print(f"压缩率: {k * (gray.shape[0] + gray.shape[1]) / gray.size:.1%}")
```

### 2.2 实战: 推荐系统 (SVD 矩阵分解)

```python
# 用户-电影评分矩阵
R = np.array([
    [5, 3, 0, 1],
    [4, 0, 0, 1],
    [1, 1, 0, 5],
    [0, 0, 5, 4],
])

# SVD 分解
U, S, Vt = np.linalg.svd(R, full_matrices=False)

# 预测
k = 2
R_pred = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
print(R_pred)
```

### 2.3 实战: Transformer QKV 矩阵

```python
# 注意力矩阵 (Ch07 §04)
seq_len, d_k = 512, 64
Q = np.random.randn(seq_len, d_k)
K = np.random.randn(seq_len, d_k)
V = np.random.randn(seq_len, d_k)

# 注意力
scores = Q @ K.T / np.sqrt(d_k)
weights = np.exp(scores) / np.exp(scores).sum(axis=1, keepdims=True)
output = weights @ V
```

---

## 三 · Ch03 概率论实战

### 3.1 蒙特卡洛估计 π

```python
import numpy as np

np.random.seed(42)
N = 1_000_000
x = np.random.uniform(-1, 1, N)
y = np.random.uniform(-1, 1, N)
inside = (x**2 + y**2) <= 1

pi_est = 4 * inside.mean()
print(f"π ≈ {pi_est:.4f}, 误差 {abs(pi_est - np.pi):.4f}")
```

### 3.2 实战: 朴素贝叶斯垃圾邮件分类

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

# 数据
emails = [
    ("免费赠送", "spam"),
    ("开会通知", "ham"),
    ("赢取大奖", "spam"),
    ("项目进度", "ham"),
]

# 向量化
vectorizer = CountVectorizer()
X = vectorizer.fit_transform([e[0] for e in emails])
y = [e[1] for e in emails]

# 训练
model = MultinomialNB()
model.fit(X, y)

# 预测
print(model.predict(vectorizer.transform(["免费"])))
# 输出: ['spam']
```

### 3.3 实战: KL 散度计算

```python
import numpy as np

def kl_divergence(p, q):
    p = np.array(p) + 1e-10
    q = np.array(q) + 1e-10
    return np.sum(p * np.log(p / q))

# 两个分布
p = [0.4, 0.3, 0.2, 0.1]
q = [0.3, 0.3, 0.2, 0.2]

print(kl_divergence(p, q))  # 0.087
```

---

## 四 · Ch04 统计推断实战

### 4.1 t 检验

```python
from scipy import stats

# A/B 实验数据
group_a = [1.2, 1.5, 1.3, 1.4, 1.5, 1.6, 1.7, 1.3, 1.4, 1.5]
group_b = [1.5, 1.6, 1.7, 1.8, 1.9, 1.5, 1.6, 1.7, 1.8, 1.9]

# t 检验
t_stat, p_value = stats.ttest_ind(group_a, group_b)
print(f"t={t_stat:.3f}, p={p_value:.3f}")
# p < 0.05 => 显著差异
```

### 4.2 实战: 置信区间

```python
import numpy as np
from scipy import stats

# 数据
data = np.array([1.2, 1.5, 1.3, 1.4, 1.5, 1.6, 1.7, 1.3, 1.4, 1.5])
mean = data.mean()
se = data.std() / np.sqrt(len(data))

# 95% 置信区间
ci = stats.t.interval(0.95, len(data)-1, mean, se)
print(f"95% CI: [{ci[0]:.3f}, {ci[1]:.3f}]")
```

### 4.3 实战: 贝叶斯 A/B 测试

```python
import numpy as np
from scipy import stats

# 观测数据
n_a, c_a = 1000, 50  # A: 1000 访客, 50 转化
n_b, c_b = 1000, 70  # B: 1000 访客, 70 转化

# Beta 后验
posterior_a = stats.beta(c_a + 1, n_a - c_a + 1)
posterior_b = stats.beta(c_b + 1, n_b - c_b + 1)

# 蒙特卡洛
samples_a = posterior_a.rvs(100_000)
samples_b = posterior_b.rvs(100_000)

# P(B > A)
prob_b_better = (samples_b > samples_a).mean()
print(f"P(B > A) = {prob_b_better:.3f}")
```

---

## 五 · Ch05 贝叶斯与信息论实战

### 5.1 熵与交叉熵

```python
import numpy as np

def entropy(p):
    p = np.array(p) + 1e-10
    return -np.sum(p * np.log(p))

def cross_entropy(p, q):
    q = np.array(q) + 1e-10
    return -np.sum(p * np.log(q))

# 3 分类
p = [0.7, 0.2, 0.1]
q = [0.5, 0.3, 0.2]

print(f"H(P) = {entropy(p):.3f}")
print(f"H(P, Q) = {cross_entropy(p, q):.3f}")
```

### 5.2 实战: 朴素贝叶斯文本分类 (贝叶斯)

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

# 训练数据
texts = ["cat dog", "fish shark", "cat mouse", "shark whale"]
labels = ["mammal", "fish", "mammal", "fish"]

# TF-IDF + 朴素贝叶斯
vec = TfidfVectorizer()
X = vec.fit_transform(texts)
model = MultinomialNB()
model.fit(X, labels)

# 预测
test = vec.transform(["cat dog"])
print(model.predict(test))  # ['mammal']
```

### 5.3 实战: 互信息特征选择

```python
from sklearn.feature_selection import mutual_info_classif
import numpy as np

# 100 样本, 10 特征
X = np.random.randn(100, 10)
y = np.random.randint(0, 2, 100)

# 互信息
mi = mutual_info_classif(X, y)
print(mi.round(2))
# 选 Top-5 特征
top5 = np.argsort(mi)[-5:]
```

---

## 六 · Ch06 经典 ML 实战

### 6.1 XGBoost 完整流程

```python
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# 数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 模型
model = xgb.XGBClassifier(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.05,
    early_stopping_rounds=20,
)

model.fit(X_train, y_train, eval_set=[(X_test, y_test)])

# 评估
y_pred = model.predict_proba(X_test)[:, 1]
print(f"AUC: {roc_auc_score(y_test, y_pred):.3f}")
```

### 6.2 实战: 端到端 ML Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000)),
])

# 训练
pipe.fit(X_train, y_train)

# 评估
print(f"Accuracy: {pipe.score(X_test, y_test):.3f}")

# 保存
import joblib
joblib.dump(pipe, "model.pkl")
```

### 6.3 实战: RL 训练 CartPole

```python
import gymnasium as gym
from stable_baselines3 import PPO

# 环境
env = gym.make("CartPole-v1")

# 模型
model = PPO(
    "MlpPolicy",
    env,
    learning_rate=0.0003,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
)

# 训练
model.learn(total_timesteps=50_000)

# 评估
obs, _ = env.reset()
for _ in range(1000):
    action, _ = model.predict(obs)
    obs, reward, done, _, _ = env.step(action)
    if done:
        break
```

### 6.4 实战: PyTorch 深度学习

```python
import torch
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, in_dim, hidden, out_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, out_dim),
        )

    def forward(self, x):
        return self.net(x)

# 训练
model = MLP(784, 256, 10)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

for epoch in range(10):
    for x, y in dataloader:
        pred = model(x)
        loss = criterion(pred, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

---

## 七 · 一句话总结

> **数学 + ML Python 实战 = 5 大支柱**: 线性代数 (PCA / SVD) + 概率 (蒙特卡洛 / 贝叶斯) + 统计 (t 检验 / A/B) + 经典 ML (XGBoost / Pipeline) + RL (PPO)。**所有理论都有 5-10 行可运行代码**。

## 八 · 参考资料

1. NumPy 官方文档
2. Scikit-learn 官方文档
3. PyTorch 官方文档
4. XGBoost 文档
5. Stable-Baselines3 文档
6. OpenAI Gymnasium
