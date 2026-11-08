# Pokédex Plus — GENERATION III completion plan (phase tracker)

This file is the SINGLE SOURCE OF TRUTH for the Gen-3 build-out. The scheduled
runner (cron job `gen3-phases-runner`) reads it on every run, executes the
lowest-numbered phase whose status is not DONE, then commits + pushes and
updates the statuses below. Work through the phases IN ORDER.

## Golden rules (every phase, every run)

1. Repo: `/home/z/my-project/repos/pokedex` (branch `main`). Before starting:
   `git status` must be clean; if dirty, `git checkout -- .`; if clean,
   `git pull --ff-only origin main`.
2. GitHub token: `/home/z/my-project/.secrets/github_token` (saved, verified
   working, push scope). Push with:
   `git push https://x-access-token:$(cat /home/z/my-project/.secrets/github_token)@github.com/Ali-F-Harandi/pokedex.git main`
   NEVER print, echo, commit or expose the token anywhere.
3. References: `gen1.html` and `gen2.html` (+ their js/css) are the STRUCTURAL
   reference implementations — gen3 must match their layout, conventions and
   quality: same settings panel pattern, same i18n pattern (`I18N.en`/`I18N.fa`
   with identical key names wherever possible), same localStorage pattern with
   `pkd_g3_` prefix, same mobile reading order (DEX STATUS → search box →
   SETTINGS → Pokémon card → details) — and the mobile `#main` rule MUST use
   `align-items:stretch` (the b0e9a15 lesson: never let panels shrink to
   content width), same bilingual Pokémon NAME in the card (`.altName` under
   `#sprName`). Gen 3 may look a notch more refined (GBA era vs GBC era) but
   stays the same app family — nothing out-of-band.
4. EVERYTHING user-visible is bilingual EN/FA. FA strings live in the page's
   `I18N.fa`. Persian digits via the `num()` helper. FA layout = rtl via
   `body.fa`. Never ship placeholder UI — sections render real data or stay
   hidden (typeof-guards). Never invent data: the `pret` disassemblies are the
   source of record for gameplay data (wilds, learnsets, items, prices,
   levels); PokeAPI for per-version texts, forms, cross-checks and sprites;
   ALL Persian is hand-written (PokeAPI has no Persian).
5. Test before pushing: run the phase's test command(s) (playwright is
   installed; `playwright install firefox` when a phase needs Firefox). A
   phase is DONE only if its tests pass. Do a quick screenshot check of the
   pages touched. When seeding localStorage from tests remember `store()`
   JSON-parses — write values with `JSON.stringify`.
6. Commit style: one descriptive commit per phase. Update this file's status
   table + notes in the SAME commit. Then push.
7. If blocked >15 minutes: write the problem into the phase's notes, set
   status to `BLOCKED`, commit+push that, and continue with the NEXT phase
   if it doesn't depend on it. The next run retries.
8. Do not delete or rewrite Gen-1/Gen-2/emerald files. `emerald.js` is the
   legacy Gen-3 page's data and the DONOR for gen3-data.js — it stays in the
   repo untouched, forever. `emerald.html` becomes a redirect to gen3.html
   (copy the goldsilver.html redirect pattern), but emerald.js itself is
   never edited or removed.
9. After the LAST phase (status table all DONE): update README.md for Gen 3,
   then DELETE the cron job `gen3-phases-runner` (cron tool: action list →
   find id → delete). Do not leave the runner alive.

## Status table

| # | Phase | Status | Notes |
|---|-------|--------|-------|
| 1 | Landing + `gen3.html` unified dex (GBA styling, 5 themes RUBY/SAPPHIRE/EMERALD/FIRERED/LEAFGREEN, 386 data + per-game dex-text wordings R/S·EMERALD·FRLG, Deoxys per-game formes, full i18n + persistence) | DONE | see phase notes below |
| 2 | Sprite & cry completeness audit (every variant × 386) + fixes | DONE | see phase notes below |
| 3 | Moves Dex wiring (R/S · EMERALD · FRLG) + contest data + verification | DONE | see phase notes below |
| 4 | Item Dex wiring (Gen 3, per-game lists + prices, berries) + verification | TODO | |
| 5 | Location Dex + How to Catch — Hoenn (R/S/E) | TODO | |
| 6 | Location Dex + How to Catch — Kanto + Sevii (FRLG) | TODO | |
| 7 | Gen-3 signature: Ability Dex overlay + Natures (25, interactive) + contest polish | TODO | |
| 8 | Final QA (all-gen regression, VLM visual audit EN/FA, README, landing) + delete cron | TODO | |

