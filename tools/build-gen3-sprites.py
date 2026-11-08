#!/usr/bin/env python3
"""Build the Gen-3 sprite banks (phase 1).

Fronts + backs + shinies for the two cartridge pairs, straight from the
PokeAPI sprites repo (era-authentic 64x64 Game Boy Advance sprites):

  gen3-rs{,-shiny,-back,-back-shiny}     <- versions/generation-iii/ruby-sapphire
  gen3-frlg{,-shiny,-back,-back-shiny}   <- versions/generation-iii/firered-leafgreen

  * Deoxys formes ride the cartridge in Gen 3 (R/S=Normal, FR=Attack,
    LG=Defense, E=Speed): the forme sprites are stored under their PokeAPI
    form ids (10013 attack / 10014 defense / 10015 speed) in the FR bank
    (normal+attack+defense) and RS bank (speed, used by the EMERALD chip).

  gen3-emerald                            <- stills cut from the existing
    emerald-atlas.png (64x64 cells, COLS=20, id-ordered — the same art the
    approved emerald page uses); #386 overridden with the Speed forme.

All outputs are re-encoded onto a uniform 64x64 RGBA canvas.
Usage: python3 tools/build-gen3-sprites.py [--skip-net]
"""
import argparse, io, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SPR = f'{REPO}/assets/sprites'
IMG = f'{REPO}/assets/img'
BASE = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii'
TOKEN_PATH = '/home/z/my-project/.secrets/github_token'

def fetch(path, retries=4):
    hdrs = {'User-Agent': 'pokedex-tools'}
    try:
        with open(TOKEN_PATH) as f:
            hdrs['Authorization'] = f'token {f.read().strip()}'
    except OSError:
        pass
    last = None
    for _ in range(retries):
        try:
            req = urllib.request.Request(f'{BASE}/{path}', headers=hdrs)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(0.8)
    raise RuntimeError(f'fetch failed: {path}: {last}')

def save64(data, out):
    im = Image.open(io.BytesIO(data)).convert('RGBA')
    if im.size != (64, 64):
        canvas = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        canvas.paste(im, ((64 - im.width) // 2, (64 - im.height) // 2), im)
        im = canvas
    im.save(out)

def bank(kind, sub, out, ids):
    os.makedirs(out, exist_ok=True)
    jobs = []
    for i in ids:
        dst = f'{out}/{i}.png'
        if os.path.exists(dst) and os.path.getsize(dst) > 0:
            continue
        path = f'{kind}/{sub}/{i}.png' if sub else f'{kind}/{i}.png'
        jobs.append((path, dst))
    def work(job):
        path, dst = job
        save64(fetch(path), dst)
        return dst
    done = 0
    with ThreadPoolExecutor(max_workers=10) as ex:
        for _ in as_completed([ex.submit(work, j) for j in jobs]):
            done += 1
            if done % 250 == 0:
                print(f'  {out.split("/")[-1]}: {done}/{len(jobs)}')
    print(f'{os.path.basename(out)}: {len(jobs)} fetched ({len(ids)} ids)')

def emerald_stills():
    """Cut 64x64 stills from the emerald atlas (the approved emerald-page art).
    Atlas layout (from emerald.js spriteCell): rows 0-19 normal, rows 20-39
    shiny — the shiny stills ride along so the EMERALD chip keeps its
    shiny switch, exactly like the legacy page."""
    out = f'{SPR}/gen3-emerald'
    out_s = f'{SPR}/gen3-emerald-shiny'
    os.makedirs(out, exist_ok=True)
    os.makedirs(out_s, exist_ok=True)
    atlas = Image.open(f'{IMG}/emerald-atlas.png').convert('RGBA')
    CELL, COLS = 64, 20
    made = 0
    for i in range(1, 387):
        idx = i - 1
        col = idx % COLS
        row = idx // COLS
        dst = f'{out}/{i}.png'
        if not os.path.exists(dst):
            atlas.crop((col * CELL, row * CELL, col * CELL + CELL, row * CELL + CELL)).save(dst)
            made += 1
        dst_s = f'{out_s}/{i}.png'
        if not os.path.exists(dst_s):
            atlas.crop((col * CELL, (row + 20) * CELL, col * CELL + CELL, (row + 20) * CELL + CELL)).save(dst_s)
            made += 1
    print(f'gen3-emerald(-shiny): {made} stills cut from atlas')
    # Deoxys: the atlas stills are the Normal forme; Emerald's dex shows the
    # SPEED forme — store the era 64x64 speed sprites under 386.png.
    save64(fetch('ruby-sapphire/10015.png'), f'{out}/386.png')
    save64(fetch('ruby-sapphire/back/shiny/10015.png'), f'{out_s}/386.png')
    print('gen3-emerald/386.png = Deoxys Speed forme (era-authentic)')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skip-net', action='store_true', help='emerald stills only')
    args = ap.parse_args()
    ids = list(range(1, 387))
    # Deoxys forme sprites: attack 10013 + defense 10014 live in the FR bank
    # (LEAFGREEN pairs its own bank with the defense forme), speed 10015 in RS.
    fr_ids = ids + [10013, 10014]
    rs_ids = ids + [10015]
    plan = [
        ('ruby-sapphire', '', f'{SPR}/gen3-rs', rs_ids),
        ('ruby-sapphire', 'shiny', f'{SPR}/gen3-rs-shiny', rs_ids),
        ('ruby-sapphire', 'back', f'{SPR}/gen3-rs-back', rs_ids),
        ('ruby-sapphire', 'back/shiny', f'{SPR}/gen3-rs-back-shiny', rs_ids),
        ('firered-leafgreen', '', f'{SPR}/gen3-frlg', fr_ids),
        ('firered-leafgreen', 'shiny', f'{SPR}/gen3-frlg-shiny', fr_ids),
        ('firered-leafgreen', 'back', f'{SPR}/gen3-frlg-back', fr_ids),
        ('firered-leafgreen', 'back/shiny', f'{SPR}/gen3-frlg-back-shiny', fr_ids),
    ]
    if not args.skip_net:
        jobs = []
        for kind, sub, out, bank_ids in plan:
            os.makedirs(out, exist_ok=True)
            for i in bank_ids:
                dst = f'{out}/{i}.png'
                if os.path.exists(dst) and os.path.getsize(dst) > 0:
                    continue
                path = f'{kind}/{sub}/{i}.png' if sub else f'{kind}/{i}.png'
                jobs.append((path, dst))
        print(f'fetching {len(jobs)} sprites with 16 workers...')
        with ThreadPoolExecutor(max_workers=16) as ex:
            futs = [ex.submit(lambda j: save64(fetch(j[0]), j[1]), j) for j in jobs]
            for n, f in enumerate(as_completed(futs), 1):
                f.result()
                if n % 500 == 0:
                    print(f'  {n}/{len(jobs)}')
        print(f'sprites fetched: {len(jobs)}')
    emerald_stills()
    print('gen3 sprite banks complete')

if __name__ == '__main__':
    main()
