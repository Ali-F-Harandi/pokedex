#!/usr/bin/env python3
"""Gen-3 phase-1 test suite: the unified gen3.html dex.
Covers: no console errors, 386 count, 5 themes (repaint + sprite bank +
dex-text wording + label), Deoxys per-game formes (#386 stats/sprite),
wording selector (R/S · EMERALD · FRLG + Sapphire/LeafGreen where they
differ), FA pass (RTL, Persian digits, .altName), persistence (pkd_g3_*),
mobile reading order + full-width panels, emerald.html redirect, landing
card + catalog links."""
import json, os
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT = '/tmp/gen3_qa'
os.makedirs(SHOT, exist_ok=True)
results = []


def check(name, cond, extra=''):
    results.append((name, bool(cond), extra))
    print(f'  {"PASS" if cond else "FAIL"}  {name}  {extra}')


def seed(pg, lang='en', theme='ruby'):
    pg.add_init_script(f"""
        localStorage.setItem('pkd_lang', JSON.stringify('{lang}'));
        localStorage.setItem('pkd_g3_theme', JSON.stringify('{theme}'));
        localStorage.setItem('pkd_g3_seen', JSON.stringify([]));
        localStorage.setItem('pkd_g3_text', JSON.stringify(''));
    """)


def fresh(pg, url):
    """Force a REAL document load: init scripts (localStorage seeding) only
    run on document creation — a fragment-only goto keeps the same document."""
    pg.goto('about:blank')
    pg.goto(url)