## Phase details

### Phase 1 — Landing + gen3.html unified dex
Goal: the Gen-3 page itself, mirroring what gen2.html is for Gen 2.
- New files: `gen3.html`, `assets/css/gen3.css`, `assets/js/gen3.js`,
  `assets/js/gen3-data.js`, `tools/test-gen3.py` (+ build script
  `tools/build-gen3-data.py`). `emerald.html` becomes a redirect to
  `gen3.html` (copy the goldsilver.html pattern); landing: the Gen-3 card
  becomes GENERATION III — RUBY · SAPPHIRE · EMERALD · FIRERED · LEAFGREEN →
  `gen3.html` (update landing.js EN/FA strings; reuse
  `assets/img/featured-emerald.png` or a sibling), and update the
  `tools/test-order.py` assertions touched by the landing/redirect change.
- 5 themes + GBA-era styling, a notch more refined than gen2's GBC (wider
  GBA-style screen proportion, GBA wordmark, power LED). gen3.css owns it;
  gen1.css/gen2.css untouched. GAME chips grouped like gen2's:
  RUBY+SAPPHIRE share one cartridge group, EMERALD alone, FIRERED+LEAFGREEN
  share one. The THEME map in gen3.js swaps per game: sprite bank, dex-text
  wording, moves set (lands in phase 3), game label.
- Data (386): build gen3-data.js from the emerald.js donor (stats, types,
  HT/WT, egg, capture, happiness, growth, habitat, gender, legendary/mythical
  + FA names + FA genus + the Emerald-wording dex texts EN/FA) + PokeAPI
  species flavor texts for the R/S and FRLG wordings (version groups
  "ruby-sapphire" and "firered-leafgreen"); hand-translate FA for every
  unique new wording (dedupe identical wordings across the three games
  before translating — many entries are shared). Dex-text selector on the
  entry box: R/S ↔ EMERALD ↔ FRLG buttons (gen2's GOLD/SILVER/CRYSTAL
  pattern); a wording a game doesn't have in-game is not offered for it
  (never invent).
