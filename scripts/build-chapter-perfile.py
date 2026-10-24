#!/usr/bin/env python3
"""
build-chapter-perfile.py — 章节构建管线 (per-file 模式)

用法:
    python3 scripts/build-chapter-perfile.py Ch09
    python3 scripts/build-chapter-perfile.py Ch09 --skip-gates

为什么需要它:
    scripts/build-chapter.sh 把所有 md 交给**一次** render-formulas (整章一个
    Chromium 进程)。整章规模下 Chromium 有概率启动失败或挂起 (见
    zhbook-publish-pipeline-hazards #11), 且 .sh 是 gitignored 本地文件, 丢失后
    门禁逻辑与构建顺序会一起消失。本脚本是等价流程的**可提交**版本, 逐文件渲染,
    单文件失败不影响其余文件, 并把 parity + hygiene 两道门禁挂死在最前面。

依赖:
    bun 在 PATH 上 (exec-task 场景需 export PATH=$HOME/.bun/bin:$PATH)
    baoyu-markdown-to-html 的 main.ts (MD2HTML)
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD2HTML = Path(os.environ.get(
    "BAOYU_MD2HTML",
    "/Users/chenchen/working/sourcecode/tools/llm_apps/ultraskills/community/"
    "baoyu-skills/baoyu-markdown-to-html/scripts/main.ts",
))


def run(cmd: list[str], cwd: Path = ROOT) -> int:
    print("  $ " + " ".join(str(c) for c in cmd), flush=True)
    env = dict(os.environ)
    env["PATH"] = os.path.expanduser("~/.bun/bin") + ":" + env.get("PATH", "")
    return subprocess.run(cmd, cwd=cwd, env=env).returncode


def chapter_dir(num: str) -> Path | None:
    hits = sorted(glob.glob(str(ROOT / f"zh/第{num}章*")))
    return Path(hits[0]) if hits else None


def gates(chdir: Path) -> bool:
    mds = sorted(glob.glob(str(chdir / "*.md")))
    print("→ 发布门禁 (parity + hygiene)")
    for script in ("check-math-parity.py", "check-publish-hygiene.py"):
        rc = run([sys.executable, str(ROOT / "scripts" / script), *mds])
        if rc != 0:
            print(f"!! 门禁失败: {script}")
            return False
    return True


def render_svgs(mds: list[str]) -> None:
    """把本章 md 里引用的 zh/images/*.svg 渲染成 images/png/*.png。

    不做这一步的话, patch-html-svg-to-png.mjs 会因为找不到对应 PNG 而**静默跳过**
    (它先 existsSync 再改写), 草稿里就会留下 .svg 引用 —— 微信不渲染 SVG, 结果是裂图。
    """
    import re
    svgs: list[str] = []
    for md in mds:
        text = Path(md).read_text(encoding="utf-8")
        for ref in re.findall(r"!\[[^\]]*\]\(([^)]+\.svg)\)", text):
            p = (Path(md).parent / ref).resolve()
            if p.exists() and str(p) not in svgs:
                svgs.append(str(p))
    if not svgs:
        return
    print(f"→ 渲染本章 SVG → PNG ({len(svgs)} 张)")
    run(["bun", str(ROOT / "scripts/svg-to-png.mjs"), *svgs])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", help="章号, 如 Ch09")
    ap.add_argument("--skip-gates", action="store_true")
    args = ap.parse_args()

    num = args.chapter.removeprefix("Ch")
    chdir = chapter_dir(num)
    if chdir is None:
        print(f"! 找不到 zh/第{num}章*/ 目录")
        return 1
    html_dir = ROOT / "wechat" / "articles" / f"ch{num}"
    html_dir.mkdir(parents=True, exist_ok=True)

    if not args.skip_gates and not gates(chdir):
        return 2

    mds = sorted(glob.glob(str(chdir / "*.md")))
    render_svgs(mds)
    backup = Path(f"/tmp/build-ch{num}-backup")
    if backup.exists():
        shutil.rmtree(backup)
    backup.mkdir(parents=True)
    for md in mds:
        shutil.copy2(md, backup / Path(md).name)
    print(f"→ 备份 md 到 {backup}")

    def restore() -> None:
        for md in mds:
            src = backup / Path(md).name
            if src.exists():
                shutil.copy2(src, md)
        print("→ md 已恢复 LaTeX 源")

    failed = []
    try:
        for md in mds:
            base = Path(md).stem
            print(f"=== {base} ===")
            if run(["bun", str(ROOT / "scripts/render-formulas.mjs"), md]) != 0:
                print(f"! render-formulas 失败: {base}")
                failed.append(base)
                continue
            run(["bun", str(MD2HTML), md, "--theme", "modern", "--color", "blue"])
            produced = chdir / f"{base}.html"
            if not produced.exists():
                print(f"! 未生成 {base}.html")
                failed.append(base)
                continue
            out = html_dir / f"{base}.html"
            shutil.move(str(produced), out)
            run(["bun", str(ROOT / "scripts/fix-placeholders.mjs"), md, str(out)])
            run(["bun", str(ROOT / "scripts/fix-data-local-path.mjs"), str(out)])
            run(["bun", str(ROOT / "scripts/patch-html-svg-to-png.mjs"), str(out)])
            run(["bun", str(ROOT / "scripts/post-process.mjs"), str(out)])
            print(f"  ✓ {out.name}")
    finally:
        restore()

    print(f"=== Ch{num} 正文构建完成: {html_dir} ===")
    if failed:
        print(f"!! 失败文件: {failed}")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
