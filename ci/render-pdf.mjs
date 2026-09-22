// render-pdf.mjs
// Render a set of Markdown files into one high-quality PDF using Playwright.
//
// Pipeline (per md file):
//   1. Extract mermaid blocks + display/inline formulas
//   2. Render them to PNG via headless Chromium (mermaid@11 + MathJax)
//   3. Build HTML with <img> substitutions; collapse display math that
//      straddles table rows so tables don't break
//   4. Print each file to PDF (wide tables / wide mermaid → named landscape page)
//   5. Concatenate with pdfunite
//
// Usage:
//   node ci/render-pdf.mjs --target=<name> [--out=<file>] [--watermark=<text>]
//                          [--no-cover] [--from-list=<file>]
// Targets (built-in file sets):
//   jiaofu  zh/教辅/信息图/第*.md           (default, 信息图审校)
//   zh      zh/第*/**/*.md (main book)
//   en      chapter */*.md  (EN book)
// Or pass --from-list=<path> (newline-separated md files, relative to ROOT).

import { chromium } from 'playwright';
import { readFileSync, writeFileSync, mkdirSync, existsSync, statSync, readdirSync, unlinkSync } from 'node:fs';
import { resolve, join, basename, dirname } from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const OUT_DIR = join(ROOT, 'pdfs');
const FORMULA_DIR = join(ROOT, 'zh/images/formulas');
const DIAGRAM_DIR = join(ROOT, 'zh/images/diagrams');

// ---- CLI options ----
const opt = (name, def) => {
  const a = process.argv.find(x => x.startsWith(`--${name}=`));
  return a ? a.split('=').slice(1).join('=') : def;
};
const hasOpt = (name) => process.argv.includes(`--${name}`);
const TARGET = opt('target', 'jiaofu');
const WATERMARK = opt('watermark', 'DRAFT · 待审校');
const NO_COVER = hasOpt('no-cover');

const OUT_PDF = opt('out', join(OUT_DIR,
  TARGET === 'jiaofu' ? '信息图审校DRAFT.pdf' : `${TARGET}-render.pdf`));

for (const dir of [OUT_DIR, FORMULA_DIR, DIAGRAM_DIR]) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

// ---- Resolve the file set for the chosen target ----
function listMd(dirRel) {
  const dir = join(ROOT, dirRel);
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter(f => f.match(/\.md$/))
    .map(f => join(dirRel, f));
}

function resolveFiles() {
  const listFile = opt('from-list', null);
  if (listFile) {
    return readFileSync(resolve(listFile), 'utf-8')
      .split('\n').map(s => s.trim()).filter(Boolean);
  }
  if (TARGET === 'jiaofu') {
    return readdirSync(join(ROOT, 'zh/教辅/信息图'))
      .filter(f => f.match(/^第\d+章\.md$/)).sort()
      .map(f => join('zh/教辅/信息图', f));
  }
  if (TARGET === 'zh') {
    // One md per chapter dir, main book (sorted by chapter number).
    const dirs = readdirSync(join(ROOT, 'zh'))
      .filter(d => d.match(/^第\d+章/)).sort((a, b) => {
        const na = parseInt(a.match(/第(\d+)章/)[1], 10);
        const nb = parseInt(b.match(/第(\d+)章/)[1], 10);
        return na - nb;
      });
    return dirs.flatMap(d => listMd(join('zh', d)));
  }
  if (TARGET === 'en') {
    const dirs = readdirSync(ROOT)
      .filter(d => d.match(/^chapter \d+/)).sort((a, b) => {
        const na = parseInt(a.match(/chapter (\d+)/)[1], 10);
        const nb = parseInt(b.match(/chapter (\d+)/)[1], 10);
        return na - nb;
      });
    return dirs.flatMap(d => listMd(d));
  }
  throw new Error(`unknown target: ${TARGET}`);
}

const FILES = resolveFiles();
// Paths are ROOT-relative; absolutize for reading.
const fileAbs = (rel) => (rel.startsWith('/') ? rel : join(ROOT, rel));

// ---------- Extract blocks ----------
function extractBlocks(md) {
  const mermaid = [];
  const display = [];
  const inline = [];

  // mermaid blocks
  const mermaidRe = /```mermaid\n([\s\S]*?)```/g;
  let m;
  while ((m = mermaidRe.exec(md)) !== null) {
    mermaid.push({ code: m[1], offset: m.index, length: m[0].length });
  }

  // display $$...$$
  const displayRe = /\$\$([\s\S]+?)\$\$/g;
  while ((m = displayRe.exec(md)) !== null) {
    display.push({ code: m[1], offset: m.index, length: m[0].length });
  }

  // inline $...$
  const inlineRe = /(?<!\\)(?<!\$)\$([^$\n]+?)(?<!\\)\$(?!\$)/g;
  while ((m = inlineRe.exec(md)) !== null) {
    inline.push({ code: m[1], offset: m.index, length: m[0].length });
  }

  return { mermaid, display, inline };
}

