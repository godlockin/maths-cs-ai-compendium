// preprocess-mermaid.mjs
// Render every ```mermaid fenced block in a Markdown file to PNG and
// replace the block with a relative image reference, so pandoc/WeasyPrint
// picks the diagram up as an <img> instead of showing the mermaid source.
//
// Reuses the existing cache under zh/images/diagrams (md5 of source →
// mermaid-<hash>.png) so unchanged blocks aren't re-rendered.
//
// Usage:
//   node ci/preprocess-mermaid.mjs <md-file> --cache-dir=<png-dir> [--write]
// Default prints the transformed Markdown to stdout; --write edits in place.

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join, resolve, basename } from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const args = process.argv.slice(2);
const mdFile = args.find(a => !a.startsWith('--'));
const write = args.includes('--write');
const cacheArg = args.find(a => a.startsWith('--cache-dir='));
if (!mdFile) {
  console.error('usage: preprocess-mermaid.mjs <md-file> --cache-dir=<dir> [--write]');
  process.exit(1);
}
const cacheDir = cacheArg ? resolve(cacheArg.split('=')[1]) : resolve('zh/images/diagrams');

// POSIX-style relative path from `from` to `to` (Node has no built-in for
// producing a path string; path.relative exists but uses platform sep).
import { relative } from 'node:path';
function relativePath(from, to) {
  let rel = relative(from, to).split('\\').join('/');
  if (!rel.startsWith('.')) rel = './' + rel;
  return encodeURI(rel);
}

const mdPath = resolve(mdFile);
let md = readFileSync(mdPath, 'utf-8');

function hashOf(code) {
  return createHash('md5').update(code).digest('hex').slice(0, 12);
}

// Extract mermaid blocks (only ```mermaid ... ```)
const blocks = [];
const re = /```mermaid\s*\n([\s\S]*?)```/g;
let m;
while ((m = re.exec(md)) !== null) {
  blocks.push({ code: m[1].replace(/\n+$/, ''), index: m.index, raw: m[0] });
}

if (!blocks.length) {
  process.stdout.write(md);
  process.exit(0);
}

// Launch one browser and render each missing block.
const browser = await chromium.launch();
const ctx = await browser.newContext({
  viewport: { width: 1600, height: 1000 },
  deviceScaleFactor: 2,
});
const page = await ctx.newPage();

const renderHtml = `<!DOCTYPE html><html><head><meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<style>body{margin:0;background:#fff;font-family:'PingFang SC','Microsoft YaHei',sans-serif;}
#wrap{display:inline-block;padding:8px;}</style></head>
<body><div id="wrap"></div></body></html>`;

for (const b of blocks) {
  const h = hashOf(b.code);
  const pngPath = join(cacheDir, `mermaid-${h}.png`);
  b.pngPath = pngPath;
  b.hash = h;
  if (existsSync(pngPath)) continue;
  await page.setContent(renderHtml, { waitUntil: 'networkidle' });
  const ok = await page.evaluate(async (code) => {
    mermaid.initialize({
      startOnLoad: false,
      theme: 'default',
      fontFamily: "'PingFang SC','Microsoft YaHei',sans-serif",
    });
    try {
      const { svg } = await mermaid.render('m' + Math.random().toString(36).slice(2), code);
      document.getElementById('wrap').innerHTML = svg;
      return true;
    } catch (e) {
      console.error('mermaid error:', e.message);
      return false;
    }
  }, b.code);
  if (!ok) continue;
  await page.waitForTimeout(150);
  const el = await page.$('#wrap svg');
  if (!el) continue;
  const png = await el.screenshot({ type: 'png', omitBackground: false });
  writeFileSync(pngPath, png);
}
await browser.close();

// Replace blocks with image references. Use an absolute (workspace-relative)
// path; pandoc's --resource-path and the fix-paths Lua filter resolve it.
let out = md;
// Replace from the end so indices stay valid.
for (let i = blocks.length - 1; i >= 0; i--) {
  const b = blocks[i];
  if (!existsSync(b.pngPath)) continue; // keep source if render failed
  // Path relative to the md file (works for both zh/** and repo root).
  let rel = relativePath(dirname(mdPath), b.pngPath);
  const img = `![mermaid diagram](${rel})`;
  out = out.slice(0, b.index) + img + out.slice(b.index + b.raw.length);
}

if (write) {
  writeFileSync(mdPath, out);
} else {
  process.stdout.write(out);
}