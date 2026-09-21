#!/usr/bin/env python3
"""Stamp "Steven Chen" watermark on every page of the listed PDFs.

Uses qpdf --underlay (qpdf was installed via `brew install qpdf`). qpdf
streams the overlay without re-encoding, so it stays fast and produces
output of nearly identical size to the input.
"""
import os
import io
import subprocess
import sys
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

PDFS = [
    ('pdfs/EN-Maths-CS-AI-Compendium.pdf',  'EN-Maths-CS-AI-Compendium'),
    ('pdfs/ZH-教辅资料.pdf',                'ZH-教辅资料'),
    ('pdfs/ZH-Maths-CS-AI-Compendium.pdf',  'ZH-Maths-CS-AI-Compendium'),
]

TEXT = 'Steven Chen'
ROT = -30
FONT = 'Helvetica'    # PDF base-14 → no font subset embedded
SIZE_RATIO = 0.10
COLOR = Color(0.78, 0.78, 0.78, alpha=0.40)


def build_watermark(w, h, out_path):
    c = canvas.Canvas(out_path, pagesize=(w, h))
    c.saveState()
    c.translate(w / 2, h / 2)
    c.rotate(ROT)
    c.setFont(FONT, max(w, h) * SIZE_RATIO)
    c.setFillColor(COLOR)
    c.drawCentredString(0, 0, TEXT)
    c.restoreState()
    c.showPage()
    c.save()


def page_size(pdf_path):
    """Return (max_w, max_h) across all pages — watermark must cover the biggest."""
    info = subprocess.check_output(['pdfinfo', pdf_path], text=True)
    w, h = None, None
    for line in info.splitlines():
        if 'Page size' in line:
            parts = line.split(':', 1)[1].strip().split(' x ')
            w = float(parts[0])
            h = float(parts[1].split()[0])
            break
    return (w or 595.276, h or 841.89)


def stamp(src, dst):
    w, h = page_size(src)
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as wmf:
        wm_path = wmf.name
    try:
        build_watermark(w, h, wm_path)
        # qpdf --underlay maps 1 overlay page → 1 input page by default,
        # which would only stamp the first page of a long book. Use
        # `--from=1 --to=1-z --repeat=1` to re-apply the single watermark
        # page to every input page (1-z = every page).
        subprocess.run(
            ['qpdf', '--underlay', wm_path,
             '--from=1', '--to=1-z', '--repeat=1',
             '--', src, dst],
            check=True, capture_output=True,
        )
    finally:
        os.remove(wm_path)
    print(f'stamped {src} -> {dst} ({os.path.getsize(dst) // 1024} KiB)')


def main():
    for src, stem in PDFS:
        if not os.path.exists(src):
            print(f'skip (missing): {src}')
            continue
        dst = f'pdfs/{stem}-watermarked.pdf'
        if os.path.exists(dst) and os.path.getsize(dst) == 0:
            os.remove(dst)
        stamp(src, dst)


if __name__ == '__main__':
    main()