function hashCode(code) {
  return createHash('md5').update(code).digest('hex').slice(0, 12);
}

// ---------- Build HTML ----------
function buildHtml(mdText, fileName, formulaMap, mermaidMap) {
  // Replace mermaid blocks with <img>
  let html = mdText
    .replace(/```mermaid\n([\s\S]*?)```/g, (match, code) => {
      const h = hashCode(code);
      const fname = `mermaid-${h}.png`;
      if (mermaidMap.has(h)) {
        return `<div class="mermaid-wrap"><img src="${mermaidMap.get(h)}" alt="mermaid diagram" /></div>`;
      }
      return `<pre class="mermaid-pending"><code>${escapeHtml(code)}</code></pre>`;
    })
    // Replace display math with <img>
    .replace(/\$\$([\s\S]+?)\$\$/g, (match, code) => {
      const h = hashCode(code);
      const fname = `formula-${h}.png`;
      if (formulaMap.has(h)) {
        return `<div class="formula-display"><img src="${formulaMap.get(h)}" alt="formula" /></div>`;
      }
      return `<pre class="formula-pending"><code>${escapeHtml(code)}</code></pre>`;
    })
    // Replace inline math with <img>
    .replace(/(?<!\\)(?<!\$)\$([^$\n]+?)(?<!\\)\$(?!\$)/g, (match, code) => {
      const h = hashCode(code);
      const fname = `formula-${h}.png`;
      if (formulaMap.has(h)) {
        return `<img class="formula-inline" src="${formulaMap.get(h)}" alt="formula" />`;
      }
      return `<code class="formula-pending">${escapeHtml(code)}</code>`;
    });

  // Escape remaining HTML
  return wrapHtml(html, fileName);
}

