#!/usr/bin/env python3
"""Derive assets/js/gen1.js (the merged Gen-1 page) from redblue.js.

gen1.html is one dex for all four Gen-1 games. Its logic is the Red/Blue
page's logic plus a GAME THEME layer:

  state.theme  red | blue | green | yellow   (persisted pkd_g1_theme)
    -> sprite set family (rb/rbc, green, y/yc), moves data (MD_RB / MD_Y),
       shell theme class, default dex-text version
  state.text   rb | y                        (persisted pkd_g1_text)
    -> which version's dex entry text is shown; the R/B <-> YELLOW
       selector sits next to the entry title (all 151 texts differ)

This script applies surgical replacements to the Red/Blue page script so
the battle-tested logic stays byte-identical everywhere else. Every
replacement is asserted to match exactly once.
"""
import os
import sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SRC = f'{REPO}/assets/js/redblue.js'
DST = f'{REPO}/assets/js/gen1.js'


def sub(src, old, new, n=1):
    count = src.count(old)
    assert count == n, f'expected {n} match(es), got {count} for: {old[:70]!r}...'
    return src.replace(old, new)


def main():
    src = open(SRC, encoding='utf-8').read()

    # ---- 1. drop the injected data (gen1-data.js provides DATA/EVOLUTIONS/SPRITE_SETS)
    lines = src.split('\n')
    head = []
    for l in lines:
        if l.startswith('const DATA = ') or l.startswith('const EVOLUTIONS = ') or l.startswith('const SPRITE_SETS = '):
            continue
        head.append(l)
    src = '\n'.join(head)
    src = src.replace('"use strict";\n/* ===== injected build data ===== */',
                      '"use strict";\n/* ===== Pokédex Plus — GENERATION I: all four games in one dex (Red · Blue ·\n   Green (Japan) · Yellow). Derived from the Red/Blue page; loads gen1-data.js\n   (DATA / EVOLUTIONS / SPRITE_SETS) and moves-gen1.js (MD_RB / MD_Y). ===== */')

    # ---- 2. i18n: EN block --------------------------------------------------
    src = sub(src, '  brand_sub:"GEN I · RED/BLUE STYLE", brand_main:"Kanto Pokédex — 151 Pokémon",',
              '  brand_main:"Kanto Pokédex — 151 Pokémon",')
    src = sub(src, '  set_mark:"Sprites", set_names:{rb:"Red/Blue", rbc:"Red/Blue Color", green:"Green (Japan)"},',
              '  set_mark:"Sprites", set_names:{rb:"Red/Blue", rbc:"Red/Blue Color", green:"Green (Japan)", y:"Yellow", yc:"Yellow Color"},\n'
              '  theme_short:{red:"RED", blue:"BLUE", green:"GREEN", yellow:"YELLOW"},\n'
              '  theme_names:{red:"Pokémon Red", blue:"Pokémon Blue", green:"Pokémon Green (Japan)", yellow:"Pokémon Yellow"},\n'
              '  theme_tag:{red:"GEN I · RED VERSION", blue:"GEN I · BLUE VERSION", green:"GEN I · GREEN VERSION (JAPAN)", yellow:"GEN I · YELLOW VERSION"},\n'
              '  chip_mono:"MONO", chip_color:"COLOR",\n'
              '  text_ver:"Dex text version",\n'
              '  m_game_tpl:"Game: {v}", m_game:"Game: Red",')
    src = sub(src, '  title:"Pokédex — Red/Blue Style (Gen 1)"',
              '  title:"Pokédex — Generation I (Red · Blue · Green · Yellow)"')

    # ---- 3. i18n: FA block --------------------------------------------------
    src = sub(src, '  brand_sub:"نسل ۱ · سبک قرمز و آبی", brand_main:"پوکیدکس کانتو — ۱۵۱ پوکمون",',
              '  brand_main:"پوکیدکس کانتو — ۱۵۱ پوکمون",')
    src = sub(src, '  set_mark:"اسپرایت", set_names:{rb:"قرمز/آبی", rbc:"قرمز/آبی رنگی", green:"سبز (ژاپن)"},',
              '  set_mark:"اسپرایت", set_names:{rb:"قرمز/آبی", rbc:"قرمز/آبی رنگی", green:"سبز (ژاپن)", y:"زرد", yc:"زرد رنگی"},\n'
              '  theme_short:{red:"قرمز", blue:"آبی", green:"سبز", yellow:"زرد"},\n'
              '  theme_names:{red:"پوکمون قرمز", blue:"پوکمون آبی", green:"پوکمون سبز (ژاپن)", yellow:"پوکمون زرد"},\n'
              '  theme_tag:{red:"نسل ۱ · نسخه‌ی قرمز", blue:"نسل ۱ · نسخه‌ی آبی", green:"نسل ۱ · نسخه‌ی سبز (ژاپن)", yellow:"نسل ۱ · نسخه‌ی زرد"},\n'
              '  chip_mono:"تک‌رنگ", chip_color:"رنگی",\n'
              '  text_ver:"نسخه‌ی متن پوکیدکس",\n'
              '  m_game_tpl:"بازی: {v}", m_game:"بازی: قرمز",')
    src = sub(src, '  title:"پوکیدکس — سبک قرمز و آبی (نسل ۱)"',
              '  title:"پوکیدکس — نسل ۱ (قرمز · آبی · سبز · زرد)"')

    # ---- 4. state: theme + text + pkd_g1_* keys -----------------------------
    src = sub(src, '''  pal: store("pkd_rb_pal", "dmg") === "pocket" ? "pocket" : "dmg",
  set: ["rb","rbc","green"].indexOf(store("pkd_rb_set", "rb")) !== -1 ? store("pkd_rb_set", "rb") : "rb",
  back: store("pkd_rb_back", "front") === "back",
  favOnly: false,
  page: 1,
  favs: new Set(store("pkd_rb_favs", [])),
  seen: new Set(store("pkd_rb_seen", [])),
  own:  new Set(store("pkd_rb_own", []))''',
              '''  pal: store("pkd_g1_pal", "dmg") === "pocket" ? "pocket" : "dmg",
  theme: ["red","blue","green","yellow"].indexOf(store("pkd_g1_theme", "red")) !== -1 ? store("pkd_g1_theme", "red") : "red",
  set: ["rb","rbc","green","y","yc"].indexOf(store("pkd_g1_set", "rb")) !== -1 ? store("pkd_g1_set", "rb") : "rb",
  text: store("pkd_g1_text", null) === "y" ? "y" : "rb",
  back: store("pkd_g1_back", "front") === "back",
  favOnly: false,
  page: 1,
  favs: new Set(store("pkd_g1_favs", [])),
  seen: new Set(store("pkd_g1_seen", [])),
  own:  new Set(store("pkd_g1_own", []))''')

    # ---- 5. theme table right after the state block -------------------------
    src = sub(src, 'const isMobile = () => window.matchMedia("(max-width:860px)").matches;',
              '''const isMobile = () => window.matchMedia("(max-width:860px)").matches;

/* ===== GAME THEMES — which of the four Gen-1 games the dex is "running" =====
   set family: red/blue share the international sprites; green (Japan) is
   mono-only; yellow has its own redrawn sprites + its own dex texts. */
const THEMES = {
  red:    { sets:["rb","rbc"], def:"rb",    text:"rb", moves:"MD_RB", cls:"theme-red" },
  blue:   { sets:["rb","rbc"], def:"rb",    text:"rb", moves:"MD_RB", cls:"theme-blue" },
  green:  { sets:["green"],    def:"green", text:"rb", moves:"MD_RB", cls:"theme-green" },
  yellow: { sets:["y","yc"],   def:"y",     text:"y",  moves:"MD_Y",  cls:"theme-yellow" }
};
const THEME_ORDER = ["red","blue","green","yellow"];
function activeMoves(){ try { return MD_RB && MD_Y ? (THEMES[state.theme].moves === "MD_Y" ? MD_Y : MD_RB) : null; } catch(e){ return null; } }
function applyTheme(){
  const th = THEMES[state.theme] || THEMES.red;
  document.body.classList.remove("theme-red","theme-blue","theme-green","theme-yellow");
  document.body.classList.add(th.cls);
  if (th.sets.indexOf(state.set) === -1){ state.set = th.def; save("pkd_g1_set", state.set); }
  if (typeof MovesUI !== "undefined"){
    const md = activeMoves();
    if (md) MovesUI.setGame(md);
  }
  const t1 = document.querySelector("#topbar .t1");
  if (t1) t1.textContent = t("theme_tag." + state.theme);
}
function toggleTheme(th){
  if (!THEMES[th] || th === state.theme) return;
  state.theme = th;
  save("pkd_g1_theme", th);
  state.text = THEMES[th].text;          /* each game opens on its own texts */
  save("pkd_g1_text", state.text);
  state.page = 1;
  applyTheme();
  renderThemeRow(); renderSetRow();
  renderSpritePane(); renderDetail();
  refreshMenuLabels();
}
function cycleTheme(){
  const i = THEME_ORDER.indexOf(state.theme);
  toggleTheme(THEME_ORDER[(i + 1) % THEME_ORDER.length]);
}''')

    # ---- 6. sprite pane: theme row + dynamic set row ------------------------
    src = sub(src, '''  document.querySelectorAll("#setRow .setchip").forEach(ch => {
    const s = ch.dataset.set;
    ch.classList.toggle("on", state.set === s);
    ch.title = t("set_names." + s);
  });''',
              '''  renderSetRow();''')
    src = sub(src, '''  const gn = $("#setNote");
  if (gn){ gn.classList.toggle("hidden", state.set !== "green"); gn.textContent = t("green_note"); }''',
              '''  const gn = $("#setNote");
  if (gn){ gn.classList.toggle("hidden", state.theme !== "green"); gn.textContent = t("green_note"); }''')

    # ---- 7. set handling within a theme -------------------------------------
    src = sub(src, '''/* ===== sprite set (R/B mono · R/B color) ===== */
function toggleSet(s){
  if (!SPRITE_SETS[s]) return;
  state.set = s;
  save("pkd_rb_set", state.set);
  renderSpritePane();
  renderDetail();
}''',
              '''/* ===== sprite set (MONO / COLOR within the active game) ===== */
function toggleSet(s){
  if (!SPRITE_SETS[s]) return;
  if (THEMES[state.theme].sets.indexOf(s) === -1) return;   /* other games' sets live behind their theme */
  state.set = s;
  save("pkd_g1_set", state.set);
  renderSpritePane();
  renderDetail();
}
function renderThemeRow(){
  const el = $("#themeRow");
  if (!el) return;
  el.innerHTML = THEME_ORDER.map(th =>
    '<button class="tchip' + (state.theme === th ? " on" : "") + '" data-th="' + th +
    '" title="' + esc(t("theme_names." + th)) + '"><span class="dot"></span>' + esc(t("theme_short." + th)) + '</button>'
  ).join("");
}
function renderSetRow(){
  const el = $("#setRow");
  if (!el) return;
  el.innerHTML = THEMES[state.theme].sets.map(s =>
    '<button class="setchip' + (state.set === s ? " on" : "") + '" data-set="' + s +
    '" title="' + esc(t("set_names." + s)) + '">' +
    esc(SPRITE_SETS[s].color ? t("chip_color") : t("chip_mono")) + '</button>'
  ).join("");
}''')
    src = sub(src, '''/* ===== sprite set cycling (menu) ===== */
const SET_ORDER = ["rb", "rbc", "green"];
function cycleSet(){
  const i = SET_ORDER.indexOf(state.set);
  toggleSet(SET_ORDER[(i + 1) % SET_ORDER.length]);
}''',
              '''/* ===== sprite set cycling (menu) — within the active game ===== */
function cycleSet(){
  const order = THEMES[state.theme].sets;
  const i = order.indexOf(state.set);
  toggleSet(order[(i + 1) % order.length]);
}''')

    # ---- 8. dex text: R/B <-> YELLOW ---------------------------------------
    src = sub(src, '''function flavorPages(p){
  if (state.lang === "fa"){
    return p.flavor_fa ? [p.flavor_fa] : [(p.e1 || []).join(" ")];
  }
  const pgs = [];
  if (p.e1 && p.e1.length) pgs.push(p.e1.join(" "));
  if (p.e2 && p.e2.length) pgs.push(p.e2.join(" "));
  return pgs.length ? pgs : [""];
}''',
              '''function flavorPages(p){
  const yl = state.text === "y";
  const a = yl ? p.ey1 : p.e1, b = yl ? p.ey2 : p.e2;
  if (state.lang === "fa"){
    const fa = yl ? p.flavor_fa_y : p.flavor_fa;
    return fa ? [fa] : [((a) || []).join(" ")];
  }
  const pgs = [];
  if (a && a.length) pgs.push(a.join(" "));
  if (b && b.length) pgs.push(b.join(" "));
  return pgs.length ? pgs : [""];
}''')
    src = sub(src, '''    '<div class="sec"><div class="sec-t">' + esc(t("entry_t")) + '</div>' + flavorHtml + '</div>' +''',
              '''    '<div class="sec"><div class="sec-t"><span>' + esc(t("entry_t")) + '</span>' +
      '<span class="verSel" role="group" aria-label="' + esc(t("text_ver")) + '" title="' + esc(t("text_ver")) + '">' +
        '<button class="vbtn' + (state.text === "rb" ? " on" : "") + '" data-txt="rb">R/B</button>' +
        '<button class="vbtn' + (state.text === "y" ? " on" : "") + '" data-txt="y">YELLOW</button>' +
      '</span></div>' + flavorHtml + '</div>' +''')
    src = sub(src, '''  document.querySelectorAll("#detailPane .evo").forEach(el =>
    el.addEventListener("click", () => select(parseInt(el.dataset.id, 10))));''',
              '''  document.querySelectorAll("#detailPane [data-txt]").forEach(el =>
    el.addEventListener("click", () => { state.text = el.dataset.txt; save("pkd_g1_text", state.text); renderDetail(); }));
  document.querySelectorAll("#detailPane .evo").forEach(el =>
    el.addEventListener("click", () => select(parseInt(el.dataset.id, 10))));''')

    # ---- 9. storage keys ----------------------------------------------------
    for old, new in [
        ('save("pkd_rb_own", [...state.own]);', 'save("pkd_g1_own", [...state.own]);'),
        ('save("pkd_rb_favs", [...state.favs]);', 'save("pkd_g1_favs", [...state.favs]);'),
        ('save("pkd_rb_pal", state.pal);', 'save("pkd_g1_pal", state.pal);'),
        ('save("pkd_rb_set", state.set);', None),
        ('save("pkd_rb_back", state.back ? "back" : "front");', 'save("pkd_g1_back", state.back ? "back" : "front");'),
        ('save("pkd_rb_seen", [...state.seen]);', 'save("pkd_g1_seen", [...state.seen]);'),
        ('save("pkd_rb_seen", []); save("pkd_rb_own", []);', 'save("pkd_g1_seen", []); save("pkd_g1_own", []);'),
    ]:
        if new is not None:
            src = sub(src, old, new)
        else:
            assert src.count(old) == 0, f'stale ref still present: {old}'

    # ---- 10. menu: game entry + labels --------------------------------------
    src = sub(src, '''  $("#menuPop [data-act=set] span:last-child").textContent = tpl(t("m_set_tpl"), {v: t("set_names."+state.set)});''',
              '''  $("#menuPop [data-act=set] span:last-child").textContent = tpl(t("m_set_tpl"), {v: t("set_names."+state.set)});
  $("#menuPop [data-act=game] span:last-child").textContent = tpl(t("m_game_tpl"), {v: t("theme_short."+state.theme)});''')

    # ---- 11. events: theme row, keyboard T, menu game ------------------------
    src = sub(src, '''  $("#setRow").addEventListener("click", e => {
    const c = e.target.closest(".setchip");
    if (c) toggleSet(c.dataset.set);
  });''',
              '''  $("#setRow").addEventListener("click", e => {
    const c = e.target.closest(".setchip");
    if (c) toggleSet(c.dataset.set);
  });
  $("#themeRow").addEventListener("click", e => {
    const c = e.target.closest(".tchip");
    if (c) toggleTheme(c.dataset.th);
  });''')
    src = sub(src, '''    else if (act === "set") cycleSet();''',
              '''    else if (act === "set") cycleSet();
    else if (act === "game") cycleTheme();''')
    src = sub(src, '''    else if (e.key.toLowerCase() === "r") randomPick();''',
              '''    else if (e.key.toLowerCase() === "r") randomPick();
    else if (e.key.toLowerCase() === "t") cycleTheme();''')

    # ---- 12. init: apply theme before first paint ---------------------------
    src = sub(src, '''  applyPalette();
  applyLang();''',
              '''  applyPalette();
  applyTheme();
  applyLang();''')
    src = sub(src, '''  renderTabs(); renderChips(); renderList(); renderSpritePane(); renderDetail(); renderCounters();
  refreshMenuLabels();
  if (typeof MovesUI !== "undefined") MovesUI.applyLang();
  if (window.ItemsUI) ItemsUI.applyLang();''',
              '''  renderTabs(); renderChips(); renderList(); renderThemeRow(); renderSetRow(); renderSpritePane(); renderDetail(); renderCounters();
  refreshMenuLabels();
  const t1 = document.querySelector("#topbar .t1");
  if (t1) t1.textContent = t("theme_tag." + state.theme);
  if (typeof MovesUI !== "undefined") MovesUI.applyLang();''')

    # ---- 13. about text ------------------------------------------------------
    src = sub(src, 'about_p1:"A fan-made, offline Pokédex covering all 151 Pokémon of Generation I, styled after the in-game Pokédex of Pokémon Red/Blue. Data, sprites, cries and fonts live in local files next to the page — everything runs without internet.",',
              'about_p1:"A fan-made, offline Pokédex covering all 151 Pokémon of Generation I — all four Game Boy games in one dex. Data, sprites, cries and fonts live in local files next to the page — everything runs without internet.",')
    old_p3 = src[src.index('  about_p3:"Mark Pokémon'):]
    old_p3 = old_p3[:old_p3.index('",\n')]
    src = sub(src, old_p3,
              '  about_p3:"Mark Pokémon as Seen (automatic while browsing) and Owned (pokeball button) to fill your dex status, just like the game. The GAME chips (or key T) switch this dex between the four Gen-1 releases: RED and BLUE (the international pair), GREEN (the Japan-only 1996 version with its older artwork) and YELLOW (its own redrawn sprites and its own rewritten dex texts). Within each game the MONO / COLOR chips pick the sprite set, and every dex entry can be read in either the Red/Blue or the Yellow wording with the R/B · YELLOW selector. The Back button (key B) flips to the in-game back side.')
    old_p3fa = src[src.index('  about_p3:"با مرور هر پوکمون'):]
    old_p3fa = old_p3fa[:old_p3fa.index('",\n')]
    src = sub(src, old_p3fa,
              '  about_p3:"با مرور هر پوکمون، به‌طور خودکار «دیده‌شده» ثبت می‌شود و با دکمه پوکربال می‌توانید آن را «گرفته‌شده» علامت بزنید تا وضعیت پوکیدکس مثل خود بازی پر شود. متن توضیحات مثل بازی صفحه‌ور می‌خورد — روی جعبه متن کلیک کنید. چیپ‌های بازی (یا کلید T) این دکس را بین چهار نسخه‌ی نسل اول جابه‌جا می‌کنند: قرمز و آبی (نسخه‌های جهانی)، سبز (نسخه‌ی ۱۹۹۶ ژاپن با طرح‌های قدیمی‌تر) و زرد (اسپرایت‌های بازطراحی‌شده و متن‌های بازنویسی‌شده‌ی خودش). داخل هر بازی، چیپ‌های تک‌رنگ/رنگی مجموعه اسپرایت را عوض می‌کنند و با انتخابگر R/B · YELLOW می‌توان هر توضیح را با متن قرمز/آبی یا زرد خواند. دکمه پشت (کلید B) اسپرایت را به نمای پشت بازی برمی‌گرداند.')

    open(DST, 'w', encoding='utf-8').write(src)
    print(f'gen1.js written ({len(src.splitlines())} lines)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
