# Pokédex Plus — GENERATION II completion plan (phase tracker)

This file is the SINGLE SOURCE OF TRUTH for the Gen-2 build-out. The scheduled
runner (cron job `gen2-phases-runner`) reads it on every run, executes the
lowest-numbered phase whose status is not DONE, then commits + pushes and
updates the statuses below. Work through the phases IN ORDER.

## Golden rules (every phase, every run)

1. Repo: `/home/z/my-project/repos/pokedex` (branch `main`). Before starting:
   `git status` must be clean; if dirty, `git checkout -- .` (or stash), then
   `git fetch origin && git reset --hard origin/main` only if local == remote
   ancestor. Keep it simple: if clean, `git pull --ff-only origin main`.
2. GitHub token: `/home/z/my-project/.secrets/github_token` (already saved,
   verified working). Push with:
   `git push https://x-access-token:$(cat /home/z/my-project/.secrets/github_token)@github.com/Ali-F-Harandi/pokedex.git main`
   NEVER print, echo, commit or expose the token anywhere.
3. Gen 1 (`gen1.html` + `assets/js/gen1.js` + `assets/css/gen1.css`) is the
   reference implementation. Every Gen-2 feature must match its structure,
   conventions and quality — same layout, same settings panel pattern, same
   i18n pattern (`I18N.en` / `I18N.fa` with identical key names wherever
   possible), same localStorage pattern with `pkd_g2_` prefix, same mobile
   reading order (DEX STATUS → search box → SETTINGS → Pokémon card → details),
   same bilingual Pokémon NAME in the card (`.altName` under `#sprName`).
   Gen 2 is ALLOWED to look a notch more refined (GBC era vs DMG era) but must
   stay the same app family. Nothing out-of-band.
4. EVERYTHING user-visible is bilingual EN/FA (names, labels, descriptions,
   notes, tests include an FA pass). FA strings live in the page's `I18N.fa`.
5. Test before pushing: run the phase's test command(s) (playwright is
   installed). A phase is DONE only if its tests pass. Also do a quick
   screenshot check for the pages you touched.
6. Commit style: one descriptive commit per phase, like the existing history
   (subject line + details). Update this file's status table + notes in the
   SAME commit. Then push.
7. If something blocks you >15 minutes: write the problem into the phase's
   notes, set status to `BLOCKED`, commit+push that, and continue with the
   NEXT phase if it doesn't depend on it. The next run retries.
8. Do not delete or rewrite Gen-1 files. Do not remove `goldsilver.js` /
   `crystal.js` (they are the data source of record for `gen2-data.js`).
9. After the LAST phase (status table all DONE): update README.md for Gen 2,
   then DELETE the cron job named `gen2-phases-runner` (cron tool, action
   delete / find the job id via list). Do not leave the runner alive.

## Status table

| # | Phase | Status | Notes |
|---|-------|--------|-------|
| 1 | Landing by generations + `gen2.html` unified dex (GBC styling, 3 themes, data, sprites incl. shiny/back/anim, corrected Gen-2 type chart, full i18n + persistence) | DONE (see git log: "Gen 2 unified dex…") | Built in the session that set up this plan |
| 2 | Sprite & cry completeness audit (every variant × 251) + fixes | DONE | tools/test-gen2-sprites.py 30/30 — all 12 static banks ×251 (exists/size/PIL decode/RGBA alpha), 251 animated webp all multi-frame, cries 1..251 >2KB, SPRITE_SETS wiring verified; 0 of 753 shiny sprites identical to normal (front+back, 3 games); pixelated rendering confirmed on #sprImg/evo/list; webp playback proven by pixel-diff in Chromium AND Firefox (playwright firefox installed for the audit) |
| 3 | Moves Dex wiring (GOLD/SILVER · CRYSTAL) + verification | TODO | |
| 4 | Item Dex wiring (games "gc", gen 2) + verification | TODO | |
| 5 | How to Catch + Location Dex (Johto & Kanto, G/S/C) | TODO | biggest data phase — start early, see notes |
| 6 | Final QA (all-gen regression, VLM visual audit EN/FA, README, landing) + delete cron | TODO | |

Phase 1 was already completed together with this plan (landing reorganization
by generations, gen2.html + assets/js/gen2.js + assets/css/gen1.css-family
gen2.css + assets/js/gen2-data.js + tools/test-gen2.py + redirects from
goldsilver.html / crystal.html). Phases 2-6 remain for the scheduled runs.

## Phase details

