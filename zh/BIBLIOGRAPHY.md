# 参考文献 (Bibliography)

> 本书正文中高频引用文献的统一 BibTeX 条目, 按学科领域分类.
> 引用格式: `[Author+Year]`, 例如 `[Vaswani+2017]` 对应 Transformer 原始论文.
> 若同一作者同年多篇, 追加小写字母区分, 如 `[He+2016a]`, `[He+2016b]`.

---

## 目录

- [1. 深度学习基础与训练](#1-深度学习基础与训练)
- [2. Transformer 与大语言模型](#2-transformer-与大语言模型)
- [3. 计算机视觉](#3-计算机视觉)
- [4. 生成模型 (VAE / GAN / Diffusion)](#4-生成模型-vae--gan--diffusion)
- [5. 强化学习与对齐](#5-强化学习与对齐)
- [6. AI for Science (蛋白质 / 材料 / 物理)](#6-ai-for-science-蛋白质--材料--物理)
- [7. 优化与数值方法](#7-优化与数值方法)
- [8. 数学基础 (代数 / 分析 / 几何)](#8-数学基础-代数--分析--几何)
- [9. 概率与统计](#9-概率与统计)
- [10. 信息论与编码](#10-信息论与编码)
- [11. 算法与理论计算机科学](#11-算法与理论计算机科学)
- [12. 教材与专著](#12-教材与专著)

---

## 1. 深度学习基础与训练

### [Rumelhart+1986] 反向传播算法

```bibtex
@article{rumelhart1986learning,
  title   = {Learning representations by back-propagating errors},
  author  = {Rumelhart, David E. and Hinton, Geoffrey E. and Williams, Ronald J.},
  journal = {Nature},
  volume  = {323},
  number  = {6088},
  pages   = {533--536},
  year    = {1986},
  doi     = {10.1038/323533a0}
}
```

### [LeCun+1998] LeNet 与卷积网络

```bibtex
@article{lecun1998gradient,
  title   = {Gradient-based learning applied to document recognition},
  author  = {LeCun, Yann and Bottou, L{\'e}on and Bengio, Yoshua and Haffner, Patrick},
  journal = {Proceedings of the IEEE},
  volume  = {86},
  number  = {11},
  pages   = {2278--2324},
  year    = {1998}
}
```

### [Hinton+2006] 深度信念网络

```bibtex
@article{hinton2006fast,
  title   = {A fast learning algorithm for deep belief nets},
  author  = {Hinton, Geoffrey E. and Osindero, Simon and Teh, Yee-Whye},
  journal = {Neural Computation},
  volume  = {18},
  number  = {7},
  pages   = {1527--1554},
  year    = {2006}
}
```

### [Kingma+2014] Adam 优化器

```bibtex
@inproceedings{kingma2015adam,
  title     = {Adam: A Method for Stochastic Optimization},
  author    = {Kingma, Diederik P. and Ba, Jimmy},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2015},
  eprint    = {1412.6980}
}
```

### [Loshchilov+2019] AdamW

```bibtex
@inproceedings{loshchilov2019decoupled,
  title     = {Decoupled Weight Decay Regularization},
  author    = {Loshchilov, Ilya and Hutter, Frank},
  booktitle = {ICLR},
  year      = {2019}
}
```

### [Ioffe+2015] Batch Normalization

```bibtex
@inproceedings{ioffe2015batch,
  title     = {Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift},
  author    = {Ioffe, Sergey and Szegedy, Christian},
  booktitle = {ICML},
  year      = {2015}
}
```

### [Ba+2016] Layer Normalization

```bibtex
@article{ba2016layer,
  title   = {Layer Normalization},
  author  = {Ba, Jimmy Lei and Kiros, Jamie Ryan and Hinton, Geoffrey E.},
  journal = {arXiv preprint arXiv:1607.06450},
  year    = {2016}
}
```

### [Srivastava+2014] Dropout

```bibtex
@article{srivastava2014dropout,
  title   = {Dropout: A Simple Way to Prevent Neural Networks from Overfitting},
  author  = {Srivastava, Nitish and Hinton, Geoffrey and Krizhevsky, Alex and Sutskever, Ilya and Salakhutdinov, Ruslan},
  journal = {Journal of Machine Learning Research},
  volume  = {15},
  pages   = {1929--1958},
  year    = {2014}
}
```

### [Glorot+2010] Xavier 初始化

```bibtex
@inproceedings{glorot2010understanding,
  title     = {Understanding the difficulty of training deep feedforward neural networks},
  author    = {Glorot, Xavier and Bengio, Yoshua},
  booktitle = {AISTATS},
  year      = {2010}
}
```

### [He+2015] He 初始化 / PReLU

```bibtex
@inproceedings{he2015delving,
  title     = {Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification},
  author    = {He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
  booktitle = {ICCV},
  year      = {2015}
}
```

---

## 2. Transformer 与大语言模型

### [Vaswani+2017] Transformer 原始论文

```bibtex
@inproceedings{vaswani2017attention,
  title     = {Attention Is All You Need},
  author    = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N. and Kaiser, Lukasz and Polosukhin, Illia},
  booktitle = {NeurIPS},
  year      = {2017}
}
```

### [Devlin+2019] BERT

```bibtex
@inproceedings{devlin2019bert,
  title     = {BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding},
  author    = {Devlin, Jacob and Chang, Ming-Wei and Lee, Kenton and Toutanova, Kristina},
  booktitle = {NAACL-HLT},
  year      = {2019}
}
```

### [Radford+2018] GPT-1

```bibtex
@techreport{radford2018improving,
  title       = {Improving Language Understanding by Generative Pre-training},
  author      = {Radford, Alec and Narasimhan, Karthik and Salimans, Tim and Sutskever, Ilya},
  institution = {OpenAI},
  year        = {2018}
}
```

### [Radford+2019] GPT-2

```bibtex
@techreport{radford2019language,
  title       = {Language Models are Unsupervised Multitask Learners},
  author      = {Radford, Alec and Wu, Jeffrey and Child, Rewon and Luan, David and Amodei, Dario and Sutskever, Ilya},
  institution = {OpenAI},
  year        = {2019}
}
```

### [Brown+2020] GPT-3

```bibtex
@inproceedings{brown2020language,
  title     = {Language Models are Few-Shot Learners},
  author    = {Brown, Tom B. and others},
  booktitle = {NeurIPS},
  year      = {2020}
}
```

### [OpenAI+2023] GPT-4

```bibtex
@article{openai2023gpt4,
  title   = {GPT-4 Technical Report},
  author  = {{OpenAI}},
  journal = {arXiv preprint arXiv:2303.08774},
  year    = {2023}
}
```

### [Kaplan+2020] 扩展定律 (Scaling Laws)

```bibtex
@article{kaplan2020scaling,
  title   = {Scaling Laws for Neural Language Models},
  author  = {Kaplan, Jared and McCandlish, Sam and Henighan, Tom and Brown, Tom B. and Chess, Benjamin and Child, Rewon and Gray, Scott and Radford, Alec and Wu, Jeffrey and Amodei, Dario},
  journal = {arXiv preprint arXiv:2001.08361},
  year    = {2020}
}
```

### [Hoffmann+2022] Chinchilla

```bibtex
@inproceedings{hoffmann2022chinchilla,
  title     = {Training Compute-Optimal Large Language Models},
  author    = {Hoffmann, Jordan and others},
  booktitle = {NeurIPS},
  year      = {2022}
}
```

### [Hu+2022] LoRA

```bibtex
@inproceedings{hu2022lora,
  title     = {LoRA: Low-Rank Adaptation of Large Language Models},
  author    = {Hu, Edward J. and Shen, Yelong and Wallis, Phillip and Allen-Zhu, Zeyuan and Li, Yuanzhi and Wang, Shean and Wang, Lu and Chen, Weizhu},
  booktitle = {ICLR},
  year      = {2022}
}
```

### [Dao+2022] FlashAttention

```bibtex
@inproceedings{dao2022flashattention,
  title     = {FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness},
  author    = {Dao, Tri and Fu, Daniel Y. and Ermon, Stefano and Rudra, Atri and R{\'e}, Christopher},
  booktitle = {NeurIPS},
  year      = {2022}
}
```

### [Su+2021] RoPE 旋转位置编码

```bibtex
@article{su2021roformer,
  title   = {RoFormer: Enhanced Transformer with Rotary Position Embedding},
  author  = {Su, Jianlin and Lu, Yu and Pan, Shengfeng and Murtadha, Ahmed and Wen, Bo and Liu, Yunfeng},
  journal = {arXiv preprint arXiv:2104.09864},
  year    = {2021}
}
```

### [Touvron+2023] LLaMA

```bibtex
@article{touvron2023llama,
  title   = {LLaMA: Open and Efficient Foundation Language Models},
  author  = {Touvron, Hugo and others},
  journal = {arXiv preprint arXiv:2302.13971},
  year    = {2023}
}
```

---

## 3. 计算机视觉

### [Krizhevsky+2012] AlexNet

```bibtex
@inproceedings{krizhevsky2012imagenet,
  title     = {ImageNet Classification with Deep Convolutional Neural Networks},
  author    = {Krizhevsky, Alex and Sutskever, Ilya and Hinton, Geoffrey E.},
  booktitle = {NeurIPS},
  year      = {2012}
}
```

### [Simonyan+2015] VGGNet

```bibtex
@inproceedings{simonyan2015very,
  title     = {Very Deep Convolutional Networks for Large-Scale Image Recognition},
  author    = {Simonyan, Karen and Zisserman, Andrew},
  booktitle = {ICLR},
  year      = {2015}
}
```

### [He+2016a] ResNet

```bibtex
@inproceedings{he2016deep,
  title     = {Deep Residual Learning for Image Recognition},
  author    = {He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
  booktitle = {CVPR},
  year      = {2016}
}
```

### [He+2016b] Identity Mappings

```bibtex
@inproceedings{he2016identity,
  title     = {Identity Mappings in Deep Residual Networks},
  author    = {He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
  booktitle = {ECCV},
  year      = {2016}
}
```

### [Dosovitskiy+2021] Vision Transformer (ViT)

```bibtex
@inproceedings{dosovitskiy2021an,
  title     = {An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale},
  author    = {Dosovitskiy, Alexey and others},
  booktitle = {ICLR},
  year      = {2021}
}
```

### [Ronneberger+2015] U-Net

```bibtex
@inproceedings{ronneberger2015unet,
  title     = {U-Net: Convolutional Networks for Biomedical Image Segmentation},
  author    = {Ronneberger, Olaf and Fischer, Philipp and Brox, Thomas},
  booktitle = {MICCAI},
  year      = {2015}
}
```

### [Kirillov+2023] Segment Anything (SAM)

```bibtex
@inproceedings{kirillov2023segment,
  title     = {Segment Anything},
  author    = {Kirillov, Alexander and others},
  booktitle = {ICCV},
  year      = {2023}
}
```

### [Radford+2021] CLIP

```bibtex
@inproceedings{radford2021learning,
  title     = {Learning Transferable Visual Models From Natural Language Supervision},
  author    = {Radford, Alec and others},
  booktitle = {ICML},
  year      = {2021}
}
```

---

## 4. 生成模型 (VAE / GAN / Diffusion)

### [Kingma+2014b] VAE

```bibtex
@inproceedings{kingma2014auto,
  title     = {Auto-Encoding Variational Bayes},
  author    = {Kingma, Diederik P. and Welling, Max},
  booktitle = {ICLR},
  year      = {2014}
}
```

### [Goodfellow+2014] GAN

```bibtex
@inproceedings{goodfellow2014generative,
  title     = {Generative Adversarial Nets},
  author    = {Goodfellow, Ian and Pouget-Abadie, Jean and Mirza, Mehdi and Xu, Bing and Warde-Farley, David and Ozair, Sherjil and Courville, Aaron and Bengio, Yoshua},
  booktitle = {NeurIPS},
  year      = {2014}
}
```

### [Ho+2020] DDPM

```bibtex
@inproceedings{ho2020denoising,
  title     = {Denoising Diffusion Probabilistic Models},
  author    = {Ho, Jonathan and Jain, Ajay and Abbeel, Pieter},
  booktitle = {NeurIPS},
  year      = {2020}
}
```

### [Song+2021] Score-Based SDE

```bibtex
@inproceedings{song2021score,
  title     = {Score-Based Generative Modeling through Stochastic Differential Equations},
  author    = {Song, Yang and Sohl-Dickstein, Jascha and Kingma, Diederik P. and Kumar, Abhishek and Ermon, Stefano and Poole, Ben},
  booktitle = {ICLR},
  year      = {2021}
}
```

### [Rombach+2022] Latent Diffusion (Stable Diffusion)

```bibtex
@inproceedings{rombach2022high,
  title     = {High-Resolution Image Synthesis with Latent Diffusion Models},
  author    = {Rombach, Robin and Blattmann, Andreas and Lorenz, Dominik and Esser, Patrick and Ommer, Bj{\"o}rn},
  booktitle = {CVPR},
  year      = {2022}
}
```

### [Karras+2019] StyleGAN

```bibtex
@inproceedings{karras2019style,
  title     = {A Style-Based Generator Architecture for Generative Adversarial Networks},
  author    = {Karras, Tero and Laine, Samuli and Aila, Timo},
  booktitle = {CVPR},
  year      = {2019}
}
```

---

## 5. 强化学习与对齐

### [Sutton+1988] TD 学习

```bibtex
@article{sutton1988learning,
  title   = {Learning to Predict by the Methods of Temporal Differences},
  author  = {Sutton, Richard S.},
  journal = {Machine Learning},
  volume  = {3},
  pages   = {9--44},
  year    = {1988}
}
```

### [Mnih+2015] DQN

```bibtex
@article{mnih2015human,
  title   = {Human-level control through deep reinforcement learning},
  author  = {Mnih, Volodymyr and others},
  journal = {Nature},
  volume  = {518},
  pages   = {529--533},
  year    = {2015}
}
```

### [Schulman+2017] PPO

```bibtex
@article{schulman2017proximal,
  title   = {Proximal Policy Optimization Algorithms},
  author  = {Schulman, John and Wolski, Filip and Dhariwal, Prafulla and Radford, Alec and Klimov, Oleg},
  journal = {arXiv preprint arXiv:1707.06347},
  year    = {2017}
}
```

### [Silver+2016] AlphaGo

```bibtex
@article{silver2016mastering,
  title   = {Mastering the game of Go with deep neural networks and tree search},
  author  = {Silver, David and others},
  journal = {Nature},
  volume  = {529},
  pages   = {484--489},
  year    = {2016}
}
```

### [Silver+2017] AlphaGo Zero

```bibtex
@article{silver2017mastering,
  title   = {Mastering the game of Go without human knowledge},
  author  = {Silver, David and others},
  journal = {Nature},
  volume  = {550},
  pages   = {354--359},
  year    = {2017}
}
```

### [Ouyang+2022] InstructGPT / RLHF

```bibtex
@inproceedings{ouyang2022training,
  title     = {Training language models to follow instructions with human feedback},
  author    = {Ouyang, Long and others},
  booktitle = {NeurIPS},
  year      = {2022}
}
```

### [Rafailov+2023] DPO

```bibtex
@inproceedings{rafailov2023direct,
  title     = {Direct Preference Optimization: Your Language Model is Secretly a Reward Model},
  author    = {Rafailov, Rafael and Sharma, Archit and Mitchell, Eric and Ermon, Stefano and Manning, Christopher D. and Finn, Chelsea},
  booktitle = {NeurIPS},
  year      = {2023}
}
```

---

## 6. AI for Science (蛋白质 / 材料 / 物理)

### [Jumper+2021] AlphaFold 2

```bibtex
@article{jumper2021highly,
  title   = {Highly accurate protein structure prediction with AlphaFold},
  author  = {Jumper, John and others},
  journal = {Nature},
  volume  = {596},
  pages   = {583--589},
  year    = {2021},
  doi     = {10.1038/s41586-021-03819-2}
}
```

### [Abramson+2024] AlphaFold 3

```bibtex
@article{abramson2024accurate,
  title   = {Accurate structure prediction of biomolecular interactions with AlphaFold 3},
  author  = {Abramson, Josh and others},
  journal = {Nature},
  volume  = {630},
  pages   = {493--500},
  year    = {2024}
}
```

### [Merchant+2023] GNoME 材料发现

```bibtex
@article{merchant2023scaling,
  title   = {Scaling deep learning for materials discovery},
  author  = {Merchant, Amil and Batzner, Simon and Schoenholz, Samuel S. and Aykol, Muratahan and Cheon, Gowoon and Cubuk, Ekin Dogus},
  journal = {Nature},
  volume  = {624},
  pages   = {80--85},
  year    = {2023}
}
```

### [Raissi+2019] PINN 物理约束神经网络

```bibtex
@article{raissi2019physics,
  title   = {Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations},
  author  = {Raissi, Maziar and Perdikaris, Paris and Karniadakis, George E.},
  journal = {Journal of Computational Physics},
  volume  = {378},
  pages   = {686--707},
  year    = {2019}
}
```

### [Batzner+2022] NequIP 等变神经网络势

```bibtex
@article{batzner2022e3equivariant,
  title   = {E(3)-equivariant graph neural networks for data-efficient and accurate interatomic potentials},
  author  = {Batzner, Simon and Musaelian, Albert and Sun, Lixin and Geiger, Mario and Mailoa, Jonathan P. and Kornbluth, Mordechai and Molinari, Nicola and Smidt, Tess E. and Kozinsky, Boris},
  journal = {Nature Communications},
  volume  = {13},
  pages   = {2453},
  year    = {2022}
}
```

---

## 7. 优化与数值方法

### [Nesterov+1983] 加速梯度法

```bibtex
@article{nesterov1983method,
  title   = {A method for solving the convex programming problem with convergence rate $O(1/k^2)$},
  author  = {Nesterov, Yurii},
  journal = {Doklady Akademii Nauk SSSR},
  volume  = {269},
  pages   = {543--547},
  year    = {1983}
}
```

### [Boyd+2004] 凸优化教材

```bibtex
@book{boyd2004convex,
  title     = {Convex Optimization},
  author    = {Boyd, Stephen and Vandenberghe, Lieven},
  publisher = {Cambridge University Press},
  year      = {2004}
}
```

### [Nocedal+2006] 数值优化

```bibtex
@book{nocedal2006numerical,
  title     = {Numerical Optimization},
  author    = {Nocedal, Jorge and Wright, Stephen J.},
  publisher = {Springer},
  edition   = {2},
  year      = {2006}
}
```

### [Trefethen+1997] 数值线性代数

```bibtex
@book{trefethen1997numerical,
  title     = {Numerical Linear Algebra},
  author    = {Trefethen, Lloyd N. and Bau, David},
  publisher = {SIAM},
  year      = {1997}
}
```

---

## 8. 数学基础 (代数 / 分析 / 几何)

### [Rudin+1976] 数学分析原理

```bibtex
@book{rudin1976principles,
  title     = {Principles of Mathematical Analysis},
  author    = {Rudin, Walter},
  publisher = {McGraw-Hill},
  edition   = {3},
  year      = {1976}
}
```

### [Axler+2015] 线性代数应该这样学

```bibtex
@book{axler2015linear,
  title     = {Linear Algebra Done Right},
  author    = {Axler, Sheldon},
  publisher = {Springer},
  edition   = {3},
  year      = {2015}
}
```

### [Strang+2016] 线性代数导论

```bibtex
@book{strang2016introduction,
  title     = {Introduction to Linear Algebra},
  author    = {Strang, Gilbert},
  publisher = {Wellesley-Cambridge Press},
  edition   = {5},
  year      = {2016}
}
```

### [Lee+2013] 光滑流形导论

```bibtex
@book{lee2013introduction,
  title     = {Introduction to Smooth Manifolds},
  author    = {Lee, John M.},
  publisher = {Springer},
  edition   = {2},
  year      = {2013}
}
```

### [Hatcher+2002] 代数拓扑

```bibtex
@book{hatcher2002algebraic,
  title     = {Algebraic Topology},
  author    = {Hatcher, Allen},
  publisher = {Cambridge University Press},
  year      = {2002}
}
```

---

## 9. 概率与统计

### [Durrett+2019] 概率论与实例

```bibtex
@book{durrett2019probability,
  title     = {Probability: Theory and Examples},
  author    = {Durrett, Rick},
  publisher = {Cambridge University Press},
  edition   = {5},
  year      = {2019}
}
```

### [Wasserman+2004] 全统计

```bibtex
@book{wasserman2004all,
  title     = {All of Statistics: A Concise Course in Statistical Inference},
  author    = {Wasserman, Larry},
  publisher = {Springer},
  year      = {2004}
}
```

### [Bishop+2006] 模式识别与机器学习

```bibtex
@book{bishop2006pattern,
  title     = {Pattern Recognition and Machine Learning},
  author    = {Bishop, Christopher M.},
  publisher = {Springer},
  year      = {2006}
}
```

### [Murphy+2022] 概率机器学习

```bibtex
@book{murphy2022probabilistic,
  title     = {Probabilistic Machine Learning: An Introduction},
  author    = {Murphy, Kevin P.},
  publisher = {MIT Press},
  year      = {2022}
}
```

---

## 10. 信息论与编码

### [Shannon+1948] 通信的数学理论

```bibtex
@article{shannon1948mathematical,
  title   = {A Mathematical Theory of Communication},
  author  = {Shannon, Claude E.},
  journal = {Bell System Technical Journal},
  volume  = {27},
  pages   = {379--423, 623--656},
  year    = {1948}
}
```

### [Cover+2006] 信息论基础

```bibtex
@book{cover2006elements,
  title     = {Elements of Information Theory},
  author    = {Cover, Thomas M. and Thomas, Joy A.},
  publisher = {Wiley},
  edition   = {2},
  year      = {2006}
}
```

### [MacKay+2003] 信息论 / 推断 / 学习

```bibtex
@book{mackay2003information,
  title     = {Information Theory, Inference, and Learning Algorithms},
  author    = {MacKay, David J. C.},
  publisher = {Cambridge University Press},
  year      = {2003}
}
```

---

## 11. 算法与理论计算机科学

### [Cormen+2022] 算法导论 (CLRS)

```bibtex
@book{cormen2022introduction,
  title     = {Introduction to Algorithms},
  author    = {Cormen, Thomas H. and Leiserson, Charles E. and Rivest, Ronald L. and Stein, Clifford},
  publisher = {MIT Press},
  edition   = {4},
  year      = {2022}
}
```

### [Sipser+2012] 计算理论导引

```bibtex
@book{sipser2012introduction,
  title     = {Introduction to the Theory of Computation},
  author    = {Sipser, Michael},
  publisher = {Cengage Learning},
  edition   = {3},
  year      = {2012}
}
```

### [Arora+2009] 计算复杂性

```bibtex
@book{arora2009computational,
  title     = {Computational Complexity: A Modern Approach},
  author    = {Arora, Sanjeev and Barak, Boaz},
  publisher = {Cambridge University Press},
  year      = {2009}
}
```

---

## 12. 教材与专著

### [Goodfellow+2016] 深度学习花书

```bibtex
@book{goodfellow2016deep,
  title     = {Deep Learning},
  author    = {Goodfellow, Ian and Bengio, Yoshua and Courville, Aaron},
  publisher = {MIT Press},
  year      = {2016},
  url       = {https://www.deeplearningbook.org}
}
```

### [Sutton+2018] 强化学习导论

```bibtex
@book{sutton2018reinforcement,
  title     = {Reinforcement Learning: An Introduction},
  author    = {Sutton, Richard S. and Barto, Andrew G.},
  publisher = {MIT Press},
  edition   = {2},
  year      = {2018}
}
```

### [Hastie+2009] 统计学习基础 (ESL)

```bibtex
@book{hastie2009elements,
  title     = {The Elements of Statistical Learning},
  author    = {Hastie, Trevor and Tibshirani, Robert and Friedman, Jerome},
  publisher = {Springer},
  edition   = {2},
  year      = {2009}
}
```

### [Koller+2009] 概率图模型

```bibtex
@book{koller2009probabilistic,
  title     = {Probabilistic Graphical Models: Principles and Techniques},
  author    = {Koller, Daphne and Friedman, Nir},
  publisher = {MIT Press},
  year      = {2009}
}
```

### [Prince+2023] 理解深度学习

```bibtex
@book{prince2023understanding,
  title     = {Understanding Deep Learning},
  author    = {Prince, Simon J. D.},
  publisher = {MIT Press},
  year      = {2023},
  url       = {https://udlbook.github.io/udlbook/}
}
```

---

## 引用规范

**正文引用**: 使用方括号短标签, 如 `[Vaswani+2017]`.

**参考本文件**: 在章节末尾附 "参考文献" 小节, 列出本章涉及条目, 例如:

```markdown
## 参考文献

- [Vaswani+2017] Transformer 原始论文, 见 BIBLIOGRAPHY.md §2
- [He+2016a] ResNet, 见 BIBLIOGRAPHY.md §3
- [Jumper+2021] AlphaFold 2, 见 BIBLIOGRAPHY.md §6
```

**BibTeX 导出**: 本文件条目可直接复制到 `.bib` 文件供 LaTeX 使用.

---

**条目总数**: 55 (覆盖 12 个领域, 从 1948 年 Shannon 到 2024 年 AlphaFold 3)
