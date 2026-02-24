#!/usr/bin/env python3
"""
Generate favicon and related icon files from the kangaroo logo.

Creates:
- static/favicons/favicon-32x32.png
- static/favicons/favicon-16x16.png
- static/favicons/apple-touch-icon.png
- static/favicons/favicon.ico

Run inside the app container (recommended) so Pillow is available:
  docker compose exec server python3 scripts/generate_favicons.py

Or locally if your venv has Pillow installed.
"""
import os
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'static', 'images', 'ui', 'kangaroo-logo.png')
OUT_DIR = os.path.join(ROOT, 'static', 'favicons')

os.makedirs(OUT_DIR, exist_ok=True)

def make_png(size, out_name):
    with Image.open(SRC) as im:
        im = im.convert('RGBA')
        im.thumbnail((size, size), Image.LANCZOS)
        # create square canvas
        canvas = Image.new('RGBA', (size, size), (0,0,0,0))
        w, h = im.size
        canvas.paste(im, ((size-w)//2, (size-h)//2), im)
        canvas.save(os.path.join(OUT_DIR, out_name), format='PNG')

def make_ico(sizes, out_name='favicon.ico'):
    imgs = []
    with Image.open(SRC) as im0:
        for s in sizes:
            im = im0.convert('RGBA')
            im.thumbnail((s, s), Image.LANCZOS)
            canvas = Image.new('RGBA', (s, s), (0,0,0,0))
            w,h = im.size
            canvas.paste(im, ((s-w)//2, (s-h)//2), im)
            imgs.append(canvas)
        imgs[0].save(os.path.join(OUT_DIR, out_name), format='ICO', sizes=[(s,s) for s in sizes])

if not os.path.exists(SRC):
    print('Source logo not found at', SRC)
    raise SystemExit(1)

print('Generating PNG icons...')
make_png(32, 'favicon-32x32.png')
make_png(16, 'favicon-16x16.png')
make_png(180, 'apple-touch-icon.png')
print('Generating ICO...')
make_ico([16,32,48,64,128,256])
print('Favicons generated in', OUT_DIR)