with sync_playwright() as pw:
    browser = pw.chromium.launch()

    # ---------- desktop, EN ----------
    ctx = browser.new_context(viewport={'width': 1440, 'height': 950})
    page = ctx.new_page()
    errors = []
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: errors.append(str(e)))
    seed(page)
    page.goto(f'file://{R}/gen3.html')
    page.wait_for_timeout(1800)

    check('desktop: no console errors', not errors, '; '.join(errors[:3]))
    check('desktop: 386 rows', page.evaluate('DATA.length') == 386)
    check('desktop: all 386 have EN+FA names', page.evaluate('DATA.every(p=>p.display&&p.fa)'))
    check('desktop: default theme ruby, label RUBY',
          page.evaluate('state.theme') == 'ruby' and 'RUBY VERSION' in page.text_content('#brandSub'))
    check('desktop: default sel follows deep link / 252', page.evaluate('state.sel') in (252, 1))

    # theme chips: 3 cartridge groups, 5 chips
    chips = page.eval_on_selector_all('#themeRow .tchip', 'els=>els.map(e=>e.dataset.th)')
    check('theme chips: 5 in 3 groups', chips == ['ruby', 'sapphire', 'emerald', 'firered', 'leafgreen'], str(chips))

    # theme swap: class + sprite bank + wording + label + set
    page.click('.tchip[data-th=emerald]')
    page.wait_for_timeout(250)
    check('theme emerald: body class', page.evaluate('document.body.classList.contains("theme-emerald")'))
    check('theme emerald: sprite bank em', page.evaluate('state.set') == 'em')
    check('theme emerald: wording em', page.evaluate('effText(PMAP[state.sel])') == 'em')
    check('theme emerald: EMERALD VERSION label', 'EMERALD VERSION' in page.text_content('#brandSub'))
    img_em = page.get_attribute('#sprImg', 'src')
    check('theme emerald: sprite from emerald bank', 'gen3-emerald/' in img_em, img_em)
    page.screenshot(path=f'{SHOT}/desktop-emerald.png')

    page.click('.tchip[data-th=firered]')
    page.wait_for_timeout(250)
    img_fr = page.get_attribute('#sprImg', 'src')
    check('theme firered: sprite from frlg bank', 'gen3-frlg/' in img_fr, img_fr)
    check('theme firered: wording fr', page.evaluate('effText(PMAP[state.sel])') == 'fr')
    page.click('.tchip[data-th=leafgreen]')
    page.wait_for_timeout(250)
    check('theme leafgreen: wording stays frlg group', page.evaluate('effText(PMAP[state.sel])') in ('fr', 'lg'))
    page.click('.tchip[data-th=sapphire]')
    page.wait_for_timeout(250)
    check('theme sapphire: rs bank', page.evaluate('state.set') == 'rs')

    # ---------- Deoxys per-cartridge formes ----------
    page.evaluate('select(386, {scroll:false})')
    page.wait_for_timeout(200)
    stats = lambda: page.evaluate('JSON.stringify(statsOf(PMAP[386]))')
    page.click('.tchip[data-th=sapphire]'); page.wait_for_timeout(200)
    check('deoxys R/S: Normal 50/150/50/150/50/150',
          json.loads(stats()) == {'hp': 50, 'atk': 150, 'def': 50, 'spa': 150, 'spd': 50, 'spe': 150}, stats())
    src_rs = page.get_attribute('#sprImg', 'src')
    check('deoxys R/S: normal sprite 386', src_rs.endswith('gen3-rs/386.png'), src_rs)
    page.click('.tchip[data-th=emerald]'); page.wait_for_timeout(200)
    check('deoxys EMERALD: Speed 50/95/90/95/90/180',
          json.loads(stats()) == {'hp': 50, 'atk': 95, 'def': 90, 'spa': 95, 'spd': 90, 'spe': 180}, stats())
    src_em = page.get_attribute('#sprImg', 'src')
    check('deoxys EMERALD: speed sprite (forme id 10015)', 'gen3-emerald/10015.png' in src_em, src_em)
    page.click('.tchip[data-th=firered]'); page.wait_for_timeout(200)
    check('deoxys FIRERED: Attack 50/180/20/180/20/150',
          json.loads(stats()) == {'hp': 50, 'atk': 180, 'def': 20, 'spa': 180, 'spd': 20, 'spe': 150}, stats())
    src_fr = page.get_attribute('#sprImg', 'src')
    check('deoxys FIRERED: attack sprite 10013 in frlg bank', 'gen3-frlg/10013.png' in src_fr, src_fr)
    page.click('.tchip[data-th=leafgreen]'); page.wait_for_timeout(200)
    check('deoxys LEAFGREEN: Defense 50/70/160/70/160/90',
          json.loads(stats()) == {'hp': 50, 'atk': 70, 'def': 160, 'spa': 70, 'spd': 160, 'spe': 90}, stats())
    src_lg = page.get_attribute('#sprImg', 'src')
    check('deoxys LEAFGREEN: defense sprite 10014 in frlg bank', 'gen3-frlg/10014.png' in src_lg, src_lg)
    total_by_theme = page.evaluate('total(PMAP[386])')
    check('deoxys total follows forme (600 on lg)', total_by_theme == 600, str(total_by_theme))
    page.screenshot(path=f'{SHOT}/desktop-deoxys-lg.png')

    # ---------- abilities: era slots, no hidden ----------
    page.evaluate('select(252, {scroll:false})')
    page.wait_for_timeout(200)
    check('abilities: treecko has only overgrow (era)', page.evaluate('JSON.stringify(PMAP[252].abilities)') == '["overgrow"]')
    check('abilities: no hidden flag anywhere', page.evaluate('DATA.every(p=>p.abilities.every(a=>typeof a==="string"))'))
    ERA_ABILITIES = {"air-lock","arena-trap","battle-armor","blaze","chlorophyll","clear-body","cloud-nine","color-change","compound-eyes","cute-charm","damp","drizzle","drought","early-bird","effect-spore","flame-body","flash-fire","forecast","guts","huge-power","hustle","hyper-cutter","illuminate","immunity","inner-focus","insomnia","intimidate","keen-eye","levitate","lightning-rod","limber","liquid-ooze","magma-armor","magnet-pull","marvel-scale","minus","natural-cure","oblivious","overgrow","own-tempo","pickup","plus","poison-point","pressure","pure-power","rain-dish","rock-head","rough-skin","run-away","sand-stream","sand-veil","serene-grace","shadow-tag","shed-skin","shell-armor","shield-dust","soundproof","speed-boost","static","stench","sticky-hold","sturdy","suction-cups","swarm","swift-swim","synchronize","thick-fat","torrent","trace","truant","vital-spirit","volt-absorb","water-absorb","water-veil","white-smoke","wonder-guard"}
    era_js = json.dumps(sorted(ERA_ABILITIES))
    off = page.evaluate(f'(()=>{{ const era=new Set({era_js}); const bad=new Set(); DATA.forEach(p=>p.abilities.forEach(x=>{{ if(!era.has(x)) bad.add(x); }})); return JSON.stringify([...bad]); }})()')
    check('abilities: every slot is a pokeemerald-defined ability', off == '[]', off)
    ab_chips = page.eval_on_selector_all('#detailPane .abchip', 'els=>els.map(e=>e.textContent.trim())')
    check('abilities: chips render (treecko=Overgrow)', ab_chips == ['Overgrow'], str(ab_chips))

    # ---------- wording selector ----------
    page.evaluate('select(25, {scroll:false})')  # pikachu: fr != lg, s vs r?
    page.wait_for_timeout(200)
    btns = page.eval_on_selector_all('#detailPane .verSel .vbtn', 'els=>els.map(e=>e.textContent)')
    check('wording: pikachu shows per-game FR/LG buttons', 'FIRERED' in btns and 'LEAFGREEN' in btns, str(btns))
    check('wording: emerald button always present', 'EMERALD' in btns)
    page.click('#detailPane .verSel .vbtn[data-txt=em]')
    page.wait_for_timeout(200)
    check('wording: switch to Emerald repaints text', page.evaluate('effText(PMAP[state.sel])') == 'em')
    page.click('#detailPane .verSel .vbtn[data-txt=lg]')
    page.wait_for_timeout(200)
    check('wording: switch to LeafGreen', page.evaluate('effText(PMAP[state.sel])') == 'lg')

    # sapphire gets its own button where texts differ
    has_s = page.evaluate('DATA.filter(p=>p.ts).length')
    check('wording: some mons have distinct sapphire texts', has_s > 150, str(has_s))
    has_lg = page.evaluate('DATA.filter(p=>p.tlg).length')
    check('wording: some mons have distinct leafgreen texts', has_lg > 150, str(has_lg))

    # ---------- cries + sprites exist on disk ----------
    missing = []
    for i in list(range(1, 387)):
        if not os.path.exists(f'{R}/assets/audio/cries/{i}.ogg'):
            missing.append(i)
    check('cries: 1..386 all present', not missing, str(missing[:6]))
    banks = ['gen3-rs', 'gen3-rs-shiny', 'gen3-rs-back', 'gen3-rs-back-shiny',
             'gen3-frlg', 'gen3-frlg-shiny', 'gen3-frlg-back', 'gen3-frlg-back-shiny',
             'gen3-emerald', 'gen3-emerald-shiny']
    gaps = {b: [i for i in range(1, 387) if not os.path.exists(f'{R}/assets/sprites/{b}/{i}.png')] for b in banks}
    check('sprites: 10 banks complete (1..386)', all(not v for v in gaps.values()),
          str({k: v[:3] for k, v in gaps.items() if v}))

    # ---------- FA pass ----------
    seed(page, lang='fa', theme='emerald')
    fresh(page, f'file://{R}/gen3.html#025')
    page.wait_for_timeout(1500)
    check('FA: body rtl + .fa', page.evaluate('document.body.dir') == 'rtl' and page.evaluate('document.body.classList.contains("fa")'))
    main_fa = page.evaluate("document.querySelector('#sprName bdi').textContent")
    check('FA: main name is Persian', main_fa == 'پیکاچو', main_fa)
    alt_fa = page.evaluate("document.querySelector('#sprName .altName bdi') && document.querySelector('#sprName .altName bdi').textContent")
    check('FA: alt name is English', alt_fa == 'Pikachu', str(alt_fa))
    check('FA: dex text is Persian (emerald wording)', any('\u0600' <= c <= '\u06FF' for c in page.text_content('#flavorBox')))
    cnt = page.text_content('#cntRows')
    check('FA: persian digits in dex status', any('\u06F0' <= c <= '\u06F9' for c in cnt), cnt)
    page.screenshot(path=f'{SHOT}/desktop-fa.png')

    # FA rs wording: Persian
    page.click('.tchip[data-th=ruby]')
    page.wait_for_timeout(300)
    check('FA: rs wording also Persian', any('\u0600' <= c <= '\u06FF' for c in page.text_content('#flavorBox')))
    # frlg wording: Persian since phase 2 (fa_frlg follows the FireRed wording)
    page.click('.tchip[data-th=firered]')
    page.wait_for_timeout(300)
    fr_text = page.text_content('#flavorBox')
    check('FA: frlg wording is Persian (fa_frlg)', fr_text and any('\u0600' <= c <= '\u06FF' for c in fr_text), (fr_text or '')[:60])
    # FA leafgreen wording group: still the same FA group text (fa_rs pattern)
    page.click('.tchip[data-th=leafgreen]')
    page.wait_for_timeout(300)
    lg_text = page.text_content('#flavorBox')
    check('FA: leafgreen wording is Persian too', lg_text and any('\u0600' <= c <= '\u06FF' for c in lg_text), (lg_text or '')[:60])

    # Deoxys on the EMERALD chip must never show the NORMAL-forme animation —
    # animURL() returns "" for it, so the era Speed-forme still renders.
    page.click('.tchip[data-th=emerald]')
    page.wait_for_timeout(300)
    page.evaluate("select(386,{scroll:false})")
    page.evaluate("if(!state.anim) toggleAnim()")
    page.wait_for_timeout(400)
    src386 = page.evaluate("document.querySelector('#sprImg').getAttribute('src')")
    check('Deoxys EMERALD anim-guard: still, not wrong-forme webp',
          src386 and 'gen3-emerald-anim' not in src386 and 'gen3-emerald/10015.png' in src386, str(src386))
    # and SHINY on EMERALD resolves to the genuine speed-forme shiny view
    page.evaluate("if(!state.shiny) toggleShiny()")
    page.wait_for_timeout(300)
    src386s = page.evaluate("document.querySelector('#sprImg').getAttribute('src')")
    check('Deoxys EMERALD shiny: speed-forme shiny still',
          src386s and 'gen3-emerald-shiny/10015.png' in src386s, str(src386s))
    page.evaluate("if(state.shiny) toggleShiny()")

    # ---------- persistence ----------
    seed(page, lang='en', theme='leafgreen')
    fresh(page, f'file://{R}/gen3.html')
    page.wait_for_timeout(1400)
    page.evaluate("select(77,{scroll:false})")
    page.evaluate("toggleShiny()")
    page.reload()
    page.wait_for_timeout(1400)
    check('persistence: theme leafgreen', page.evaluate('state.theme') == 'leafgreen')
    check('persistence: last selection', page.evaluate('state.sel') == 77)
    check('persistence: shiny on', page.evaluate('state.shiny') == True)
    check('persistence: keys are pkd_g3_*', page.evaluate('JSON.stringify(Object.keys(localStorage).filter(k=>k.startsWith("pkd_g3_")).length) >= 4'))
    ctx.close()

    # ---------- mobile 390 ----------
    ctx2 = browser.new_context(viewport={'width': 390, 'height': 844})
    m = ctx2.new_page()
    merr = []
    m.on('console', lambda msg: merr.append(msg.text) if msg.type == 'error' else None)
    m.on('pageerror', lambda e: merr.append(str(e)))
    seed(m)
    m.goto(f'file://{R}/gen3.html')
    m.wait_for_timeout(1700)
    check('mobile: no console errors', not merr, '; '.join(merr[:3]))

    def box(sel):
        el = m.query_selector(sel)
        return el.bounding_box() if el else None
    check('mobile order: DEX STATUS first', box('.cntBox')['y'] < box('#listPane')['y'])
    check('mobile order: search box second', box('#listPane')['y'] < box('#gameCfg')['y'])
    check('mobile order: SETTINGS third', box('#gameCfg')['y'] < box('.sprCard')['y'])
    check('mobile order: Pokémon card fourth', box('.sprCard')['y'] < box('#detailPane')['y'])
    # full-width panels (the b0e9a15 lesson): every panel stretches to the
    # same width as the list column — never shrinks to fit-content
    vw = 390
    widths = {sel: box(sel)['width'] for sel in ('.cntBox', '#gameCfg', '.sprCard', '#listPane')}
    check('mobile width: all panels stretch (>300px @390)', all(w > 300 for w in widths.values()), str({k: round(v) for k, v in widths.items()}))
    check('mobile width: panels share one width (stretch, not fit-content)',
          max(widths.values()) - min(widths.values()) < 6, str({k: round(v) for k, v in widths.items()}))
    check('mobile: bilingual name present', m.evaluate("!!document.querySelector('#sprName .altName')"))
    m.screenshot(path=f'{SHOT}/mobile-en.png')
    ctx2.close()

    # ---------- emerald.html redirect ----------
    ctx3 = browser.new_context(viewport={'width': 1280, 'height': 900})
    r = ctx3.new_page()
    r.goto(f'file://{R}/emerald.html')
    r.wait_for_timeout(1700)
    check('emerald.html: redirects to gen3.html', r.url.endswith('gen3.html') or r.url.endswith('gen3.html#252'), r.url)
    check('emerald.html: gen3 dex live after redirect', r.evaluate('typeof DATA!=="undefined" && DATA.length===386'))

    # ---------- landing ----------
    r.goto(f'file://{R}/index.html')
    r.wait_for_timeout(900)
    cards = r.eval_on_selector_all('.featured .playbtn', 'els=>els.map(e=>e.getAttribute("href"))')
    check('landing: featured order gen1 → gen2 → gen3', cards == ['gen1.html', 'gen2.html', 'gen3.html'], str(cards))
    gens = r.eval_on_selector_all('#gens .card.active', 'els=>els.map(e=>e.getAttribute("href"))')
    check('landing: catalog active gen1, gen2, gen3', gens == ['gen1.html', 'gen2.html', 'gen3.html'], str(gens))
    h2s = r.eval_on_selector_all('.featured h2', 'els=>els.map(e=>e.textContent)')
    check('landing: gen3 card title', any('GENERATION III' in x and 'FIRERED' in x for x in h2s), str(h2s[2] if len(h2s) > 2 else ''))
    r.click('#langBtn')
    r.wait_for_timeout(400)
    fa_h2 = r.eval_on_selector_all('.featured h2', 'els=>els.map(e=>e.textContent)')
    check('landing FA: gen3 card in Persian', any('نسل سوم' in x for x in fa_h2), str(fa_h2[2] if len(fa_h2) > 2 else ''))
    r.screenshot(path=f'{SHOT}/landing-fa.png')

    # ==================== PHASE 3 — Moves Dex (R/S · EMERALD · FRLG) ====================
    mctx = browser.new_context(viewport={'width': 1440, 'height': 950})
    mp = mctx.new_page()
    merrs = []
    mp.on('console', lambda m: merrs.append(m.text) if m.type == 'error' else None)
    mp.on('pageerror', lambda e: merrs.append(str(e)))
    seed(mp, theme='ruby')
    mp.goto(f'file://{R}/gen3.html')
    mp.wait_for_timeout(1800)

    check('moves: scripts load (module + merged data + names)',
          mp.evaluate('typeof MovesUI!=="undefined" && typeof MD!=="undefined" && typeof MOVE_INFO!=="undefined" && typeof MD_RS!=="undefined" && typeof MD_EM!=="undefined" && typeof MD_FRLG!=="undefined"'))
    check('moves: no console errors with moves wired', not merrs, '; '.join(merrs[:3]))
    check('moves data: each game 354 moves / 386 learnsets / 50 TM + 8 HM',
          mp.evaluate('[MD_RS,MD_EM,MD_FRLG].every(d=>Object.keys(d.moves).length===354 && Object.keys(d.learn).length===386 && Object.keys(d.tm).length===50 && Object.keys(d.hm).length===8)'))
    check('moves data: every learnset row is a real move id',
          mp.evaluate('[MD_RS,MD_EM,MD_FRLG].every(d=>Object.values(d.learn).every(e=>e.lv.every(x=>d.moves[x[1]]) && e.tm.concat(e.egg,e.tutor).every(x=>d.moves[x])))'))
    check('moves data: every move has FA name + FA description (base or per-game)',
          mp.evaluate('[MD_RS,MD_EM,MD_FRLG].every(d=>Object.entries(d.moves).every(([id,r])=>{const bi=MOVE_INFO[r[0]];return bi && bi[1] && bi[3] && (!d.desc || !d.desc[id] || d.desc[id][1]);}))'))
    check('moves data: R/S has contests, Emerald has contests, FRLG has none (authentic)',
          mp.evaluate('Object.keys(MD_RS.contest).length===354 && Object.keys(MD_EM.contest).length===354 && MD_FRLG.contest===undefined'))
    check('moves data: R/S has NO tutors, Emerald + FRLG do',
          mp.evaluate('Object.values(MD_RS.learn).every(e=>e.tutor.length===0) && MD_EM.learn[25].tutor.length>0 && MD_FRLG.learn[25].tutor.length>0'))

    # START menu entries
    mp.click('#startBtn')
    mp.wait_for_timeout(300)
    check('moves: START menu has Moves Dex + TM/HM entries (EN)',
          mp.evaluate('[...document.querySelectorAll("#menuPop .m-item")].filter(b=>["movesdex","tmhm"].includes(b.dataset.act)).length===2')
          and 'Moves Dex' in mp.text_content('#menuPop'))
    mp.keyboard.press('Escape')

    # detail-pane section on default RUBY
    check('moves: detail section labels the cartridge (RUBY/SAPPHIRE)',
          mp.evaluate('document.querySelector("#movesSec .mv-game") && document.querySelector("#movesSec .mv-game").textContent.includes("RUBY/SAPPHIRE")'))
    check('moves: level-up rows render for the selected mon (Treecko)',
          mp.eval_on_selector_all('#movesSec .mrow', 'els=>els.length') > 0)
    check('moves: no TUTOR tab on R/S (the games had no tutors)',
          mp.evaluate('!document.querySelector("#movesSec .mtab[data-mt=tutor]")'))

    # overlay: 354 bilingual cards
    mp.evaluate('MovesUI.openDex("list")')
    mp.wait_for_timeout(400)
    check('moves: overlay lists 354 bilingual cards',
          mp.eval_on_selector_all('#movesBox .mcard', 'els=>els.length') == 354
          and mp.evaluate('(()=>{const c=document.querySelector("#movesBox .mcard");return c.querySelector(".mv-en") && c.querySelector(".mv-fa");})()'))
    check('moves: overlay is genuinely on screen (visible, covers the page)',
          mp.evaluate('(()=>{const w=document.getElementById("movesWrap");const r=w.getBoundingClientRect();const st=getComputedStyle(w);return !w.classList.contains("hidden") && st.display!=="none" && r.width>innerWidth*0.5 && r.height>innerHeight*0.5;})()'))
    # era type check: Gust (16) is FLYING in Gen 3 (NORMAL in Gen 1)
    mp.evaluate('MovesUI.openDex("detail", 16)')
    mp.wait_for_timeout(300)
    check('moves: era type — Gust badge FLYING (Gen-3 data)',
          mp.evaluate('document.querySelector("#movesBox .md-meta .tbadge").className.includes("T-flying")'))
    # contest on RUBY: Overheat (315) = BEAUTY ♥6; FRLG hides the contest cell
    mp.evaluate('MovesUI.openDex("detail", 315)')
    mp.wait_for_timeout(300)
    check('moves: RUBY contest — Overheat shows BEAUTY chip with appeal hearts',
          mp.evaluate('(()=>{const c=document.querySelector("#movesBox .md-contest .mv-contest");return c && c.className.includes("C1") && c.querySelectorAll(".mv-hearts")[0].textContent.length===6;})()'))
    check('moves: RUBY contest chip is bilingual-labelled',
          mp.evaluate('document.querySelector("#movesBox .md-contest .mv-contest").getAttribute("title")==="CONTEST"'))
    mp.keyboard.press('Escape')

    # TM/HM list: 58 machines, TM01 = Focus Punch, HM08 = Dive
    mp.evaluate('MovesUI.openDex("tmhm")')
    mp.wait_for_timeout(300)
    check('moves: TM/HM list — 50 TMs + 8 HMs, TM01=Focus Punch, HM08=Dive',
          mp.eval_on_selector_all('#movesBox .tmrow', 'els=>els.length') == 58
          and mp.evaluate('MD.tm[1]===264 && MD.hm[8]===291'))
    check('moves: R/S tutor note NOT shown in TM/HM view',
          mp.evaluate('!document.querySelector("#movesBox .mv-note")'))
    mp.keyboard.press('Escape')

    # per-game wording: FRLG Pound differs from the Emerald base; R/S shares it
    check('moves: FRLG wording differs, R/S Pound shares the Emerald base (7 era diffs stay per-game)',
          mp.evaluate('MD_FRLG.desc[1]!==undefined && MD_RS.desc[1]===undefined && MOVE_INFO["pound"][2]==="Pounds the foe with forelegs or tail." && Object.keys(MD_RS.desc).length===7'))

    # theme swap follows the cartridge
    mp.evaluate('toggleTheme("emerald")')
    mp.wait_for_timeout(500)
    check('moves: EMERALD chip swaps the moves data + shows tutor note',
          mp.evaluate('MD.label==="EMERALD"')
          and mp.evaluate('!!document.querySelector("#movesSec .mv-game")') and 'EMERALD' in mp.text_content('#movesSec .mv-game')
          and mp.evaluate('!!document.querySelector("#movesSec .mv-note")'))
    check('moves: EMERALD Pikachu gets a TUTOR tab (Battle Frontier tutors)',
          mp.evaluate('select(25), !!document.querySelector("#movesSec .mtab[data-mt=tutor]")'))
    mp.evaluate('toggleTheme("firered")')
    mp.wait_for_timeout(500)
    check('moves: FIRERED chip swaps to FIRERED/LEAFGREEN + hides contest',
          mp.evaluate('MD.label==="FIRERED/LEAFGREEN"')
          and mp.evaluate('MovesUI.openDex("detail",315), !document.querySelector("#movesBox .md-contest")'))
    check('moves: FRLG TM/HM view shows the Cape Brink tutor note',
          mp.evaluate('MovesUI.openDex("tmhm"), !!document.querySelector("#movesBox .mv-note")'))
    mp.keyboard.press('Escape')

    # ---------- moves FA pass ----------
    fa2 = browser.new_context(viewport={'width': 1440, 'height': 950})
    fp = fa2.new_page()
    seed(fp, lang='fa', theme='ruby')
    fp.goto(f'file://{R}/gen3.html')
    fp.wait_for_timeout(1600)
    check('moves FA: section title + game label in Persian UI',
          fp.evaluate('document.body.dir==="rtl" && !!document.querySelector("#movesSec .mv-sec-title")'))
    check('moves FA: level rows use Persian Lv digits',
          fp.evaluate('(()=>{const b=document.querySelector("#movesSec .mrow .mv-badge");return b && /[\u06F0-\u06F9]/.test(b.textContent);})()'))
    fp.evaluate('MovesUI.openDex("detail", 315)')
    fp.wait_for_timeout(300)
    check('moves FA: card shows Persian name + Persian description',
          fp.evaluate('(()=>{const n=document.querySelector("#movesBox .md-name .mv-fa");const d=document.querySelector("#movesBox .md-desc .d-fa");return n && /[\u0600-\u06FF]/.test(n.textContent) && d && /[\u0600-\u06FF]/.test(d.textContent);})()'))
    check('moves FA: contest chip Persian (زیبایی + Persian digit jam/none)',
          fp.evaluate('(()=>{const c=document.querySelector("#movesBox .md-contest .mv-contest");return c && c.textContent.includes("زیبایی") && c.textContent.includes("♥");})()'))
    fp.screenshot(path=f'{SHOT}/gen3-moves-fa.png')
    fa2.close()
    mp.screenshot(path=f'{SHOT}/gen3-moves-overlay-en.png')
    mctx.close()

    # ==================== PHASE 4 — Item Dex (R/S · EMERALD · FRLG) ====================
    ictx = browser.new_context(viewport={'width': 1440, 'height': 950})
    ip = ictx.new_page()
    ierr = []
    ip.on('console', lambda m: ierr.append(m.text) if m.type == 'error' else None)
    ip.on('pageerror', lambda e: ierr.append(str(e)))
    seed(ip, theme='ruby')
    ip.goto(f'file://{R}/gen3.html')
    ip.wait_for_timeout(1800)

    check('items: scripts load (module + data + config)',
          ip.evaluate('typeof ItemsUI!=="undefined" && typeof ITEMS!=="undefined" && typeof ITEM_CATS!=="undefined" && window.ITEM_DEX_CONFIG && window.ITEM_DEX_CONFIG.gen===3'))
    check('items: no console errors with items wired', not ierr, '; '.join(ierr[:3]))

    # counts per game (union and per-cartridge membership)
    check('items data: 248 items in the Gen-3 universe', ip.evaluate('ITEMS.length') == 248)
    check('items data: R/S 222 · EM 247 · FRLG 248',
          ip.evaluate('ITEMS.filter(i=>i.g.includes("r")).length') == 222 and
          ip.evaluate('ITEMS.filter(i=>i.g.includes("e")).length') == 247 and
          ip.evaluate('ITEMS.filter(i=>i.g.includes("f")).length') == 248)
    check('items data: sapphire == ruby lists, leafgreen == fireren lists',
          ip.evaluate('ITEMS.every(i=>i.g.includes("r")===i.g.includes("s") && i.g.includes("f")===i.g.includes("l"))'))
    check('items data: no TM/HM machines leaked into the bag list',
          ip.evaluate('ITEMS.every(i=>!i.k.startsWith("ITEM_TM") && !i.k.startsWith("ITEM_HM"))'))
    check('items data: every item has EN + FA name, pocket, category, price table',
          ip.evaluate('ITEMS.every(i=>i.en && i.fa && i.pk && i.cat && i.p && ["rs","e","frlg"].some(g=>i.p[g]!==undefined))'))
    check('items data: 43 berries with 5 flavors each (0..40) + firmness',
          ip.evaluate('(()=>{const b=ITEMS.filter(i=>i.cat==="berry");return b.length===43 && b.every(i=>i.fl && ["spicy","dry","sweet","bitter","sour"].every(f=>Number.isInteger(i.fl[f]) && i.fl[f]>=0) && i.firm);})()'))
    check('items data: flavors era-true spot checks (CHERI 10/0/0/0/0, SITRUS all 10)',
          ip.evaluate('(()=>{const c=ITEMS.find(i=>i.k==="ITEM_CHERI_BERRY").fl, s=ITEMS.find(i=>i.k==="ITEM_SITRUS_BERRY").fl; return c.spicy===10&&c.dry===0&&c.sour===0 && ["spicy","dry","sweet","bitter","sour"].every(f=>s[f]===10);})()'))
    check('items data: per-cartridge wordings differ where the carts did (MASTER BALL)',
          ip.evaluate('(()=>{const m=ITEMS.find(i=>i.k==="ITEM_MASTER_BALL"); return m.d.rs===m.d.e && m.d.rs!==m.d.frlg;})()'))
    check('items data: FRLG-only key items flagged (TOWN MAP not on R/S)',
          ip.evaluate('(()=>{const t=ITEMS.find(i=>i.k==="ITEM_TOWN_MAP"); return t && !t.g.includes("r") && t.g.includes("f");})()'))

    # overlay UI
    ip.evaluate('ItemsUI.openDex()')
    ip.wait_for_timeout(400)
    check('items UI: overlay opens with head label', ip.text_content('#itHeadT').startswith('ITEM DEX'))
    check('items UI: 248 cards, count label', ip.evaluate('document.querySelectorAll("#itBody .icard").length') == 248)
    check('items UI: no GB/COLOR toggle for gen3 (fixed color icons)',
          ip.evaluate('!document.querySelector("#itStyle")'))
    check('items UI: honest color-only note shown (EN)',
          ip.evaluate('(()=>{const n=[...document.querySelectorAll("#itBody .it-note")].map(e=>e.textContent).join(" ");return n.includes("color item art");})()'))
    check('items UI: ruby price column on card (HYPER POTION ¥1200, MASTER BALL not sold)',
          ip.evaluate('(()=>{const f=k=>{const c=[...document.querySelectorAll("#itBody .icard")].find(x=>x.dataset.k===k);return c.querySelector(".it-price").textContent;};return f("ITEM_HYPER_POTION")==="¥1200" && f("ITEM_MASTER_BALL").includes("NOT FOR SALE");})()'))
    ip.screenshot(path=f'{SHOT}/gen3-items-overlay-en.png')

    # detail view + per-group price rows
    ip.evaluate('ItemsUI.closeDex()')
    ip.evaluate('ItemsUI.setGroup("frlg")')
    ip.evaluate('ItemsUI.openDex()')
    ip.wait_for_timeout(300)
    check('items UI: setGroup follows the cartridge (RETRO MAIL ¥50 only on FRLG)',
          ip.evaluate('(()=>{const c=[...document.querySelectorAll("#itBody .icard")].find(x=>x.dataset.k==="ITEM_RETRO_MAIL");return c && c.querySelector(".it-price").textContent==="¥50";})()'))
    ip.evaluate('ItemsUI.setGroup("rs")')  # back to the ruby cartridge
    ip.evaluate('ItemsUI.closeDex()')
    ip.evaluate('ItemsUI.openDex()')
    ip.wait_for_timeout(300)
    ip.evaluate('(()=>{const c=[...document.querySelectorAll("#itBody .icard")].find(x=>x.dataset.k==="ITEM_CHERI_BERRY");c.click();})()')
    ip.wait_for_timeout(300)
    check('items UI: berry detail shows FLAVORS + 5 rows + firmness',
          ip.evaluate('(()=>{const b=document.querySelector("#itemsBox");const fl=b.querySelectorAll(".id-fl");return !!b.querySelector(".id-flavors") && fl.length>=6 && b.textContent.includes("FIRMNESS");})()'))
    check('items UI: ruby cartridge shows the R/S berry wording',
          ip.evaluate('(()=>{const b=document.querySelector("#itemsBox");return b.querySelector(".d-en").textContent.includes("Blooms with delicate");})()'))
    ip.screenshot(path=f'{SHOT}/gen3-items-detail-en.png')

    # theme change → price group + wording swap (ruby → firered), live overlay
    ip.evaluate('toggleTheme("firered")')
    ip.wait_for_timeout(400)
    check('items UI: theme swap swaps the detail wording to the FRLG cart\'s own',
          ip.evaluate('(()=>{const b=document.querySelector("#itemsBox");return b && b.querySelector(".d-en").textContent.includes("When held by a POKéMON, it will be used in battle to heal paralysis");})()'))

    # FA pass
    fctx = browser.new_context(viewport={'width': 1440, 'height': 950})
    fp2 = fctx.new_page()
    seed(fp2, lang='fa', theme='ruby')
    fp2.goto(f'file://{R}/gen3.html')
    fp2.wait_for_timeout(1600)
    check('items FA: menu entry in Persian', fp2.evaluate('document.querySelector("#menuPop [data-act=itemsdex]").textContent.includes("دکس آیتم")'))
    fp2.evaluate('ItemsUI.openDex()')
    fp2.wait_for_timeout(400)
    check('items FA: overlay head + chips in Persian, RTL',
          fp2.evaluate('document.querySelector("#itemsWrap").textContent.includes("دکس آیتم")'))
    check('items FA: all 248 FA names render (first card has Persian)',
          fp2.evaluate('(()=>{const c=document.querySelector("#itBody .icard .icard-fa");return c && /[\u0600-\u06FF]/.test(c.textContent);})()'))
    check('items FA: prices use Persian digits',
          fp2.evaluate('(()=>{const c=[...document.querySelectorAll("#itBody .icard")].find(x=>x.dataset.k==="ITEM_HYPER_POTION");return c && /[\u06F0-\u06F9]/.test(c.querySelector(".it-price").textContent);})()'))
    check('items FA: honest color note in Persian',
          fp2.evaluate('(()=>{const n=[...document.querySelectorAll("#itBody .it-note")].map(e=>e.textContent).join(" ");return n.includes("رنگی");})()'))
    fp2.evaluate('(()=>{const c=[...document.querySelectorAll("#itBody .icard")].find(x=>x.dataset.k==="ITEM_CHERI_BERRY");c.click();})()')
    fp2.wait_for_timeout(300)
    check('items FA: berry detail — Persian flavor labels + Persian digits + FA wording',
          fp2.evaluate('(()=>{const b=document.querySelector("#itemsBox");return b.querySelector(".id-flavors") && b.textContent.includes("تندی") && /[\u06F0-\u06F9]/.test(b.querySelector(".id-fl-v").textContent) && /[\u0600-\u06FF]/.test(b.querySelector(".d-fa").textContent);})()'))
    check('items FA: detail FRLG price row labels in Persian',
          fp2.evaluate('(()=>{const b=document.querySelector("#itemsBox");return b.textContent.includes("یاقوت/یاقوت کبود") && b.textContent.includes("زمرد") && b.textContent.includes("آتشین/برگ سبز");})()'))
    fp2.screenshot(path=f'{SHOT}/gen3-items-detail-fa.png')

    # icons on disk for every mapped item; the 5 unmapped are honest misses
    miss = ip.evaluate('ITEMS.filter(i=>!i.i).map(i=>i.k)')
    check('items icons: only ITEMFINDER + 4 ship-room keys lack menu art',
          sorted(miss) == ['ITEM_ITEMFINDER', 'ITEM_ROOM_1_KEY', 'ITEM_ROOM_2_KEY', 'ITEM_ROOM_4_KEY', 'ITEM_ROOM_6_KEY'], str(miss))
    icons_needed = ip.evaluate('ITEMS.filter(i=>i.i).map(i=>i.i)')
    missing_on_disk = [sl for sl in icons_needed
                       if not os.path.exists(f'{R}/assets/itemicons/{sl}.png')]
    check('items icons: every mapped icon file exists on disk', missing_on_disk == [], str(missing_on_disk[:5]))

    # search + category chips (fresh page: the overlay remembers the last
    # detail view, like gen1/gen2)
    ip2 = browser.new_context(viewport={'width': 1440, 'height': 950}).new_page()
    seed(ip2, theme='ruby')
    ip2.goto(f'file://{R}/gen3.html')
    ip2.wait_for_timeout(1600)
    ip2.evaluate('ItemsUI.openDex()')
    ip2.wait_for_timeout(300)
    ip2.fill('#itQ', 'توت چری')
    ip2.wait_for_timeout(300)
    check('items search: FA query finds CHERI BERRY',
          ip2.evaluate('(()=>{const cs=[...document.querySelectorAll("#itBody .icard")];return cs.length===1 && cs[0].dataset.k==="ITEM_CHERI_BERRY";})()'))
    ip2.fill('#itQ', '')
    ip2.wait_for_timeout(200)
    ip2.evaluate('(()=>{const b=[...document.querySelectorAll("#itSub .it-chip")].find(x=>x.textContent==="Berries");b.click();})()')
    ip2.wait_for_timeout(300)
    check('items chips: Berries filter → 43 cards',
          ip2.evaluate('document.querySelectorAll("#itBody .icard").length') == 43)
    ip2.screenshot(path=f'{SHOT}/gen3-items-chips-en.png')
    ip2.context.close()

    fp2.close(); fctx.close()
    ictx.close()

    # ==================== PHASE 5 — Location Dex + How to Catch (Hoenn) ====================
    lctx = browser.new_context(viewport={'width': 1440, 'height': 950})
    lp = lctx.new_page()
    lerr = []
    lp.on('console', lambda m: lerr.append(m.text) if m.type == 'error' else None)
    lp.on('pageerror', lambda e: lerr.append(str(e)))
    seed(lp, theme='ruby')
    lp.goto(f'file://{R}/gen3.html')
    lp.wait_for_timeout(1800)

    check('locations: scripts load (LOC3 + module) with no console errors',
          lp.evaluate('typeof LOC3!=="undefined" && typeof LocUI!=="undefined"') and not lerr, '; '.join(lerr[:3]))
    check('locations: START menu entry present (ruby)',
          lp.evaluate('!!document.querySelector("#menuPop [data-act=locdex]")'))
    check('locations: HOW TO CATCH section in the detail pane',
          lp.evaluate('!!document.querySelector("#locSec")'))
    check('locations: section follows the active game (RUBY chip on)',
          lp.evaluate('(()=>{const c=[...document.querySelectorAll("#locSec .lchip")].find(x=>x.dataset.lg==="ruby");return c && c.classList.contains("on");})()'))

    # data-level checks straight from LOC3
    ldata = lp.evaluate("""(function(){
      const H = LOC3.regions.hoenn;
      const noFA = H.locs.filter(l=>!l.fa || !/[\\u0600-\\u06FF]/.test(l.fa)).length;
      const ids = H.locs.map(l=>l.id);
      const groups = {}; H.locs.forEach(l=>groups[l.g]=(groups[l.g]||0)+1);
      const r101 = H.locs.find(l=>l.id==='MAPSEC_ROUTE_101');
      const isStart = id => id===252 || id===255 || id===258;
      const noStarter = H.locs.every(l=>Object.values(l.t||{}).every(rooms=>!rooms || rooms.every(rm=>
        !(rm.land && rm.land.s.some(e=>isStart(e[0]))) &&
        !(rm.surf && rm.surf.w.some(e=>isStart(e[0]))) &&
        !(rm.rk && rm.rk.s2.some(e=>isStart(e[0]))))));
      const saf = H.locs.find(l=>l.id==='MAPSEC_SAFARI_ZONE');
      const coo = H.locs.find(l=>l.id==='MAPSEC_CAVE_OF_ORIGIN');
      const spOf = id => H.sp.filter(s=>s.m && s.m.some(x=>x[0]===id));
      const grou = {}; spOf(383).forEach(s=>{grou[s.v.join('+')+'@'+(s.loc||'roam')]=s.m[0][1];});
      const kyo = {}; spOf(382).forEach(s=>{kyo[s.v.join('+')+'@'+(s.loc||'roam')]=s.m[0][1];});
      const lvl = (id, v) => { const s=H.sp.find(s=>s.m&&s.m[0][0]===id&&s.v.includes(v)); return s?s.m[0][1]:null; };
      const trades = { rs: H.sp.filter(s=>s.k==='trade'&&s.v.includes('ruby')).length,
                       em: H.sp.filter(s=>s.k==='trade'&&s.v.includes('emerald')).length };
      const fishAllMagikarp = H.fish.every(f=>(f.o||[]).every(r=>r[0]===129));
      const uw = {}; ['MAPSEC_UNDERWATER_124','MAPSEC_UNDERWATER_125','MAPSEC_UNDERWATER_126'].forEach(id=>{
        const l=H.locs.find(x=>x.id===id); uw[id]=l?Object.keys(l.t):null; });
      const spFA = H.sp.every(s=>s.d.fa && /[\\u0600-\\u06FF]/.test(s.d.fa));
      const evos = H.sp.filter(s=>s.k==='egg').length;
      return { n: H.locs.length, noFA, uniq: new Set(ids).size, groups,
               r101rate: r101.t.ruby[0].land.r, r101has261: r101.t.ruby[0].land.s.some(e=>e[0]===261),
               noStarter,
               safRuby: saf.t.ruby.length, safEm: saf.t.emerald.length,
               cooRuby: coo.t.ruby.length, cooEm: coo.t.emerald.length,
               grou, kyo, grouSapph: spOf(383).some(s=>s.v.includes('sapphire')),
               ray: spOf(384).map(s=>[s.v.join('+'), s.m[0][1]]),
               regice: lvl(378,'ruby'), voltorbN: (H.sp.find(s=>s.k==='static'&&s.loc==='MAPSEC_NEW_MAUVILLE').m||[]).length,
               sudowoodo: lvl(185,'emerald'), kecleon: lvl(352,'ruby'),
               trades, beldum: H.sp.some(s=>s.m&&s.m[0][0]===374&&s.v.length===3),
               castform: H.sp.some(s=>s.m&&s.m[0][0]===351&&s.v.length===3),
               wynaut: evos,
               latiRoam: H.sp.filter(s=>s.k==='roamer').length,
               south: H.sp.filter(s=>s.loc==='MAPSEC_SOUTHERN_ISLAND').map(s=>s.v.join('+')),
               mew: lvl(151,'emerald'), lugia: lvl(249,'emerald'), hooh: lvl(250,'emerald'), deoxys: lvl(386,'emerald'),
               deoxysRS: spOf(386).some(s=>s.v.some(v=>v!=='emerald')),
               swarms: H.swarms.map(s=>[s.id,s.lvl,s.loc]),
               fishAllMagikarp, bite: LOC3.bite,
               uw, spFA,
               notes: H.locs.filter(l=>l.note).map(l=>l.id),
               noTimeTabs: true,
               dedup: H.locs.filter(l=>l.t.sapphire===undefined && l.t.ruby!==undefined).length,
               kantoNull: LOC3.regions.kanto === null }; })()""")
    check('80 locations, all bilingual, unique ids', ldata['n'] == 80 and ldata['noFA'] == 0 and ldata['uniq'] == 80, str(ldata['n']))
    check('every group represented (routes/cities/caves/water/safari/island/building)',
          all(g in ldata['groups'] for g in ['route','city','cave','water','safari','island','building']), str(ldata['groups']))
    check('Route 101 ruby: rate 20 + Poochyena in slot table', ldata['r101rate'] == 20 and ldata['r101has261'])
    check('no wild starters anywhere (Treecko/Torchic/Mudkip)', ldata['noStarter'])
    check('Safari Zone areas: 4 on R/S, 6 on Emerald (N+S Emerald-only)',
          ldata['safRuby'] == 4 and ldata['safEm'] == 6, f"{ldata['safRuby']}/{ldata['safEm']}")
    check('Cave of Origin rooms: 5 on R/S (B4F special), 2 on Emerald',
          ldata['cooRuby'] == 5 and ldata['cooEm'] == 2, f"{ldata['cooRuby']}/{ldata['cooEm']}")
    check('Groudon version-locked: R 45 @Cave of Origin · E 70 @Terra Cave · never Sapphire',
          ldata['grou'] == {'ruby@MAPSEC_CAVE_OF_ORIGIN': 45, 'emerald@MAPSEC_TERRA_CAVE': 70} and not ldata['grouSapph'], str(ldata['grou']))
    check('Kyogre version-locked: S 45 @Cave of Origin · E 70 @Marine Cave',
          ldata['kyo'] == {'sapphire@MAPSEC_CAVE_OF_ORIGIN': 45, 'emerald@MAPSEC_MARINE_CAVE': 70}, str(ldata['kyo']))
    check('Rayquaza Lv 70 in all three games at Sky Pillar',
          ldata['ray'] == [["ruby+sapphire+emerald", 70]], str(ldata['ray']))
    check('Regice Lv 40 (Island Cave), Voltorb trio Lv 25, Kecleon Lv 30, Sudowoodo Lv 40 Emerald-only',
          ldata['regice'] == 40 and ldata['voltorbN'] == 3 and ldata['kecleon'] == 30 and ldata['sudowoodo'] == 40, str((ldata['regice'], ldata['voltorbN'], ldata['kecleon'], ldata['sudowoodo'])))
    check('in-game trades: 3 on R/S + 4 on Emerald', ldata['trades'] == {'rs': 3, 'em': 4}, str(ldata['trades']))
    check('Beldum + Castform gifts + Wynaut egg in every game', ldata['beldum'] and ldata['castform'] and ldata['wynaut'])
    check('Latis: 4 roamer entries (40) + Southern Island per game (50)',
          ldata['latiRoam'] == 4 and sorted(ldata['south']) == ['emerald', 'ruby', 'sapphire'], str((ldata['latiRoam'], ldata['south'])))
    check('ticket events Emerald-only: Mew 30 · Lugia 70 · Ho-Oh 70 · Deoxys 30',
          (ldata['mew'], ldata['lugia'], ldata['hooh'], ldata['deoxys']) == (30, 70, 70, 30) and not ldata['deoxysRS'])
    check('Emerald swarms: Seedot3/R102 · Skitty8/R116 · Seedot13/R117 · Nuzleaf15/R114 · Seedot25/R120',
          ldata['swarms'] == [[273, 3, 'MAPSEC_ROUTE_102'], [300, 8, 'MAPSEC_ROUTE_116'], [273, 13, 'MAPSEC_ROUTE_117'], [274, 15, 'MAPSEC_ROUTE_114'], [273, 25, 'MAPSEC_ROUTE_120']], str(ldata['swarms']))
    check('fishing: Old Rod hooks only Magikarp everywhere · bite 50%',
          ldata['fishAllMagikarp'] and ldata['bite'] == 50)
    check('underwater coverage: R/S 124+125 · Emerald 124+126 (sapphire deduped to ruby)',
          ldata['uw']['MAPSEC_UNDERWATER_124'] == ['ruby', 'emerald'] and
          ldata['uw']['MAPSEC_UNDERWATER_125'] == ['ruby'] and
          ldata['uw']['MAPSEC_UNDERWATER_126'] == ['emerald'], str(ldata['uw']))
    check('every special way carries a Persian description', ldata['spFA'])
    check('per-location notes: Feebas (R119) · Altering Cave · Shoal tides',
          sorted(ldata['notes']) == ['MAPSEC_ALTERING_CAVE', 'MAPSEC_ROUTE_119', 'MAPSEC_SHOAL_CAVE'], str(ldata['notes']))
    check('R/S dedupe: identical Sapphire tables omitted (fallback to ruby)',
          ldata['dedup'] >= 30, str(ldata['dedup']))
    check('kanto region stays null until phase 6 (FRLG hidden)', ldata['kantoNull'])

    # HOW TO CATCH per Pokémon
    lp.evaluate("select(304)")   # Aron — Granite Cave wild
    lp.wait_for_timeout(250)
    txt = lp.evaluate("document.querySelector('#locSec').textContent")
    check('Aron HOW TO CATCH lists Granite Cave (bilingual)',
          'Granite Cave' in txt and 'غار گرانیت' in txt, txt[:60])
    lp.evaluate("select(383)")   # Groudon — version-dependent static
    lp.wait_for_timeout(250)
    txt = lp.evaluate("document.querySelector('#locSec').textContent")
    check('Groudon shows Lv 45 Cave of Origin on RUBY', '45' in txt and 'Cave of Origin' in txt, txt[:70])
    lp.evaluate("[...document.querySelectorAll('#locSec .lchip')].find(x=>x.dataset.lg==='sapphire').click()")
    lp.wait_for_timeout(250)
    txt = lp.evaluate("document.querySelector('#locSec').textContent")
    check('Groudon locked out on SAPPHIRE with the trade note', 'NOT IN THIS GAME' in txt.upper() and 'Trade' in txt, txt[:70])
    lp.evaluate("[...document.querySelectorAll('#locSec .lchip')].find(x=>x.dataset.lg==='emerald').click()")
    lp.wait_for_timeout(250)
    txt = lp.evaluate("document.querySelector('#locSec').textContent")
    check('Groudon chip switch shows Lv 70 Terra Cave (Emerald)', '70' in txt and 'Terra Cave' in txt, txt[:70])
    lp.evaluate("select(149)")   # Dragonite — not obtainable in Hoenn at all
    lp.wait_for_timeout(250)
    txt = lp.evaluate("document.querySelector('#locSec').textContent")
    check('Dragonite: honest not-obtainable note (cartridge trade)', 'NOT IN THIS GAME' in txt.upper() and 'Generation III' in txt, txt[:80])
    lp.evaluate("select(350)")   # Milotic — beauty evolution from wild Feebas
    lp.wait_for_timeout(250)
    txt = lp.evaluate("document.querySelector('#locSec').textContent")
    check('Milotic: evolution path via Beauty 170 (gen-3 condition)', 'Beauty' in txt and '170' in txt, txt[:80])
    lp.evaluate("select(336)")   # Seviper — sapphire/emerald only (route 114)
    lp.wait_for_timeout(250)
    txt = lp.evaluate("document.querySelector('#locSec').textContent")
    check('Seviper: wild rows only in the games that have it', 'Route 114' in txt or 'Safari' in txt, txt[:60])
    lp.evaluate("select(386)")   # Deoxys — Emerald ticket event
    lp.wait_for_timeout(250)
    txt = lp.evaluate("document.querySelector('#locSec').textContent")
    check('Deoxys: EVENT row on Emerald (Birth Island, Speed forme)', 'EVENT' in txt.upper() and 'Birth Island' in txt, txt[:80])

    # Location Dex overlay
    lp.keyboard.press('l')
    lp.wait_for_timeout(350)
    check('overlay opens with L', lp.evaluate("!document.querySelector('#locWrap').classList.contains('hidden')"))
    ov_n = lp.evaluate("document.querySelectorAll('#locWrap .lcard').length")
    check('overlay lists all 80 locations', ov_n == 80, f'cards={ov_n}')
    ov_head = lp.evaluate("document.querySelector('#lcHeadT').textContent")
    check('overlay head follows the theme game (ruby seed)', 'RUBY' in ov_head, ov_head)
    lp.evaluate("[...document.querySelectorAll('#lcViewbar .gchip')].find(x=>x.dataset.gm==='emerald').click()")
    lp.wait_for_timeout(250)
    ov_head2 = lp.evaluate("document.querySelector('#lcHeadT').textContent")
    check('overlay game chip switches to EMERALD', 'EMERALD' in ov_head2, ov_head2)
    lp.evaluate("[...document.querySelectorAll('#lcViewbar .gchip')].find(x=>x.dataset.gm==='ruby').click()")
    lp.wait_for_timeout(250)
    lp.evaluate("LocUI.openDex('MAPSEC_ROUTE_101')")
    lp.wait_for_timeout(300)
    r101 = lp.evaluate("document.querySelector('#lcBody').textContent")
    check('Route 101 view: grass + Persian name + Poochyena',
          'GRASS' in r101 and 'مسیر ۱۰۱' in r101 and 'Poochyena' in r101, r101[:70].replace('\n', ' '))
    check('no time tabs in Gen 3 (day/night dropped)', lp.evaluate("document.querySelectorAll('#lcBody .tchip').length") == 0)
    check('slot percentages aggregate (Zigzagoon 45% on R101)',
          lp.evaluate("(()=>{const r=[...document.querySelectorAll('#lcBody .lrow.mon')].find(x=>x.textContent.includes('Zigzagoon'));return r && r.querySelector('.lrow-pc').textContent.trim().replace('%','')==='45';})()"))
    lp.screenshot(path=f'{SHOT}/loc_route101.png')
    lp.evaluate("LocUI.openDex('MAPSEC_ROUTE_119')")
    lp.wait_for_timeout(300)
    r119 = lp.evaluate("document.querySelector('#lcBody').textContent")
    check('Route 119 view: Feebas tile note present', 'FEEBAS' in r119.upper() and '6 random' in r119, r119[:70])
    check('Route 119 underwater badge absent (land route)',
          lp.evaluate("!document.querySelector('#lcBody .lcb-uw')"))
    lp.evaluate("LocUI.openDex('MAPSEC_UNDERWATER_124')")
    lp.wait_for_timeout(300)
    uw = lp.evaluate("document.querySelector('#lcBody').textContent")
    check('Underwater Route 124: UNDERWATER label + absent note on RUBY (EM-only? no: exists)',
          'UNDERWATER' in uw.upper(), uw[:70])
    lp.evaluate("[...document.querySelectorAll('#lcViewbar .gchip')].find(x=>x.dataset.gm==='emerald').click()")
    lp.wait_for_timeout(250)
    uw2 = lp.evaluate("document.querySelector('#lcBody').textContent")
    check('Underwater 124 shows tables on Emerald (no absent note)',
          'does not exist' not in uw2 and 'UNDERWATER' in uw2.upper(), uw2[:70])
    lp.evaluate("LocUI.openDex('MAPSEC_UNDERWATER_126')")
    lp.wait_for_timeout(250)
    lp.evaluate("[...document.querySelectorAll('#lcViewbar .gchip')].find(x=>x.dataset.gm==='ruby').click()")
    lp.wait_for_timeout(250)
    uw3 = lp.evaluate("document.querySelector('#lcBody').textContent")
    check('Underwater 126 on RUBY: honest absent note', 'does not exist in RUBY' in uw3, uw3[:70])
    lp.evaluate("LocUI.openDex('MAPSEC_SAFARI_ZONE')")
    lp.wait_for_timeout(250)
    saf = lp.evaluate("document.querySelector('#lcBody').textContent")
    check('Safari Zone on RUBY: 4 area blocks', all(a in saf for a in ['Northwest', 'Northeast', 'Southwest', 'Southeast']), saf[:80])
    lp.evaluate("[...document.querySelectorAll('#lcViewbar .gchip')].find(x=>x.dataset.gm==='emerald').click()")
    lp.wait_for_timeout(250)
    saf2 = lp.evaluate("document.querySelector('#lcBody').textContent")
    check('Safari Zone on EMERALD adds North + South areas',
          all(a in saf2 for a in ['North area', 'South area']), saf2[:80])
    lp.evaluate("LocUI.openDex('MAPSEC_SHOAL_CAVE')")
    lp.wait_for_timeout(250)
    sh = lp.evaluate("document.querySelector('#lcBody').textContent")
    check('Shoal Cave: low-tide room labels + tide note',
          'low tide' in sh and 'Tides' in sh, sh[:80])
    lp.evaluate("LocUI.openDex('MAPSEC_ROUTE_116')")
    lp.wait_for_timeout(250)
    sw = lp.evaluate("[...document.querySelectorAll('#lcViewbar .gchip')].find(x=>x.dataset.gm==='emerald').click(), document.querySelector('#lcBody').textContent")
    check('Route 116 (Emerald): Skitty swarm block + note', 'SWARM' in sw.upper() and 'Skitty' in sw, sw[:80])
    lp.screenshot(path=f'{SHOT}/loc_r116_swarm.png')
    lp.evaluate("LocUI.openDex('MAPSEC_TERRA_CAVE')")
    lp.wait_for_timeout(250)
    coo = lp.evaluate("[...document.querySelectorAll('#lcViewbar .gchip')].find(x=>x.dataset.gm==='emerald').click(), document.querySelector('#lcBody').textContent")
    check('Terra Cave (Emerald): Groudon Lv 70 + legend note',
          'GROUDON' in coo.upper() and '70' in coo and 'one-time legendary' in coo, coo[:80])
    lp.evaluate("LocUI.openDex()")
    lp.wait_for_timeout(300)
    check('group chips filter (Caves → cave-only cards)',
          lp.evaluate("(()=>{document.querySelector('#lcViewbar .it-chip[data-g=cave]').click();const r=document.querySelector('#locWrap').textContent;return !r.includes('Route 101');})()"))
    lp.evaluate("[...document.querySelectorAll('#lcViewbar .it-chip')].find(x=>x.dataset.g==='all').click()")
    lp.wait_for_timeout(200)
    lp.fill('#lcQ', 'غار گرانیت')
    lp.wait_for_timeout(250)
    check('search matches the Persian name (Granite Cave)',
          lp.evaluate("(()=>{const c=[...document.querySelectorAll('#lcBody .lcard')];return c.length===1 && c[0].dataset.loc==='MAPSEC_GRANITE_CAVE';})()"))
    lp.keyboard.press('Escape')
    lp.wait_for_timeout(200)
    check('Escape closes the overlay', lp.evaluate("document.querySelector('#locWrap').classList.contains('hidden')"))

    # FRLG: no Hoenn section (kanto lands in phase 6)
    lp.evaluate("toggleTheme('firered')")
    lp.wait_for_timeout(400)
    check('FRLG: HOW TO CATCH section hidden (no invented data)',
          lp.evaluate("!document.querySelector('#locSec')"))
    check('FRLG: START menu entry hidden', lp.evaluate("document.querySelector('#menuPop [data-act=locdex]').style.display === 'none'"))
    check('FRLG: openDex is a no-op', lp.evaluate("LocUI.openDex(), document.querySelector('#locWrap').classList.contains('hidden')"))
    lp.evaluate("toggleTheme('ruby')")
    lp.wait_for_timeout(300)
    check('back on RUBY: section + menu return', lp.evaluate("!!document.querySelector('#locSec')") and
          lp.evaluate("document.querySelector('#menuPop [data-act=locdex]').style.display !== 'none'"))

    # mobile: full-width panels (the b0e9a15 lesson) + overlay fits
    mctx = browser.new_context(viewport={'width': 390, 'height': 844})
    mp = mctx.new_page()
    seed(mp, theme='emerald')
    mp.goto(f'file://{R}/gen3.html')
    mp.wait_for_timeout(1600)
    mp.evaluate("select(304)")
    mp.wait_for_timeout(250)
    mw = mp.evaluate("(()=>{const s=document.querySelector('#locSec').getBoundingClientRect();const p=document.querySelector('#detailPane').getBoundingClientRect();return {sec:s.width, pane:p.width};})()")
    check('mobile: location section stretches with the pane (no shrink)',
          mw['sec'] >= mw['pane'] - 40, str(mw))
    mp.evaluate("LocUI.openDex()")
    mp.wait_for_timeout(300)
    mo = mp.evaluate("(()=>{const b=document.querySelector('#locBox').getBoundingClientRect();return {w:Math.round(b.width), inner:window.innerWidth};})()")
    check('mobile: overlay fits the viewport', mo['w'] <= mo['inner'] and mo['w'] >= mo['inner'] - 30, str(mo))
    mp.screenshot(path=f'{SHOT}/loc_mobile.png')
    mctx.close()

    # FA pass for the location module
    lfctx = browser.new_context(viewport={'width': 1440, 'height': 950})
    lfp = lfctx.new_page()
    seed(lfp, lang='fa', theme='sapphire')
    lfp.goto(f'file://{R}/gen3.html')
    lfp.wait_for_timeout(1600)
    check('locations FA: START menu entry in Persian',
          lfp.evaluate('document.querySelector("#menuPop [data-act=locdex]").textContent.includes("دکس مکان")'))
    lfp.evaluate("select(252)")
    lfp.wait_for_timeout(250)
    fa_sec = lfp.evaluate("document.querySelector('#locSec').textContent")
    check('locations FA: starter special renders in Persian',
          'استارتر' in fa_sec and 'برچ' in fa_sec and 'سطح ۵' in fa_sec, fa_sec[:80])
    check('locations FA: Persian digits in the section',
          any('\u06F0' <= ch <= '\u06F9' for ch in fa_sec))
    lfp.evaluate("select(149)")
    lfp.wait_for_timeout(250)
    fa_none = lfp.evaluate("document.querySelector('#locSec').textContent")
    check('locations FA: not-obtainable note in Persian',
          'در این نسخه نیست' in fa_none and 'کارتریج' in fa_none, fa_none[:90])
    lfp.evaluate("select(130)")
    lfp.wait_for_timeout(250)
    fa_wild = lfp.evaluate("document.querySelector('#locSec').textContent")
    check('locations FA: Gyarados via Magikarp evolution (Lv 20, no wild Gyarados in Hoenn)',
          'با تکامل' in fa_wild and 'ماجیکارپ' in fa_wild and 'سطح ۲۰' in fa_wild, fa_wild[:80])
    lfp.evaluate("LocUI.openDex()")
    lfp.wait_for_timeout(400)
    check('locations FA: overlay head + cards in Persian',
          lfp.evaluate('document.querySelector("#lcHeadT").textContent.includes("دکس مکان")'))
    check('locations FA: FA search works (یاقوت کبود header present)',
          lfp.evaluate('document.querySelector("#locWrap").textContent.includes("یاقوت کبود")'))
    lfp.evaluate("LocUI.openDex('MAPSEC_ROUTE_119')")
    lfp.wait_for_timeout(300)
    fa_note = lfp.evaluate("document.querySelector('#lcBody').textContent")
    check('locations FA: Feebas note in Persian with Persian digits',
          'فِیباس' in fa_note and '۵۰٪' in fa_note, fa_note[:90])
    lfp.screenshot(path=f'{SHOT}/loc_fa.png')
    lfctx.close()
    lctx.close()

    ctx3.close()
    browser.close()

fails = [x for x in results if not x[1]]
print(f'\n{len(results) - len(fails)}/{len(results)} passed')
raise SystemExit(1 if fails else 0)
