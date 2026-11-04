#!/usr/bin/env python3
"""Build every Gen-1/Gen-2 *back* sprite folder + the Japan Green set for this repo.

Self-contained: downloads straight from the PokeAPI/sprites GitHub repo and
reproduces, pixel-exactly, the conventions already used by assets/sprites/:
  - gen-1 sprites: border-flood the white background, keep interior white
  - mono sets: recolor the 4-shade gray ramp onto the DMG / Pocket palettes
  - gen-2 sprites: same border-flood (raw backs ship with a white background)
  - transparent pixels are stored as (0,0,0,0); back sprites are padded onto a
    40x40 canvas (Gen-1) so they keep the same pixel density as the fronts

Outputs (assets/sprites/):
  gen1-rb-color-back  gen1-rb-dmg-back  gen1-rb-pocket-back
  gen1-yellow-back    gen1-y-dmg-back   gen1-y-pocket-back
  gen1-green-dmg      gen1-green-pocket gen1-green-dmg-back  gen1-green-pocket-back
  gen2-gold-back      gen2-gold-back-shiny
  gen2-silver-back    gen2-silver-back-shiny
  gen2-crystal-back   gen2-crystal-back-shiny

Usage:
  python3 tools/build-sprites.py                 # build everything (skips existing)
  python3 tools/build-sprites.py --ids 25        # smoke-test one pokemon
  python3 tools/build-sprites.py --refresh       # rebuild all outputs
"""
import argparse
import io
import os
import sys
import urllib.request
from collections import Counter, deque
from concurrent.futures import ThreadPoolExecutor, as_completed

from PIL import Image

BASE = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions'
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

RAMP_DMG = [(255, 255, 255), (139, 172, 15), (48, 98, 48), (15, 56, 15)]
RAMP_POCKET = [(255, 255, 255), (168, 168, 146), (85, 85, 74), (28, 28, 22)]
GRAY_KEYS = [(255, 255, 255), (170, 170, 170), (85, 85, 85), (0, 0, 0)]


def fetch(path, retries=3):
    last = None
    for _ in range(retries):
        try:
            req = urllib.request.Request(f'{BASE}/{path}', headers={'User-Agent': 'pokedex-tools'})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
    raise RuntimeError(f'fetch failed: {path}: {last}')


def load(path):
    return Image.open(io.BytesIO(fetch(path))).convert('RGBA')


def flood(im):
    """Border-connected pure-white pixels -> fully-transparent black."""
    px = im.load()
    w, h = im.size
    seen = [[False] * w for _ in range(h)]
    q = deque()
    for x in range(w):
        q.append((x, 0))
        q.append((x, h - 1))
    for y in range(h):
        q.append((0, y))
        q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h or seen[y][x]:
            continue
        seen[y][x] = True
        r, g, b, a = px[x, y]
        if a == 0:
            pass
        elif (r, g, b) == (255, 255, 255):
            px[x, y] = (0, 0, 0, 0)
        else:
            continue
        q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return im


def normalize_alpha(im):
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0 and (r, g, b) != (0, 0, 0):
                px[x, y] = (0, 0, 0, 0)
    return im


def recolor_gray(im, ramp):
    im = im.copy()
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            v = (r + g + b) / 3
            best, bi = None, 0
            for i, (kr, kg, kb) in enumerate(GRAY_KEYS):
                d = abs(v - (kr + kg + kb) / 3)
                if best is None or d < best:
                    best, bi = d, i
            px[x, y] = (*ramp[bi], a)
    return im


