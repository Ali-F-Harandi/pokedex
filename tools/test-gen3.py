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
    check('deoxys EMERALD: speed sprite in emerald bank', 'gen3-emerald/386.png' in src_em, src_em)
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
    # frlg wording falls back to EN until its FA lands (gen2 fallback pattern)
    page.click('.tchip[data-th=firered]')
    page.wait_for_timeout(300)
    fr_text = page.text_content('#flavorBox')
    check('FA: frlg wording falls back to EN (fa_frlg pending)', fr_text and not any('\u0600' <= c <= '\u06FF' for c in fr_text))

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
    ctx3.close()
    browser.close()

fails = [x for x in results if not x[1]]
print(f'\n{len(results) - len(fails)}/{len(results)} passed')
raise SystemExit(1 if fails else 0)
