#!/usr/bin/env python3
"""Phase 8 QA: gen3.html — screenshots (mobile 390 EN+FA, desktop 1440, all 5
themes) + DOM geometry audit (mobile reading order, bilingual name, panel
widths == viewport, no horizontal overflow, RTL sane)."""
import sys, pathlib, json
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = (ROOT / "gen3.html").as_uri()
OUT = pathlib.Path("/tmp/gen3qa"); OUT.mkdir(exist_ok=True)

SHOTS = [
    # (name, w, h, lang, theme, full_page)
    ("m-ruby-en",     390, 844, "en", "ruby",      True),
    ("m-sapphire-fa", 390, 844, "fa", "sapphire",  True),
    ("m-emerald-fa",  390, 844, "fa", "emerald",   True),
    ("d-ruby-en",    1440, 900, "en", "ruby",      False),
    ("d-sapphire-en",1440, 900, "en", "sapphire",  False),
    ("d-emerald-en", 1440, 900, "en", "emerald",   False),
    ("d-firered-fa", 1440, 900, "fa", "firered",   False),
    ("d-leafgreen-en",1440,900, "en", "leafgreen", False),
]

ORDER = [".cntBox", "#listPane", "#gameCfg", ".sprCard", "#detailPane"]
checks = []
def check(name, cond, info=""):
    checks.append((name, bool(cond), info))

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, w, h, lang, theme, full in SHOTS:
        ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg = ctx.new_page()
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.add_init_script(f"""
            localStorage.setItem('pkd_lang', JSON.stringify('{lang}'));
            localStorage.setItem('pkd_g3_theme', JSON.stringify('{theme}'));
        """)
        pg.goto(PAGE)
        pg.wait_for_timeout(2200)
        pg.screenshot(path=str(OUT / f"{name}.png"), full_page=full)

        if w == 390:
            # mobile reading order: DEX STATUS → search → SETTINGS → card → details
            tops = pg.evaluate("""sels => sels.map(s => {
                const el = document.querySelector(s);
                return el ? el.getBoundingClientRect().top : null;
            })""", ORDER)
            ok_order = all(t is not None for t in tops) and all(
                tops[i] <= tops[i+1] + 1 for i in range(len(tops)-1))
            check(f"{name}: mobile order DEX STATUS→search→SETTINGS→card→details",
                  ok_order, f"tops={[round(t) for t in tops if t is not None]}")
            # panel widths equal #main inner width (align-items:stretch lesson)
            widths = pg.evaluate("""() => {
                const m = document.querySelector('#main');
                const cs = getComputedStyle(m);
                const inner = m.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
                const sels = ['#listPane','#gameCfg','.sprCard','#detailPane','.cntBox'];
                return { inner: Math.round(inner),
                         panels: sels.map(s => Math.round(document.querySelector(s).getBoundingClientRect().width)) };
            }""")
            check(f"{name}: panels stretch to #main width (stretch, not shrink)",
                  all(abs(x - widths["inner"]) <= 2 for x in widths["panels"]),
                  f"main={widths['inner']} panels={widths['panels']}")
            # no horizontal overflow
            ov = pg.evaluate("document.documentElement.scrollWidth")
            check(f"{name}: no horizontal overflow (scrollWidth<=390)", ov <= 391, f"scrollWidth={ov}")
            # bilingual name in card
            bn = pg.evaluate("""() => {
                const n = document.querySelector('#sprName');
                const a = document.querySelector('#sprName .altName') ||
                          (n && n.parentElement.querySelector('.altName'));
                return { name: n ? n.textContent.trim() : '',
                         alt: a ? a.textContent.trim() : '', hasAlt: !!a };
            }""")
            check(f"{name}: bilingual name (EN + FA altName)",
                  bn["hasAlt"] and len(bn["alt"]) > 0 and bn["name"] not in ("---", ""),
                  json.dumps(bn, ensure_ascii=False))
        if lang == "fa":
            # RTL sane: html/body rtl, first panel content right-aligned
            d = pg.evaluate("""() => ({
                dir: document.body.classList.contains('fa'),
                rtl: getComputedStyle(document.body).direction
            })""")
            check(f"{name}: FA mode rtl", d["dir"] and d["rtl"] == "rtl", json.dumps(d))

        check(f"{name}: no page errors", not errors, str(errors or ""))
        ctx.close()
    browser.close()

ok = True
for n, c, info in checks:
    print(("PASS " if c else "FAIL ") + n + ("  " + info if info and not c else ""))
    ok = ok and c
print(f"\n{sum(1 for _,c,_ in checks if c)}/{len(checks)} geometry checks passed")
print("QA-SHOTS", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
