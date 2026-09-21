#!/usr/bin/env python3
"""Downscale formula PNGs for tables. Called by v24 render script.

We resize matrix/array PNGs (identified by hash list or filename pattern) so
they fit cleanly inside a 45mm table cell when the PDF prints at 150dpi.
"""
import sys
import os
import json
import subprocess
from PIL import Image

if __name__ == '__main__':
    # Args: png_path [target_width]
    if len(sys.argv) < 2:
        sys.exit(1)
    png_path = sys.argv[1]
    target_w = int(sys.argv[2]) if len(sys.argv) > 2 else 600
    if not os.path.exists(png_path):
        sys.exit(0)
    img = Image.open(png_path)
    if img.width <= target_w:
        sys.exit(0)
    new_h = round(img.height * target_w / img.width)
    img2 = img.resize((target_w, new_h), Image.LANCZOS)
    img2.save(png_path, optimize=True)
    print(f'resized {png_path}: {img.size} -> {img2.size}', file=sys.stderr)