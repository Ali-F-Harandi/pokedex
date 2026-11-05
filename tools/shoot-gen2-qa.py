#!/usr/bin/env python3
"""Phase 6 QA screenshots: gen2.html — mobile 390 EN+FA, desktop 1440, 3 themes."""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = (ROOT / "gen2.html").as_uri()
OUT = pathlib.Path("/tmp/gen2qa"); OUT.mkdir(exist_ok=True)

SHOTS = [
    # (name, w, h, lang, theme, full_page)
    ("m-gold-en",   390, 844, "en", "gold",    True),
    ("m-silver-fa", 390, 844, "fa", "silver",  True),
    ("m-crystal-fa",390, 844, "fa", "crystal",True),
    ("d-gold-en",  1440, 900, "en", "gold",    False),
    ("d-silver-en",1440, 900, "en", "silver",  False),
    ("d-crystal-fa",1440,900, "fa", "crystal", False),
]

ok = True
with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, w, h, lang, theme, full in SHOTS:
        ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg = ctx.new_page()
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.add_init_script(f"""
            localStorage.setItem('pkd_lang', JSON.stringify('{lang}'));
            localStorage.setItem('pkd_g2_theme', JSON.stringify('{theme}'));
        """)
        pg.goto(PAGE)
        pg.wait_for_timeout(1800)
        # scroll a bit to expose details section, then back to top for full page shots
        pg.screenshot(path=str(OUT / f"{name}.png"), full_page=full)
        print(f"shot {name}: errors={errors or 'none'}")
        if errors: ok = False
        ctx.close()
    browser.close()

print("QA-SHOTS", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