def pad_to(im, size):
    w, h = im.size
    if w >= size or h >= size:
        return im
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.paste(im, ((size - w) // 2, size - h))
    return out


def build_gen1(pid, refresh):
    outs = {
        'gen1-rb-color-back': None, 'gen1-rb-dmg-back': None, 'gen1-rb-pocket-back': None,
        'gen1-yellow-back': None, 'gen1-y-dmg-back': None, 'gen1-y-pocket-back': None,
        'gen1-green-dmg': None, 'gen1-green-pocket': None,
        'gen1-green-dmg-back': None, 'gen1-green-pocket-back': None,
    }
    outdir = f'{REPO}/assets/sprites'
    if not refresh and all(os.path.exists(f'{outdir}/{d}/{pid}.png') for d in outs):
        return 'skip'
    rb_back_color = flood(load(f'generation-i/red-blue/back/{pid}.png'))
    rb_back_gray = flood(load(f'generation-i/red-blue/back/gray/{pid}.png'))
    y_back_color = flood(load(f'generation-i/yellow/back/{pid}.png'))
    y_back_gray = flood(load(f'generation-i/yellow/back/gray/{pid}.png'))
    gf = flood(load(f'generation-i/red-green-japan/gray/{pid}.png'))
    gb = flood(load(f'generation-i/red-green-japan/back/gray/{pid}.png'))
    outs['gen1-rb-color-back'] = pad_to(normalize_alpha(rb_back_color), 40)
    outs['gen1-rb-dmg-back'] = pad_to(normalize_alpha(recolor_gray(rb_back_gray, RAMP_DMG)), 40)
    outs['gen1-rb-pocket-back'] = pad_to(normalize_alpha(recolor_gray(rb_back_gray, RAMP_POCKET)), 40)
    outs['gen1-yellow-back'] = pad_to(normalize_alpha(y_back_color), 40)
    outs['gen1-y-dmg-back'] = pad_to(normalize_alpha(recolor_gray(y_back_gray, RAMP_DMG)), 40)
    outs['gen1-y-pocket-back'] = pad_to(normalize_alpha(recolor_gray(y_back_gray, RAMP_POCKET)), 40)
    outs['gen1-green-dmg'] = normalize_alpha(recolor_gray(gf, RAMP_DMG))
    outs['gen1-green-pocket'] = normalize_alpha(recolor_gray(gf, RAMP_POCKET))
    outs['gen1-green-dmg-back'] = normalize_alpha(recolor_gray(gb, RAMP_DMG))
    outs['gen1-green-pocket-back'] = normalize_alpha(recolor_gray(gb, RAMP_POCKET))
    for d, im in outs.items():
        os.makedirs(f'{outdir}/{d}', exist_ok=True)
        im.save(f'{outdir}/{d}/{pid}.png', optimize=True)
    return 'ok'


def build_gen2(pid, refresh):
    dirs = ['gen2-gold-back', 'gen2-gold-back-shiny', 'gen2-silver-back', 'gen2-silver-back-shiny',
            'gen2-crystal-back', 'gen2-crystal-back-shiny']
    outdir = f'{REPO}/assets/sprites'
    if not refresh and all(os.path.exists(f'{outdir}/{d}/{pid}.png') for d in dirs):
        return 'skip'
    srcs = {
        'gen2-gold-back': f'generation-ii/gold/back/{pid}.png',
        'gen2-gold-back-shiny': f'generation-ii/gold/back/shiny/{pid}.png',
        'gen2-silver-back': f'generation-ii/silver/back/{pid}.png',
        'gen2-silver-back-shiny': f'generation-ii/silver/back/shiny/{pid}.png',
        'gen2-crystal-back': f'generation-ii/crystal/back/{pid}.png',
        'gen2-crystal-back-shiny': f'generation-ii/crystal/back/shiny/{pid}.png',
    }
    for d, path in srcs.items():
        im = normalize_alpha(flood(load(path)))
        os.makedirs(f'{outdir}/{d}', exist_ok=True)
        im.save(f'{outdir}/{d}/{pid}.png', optimize=True)
    return 'ok'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ids', help='pokemon id or range, e.g. 25 or 1-151 (default: all needed)')
    ap.add_argument('--refresh', action='store_true', help='rebuild even if outputs exist')
    ap.add_argument('--workers', type=int, default=8)
    args = ap.parse_args()

    if args.ids:
        if '-' in args.ids:
            a, b = args.ids.split('-')
            ids = list(range(int(a), int(b) + 1))
        else:
            ids = [int(args.ids)]
    else:
        ids = list(range(1, 252))

    jobs = [('g1', i) for i in ids if i <= 151] + [('g2', i) for i in ids if i > 151]
    stats = Counter()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(build_gen1 if k == 'g1' else build_gen2, i, args.refresh): i for k, i in jobs}
        for n, f in enumerate(as_completed(futs), 1):
            stats[f.result()] += 1
            if n % 50 == 0:
                print(f'  {n}/{len(jobs)} done')
    print(f'done: {dict(stats)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
