#!/usr/bin/env python3
"""Build every Gen-1/Gen-2 *back* sprite folder, the Japan Green set and
front-sprite repairs for this repo — using PokeAPI's ORIGINAL transparent
sprites as the source of truth.

Why: the previous border-flood pipeline destroyed sprites whose white body
touches the background (every Gen-1 back sprite was hollowed out — e.g.
Pikachu's back lost ~65% of its body). PokeAPI ships official *transparent*
variants whose cut-out is authoritative, so we no longer invent our own:

  gen-1 rb/yellow BACKS : native 32x32 white-bg source (colors + geometry)
                          + alpha mask from the official `transparent/back`
                          sprite (96x96, art at 2x -> downscaled 2:1 with BOX).
                          The mask is aligned onto the native sprite by a
                          dark-pixel bbox search (+-2 px, scored); dark pixels
                          are never dropped (safety net). Art is then doubled
                          with NEAREST (the games render backs at 2x) and
                          bottom-centered on the native 56x56 canvas — the
                          same scale as the Japan Green backs.
  gen-1 GREEN (4 sets)  : the red-green-japan sources are already transparent
                          and already on the full 56x56 tile canvas
                          -> used as-is, only recolored onto the DMG / Pocket
                          ramps. Zero transparency processing.
  gen-2 BACKS (+shiny)  : native 48x48 white-bg source + mask from the
                          official `transparent/back` sprite (art at 1:1).
  gen-1/2 FRONTS        : scanned against the official transparent sprites;
                          any pokemon that lost >2% of its body vs official
                          (flood damage: Blissey, Growlithe, Goldeen) is
                          rebuilt with the same mask-transfer method.
  mono sets             : the 4-shade gray ramp is recolored onto the
                          DMG / Pocket palettes (as before).

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
  python3 tools/build-sprites.py --skip-fronts   # backs + green only
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
SPR = f'{REPO}/assets/sprites'

RAMP_DMG = [(255, 255, 255), (139, 172, 15), (48, 98, 48), (15, 56, 15)]
RAMP_POCKET = [(255, 255, 255), (168, 168, 146), (85, 85, 74), (28, 28, 22)]
GRAY_KEYS = [(255, 255, 255), (170, 170, 170), (85, 85, 85), (0, 0, 0)]
WHITE = (255, 255, 255)


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


# ---------------------------------------------------------------- helpers
def bbox(im, dark=False):
    px = im.load()
    w, h = im.size
    xs, ys = [], []
    lmode = im.mode == 'L'
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            if lmode:
                hit = p > 0
            else:
                hit = p[3] > 0 if not dark else (p[3] > 0 and p[:3] != WHITE)
            if hit:
                xs.append(x)
                ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


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


def normalize_alpha(im):
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0 and (r, g, b) != (0, 0, 0):
                px[x, y] = (0, 0, 0, 0)
    return im


def pad_to(im, size):
    w, h = im.size
    if w > size or h > size:
        return im
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.paste(im, ((size - w) // 2, size - h))
    return out


def back_to_56(im):
    """Gen-1 back: games render the half-res art at 2x — crop, double
    (NEAREST, the authentic chunky look), clamp, bottom-center on 56x56.
    Matches the Japan Green back canvases 1:1 in scale."""
    bb = im.getbbox()
    if bb is None:
        return pad_to(im, 56)
    art = im.crop(bb)
    w, h = art.size
    w2, h2 = w * 2, h * 2
    if w2 > 56 or h2 > 56:
        r = min(56 / w2, 56 / h2)
        w2, h2 = max(1, round(w2 * r)), max(1, round(h2 * r))
    return pad_to(art.resize((w2, h2), Image.NEAREST), 56)


def save(im, d, pid):
    os.makedirs(f'{SPR}/{d}', exist_ok=True)
    im.save(f'{SPR}/{d}/{pid}.png', optimize=True)


# ---------------------------------------------------------------- mask transfer
def apply_official_mask(N, T, scale_down):
    """Transfer the official transparent cut-out onto native source N."""
    bt = bbox(T)
    if bt is None:
        return None
    art = T.crop(bt)
    if scale_down:  # gen-1 backs: official art is 2x native
        art = art.resize((round(art.size[0] / 2), round(art.size[1] / 2)), Image.BOX)
    mask = art.getchannel('A').point(lambda v: 255 if v >= 128 else 0)
    mw, mh = mask.size
    nw, nh = N.size
    npx, mpx = N.load(), mask.load()

    dbn = bbox(N, dark=True)
    dbm = bbox(mask)  # mask is L-mode: any value > 0 is body
    if dbn is None or dbm is None:
        return None
    base = (dbn[0] - dbm[0], dbn[1] - dbm[1])

    def score(ox, oy):
        s = 0
        for y in range(mh):
            ny = oy + y
            for x in range(mw):
                nx = ox + x
                m = mpx[x, y] > 0
                if nx < 0 or ny < 0 or nx >= nw or ny >= nh:
                    s -= 2 if m else 0
                    continue
                ndark = npx[nx, ny][:3] != WHITE
                if m and ndark:
                    s += 3
                elif not m and ndark:
                    s -= 6
                elif not m:
                    s += 1
        return s

    best = None
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            ox, oy = base[0] + dx, base[1] + dy
            if ox < -2 or oy < -2 or ox + mw > nw + 2 or oy + mh > nh + 2:
                continue
            sc = score(ox, oy)
            if best is None or sc > best[0]:
                best = (sc, ox, oy)
    _, ox, oy = best

    out = Image.new('RGBA', N.size, (0, 0, 0, 0))
    opx = out.load()
    for y in range(nh):
        for x in range(nw):
            n = npx[x, y]
            mx, my = x - ox, y - oy
            m = 0 <= mx < mw and 0 <= my < mh and mpx[mx, my] > 0
            if m or n[:3] != WHITE:  # mask says body, or dark pixel (safety net)
                opx[x, y] = (*n[:3], 255)
    return out


# ---------------------------------------------------------------- builders
def build_gen1(pid, refresh=False):
    outs = {
        'gen1-rb-color-back': (f'generation-i/red-blue/back/{pid}.png',
                               f'generation-i/red-blue/transparent/back/{pid}.png', None),
        'gen1-rb-dmg-back': (f'generation-i/red-blue/back/gray/{pid}.png',
                             f'generation-i/red-blue/transparent/back/gray/{pid}.png', 'dmg'),
        'gen1-rb-pocket-back': (f'generation-i/red-blue/back/gray/{pid}.png',
                                f'generation-i/red-blue/transparent/back/gray/{pid}.png', 'pocket'),
        'gen1-yellow-back': (f'generation-i/yellow/back/{pid}.png',
                             f'generation-i/yellow/transparent/back/{pid}.png', None),
        'gen1-y-dmg-back': (f'generation-i/yellow/back/gray/{pid}.png',
                            f'generation-i/yellow/transparent/back/gray/{pid}.png', 'dmg'),
        'gen1-y-pocket-back': (f'generation-i/yellow/back/gray/{pid}.png',
                               f'generation-i/yellow/transparent/back/gray/{pid}.png', 'pocket'),
        'gen1-green-dmg': (f'generation-i/red-green-japan/gray/{pid}.png', None, 'dmg'),
        'gen1-green-pocket': (f'generation-i/red-green-japan/gray/{pid}.png', None, 'pocket'),
        'gen1-green-dmg-back': (f'generation-i/red-green-japan/back/gray/{pid}.png', None, 'dmg'),
        'gen1-green-pocket-back': (f'generation-i/red-green-japan/back/gray/{pid}.png', None, 'pocket'),
    }
    if not refresh and all(os.path.exists(f'{SPR}/{d}/{pid}.png') for d in outs):
        return 'skip'
    for d, (npath, tpath, ramp) in outs.items():
        N = load(npath)                     # green sources are already transparent
        im = apply_official_mask(N, load(tpath), True) if tpath else N.copy()
        if ramp == 'dmg':
            im = recolor_gray(im, RAMP_DMG)
        elif ramp == 'pocket':
            im = recolor_gray(im, RAMP_POCKET)
        # green sets ship native (fronts AND backs already on the full
        # 56x56 tile canvas) — international backs carry half-res art
        # that the games render at 2x.
        if d.startswith('gen1-green'):
            out = pad_to(normalize_alpha(im), 56)
        elif d.endswith('-back'):
            out = back_to_56(normalize_alpha(im))
        else:
            out = pad_to(normalize_alpha(im), 56)
        save(out, d, pid)
    return 'ok'


def build_gen2(pid, refresh=False):
    dirs = ['gen2-gold-back', 'gen2-gold-back-shiny', 'gen2-silver-back', 'gen2-silver-back-shiny',
            'gen2-crystal-back', 'gen2-crystal-back-shiny']
    if not refresh and all(os.path.exists(f'{SPR}/{d}/{pid}.png') for d in dirs):
        return 'skip'
    for d in dirs:
        ver = d.split('-')[1]
        sfx = 'shiny/' if 'shiny' in d else ''
        N = load(f'generation-ii/{ver}/back/{sfx}{pid}.png')
        T = load(f'generation-ii/{ver}/transparent/back/{sfx}{pid}.png')
        im = apply_official_mask(N, T, False)
        save(normalize_alpha(im), d, pid)  # native 48x48 canvas, no padding
    return 'ok'


FRONT_SETS = {
    'gen2-gold': ('gold', ''), 'gen2-gold-shiny': ('gold', 'shiny/'),
    'gen2-silver': ('silver', ''), 'gen2-silver-shiny': ('silver', 'shiny/'),
    'gen2-crystal': ('crystal', ''), 'gen2-crystal-shiny': ('crystal', 'shiny/'),
}


def fix_front(pid):
    """Rebuild any front sprite that lost >2% of its body vs official."""
    fixed = []
    if pid <= 151:
        checks = {
            'gen1-rb-color': (f'generation-i/red-blue/{pid}.png', f'generation-i/red-blue/transparent/{pid}.png'),
            'gen1-rb-dmg': (f'generation-i/red-blue/gray/{pid}.png', f'generation-i/red-blue/transparent/gray/{pid}.png'),
            'gen1-yellow': (f'generation-i/yellow/{pid}.png', f'generation-i/yellow/transparent/{pid}.png'),
        }
    else:
        checks = {d: (f'generation-ii/{v}/{s}{pid}.png', f'generation-ii/{v}/transparent/{s}{pid}.png')
                  for d, (v, s) in FRONT_SETS.items()}
    for d, (npath, tpath) in checks.items():
        try:
            rep = Image.open(f'{SPR}/{d}/{pid}.png').convert('RGBA')
            off = load(tpath)
        except OSError:
            continue
        ro = sum(1 for p in rep.getdata() if p[3] == 255)
        oo = sum(1 for p in off.getdata() if p[3] == 255)
        if ro >= oo * 0.98 or oo == 0:
            continue
        im = apply_official_mask(load(npath), off, False)
        save(pad_to(normalize_alpha(im), 56), d, pid)  # uniform 56x56 canvas (green convention)
        fixed.append((d, ro, oo))
    return fixed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ids', help='pokemon id or range, e.g. 25 or 1-151 (default: all needed)')
    ap.add_argument('--refresh', action='store_true', help='rebuild even if outputs exist')
    ap.add_argument('--skip-fronts', action='store_true', help='do not scan/repair front sprites')
    ap.add_argument('--workers', type=int, default=8)
    args = ap.parse_args()

    if args.ids:
        if '-' in args.ids:
            a, b = args.ids.split('-')
            ids = list(range(int(a), int(b) + 1))
        else:
            ids = [int(x) for x in args.ids.split(',')]
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
    print(f'backs+green: {dict(stats)}')

    if not args.skip_fronts:
        repaired = []
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(fix_front, i): i for i in ids}
            for f in as_completed(futs):
                repaired.extend(f.result())
        print(f'fronts repaired (>2% body loss vs official): {len(repaired)}')
        for r in repaired:
            print('   ', r)
    return 0


if __name__ == '__main__':
    sys.exit(main())