### Phase 2 — sprite & cry completeness audit
Goal: prove (and if needed fix) that every Gen-2 sprite variant exists and
renders correctly, for all 251 Pokémon:
- folders to audit (each must have exactly ids 1..251):
  `assets/sprites/gen2-gold{,-back,-shiny,-back-shiny}/`
  `assets/sprites/gen2-silver{,-back,-shiny,-back-shiny}/`
  `assets/sprites/gen2-crystal{,-back,-shiny,-back-shiny}/`
  `assets/sprites/gen2-crystal-anim/` (webp)
- checks: file exists, non-empty, decodes (PIL), correct mode (has alpha),
  not identical-to-normal for shiny sets (sample), webp frames > 1 for anim.
- cries: `assets/audio/cries/1..251.ogg` exist + non-trivial size.
- UI: 56×56 GBC sprites must not be upscaled blurry — confirm
  `image-rendering:pixelated` on `#sprImg` and evo sprites (gen2.css already
  has it; verify in browser), animated webp plays in Chromium + Firefox.
- If gaps: refetch with the existing tools (see `tools/build-sprites.py`
  patterns; PokeAPI via token in `.secrets/github_token` header if rate
  limited). Keep fetched files under `assets/sprites/gen2-*`.
- Write `tools/test-gen2-sprites.py` proving the audit (run it; commit it).
- Test: `python3 tools/test-gen2-sprites.py && python3 tools/test-gen2.py`.

### Phase 3 — Moves Dex wiring
Goal: gen2.html gets the per-game Moves section + Moves Dex overlay, like
gen1.html.
- Add to gen2.html (after gen2-data.js, before gen2.js):
  `<script src="assets/js/moves-gs.js"></script>` (defines MD_GS — check the
  actual global name inside the file; it may define `MD` and a page shim may
  be needed like gen1 does with MD_RB/MD_Y — look at how gen1.html wires
  moves-gen1.js and copy that pattern),
  `<script src="assets/js/moves-crystal.js"></script>`,
  `<script src="assets/js/moves-fa.js"></script>`,
  `<script src="assets/js/moves-module.js"></script>`.
- In gen2.js: THEMES map gets `moves:` field ("MD_GS" for gold/silver,
  "MD_CRYSTAL" for crystal) and `activeMoves()` + `MovesUI.setGame(...)` on
  theme change — copy gen1.js exactly (it already does this for MD_RB/MD_Y).
- Verify: every Gen-2 move has a Persian description in moves-fa.js (the ~86
  new Gen-2 moves: spark, rollout, …); learnsets exist for all 251 per game;
  Crystal move-tutor moves (Flamethrower/Thunderbolt/Ice Beam) appear for
  Crystal and not for G/S; TM/HM lists differ correctly (G/S vs C).
- Item/move names bilingual in the overlay; game label "GOLD/SILVER" vs
  "CRYSTAL" follows the theme.
- Extend `tools/test-gen2.py` with moves checks (mirror test-gen1.py) and run.

### Phase 4 — Item Dex wiring
Goal: the Item Dex overlay on gen2.html, Gen-2 scoped.
- gen2.html before items-module.js:
  `<script>window.ITEM_DEX_CONFIG = { games:"gc", label:"G/S/C", gen:2, icons:"gb" };</script>`
  then `items-data.js` + `items-module.js`.
- Verify: all Gen-2 items show (Apricorn balls, berries, new held items,
  Gen-2 TMs? — items-data `g` flag contains g/c), prices column = Gen 2
  (`gen:2` → p2), FA names + descriptions present, GB icons + color icons
  both exist (`window.__itemIconHint` — gen2 sprites are always color, so
  decide: default "color" and let the chip toggle; keep parity with gen1's
  MONO/COLOR coupling but gen2 has no mono mode → icons follow the LCD/color
  choice; simplest: icons "gb" default with a chip in the overlay).
- Extend test-gen2.py with an items check; run all.

