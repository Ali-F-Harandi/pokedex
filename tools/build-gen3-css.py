#!/usr/bin/env python3
"""Derive assets/css/gen3.css from assets/css/gen2.css (phase 1).

gen2.css is the structural reference; gen3.css keeps the whole component
family and re-skins the IDENTITY layer for the Game Boy Advance era:
  · indigo GBA shell, "GAME BOY ADVANCE" wordmark, power LED,
    decorative L/R shoulder buttons (the GBA's signature)
  · wider screen proportion (GBA vs GBC)
  · FIVE theme layers — Ruby / Sapphire / Emerald / FireRed / LeafGreen —
    grouped R+S, E, FR+LG like the cartridges
The gen2-specific Location-Dex extension block at the tail is dropped
(gen-3's own lands with phase 5/6). gen1.css / gen2.css stay untouched.
"""
import re

REPO = '/home/z/my-project/repos/pokedex'
src = open(f'{REPO}/assets/css/gen2.css', encoding='utf-8').read()

def cut(start_marker, end_marker, s=None, keep_end=True):
    """Return (before, block, after)."""
    s = src if s is None else s
    a = s.index(start_marker)
    b = s.index(end_marker, a)
    return s[:a], s[a:b], s[b:] if keep_end else ''

# ---------- 1. replace the header comment + :root + shell/wordmark/LED ----------
_, head_old, rest = cut('/* ============ Pokémon Gold/Silver/Crystal',
                        '#screen > *{position:relative;z-index:1}')
