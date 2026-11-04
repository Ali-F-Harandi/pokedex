#!/usr/bin/env python3
"""Verify the new phone section order + bilingual Pokémon name in the card."""
import os
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT = '/tmp/gen1_order'
os.makedirs(SHOT, exist_ok=True)
results = []


def check(name, cond, extra=''):
    results.append((name, bool(cond), extra))
    print(f'  {"PASS" if cond else "FAIL"}  {name}  {extra}')


with sync_playwright() as pw:
    browser = pw.chromium.launch()

    # ---------- PHONE (390px) ----------
    ctx = browser.new_context(viewport={'width': 390, 'height': 844})
    page = ctx.new_page()
    errors = []
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(f'file://{R}/gen1.html')
    page.wait_for_timeout(1700)

    check('phone: no console errors', not errors, '; '.join(errors[:3]))

    def box(sel):
        el = page.query_selector(sel)
        return el.bounding_box() if el else None

    tops = {s: box(s)['y'] for s in ['.cntBox', '#listPane', '#gameCfg', '.sprCard', '#detailPane']}
    check('phone order: DEX STATUS first', box('.cntBox')['y'] < box('#listPane')['y'])
    check('phone order: search box second', box('#listPane')['y'] < box('#gameCfg')['y'])
    check('phone order: SETTINGS third', box('#gameCfg')['y'] < box('.sprCard')['y'])
    check('phone order: Pokémon card fourth', box('.sprCard')['y'] < box('#detailPane')['y'])
    print('    section tops:', {k: round(v) for k, v in tops.items()})

    # bilingual name — EN mode: FA name under EN name
    main = page.evaluate("document.querySelector('#sprName').textContent")
    alt = page.evaluate("document.querySelector('#sprName .altName') && document.querySelector('#sprName .altName').textContent")
    sel_name = page.evaluate("PMAP[state.sel].display")
    sel_fa = page.evaluate("PMAP[state.sel].fa")
    check('phone EN mode: main name is English', main.strip().startswith(sel_name), main)
    check('phone EN mode: alt name is Persian', alt == sel_fa, str(alt))
    alt_y = page.evaluate("document.querySelector('#sprName .altName').getBoundingClientRect().top")
    main_y = page.evaluate("document.querySelector('#sprName bdi').getBoundingClientRect().top")
    check('phone EN mode: alt name renders BELOW the main name', alt_y > main_y)

    page.screenshot(path=f'{SHOT}/phone-en.png')

    # FA mode: EN name under FA name
    page.click('#langBtn')
    page.wait_for_timeout(300)
    main_fa = page.evaluate("document.querySelector('#sprName').textContent")
    alt_fa = page.evaluate("document.querySelector('#sprName .altName') && document.querySelector('#sprName .altName').textContent")
    check('phone FA mode: main name is Persian', main_fa.strip().startswith(sel_fa), main_fa)
    check('phone FA mode: alt name is English', alt_fa == sel_name, str(alt_fa))
    # only ONE alt line (nothing else is bilingual)
    n_alt = page.evaluate("document.querySelectorAll('#sprName .altName').length")
    check('exactly one secondary name line', n_alt == 1)
    dnm = page.evaluate("document.querySelector('.dnm').textContent")
    check('detail header stays single-language', dnm == sel_fa, dnm)
    page.screenshot(path=f'{SHOT}/phone-fa.png')

    # scrolling reaches the card naturally (order = document flow)
    page.evaluate("document.querySelector('.sprCard').scrollIntoView()")
    page.wait_for_timeout(250)
    check('phone: card scrolls into view above detail pane',
          page.evaluate("document.querySelector('.sprCard').getBoundingClientRect().top") <
          page.evaluate("document.querySelector('#detailPane').getBoundingClientRect().top"))
    ctx.close()

    # ---------- TABLET (900px) ----------
    ctx2 = browser.new_context(viewport={'width': 900, 'height': 1000})
    p2 = ctx2.new_page()
    p2.goto(f'file://{R}/gen1.html')
    p2.wait_for_timeout(1500)
    b = lambda s: p2.query_selector(s).bounding_box()
    check('tablet: detail right of list', b('#detailPane')['x'] > b('#listPane')['x'])
    check('tablet: settings below list, same column',
          abs(b('#gameCfg')['x'] - b('#listPane')['x']) < 4 and b('#gameCfg')['y'] > b('#listPane')['y'])
    check('tablet: card + status below settings',
          b('.sprCard')['y'] > b('#gameCfg')['y'] and b('.cntBox')['y'] > b('.sprCard')['y'])
    p2.screenshot(path=f'{SHOT}/tablet.png')
    ctx2.close()

    # ---------- DESKTOP (1440px) ----------
    ctx3 = browser.new_context(viewport={'width': 1440, 'height': 950})
    p3 = ctx3.new_page()
    p3.goto(f'file://{R}/gen1.html')
    p3.wait_for_timeout(1500)
    b3 = lambda s: p3.query_selector(s).bounding_box()
    check('desktop: three columns (list | settings/card/status | detail)',
          b3('#listPane')['x'] < b3('#gameCfg')['x'] < b3('#detailPane')['x'])
    check('desktop: settings, card, status stacked in middle column',
          abs(b3('#gameCfg')['x'] - b3('.sprCard')['x']) < 4 and
          abs(b3('.sprCard')['x'] - b3('.cntBox')['x']) < 4 and
          b3('#gameCfg')['y'] < b3('.sprCard')['y'] < b3('.cntBox')['y'])
    check('desktop: detail pane top aligns with list',
          abs(b3('#detailPane')['y'] - b3('#listPane')['y']) < 4)
    check('desktop: bilingual name present too',
          p3.evaluate("!!document.querySelector('#sprName .altName')"))
    p3.screenshot(path=f'{SHOT}/desktop.png')
    ctx3.close()
    browser.close()

fails = [r for r in results if not r[1]]
print(f'\n{len(results) - len(fails)}/{len(results)} passed')
raise SystemExit(1 if fails else 0)
