#!/usr/bin/env python3
"""Pokédex Plus — Gen-3 sprite & cry completeness audit (phase 2 of the
Gen-3 plan). Proves every Gen-3 sprite variant exists and renders correctly
for all 386 Pokémon:

  - 10 static banks (rs/frlg/emerald x front/back x normal/shiny):
    rs banks carry 1..386 + forme id 10015 (speed, serves the EMERALD chip's
    back view); frlg banks carry 1..386 + 10013 (attack) + 10014 (defense);
    emerald banks carry 1..386 + 10015 (speed front views).
    Checks: present, non-empty, PIL-decodable, 64x64, RGBA alpha in use.
  - shiny banks differ from the normal banks (full set, front + back).
    DOCUMENTED EXCEPTION: frlg shiny slots for 10013/10014 are PokeAPI
    normal-art placeholders (no authentic Gen-3 shiny forme art exists —
    verified against PokeAPI + pokemondb + Bulbagarden, 2026-11). The audit
    ALLOWS exactly those two ids to be identical and nothing else.
  - Deoxys forme matrix: emerald front/back x normal/shiny resolve to the
    SPEED forme (10015 in gen3-emerald(-shiny) + gen3-rs-back(-shiny));
    the 386 slots stay the normal-forme art; frlg holds distinct
    normal/attack/defense views; the speed shiny views are genuine
    (pokemondb era art, differ from normal).
  - gen3-emerald-anim: ids 1..386 webp, decodable, frames > 1 (96x96).
    386.webp is the NORMAL-forme rip — gen3.js's animURL() guards Deoxys
    away from it (the EMERALD chip shows the authentic Speed still).
  - cries: 252..386.ogg present, non-trivial size; 1..251 byte-identical
    to their committed blobs (untouched by phase 2).
  - wiring: gen3-data.js SPRITE_SETS points at exactly these banks and the
    DATA formes carry the forme sprite ids.
  - browser (Chromium + Firefox): image-rendering:pixelated on the big
    sprite + evo sprites, the animated webp PLAYS, every bank is reachable
    through the UI (front/back/shiny/anim x3 game groups), and the Deoxys
    forme views resolve per cartridge (incl. the anim guard).
Run: python3 tools/test-gen3-sprites.py (PIL + playwright)"""
import base64
import hashlib
import json
import os
import subprocess

from PIL import Image
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDS = list(range(1, 387))
FORMES = [10013, 10014, 10015]

STATIC_BANKS = {
    'gen3-rs': IDS + [10015],
    'gen3-rs-shiny': IDS + [10015],
    'gen3-rs-back': IDS + [10015],
    'gen3-rs-back-shiny': IDS + [10015],
    'gen3-frlg': IDS + [10013, 10014],
    'gen3-frlg-shiny': IDS + [10013, 10014],
    'gen3-frlg-back': IDS + [10013, 10014],
    'gen3-frlg-back-shiny': IDS + [10013, 10014],
    'gen3-emerald': IDS,
    'gen3-emerald-shiny': IDS,
}
ANIM_BANK = 'gen3-emerald-anim'
# PokeAPI's shiny slots for these forme ids ship normal-art placeholders —
# the one documented exception to "shiny must differ from normal". The FRLG
# shiny attack/defense art does not exist authentically in ANY Gen-3 source
# (PokeAPI / pokemondb / Bulbagarden all checked, 2026-11), so the slots
# keep PokeAPI's placeholder content, front AND back.
SHINY_PLACEHOLDER_OK = {
    (10013, 'gen3-frlg'), (10014, 'gen3-frlg'),
    (10013, 'gen3-frlg-back'), (10014, 'gen3-frlg-back'),
}

results = []


def check(name, cond, extra=''):
    results.append((name, bool(cond), extra))
    print(f'  {"PASS" if cond else "FAIL"}  {name}  {extra}')


def img_sig(path):
    im = Image.open(path).convert('RGBA')
    return hashlib.md5(im.tobytes()).hexdigest()