head_new = '''/* ============ Pokémon Ruby/Sapphire/Emerald/FireRed/LeafGreen in-game
   Pokédex — web edition ============
   The Gen-2 dex, one console generation later: the same structure and
   layout, dressed as the Game Boy ADVANCE — the indigo translucent shell,
   the GAME BOY ADVANCE wordmark, a power LED and — the GBA's signature —
   L / R shoulder buttons over the screen. Switching the GAME chips
   (RUBY · SAPPHIRE · EMERALD · FIRERED · LEAFGREEN) slides a different
   cartridge into the same console, like the Gen-2 dex's three GBC games. */
:root{
  --shell-a:#6a6ab8; --shell-b:#3c3c8c; --deep:#101024;
  --screen:#d4d4c8; --screen-line:#c0c0b2;
  --panel:#fdfef6; --panel-edge:#bcc6a6; --panel-edge-d:#7e8a6c;
  --ink:#212b18; --ink-soft:#5c6753; --ink-faint:#8d9683;
  --red:#c84454; --red-deep:#8c1c2c; --sel-a:#d86a74; --sel-b:#98303c;
  --gold:#e8b840; --gold-d:#a87814;
  --ball-red:#d84038;
  --head-a:#44449a; --head-b:#2c2c6e;
  --foot-a:#383880; --foot-b:#24245a;
  --row-line:#e2e6d4; --num:#5e6a58;
  --sprbg:#f1f2ee;
  --stat-hp:#f0a030; --stat-atk:#e05038; --stat-def:#4890d0;
  --stat-spa:#a870d8; --stat-spd:#58b868; --stat-spe:#f0d048;
  --font-px:'PS2P','Courier New',monospace;
  --font-fa:'Vazirmatn',Tahoma,'Segoe UI',sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{margin:0;padding:0}
body{
  font-family:var(--font-fa);
  background:
    radial-gradient(1100px 640px at 50% -8%, #2c2c58, transparent 60%),
    radial-gradient(900px 560px at 94% 108%, #1a1a3a, transparent 55%),
    var(--deep);
  color:#e8ecf0;
  min-height:100vh;
  padding:20px 12px 30px;
}
body.dopen{overflow:hidden}
.hidden{display:none!important}
bdi{unicode-bidi:isolate}

/* ---------- shell (Game Boy Advance: indigo + wordmark + shoulders) ----------
   A notch more refined than the Gen-2 Game Boy Color: the GBA is wider,
   its screen is landscape, and it introduced the L/R shoulder buttons. */
#shell{
  max-width:1460px;margin:0 auto;
  background:linear-gradient(180deg,var(--shell-a),var(--shell-b));
  border:4px solid #22224a;border-radius:30px;
  box-shadow:0 30px 70px rgba(0,0,0,.62), inset 0 2px 0 rgba(255,255,255,.30), inset 0 -6px 0 rgba(0,0,0,.3);
  padding:56px 10px 10px;
  position:relative;
}
/* GBA bezel: the GAME BOY ADVANCE wordmark above the screen */
#shell::before{
  content:"GAME BOY ADVANCE";
  position:absolute;top:15px;left:0;right:0;text-align:center;
  font-family:var(--font-px);font-size:9px;letter-spacing:4px;direction:ltr;
  background:linear-gradient(90deg,
    #e8e4f6 0 30%, #b8b4d8 30% 55%, #d8d4ec 55% 78%, #a8a4cc 78% 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent;
  pointer-events:none;z-index:5;
}
/* GBA power LED, left of the wordmark */
#shell::after{
  content:"";position:absolute;top:17px;left:26px;width:9px;height:9px;border-radius:50%;
  background:radial-gradient(circle at 35% 30%, #c8f0a8, #48a838 60%, #1c5c14);
  box-shadow:0 0 6px rgba(120,255,120,.55), inset 0 -1px 2px rgba(0,0,0,.5);
  pointer-events:none;z-index:5;
}
/* L / R shoulder buttons — the GBA's own innovation, resting above the shell */
.shoulder{
  position:absolute;top:-4px;z-index:6;pointer-events:none;
  font-family:var(--font-px);font-size:9px;color:rgba(255,255,255,.85);
  background:linear-gradient(180deg,var(--shell-a),var(--shell-b));
  border:3px solid #22224a;border-bottom:0;
  border-radius:14px 14px 0 0;
  padding:8px 26px 14px;
  box-shadow:inset 0 2px 0 rgba(255,255,255,.3);
}
.shoulder.l{left:34px}
.shoulder.r{right:34px}
#screen{
  background:var(--screen);border-radius:16px;border:4px solid #1e1e3e;
  box-shadow:inset 0 0 0 2px rgba(255,255,255,.5), inset 0 0 46px rgba(50,55,70,.22);
  overflow:hidden;position:relative;color:var(--ink);
  transition:background .25s;
}
#screen::after{ /* soft LCD scanlines */
  content:"";position:absolute;inset:0;pointer-events:none;z-index:0;
  background:repeating-linear-gradient(0deg, rgba(0,0,0,.025) 0 2px, transparent 2px 4px);
}
#screen > *{position:relative;z-index:1}'''

# ---------- 2. the five-theme section replaces gen2's theme section ----------
_, themes_old, rest2 = cut('/* ============================================================\n   GENERATION II — one dex, three games',
                           '/* ============================================================\n   GEN II — settings panel', rest)
