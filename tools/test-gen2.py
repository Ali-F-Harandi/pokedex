#!/usr/bin/env python3
"""Pokédex Plus — Generation II merged page test: 3 themes (gold/silver/
crystal), sprite sets incl. shiny + animated, per-game dex texts, dark &
steel types, Gen-2 type chart, bilingual names, persistence. Run:
python3 tools/test-gen2.py (needs playwright)"""
import os
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT = '/tmp/gen2_shots'
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

        print('== gen2.html ==')
        page.goto(f'file://{R}/gen2.html')
        page.wait_for_timeout(1700)

        check('no console errors on load', not errors, '; '.join(errors[:3]))
        check('GOLD theme initially', page.evaluate("document.body.classList.contains('theme-gold')"))
        check('251 rows in list', page.evaluate("document.querySelectorAll('#list .row').length") == 251)
        chips = page.evaluate("[...document.querySelectorAll('#themeRow .tchip')].map(c=>c.dataset.th)")
        check('3 theme chips (gold silver crystal)', chips == ['gold', 'silver', 'crystal'], str(chips))
        check('GOLD+SILVER grouped with CRYSTAL separate',
              page.evaluate("document.querySelectorAll('#themeRow .gcGroup').length") == 2)
        check('default sel is a Gen-2 starter (#155 Chikorita)',
              page.evaluate("state.sel") == 155)
        check('bilingual name: FA under EN in card',
              page.evaluate("document.querySelector('#sprName .altName') && document.querySelector('#sprName .altName').textContent.length > 0"))

        # --- dex text selector: GOLD -> SILVER -> CRYSTAL
        g_text = page.evaluate("document.querySelector('#flavorBox').textContent")
        page.click('#detailPane [data-txt="s"]')
        s_text = page.evaluate("document.querySelector('#flavorBox').textContent")
        check('SILVER text differs from GOLD text', g_text != s_text)
        page.click('#detailPane [data-txt="c"]')
        c_text = page.evaluate("document.querySelector('#flavorBox').textContent")
        check('CRYSTAL text differs from GOLD text', c_text != g_text)
        check('3 text buttons (G/S/C)', page.evaluate("document.querySelectorAll('#detailPane .vbtn').length") == 3)

        # --- dark & steel types present (chips + a Dark-type mon)
        chips_n = page.evaluate("document.querySelectorAll('#typeRow .chip').length")
        check('17 type chips (dark + steel included)', chips_n == 17, str(chips_n))
        page.evaluate("select(197)")   # Umbreon — Dark
        page.wait_for_timeout(150)
        check('Umbreon shows a DARK badge',
              page.evaluate("document.querySelector('#sprTypes .tbadge').classList.contains('T-dark')"))
        page.evaluate("select(208)")   # Steelix — Steel
        page.wait_for_timeout(150)
        check('Steelix shows a STEEL badge',
              page.evaluate("[...document.querySelectorAll('#sprTypes .tbadge')].some(b=>b.classList.contains('T-steel'))"))

        # --- Gen-2 type mechanics: Poison immune vs Steel (Gen-2 rule)
        wk = page.evaluate("(function(){ const out=document.querySelector('#detailPane').textContent; return out; })()")
        check('Steelix immune to Poison (authentic Gen-2 chart)',
              'مصون' in wk or 'Immune' in wk)

        # --- SILVER theme: own sprites
        page.click('#themeRow [data-th="silver"]')
        page.wait_for_timeout(200)
        check('SILVER theme applied', page.evaluate("document.body.classList.contains('theme-silver')"))
        check('SILVER sprite bank active',
              page.evaluate("document.querySelector('#sprImg').src").find('gen2-silver') is not None)
        # an EXPLICIT text choice (we clicked CRYSTAL earlier) is remembered
        # across games — the gen1 pattern
        check('explicit text choice persists across themes',
              page.evaluate("document.querySelector('#detailPane [data-txt=c]').classList.contains('on')"))
        # …but a fresh visitor gets each game's own wording
        fresh_ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
        fresh = fresh_ctx.new_page()
        fresh.goto(f'file://{R}/gen2.html')
        fresh.wait_for_timeout(1500)
        fresh.click('#themeRow [data-th="silver"]')
        fresh.wait_for_timeout(250)
        check('fresh visitor: SILVER theme opens on SILVER text',
              fresh.evaluate("document.querySelector('#detailPane [data-txt=s]').classList.contains('on')"))
        fresh_ctx.close()

        # --- CRYSTAL theme: own sprites + ANIM
        page.click('#themeRow [data-th="crystal"]')
        page.wait_for_timeout(200)
        check('CRYSTAL theme applied', page.evaluate("document.body.classList.contains('theme-crystal')"))
        check('CRYSTAL sprite bank active',
              page.evaluate("document.querySelector('#sprImg').src").find('gen2-crystal') is not None)
        check('CRYSTAL text selected by default',
              page.evaluate("document.querySelector('#detailPane [data-txt=c]').classList.contains('on')"))

        # --- Gen-2 phase 3: CRYSTAL gets its own move data (label + Move Tutor)
        mv_lbl = page.evaluate("(document.querySelector('.mv-game')||{textContent:''}).textContent")
        check('moves label follows theme to CRYSTAL', mv_lbl == 'CRYSTAL', str(mv_lbl))
        page.evaluate("select(155)")   # Cyndaquil learns Flamethrower from Crystal's tutor
        page.wait_for_timeout(200)
        tabs = page.evaluate("[...document.querySelectorAll('#movesSec .mtab')].map(b=>b.dataset.mt)")
        check('Crystal: Cyndaquil gains the TUTOR tab', 'tutor' in tabs, str(tabs))
        page.click('#movesSec [data-mt=tutor]')
        page.wait_for_timeout(150)
        tr = page.evaluate("[...document.querySelectorAll('#movesSec .mrow .mv-en')].map(b=>b.textContent.trim())")
        check('Cyndaquil\'s Crystal tutor move is Flamethrower',
              len(tr) == 1 and tr[0] == 'FLAMETHROWER', str(tr))

        check('ANIM chip visible on Crystal',
              page.evaluate("document.querySelector('#chipAnim') !== null"))
        page.click('#chipAnim')
        page.wait_for_timeout(250)
        src = page.evaluate("document.querySelector('#sprImg').src")
        check('animated webp loaded (gen2-crystal-anim)', src.find('gen2-crystal-anim') is not None and src.endswith('.webp'), src[-42:])
        page.screenshot(path=f'{SHOT}/crystal-anim.png')

        # shiny on crystal: static shiny (anim yields to shiny)
        page.click('#chipShiny')
        page.wait_for_timeout(200)
        check('SHINY takes over the front view (static shiny png)',
              page.evaluate("document.querySelector('#sprImg').src").find('-shiny/') is not None)
        # back view with shiny
        page.click('#btnBack')
        page.wait_for_timeout(200)
        check('back view uses back-shiny bank',
              page.evaluate("document.querySelector('#sprImg').src").find('-back-shiny/') is not None)
        page.click('#btnBack')   # front again
        page.wait_for_timeout(150)
        page.click('#chipShiny')  # shiny off
        page.wait_for_timeout(150)

        # --- GOLD theme: no ANIM chip (crystal-only), anim auto-off
        page.click('#themeRow [data-th="gold"]')
        page.wait_for_timeout(200)
        check('GOLD theme applied', page.evaluate("document.body.classList.contains('theme-gold')"))
        check('no ANIM chip outside Crystal',
              page.evaluate("document.querySelector('#chipAnim') === null"))
        check('card ANIM button disabled outside Crystal',
              page.evaluate("document.querySelector('#btnAnim').disabled === true"))
        check('GOLD sprite bank active',
              page.evaluate("document.querySelector('#sprImg').src").find('gen2-gold') is not None)

        # --- shiny on gold set (Gen 2 introduced shinies)
        page.click('#btnShiny')
        page.wait_for_timeout(200)
        check('shiny sprites on the gold set',
              page.evaluate("document.querySelector('#sprImg').src").find('gen2-gold-shiny') is not None)
        page.click('#btnShiny')
        page.wait_for_timeout(150)

        # --- MOVES (Gen-2 phase 3): per-game learnsets wired to the theme
        page.evaluate("select(155)")   # Cyndaquil
        page.wait_for_timeout(200)
        mv_lbl = page.evaluate("(document.querySelector('.mv-game')||{textContent:''}).textContent")
        check('MOVES section on gen2.html shows GOLD/SILVER', mv_lbl == 'GOLD/SILVER', str(mv_lbl))
        tabs = page.evaluate("[...document.querySelectorAll('#movesSec .mtab')].map(b=>b.dataset.mt)")
        check('G/S: no tutor tab (Gold/Silver had no Move Tutor)',
              'tutor' not in tabs, str(tabs))

        # data: learnsets for all 251 per game; every move bilingual (FA name + FA description)
        md_bad = page.evaluate("""(function(){
          const bad=[];
          [MD_GS, MD_CRYSTAL].forEach(function(M){
            if (Object.keys(M.learn).length !== 251) bad.push(M.game + ':learn=' + Object.keys(M.learn).length);
            Object.keys(M.moves).forEach(function(id){
              const s = M.moves[id][0], inf = MOVE_INFO[s];
              if (!inf) { bad.push(M.game + ':noinfo:' + s); return; }
              if (!inf[0]) bad.push('noEN:' + s);
              if (!inf[1] || !/[\\u0600-\\u06FF]/.test(inf[1])) bad.push('noFAname:' + s);
              if (!inf[3] || !/[\\u0600-\\u06FF]/.test(inf[3])) bad.push('noFAdesc:' + s);
            });
          });
          return bad; })()""")
        check('251 learnsets per game + every move bilingual (FA name + FA description)',
              not md_bad, '; '.join(md_bad[:4]))

        # data: Crystal move tutor = Flamethrower / Thunderbolt / Ice Beam; none in G/S
        tutor = page.evaluate("""(function(){
          const ids=[53,58,85];
          const names=ids.map(function(i){ return MD_GS.moves[i][0]; }).sort().join(',');
          const gsT=Object.keys(MD_GS.learn).filter(function(p){ return MD_GS.learn[p].tutor.length > 0; }).length;
          const crT=Object.keys(MD_CRYSTAL.learn).filter(function(p){ return MD_CRYSTAL.learn[p].tutor.length > 0; }).length;
          return { names: names, gsT: gsT, crT: crT }; })()""")
        check('Crystal tutor teaches Flamethrower/Ice Beam/Thunderbolt to 150+ mons, none in G/S',
              tutor['names'] == 'flamethrower,ice-beam,thunderbolt' and tutor['gsT'] == 0 and tutor['crT'] >= 150,
              str(tutor))

        # data: TM/HM machines — authentic (Crystal kept the Gold/Silver machines)
        mach = page.evaluate("""(function(){
          const a = JSON.stringify(MD_GS.tm) + JSON.stringify(MD_GS.hm);
          const b = JSON.stringify(MD_CRYSTAL.tm) + JSON.stringify(MD_CRYSTAL.hm);
          return { same: a === b, tm: Object.keys(MD_GS.tm).length, hm: Object.keys(MD_GS.hm).length }; })()""")
        check('TM/HM lists authentic and complete (50 TM + 7 HM, same in G/S and Crystal)',
              mach['same'] and mach['tm'] == 50 and mach['hm'] == 7, str(mach))

        # START menu entries + Moves Dex overlay (M shortcut)
        page.click('#startBtn')
        page.wait_for_timeout(250)
        acts = page.evaluate("[...document.querySelectorAll('#menuPop .m-item')].map(b=>b.dataset.act)")
        check('START menu has MOVES DEX + TM/HM entries',
              'movesdex' in acts and 'tmhm' in acts, str(acts))
        page.keyboard.press('Escape')
        page.wait_for_timeout(200)
        page.keyboard.press('m')
        page.wait_for_timeout(400)
        head = page.evaluate("(document.querySelector('#mvHeadT')||{textContent:''}).textContent")
        check('Moves Dex overlay shows GOLD/SILVER', 'GOLD/SILVER' in head, head)
        ov_n = page.evaluate("document.querySelectorAll('#movesWrap .mcard').length")
        check('Moves Dex overlay lists all 251 Gen-2 moves', ov_n == 251, f'cards={ov_n}')
        en_fa = page.evaluate("""(function(){
          const c = document.querySelector('#movesWrap .mcard');
          if (!c) return { en: false, fa: false };
          return { en: (c.querySelector('.mv-en')||{textContent:''}).textContent.length > 0,
                   fa: /[\\u0600-\\u06FF]/.test((c.querySelector('.mv-fa')||{textContent:''}).textContent) }; })()""")
        check('overlay move cards are bilingual (EN + FA names)', en_fa['en'] and en_fa['fa'], str(en_fa))
        page.screenshot(path=f'{SHOT}/movesdex.png')
        page.keyboard.press('Escape')
        page.wait_for_timeout(200)

        # --- evolution: Pichu -> Pikachu -> Raichu (Gen-2 baby chain)
        page.evaluate("select(172)")
        page.wait_for_timeout(200)
        evo_txt = page.evaluate("document.querySelector('#detailPane').textContent")
        check('Pichu evo chain shows Pikachu & Raichu', 'Pikachu' in evo_txt and 'Raichu' in evo_txt)
        check('Gen-2 happiness condition rendered',
              'Happiness' in evo_txt or 'شادی' in evo_txt)

        # --- LCD shader toggle
        page.click('#btnLcd')
        page.wait_for_timeout(150)
        check('LCD shader class applied', page.evaluate("document.body.classList.contains('lcd-on')"))
        page.click('#btnLcd')

        # --- persistence: reload keeps crystal theme + shiny
        page.click('#themeRow [data-th="crystal"]')
        page.click('#btnShiny')
        page.wait_for_timeout(200)
        page.reload()
        page.wait_for_timeout(1700)
        check('theme persists (crystal)', page.evaluate("document.body.classList.contains('theme-crystal')"))
        check('shiny persists', page.evaluate("state.shiny === true"))
        check('no console errors overall', not errors, '; '.join(errors[:4]))
        page.screenshot(path=f'{SHOT}/final.png')

        # --- FA mode
        page.click('#langBtn')
        page.wait_for_timeout(250)
        check('FA mode flips direction', page.evaluate("document.body.dir") == 'rtl')
        fa_chips = page.evaluate("[...document.querySelectorAll('#themeRow .tchip')].map(c=>c.textContent.trim())")
        check('FA theme labels in Persian', any('\u0600' <= c[0] <= '\u06FF' for c in fa_chips if c), str(fa_chips))
        fa_alt = page.evaluate("document.querySelector('#sprName .altName') && document.querySelector('#sprName .altName').textContent")
        check('FA card shows EN name under the FA name', fa_alt and fa_alt.isascii(), str(fa_alt))
        check('FA dark type label', page.evaluate("I18N.fa.types.dark") == 'تاریک')
        # FA moves (phase 3): section, rows and the move card all Persian
        fa_sec = page.evaluate("(document.querySelector('.mv-sec-title')||{textContent:''}).textContent")
        check('FA moves section title in Persian', 'حرکت' in fa_sec, fa_sec)
        fa_mv = page.evaluate("/[\\u0600-\\u06FF]/.test((document.querySelector('#movesSec .mrow .mv-fa')||{textContent:''}).textContent)")
        check('FA move names in Persian in the learnset', fa_mv)
        page.evaluate("document.querySelector('#movesSec .mrow').click()")
        page.wait_for_timeout(350)
        fa_desc = page.evaluate("/[\\u0600-\\u06FF]/.test((document.querySelector('#mvBody')||{textContent:''}).textContent)")
        check('FA move description in the move card', fa_desc)
        fa_menu = page.evaluate("[...document.querySelectorAll('.mv-menu-l')].map(s=>s.textContent)")
        check('FA START menu moves entries in Persian',
              len(fa_menu) == 2 and all('\u0600' <= s[0] <= '\u06FF' for s in fa_menu), str(fa_menu))
        page.keyboard.press('Escape')
        page.wait_for_timeout(150)
        page.screenshot(path=f'{SHOT}/fa.png')

        browser.close()

    fails = [r for r in results if not r[1]]
    print(f'\n{len(results) - len(fails)}/{len(results)} passed')
    return 1 if fails else 0


if __name__ == '__main__':
    raise SystemExit(run())
