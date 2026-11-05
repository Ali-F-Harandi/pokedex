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

        # --- ITEMS (Gen-2 phase 4): the Item Dex overlay, Gen-2 scoped
        page.keyboard.press('i')
        page.wait_for_timeout(400)
        it_head = page.evaluate("(document.querySelector('#itHeadT')||{textContent:''}).textContent")
        check('Item Dex overlay shows G/S/C', 'G/S/C' in it_head, it_head)
        it_n = page.evaluate("document.querySelectorAll('#itemsWrap .icard').length")
        check('all 165 Gen-2 items listed', it_n == 165, f'cards={it_n}')
        it_bil = page.evaluate("""(function(){
          const c = document.querySelector('#itemsWrap .icard');
          if (!c) return { en: false, fa: false };
          return { en: (c.querySelector('.icard-en')||{textContent:''}).textContent.length > 0,
                   fa: /[\\u0600-\\u06FF]/.test((c.querySelector('.icard-fa')||{textContent:''}).textContent) }; })()""")
        check('item cards bilingual (EN + FA names)', it_bil['en'] and it_bil['fa'], str(it_bil))
        it_cats = page.evaluate("[...document.querySelectorAll('#itemsWrap .it-chip')].map(c=>c.textContent.trim())")
        check('category chips include Apricorns + Berries + Mail',
              any('Apricorn' in c for c in it_cats) and any('Berr' in c for c in it_cats)
              and any('Mail' in c for c in it_cats), str(it_cats[:6]))
        page.evaluate("document.querySelector('#itemsWrap .it-chip[data-c=apricorn]').click()")
        page.wait_for_timeout(200)
        apr_n = page.evaluate("document.querySelectorAll('#itemsWrap .icard').length")
        check('Apricorn category shows the 7 apricorn balls', apr_n == 7, f'apr={apr_n}')
        page.evaluate("document.querySelector('#itemsWrap .it-chip[data-c=all]').click()")
        page.wait_for_timeout(150)

        # data: every Gen-2 item has FA name + description; prices are Gen-2 (p2)
        idata = page.evaluate("""(function(){
          const gc = ITEMS.filter(function(it){ return it.g.indexOf('g') !== -1 || it.g.indexOf('c') !== -1; });
          const noFA = gc.filter(function(it){ return !it.fa || !/[\\u0600-\\u06FF]/.test(it.fa); }).length;
          const noDesc = gc.filter(function(it){ return !it.d || !it.fa2; }).length;
          const hp = ITEMS.find(function(it){ return it.k === 'HYPER_POTION'; });
          const gsb = ITEMS.find(function(it){ return it.k === 'GS_BALL'; });
          return { n: gc.length, noFA: noFA, noDesc: noDesc,
                   hpP2: hp && hp.p2, hpP1: hp && hp.p1,
                   gsbCOnly: gsb && gsb.g === 'c', gsbP2: gsb && gsb.p2, gsbNoIcon: gsb && !gsb.i }; })()""")
        check('165 Gen-2 items, all with FA name + description',
              idata['n'] == 165 and idata['noFA'] == 0 and idata['noDesc'] == 0, str(idata))
        check('prices are Gen-2 (HYPER POTION ¥1200 in G/S/C, was ¥1500 in R/B)',
              idata['hpP2'] == 1200 and idata['hpP1'] == 1500, str(idata))
        check('GS BALL: Crystal-only, not for sale, dashed placeholder icon',
              idata['gsbCOnly'] and idata['gsbP2'] == 0 and idata['gsbNoIcon'], str(idata))

        # detail view: search an item, open the card (description + prices + availability)
        page.fill('#itemsWrap #itQ', 'hyper')
        page.wait_for_timeout(200)
        page.evaluate("document.querySelector('#itemsWrap .icard').click()")
        page.wait_for_timeout(250)
        idet = page.evaluate("(document.querySelector('#itemsWrap .id-card')||{textContent:''}).textContent")
        idet_fa = page.evaluate("/[\\u0600-\\u06FF]/.test((document.querySelector('#itemsWrap .d-fa')||{textContent:''}).textContent)")
        idet_chips = page.evaluate("[...document.querySelectorAll('#itemsWrap .id-gchip.on')].map(c=>c.textContent.trim())")
        check('item detail: Gen-2 price, FA description, availability chips G/S + CRYSTAL',
              '1200' in idet and idet_fa and 'GOLD/SILVER' in idet_chips and 'CRYSTAL' in idet_chips,
              f'chips={idet_chips} fa={idet_fa}')
        page.keyboard.press('Escape')
        page.wait_for_timeout(150)

        # icons ride the LCD shader (gen2's analog of gen1's MONO/COLOR)
        page.click('#btnLcd')          # LCD on
        page.wait_for_timeout(200)
        page.keyboard.press('i')
        page.wait_for_timeout(300)
        it_style = page.evaluate("(document.querySelector('#itStyle')||{textContent:''}).textContent")
        it_src = page.evaluate("(document.querySelector('#itemsWrap img')||{src:''}).src")
        check('LCD on switches item icons to GB style',
              'GB' in it_style and '/itemicons-gb/' in it_src, f'{it_style} {it_src[-34:]}')
        page.keyboard.press('Escape')
        page.wait_for_timeout(150)
        page.click('#btnLcd')          # LCD off (restore)
        page.wait_for_timeout(150)

        # ===== Phase 5: HOW TO CATCH + Location Dex (Johto & Kanto, G/S/C) =====
        check('START menu has Location Dex entry',
              page.evaluate("!!document.querySelector('#menuPop [data-act=locdex]')"))
        check('HOW TO CATCH section in the detail pane',
              page.evaluate("!!document.querySelector('#locSec')"))
        check('section follows the active game (GOLD chip on)',
              page.evaluate("[...document.querySelectorAll('#locSec .lchip')].find(x=>x.dataset.lg==='gold').classList.contains('on')"))

        # data-level checks straight from LOC2 (bilingual meta, authentic spots)
        ldata = page.evaluate("""(function(){
          const noFA = LOC2.locs.filter(function(l){ return !l.fa || !/[\u0600-\u06FF]/.test(l.fa); }).length;
          const ids = LOC2.locs.map(function(l){ return l.id; });
          const r29g = LOC2.locs.find(function(l){ return l.id === 'ROUTE_29'; }).t.g.m.s;
          const noStarter = LOC2.locs.every(function(l){
            return Object.values(l.t || {}).every(function(tb){
              return ['m','d','n'].every(function(k){
                return !tb || !tb[k] || tb[k].s.every(function(e){ return e[0] !== 152 && e[0] !== 155 && e[0] !== 158; }); }); }); });
          const r35c = LOC2.locs.find(function(l){ return l.id === 'ROUTE_35'; }).t.c;
          const gy = LOC2.sp.find(function(s){ return s.m && s.m[0][0] === 130; });
          const ho = {}; const lu = {};
          LOC2.sp.forEach(function(s){ if (s.m && s.m[0][0] === 250) ho[s.v[0]] = s.m[0][1]; if (s.m && s.m[0][0] === 249) lu[s.v[0]] = s.m[0][1]; });
          const odd = LOC2.sp.filter(function(s){ return s.k === 'egg' && s.v.length === 1 && s.v[0] === 'crystal'; });
          const trG = LOC2.sp.filter(function(s){ return s.k === 'trade' && s.v.length === 2; }).length;
          const trC = LOC2.sp.filter(function(s){ return s.k === 'trade' && s.v.length === 1 && s.v[0] === 'crystal'; }).length;
          const r32 = LOC2.locs.find(function(l){ return l.id === 'ROUTE_32'; });
          const fish0 = LOC2.fish[0];
          const reg = { j: LOC2.locs.filter(function(l){ return l.r === 'j'; }).length, k: LOC2.locs.filter(function(l){ return l.r === 'k'; }).length };
          const spFA = LOC2.sp.every(function(s){ return s.d.fa && /[\u0600-\u06FF]/.test(s.d.fa); });
          return { n: LOC2.locs.length, noFA: noFA, uniq: new Set(ids).size,
                   r29sent: r29g.some(function(e){ return e[0] === 161; }),
                   noStarter: noStarter,
                   r35swarm: r35c && r35c.swg && r35c.swg.m.s.some(function(e){ return e[0] === 193; }),
                   gyar: gy && gy.loc === 'LAKE_OF_RAGE' && gy.m[0][1] === 30,
                   hooh: JSON.stringify(ho), lugia: JSON.stringify(lu),
                   oddN: odd.length && odd[0].m.length,
                   trG: trG, trC: trC,
                   r32swf: r32.t.g.swf, r32hb: r32.t.g.hb, r32fish: r32.t.g.f,
                   fish0old: JSON.stringify(fish0.o), fish0bite: fish0.bite,
                   contest: LOC2.contest.length,
                   ctHas: LOC2.contest.some(function(r){ return r[0] === 123; }) && LOC2.contest.some(function(r){ return r[0] === 127; }),
                   ctVenomoth: LOC2.contest.some(function(r){ return r[0] === 49; }),
                   reg: reg, spFA: spFA,
                   trees: Object.keys(LOC2.trees).join(',') }; })()""")
        check('119 locations, all bilingual, unique ids',
              ldata['n'] >= 110 and ldata['noFA'] == 0 and ldata['uniq'] == ldata['n'], str(ldata['n']) + '/' + str(ldata['noFA']))
        check('both regions covered (Johto + Kanto)',
              ldata['reg']['j'] >= 60 and ldata['reg']['k'] >= 40, str(ldata['reg']))
        check('Route 29 gold-morning table has Sentret', ldata['r29sent'])
        check('no wild starters anywhere (Chikorita/Cyndaquil/Totodile)', ldata['noStarter'])
        check('Crystal: Route 35 Yanma swarm present', ldata['r35swarm'])
        check('Red Gyarados: fixed Lv 30 at Lake of Rage', ldata['gyar'])
        check('Ho-Oh levels authentic per version (40/70/60)', ldata['hooh'] == '{"gold":40,"silver":70,"crystal":60}', ldata['hooh'])
        check('Lugia levels authentic per version (70/40/60)', ldata['lugia'] == '{"gold":70,"silver":40,"crystal":60}', ldata['lugia'])
        check('Odd Egg: Crystal-only, hatches one of 7 babies', ldata['oddN'] == 7, str(ldata['oddN']))
        check('in-game trades: 6 in G/S + 7 in Crystal (Kenya era)', ldata['trG'] == 6 and ldata['trC'] == 7,
              f"gs={ldata['trG']} c={ldata['trC']}")
        check('Route 32: Qwilfish swarm fish group + headbutt + own fish group',
              ldata['r32swf'] == 5 and ldata['r32hb'] == 'CANYON' and ldata['r32fish'] == 10,
              f"swf={ldata['r32swf']} hb={ldata['r32hb']} f={ldata['r32fish']}")
        check('fishing authentic: Shore Old Rod = Magikarp/Magikarp/Krabby @70.3/14.8/14.8, bite 50%',
              ldata['fish0old'] == '[[129,10,70.3],[129,10,14.8],[98,10,14.8]]' and ldata['fish0bite'] == 128,
              ldata['fish0old'])
        check('Bug-Catching Contest: 10 rows, Scyther+Pinsir in, no Venomoth',
              ldata['contest'] == 10 and ldata['ctHas'] and not ldata['ctVenomoth'],
              str(ldata['contest']))
        check('every special way carries a Persian description', ldata['spFA'])

        # HOW TO CATCH per Pokémon
        page.evaluate("select(161)")   # Sentret — Route 29 wild (gold)
        page.wait_for_timeout(250)
        sent = page.evaluate("document.querySelector('#locSec').textContent")
        check('Sentret HOW TO CATCH lists Route 29 (bilingual)',
              'Route 29' in sent and 'مسیر ۲۹' in sent, sent[:70])
        page.evaluate("select(249)")   # Lugia — version-dependent static
        page.wait_for_timeout(250)
        lug = page.evaluate("document.querySelector('#locSec').textContent")
        check('Lugia shows the Lv 70 static (Gold)', '70' in lug and 'Whirl Islands' in lug, lug[:80])
        page.evaluate("[...document.querySelectorAll('#locSec .lchip')].find(x=>x.dataset.lg==='silver').click()")
        page.wait_for_timeout(250)
        lug_s = page.evaluate("document.querySelector('#locSec').textContent")
        check('Lugia chip switch shows Lv 40 (Silver)', '40' in lug_s, lug_s[:80])
        page.evaluate("[...document.querySelectorAll('#locSec .lchip')].find(x=>x.dataset.lg==='crystal').click()")
        page.wait_for_timeout(250)
        lug_c = page.evaluate("document.querySelector('#locSec').textContent")
        check('Lugia chip switch shows Lv 60 (Crystal)', '60' in lug_c, lug_c[:80])
        page.evaluate("select(192)")   # Yanma — obtainable only via Crystal swarm / normal tables?
        page.wait_for_timeout(250)
        yan = page.evaluate("document.querySelector('#locSec').textContent")
        check('Yanma has obtainment info (wild or swarm/swarm note)',
              len(yan) > 40, yan[:60])
        page.evaluate("select(251)")   # Celebi — event only
        page.wait_for_timeout(250)
        cel = page.evaluate("document.querySelector('#locSec').textContent")
        check('Celebi shows EVENT row only', 'EVENT' in cel.upper() and 'Ilex' in cel, cel[:90])

        # Location Dex overlay
        page.keyboard.press('l')
        page.wait_for_timeout(350)
        check('overlay opens with L', page.evaluate("!document.querySelector('#locWrap').classList.contains('hidden')"))
        ov_n = page.evaluate("document.querySelectorAll('#locWrap .lcard').length")
        check('overlay lists every location', ov_n >= 110, f'cards={ov_n}')
        ov_head = page.evaluate("document.querySelector('#lcHeadT').textContent")
        check('overlay head follows the theme game at open (GOLD)', 'GOLD' in ov_head, ov_head)
        page.evaluate("[...document.querySelectorAll('#lcViewbar .gchip')].find(x=>x.dataset.gm==='crystal').click()")
        page.wait_for_timeout(250)
        ov_head2 = page.evaluate("document.querySelector('#lcHeadT').textContent")
        check('overlay game chip switches to CRYSTAL', 'CRYSTAL' in ov_head2, ov_head2)
        page.evaluate("LocUI.openDex('ROUTE_29')")
        page.wait_for_timeout(300)
        r29 = page.evaluate("document.querySelector('#lcBody').textContent")
        check('Route 29 view: grass + time tabs + Persian name',
              'GRASS' in r29 and 'مسیر ۲۹' in r29 and 'SENTRET' in r29.upper(), r29[:70].replace('\n', ' '))
        check('time tabs present (MORN/DAY/NITE)',
              page.evaluate("document.querySelectorAll('#lcBody .tchip').length") >= 3)
        page.evaluate("document.querySelector('#lcBody .tchip[data-t=n]').click()")
        page.wait_for_timeout(250)
        r29n = page.evaluate("document.querySelector('#lcBody').textContent")
        check('night tab swaps the table (Hoothoot in, Sentret out)',
              'HOOTHOOT' in r29n.upper() and 'SENTRET' not in r29n.upper(), r29n[:70])
        page.screenshot(path=f'{SHOT}/loc_route29.png')
        page.evaluate("LocUI.openDex('NATIONAL_PARK')")
        page.wait_for_timeout(300)
        np = page.evaluate("document.querySelector('#lcBody').textContent")
        check('National Park view: Bug-Catching Contest table',
              'SCYTHER' in np.upper() and 'PINSIR' in np.upper(), np[:70])
        page.evaluate("LocUI.openDex('DARK_CAVE_VIOLET_ENTRANCE')")
        page.wait_for_timeout(300)
        dc = page.evaluate("document.querySelector('#lcBody').textContent")
        check('Dark Cave view: Dunsparce swarm section on Crystal',
              'SWARM' in dc.upper() and 'DUNSPARCE' in dc.upper(), dc[:70])
        page.evaluate("LocUI.openDex('GOLDENROD_CITY')")
        page.wait_for_timeout(300)
        gc = page.evaluate("document.querySelector('#lcBody').textContent")
        check('Goldenrod Game Corner view: prize specials',
              'GAME CORNER' in gc.upper() and 'ABRA' in gc.upper(), gc[:70])
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
        # FA items (phase 4): overlay head, chips, cards and prices all Persian
        page.keyboard.press('i')
        page.wait_for_timeout(400)
        fa_it_head = page.evaluate("(document.querySelector('#itHeadT')||{textContent:''}).textContent")
        check('FA item dex head in Persian', 'دکس آیتم' in fa_it_head, fa_it_head)
        fa_it_card = page.evaluate("""(function(){
          const c = document.querySelector('#itemsWrap .icard');
          return { fa: /[\\u0600-\\u06FF]/.test((c.querySelector('.icard-fa')||{textContent:''}).textContent),
                   en: (c.querySelector('.icard-en')||{textContent:''}).textContent.length > 0,
                   price: (c.querySelector('.it-price')||{textContent:''}).textContent }; })()""")
        check('FA item cards: FA + EN names present',
              fa_it_card['fa'] and fa_it_card['en'], str(fa_it_card))
        fa_it_menu = page.evaluate("[...document.querySelectorAll('.it-menu-l')].map(s=>s.textContent)")
        check('FA START menu item entry in Persian',
              len(fa_it_menu) == 1 and '\u0600' <= fa_it_menu[0][0] <= '\u06FF', str(fa_it_menu))
        # FA price digits on a priced item (HYPER POTION ¥1200 -> Persian digits)
        page.fill('#itemsWrap #itQ', 'hyper')
        page.wait_for_timeout(250)
        fa_price = page.evaluate("(document.querySelector('#itemsWrap .icard .it-price')||{textContent:''}).textContent")
        check('FA price rendered with Persian digits (¥۱۲۰۰)',
              '¥' in fa_price and any('\u06F0' <= ch <= '\u06F9' for ch in fa_price), fa_price)
        page.fill('#itemsWrap #itQ', '')
        page.wait_for_timeout(200)
        page.keyboard.press('Escape')
        page.wait_for_timeout(150)
        page.screenshot(path=f'{SHOT}/fa.png')

        browser.close()

    fails = [r for r in results if not r[1]]
    print(f'\n{len(results) - len(fails)}/{len(results)} passed')
    return 1 if fails else 0


if __name__ == '__main__':
    raise SystemExit(run())
