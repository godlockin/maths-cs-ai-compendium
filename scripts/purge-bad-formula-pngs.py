#!/usr/bin/env python3
"""Delete MathJax error PNGs (red text on yellow background) from the formula pool.

MathJax renders parse errors as red text on a yellow highlight. Any cached PNG
from a failed inline-mode render stays in the pool forever (existsSync skips
re-render), so we detect them by dominant color and delete.
"""
import os
import sys
from PIL import Image

DIR = sys.argv[1] if len(sys.argv) > 1 else 'zh/images/formulas'

deleted = 0
scanned = 0
for f in sorted(os.listdir(DIR)):
    if not f.endswith('.png'):
        continue
    path = os.path.join(DIR, f)
    scanned += 1
    try:
        img = Image.open(path).convert('RGB')
    except Exception:
        continue
    # Downsample for speed
    img2 = img.resize((min(img.width, 80), min(img.height, 40)))
    px = list(img2.getdata())
    if not px:
        continue
    # MathJax error highlight: pure yellow (255,255,0)-ish
    yellow = sum(1 for r, g, b in px if r > 200 and g > 200 and b < 100)
    # Error text: saturated red
    red = sum(1 for r, g, b in px if r > 150 and g < 80 and b < 80)
    frac_yellow = yellow / len(px)
    frac_red = red / len(px)
    if frac_yellow > 0.2 or frac_red > 0.1:
        os.remove(path)
        deleted += 1
        print(f'deleted {f}: yellow={frac_yellow:.2f} red={frac_red:.2f}')

print(f'\nscanned={scanned} deleted={deleted}')