# Pandoc PDF 排版模板 · README

> **位置**: `zh/templates/`
> **文件**: `pandoc-book.yaml` + `zh-book.tex`
> **用途**: 一键生成出版级 PDF / EPUB / HTML

---

## 一 · 快速开始

```bash
# 1. 安装依赖 (macOS)
brew install pandoc
brew install --cask mactex-no-gui
brew install --cask font-source-han-serif

# 2. 生成 PDF (在项目根目录运行)
cd /Users/chenchen/working/sourcecode/study/math/maths-cs-ai-compendium
pandoc -d zh/templates/pandoc-book.yaml \
       --template=zh/templates/zh-book.tex \
       -o book.pdf

# 3. 验证 PDF
open book.pdf
```

---

## 二 · 输出格式

### 2.1 PDF (推荐, 出版级)

```bash
pandoc -d zh/templates/pandoc-book.yaml \
       --template=zh/templates/zh-book.tex \
       -o book.pdf
```

输出 ~1500 页 A4 中文教材, 含目录 / 插图 / 公式 / 表格 / 参考文献。

### 2.2 EPUB (电子书)

```bash
pandoc -d zh/templates/pandoc-book.yaml \
       -t epub3 \
       --epub-cover-image=cover.jpg \
       -o book.epub
```

可在 Kindle / Apple Books / 微信读书阅读。

### 2.3 HTML (网页版)

```bash
pandoc -d zh/templates/pandoc-book.yaml \
       -t html5 \
       --self-contained \
       --css=style.css \
       -o book.html
```

单文件 HTML, 含 SVG 内嵌。

### 2.4 DOCX (Word)

```bash
pandoc -d zh/templates/pandoc-book.yaml \
       -o book.docx
```

Word 二次编辑。

---

## 三 · 排版特性

| 特性 | 说明 |
|------|------|
| **中文支持** | xeCJK + 思源宋体 |
| **章节编号** | 一级 / 二级 / 三级 (1.1.1) |
| **代码块** | 语法高亮 + 行号 |
| **数学公式** | LaTeX 完美渲染 |
| **表格** | booktabs 三线表 |
| **图形** | PNG / JPG / SVG |
| **超链接** | 蓝色链接 + 书签 |
| **目录** | 自动生成 3 级目录 |
| **参考文献** | BibTeX 自动 |

---

## 四 · 已知限制

- **SVG**: 需 `--pdf-engine=pdflatex` + Inkscape, 或用 PNG 替代
- **图表自动编号**: Pandoc 不支持, 需手工加 `图 1.1` 等
- **交叉引用**: 需手工维护 `\label{}` `\ref{}`
- **大文件编译**: 1500+ 页需 XeLaTeX + 充足内存 (8 GB+)

---

## 五 · 优化建议

### 5.1 减小 PDF 体积

```bash
# Ghostscript 压缩
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
   -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=book-compressed.pdf book.pdf
```

### 5.2 加封面图

```bash
# 用 ImageMagick 创建封面
convert -size 1600x2400 xc:white \
  -font /System/Library/Fonts/PingFang.ttc \
  -pointsize 80 -fill navy \
  -annotate +200+800 "数学·计算机·AI 全栈" \
  cover.jpg
```

### 5.3 加快编译

```bash
# 增量编译 (只编译修改章节)
pandoc -d zh/templates/pandoc-book.yaml --skip-index -o book.partial.tex
xelatex book.partial.tex
xelatex book.partial.tex  # 第二次跑生成目录
```

---

## 六 · CI/CD 集成

```yaml
# .github/workflows/pdf-build.yml
name: Build PDF
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install
        run: |
          sudo apt install -y pandoc texlive-xetex texlive-lang-chinese
      - name: Build
        run: |
          pandoc -d zh/templates/pandoc-book.yaml \
                 --template=zh/templates/zh-book.tex \
                 -o book.pdf
      - uses: actions/upload-artifact@v3
        with:
          name: book-pdf
          path: book.pdf
```

---

## 七 · 一句话总结

> **Pandoc + XeLaTeX = 出版级 PDF, 零成本, 高度可定制**。
> 当前模板已配置完整, 一行命令即可生成。
> **2-3 小时首次配置后, 后续每次重新生成 < 5 分钟**。