- Era corrections vs the donor (emerald.js is PokeAPI-generated, so fix):
  abilities — Gen 3 had NO hidden abilities: keep only the era 1-2 slots per
  mon, drop the `hidden` anachronism; Deoxys — forme is tied to the cartridge
  in Gen 3 (R/S=Normal, FIRERED=Attack, LEAFGREEN=Defense, EMERALD=Speed):
  per-forme stats from PokeAPI pokemon-forms; the card, stats and detail all
  follow the selected game chip, exactly like the real games; type chart =
  the gen2 one (Gen 3's chart is identical; the next change was Gen 5).
- Sprites: build `assets/sprites/gen3-rs{,-shiny,-back,-back-shiny}/` and
  `gen3-frlg{,-shiny,-back,-back-shiny}/` from the PokeAPI sprites repo
  (versions/generation-iii/ruby-sapphire and firered-leafgreen; fetch
  patterns from tools/build-sprites.py; token header if rate-limited).
  EMERALD chip: reuse the existing local `gen3-emerald-anim/` WebP set and
  extract stills into `gen3-emerald/` from its first frames (a small tools
  script; PokeAPI has no gen-3 emerald statics — era-authentic, Emerald's
  own dex animates). 64×64 uniform canvas, `image-rendering:pixelated`,
  SPRITE_SETS wiring like gen2.js.
- Cries: reuse `assets/audio/cries/1..251` as-is and fetch 252..386 from
  PokéAPI cries into the same folder (those species debuted in Gen 3); the
  cry button only renders when the file exists (phase 2 audits sizes).
- i18n EN/FA complete (reuse donor strings where possible + new GBA-era
  strings), persistence `pkd_g3_*` (theme/set/text/shiny/anim/back/lcd/
  favonly/sort/favs/seen/own), deep links `gen3.html#025`, mobile order +
  `align-items:stretch`, bilingual `.altName` card name, START menu with
  later-phase entries wired via typeof-guards (hidden until they land).
- Tests: tools/test-gen3.py — loads with no console errors, 386 count, theme
  swap repaints + swaps sprite bank + dex-text wording + label, Deoxys
  per-game forme stats (#386 EMERALD → Speed forme 50/95/90/95/90/180; FR →
  Attack 50/180/20/180/20/150), FA pass (RTL, Persian digits, .altName),
  persistence, mobile order, emerald.html redirect, landing card href.
  Regression: test-gen1, test-gen2, test-order all still green.

### Phase 1 — RESULT (2026-11-08, this run)
DONE in one run. Delivered: `gen3.html` + `assets/css/gen3.css` (GBA indigo
shell, GAME BOY ADVANCE wordmark, power LED, L/R shoulder buttons, wider
1460px layout, 5 theme layers with per-game chip groups R+S / E / FR+LG;
mobile `#main` keeps `align-items:stretch` — the b0e9a15 lesson) +
`assets/js/gen3.js` (I18N EN/FA complete, `pkd_g3_*` persistence, deep
links, 3-group game chips, ANIM = Emerald-only, wording selector that
grows RUBY/SAPPHIRE and FIRERED/LEAFGREEN buttons exactly where the games'
texts differ — 203 and 251 species respectively) + `assets/js/gen3-data.js`
(built by `tools/build-gen3-data.py` from the emerald.js donor + PokeAPI
cached species + `tools/gen3-fa-rs.json` — 386 hand-written Persian R/S
wordings; abilities are the ERA-TRUE slots parsed from the pokeemerald
`species_info.h` — 76 era abilities, Treecko=Overgrow only, Deoxys=Pressure;
Deoxys per-cartridge formes: Normal R/S, Attack FR, Defense LG, Speed EM,
per-game stats from PokeAPI forms and forme sprites 10013/10014/10015
stored in the frlg/rs banks, emerald bank's 386.png IS the Speed forme) +
`tools/build-gen3-sprites.py` (10 complete 64x64 banks: rs/frlg ×
front/shiny/back/back-shiny + emerald/emerald-shiny cut from the legacy
atlas — shiny rides atlas row-block 20; emerald BACK view reuses the rs
bank — pokeemerald back sprites verified byte-identical to pokeruby's) +
cries 252..386 fetched (1..251 untouched) + `emerald.html` redirect +
landing card/catalog/roadmap Gen-3 (landing.css got an `.fcard.em`
variant) + `tools/test-gen3.py` (61 checks) — full regression green:
gen3 61, gen2 103, gen2-order 9, gen2-sprites 30, gen1 24, order 20,
items 27, moves 44, locations 42.
STAGED to phase 2 (tracked there): the FRLG Persian wording group
(`fa_frlg`) — FA mode honestly falls back to the EN text for FRLG until
then (the gen2 fallback pattern); the Deoxys SPEED *animated* webp (the
anim set's 386.webp is still the normal forme; the still bank is correct).

### Phase 2 — RESULT (2026-11-08, this run)
DONE. `tools/test-gen3-sprites.py` (50 checks, all green) audits: 10 static
banks × their ids (exists / non-empty / PIL-decode / 64×64 / alpha in use;
rs banks +10015, frlg +10013+10014), full shiny≠normal pair diffs on all 5
shiny pairs, the Deoxys forme matrix, gen3-emerald-anim ×386 multi-frame,
cries 252..386 >2KB with 1..251 blob-identical to HEAD, SPRITE_SETS wiring,
and browser behavior (pixelated on #sprImg + evo sprites, webp PLAYS in
Chromium AND Firefox, every bank reachable through the UI on all three
cartridge groups, per-cartridge Deoxys routing).
FIXES the audit surfaced:
1. Real phase-1 bug: `gen3-emerald-shiny/386.png` was a back-view crop
   (back/shiny/10015 in the front-shiny slot). Emerald banks re-keyed to the
   uniform layout — 1..386 atlas stills (normal-forme 386 restored) + forme
   id **10015** carries the speed-forme views; `FORME_GAME.em` added so
   spriteId resolves EMERALD Deoxys to 10015 across front/back/shiny; the
   speed back normal is PokeAPI's genuine back/10015 (via rs-back bank).
2. PokeAPI shiny placeholders replaced with GENUINE era art (pokemondb,
   pixel-verified): speed shiny front (emerald + rs banks), speed shiny
   back (rs-back-shiny), and ruby-sapphire back-shiny Diglett 50 / Dugtrio
   51 (PokeAPI ships normal art there too). All wired into
   build-gen3-sprites.py (`forme_files` + `shiny_fixes`) — reproducible.
3. Documented exception (audited, whitelisted): the FRLG 10013/10014 shiny
   + back-shiny slots keep PokeAPI's placeholder-normal art — no authentic
   Gen-3 shiny attack/defense forme art exists anywhere (PokeAPI,
   pokemondb, Bulbagarden all checked 2026-11); inventing art is worse.
4. Deoxys anim guard: the anim bank's 386.webp is the NORMAL-forme rip and
   no genuine Emerald speed-forme ANIMATION could be sourced (Showdown's
   /ani is Gen-5 art; Spriters Resource is Cloudflare-gated; Bulbagarden
   403) — `animURL()` now returns "" for Deoxys, so the EMERALD chip shows
   the authentic Speed STILL instead of the wrong-forme animation. The
   other 385 animate as before.
5. fa_frlg delivered: `tools/gen3-fa-frlg.json` — 386 hand-written Persian
   FRLG wordings (all 386 differ from the R/S and Emerald wordings, so no
   dedupe reuse was possible), following the FIRERED wording like fa_rs
   follows RUBY; wired as the `fa_frlg` field by build-gen3-data.py
   (header updated); the phase-1 EN-fallback test now asserts Persian for
   both FIRERED and LEAFGREEN chips; +Deoxys anim-guard and speed-shiny
   checks in test-gen3.py.
6. build-gen3-data.py self-heals its gitignored cache now (fetches cached
   species JSONs + pret species.h/species_info.h on demand); the rebuild
   was diffed against the committed file — zero unexpected changes.
Regression: test-gen3-sprites 50/50 (new), test-gen3 64/64, gen2 103,
gen2-sprites 30, gen2-order 9, gen1 24, order 20, items 27, moves 44,
locations 42 — all green.
STAGED to later phases (not blockers): a genuine Emerald speed-forme
ANIMATION would still be welcome if a source surfaces (the guard makes the
chip correct meanwhile); the FRLG 10013/10014 shiny slots stay placeholders
until authentic art appears (if ever).

### Phase 2 — sprite & cry completeness audit (gen3)
- Audit every bank × 386: gen3-rs, gen3-rs-shiny, gen3-rs-back,
  gen3-rs-back-shiny, gen3-frlg (same four), gen3-emerald (extracted
  stills), gen3-emerald-anim (webp frames > 1); Deoxys forme sprites present
  in the right game's banks (Normal in rs, Attack in firered, Defense in
  leafgreen — same bank as firered with its own forme sprites, Speed in
  emerald).
- Checks: file exists, non-empty, decodes (PIL), RGBA alpha, shiny ≠ normal
  (full pair diff, like gen2's 753-pair audit), webp multi-frame + plays in
  Chromium AND Firefox, pixelated rendering on #sprImg/evo/list, cries
  252..386 > 2KB (and 1..251 untouched).
- Fix gaps via tools (build-sprites.py patterns). Write
  `tools/test-gen3-sprites.py`; run it + test-gen3.py.
- ALSO owed from phase 1: hand-write the FRLG Persian wording group
  (`fa_frlg`, 386 texts, dedupe FR==LG where shared) into
  tools/gen3-fa-frlg.json + build wiring + swap the phase-1 test's
  "falls back to EN" check to "is Persian"; and fetch/convert the Deoxys
  SPEED animated webp for gen3-emerald-anim (the anim still shows the
  normal forme on the EMERALD chip).

### Phase 3 — RESULT (2026-11-08, this run)
DONE. Delivered: `assets/js/moves-gen3.js` (MD_RS + MD_EM + MD_FRLG + `var MD`
— the gen2 merge pattern; built by `tools/build-gen3-moves.py` from the pret
decompiles pokeemerald/pokeruby/pokefirered + PokeAPI flavor texts) +
`assets/js/moves-fa-gen3.js` (`var MOVE_INFO` — 354 [EN, FA, EN-Emerald-base,
FA] rows; the shared moves-fa.js untouched). DATA (all era-verified against
three repos, pret slug ↔ PokeAPI slug cross-checked for all 354): 354 moves ×
3 games (power/type/accuracy/PP/priority; Gust=FLYING, Curse=???/"unknown"
TYPE_MYSTERY), level-up learnsets 386/386 PER GAME (internal→national species
id remap by name — Treecko is internal 277 in all three repos), egg moves,
TM/HM compat 386/386 with 50 TMs + 8 HMs per game (TM01=Focus Punch …
HM08=Dive), tutors: R/S none (verified — no tutor file in pokeruby),
Emerald 372 species (Battle Frontier), FRLG 372 (the 15 classic tutors) —
tutor tab renders only where the game has tutors. Contest data (R/S/E only,
from pret contest tables: category + appeal + jam hearts; FRLG has none —
authentically hidden, cell absent): Overheat=BEAUTY♥6, Pound=TOUGH♥4.
Per-game wordings: desc keyed per MD carrying only the wordings that differ
from the Emerald base (R/S 7 diffs, FRLG 352) — 686 unique EN wordings, all
686 hand-translated to Persian (`tools/gen3-moves-fa-desc-p1/2/3.json`),
103 hand-written FA names (252-354) + 251 reused from moves-fa.js where the
name is unchanged. FRLG Cape Brink ultimate-move tutor VERIFIED in
pokefirered field_specials.c (Venusaur/Charizard/Blastoise, friendship 255)
and noted EN/FA in the TM/HM view; Emerald BF note likewise.
WIRING: gen3.html loads moves.css + moves-gen3.js + moves-fa-gen3.js +
moves-module.js; gen3.js THEMES gained `moves` keys + `activeMoves()` +
applyTheme→MovesUI.setGame (label follows the cartridge like gen1/gen2);
START menu entries (Moves Dex / TM·HM) injected by the module; hotkey M
documented in the About box. moves-module.js got three backward-compatible,
typeof-guarded extensions (gen1/gen2 behavior untouched — all 9 suites
re-run green): per-game `MD.desc` fallback in move details, contest chip on
list cards + CONTEST cell on the detail card, gen3 tutor notes.
TESTS: tools/test-gen3.py extended to 91 checks (was 64): data integrity
(354/386/50+8 per game; every learnset row a real move id; every move has FA
name + FA desc; contest/tutor authenticity), START menu, section label per
cartridge, 354-card bilingual overlay, overlay VISIBILITY (getBoundingClientRect
— caught moves.css missing from gen3.html), era types, contest chip hearts,
per-game wording fallback, theme swap, FRLG no-contest, tutor notes, FA pass
(RTL, Persian Lv digits, Persian chip). Full regression: gen3 91, gen3-sprites
50, gen2 103, gen2-sprites 30, gen2-order 9, gen1 24, order 20, items 27,
moves 44, locations 42 — all green.

### Phase 3 — Moves Dex (R/S · EMERALD · FRLG) + contest data
- Data: 354 moves (Gen-3 total; ids 1-354). Era stats from pret move tables
  (pokeemerald; R/S = pokeruby, FRLG = pokefirered where they differ) —
  power/type/accuracy/PP/priority; EN descriptions per version group from
  PokeAPI move flavor texts (ruby-sapphire / emerald / firered-leafgreen).
  FA names (reuse moves-fa.js's 1-251 where the name is unchanged; 103 new
  names hand-written) + FA descriptions hand-written for all 354 Gen-3
  wordings (dedupe identical wordings across the three games first).
- One merged file `moves-gen3.js` (MD_RS + MD_EM + MD_FRLG + var MD —
  the gen2 merge pattern; the per-game sources can't coexist as-is).
  gen3.html loads moves-gen3.js + a new moves-fa-gen3.js (do not edit
  moves-fa.js — it serves gen1/gen2) + moves-module.js + moves.css;
  gen3.js pre-wires THEMES.moves + MovesUI.setGame following the theme.
- Learnsets per game from pret (level-up / egg / machine / tutor): R/S,
  Emerald (≈R/S + its own tutors), FRLG. TM/HM: 50 TMs + 8 HMs per game
  (verify each game's list from the disasm; Dive is the new HM08). Tutor
  lists per game from the disasm (Emerald and FRLG have tutors; R/S has
  none — verify); the tutor tab only shows where the game has tutors.
- Class: Gen 3 kept type-based physical/special (the split came in Gen 4) —
  move card class derived from the move's type, like gen1/gen2.
- Contest data (R/S/E only — FRLG has no contests, authentically hidden
  there): contest type (Cool/Beauty/Cute/Smart/Tough) + appeal + jam on
  every move card, from the pret contest tables; FA for the 5 contest types.
- Verify: every move has FA name + FA description; learnsets for all 386
  per game; label follows theme; TM/HM authentic per game; overlay lists
  354 bilingual cards; START menu entries; FA pass. Extend test-gen3.py
  (mirror gen2's moves checks).

### Phase 4 — Item Dex (Gen 3)
- Per-game item lists from pret item tables (pokeruby / pokeemerald /
  pokefirered) — R/S, Emerald, FRLG; prices per game from the disasm price
  fields (NOT PokeAPI's `cost`, which is the modern value); descriptions per
  version group from PokeAPI item flavor texts; FA names + FA descriptions
  hand-written (dedupe wordings). Machines stay in the TM/HM list.
- Cover: key items, hold items, medicine, and the full Gen-3 berry set with
  flavor profiles (spicy/dry/sweet/bitter/sour) from the pret berry data —
  flavors tie into contests and natures (cross-noted in phase 7).
- Icons: PokeAPI item menu sprites, color only — Gen 3 games were always
  color; NO GB/color icon toggle (unlike gen1/gen2) — note that honestly in
  the overlay footer EN/FA.
- Wiring: gen3.html loads `window.ITEM_DEX_CONFIG = { games:"rse-frlg",
  label:"R/S/E · FRLG", gen:3, icons:"color" }` + a NEW `items-gen3.js`
  (do not rewrite items-data.js, which serves gen1/gen2) + items-module.js
  (reused; extend only if the module needs a gen3 tweak — keep its API).
  Buy/sell columns per game, FA prices with Persian digits.
- Verify: counts per game, version-exclusives appear only on their games,
  FA pass. Extend test-gen3.py.

### Phase 5 — Location Dex + How to Catch — Hoenn (R/S/E)
- Sources: pokeruby (Ruby+Sapphire) + pokeemerald, raw.githubusercontent.com,
  cached under `tools/loc3-cache/` (gitignored). Prefer the
  `wild_encounter.json` at both repo roots: land (12-slot tables with the
  real percentages), surf, rock-smash, and the Old/Good/Super rod tables.
  Read maps/ + event scripts for the specials.
- All Hoenn encounter maps (~110 — take the real list from the json):
  routes 101-134, cities, caves (Rusturf, Granite, Meteor Falls, Jagged
  Pass, Sky Pillar, Victory Road, Sealed Chamber, Abandoned Ship, New
  Mauville, Mt. Pyre, Safari Zone areas, underwater routes 124-126, Shoal
  Cave tides noted).
- Per-game: ruby vs sapphire differ only in version-exclusive slots (dedupe
  like gen2: sapphire omitted when equal); emerald separate (tables AND
  swarms differ — Emerald has its own swarm table). Methods new in Gen 3:
  rock-smash encounters, underwater; NO time tabs (Gen 3 dropped day/night
  wilds — unlike gen2's module); swarm sections; fishing with bite chances;
  Feebas special note (Route 119, 6 random tiles; Milicot via beauty
  evolution — gen3 evo conditions incl. beauty and trade items Deep Sea
  Tooth/Scale).
- Specials curated from the disasm scripts (never from memory): starters
  (Birch, L5), egg gifts (Wynaut egg — location/level from the scripts),
  Beldum gift (Emerald-only — verify), trades per game (R/S vs Emerald
  differ), Mauville Game Corner prizes per game, Safari Zone per game,
  legendaries with authentic levels/conditions: Groudon (RUBY-only) /
  Kyogre (SAPPHIRE-only) Cave of Origin; EMERALD: both via Terra/Marine Cave
  (randomized spot — noted authentically); Rayquaza Sky Pillar; the Regi
  trio (Sealed Chamber braille → Desert Ruins / Island Cave / Ancient Tomb;
  per-game levels from data); Lati@s (R/S: one roams + the other via the
  Southern Island event; Emerald: the red/blue choice); EMERALD events:
  Aurora Ticket (Birth Island — Deoxys SPEED forme) and Old Sea Chart
  (Faraway Island — Mew). Version-lock authentically (Groudon never shows
  on the Sapphire dex).
- Output: `assets/js/locations-gen3.js` + `assets/js/locations-module3.js`
  (sister of gen2's module2, same LocUI global/API; new method badges
  rock-smash/underwater/swarm; NO time tabs). Wire into gen3.html + gen3.js
  (LocUI.syncGame on theme change). FA: every location name + method +
  special text EN/FA, Persian digits.
- HOW TO CATCH on every Pokémon mirrors gen1/gen2 (evolve paths with gen3
  conditions: beauty, trade items, friendship; impossible-in-that-game says
  so and names the games that have it).
- Extend test-gen3.py (locations data + section + overlay + per-game
  legendary levels/locks + FA). If the full Hoenn set is too large for one
  run: land what is real, note the remainder in the tracker (BLOCKED),
  the next run finishes — never placeholder rows.

### Phase 6 — Location Dex + How to Catch — Kanto + Sevii (FRLG)
- Source: pokefirered (IF DEF(_FIRERED)/ELIF DEF(_LEAFGREEN)), same cache.
  FRLG's Kanto is redesigned vs Gen 1 — build its own tables; never reuse
  the gen1 locations data.
- Cover: all Kanto routes/cities/caves (Safari Zone FRLG areas, Seafoam,
  Power Plant, Pokémon Tower, Cerulean Cave — Mewtwo L70), Mt. Ember
  (Moltres + the Ruby/Sapphire item quest noted), the roaming beasts (which
  beast roams depends on the starter — the authentic rule from the
  scripts), Navel Rock event (Ho-Oh + Lugia — levels from data), Birth
  Island (Deoxys: FIRERED=Attack / LEAFGREEN=Defense forme, L30), trades
  (FRLG's own set — differs from Gen 1's), Celadon Game Corner (FRLG
  prizes), starters from Oak, the Magikarp salesman (verify from scripts),
  Sevii Islands: One/Two/Three (Berry Forest, Mt. Ember areas) + post-E4
  Four-Seven (Tanoby Ruins Unown rooms with their letter sets, Altering
  Cave event-only note, Trainer Tower no wilds).
- Wire into the SAME gen3 locations overlay (region chips HOENN / KANTO —
  Sevii under Kanto or its own chip, following the module's pattern).
- FA everything; extend test-gen3.py (FRLG Kanto tables differ from gen1's —
  assert a known difference; Sevii present; Deoxys FR=Attack/LG=Defense
  formes; per-starter roaming rule).

### Phase 7 — Gen-3 signature: Ability Dex + Natures + contest polish
- Abilities (era-authentic): per-mon 1-2 slots, NO hidden (already fixed in
  phase 1); the era ability list from pokeemerald (~76 — take the real
  list; defined-but-unused ones like Cacophony noted honestly). FA names +
  one-line FA effects (reuse the donor ability table's FA where present —
  verify; hand-write the rest).
- NEW Ability Dex overlay — gen3's fourth dex (Moves `M` / Items `I` /
  Locations `L`): every ability card with its effect EN/FA + which Pokémon
  have it (slot 1 / slot 2 lists); START menu entry + a free hotkey (e.g.
  `Y` — must not collide with S/A/B/R/T/C/M/I/L); document it in the About
  box EN/FA.
- Natures: 25, FA names hand-written; interactive nature selector on the
  stat panel — picking a nature shows +10%/−10% arrows on the affected base
  stats (EN/FA labels, Persian digits), neutral natures noted; each nature's
  liked/disliked berry flavor (PokeAPI /nature preferred flavor) shown as a
  Pokéblock-era tie-in. Cross-note: berry flavors in the Item Dex and
  contest types on move cards get a short explainer EN/FA.
- Extend test-gen3.py: ability overlay counts, per-mon slots (no hidden
  anywhere), nature math (+10%/−10% on base stats, neutral = unchanged),
  FA pass.

### Phase 8 — Final QA + ship
- Run EVERYTHING: test-gen1, test-gen2, test-gen3, test-order,
  test-gen2-order, test-items, test-moves, test-locations,
  test-gen2-sprites, test-gen3-sprites — all green.
- Playwright screenshots of gen3.html: mobile 390 EN+FA, desktop 1440, all
  5 themes; audit with `z-ai vision` — mobile order, bilingual name, no
  overlap/overflow, RTL sane. Remember: seed localStorage with
  JSON.stringify values; mobile #main keeps align-items:stretch.
- Landing final look: generations ordered 1→2→3, Gen-3 card → gen3.html,
  counts updated, FA complete; emerald.html redirect verified.
- README.md: Gen-3 section mirroring the Gen-2 section's structure; roadmap
  + structure + built-with updated.
- Verify the live deploy: poll the Pages builds API (token header) until
  `built`, then curl gen3.html / gen3.js / gen3.css from the live URL and
  md5-compare to local.
- Mark the table all DONE, commit, push — then DELETE the cron job
  `gen3-phases-runner` (cron tool: list → id → delete). Confirm deletion.
  Leave a short summary in the final commit message.

## Environment facts (for the runs)

- Sandbox: Linux, python3 + node + playwright (chromium installed).
  `playwright install firefox` when a phase needs it.
- The repo persists at `/home/z/my-project/repos/pokedex` between runs.
  Nothing else persists — do not rely on running processes.
- Live site: https://ali-f-harandi.github.io/pokedex/ (GitHub Pages from
  `main` root). Deploys ~30 s; transient build failures = GitHub hiccup,
  re-run via the Actions API if needed.
- Data sources:
  - pret disassemblies (raw.githubusercontent.com/pret/...): `pokeruby`
    (Ruby+Sapphire), `pokeemerald`, `pokefirered` (FireRed+LeafGreen).
    Cache raw files under `tools/loc3-cache/` and `tools/gen3-cache/` —
    both gitignored.
  - PokeAPI (https://pokeapi.co/api/v2/): species flavor texts per version
    group ("ruby-sapphire", "emerald", "firered-leafgreen"), pokemon-forms
    (Deoxys), /nature, /contest-type, /berry, /move, /item flavor texts;
    sprites repo paths versions/generation-iii/{ruby-sapphire,
    firered-leafgreen}. If rate-limited, retry with the GitHub token as an
    Authorization header.
  - `assets/js/emerald.js`: the legacy donor — stats/types/HT/WT/abilities/
    egg/capture/growth/habitat/gender for 386 + FA names + FA genus + FA
    Emerald-wording dex texts + an ability table.
    `assets/img/emerald-atlas.png` + `assets/sprites/gen3-emerald-anim/`
    are the emerald page's sprite sets.
- Gen-3 era facts (verify from data, never trust memory): 354 moves;
  50 TMs + 8 HMs (Dive is the new HM08); physical/special still derived
  from the move's TYPE (no stat split until Gen 4); type chart identical
  to Gen 2's; NO hidden abilities; NO time-of-day wilds (day/night wilds
  returned in Gen 4); Deoxys forme tied to the cartridge (R/S=Normal,
  FR=Attack, LG=Defense, E=Speed); contests exist only in R/S/E.
- cries: `assets/audio/cries/` has 1..251 (the gen1/gen2 pages only ever
  reference those). gen3 extends the folder with 252..386 (PokéAPI) —
  the gen1/gen2 pages are unaffected.
- The `I18N` convention: every new user-visible string needs an `fa` twin.
  Persian digits via `num()`. FA layout = rtl via `body.fa`.
- CSS: gen3.css owns the GBA-era look. gen1.css / gen2.css / the emerald
  page's css stay untouched.
