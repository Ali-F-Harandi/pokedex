#!/usr/bin/env python3
"""Gen-2 phone order + landing page generation order checks."""
import os
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT = '/tmp/gen2_shots'
os.makedirs(SHOT, exist_ok=True)
results = []


def check(name, cond, extra=''):
    results.append((name, bool(cond), extra))
    print(f'  {"PASS" if cond else "FAIL"}  {name}  {extra}')


with sync_playwright() as pw:
    browser = pw.chromium.launch()

    # ---------- PHONE 390px ----------
    ctx = browser.new_context(viewport={'width': 390, 'height': 844})
    page = ctx.new_page()
    errors = []
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(f'file://{R}/gen2.html')
    page.wait_for_timeout(1700)
    check('phone: no console errors', not errors, '; '.join(errors[:3]))
    b = lambda s: page.query_selector(s).bounding_box()
    check('phone order: DEX STATUS → search → SETTINGS → card → details',
          b('.cntBox')['y'] < b('#listPane')['y'] < b('#gameCfg')['y'] < b('.sprCard')['y'] < b('#detailPane')['y'])
    page.screenshot(path=f'{SHOT}/phone-en.png', full_page=True)
    page.click('#langBtn')
    page.wait_for_timeout(300)
    page.screenshot(path=f'{SHOT}/phone-fa.png', full_page=True)
    ctx.close()

    # ---------- DESKTOP 1440px ----------
    ctx2 = browser.new_context(viewport={'width': 1440, 'height': 950})
    p2 = ctx2.new_page()
    p2.goto(f'file://{R}/gen2.html')
    p2.wait_for_timeout(1500)
    b2 = lambda s: p2.query_selector(s).bounding_box()
    check('desktop: three columns (list | settings/card/status | detail)',
          b2('#listPane')['x'] < b2('#gameCfg')['x'] < b2('#detailPane')['x'])
    check('desktop: card + status stacked under settings in middle column',
          abs(b2('#gameCfg')['x'] - b2('.sprCard')['x']) < 4 and
          b2('#gameCfg')['y'] < b2('.sprCard')['y'] < b2('.cntBox')['y'])
    p2.screenshot(path=f'{SHOT}/desktop.png')
    ctx2.close()

    # ---------- LANDING ----------
    ctx3 = browser.new_context(viewport={'width': 1280, 'height': 900})
    p3 = ctx3.new_page()
    err3 = []
    p3.on('pageerror', lambda e: err3.append(str(e)))
    p3.goto(f'file://{R}/index.html')
    p3.wait_for_timeout(900)
    check('landing: no JS errors', not err3)
    cards = p3.evaluate("[...document.querySelectorAll('.featured .fcard .playbtn')].map(a=>a.getAttribute('href'))")
    check('featured order: gen1 → gen2 → emerald', cards == ['gen1.html', 'gen2.html', 'emerald.html'], str(cards))
    gens = p3.evaluate("[...document.querySelectorAll('#gens .card.active')].map(a=>a.getAttribute('href'))")
    check('catalog active cards: gen1, gen2, emerald', gens == ['gen1.html', 'gen2.html', 'emerald.html'], str(gens))
    gen_order = p3.evaluate("[...document.querySelectorAll('#gens .sec-h .st')].map(x=>x.textContent.trim())")
    check('catalog sections ordered GEN 1..9', all(f'GENERATION {i}' in gen_order[i-1] for i in range(1, 10)), str(gen_order[:3]))
    p3.screenshot(path=f'{SHOT}/landing.png')
    p3.click('#langBtn')
    p3.wait_for_timeout(400)
    fa_h2 = p3.evaluate("[...document.querySelectorAll('.featured h2')].map(x=>x.textContent)")
    check('landing FA: featured titles in Persian', any('\u0600' <= c[0] <= '\u06FF' for c in fa_h2 if c), str(fa_h2))
    p3.screenshot(path=f'{SHOT}/landing-fa.png')
    ctx3.close()
    browser.close()

fails = [r for r in results if not r[1]]
print(f'\n{len(results) - len(fails)}/{len(results)} passed')
raise SystemExit(1 if fails else 0)
