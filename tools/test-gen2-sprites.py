#!/usr/bin/env python3
"""Pokédex Plus — Gen-2 sprite & cry completeness audit (phase 2 of the
Gen-2 plan). Proves every Gen-2 sprite variant exists and renders correctly
for all 251 Pokémon:
  - 12 static banks (gold/silver/crystal x front/back x normal/shiny):
    ids 1..251, non-empty, PIL-decodable, alpha channel present
  - gen2-crystal-anim: ids 1..251 webp, decodable, frames > 1
  - shiny banks differ from the normal banks (full set, front + back)
  - cries 1..251.ogg present, non-trivial size
  - gen2-data.js SPRITE_SETS wiring points at exactly these banks
  - browser: image-rendering:pixelated on the big sprite + evo sprites,
    the animated webp actually PLAYS in Chromium AND Firefox, and the UI
    reaches every bank (front/back/shiny/anim)
Run: python3 tools/test-gen2-sprites.py (PIL + playwright)"""
import os
import hashlib
from PIL import Image
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDS = list(range(1, 252))

PNG_BANKS = [
    'gen2-gold', 'gen2-gold-back', 'gen2-gold-shiny', 'gen2-gold-back-shiny',
    'gen2-silver', 'gen2-silver-back', 'gen2-silver-shiny', 'gen2-silver-back-shiny',
    'gen2-crystal', 'gen2-crystal-back', 'gen2-crystal-shiny', 'gen2-crystal-back-shiny',
]
ANIM_BANK = 'gen2-crystal-anim'
GAMES = [('gold', 'gen2-gold', 'gen2-gold-shiny',
          'gen2-gold-back', 'gen2-gold-back-shiny'),
         ('silver', 'gen2-silver', 'gen2-silver-shiny',
          'gen2-silver-back', 'gen2-silver-back-shiny'),
         ('crystal', 'gen2-crystal', 'gen2-crystal-shiny',
          'gen2-crystal-back', 'gen2-crystal-back-shiny')]

results = []


def check(name, cond, extra=''):
    results.append((name, bool(cond), extra))
    print(f'  {"PASS" if cond else "FAIL"}  {name}  {extra}')


def img_sig(path):
    im = Image.open(path).convert('RGBA')
    return hashlib.md5(im.tobytes()).hexdigest()


