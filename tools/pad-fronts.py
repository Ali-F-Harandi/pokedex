#!/usr/bin/env python3
"""Normalize sprite canvases so every set scales like the Japan Green set.

Problem (reported Phase 2.5): the Green set ships on the *native* 56x56
(7x7-tile) canvas, so every Pokemon keeps its true relative size and the
whole set renders at one uniform scale. The other sets came from PokeAPI
*cropped to size classes* (40 / 48 / 56): the CSS `object-fit:contain`
then zooms each canvas to fill the 132px box, so a Caterpie is stretched
almost as large as a Gyarados — a "zoom to fit" that the real games never
do. (The Crystal animated set is already native 56x56, which is why it
never had the problem.)

Fix, matching how the games themselves render:

  gen-1/2 FRONTS  rb, rb-color, pocket, yellow (+ gen-2 gold/silver/
                  crystal fronts & shinies): pad the 40/48 canvases onto
                  a uniform 56x56 canvas, bottom-centered — exactly the
                  green convention (art bottom-aligned, horizontally
                  centered). 56x56 files are left untouched.
  gen-1 BACKS     the international games store back sprites at HALF
                  resolution and render them at 2x (PokeAPI's official
                  transparent backs are 96x96 "art at 2x"). The Japan
                  Green backs are stored at full 56x56 — and indeed
                  green-back #1 is 56x38 where the rb native art is
                  28x19: exactly 2x. So: crop the art, upscale 2x with
                  NEAREST (the authentic chunky look), clamp to <=56,
                  bottom-center on 56x56. After this, rb/yellow backs
                  match the green backs pixel-for-pixel in scale.
  gen-2 BACKS     already uniform 48x48 at 1:1 (authentic — the official
                  transparent gen-2 backs carry the art at 1:1): untouched.
  gen-3 emerald   animated .webp on variable 64..96 canvases; the union of
                  every frame's art reaches 96x96 (Emerald's animation
                  envelope), so --emerald re-anchors all frames onto a
                  uniform 96x96 canvas, bottom-centered on the union box.

Idempotent: files already on the target canvas are skipped, so the script
can be re-run safely. tools/build-sprites.py keeps parity for fresh
rebuilds from source.

Usage:
  python3 tools/pad-fronts.py            # gen-1/2 PNG sets
  python3 tools/pad-fronts.py --emerald  # also re-pad emerald anims
  python3 tools/pad-fronts.py --dry
"""
import argparse
import os
import sys

from PIL import Image

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SPR = f'{REPO}/assets/sprites'

FRONT_56 = [  # gen-1 fronts (rb + yellow families) + gen-2 fronts & shinies
    'gen1-rb-dmg', 'gen1-rb-pocket', 'gen1-rb-color',
    'gen1-y-dmg', 'gen1-y-pocket', 'gen1-yellow',
    'gen2-gold', 'gen2-gold-shiny', 'gen2-silver', 'gen2-silver-shiny',
    'gen2-crystal', 'gen2-crystal-shiny',
]
BACK_2X = [  # gen-1 international backs: native art -> 2x on 56x56
    'gen1-rb-dmg-back', 'gen1-rb-pocket-back', 'gen1-rb-color-back',
    'gen1-y-dmg-back', 'gen1-y-pocket-back', 'gen1-yellow-back',
]


def pad_onto(im, size):
    """Bottom-center `im` on a transparent `size`x`size` canvas."""
    w, h = im.size
    if (w, h) == (size, size):
        return im
    if w > size or h > size:  # shouldn't happen; guard anyway
        return im
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.paste(im, ((size - w) // 2, size - h))
    return out


def upscale_2x_bottom(im, size):
    """Crop to content, double with NEAREST, clamp to `size`, bottom-center."""
    bb = im.getbbox()
    if bb is None:
        return im
    art = im.crop(bb)
    w, h = art.size
    w2, h2 = w * 2, h * 2
    if w2 > size or h2 > size:  # a 29px native art doubles to 58: clamp ~3%
        r = min(size / w2, size / h2)
        w2, h2 = max(1, round(w2 * r)), max(1, round(h2 * r))
    art = art.resize((w2, h2), Image.NEAREST)
    return pad_onto(art, size)


def process_png_folder(folder, mode, dry):
    d = f'{SPR}/{folder}'
    if not os.path.isdir(d):
        print(f'  ! missing folder {folder}')
        return 0, 0
    changed = skipped = 0
    for f in sorted(os.listdir(d)):
        if not f.endswith('.png'):
            continue
        p = os.path.join(d, f)
        im = Image.open(p).convert('RGBA')
        if im.size == (56, 56):  # already normalized
            skipped += 1
            continue
        if dry:
            changed += 1
            continue
        out = upscale_2x_bottom(im, 56) if mode == '2x' else pad_onto(im, 56)
        out.save(p, optimize=True)
        changed += 1
    return changed, skipped


def process_emerald(dry):
    """Re-anchor every frame of the animated emerald .webp onto 96x96.

    The art moves between frames, so the anchor is the UNION bbox of all
    frames; every frame is pasted at the offset that bottom-centers that
    union box, keeping the animation's internal motion intact.
    """
    d = f'{SPR}/gen3-emerald-anim'
    changed = skipped = 0
    for f in sorted(os.listdir(d)):
        if not f.endswith('.webp'):
            continue
        p = os.path.join(d, f)
        im = Image.open(p)
        if im.size == (96, 96):
            skipped += 1
            continue
        frames, durations, u = [], [], None
        for i in range(getattr(im, 'n_frames', 1)):
            im.seek(i)
            fr = im.convert('RGBA')
            bb = fr.getbbox()
            if bb:
                u = (min(u[0], bb[0]), min(u[1], bb[1]), max(u[2], bb[2]), max(u[3], bb[3])) if u else bb
            frames.append(fr)
            durations.append(im.info.get('duration', 80))
        if u is None:
            skipped += 1
            continue
        uw, uh = u[2] - u[0], u[3] - u[1]
        # union box top-left lands at ((96-uw)//2, 96-uh):
        dx, dy = (96 - uw) // 2, 96 - uh
        out_frames = []
        for fr in frames:
            canvas = Image.new('RGBA', (96, 96), (0, 0, 0, 0))
            canvas.paste(fr, (dx - u[0], dy - u[1]))
            out_frames.append(canvas)
        if dry:
            changed += 1
            continue
        out_frames[0].save(p, save_all=True, append_images=out_frames[1:],
                           duration=durations, loop=im.info.get('loop', 0),
                           method=4, lossless=True)
        changed += 1
    return changed, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--emerald', action='store_true', help='also pad gen-3 emerald anims to 64x64')
    a = ap.parse_args()

    for folder in FRONT_56:
        c, s = process_png_folder(folder, 'pad', a.dry)
        print(f'{folder:24s} padded={c:3d} already-56={s:3d}' + (' (dry)' if a.dry else ''))
    for folder in BACK_2X:
        c, s = process_png_folder(folder, '2x', a.dry)
        print(f'{folder:24s} 2x-padded={c:3d} already-56={s:3d}' + (' (dry)' if a.dry else ''))
    if a.emerald:
        c, s = process_emerald(a.dry)
        print(f'{"gen3-emerald-anim":24s} padded={c:3d} already-64={s:3d}' + (' (dry)' if a.dry else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
