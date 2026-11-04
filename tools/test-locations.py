#!/usr/bin/env python3
"""Pokédex Plus — Phase 4 browser test: Location Dex + HOW TO CATCH on gen1.html.
Run: python3 tools/test-locations.py (needs playwright)"""
import os
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT = '/tmp/loc_shots'
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

        print('== gen1.html — load ==')
        page.goto(f'file://{R}/gen1.html')
        page.wait_for_timeout(1800)
        check('loads clean', not errors, '; '.join(errors[:2]))
        check('START menu has Location Dex entry',
              page.evaluate("!!document.querySelector('#menuPop [data-act=locdex]')"))
        check('HOW TO CATCH section in detail pane',
              page.evaluate("!!document.querySelector('#locSec')"))
        check('section follows the active game (RED chip on)',
              page.evaluate("[...document.querySelectorAll('#locSec .lchip')].find(x=>x.dataset.lg==='red').classList.contains('on')"))

        # ---- wild rows for a wild Pokémon (Pikachu #25) ----
        page.evaluate("select(25)")
        page.wait_for_timeout(250)
        rows = page.evaluate("[...document.querySelectorAll('#locSec .lrow')].length")
        check('Pikachu has wild rows (R/B)', rows > 0, str(rows))

        # ---- Mewtwo: static only ----
        page.evaluate("select(150)")
        page.wait_for_timeout(250)
        body = page.evaluate("document.querySelector('#locSec').textContent")
        check('Mewtwo shows a FIXED encounter at Cerulean Cave',
              'CERULEAN CAVE' in body.upper() and '70' in body, body[:90].replace('\n', ' '))
        page.screenshot(path=f'{SHOT}/mewtwo-section.png')

        # ---- Magikarp: rods everywhere ----
        page.evaluate("select(129)")
        page.wait_for_timeout(250)
        body = page.evaluate("document.querySelector('#locSec').textContent")
        check('Magikarp has the Old-Rod-anywhere row', 'OLD ROD' in body)
        check('Magikarp also has wild Super-Rod rows', 'SUPER ROD' in body)

        # ---- Raichu in YELLOW: blocked note ----
        page.evaluate("select(26)")
        page.wait_for_timeout(200)
        page.evaluate("[...document.querySelectorAll('#locSec .lchip')].find(x=>x.dataset.lg==='yellow').click()")
        page.wait_for_timeout(250)
        body = page.evaluate("document.querySelector('#locSec').textContent")
        check('Raichu in Yellow = NOT IN THIS GAME', 'NOT IN THIS GAME' in body)
        check('Raichu in Yellow shows the Thunder-Stone note', 'refuses the Thunder Stone' in body)
        page.screenshot(path=f'{SHOT}/raichu-yellow.png')

        # ---- evolution path: Charizard in RED ----
        page.evaluate("select(6)")
        page.wait_for_timeout(200)
        page.evaluate("[...document.querySelectorAll('#locSec .lchip')].find(x=>x.dataset.lg==='red').click()")
        page.wait_for_timeout(250)
        check('Charizard gets a BY EVOLUTION block',
              page.evaluate("!!document.querySelector('#locSec .lc-evo')"))
        evo_txt = page.evaluate("document.querySelector('#locSec .lc-evo').textContent")
        check('evolution path starts at Charmander', 'CHARMANDER' in evo_txt.upper(), evo_txt[:60])
        check('evolution path mentions Lv 36', '36' in evo_txt)

        # ---- Location Dex overlay ----
        print('== Location Dex overlay ==')
        page.keyboard.press('l')
        page.wait_for_timeout(300)
        check('overlay opens with L key', page.evaluate("!document.querySelector('#locWrap').classList.contains('hidden')"))
        n = page.evaluate("document.querySelectorAll('.lcard').length")
        check('all 68 locations listed', n == 68, str(n))
        head = page.evaluate("document.querySelector('#lcHeadT').textContent")
        check('head shows the game', 'LOCATION DEX' in head and 'RED' in head, head)

        # search
        page.fill('#lcQ', 'cerulean cave')
        page.wait_for_timeout(250)
        n = page.evaluate("document.querySelectorAll('.lcard').length")
        check('search finds Cerulean Cave floors', n == 3, str(n))
        # FA search
        page.fill('#lcQ', 'غار سرولین')
        page.wait_for_timeout(250)
        n = page.evaluate("document.querySelectorAll('.lcard').length")
        check('FA search finds the same floors', n == 3, str(n))
        page.fill('#lcQ', '')
        page.wait_for_timeout(250)

        # open Route 1 detail
        page.evaluate("[...document.querySelectorAll('.lcard')].find(c=>c.dataset.loc==='Route1').click()")
        page.wait_for_timeout(250)
        body = page.evaluate("document.querySelector('#lcBody').textContent")
        check('Route 1 shows Pidgey ~50%', 'PIDGEY' in body.upper() and '50%' in body, body[:80].replace('\n', ' '))
        check('Route 1 shows Rattata', 'RATTATA' in body.upper())
        check('Route 1 shows the encounter rate', '25/255' in body)
        check('global Old/Good Rod note present', 'OLD ROD' in body and 'GOOD ROD' in body)
        page.screenshot(path=f'{SHOT}/route1-loc.png')

        # game switch inside the overlay (YELLOW)
        page.evaluate("[...document.querySelectorAll('.gchip')].find(x=>x.textContent.trim()==='YELLOW').click()")
        page.wait_for_timeout(250)
        body = page.evaluate("document.querySelector('#lcBody').textContent")
        check('Yellow Route 1 still Pidgey/Rattata', 'PIDGEY' in body.upper() and 'RATTATA' in body.upper())

        # species click jumps to the dex
        page.evaluate("document.querySelector('.lrow.mon').click()")
        page.wait_for_timeout(400)
        check('clicking a species closes the overlay',
              page.evaluate("document.querySelector('#locWrap').classList.contains('hidden')"))
        sel = page.evaluate("state.sel")
        check('dex selected that species', sel in (16, 19), str(sel))

        # ---- special location: Power Plant (Zapdos + Voltorb balls) ----
        page.keyboard.press('l')
        page.wait_for_timeout(300)
        page.evaluate("[...document.querySelectorAll('.gchip')].find(x=>x.textContent.trim()==='RED').click()")
        page.wait_for_timeout(200)
        page.evaluate("[...document.querySelectorAll('.lcard')].find(c=>c.dataset.loc==='PowerPlant').click()")
        page.wait_for_timeout(250)
        body = page.evaluate("document.querySelector('#lcBody').textContent")
        check('Power Plant lists Zapdos Lv 50', 'ZAPDOS' in body.upper() and '50' in body)
        check('Power Plant lists the Voltorb item-balls', 'VOLTORB' in body.upper() and '40' in body)
        page.screenshot(path=f'{SHOT}/powerplant-loc.png')

        # ---- Game Corner shows up under Celadon City ----
        page.evaluate("document.querySelector('#lcBack') && document.querySelector('#lcBack').click()")
        page.wait_for_timeout(200)
        page.evaluate("[...document.querySelectorAll('.lcard')].find(c=>c.dataset.loc==='CeladonCity').click()")
        page.wait_for_timeout(250)
        body = page.evaluate("document.querySelector('#lcBody').textContent")
        check('Celadon City shows Game Corner prizes', 'GAME CORNER' in body and 'PORYGON' in body.upper())
        check('Celadon City shows the Eevee gift', 'EEVEE' in body.upper())

        # ---- settings persistence: COLOR survives a version switch ----
        print('== settings persistence ==')
        page.keyboard.press('Escape')
        page.wait_for_timeout(200)
        page.evaluate("select(6)")   # Charizard
        page.wait_for_timeout(200)
        # switch to COLOR chips in RED
        page.evaluate("[...document.querySelectorAll('#setRow .setchip')].find(x=>x.textContent.trim().toLowerCase().includes('color')||x.classList.contains('setchip')&&x.dataset.set==='rbc')&&[...document.querySelectorAll('#setRow .setchip')].find(x=>x.dataset.set==='rbc').click()")
        page.wait_for_timeout(250)
        set1 = page.evaluate("state.set")
        check('picked COLOR set in RED (rbc)', set1 == 'rbc', set1)
        # switch theme to YELLOW
        page.evaluate("[...document.querySelectorAll('#themeRow .tchip')].find(x=>x.dataset.th==='yellow').click()")
        page.wait_for_timeout(350)
        set2 = page.evaluate("state.set")
        check('COLOR preference survives the switch to YELLOW (yc)', set2 == 'yc', set2)
        body = page.evaluate("document.querySelector('#locSec').textContent")
        check('HOW TO CATCH follows the new game', 'YELLOW' in page.evaluate("document.querySelector('#topbar .t1').textContent"))
        page.screenshot(path=f'{SHOT}/yellow-color.png')
        # reload → everything remembered
        page.reload()
        page.wait_for_timeout(1800)
        check('reload: still YELLOW theme', page.evaluate("state.theme") == 'yellow')
        check('reload: still COLOR set (yc)', page.evaluate("state.set") == 'yc')
        check('reload: last Pokémon remembered (Charizard)', page.evaluate("state.sel") == 6,
              str(page.evaluate("state.sel")))

        # ---- FA language ----
        print('== FA language ==')
        page.evaluate("toggleLang()")
        page.wait_for_timeout(400)
        check('body is RTL', page.evaluate("document.body.dir") == 'rtl')
        head = page.evaluate("document.querySelector('#lcHeadT') && document.querySelector('#lcHeadT').textContent")
        page.keyboard.press('l')
        page.wait_for_timeout(300)
        head = page.evaluate("document.querySelector('#lcHeadT').textContent")
        check('overlay head in FA', 'دکس مکان‌ها' in head, head)
        body = page.evaluate("document.querySelector('#lcBody').textContent")
        check('FA location names render (مسیر)', 'مسیر' in body or 'شهر' in body)
        check('FA numbers are Eastern Arabic', '۵' in body or '۱' in body)
        page.screenshot(path=f'{SHOT}/fa-list.png')
        # FA detail
        page.evaluate("[...document.querySelectorAll('.lcard')].find(c=>c.dataset.loc==='Route24').click()")
        page.wait_for_timeout(250)
        body = page.evaluate("document.querySelector('#lcBody').textContent")
        check('FA location view renders', 'مسیر ۲۴' in body, body[:60].replace('\n', ' '))
        page.screenshot(path=f'{SHOT}/fa-route24.png')
        page.keyboard.press('Escape')
        page.wait_for_timeout(150)
        sec = page.evaluate("document.querySelector('#locSec').textContent")
        check('FA section title', 'نحوه‌ی به‌دست‌آوردن' in sec)

        # back to EN, reset test state keys so the user's defaults stay clean
        page.evaluate("toggleLang()")
        page.evaluate("localStorage.removeItem('pkd_g1_color'); localStorage.removeItem('pkd_g1_sel'); localStorage.removeItem('pkd_g1_favonly'); localStorage.removeItem('pkd_g1_sort'); localStorage.removeItem('pkd_g1_text')")
        page.wait_for_timeout(200)

        # ---- console errors at the end ----
        check('no console errors during the whole run', not errors, '; '.join(errors[:3]))

        browser.close()

    fails = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(fails)}/{len(results)} passed")
    if fails:
        raise SystemExit(1)


if __name__ == '__main__':
    run()