### Phase 5 — How to Catch + Location Dex (Johto & Kanto, G/S/C)
Goal: parity with gen1's Location Dex + HOW TO CATCH section, for Gold,
Silver and Crystal (Johto + Kanto). Biggest phase — budget the run for it.
- Data source (authentic): pret disassemblies `pokecrystal` (and `pokegold` /
  `pokesilver` where they differ — mostly they don't for wild data):
  `https://raw.githubusercontent.com/pret/pokecrystal/master/data/wild/…`
  plus `maps/…` encounter scripts. Fetch via curl with the token header only
  if rate-limited. Cache raw files under `tools/loc2-cache/` (gitignore it,
  mirroring `tools/loc-cache/`).
- Build `tools/build-locations-gen2.py` → `assets/js/locations-gen2.js`,
  format IDENTICAL to `locations-gen1.js` (read it first; reuse
  `locations-module.js` as-is if the data shape matches — prefer adapting the
  builder, not the module; if the module needs a Gen-2 tweak, keep the
  module's API and extend, don't fork behaviour for gen1).
- Cover: wild grass (morning/day/night where they differ), surf, fishing
  (Old/Good/Super Rod), Rock Smash, Headbutt trees, Bug-Catching Contest,
  Waterfall/Whirlpool spots, swarm Pokémon (radio), the two regions' routes &
  caves & dungeons (Johto ~40 maps + Kanto ~20), plus specials: starters
  (Chikorita/Cyndaquil/Totodile from Elm), Togepi egg, Shuckle (Cianwood),
  Tyrogue (Mt. Mortar), Eevee (Bill, Goldenrod — G/S/C), Lapras (Union Cave
  Fridays), Dratini line (Dragon's Den / Game Corner), Game Corner prizes
  (Goldenrod: Abra? — verify from disasm data; Celadon: —), fossils? (Gen 2:
  none new), Ho-Oh (Tin Tower; requirements differ per version), Lugia
  (Whirl Islands), Suicune (Crystal: scripted encounters; G/S: roaming),
  Raikou/Entei roaming, Celebi (Ilex shrine, event), Red Gyarados (Lake of
  Rage), Snorlax (Kanto, radio), Lapras, Kenya the Spearow trade, in-game
  trades per version, Crystal-exclusive: Odd Egg (Day-Care, shiny hatched).
- Every location name + method label bilingual EN/FA (extend the module's
  i18n like locations-gen1.js does — check how gen1 carries FA labels).
- Wire into gen2.html (`locations-gen2.js` + `locations-module.js`) and
  gen2.js (`LocUI.syncGame()` on theme change, games: GOLD/SILVER share
  tables unless they differ; Crystal gets its own where it differs).
- Extend test-gen2.py (locations section present, a known encounter correct:
  e.g. Chikorita only via starter; Sentret on Route 29; Red Gyarados Lake of
  Rage; Crystal Odd Egg exists, G/S doesn't).
- If the full data set is too large for one run: land Johto first with
  Kanto TODO noted in the table (status BLOCKED with details), next run
  finishes. Do not ship placeholder UI — sections must render real data or
  stay absent (the typeof-guard hides them).

### Phase 6 — final QA + ship
- Run EVERYTHING: `python3 tools/test-gen1.py && python3 tools/test-gen2.py
  && python3 tools/test-order.py` (+ any phase tests). All green.
- Playwright screenshots of gen2.html: mobile 390 EN + FA, desktop 1440,
  each theme (gold/silver/crystal); check with the vision CLI
  (`z-ai vision -p "..." -i shot.png`) — mobile order (DEX STATUS → search →
  SETTINGS → card → details), bilingual name, no overlap/overflow, RTL sane.
- Landing page final look (index.html): generations ordered 1→2→3, Gen-2
  card points to gen2.html, counts updated, FA strings complete.
- README.md: add the Gen-2 section (mirror the Gen-1 section's structure).
- Verify the live deploy: after push, poll
  `https://api.github.com/repos/Ali-F-Harandi/pokedex/pages/builds?per_page=1`
  (token header) until status `built` (retry a few times, deploys take
  ~30 s - few min; a rare transient failure = GitHub CDN issue, re-run via
  the Actions API if needed: POST /repos/.../actions/runs/{id}/rerun).
  Then `curl -s` gen2.html + gen2.js from the live URL and md5-compare to
  the local files.
- Finally: mark the table all DONE, commit, push — then DELETE the cron job
  `gen2-phases-runner` (cron tool: action list → find id → delete). Confirm
  deletion. Leave a short summary in the final commit message.

## Environment facts (for the runs)

- Sandbox: Linux, python3 + node + playwright (chromium) installed.
- Repo working tree is at `/home/z/my-project/repos/pokedex` and persists
  between runs. Nothing else persists — do not rely on running processes.
- Tests write screenshots to /tmp — that's fine.
- Live site: https://ali-f-harandi.github.io/pokedex/ (GitHub Pages from
  `main` root). Deploys: ~30 s normally; transient "Page build failed" on
  the deploy step = GitHub-side hiccup, the auto-retry usually fixes it.
- The `I18N` convention: any new user-visible string needs an `fa` twin.
  Persian digits via the existing `num()` helper. FA layout = rtl via
  `body.fa`.
- CSS: gen2.css owns the Gen-2 look (GBC bezel wordmark, power LED, atomic-
  purple base shell, per-theme repaints). Keep gen1.css untouched.