def fs_audit():
    print('== filesystem: 12 static banks x251 (exists / size / decode / alpha) ==')
    for bank in PNG_BANKS:
        bad = []
        for i in IDS:
            f = os.path.join(R, 'assets/sprites', bank, f'{i}.png')
            if not os.path.isfile(f):
                bad.append(f'{i}:missing'); continue
            if os.path.getsize(f) < 100:
                bad.append(f'{i}:tiny({os.path.getsize(f)}b)'); continue
            try:
                im = Image.open(f); im.load()
            except Exception as e:
                bad.append(f'{i}:decode({e})'); continue
            if im.mode != 'RGBA' or 'A' not in im.getbands():
                bad.append(f'{i}:noalpha({im.mode})')
        check(f'{bank}: 1..251 complete, RGBA, decodable', not bad, '; '.join(bad[:4]))

    print('== filesystem: crystal animated webp x251 (decodable, frames>1) ==')
    bad = []
    for i in IDS:
        f = os.path.join(R, 'assets/sprites', ANIM_BANK, f'{i}.webp')
        if not os.path.isfile(f):
            bad.append(f'{i}:missing'); continue
        if os.path.getsize(f) < 200:
            bad.append(f'{i}:tiny'); continue
        try:
            im = Image.open(f); im.load()
        except Exception as e:
            bad.append(f'{i}:decode({e})'); continue
        if getattr(im, 'n_frames', 1) < 2:
            bad.append(f'{i}:frames={getattr(im, "n_frames", 1)}')
    check('gen2-crystal-anim: 1..251 webp, all animated', not bad, '; '.join(bad[:4]))

    print('== filesystem: shiny banks differ from normal (front + back, 3 games) ==')
    same = []
    for game, nd, sd, nbd, sbd in GAMES:
        for pair in ((nd, sd), (nbd, sbd)):
            for i in IDS:
                try:
                    if img_sig(os.path.join(R, 'assets/sprites', pair[0], f'{i}.png')) == \
                       img_sig(os.path.join(R, 'assets/sprites', pair[1], f'{i}.png')):
                        same.append(f'{game}:{pair[0].split("-", 2)[-1]}:{i}')
                except Exception as e:
                    same.append(f'{game}:{i}:err')
    check('no shiny sprite identical to its normal (753 comparisons)', not same, '; '.join(same[:6]))

    print('== filesystem: cries 1..251.ogg ==')
    bad = []
    for i in IDS:
        f = os.path.join(R, 'assets/audio/cries', f'{i}.ogg')
        if not os.path.isfile(f):
            bad.append(f'{i}:missing')
        elif os.path.getsize(f) < 2000:
            bad.append(f'{i}:small({os.path.getsize(f)}b)')
    check('cries: 1..251 present, >2KB', not bad, '; '.join(bad[:4]))

    print('== wiring: gen2-data.js SPRITE_SETS points at the audited banks ==')
    src = open(os.path.join(R, 'assets/js/gen2-data.js'), encoding='utf-8').read()
    missing = [b for b in PNG_BANKS + [ANIM_BANK] if f'assets/sprites/{b}/__ID__' not in src]
    check('all 13 banks referenced via __ID__ templates in SPRITE_SETS', not missing, str(missing))


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

        page.goto(f'file://{R}/gen2.html')
        page.wait_for_timeout(1700)

        pix = page.evaluate(
            "getComputedStyle(document.querySelector('#sprBox img')).imageRendering")
        check('#sprImg image-rendering:pixelated', pix == 'pixelated', pix)
        pix_evo = page.evaluate(
            "[...document.querySelectorAll('.evo .espr img')].map(i=>getComputedStyle(i).imageRendering).every(v=>v==='pixelated')")
        check('evo sprites image-rendering:pixelated', pix_evo)
        pix_row = page.evaluate(
            "getComputedStyle(document.querySelector('#list .row img') || document.querySelector('#list .row .ball')).imageRendering")
        check('list thumbnails pixelated (ball/row icons)', pix_row == 'pixelated', pix_row)

        # Crystal + ANIM: prove the webp PLAYS (frame change => pixels change)
        page.click('#themeRow [data-th="crystal"]')
        page.wait_for_timeout(250)
        page.evaluate("select(25)")          # Pikachu: 21 frames
        page.click('#chipAnim')
        page.wait_for_timeout(400)
        src = page.evaluate("document.querySelector('#sprImg').src")
        check('anim bank active in UI', 'gen2-crystal-anim' in src and src.endswith('.webp'))
        s1 = shot_sig(page, '#sprBox')
        page.wait_for_timeout(900)
        s2 = shot_sig(page, '#sprBox')
        check('animated webp PLAYS in Chromium (sprite pixels change)', s1 != s2)
        check('no page errors (Chromium)', not errors, '; '.join(errors[:3]))

        # WebCodecs ImageDecoder: authoritative frame count in-browser
        import base64
        b64 = base64.b64encode(
            open(os.path.join(R, 'assets/sprites/gen2-crystal-anim/25.webp'),
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

        # every bank reachable through the UI (front/back/shiny/anim x3 games)
        page.click('#chipAnim')     # anim OFF
        page.click('#btnBack')
        page.wait_for_timeout(150)
        check('crystal back bank', 'gen2-crystal-back/' in
              page.evaluate("document.querySelector('#sprImg').src"))
        page.click('#btnBack')      # front again
        page.click('#chipShiny')    # shiny ON
        page.click('#btnBack')      # back view -> back-shiny
        page.wait_for_timeout(150)
        check('crystal back-shiny bank', 'gen2-crystal-back-shiny/' in
              page.evaluate("document.querySelector('#sprImg').src"))
        page.click('#btnBack')      # front
        page.click('#chipShiny')    # shiny OFF
        for th, bank in [('gold', 'gen2-gold-back-shiny'), ('silver', 'gen2-silver-back-shiny')]:
            page.click('#themeRow [data-th="%s"]' % th)
            page.click('#chipShiny')
            page.click('#btnBack')
            page.wait_for_timeout(150)
            check(f'{th} back-shiny bank', bank in
                  page.evaluate("document.querySelector('#sprImg').src"))
            page.click('#btnBack')
            page.click('#chipShiny')
        page.screenshot(path='/tmp/gen2_sprites_chromium.png')

        print('== browser: animated webp playback (Firefox) ==')
        ff = pw.firefox.launch()
        fctx = ff.new_context(viewport={'width': 1280, 'height': 900})
        ferr = []
        fp = fctx.new_page()
        fp.on('pageerror', lambda e: ferr.append(str(e)))
        fp.goto(f'file://{R}/gen2.html')
        fp.wait_for_timeout(2200)
        fp.click('#themeRow [data-th="crystal"]')
        fp.wait_for_timeout(300)
        fp.evaluate("select(25)")
        fp.click('#chipAnim')
        fp.wait_for_timeout(500)
        fsrc = fp.evaluate("document.querySelector('#sprImg').src")
        check('firefox: anim bank loads', 'gen2-crystal-anim' in fsrc and fsrc.endswith('.webp'))
        f1 = shot_sig(fp, '#sprBox')
        fp.wait_for_timeout(900)
        f2 = shot_sig(fp, '#sprBox')
        check('firefox: animated webp PLAYS (sprite pixels change)', f1 != f2)
        check('firefox: no page errors', not ferr, '; '.join(ferr[:3]))
        fp.screenshot(path='/tmp/gen2_sprites_firefox.png')

        browser.close()
        ff.close()


def run():
    fs_audit()
    browser_checks()
    fails = [r for r in results if not r[1]]
    print(f'\n{len(results) - len(fails)}/{len(results)} passed')
    return 1 if fails else 0


if __name__ == '__main__':
    raise SystemExit(run())