themes_new = '''/* ============================================================
   GENERATION III — one dex, five games (gen3.css additions)
   RUBY / SAPPHIRE / EMERALD / FIRERED / LEAFGREEN theme switcher
   + the per-game dex-text selector.
   ============================================================ */

/* ---- theme variable layers ----
   Every game repaints the WHOLE dex, like sliding a different cartridge
   into the same Game Boy Advance. A notch more refined than the Gen-2
   GBC dex: each game tints the screen glass itself — and the GBA shell
   was translucent, so the games' own colors run through the plastic. */
/* RUBY — Pokémon Ruby: crimson shell, warm screen */
body.theme-ruby{
  --shell-a:#d86878; --shell-b:#982840; --deep:#200a10;
  --head-a:#98404c; --head-b:#6c2430;
  --foot-a:#84303c; --foot-b:#581c26;
  --red:#c84854; --red-deep:#8c1c28; --sel-a:#d87078; --sel-b:#a03038;
  --screen:#dcd0c8; --screen-line:#c8bab2;
  --row-line:#eee0da; --num:#7c5a52;
  --panel-edge:#d4bcb4; --panel-edge-d:#947068;
  background:
    radial-gradient(1100px 640px at 50% -8%, #441018, transparent 60%),
    radial-gradient(900px 560px at 94% 108%, #2c0a10, transparent 55%),
    var(--deep);
}
/* SAPPHIRE — Pokémon Sapphire: deep-blue shell, cool screen */
body.theme-sapphire{
  --shell-a:#6878d8; --shell-b:#3048a8; --deep:#0a1028;
  --head-a:#4050a8; --head-b:#2a3478;
  --foot-a:#344494; --foot-b:#222c64;
  --red:#4878c8; --red-deep:#285094; --sel-a:#6888dc; --sel-b:#3858ac;
  --screen:#ccd2e0; --screen-line:#b6bccc;
  --row-line:#dce2f0; --num:#525a78;
  --panel-edge:#b0b8d4; --panel-edge-d:#6a7294;
  background:
    radial-gradient(1100px 640px at 50% -8%, #141c44, transparent 60%),
    radial-gradient(900px 560px at 94% 108%, #0c122c, transparent 55%),
    var(--deep);
}
/* EMERALD — Pokémon Emerald: emerald shell, jade screen */
body.theme-emerald{
  --shell-a:#58b878; --shell-b:#1c7848; --deep:#06221a;
  --head-a:#2c8458; --head-b:#1c5e3c;
  --foot-a:#247450; --foot-b:#164e34;
  --red:#38a868; --red-deep:#1c7844; --sel-a:#58c080; --sel-b:#288854;
  --screen:#ccd8cc; --screen-line:#b6c4b8;
  --row-line:#dbe8dc; --num:#4e6a56;
  --panel-edge:#accabc; --panel-edge-d:#648a70;
  background:
    radial-gradient(1100px 640px at 50% -8%, #0e3a28, transparent 60%),
    radial-gradient(900px 560px at 94% 108%, #082a1c, transparent 55%),
    var(--deep);
}
/* FIRERED — Pokémon FireRed: ember shell, warm screen */
body.theme-firered{
  --shell-a:#e89868; --shell-b:#b04818; --deep:#240e04;
  --head-a:#a85828; --head-b:#7c3a14;
  --foot-a:#94481c; --foot-b:#682f10;
  --red:#d86838; --red-deep:#a03c14; --sel-a:#e88048; --sel-b:#b84c1c;
  --screen:#dccec0; --screen-line:#c8b8a8;
  --row-line:#f0e2d4; --num:#7c6250;
  --panel-edge:#d4c0ac; --panel-edge-d:#94785c;
  background:
    radial-gradient(1100px 640px at 50% -8%, #441c08, transparent 60%),
    radial-gradient(900px 560px at 94% 108%, #2c1204, transparent 55%),
    var(--deep);
}
/* LEAFGREEN — Pokémon LeafGreen: leaf shell, fresh screen */
body.theme-leafgreen{
  --shell-a:#a8cc68; --shell-b:#5c9028; --deep:#141e06;
  --head-a:#6c9030; --head-b:#4c681c;
  --foot-a:#5c8028; --foot-b:#3c5a18;
  --red:#78a838; --red-deep:#4c7818; --sel-a:#94c048; --sel-b:#628c20;
  --screen:#d4dcc0; --screen-line:#c0c8aa;
  --row-line:#e8f0d8; --num:#5e6a48;
  --panel-edge:#c0ccA0; --panel-edge-d:#828e58;
  background:
    radial-gradient(1100px 640px at 50% -8%, #223208, transparent 60%),
    radial-gradient(900px 560px at 94% 108%, #162006, transparent 55%),
    var(--deep);
}
/* shell + header/footer follow the game smoothly */
#shell{transition:background .3s}
/* themed "on" chips per game */
body.theme-ruby .tab.on, body.theme-ruby .mbtn.on, body.theme-ruby .sbtn.on,
body.theme-ruby .setchip.on, body.theme-ruby .btn.on, body.theme-ruby .vbtn.on, body.theme-ruby .tchip.on, body.theme-ruby .lcdchip.on{
  background:linear-gradient(180deg,#e898a0,#b83848);color:#3c0810;border-color:#982038;
}
body.theme-sapphire .tab.on, body.theme-sapphire .mbtn.on, body.theme-sapphire .sbtn.on,
body.theme-sapphire .setchip.on, body.theme-sapphire .btn.on, body.theme-sapphire .vbtn.on, body.theme-sapphire .tchip.on, body.theme-sapphire .lcdchip.on{
  background:linear-gradient(180deg,#98a8ec,#4860c0);color:#0c1440;border-color:#3048a0;
}
body.theme-emerald .tab.on, body.theme-emerald .mbtn.on, body.theme-emerald .sbtn.on,
body.theme-emerald .setchip.on, body.theme-emerald .btn.on, body.theme-emerald .vbtn.on, body.theme-emerald .tchip.on, body.theme-emerald .lcdchip.on{
  background:linear-gradient(180deg,#88dca4,#2c9c58);color:#04301c;border-color:#1c7844;
}
body.theme-firered .tab.on, body.theme-firered .mbtn.on, body.theme-firered .sbtn.on,
body.theme-firered .setchip.on, body.theme-firered .btn.on, body.theme-firered .vbtn.on, body.theme-firered .tchip.on, body.theme-firered .lcdchip.on{
  background:linear-gradient(180deg,#f8b880,#cc6828);color:#431804;border-color:#a04c14;
}
body.theme-leafgreen .tab.on, body.theme-leafgreen .mbtn.on, body.theme-leafgreen .sbtn.on,
body.theme-leafgreen .setchip.on, body.theme-leafgreen .btn.on, body.theme-leafgreen .vbtn.on, body.theme-leafgreen .tchip.on, body.theme-leafgreen .lcdchip.on{
  background:linear-gradient(180deg,#c8e488,#84b438);color:#1e3208;border-color:#5c8820;
}
/* the brand chip rides the game colour */
body.theme-ruby .dexlogo{background:linear-gradient(180deg,#d8707c,#a02840);border-color:#7c1830}
body.theme-ruby .dexlogo .l2{color:#fcdce0;text-shadow:1px 1px 0 #7c1830}
body.theme-sapphire .dexlogo{background:linear-gradient(180deg,#7888e0,#3850b0);border-color:#243684}
body.theme-sapphire .dexlogo .l2{color:#dce4fc;text-shadow:1px 1px 0 #243684}
body.theme-emerald .dexlogo{background:linear-gradient(180deg,#68c888,#228850);border-color:#166338}
body.theme-emerald .dexlogo .l2{color:#d8f5e2;text-shadow:1px 1px 0 #166338}
body.theme-firered .dexlogo{background:linear-gradient(180deg,#f0a060,#c05818);border-color:#8c3c0c}
body.theme-firered .dexlogo .l2{color:#fde8d0;text-shadow:1px 1px 0 #8c3c0c}
body.theme-leafgreen .dexlogo{background:linear-gradient(180deg,#a8d060,#68a028);border-color:#4a7818}
body.theme-leafgreen .dexlogo .l2{color:#eaf6d0;text-shadow:1px 1px 0 #4a7818}

/* ---- theme switcher row (game selector) ----
   RUBY + SAPPHIRE share one cartridge group, EMERALD gets its own,
   FIRERED + LEAFGREEN share one — the real Gen-3 cartridge pairs. */
.gcGames{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;direction:ltr}
.tchip{
  font-family:var(--font-px);font-size:7px;letter-spacing:.5px;direction:ltr;
  color:var(--ink-soft);background:#f5f8ee;border:2px solid var(--panel-edge-d);
  border-radius:8px;padding:4px 7px;cursor:pointer;line-height:1.4;position:relative;
}
body.fa .tchip{font-family:var(--font-fa);font-size:10px;letter-spacing:0}
.tchip:hover{border-color:var(--gold);color:var(--ink)}
.tchip .dot{display:inline-block;width:8px;height:8px;border-radius:2px;margin-inline-end:4px;vertical-align:-1px;border:1px solid rgba(0,0,0,.35)}
.tchip[data-th=ruby] .dot{background:#c84858}
.tchip[data-th=sapphire] .dot{background:#4878d0}
.tchip[data-th=emerald] .dot{background:#38a868}
.tchip[data-th=emerald]{border-color:#2c8458}
.tchip[data-th=firered] .dot{background:#e07030}
.tchip[data-th=leafgreen] .dot{background:#84b438}

/* ---- R/S · EMERALD · FRLG dex-text selector (per-game wordings) ---- */
.verSel{display:inline-flex;gap:4px;margin-inline-start:auto}
.vbtn{
  font-family:var(--font-px);font-size:7px;letter-spacing:.5px;direction:ltr;cursor:pointer;
  color:var(--ink-soft);background:#f5f8ee;border:2px solid var(--panel-edge-d);
  border-radius:7px;padding:3px 6px;line-height:1.4;
}
body.fa .vbtn{font-family:var(--font-fa);font-size:10px;letter-spacing:0}
.vbtn:hover{border-color:var(--gold);color:var(--ink)}
.vbtn.on{background:linear-gradient(180deg,#ffd95e,#e8a613);color:#4d3500;border-color:#a06c00}
.sec-t .verSel{transform:translateY(-2px)}

'''