function escapeHtml(text) {
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function mdToHtmlSimple(md) {
  // Very basic md → html (sufficient for headings/lists/code/tables)
  // Headings
  let html = md;
  html = html.replace(/^######\s+(.+)$/gm, '<h6>$1</h6>');
  html = html.replace(/^#####\s+(.+)$/gm, '<h5>$1</h5>');
  html = html.replace(/^####\s+(.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^###\s+(.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^##\s+(.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^#\s+(.+)$/gm, '<h1>$1</h1>');
  // Horizontal rule
  html = html.replace(/^---$/gm, '<hr>');
  // Bold
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  // Italic
  html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  // Code blocks (4 spaces or ``` already replaced)
  return html;
}

function wrapHtml(body, fileName) {
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>${escapeHtml(fileName)}</title>
<style>
  @page { size: A4 portrait; margin: 18mm 14mm; }
  body { font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
         font-size: 11pt; line-height: 1.55; color: #222; }
  h1 { color: #0F4C81; font-size: 22pt; margin-top: 1em; border-bottom: 2px solid #E4B1A0; padding-bottom: 4px; }
  h2 { color: #0F4C81; font-size: 16pt; margin-top: 1em; }
  h3 { color: #3f3f3f; font-size: 13pt; }
  hr { border: none; border-top: 1px solid #E4B1A0; margin: 1em 0; }
  table { border-collapse: collapse; margin: 0.5em 0; font-size: 9pt; width: auto; max-width: 100%; }
  th, td { border: 1px solid #ccc; padding: 4px 8px; text-align: left; vertical-align: top; }
  th { background: #E8EEF6; font-weight: bold; }
  blockquote { border-left: 4px solid #E4B1A0; margin: 0.5em 0; padding: 6px 12px;
               background: rgba(255, 255, 255, 0.6); color: #3f3f3f; }
  code { background: #f5f5f5; padding: 1px 4px; border-radius: 3px; font-size: 90%; }
  pre { background: #f5f5f5; padding: 8px 12px; border-radius: 6px; overflow-x: auto; font-size: 9pt; }
  img { max-width: 100%; height: auto; }
  .formula-display { text-align: center; margin: 0.8em 0; }
  .formula-display img { display: inline-block; max-width: 90%; height: auto; }
  /* [v7 fix] Removed max-height that was truncating formulas */
  .formula-inline { display: inline-block; vertical-align: middle; height: auto; }
  .mermaid-wrap { text-align: center; margin: 1em 0; page-break-inside: avoid; }
  .mermaid-wrap img { max-width: 100%; }
  /* Wide table: rotate to landscape */
  table.wide { page-break-inside: avoid; }
  @media print {
    .page-break { page-break-before: always; }
    /* Force landscape for tables wider than 6 cols */
    table.wide { page-break-inside: avoid; }
  }
</style>
</head>
<body>
${mdToHtmlSimple(body)}
</body>
</html>`;
}

// ---------- Detect wide tables ----------
function detectWideTables(md) {
  // Returns list of {startLine, endLine, numCols} for tables with >5 columns
  const lines = md.split('\n');
  const wideTables = [];
  let inTable = false;
  let tableStart = 0;
  let numCols = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line.startsWith('|') && line.endsWith('|')) {
      if (!inTable) {
        inTable = true;
        tableStart = i;
        numCols = line.split('|').length - 2;
      }
    } else {
      if (inTable) {
        if (numCols >= 5) {
          wideTables.push({ startLine: tableStart, endLine: i - 1, numCols });
        }
        inTable = false;
      }
    }
  }
  return wideTables;
}

// Collapse display-math blocks that straddle a table row into a single-line
// inline formula `$\\displaystyle ...$`. Without this, the display-math
// replacement emits a block-level <div> inside a table row and breaks the
// table. Handles three opener shapes: multi-line `$$\n`, single-line `$$ `,
// and mid-row `$$code` (next char non-alphanumeric). Detects table context
// either by `|` on the opener/closer line or by walking back to a `|` row.
function collapseTableStraddlingDisplayMath(html) {
  const lineStarts = [0];
  for (let p = 0; p < html.length; p++) if (html[p] === '\n') lineStarts.push(p + 1);
  const ub = (v) => {
    let lo = 0, hi = lineStarts.length;
    while (lo < hi) { const mid = (lo + hi) >> 1; if (lineStarts[mid] <= v) lo = mid + 1; else hi = mid; }
    return lo;
  };
  const lineStartOf = (i) => lineStarts[ub(i) - 1];
  const lineEndOf = (i) => { const n = html.indexOf('\n', i); return n === -1 ? html.length : n; };

  const result = [];
  let i = 0;
  while (i < html.length) {
    let openStart = -1, openEnd = -1;
    if (html.startsWith('$$', i)) {
      const prev = i > 0 ? html[i - 1] : '\n';
      const next = html[i + 2];
      if (prev !== '\\' && prev !== '$' && (next === undefined || !/[a-zA-Z0-9]/.test(next))) {
        openStart = i; openEnd = i + 2;
      }
    }
    if (openStart === -1) { result.push(html[i]); i++; continue; }
    const closeRe = /\$\$/g;
    closeRe.lastIndex = openEnd;
    const cm = closeRe.exec(html);
    if (!cm || cm.index === openEnd) { result.push(html.slice(i, openEnd)); i = openEnd; continue; }
    const closeStart = cm.index, closeEnd = cm.index + 2;
    const body = html.slice(openEnd, closeStart);
    const bodyLines = body.replace(/^\n+/, '').replace(/\n+$/, '').split('\n');
    const stripText = (s) => s.replace(/\\text\{[^}]*\}/g, '').replace(/\\mathrm\{[^}]*\}/g, '');
    let pure = true;
    for (const ln of bodyLines) {
      const t = ln.trim();
      if (t === '' || /^#{1,6}\s/.test(t) || /^\s*>+/.test(t) || /\*\*|---|^\s*[-*]\s+/.test(t)
          || /[一-鿿]/.test(stripText(t)) || /\$[^$\n]+\$/.test(t)) { pure = false; break; }
    }
    const beforePart = html.slice(lineStartOf(openStart), openStart);
    const afterEnd = lineEndOf(closeEnd);
    const afterPart = html.slice(closeEnd, afterEnd);
    let inTableMultiLine = false;
    {
      let walk = lineStartOf(openStart);
      for (let s = 0; s < 10 && walk > 0; s++) {
        const ps = lineStarts[ub(walk) - 1];
        const pl = html.slice(ps, walk - 1).trim();
        if (pl === '') break;
        if (pl.startsWith('|')) { inTableMultiLine = true; break; }
        walk = ps;
      }
    }
    const onTable = beforePart.includes('|') || afterPart.includes('|') || inTableMultiLine;
    if (pure && onTable) {
      const joined = body.replace(/\s+/g, ' ').trim();
      const nd = afterPart.indexOf('$$');
      if (nd === -1) {
        result.push(`$\\displaystyle ${joined}$${afterPart}`);
        i = afterEnd < html.length && html[afterEnd] === '\n' ? afterEnd + 1 : afterEnd;
        // Pull continuation lines (author-wrapped table rows) onto this row.
        for (;;) {
          const nl = html.indexOf('\n', i);
          const nlText = (nl === -1 ? html.slice(i) : html.slice(i, nl)).trim();
          const cont = nlText.length > 0 && !nlText.startsWith('|') && !nlText.startsWith('$$')
            && !/^#{1,6}\s/.test(nlText) && !/^>/.test(nlText)
            && nlText.includes('|') && nlText.endsWith('|');
          if (!cont) break;
          result.push(nlText);
          i = nl === -1 ? html.length : nl + 1;
        }
      } else {
        result.push(`$\\displaystyle ${joined}$${afterPart.slice(0, nd)}`);
        i = closeEnd + nd;
      }
      continue;
    }
    result.push(html.slice(i, openEnd));
    i = openEnd;
  }
  return result.join('');
}

// ---------- Render mermaid to PNG via Playwright ----------
async function renderMermaidToPng(page, code) {
  const html = `<!DOCTYPE html><html><head><meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<style>body{margin:0;background:#fff;font-family:'PingFang SC','Microsoft YaHei',sans-serif;}
.mermaid-wrap{display:inline-block;padding:24px;}</style></head>
<body><div class="mermaid-wrap" id="wrap"></div></body></html>`;

  await page.setContent(html, { waitUntil: 'networkidle' });
  const ok = await page.evaluate(async (code) => {
    mermaid.initialize({ startOnLoad: false, theme: 'default',
      fontFamily: "'PingFang SC','Microsoft YaHei',sans-serif",
      securityLevel: 'strict' });
    try {
      const { svg } = await mermaid.render('m' + Date.now(), code);
      document.getElementById('wrap').innerHTML = svg;
      return true;
    } catch (e) {
      console.error('mermaid error:', e.message);
      return false;
    }
  }, code);
  if (!ok) return null;

  await page.waitForTimeout(300);
  const el = await page.$('#wrap svg');
  if (!el) return null;
  const png = await el.screenshot({ type: 'png', omitBackground: false });
  // [Phase1-D fix] Get bbox for aspect ratio check
  const bbox = await el.boundingBox();
  return { png, width: bbox?.width || 0, height: bbox?.height || 0 };
}

// ---------- Render formula to PNG via MathJax ----------
async function renderFormulaToPng(page, latex, isDisplay) {
  // Render every formula with the default `$$ ... $$` display delimiter so
  // MathJax parses it cleanly (custom `\[ \]` collides with processEscapes
  // and produced "Missing delimiter" errors). Inline (non-matrix) formulas
  // are still rendered at 22px and used as inline PNGs downstream.
  const hasMatrix = /\\begin\{(array|matrix|pmatrix|bmatrix|smallmatrix|align|aligned|cases)\}/.test(latex)
    || /\\cr\b/.test(latex);
  const useDisplay = isDisplay || hasMatrix;
  const fontSize = hasMatrix ? 18 : (isDisplay ? 28 : 22);
  const html = `<!DOCTYPE html><html><head><meta charset="utf-8">
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$','$']],
    displayMath: [['$$','$$']],
    processEscapes: true,
  },
  startup: {
    ready: () => { MathJax.startup.defaultReady(); }
  }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
  body { margin: 0; padding: 12px; background: #fff;
         font-family: 'Times New Roman', serif;
         font-size: ${fontSize}px;
         max-width: 700px; }
  .formula { display: inline-block; padding: 4px 8px; font-size: ${fontSize}px; }
  .display { display: block; text-align: center; padding: 12px; margin: 8px auto;
            font-size: ${fontSize}px;
            max-width: 600px; }
</style></head>
<body>
<div id="out" class="${useDisplay ? 'display' : 'formula'}">$${latex}$</div>
</body></html>`;

  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.MathJax && MathJax.typesetPromise, { timeout: 15000 }).catch(() => {});
  await page.evaluate(async () => {
    if (window.MathJax && MathJax.typesetPromise) {
      await MathJax.typesetPromise();
    }
  });
  await page.waitForTimeout(300);
  // Screenshot `#out` (mjx-container collapses its height with position:relative).
  const el = await page.$('#out');
  if (!el) return null;
  const png = await el.screenshot({ type: 'png', omitBackground: true });
  return png;
}

// Wrapper that isolates each formula render in a fresh context so MathJax
// state from earlier formulas can't corrupt later ones (long book runs hit
// "Cannot read properties of null" otherwise).
async function safeRenderFormula(browser, latex, isDisplay) {
  const ctx = await browser.newContext({ viewport: { width: 1200, height: 600 } });
  const page = await ctx.newPage();
  try {
    return await renderFormulaToPng(page, latex, isDisplay);
  } catch (e) {
    console.error(`formula render failed: ${e.message.slice(0, 100)}`);
    return null;
  } finally {
    await ctx.close();
  }
}

// ---------- Main ----------
async function main() {
  const files = FILES;
  console.log(`Target=${TARGET}; found ${files.length} files`);
  console.log(`Output=${OUT_PDF}; watermark="${WATERMARK}"`);

  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1600, height: 1000 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();
  const pdfsToMerge = [];

  if (!NO_COVER) {
    const titleMap = {
      jiaofu: '教辅·信息图 排版审校',
      zh: '数学、计算机与 AI 综合手册 (中文版)',
      en: 'Mathematics, Computer Science & AI Compendium',
    };
    const coverHtml = `<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
@page { size: A4 portrait; margin: 25mm; }
html::before {
  content: "${WATERMARK}";
  position: fixed; top: 50%; left: 50%;
  transform: translate(-50%, -50%) rotate(-30deg);
  font-size: 64pt; font-weight: bold;
  color: rgba(240, 90, 90, 0.10);
  z-index: -1; pointer-events: none; white-space: nowrap;
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
}
body { font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; color: #222; }
h1 { color: #0F4C81; font-size: 26pt; }
.cover-stats { margin-top: 20px; }
table { border-collapse: collapse; margin-top: 12px; width: 100%; font-size: 10pt; }
th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; }
th { background: #0F4C81; color: #fff; }
</style></head><body>
<h1>${titleMap[TARGET] || TARGET}</h1>
<p>包含 <b>${files.length} 个</b> Markdown 文件</p>
<div class="cover-stats">
<h2>渲染说明</h2>
<ul>
  <li><b>mermaid 块</b>：已预渲染为 PNG 嵌入</li>
  <li><b>$$ display / $ inline 公式</b>：已预渲染为 PNG 嵌入</li>
  <li><b>宽表格 / 宽图</b>：自动旋转为横向页面</li>
</ul>
</div>
</body></html>`;
    const coverPath = join(OUT_DIR, '_cover.html');
    const coverPdf = join(OUT_DIR, '_cover.pdf');
    writeFileSync(coverPath, coverHtml);
    await page.goto(`file://${coverPath}`, { waitUntil: 'networkidle' });
    await page.pdf({ path: coverPdf, format: 'A4', printBackground: true,
      margin: { top: '25mm', bottom: '20mm', left: '20mm', right: '20mm' } });
    pdfsToMerge.push(coverPdf);
  }

  for (const rel of files) {
    const mdPath = fileAbs(rel);
    console.log(`Processing ${rel}...`);
    let mdText = readFileSync(mdPath, 'utf-8');
    mdText = collapseTableStraddlingDisplayMath(mdText);
    const { mermaid, display, inline } = extractBlocks(mdText);

    const mermaidMap = new Map();
    for (const block of mermaid) {
      const h = hashCode(block.code);
      const pngPath = join(DIAGRAM_DIR, `mermaid-${h}.png`);
      let aspect = 1;
      if (!existsSync(pngPath)) {
        const result = await renderMermaidToPng(page, block.code);
        if (result && result.png) {
          writeFileSync(pngPath, result.png);
          aspect = result.height > 0 ? result.width / result.height : 1;
        }
      } else {
        const dim = pngDimensions(pngPath);
        if (dim) aspect = dim.w / dim.h;
      }
      mermaidMap.set(h, { path: pngPath, aspect });
    }

    const formulaMap = new Map();
    for (const block of [...display, ...inline]) {
      const h = hashCode(block.code);
      const pngPath = join(FORMULA_DIR, `formula-${h}.png`);
      const isMatrix = /\\begin\{(array|matrix|pmatrix|bmatrix|smallmatrix|align|aligned|cases)\}/.test(block.code)
        || /\\cr\b/.test(block.code);
      const needsDisplay = display.includes(block) || isMatrix;
      if (!existsSync(pngPath)) {
        const png = await safeRenderFormula(browser, block.code, needsDisplay);
        if (png) writeFileSync(pngPath, png);
      }
      if (isMatrix && existsSync(pngPath)) {
        try {
          execFileSync('python3', [
            join(ROOT, 'scripts/resize-matrix-png.py'), pngPath, '360',
          ], { stdio: 'ignore' });
        } catch (e) { /* best-effort */ }
      }
      if (existsSync(pngPath)) formulaMap.set(h, pngPath);
    }

    const pngToBase64 = (pngPath) =>
      'data:image/png;base64,' + readFileSync(pngPath).toString('base64');

    let html = mdText;
    html = html.replace(/```mermaid\n([\s\S]*?)```/g, (match, code) => {
      const h = hashCode(code.replace(/\n+$/, ''));
      const entry = mermaidMap.get(h);
      if (entry && existsSync(entry.path)) {
        const cls = entry.aspect >= 2.0 ? ' class="mermaid-wrap wide"' : ' class="mermaid-wrap"';
        return `\n<div${cls}><img src="file://${entry.path}" /></div>\n`;
      }
      return `<pre>${escapeHtml(code)}</pre>`;
    });
    html = html.replace(/\$\$([\s\S]+?)\$\$/g, (match, code) => {
      const h = hashCode(code);
      if (formulaMap.has(h)) {
        return `\n<div class="formula-display"><img class="formula-img" src="${pngToBase64(formulaMap.get(h))}" /></div>\n`;
      }
      return `<pre>${escapeHtml(code)}</pre>`;
    });
    html = html.replace(/(?<!\\)(?<!\$)\$([^$\n]+?)(?<!\\)\$(?!\$)/g, (match, code) => {
      const h = hashCode(code);
      if (formulaMap.has(h)) {
        return `<img class="formula-inline" src="${pngToBase64(formulaMap.get(h))}" />`;
      }
      return `<code>${escapeHtml(code)}</code>`;
    });

    html = processMdToHtml(html);
    const wideTables = detectWideTables(mdText);
    const fullHtml = wrapInPageHtml(html, basename(mdPath), wideTables, WATERMARK);

    const stamp = basename(mdPath, '.md').replace(/[^\w一-鿿.-]+/g, '_');
    const htmlPath = join(OUT_DIR, `_tmp_${stamp}.html`);
    const pdfPath = join(OUT_DIR, `_tmp_${stamp}.pdf`);
    writeFileSync(htmlPath, fullHtml);

    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(400);
    await page.pdf({
      path: pdfPath,
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: true,
      margin: { top: '20mm', bottom: '20mm', left: '15mm', right: '15mm' },
    });
    pdfsToMerge.push(pdfPath);
  }

  await browser.close();

  console.log('\nMerging PDFs...');
  try {
    execFileSync('pdfunite', [...pdfsToMerge, OUT_PDF], { stdio: 'inherit' });
    console.log(`✓ Merged into ${OUT_PDF}`);
  } catch (e) {
    console.log('pdfunite failed:', e.message);
  }

  // Clean intermediate artefacts.
  for (const p of pdfsToMerge) {
    try { unlinkSync(p); } catch {}
  }
  for (const p of [join(OUT_DIR, '_cover.html'), join(OUT_DIR, '_cover.pdf')]) {
    try { unlinkSync(p); } catch {}
  }
  for (const f of readdirSync(OUT_DIR)) {
    if (f.startsWith('_tmp_') && f.endsWith('.html')) {
      try { unlinkSync(join(OUT_DIR, f)); } catch {}
    }
  }
}

// PNG width/height from IHDR (no deps).
function pngDimensions(path) {
  try {
    const buf = readFileSync(path);
    if (buf.length < 24 || buf.toString('ascii', 12, 16) !== 'IHDR') return null;
    return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
  } catch { return null; }
}
function processMdToHtml(md) {
  // Convert markdown structure to HTML
  let html = md;
  // Code blocks ``` ... ```
  html = html.replace(/^```(\w*)\n([\s\S]*?)```$/gm, (m, lang, code) => {
    return `<pre><code class="language-${lang}">${escapeHtml(code)}</code></pre>`;
  });

  // Process line by line for tables, headings, lists, blockquotes
  const lines = html.split('\n');
  const out = [];
  let inTable = false;
  let tableBuf = [];
  let inListType = null;  // 'ul' | 'ol' | null
  let listBuf = [];
  let inBlockquote = false;
  let blockquoteBuf = [];

  // Inline markdown regexes [Phase1-A fix]
  function applyInlineMarkdown(text) {
    return text
      .replace(/~~([^~\n]+)~~/g, '<del>$1</del>')
      .replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*\n]+)\*/g, '<em>$1</em>')
      .replace(/`([^`\n]+)`/g, '<code>$1</code>')
      .replace(/\[([^\]]+)\]\(([^)\n]+)\)/g, (m, label, url) => {
        // [security] Reject non-http schemes (javascript:, data:, etc.)
        const u = url.trim().toLowerCase();
        if (!/^https?:\/\//i.test(u)) return m;
        return `<a href="${escapeHtml(url)}">${escapeHtml(label)}</a>`;
      });
  }
  // Inline markdown but preserve <img> tags
  function applyInlineKeepImg(text) {
    const parts = text.split(/(<img\s[^>]*>)/g);
    return parts.map(p => p.startsWith('<img') ? p : applyInlineMarkdown(escapeHtml(p))).join('');
  }

  function flushTable() {
    if (!tableBuf.length) return;
    const rows = tableBuf.map(r => r.trim()).filter(r => r.startsWith('|') && r.endsWith('|'));
    if (rows.length < 2) {
      out.push(...tableBuf);
      tableBuf = [];
      return;
    }
    const data = rows.filter(r => !/^[\s\-:|]+$/.test(r.trim().slice(1, -1)))
      .map(r => r.slice(1, -1).split('|').map(c => c.trim()));
    const numCols = data[0]?.length || 0;
    const numRows = data.length;

    // [Phase1-C fix] Width-based rotation decision
    const portraitAvail = 180;   // mm
    const landscapeAvail = 257;  // mm
    let totalWidth = 0;
    for (let c = 0; c < numCols; c++) {
      let colW = 0;
      for (const row of data) {
        const cell = row[c] || '';
        if (cell.includes('<img')) {
          colW = Math.max(colW, 30);  // formula PNG ≈ 30mm
        } else {
          const cjk = (cell.match(/[一-鿿]/g) || []).length;
          const other = cell.length - cjk;
          colW = Math.max(colW, cjk * 2.5 + other * 1.3);
        }
      }
      totalWidth += colW;
    }
    // Only rotate if: ≥3 rows AND portrait overflows AND landscape fits
    let wideClass = '';
    if (numRows >= 3 && totalWidth > portraitAvail && totalWidth <= landscapeAvail) {
      wideClass = ' class="wide"';
    }

    out.push(`<table${wideClass}>`);
    for (let i = 0; i < data.length; i++) {
      const tag = i === 0 ? 'th' : 'td';
      out.push('<tr>' + data[i].map(c => `<${tag}>${applyInlineKeepImg(c)}</${tag}>`).join('') + '</tr>');
    }
    out.push('</table>');
    tableBuf = [];
  }

  function flushList() {
    if (!listBuf.length || !inListType) return;
    out.push(`<${inListType}>`);
    for (const item of listBuf) out.push(`<li>${applyInlineKeepImg(item)}</li>`);
    out.push(`</${inListType}>`);
    listBuf = [];
    inListType = null;
  }

  function flushBlockquote() {
    if (!blockquoteBuf.length) return;
    const content = blockquoteBuf.map(t => applyInlineKeepImg(t)).join('<br>');
    out.push(`<blockquote>${content}</blockquote>`);
    blockquoteBuf = [];
    inBlockquote = false;
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    // Skip pre-substituted raw HTML blocks (div/img/pre). Accumulate an
    // entire <pre>...</pre> as one unit so its inner lines aren't wrapped
    // in <p> or escaped (otherwise the literal tags show in the PDF).
    if (trimmed.startsWith('<pre')) {
      if (inTable) { flushTable(); inTable = false; }
      if (inListType) flushList();
      if (inBlockquote) flushBlockquote();
      out.push(line);
      for (;;) {
        if (i + 1 >= lines.length) break;
        const nxt = lines[i + 1].trim();
        out.push(lines[i + 1]);
        i++;
        if (nxt.includes('</pre>')) break;
      }
      continue;
    }
    if (trimmed.startsWith('<div ') || trimmed.startsWith('<img ') || trimmed.startsWith('</div>')
        || trimmed.startsWith('</pre>')) {
      if (inTable) { flushTable(); inTable = false; }
      if (inListType) flushList();
      if (inBlockquote) flushBlockquote();
      out.push(line);
      continue;
    }

    // Table
    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      if (inListType) flushList();
      if (inBlockquote) flushBlockquote();
      inTable = true;
      tableBuf.push(line);
      continue;
    } else if (inTable) {
      flushTable();
      inTable = false;
    }

    // Headings
    const h = trimmed.match(/^(#{1,6})\s+(.+)$/);
    if (h) {
      if (inListType) flushList();
      if (inBlockquote) flushBlockquote();
      out.push(`<h${h[1].length}>${applyInlineKeepImg(h[2])}</h${h[1].length}>`);
      continue;
    }

    // HR
    if (/^-{3,}$|^\*{3,}$/.test(trimmed)) {
      if (inListType) flushList();
      if (inBlockquote) flushBlockquote();
      out.push('<hr>');
      continue;
    }

    // Blockquote [Phase1-A fix] multi-line merging
    if (trimmed.startsWith('>')) {
      if (inListType) flushList();
      inBlockquote = true;
      blockquoteBuf.push(trimmed.replace(/^>+\s?/, ''));
      continue;
    } else if (inBlockquote) {
      flushBlockquote();
    }

    // [Phase1-A fix] Ordered list
    const ol = trimmed.match(/^(\d+)\.\s+(.+)$/);
    if (ol) {
      if (inBlockquote) flushBlockquote();
      if (inListType && inListType !== 'ol') flushList();
      inListType = 'ol';
      listBuf.push(ol[2]);
      continue;
    }

    // Unordered list
    const li = trimmed.match(/^[-*]\s+(.+)$/);
    if (li) {
      if (inBlockquote) flushBlockquote();
      if (inListType && inListType !== 'ul') flushList();
      inListType = 'ul';
      listBuf.push(li[1]);
      continue;
    } else if (inListType) {
      flushList();
    }

    // Empty
    if (!trimmed) {
      if (inListType) flushList();
      if (inBlockquote) flushBlockquote();
      out.push('');
      continue;
    }

    // Paragraph
    out.push(`<p>${applyInlineKeepImg(trimmed)}</p>`);
  }
  flushTable();
  flushList();
  flushBlockquote();

  return out.join('\n');
}

function wrapInPageHtml(body, fileName, wideTables, watermark = 'DRAFT · 待审校') {
  const processedBody = body;
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>${escapeHtml(fileName)}</title>
<style>
  @page { size: A4 portrait; margin: 18mm 14mm; }
  @page wide { size: A4 landscape; margin: 14mm 18mm; }
  html::before {
    content: "${watermark}";
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%) rotate(-30deg);
    font-size: 72pt;
    font-weight: bold;
    color: rgba(240, 90, 90, 0.10);
    z-index: -1;
    pointer-events: none;
    white-space: nowrap;
    font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
  }
  @page :left { @bottom-left { content: "数学·CS·AI 综合手册 (中文版) · ${watermark}"; font-size: 8pt; color: #666; } }
  @page :right { @bottom-right { content: "REVIEW ONLY"; font-size: 8pt; color: #666; } }
  body { font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
         font-size: 10pt; line-height: 1.55; color: #222; }
  h1 { color: #0F4C81; font-size: 20pt; margin-top: 0.5em;
       border-bottom: 2px solid #E4B1A0; padding-bottom: 4px; }
  h2 { color: #0F4C81; font-size: 14pt; margin-top: 1em; }
  h3 { color: #3f3f3f; font-size: 12pt; }
  hr { border: none; border-top: 1px solid #E4B1A0; margin: 1em 0; }
  table { border-collapse: collapse; margin: 0.5em 0; font-size: 8pt; }
  table.wide { page: wide; }
  th, td { border: 1px solid #ccc; padding: 3px 6px; text-align: left; vertical-align: top; }
  th { background: #E8EEF6; font-weight: bold; }
  td .formula-display { margin: 0; }
  td .formula-display img { max-width: 55mm; height: auto; }
  td .formula-inline { height: auto; }
  blockquote { border-left: 4px solid #E4B1A0; margin: 0.5em 0; padding: 4px 10px;
               background: rgba(255, 255, 255, 0.6); color: #3f3f3f; font-size: 9pt; }
  code { background: #f5f5f5; padding: 1px 3px; border-radius: 3px; font-size: 85%; }
  pre { background: #f5f5f5; padding: 6px 10px; border-radius: 5px; overflow-x: auto;
        font-size: 8pt; }
  img { max-width: 100%; height: auto; }
  .formula-display { text-align: center; margin: 0.6em 0; }
  .formula-display img { display: inline-block; max-width: 85%; }
  .formula-inline { display: inline-block; vertical-align: middle; }
  .mermaid-wrap { text-align: center; margin: 0.8em 0; page-break-inside: avoid; }
  .mermaid-wrap img { max-width: 90%; }
  .mermaid-wrap.wide { page: wide; }
  .mermaid-wrap.wide img { max-width: 85%; max-height: 220mm; }
  ul { margin: 0.3em 0; }
  li { margin: 0.2em 0; }
  p { margin: 0.4em 0; }
</style>
</head>
<body>
<h1>${escapeHtml(fileName)}</h1>
${processedBody}
</body>
</html>`;
}

main().catch(e => {
  console.error('Error:', e);
  process.exit(1);
});