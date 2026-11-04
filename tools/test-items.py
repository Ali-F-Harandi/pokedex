#!/usr/bin/env python3
"""Pokédex Plus — Phase 3 browser test: Item Dex on gen1/goldsilver/crystal.
Run: python3 tools/test-items.py (needs playwright)"""
import os
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT = '/tmp/items_shots'
os.makedirs(SHOT, exist_ok=True)
results = []


def check(name, cond, extra=''):
    results.append((name, bool(cond), extra))
    print(f'  {"PASS" if cond else "FAIL"}  {name}  {extra}')


def open_items(page, key='i'):
    page.keyboard.press(key)
    page.wait_for_timeout(250)


def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
        errors = []
        page = ctx.new_page()
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: errors.append(str(e)))

        # ---------------- gen1 ----------------
        print('== gen1.html ==')
        page.goto(f'file://{R}/gen1.html')
        page.wait_for_timeout(1700)
        check('gen1 loads clean', not errors, '; '.join(errors[:2]))
        menu_has_items = page.evaluate("!!document.querySelector('#menuPop [data-act=itemsdex]')")
        check('START menu has Item Dex entry', menu_has_items)
        open_items(page)
        check('overlay opens with I key', page.evaluate("!document.querySelector('#itemsWrap').classList.contains('hidden')"))
        head = page.evaluate("document.querySelector('#itHeadT').textContent")
        check('head shows R/B/Y', 'R/B/Y' in head, head)
        n = page.evaluate("document.querySelectorAll('.icard').length")
        check('gen1 item count = 72', n == 72, str(n))
        # GB icons default
        src = page.evaluate("document.querySelector('.icard .icn') && document.querySelector('.icard .icn').src")
        check('GB icons by default on gen1', src and 'itemicons-gb' in src, str(src)[-40:])
        # search FA
        page.fill('#itQ', 'مستربال')
        page.wait_for_timeout(250)
        n = page.evaluate("document.querySelectorAll('.icard').length")
        check('FA search finds MASTER BALL', n == 1, str(n))
        page.click('.icard')
        page.wait_for_timeout(200)
        check('detail view opens', page.evaluate("!!document.querySelector('.id-card')"))
        buy = page.evaluate("[...document.querySelectorAll('.id-stat b')].map(x=>x.textContent)")
        check('gen1 prices shown (master ball not for sale)', buy and buy[0] == '—', str(buy))
        body_txt = page.evaluate("document.querySelector('#itBody').textContent")
        check('no G/S/C wording label on gen1 (gen1-only info)', 'GOLD' not in body_txt.upper() and 'CRYSTAL' not in body_txt.upper())
        chips = page.evaluate("[...document.querySelectorAll('.id-gchip')].map(x=>x.textContent)")
        check('gen1 availability chips are R/B + YELLOW only', set(chips) <= {'RED/BLUE', 'YELLOW'} and len(chips) == 2, str(chips))
        page.screenshot(path=f'{SHOT}/gen1-detail.png')
        # gen1-only item without description
        page.click('#itBack')
        page.wait_for_timeout(150)
        page.fill('#itQ', 'SILPH')
        page.wait_for_timeout(250)
        page.click('.icard')
        page.wait_for_timeout(200)
        note = page.evaluate("document.querySelector('.id-desc .d-fa').textContent")
        check('gen1-only item gets the no-description note', 'نسل اول' in note or 'Generation I' in note, note[:40])
        # icon style toggle
        page.click('#itBack')
        page.wait_for_timeout(150)
        page.fill('#itQ', '')
        page.wait_for_timeout(250)
        page.click('#itStyle')
        page.wait_for_timeout(150)
        src = page.evaluate("document.querySelector('.icard .icn').src")
        check('icon toggle switches to color', 'itemicons/' in src and '-gb' not in src, str(src)[-40:])
        page.keyboard.press('Escape')

        # ---------------- goldsilver ----------------
        print('== goldsilver.html ==')
        page.goto(f'file://{R}/goldsilver.html')
        page.wait_for_timeout(1700)
        check('goldsilver loads clean', not errors, '; '.join(errors[:2]))
        open_items(page)
        head = page.evaluate("document.querySelector('#itHeadT').textContent")
        check('head shows GOLD/SILVER', 'GOLD/SILVER' in head, head)
        n = page.evaluate("document.querySelectorAll('.icard').length")
        check('gold/silver item count = 161', n == 161, str(n))
        src = page.evaluate("document.querySelector('.icard .icn').src")
        check('color icons by default on gen2', src and 'itemicons/' in src and '-gb' not in src, str(src)[-40:])
        # hyper potion price gen2 = 1200
        page.fill('#itQ', 'HYPER POTION')
        page.wait_for_timeout(250)
        page.click('.icard')
        page.wait_for_timeout(200)
        buy = page.evaluate("[...document.querySelectorAll('.id-stat b')].map(x=>x.textContent)")
        check('hyper potion costs ¥1200 in G/S', buy and '1200' in buy[0], str(buy))
        gs = page.evaluate("[...document.querySelectorAll('.id-gchip')].map(x=>x.className+':'+x.textContent)")
        check('availability chips show games', any('on' in x for x in gs), str(gs))
        page.screenshot(path=f'{SHOT}/gs-detail.png')
        page.keyboard.press('Escape')

        # ---------------- crystal ----------------
        print('== crystal.html ==')
        page.goto(f'file://{R}/crystal.html')
        page.wait_for_timeout(1700)
        check('crystal loads clean', not errors, '; '.join(errors[:2]))
        open_items(page)
        n = page.evaluate("document.querySelectorAll('.icard').length")
        check('crystal item count = 165', n == 165, str(n))
        page.fill('#itQ', 'GS BALL')
        page.wait_for_timeout(250)
        n = page.evaluate("document.querySelectorAll('.icard').length")
        check('crystal-only GS BALL found', n == 1, str(n))
        page.click('.icard')
        page.wait_for_timeout(200)
        ph = page.evaluate("!!document.querySelector('.id-ic .ph')")
        check('GS BALL shows placeholder (no icon exists)', ph)
        hold = page.evaluate("[...document.querySelectorAll('.id-gchip.on')].map(x=>x.textContent)")
        check('GS BALL is crystal-only', hold and 'CRYSTAL' in hold[0], str(hold))
        page.screenshot(path=f'{SHOT}/cr-detail.png')

        # ---------------- FA mode ----------------
        page.keyboard.press('Escape')
        page.click('#langBtn')
        page.wait_for_timeout(250)
        open_items(page)
        fa_head = page.evaluate("document.querySelector('#itHeadT').textContent")
        check('FA overlay title', 'دکس آیتم' in fa_head, fa_head)
        cat = page.evaluate("[...document.querySelectorAll('.it-chip')].slice(1,3).map(x=>x.textContent)")
        check('FA category chips', all(any('\u0600' <= c <= '\u06FF' for c in x) for x in cat if x), str(cat))
        page.screenshot(path=f'{SHOT}/fa.png')

        check('no console errors overall', not errors, '; '.join(errors[:3]))
        browser.close()

    fails = [r for r in results if not r[1]]
    print(f'\n{len(results) - len(fails)}/{len(results)} passed')
    return 1 if fails else 0


if __name__ == '__main__':
    raise SystemExit(run())