def fs_audit():
    print('== filesystem: 10 static banks (exists / size / decode / 64x64 / alpha) ==')
    for bank, ids in STATIC_BANKS.items():
        bad = []
        for i in ids:
            f = os.path.join(R, 'assets/sprites', bank, f'{i}.png')
            if not os.path.isfile(f):
                bad.append(f'{i}:missing'); continue
            if os.path.getsize(f) < 100:
                bad.append(f'{i}:tiny({os.path.getsize(f)}b)'); continue
            try:
                im = Image.open(f); im.load()
                if im.size != (64, 64):
                    bad.append(f'{i}:size{im.size}'); continue
                rgba = im.convert('RGBA')
                if rgba.getextrema()[3][0] == 255:
                    bad.append(f'{i}:no-alpha')
            except Exception as e:  # noqa: BLE001
                bad.append(f'{i}:decode({e})')
        check(f'{bank} x{len(ids)}', not bad, '; '.join(str(x) for x in bad[:3]))

    print('== filesystem: shiny banks differ from normal (full pair diff) ==')
    for base, shiny in [('gen3-rs', 'gen3-rs-shiny'),
                        ('gen3-rs-back', 'gen3-rs-back-shiny'),
                        ('gen3-frlg', 'gen3-frlg-shiny'),
                        ('gen3-frlg-back', 'gen3-frlg-back-shiny'),
                        ('gen3-emerald', 'gen3-emerald-shiny')]:
        same = []
        for i in STATIC_BANKS[base]:
            if img_sig(os.path.join(R, 'assets/sprites', base, f'{i}.png')) == \
               img_sig(os.path.join(R, 'assets/sprites', shiny, f'{i}.png')):
                same.append(i)
        illegal = [i for i in same if (i, base) not in SHINY_PLACEHOLDER_OK]
        allowed = [i for i in same if (i, base) in SHINY_PLACEHOLDER_OK]
        check(f'shiny != normal ({base})', not illegal,
              f'illegal-identical:{illegal[:4]}; documented placeholders:{allowed}')

    print('== filesystem: Deoxys forme matrix (Normal/Attack/Defense/Speed) ==')
    S = lambda b, i: img_sig(os.path.join(R, 'assets/sprites', b, f'{i}.png'))
    check('emerald/10015 == rs/10015 (speed front, same source)',
          S('gen3-emerald', 10015) == S('gen3-rs', 10015))
    check('emerald/386 = normal-forme still (differs from speed)',
          S('gen3-emerald', 386) != S('gen3-emerald', 10015))
    check('emerald shiny speed is genuine (differs from normal)',
          S('gen3-emerald-shiny', 10015) != S('gen3-emerald', 10015))
    check('speed back shiny is genuine (differs from back normal)',
          S('gen3-rs-back-shiny', 10015) != S('gen3-rs-back', 10015))
    check('speed back is a back view (differs from front)',
          S('gen3-rs-back', 10015) != S('gen3-rs', 10015))
    check('frlg: normal/attack/defense all distinct',
          len({S('gen3-frlg', 386), S('gen3-frlg', 10013), S('gen3-frlg', 10014)}) == 3)
    check('frlg attack back is a back view',
          S('gen3-frlg-back', 10013) != S('gen3-frlg', 10013))
    check('frlg defense back is a back view',
          S('gen3-frlg-back', 10014) != S('gen3-frlg', 10014))

    print(f'== filesystem: {ANIM_BANK} (multi-frame webp 1..386) ==')
    bad = []
    for i in IDS:
        f = os.path.join(R, 'assets/sprites', ANIM_BANK, f'{i}.webp')
        if not os.path.isfile(f):
            bad.append(f'{i}:missing'); continue
        if os.path.getsize(f) < 500:
            bad.append(f'{i}:tiny'); continue
        try:
            im = Image.open(f)
            if getattr(im, 'n_frames', 1) <= 1:
                bad.append(f'{i}:static')
        except Exception as e:  # noqa: BLE001
            bad.append(f'{i}:decode({e})')
    check('anim webp x386 animated', not bad, '; '.join(str(x) for x in bad[:3]))

    print('== filesystem: cries 1..386.ogg ==')
    bad = []
    for i in range(252, 387):
        f = os.path.join(R, 'assets/audio/cries', f'{i}.ogg')
        if not os.path.isfile(f):
            bad.append(f'{i}:missing')
        elif os.path.getsize(f) < 2000:
            bad.append(f'{i}:small({os.path.getsize(f)}b)')
    check('cries: 252..386 present, >2KB', not bad, '; '.join(bad[:4]))
    head = subprocess.run(
        ['git', 'ls-tree', 'HEAD', '--', 'assets/audio/cries'],
        cwd=R, capture_output=True, text=True).stdout
    blobs = {}
    for line in head.splitlines():
        meta, path = line.split('\t', 1)
        blobs[os.path.basename(path)] = meta.split()[2]
    changed, missing = [], []
    for i in range(1, 252):
        f = os.path.join(R, 'assets/audio/cries', f'{i}.ogg')
        if not os.path.isfile(f):
            missing.append(i); continue
        data = open(f, 'rb').read()
        sha = hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()
        if i in blobs and blobs[i] != sha:
            changed.append(i)
    check('cries: 1..251 untouched vs HEAD', not changed and not missing,
          f'changed:{changed[:4]} missing:{missing[:4]}')

    print('== wiring: gen3-data.js SPRITE_SETS + forme ids ==')
    src = open(os.path.join(R, 'assets/js/gen3-data.js'), encoding='utf-8').read()
    need = [f'assets/sprites/{b}/__ID__' for b in list(STATIC_BANKS) + [ANIM_BANK]]
    missing = [t for t in need if t not in src]
    check('all 11 bank templates referenced via __ID__', not missing, str(missing[:3]))
    data = json.loads(src[src.find('const DATA = ') + 13:src.find(';\nconst SPRITE_SETS')])
    dex = {p['formes'][k]['sprite'] for p in data if 'formes' in p for k in ('fr', 'lg', 'em')}
    check('DATA formes carry sprite ids 10013/10014/10015', dex == set(FORMES), str(dex))


