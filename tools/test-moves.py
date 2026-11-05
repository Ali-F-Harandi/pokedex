#!/usr/bin/env python3
"""Pokédex Plus — Phase 2 browser test: moves section, tabs, Moves Dex,
TM/HM list, FA mode. Run: python3 tools/test-moves.py (needs playwright)"""
import os
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT = '/tmp/phase02_shots'
os.makedirs(SHOT, exist_ok=True)

results = []


def check(name, cond, extra=''):
    results.append((name, bool(cond), extra))
    print(f'  {"PASS" if cond else "FAIL"}  {name}  {extra}')


def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
        errors = []
        page = ctx.new_page()
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: errors.append(str(e)))

        # ---------------- red-blue ----------------
        print('== gen1.html (RED theme) ==')
        ctx.add_init_script("try{localStorage.setItem('pkd_g1_theme', JSON.stringify('red'))}catch(e){}")
        page.goto(f'file://{R}/gen1.html')
        page.wait_for_timeout(900)
        check('rb: no js errors', not [e for e in errors if 'favicon' not in e], errors[:3])

        check('rb: moves section present', page.locator('#movesSec').count() == 1)
        n_lv = page.locator('#movesSec .mrow').count()
        check('rb: level-up rows for pikachu(25)', n_lv > 5, f'{n_lv} rows')
        # default tab = level-up, first row should be a Lv badge
        first_badge = page.locator('#movesSec .mrow .mv-badge').first.text_content()
        check('rb: first badge is level', 'Lv' in first_badge or 'سطح' in first_badge, first_badge)

        # TM tab
        page.click('#movesSec .mtab[data-mt="tm"]')
        page.wait_for_timeout(120)
        tm_badge = page.locator('#movesSec .mrow .mv-badge').first.text_content()
        check('rb: tm tab shows TM badges', 'TM' in tm_badge, tm_badge)
        n_tm = page.locator('#movesSec .mrow').count()
        check('rb: pikachu machine moves (21 TM + HM05 flash)', n_tm == 22, f'{n_tm}')
        check('rb: no egg/tutor tabs (gen1)', page.locator('#movesSec .mtab[data-mt="egg"]').count() == 0)

        # green note present on rb page
        check('rb: green note', page.locator('#movesSec .mv-note').count() >= 1)

        # click a move row -> moves dex opens in detail mode
        page.click('#movesSec .mrow')
        page.wait_for_timeout(200)
        check('rb: dex opened', page.locator('#movesWrap').is_visible())
        check('rb: detail view', page.locator('#movesWrap .md-card').count() == 1)
        # effect label (gen1 wording)
        head = page.locator('#mvHeadT').text_content()
        check('rb: header has game', 'RED/BLUE' in head, head)
        page.screenshot(path=f'{SHOT}/rb-movedetail.png')
        # learned-by chips present, click one -> selects pokemon
        n_chips = page.locator('#movesWrap .lchip').count()
        check('rb: learned-by chips', n_chips > 3, f'{n_chips}')
        page.locator('#movesWrap .lchip').first.click()
        page.wait_for_timeout(250)
        check('rb: dex closed after chip click', not page.locator('#movesWrap').is_visible())

        # back to list view: open dex via menu
        page.click('#startBtn')
        page.wait_for_timeout(150)
        check('rb: menu items injected', page.locator('#menuPop [data-act=movesdex]').count() == 1)
        page.click('#menuPop [data-act=movesdex]')
        page.wait_for_timeout(200)
        check('rb: dex list view', page.locator('#movesWrap .mgrid').count() == 1)
        n_cards = page.locator('#movesWrap .mcard').count()
        check('rb: all 165 gen-1 moves', n_cards == 165, f'{n_cards}')
        # search filter
        page.fill('#mvQ', 'thunder')
        page.wait_for_timeout(250)
        n_filtered = page.locator('#movesWrap .mcard').count()
        check('rb: search thunder', 3 <= n_filtered <= 8, f'{n_filtered}')
        page.screenshot(path=f'{SHOT}/rb-dexlist.png')
        # type filter normal (clear search first)
        page.fill('#mvQ', '')
        page.wait_for_timeout(250)
        page.click('#movesWrap .mv-typechips .mchip[data-t="normal"]')
        page.wait_for_timeout(200)
        check('rb: type filter works', page.locator('#movesWrap .mcard').count() > 10)
        page.click('#movesWrap .mv-close')
        page.wait_for_timeout(120)
        check('rb: dex closed', not page.locator('#movesWrap').is_visible())

        # TM/HM list view
        page.click('#startBtn'); page.wait_for_timeout(120)
        page.click('#menuPop [data-act=tmhm]')
        page.wait_for_timeout(200)
        n_tm_rows = page.locator('#movesWrap .tmrow').count()
        check('rb: TM/HM list = 55', n_tm_rows == 55, f'{n_tm_rows}')
        check('rb: first TM row is TM01 mega punch',
              'MEGA PUNCH' in (page.locator('#movesWrap .tmrow').first.text_content() or '').upper())
        page.screenshot(path=f'{SHOT}/rb-tmlist.png')
        page.click('#movesWrap .mv-close')

        # ---------------- yellow (spot) ----------------
        print('== gen1.html (YELLOW theme) ==')
        errors.clear()
        ctx2 = browser.new_context(viewport={'width': 1280, 'height': 900}); ctx2.add_init_script("try{localStorage.setItem('pkd_g1_theme', JSON.stringify('yellow'))}catch(e){}"); page2 = ctx2.new_page(); page2.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None); page2.on('pageerror', lambda e: errors.append(str(e))); page = page2; page.goto(f'file://{R}/gen1.html#25')
        page.wait_for_timeout(900)
        check('y: no js errors', not [e for e in errors if 'favicon' not in e], errors[:3])
        check('y: moves section', page.locator('#movesSec').count() == 1)
        # pikachu yellow: thunderbolt at 26 in level-up list
        page.click('#movesSec .mtab[data-mt="lv"]')
        page.wait_for_timeout(120)
        body_txt = page.locator('#movesSec').text_content()
        check('y: THUNDERBOLT in lv list', 'THUNDERBOLT' in body_txt.upper())
        check('y: Lv.26 badge', '26' in body_txt)

        # ---------------- goldsilver (redirects to the unified gen2.html) ----------------
        print('== goldsilver.html ==')
        errors.clear()
        page.goto(f'file://{R}/goldsilver.html#1')
        page.wait_for_timeout(1700)
        # since the Gen-2 plan phase 1, goldsilver.html redirects to gen2.html —
        # the unified Gen-2 page; G/S moves come from its GOLD/SILVER label
        check('gs: no js errors', not [e for e in errors if 'favicon' not in e], errors[:3])
        check('gs: moves section on the unified page', page.locator('#movesSec').count() == 1)
        mv_lbl = page.evaluate("(document.querySelector('#movesSec .mv-game')||{textContent:''}).textContent")
        check('gs: moves label shows GOLD/SILVER', 'GOLD/SILVER' in mv_lbl, mv_lbl)
        page.evaluate("select(1)")   # Bulbasaur (the redirect drops the #1 anchor)
        page.wait_for_timeout(250)
        tabs = page.locator('#movesSec .mtab').count()
        check('gs: 3 tabs for bulbasaur (lv/tm/egg — tutor is Crystal-only)', tabs == 3, f'{tabs}')
        page.click('#movesSec .mtab[data-mt="egg"]')
        page.wait_for_timeout(120)
        egg_txt = page.locator('#movesSec').text_content()
        check('gs: bulbasaur egg has SKULL BASH', 'SKULL BASH' in egg_txt.upper())
        page.screenshot(path=f'{SHOT}/gs-egg.png')

        # moves dex gen2: 251 moves
        page.click('#movesSec .mv-all')
        page.wait_for_timeout(200)
        check('gs: dex 251 moves', page.locator('#movesWrap .mcard').count() == 251)
        # dark type chip exists on gen2
        check('gs: dark type chip', page.locator('#movesWrap .mchip[data-t="dark"]').count() == 1)
        # curse move shows ??? type
        page.fill('#mvQ', 'curse')
        page.wait_for_timeout(250)
        page.locator('#movesWrap .mcard').first.click()
        page.wait_for_timeout(200)
        det = page.locator('#movesWrap .md-card').text_content()
        check('gs: curse ??? badge', '???' in det)
        page.screenshot(path=f'{SHOT}/gs-curse.png')
        page.click('#movesWrap .mv-close')

        # ---------------- crystal (redirects to the unified gen2.html) ----------------
        print('== crystal.html ==')
        errors.clear()
        ctx3 = browser.new_context(viewport={'width': 1280, 'height': 900}); ctx3.add_init_script("try{localStorage.setItem('pkd_g2_theme', JSON.stringify('crystal'))}catch(e){}"); page3 = ctx3.new_page(); page3.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None); page3.on('pageerror', lambda e: errors.append(str(e))); page = page3
        page.goto(f'file://{R}/crystal.html#25')
        page.wait_for_timeout(1700)
        check('c: no js errors', not [e for e in errors if 'favicon' not in e], errors[:3])
        check('c: redirected page runs the crystal theme', page.evaluate("document.body.classList.contains('theme-crystal')"))
        mv_lbl = page.evaluate("(document.querySelector('#movesSec .mv-game')||{textContent:''}).textContent")
        check('c: moves label shows CRYSTAL', 'CRYSTAL' in mv_lbl, mv_lbl)
        page.evaluate("select(25)")   # Pikachu (the redirect drops the #25 anchor)
        page.wait_for_timeout(250)
        tabs = page.locator('#movesSec .mtab').count()
        check('c: pikachu crystal has tutor tab', page.locator('#movesSec .mtab[data-mt="tutor"]').count() == 1, f'{tabs}')
        page.click('#movesSec .mtab[data-mt="tutor"]')
        page.wait_for_timeout(120)
        tut = page.locator('#movesSec').text_content().upper()
        check('c: tutor = THUNDERBOLT (pikachu)', 'THUNDERBOLT' in tut)
        # TM list has tutor note
        page.click('#movesSec .mv-all')
        page.wait_for_timeout(150)
        page.click('#movesWrap .mvtab[data-v="tmhm"]')
        page.wait_for_timeout(150)
        note = page.locator('#movesWrap .mv-note.big').count()
        check('c: tutor note on TM view', note == 1)
        page.screenshot(path=f'{SHOT}/c-tmlist.png')

        # ---------------- FA mode ----------------
        print('== FA mode ==')
        page.click('#movesWrap .mv-close')
        page.click('#langBtn')
        page.wait_for_timeout(300)
        sec_fa = page.locator('#movesSec').text_content()
        check('fa: section shows Persian', 'حرکت' in sec_fa)
        check('fa: Persian digits in badges', 'سطح' in sec_fa or '۰' in sec_fa)
        page.click('#movesSec .mtab[data-mt="lv"]')
        page.wait_for_timeout(150)
        row_fa = page.locator('#movesSec .mrow').first.text_content()
        check('fa: move row has FA name', any('\u0600' <= ch <= '\u06ff' for ch in row_fa), row_fa[:40])
        page.screenshot(path=f'{SHOT}/fa-crystal.png')
        page.click('#movesSec .mrow')
        page.wait_for_timeout(200)
        det_fa = page.locator('#movesWrap .md-desc').text_content()
        check('fa: description FA primary', any('\u0600' <= ch <= '\u06ff' for ch in det_fa), det_fa[:50])
        # menu labels FA
        page.click('#movesWrap .mv-close')
        page.click('#startBtn'); page.wait_for_timeout(150)
        m = page.locator('#menuPop [data-act=movesdex] .mv-menu-l').text_content()
        check('fa: menu label', 'دکس' in (m or ''), m)
        page.keyboard.press('Escape')

        browser.close()

    fails = [r for r in results if not r[1]]
    print()
    print(f'===== {len(results) - len(fails)}/{len(results)} passed =====')
    for name, ok, extra in fails:
        print('  FAIL:', name, extra)
    return len(fails)


if __name__ == '__main__':
    sys_exit = run()
    raise SystemExit(sys_exit)