# ---------- 3. drop the gen2 locations tail, add the gen3 note ----------
_a = rest2.index('/* ============ Location Dex (phase 5) — gen-2 extensions ============')
tail_old = rest2[_a:]
tail_new = '''/* ============================================================
   GEN III — phase-1 base. The Ability Dex, Natures, contest data
   and the gen-3 Location Dex extensions join in phases 3–7 and
   will append here, mirroring how gen2.css grew phase by phase.
   ============================================================ */
'''

out = head_new + themes_new + tail_new
# append the untouched component family (topbar → about → mobile), i.e.
# everything from the topbar comment up to the gen2 theme section,
# plus the settings/lcd section that follows it.
_, mid, _ = cut('/* ---------- top bar ---------- */',
                '/* ============================================================\n   GENERATION II — one dex, three games', src)
# settings/lcd section (between the verSel end and the gen2 locations tail)
_, setcss, _ = cut('/* ============================================================\n   GEN II — settings panel',
                   '/* ============ Location Dex (phase 5) — gen-2 extensions ============', rest2)
# retitle the settings section header for gen3
setcss = setcss.replace('GEN II — settings panel', 'GEN III — settings panel (game groups · sprite options · LCD)')
setcss = setcss.replace('in-card extras for mobile (flavor · HT/WT · swipe hint)',
                        'in-card extras for mobile (flavor · HT/WT · swipe hint)')