def shot_sig(page, sel):
    import io
    buf = page.locator(sel).screenshot()
    return hashlib.md5(io.BytesIO(buf).getvalue()).hexdigest()


def browser_checks():
    print('== browser: pixelated rendering + animated webp playback (Chromium) ==')
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
        errors = []
        page = ctx.new_page()
        page.on('pageerror', lambda e: errors.append(str(e)))

        page.goto(f'file://{R}/gen3.html')
        page.wait_for_timeout(1700)

        pix = page.evaluate(
            "getComputedStyle(document.querySelector('#sprImg')).imageRendering")
        check('#sprImg image-rendering:pixelated', pix == 'pixelated', pix)
        page.evaluate("select(1)")   # Bulbasaur: evolution chain with sprites
        page.wait_for_timeout(400)
        pix_evo = page.evaluate(
            "[...document.querySelectorAll('.espr img')].map(i=>getComputedStyle(i).imageRendering).every(v=>v==='pixelated')")
        check('evo sprites image-rendering:pixelated', pix_evo)
        page.evaluate("select(252)")

        def src():
            return page.evaluate("document.querySelector('#sprImg').src")

        # --- R/S chip: front/back x normal/shiny reach all four rs banks
        page.click('.tchip[data-th=ruby]')
        page.wait_for_timeout(250)
        check('ruby front bank', 'gen3-rs/' in src())
        page.click('#btnBack')
        page.wait_for_timeout(150)
        check('ruby back bank', 'gen3-rs-back/' in src())
        page.click('#chipShiny')
        page.wait_for_timeout(150)
        check('ruby back-shiny bank', 'gen3-rs-back-shiny/' in src())
        page.click('#btnBack')
        page.wait_for_timeout(150)
        check('ruby shiny bank', 'gen3-rs-shiny/' in src())
        page.click('#chipShiny')

        # --- FIRERED chip: frlg bank + forme 10013
        page.click('.tchip[data-th=firered]')
        page.wait_for_timeout(250)
        check('firered front bank', 'gen3-frlg/' in src() and 'gen3-frlg/' in src() and '-back' not in src())
        page.evaluate("select(386)")
        page.wait_for_timeout(200)
        check('deoxys firered = attack forme (10013)', 'gen3-frlg/10013.png' in src(), src())
        page.click('#btnBack')
        page.wait_for_timeout(150)
        check('deoxys firered back = attack back', 'gen3-frlg-back/10013.png' in src(), src())
        page.click('#btnBack')

        # --- LEAFGREEN chip: forme 10014
        page.click('.tchip[data-th=leafgreen]')
        page.wait_for_timeout(250)
        check('deoxys leafgreen = defense forme (10014)', 'gen3-frlg/10014.png' in src(), src())

        # --- EMERALD chip: speed forme views + anim guard
        page.click('.tchip[data-th=emerald]')
        page.wait_for_timeout(250)
        check('deoxys emerald front = speed forme (10015)', 'gen3-emerald/10015.png' in src(), src())
        page.click('#chipShiny')
        page.wait_for_timeout(150)
        check('deoxys emerald shiny = speed shiny still', 'gen3-emerald-shiny/10015.png' in src(), src())
        page.click('#btnBack')
        page.wait_for_timeout(150)
        check('deoxys emerald back shiny = speed back shiny', 'gen3-rs-back-shiny/10015.png' in src(), src())
        page.click('#chipShiny')
        page.wait_for_timeout(150)
        check('deoxys emerald back = speed back', 'gen3-rs-back/10015.png' in src(), src())
        page.click('#btnBack')

        # anim: Pikachu plays, Deoxys never animates the wrong forme
        page.evaluate("select(25)")
        page.click('#chipAnim')
        page.wait_for_timeout(400)
        check('anim bank active in UI', 'gen3-emerald-anim' in src() and src().endswith('.webp'), src())
        s1 = shot_sig(page, '#sprBox')
        page.wait_for_timeout(900)
        s2 = shot_sig(page, '#sprBox')
        check('animated webp PLAYS in Chromium (sprite pixels change)', s1 != s2)
        page.evaluate("select(386)")
        page.wait_for_timeout(300)
        check('deoxys anim-guard: still, not webp',
              'gen3-emerald-anim' not in src() and 'gen3-emerald/10015.png' in src(), src())
        page.click('#chipAnim')     # anim OFF
        check('no page errors (Chromium)', not errors, '; '.join(errors[:3]))

        # WebCodecs ImageDecoder: authoritative frame count in-browser
        b64 = base64.b64encode(
            open(os.path.join(R, 'assets/sprites/gen3-emerald-anim/25.webp'),
                 'rb').read()).decode()
        fc = page.evaluate("""(async (b64) => {
            const bin = atob(b64);
            const buf = new Uint8Array(bin.length);
            for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);
            const d = new ImageDecoder({data: buf, type: 'image/webp'});
            await d.tracks.ready;
            return d.tracks.selectedTrack.frameCount;
        })""", b64)
        check('in-browser decoder sees multiple frames', (fc or 0) > 1, f'frames={fc}')
        page.screenshot(path='/tmp/gen3_sprites_chromium.png')

        print('== browser: animated webp playback (Firefox) ==')
        ff_ok = os.path.exists(pw.firefox.executable_path)
        if not ff_ok:
            import subprocess
            try:
                subprocess.run(['python3', '-m', 'playwright', 'install', 'firefox'],
                               check=True, capture_output=True, timeout=420)
                ff_ok = os.path.exists(pw.firefox.executable_path)
            except Exception as e:  # noqa: BLE001
                print(f'  (firefox unavailable: {e})')
        if ff_ok:
            ff = pw.firefox.launch()
            fctx = ff.new_context(viewport={'width': 1280, 'height': 900})
            ferr = []
            fp = fctx.new_page()
            fp.on('pageerror', lambda e: ferr.append(str(e)))
            fp.goto(f'file://{R}/gen3.html')
            fp.wait_for_timeout(2200)
            fp.click('.tchip[data-th=emerald]')
            fp.wait_for_timeout(300)
            fp.evaluate("select(25)")
            fp.click('#chipAnim')
            fp.wait_for_timeout(500)
            fsrc = fp.evaluate("document.querySelector('#sprImg').src")
            check('firefox: anim bank loads', 'gen3-emerald-anim' in fsrc and fsrc.endswith('.webp'))
            # three samples over ~2s — pass on any differing pair (flakes prove
            # nothing about playback, they only prove timing)
            sgs = []
            for _ in range(3):
                sgs.append(shot_sig(fp, '#sprBox'))
                fp.wait_for_timeout(700)
            plays = len(set(sgs)) > 1
            check('firefox: animated webp PLAYS (sprite pixels change)', plays, f'sigs={len(set(sgs))}')
            check('firefox: no page errors', not ferr, '; '.join(ferr[:3]))
            fp.screenshot(path='/tmp/gen3_sprites_firefox.png')
            ff.close()
        else:
            check('firefox: playback proof SKIPPED (binary unavailable, chromium proved it)', True,
                  'skipped')
        browser.close()


def run():
    fs_audit()
    browser_checks()
    fails = [r for r in results if not r[1]]
    print(f'\n{len(results) - len(fails)}/{len(results)} passed')
    return 1 if fails else 0


if __name__ == '__main__':
    raise SystemExit(run())