# gen2 crystal anim comments → gen3 emerald anim wording
setcss = setcss.replace('GOLD + SILVER share one cartridge, CRYSTAL gets its own',
                        'RUBY + SAPPHIRE share one cartridge, EMERALD and the FR/LG pair get theirs')
out = out.replace('/* L / R shoulder buttons', mid + setcss + '''
/* L / R shoulder buttons''', 1)

# ---------- 4. wider GBA grid (one notch wider than gen2's 352/246) ----------
out = out.replace('grid-template-columns:352px 246px 1fr;', 'grid-template-columns:366px 252px 1fr;')
# the wordmark overflow guard on phones
out = out.replace('#shell::before{top:9px;font-size:7.5px;letter-spacing:2px}',
                  '#shell::before{top:11px;font-size:6.5px;letter-spacing:2.5px}')
out = out.replace('#shell::after{top:10px;left:14px;width:7px;height:7px}',
                  '#shell::after{top:12px;left:14px;width:7px;height:7px}')
out = out.replace('#shell{border-radius:16px;padding:32px 7px 7px}',
                  '#shell{border-radius:20px;padding:38px 7px 7px}')
out = out.replace('#screen{background:var(--screen);border-radius:16px;border:4px solid #1e1e3e;',
                  '#screen{background:var(--screen);border-radius:13px;border:3px solid #1e1e3e;')

open(f'{REPO}/assets/css/gen3.css', 'w', encoding='utf-8').write(out)
print('gen3.css written:', len(out), 'bytes')
