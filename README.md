# Pokédex Project

**Interactive, fully offline Pokédex apps for classic Pokémon games — each one styled exactly like the dex inside its own game.**

Every dex shares one structure and feature set; only the theme changes per game. Pages are small HTML entries that load their CSS, JS, sprites, cries and fonts from local files in `assets/` — no build step, no server, no internet required.

> 🌐 **Live site:** https://ali-f-harandi.github.io/pokedex/
>
> ▶️ **Generation I dex — Red · Blue · Green · Yellow in one page:** https://ali-f-harandi.github.io/pokedex/gen1.html
>
> ▶️ **Generation II dex — Gold · Silver · Crystal in one page:** https://ali-f-harandi.github.io/pokedex/gen2.html
>
> ▶️ **Generation III dex — Ruby · Sapphire · Emerald · FireRed · LeafGreen in one page:** https://ali-f-harandi.github.io/pokedex/gen3.html

---

## ✅ Currently available

| Game | Generation | File | Status |
|------|-----------|------|--------|
| **Generation I — Red · Blue · Green · Yellow** | Gen 1 (Kanto) | [`gen1.html`](https://ali-f-harandi.github.io/pokedex/gen1.html) | ✅ Available |
| **Generation II — Gold · Silver · Crystal** | Gen 2 (Johto + Kanto) | [`gen2.html`](https://ali-f-harandi.github.io/pokedex/gen2.html) | ✅ Available |
| **Generation III — Ruby · Sapphire · Emerald · FireRed · LeafGreen** | Gen 3 (Hoenn + Kanto + Sevii) | [`gen3.html`](https://ali-f-harandi.github.io/pokedex/gen3.html) | ✅ Available |

(`red-blue.html` / `yellow.html` redirect to `gen1.html`, `goldsilver.html` / `crystal.html` redirect to `gen2.html`, and `emerald.html` redirects to `gen3.html` — each generation lives in one dex.)

### Generation III Dex — features (Ruby · Sapphire · Emerald · FireRed · LeafGreen in one page)

- All **386 Pokémon** (Gen 1–3, National Dex #001–#386) and **all five Gen-3 games in a single dex**, themed after the Game Boy Advance era — an indigo GBA shell with the `GAME BOY ADVANCE` wordmark, power LED, L/R shoulder buttons and a wider screen proportion; each game repaints the console like its own cartridge. The GAME chips live in their own SETTINGS panel, grouped like the real cartridges: **RUBY + SAPPHIRE share one group**, **EMERALD** stands alone and **FIRERED + LEAFGREEN** share one — also reachable from the START menu or key `T`
- **Each cartridge's own sprites** — Ruby/Sapphire, Emerald and FireRed/LeafGreen each get their own banks (front, back, shiny, back-shiny — 64×64 uniform canvas, `image-rendering:pixelated`), and the dex swaps banks with the theme. **Emerald's animated battle sprites** are on the EMERALD chip only (Emerald was the first game to animate them) — all 386 authentic animations as lossless WebP with a toggle (`Anim` button, START menu or key `A`)
- **Deoxys follows its cartridge**, exactly like the real games: Normal forme on Ruby/Sapphire, Attack on FireRed, Defense on LeafGreen, Speed on Emerald — the card, stats, sprites and dex entry all switch with the selected game
- **Dex-text version selector**: Ruby/Sapphire, Emerald and FRLG each carry their own entry texts — small `R/S` / `EMERALD` / `FRLG` buttons on the entry box offer only the wordings the active game really has (203 species differ across R/S, 251 across FRLG); the box flips pages like the original
- **Ability Dex** (`Y` key or START menu) — gen 3 introduced abilities: all **77 era-authentic abilities** parsed from the pokeemerald tables, searchable EN/FA, each with its effect and its slot-1 / slot-2 carrier lists; **no hidden abilities anywhere** (they didn't exist yet), and Cacophony is kept with the honest note that it exists in the games' code but no Pokémon of the era carries it; ability chips on every Pokémon open the ability's card
- **Natures** — all **25 natures** with an interactive selector on the base-stats panel: picking one shows ▲/▼ (+10 %/−10 %) on the affected stats, notes neutral natures, and ties each nature to its loved/hated **Pokéblock flavor** straight from the games' tables
- **HOW TO CATCH section on every Pokémon** — where it actually lives in the selected game: wild grass, surfing, rock-smashing, underwater and fishing tables (with the real slot and bite chances), every special way (starters, gifts, in-game trades with their NPCs, Game Corner dolls, fossils, statics with script-true levels, roamers, ticket events), Feebas's six hidden tiles, and the full evolve paths with Gen-3 conditions (Beauty 170, trade items, happiness) — impossible-in-that-game Pokémon say so and name the games that have them
- **Location Dex** (`L` key or START menu) — **80 Hoenn** (R/S/E) **+ 87 Kanto & Sevii** (FRLG) locations with region chips `HOENN / KANTO`, per-game per-room encounter tables (Emerald-only areas, FR/LG differences, rooms that genuinely differ), fishing with bite rolls, the UNDERWATER / ROCK-SMASH / SWARM method badges, the Tanoby chambers' authentic Unown letter sets and the roaming-Lati@s / beast rules; click any Pokémon to jump to its dex page
- **Moves follow the selected game** — the learnset panel, Moves Dex and TM/HM list switch between R/S, Emerald and FRLG data with the theme; **contest data** (appeal + jam hearts) shows on R/S/E move cards and is authentically absent on FRLG — see the *Moves & learnsets* section below
- **Item Dex** — every bag item of the selected game (222 in R/S, 247 in Emerald, 248 in FRLG) with era-true prices, pockets and descriptions, and all **43 Gen-3 berries** with their flavor profiles and firmness — see the *Item Dex* section below
- Counters split like the game: seen & owned, saved in the browser
- **Authentic Gen-3 type chart** (identical to Gen 2's — the next change came in Gen 5) and **era-true move classes**: physical/special still derived from the move's type (the split came in Gen 4)
- **Authentic cries for all 386** (local OGG files; 252–386 joined the shared cry folder, 1–251 untouched) · deep links (`gen3.html#025`) · optional LCD screen shader · settings remembered (`pkd_g3_*`)

### Generation I Dex — features (Red · Blue · Green · Yellow in one page)

- All **151 Kanto Pokémon** and **all four Gen-1 games in a single dex**, themed after the Game Boy era — each game repaints the whole console like its own cartridge
- **GAME theme switcher in its own SETTINGS panel** — the game chips no longer crowd the Pokémon card: they live in a separate settings box above it, with **RED + BLUE grouped in one cartridge** (tap either to switch — the theme follows: red shell / blue shell), **GREEN** and **YELLOW** in groups of their own. Also reachable from the START menu or key `T`; each theme repaints the **cartridge-coloured shell, header, footer, accents and page glow** (Red / Blue / Green / Yellow) and swaps in that game's data:
  - **RED** / **BLUE** — the international 1998 pair sharing one sprite set: `MONO` (Game Boy monochrome, **DMG green** / **Pocket gray** palettes) and `COLOR` (the same sprites colorized)
  - **GREEN** — the **Japan-only 1996 version** with its older artwork (mono only, as the game was), with a short historical note
  - **YELLOW** — its own gold shell, its own redrawn sprites (`MONO` + `COLOR`), its own dex texts and its own moves
- **Touch-friendly browsing** — on phones, big round arrows flank the Pokémon and **swiping the sprite** goes to the next/previous one (like a slider); the arrows keep their physical direction in the Persian (RTL) layout too. **Tapping the sprite flips it front/back** (same as the `Back` button), and the phone card carries the whole essentials: sprite, HT/WT, the dex entry text (tappable to flip pages) and the cry button
- **Paper-white sprite backdrop** — every sprite (and evolution sprite) sits on a light card so even the palest sprites read clearly; the LCD screen keeps its authentic green
- **HOW TO CATCH section** on every Pokémon — where it actually lives in the selected game: wild tables (grass / surf / Super Rod with the real slot chances), every special way (starters, gifts, in-game trades with their nicknames, Game Corner prizes, fossil revivals, fixed encounters) and, when a Pokémon only comes by evolving, the full evolve path from its earliest obtainable form — Pokémon that are impossible in that game say so and name the games that have them
- **Location Dex** (`L` key or START menu) — all 68 Kanto locations of the four games with per-game encounter tables, encounter rates, fishing notes and their special encounters; click any Pokémon to jump to its dex page
- **Optional LCD screen shader** — an `LCD` toggle in the settings panel (and START menu) lays a Game Boy-style glass over every sprite bucket (main box + evolution chain): scanlines, a faint pixel grid, the DMG green tint and a soft top reflection. Pure CSS overlay — off by default, on for those who want it
- **Settings are remembered** — the game, the MONO/COLOR choice (kept when you switch games, e.g. Red COLOR → Yellow COLOR), the LCD shader, screen palette, front/back, language, sort order, favorites filter and the last-viewed Pokémon all survive reloads
- **Back sprites for every Pokémon in every set** — the `Back` button, START menu or key `B` flips to the in-game back side; international backs are rendered at the games' authentic 2× scale, matching the Japan Green backs pixel-for-pixel
- **Dex-text version selector**: Yellow rewrote **all 151** entries — small `R/B` / `YELLOW` buttons on the entry box switch between the authentic Red/Blue and Yellow texts (the choice follows the active game and can be overridden anytime)
- **Moves follow the selected game** — the learnset panel, Moves Dex and TM/HM list switch between the Red/Blue and Yellow data with the theme
- **Authentic Gen-1 cries** (local OGG files); Pokédex entries transcribed from the [`pret/pokered`](https://github.com/pret/pokered) and [`pret/pokeyellow`](https://github.com/pret/pokeyellow) decompilations (original 2-page texts, authentic categories); authentic **Gen-1 type chart** (Ghost ×0 vs Psychic, Bug ×2 vs Poison quirks included); page-flipping entries; seen/owned tracking

### Generation II Dex — features (Gold · Silver · Crystal in one page)

- All **251 Johto + Kanto Pokémon** and **all three Gen-2 games in a single dex**, themed after the Game Boy Color era — each game repaints the whole console like its own cartridge: **GOLD** (grape-purple GBC shell, gold accents), **SILVER** (bluish-silver shell) and **CRYSTAL** (teal shell, ice-blue accents), with the multicolor `GAME BOY COLOR` wordmark and POWER LED on the bezel. The GAME chips live in their own SETTINGS panel and are also reachable from the START menu or key `T`
- **Each version's own in-game sprites** — Gold, Silver and Crystal each redrew the set, and the dex swaps banks with the theme:
  - **Shiny sprites for every Pokémon in every bank** — shiny Pokémon were introduced in this very generation (`Shiny` button, START menu or key `S`); the audit proved **0 of 753 shiny sprites** (front + back × 3 games) is identical to its normal counterpart
  - **Back sprites** for every Pokémon, normal **and** shiny (`Back` button, START menu or key `B`)
  - **Animated battle sprites on CRYSTAL** — Crystal introduced the series' very first animated Pokémon sprites; all 251 authentic animations are included as lossless WebP with a toggle (`Anim` button, START menu or key `A`) — fronts only, exactly like the game
- **Dex-text version selector**: Gold, Silver and Crystal each carry their own entry texts — small `GOLD` / `SILVER` / `CRYSTAL` buttons on the entry box switch between the three authentic wordings (Crystal rewrote **every single** entry: all 251 differ from both Gold and Silver); the box flips pages like the original
- **HOW TO CATCH section on every Pokémon** — where it actually lives in the selected game: wild grass (morning / day / night tables where they differ), surfing, the three rods with the real bite chances, Headbutt and Rock Smash trees (common/rare sets), radio swarms, the Bug-Catching Contest, every special way (Elm's starters, Togepi egg, Crystal's Odd Egg, gifts, in-game trades with their NPC houses, Game Corner prizes per version, Red Gyarados, per-version static levels — Lugia 70/40/60 and Ho-Oh 40/70/60 across G/S/C — the roaming beasts, Celebi's event shrine) and, when a Pokémon only comes by evolving, the full path including Gen-2's happiness (day/night), beauty, shed-shell and trade-item evolutions — impossible-in-that-game Pokémon say so and name the games that have them
- **Location Dex** (`L` key or START menu) — **119 Johto + Kanto locations** with per-game encounter tables: grass in three time-of-day tabs (`MORN / DAY / NITE`), surfing, 13 fishing groups (Old/Good/Super Rod with bite % and level spreads), Headbutt and Rock Smash trees, Crystal's grass swarms, the Bug-Catching Contest table, region chips `JOHTO / KANTO`; click any Pokémon to jump to its dex page
- **Moves follow the selected game** — the learnset panel, Moves Dex and TM/HM list switch between the G/S and Crystal data with the theme; the Goldenrod **Move Tutor** (Flamethrower / Thunderbolt / Ice Beam) exists on Crystal only
- **Item Dex** — every bag item of the selected game (161 in Gold/Silver, 165 in Crystal; the four Crystal-only items included), Apricorn balls, berries, held items and Mail with the **Gen-2 prices** (HYPER POTION ¥1200, not R/B's ¥1500) — see the *Item Dex* section below
- **Optional LCD screen shader that the Item Dex icons follow** — LCD on shows the 4-shade Game Boy item icons, LCD off the colorized ones, mirroring how the games themselves could only show mono
- Counters split like the game: **Kanto / Johto / Total** seen & owned
- Authentic **Gen-2 type chart** — Dark & Steel types included, `Ghost ×2 vs Psychic` fixed
- **Authentic cries** for all 251 (local OGG files) · seen/owned tracking · full detail grid (catch rate, happiness, growth, egg groups, habitat, gender) · deep links (`gen2.html#025`)

### Uniform sprite scale (all dexes)

- Every sprite set now sits on its **native uniform canvas** — no more zoom-to-fit: a Caterpie stays small next to a Gyarados, exactly like the games
- Gen-1/2 fronts & shinies: uniform 56×56 (7×7 tile) canvas, bottom-centered — the Japan Green convention
- Gen-1 international backs are stored at **half resolution and rendered at 2×**, just like the games did — matching the Green backs pixel-for-pixel; Gen-2 backs keep their uniform 48×48 at 1:1
- Emerald animated sprites re-anchored onto a uniform 96×96 canvas (the animation envelope), frame-exact

### Moves & learnsets (Gen-1/2 dexes — Pokédex Plus, Phase 2)

- **MOVES panel in every Pokémon's detail view** — the learnset *of that exact game*, grouped by learn method with counts: **LEVEL-UP** (with the learn level), **TM · HM** (with the machine number), **EGG** and **TUTOR** tabs (the latter two only where the game has them — eggs and tutors are Gen-2 features, and the tutor tab is Crystal-only)
- Clicking any move opens its **move card** inside the **MOVES DEX** overlay
- **MOVES DEX** (START menu, `M` key, or the `ALL MOVES` button): every move that exists in that game — 165 in Red/Blue/Yellow, 251 in Gold/Silver/Crystal — with search (EN/FA), type and physical/special filters
- **TM / HM LIST** (START menu): the authentic machine list of that game — 50 TMs + 5 HMs in Gen 1, 50 TMs + 7 HMs in Gen 2; on Crystal it also notes the Goldenrod **Move Tutor** (Flamethrower / Thunderbolt / Ice Beam)
- **Move cards** show power / accuracy / PP, the type badge, the **Gen-1/2 physical-vs-special class** (derived from the move's type, as the games did), the authentic **Gold/Silver/Crystal in-game description** (EN + FA) and a **"who can learn it"** section — every Pokémon of that game grouped by method, with learn levels; clicking one jumps to that Pokémon
- **Historical accuracy**: power / type / accuracy / PP are taken from the `pret` decompiles (`pokered` / `pokegold` move tables) — so Gen 1 shows **Gust, Karate Chop, Bite and Sand Attack as NORMAL-type**, **Rock Throw at 65% accuracy**, **Barrier with 30 PP** etc.; Curse keeps its authentic **`???` type badge**; the Gen-1 games had no move text, so Gen-1 pages carry a short historical note instead of any wording label
- **Fully bilingual**: 251 Persian move names + all 251 descriptions translated, Persian digits, RTL-aware panels
- Reproducible: `python3 tools/build-moves.py` regenerates every data file from `pret` + PokéAPI

### Item Dex (Gen-1/2 dexes — Pokédex Plus, Phase 3)

- **ITEM DEX overlay** (START menu or `I` key) on the Generation I, Gold/Silver and Crystal dexes: every **bag item of that game** — 72 in Red/Blue/Yellow, 161 in Gold/Silver, 165 in Crystal (machines stay in the TM/HM list of the Moves Dex)
- **Game-authentic item lists** from the `pret` decompiles (`pokered` / `pokecrystal`): unused placeholder slots (TERU-SAMA) are excluded, and the four **Crystal-only items** (CLEAR BELL, GS BALL, BLUE CARD, EGG TICKET) appear only on the Crystal dex
- **Item cards**: authentic in-game name (EN + FA), bag pocket (BALLS / ITEMS / KEY ITEMS), category badge (Medicine, Battle, Berries, Apricorns, Held items, Mail, …), **buy and sell prices of that game** — prices really do differ between generations (HYPER POTION: ¥1500 in R/B, ¥1200 in G/S/C) — the item's **in-game description** (EN + FA), a HOLD badge for held items, and an **appears-in row limited to that dex's own games** (the Gen-1 dex shows only RED/BLUE · YELLOW — no Gen-2 games leak in)
- **Gen-1-only info on the Gen-1 dex**: only the 72 Red/Blue/Yellow items appear, availability is RED/BLUE · YELLOW only and no Gen-2 wording labels are shown — the Gen-1 games had no item descriptions, so items that never got one (SILPH SCOPE, GOLD TEETH, OAK'S PARCEL…) say so
- **Icons in two styles**: the PokeAPI menu icons recolored onto the **DMG 4-shade Game Boy ramp** and the original color icons — on the Gen-1 dex the icons **follow the sprite `MONO`/`COLOR` switch** (colour set → colour icons), with a manual toggle in the overlay; an icon that has no colour version falls back to its GB icon. A dozen items never had an icon anywhere (GS BALL, EGG TICKET, BERSERK GENE, the two BOWs…) and show a dashed placeholder; Gen-2 berries borrow the modern fruit icons of their Gen-3 renames (BERRY → Oran design etc.)
- **Fully bilingual**: all 181 Persian item names + all 161 descriptions translated; search works in EN and FA; category chips localized
- Reproducible: `python3 tools/build-items.py` regenerates the data and icons from `pret` + PokeAPI

### Location Dex & How to Catch (Gen-1 dex — Pokédex Plus, Phase 4; Gen-2 dex — Phase 5)

- **68 Kanto locations** — every route, city, cave, floor, the Safari Zone areas, the Power Plant, Pokémon Tower, Seafoam Islands, Pokémon Mansion, Cerulean Cave, Victory Road, even the fishable **Cerulean Gym** and **Vermilion Dock** — each with its EN/FA name and a story-order sort
- **Authentic per-game encounter tables** read from the `pret` decompiles (`pokered` for Red/Blue, `pokeyellow` for Yellow): grass and surfing tables with the real 10-slot chances (19.9/19.9/15.2/9.8/9.8/9.8/5.1/5.1/4.3/1.2 %), encounter-rate bytes (shown as `25/255 ≈ 10% per step`), Red-vs-Blue exclusive slots and Yellow's own tables
- **Fishing, exactly as the games coded it**: Old Rod = Magikarp L5 anywhere; Good Rod = a global 50/50 Goldeen/Poliwag L10; Super Rod = Red/Blue's per-map fishing groups and Yellow's own per-route 4-slot tables with 40/30/20/10 % chances
- **Green (Japan) honestly**: Bulbapedia documents that Japanese Green shares the international Blue's Pokémon distribution — Green shows the Blue tables and says so (the international Red/Blue kept the Japanese Red/Green wild data, which is exactly what `pokered` contains)
- **Every special way to obtain**: the three starters (L5, Oak's lab), Yellow's Pikachu starter and its gift Bulbasaur/Charmander/Squirtle, Eevee, Lapras, the Hitmon choice, the ¥500 Magikarp salesman, all 9+7 in-game trades (give/receive, same level, real nicknames TERRY/DUX/LOLA…), Game Corner prizes per game with real coin prices and levels, the Mt. Moon fossil choice and Old Amber revivals (L30), and the fixed encounters — Mewtwo L70, the three birds L50, both Snorlax L30 and the Power Plant's item-ball Voltorb/Electrode
- **The Yellow quirks are honoured**: Raichu is impossible in Yellow (the starter Pikachu refuses the Thunder Stone) — the dex says so instead of pretending; Weedle/Ekans/Meowth/Koffing lines, Jynx, Electabuzz and Magmar correctly show as trade-only in Yellow
- **Mew** is labelled event/glitch-only, as it was
- **Two-way navigation**: the Location Dex opens straight onto any location named in the HOW TO CATCH rows, and every species inside a location jumps back to its dex page
- Fully bilingual (all location names, methods and special-ways texts in EN/FA, Persian digits everywhere); reproducible: `python3 tools/build-locations.py` regenerates everything from `pret`

### All dexes

- **Bilingual: English (primary) + Persian (فارسی)** — full RTL, Persian digits, translated names/types/entries/abilities/evolutions
- **Moves everywhere (Gen-1/2/3 dexes)** — per-game learnset panel, Moves Dex (`M`), TM/HM list — see the *Moves & learnsets* section above
- **Item Dex everywhere (Gen-1/2/3 dexes)** — every bag item of the game with icons, prices and bilingual descriptions (`I`) — see the *Item Dex* section above
- **Location Dex on Gen-1/2/3** (`L`) with HOW TO CATCH on every Pokémon — see the *Location Dex* section above
- **100% offline** — all data, sprites, cries and fonts are plain local files next to each page
- Landing page (`index.html`) is **game-neutral**: one catalog item per game — Generation I is all four Game Boy games in one item; complementary pairs like Gold/Silver or Ruby/Sapphire share a single item

## 🏠 Landing page

`index.html` is the project hub (dark neutral theme, not tied to any single game). Every mainline Pokémon game (Gen 1–9) is listed with its own colored card; the **Generation I dex** (Red · Blue · Green · Yellow in one page), the **Generation II dex** (Gold · Silver · Crystal) and the **Generation III dex** (Ruby · Sapphire · Emerald · FireRed · LeafGreen) are live now, everything else is *Coming Soon* and will follow one by one. Bilingual EN/FA.

## 🗺 Roadmap

- [x] **Emerald (Gen 3)** — available
- [x] **Red / Blue (Gen 1)** — available
- [x] **Yellow (Gen 1)** — available (Yellow's own sprites and Yellow's own dex entries)
- [x] **Gold / Silver (Gen 2)** — available (both versions' sprites + shiny, both versions' dex texts, Game Boy Color shell)
- [x] **Crystal (Gen 2)** — available (Crystal's own sprites + shiny, animated battle sprites, fully rewritten dex entries)
- [x] **Back sprites everywhere + Japan-only Green set** (Pokédex Plus, Phase 1)
- [x] **Moves & learnsets per game (Pokédex Plus, Phase 2)** — per-game move data, learnset panel, Moves Dex & TM/HM lists on all Gen-1/2 dexes
- [x] **Location Dex & How to Catch (Pokédex Plus, Phase 4)** — all 68 Kanto locations with per-game encounter tables, rods, special encounters and evolve paths on the Gen-1 dex
- [x] **Generation II unified dex (Pokédex Plus)** — Gold · Silver · Crystal in one Game Boy Color-styled page with per-version sprites (incl. shiny + back + Crystal animations), three dex-text wordings, corrected Gen-2 type chart
- [x] **Moves & learnsets on the Gen-2 dex** — 251 moves, per-game learnsets, Crystal-only Move Tutor, authentic 50+7 TM/HM list
- [x] **Item Dex on the Gen-2 dex** — 161 Gold/Silver + 165 Crystal items with Gen-2 prices and LCD-coupled icons
- [x] **Location Dex & How to Catch on the Gen-2 dex** — 119 Johto + Kanto locations with time-of-day tables, rods, Headbutt/Rock Smash, swarms, the Bug-Catching Contest and 51 special encounters
- [x] **Generation III unified dex (Pokédex Plus)** — Ruby · Sapphire · Emerald · FireRed · LeafGreen in one Game Boy Advance-styled page: per-cartridge sprite banks, three dex-text wordings, the cartridge-bound Deoxys formes, era-true abilities (no hidden), Emerald's animated sprites
- [x] **Moves & learnsets on the Gen-3 dex** — 354 moves × 3 games, per-game learnsets/egg/machine/tutor data, contest appeal+jam on R/S/E, authentic 50 TMs + 8 HMs
- [x] **Item Dex on the Gen-3 dex** — 222 R/S + 247 Emerald + 248 FRLG items with era-true prices and all 43 berries with flavor profiles
- [x] **Location Dex & How to Catch on the Gen-3 dex** — 80 Hoenn + 87 Kanto & Sevii locations with per-game tables, underwater/rock-smash/swarm methods, Feebas tiles, roamers and ticket events
- [x] **Ability Dex + Natures on the Gen-3 dex** — all 77 era abilities with carrier lists (`Y`), the 25 natures with an interactive stat-boost selector and Pokéblock flavors
- [ ] Gen 4–9 — planned

## 🚀 Run locally

No installation needed:

```bash
git clone https://github.com/Ali-F-Harandi/pokedex.git
cd pokedex
# open index.html (or gen1.html / gen2.html / gen3.html) directly in any browser —
# everything works offline, even over file://
```

## 📁 Project structure

```
pokedex/
├── index.html                  ← game-neutral landing page (catalog + roadmap, EN/FA)
├── gen1.html                   ← Generation I dex — Red · Blue · Green · Yellow in one page
├── red-blue.html               ← redirect → gen1.html
├── yellow.html                 ← redirect → gen1.html
├── gen2.html                   ← Generation II dex — Gold · Silver · Crystal in one page
├── goldsilver.html             ← redirect → gen2.html
├── crystal.html                ← redirect → gen2.html
├── gen3.html                   ← Generation III dex — Ruby · Sapphire · Emerald · FireRed · LeafGreen in one page
├── emerald.html                ← redirect → gen3.html
└── assets/
    ├── css/                    ← one stylesheet per page (gen1 / gen2 / gen3 / landing / …)
    ├── js/                     ← data + logic per page (gen1 / gen2 / gen3 / landing) + shared moves/items/locations/abilities modules
    ├── fonts/                  ← Press Start 2P + Vazirmatn (woff2, OFL)
    ├── img/                    ← favicon, Emerald sprite atlas, featured-card images
    ├── sprites/
    │   ├── gen3-rs/            ← Ruby/Sapphire sprites (386)
    │   ├── gen3-rs-shiny/      ← Ruby/Sapphire shiny variants (386)
    │   ├── gen3-rs-back*/      ← Ruby/Sapphire backs (normal + shiny)
    │   ├── gen3-frlg/          ← FireRed/LeafGreen sprites (386 + the FR/LG Deoxys forme sprites)
    │   ├── gen3-frlg-shiny/    ← FireRed/LeafGreen shiny variants
    │   ├── gen3-frlg-back*/    ← FireRed/LeafGreen backs (normal + shiny)
    │   ├── gen3-emerald/       ← Emerald stills cut from the animation atlas (incl. the Speed-forme Deoxys)
    │   ├── gen3-emerald-shiny/ ← Emerald shiny variants
    │   ├── gen3-emerald-anim/  ← 386 animated battle sprites (lossless WebP)
    │   ├── gen1-rb-dmg/        ← Red/Blue Game Boy mono, DMG green palette
    │   ├── gen1-rb-pocket/     ← Red/Blue Game Boy mono, Pocket gray palette
    │   ├── gen1-rb-color/      ← Red/Blue sprites, colorized
    │   ├── gen1-green-dmg/     ← Japan Green version, DMG palette (56×56)
    │   ├── gen1-green-pocket/  ← Japan Green version, Pocket palette (56×56)
    │   ├── gen1-y-dmg/         ← Yellow Game Boy mono, DMG green palette
    │   ├── gen1-y-pocket/      ← Yellow Game Boy mono, Pocket gray palette
    │   ├── gen1-yellow/        ← Yellow sprites, colorized
    │   ├── gen2-gold/          ← Gold's own sprites (251)
    │   ├── gen2-silver/        ← Silver's own sprites (251)
    │   ├── gen2-gold-shiny/    ← Gold shiny variants (251)
    │   ├── gen2-silver-shiny/  ← Silver shiny variants (251)
    │   ├── gen2-crystal/       ← Crystal's own sprites (251)
    │   ├── gen2-crystal-shiny/ ← Crystal shiny variants (251)
    │   ├── gen2-crystal-anim/  ← 251 animated battle sprites (lossless WebP)
    │   ├── gen1-*-back/        ← back sprites of every Gen-1 set above
    │   └── gen2-*-back*/       ← back sprites (normal + shiny) of every Gen-2 version
    └── audio/cries/            ← 386 authentic cries (ogg, shared by all dexes; 252–386 joined for Gen 3)
```

Each HTML page is tiny (6–12 KB) and pulls in its own CSS/JS plus the shared `assets/` folder. Adding a new game dex = one more HTML entry + one CSS + one JS + a sprite folder — everything else is reused.

## 🛠 Built with

- Vanilla HTML/CSS/JS — zero dependencies, zero network calls
- Sprites from the [PokeAPI sprites](https://github.com/PokeAPI/sprites) project:
  - `generation-i/red-blue` — Red/Blue sprites (mono conversions + colored originals, front + back)
  - `generation-i/red-green-japan` — the Japan-only Green version's older artwork (front + back)
  - `generation-i/yellow` — Yellow sprites (mono conversions + colored originals, front + back)
  - `generation-ii/gold` + `generation-ii/silver` (+ `shiny`, + back sprites) — each version's own sprites (Gold/Silver)
  - `generation-ii/crystal` (+ `shiny` + `animated` + back sprites) — Crystal's own static and animated sprites
  - `generation-iii/ruby-sapphire` + `generation-iii/firered-leafgreen` (+ `shiny`, + back sprites) — each cartridge's own sprites (Gen 3), plus the legacy Emerald animation atlas for the EMERALD chip
- Pokédex entry texts, categories and in-game HT/WT from the [`pret/pokered`](https://github.com/pret/pokered) and [`pret/pokeyellow`](https://github.com/pret/pokeyellow) decompilations; Gold/Silver/Crystal EN texts per version from PokeAPI; Gen-3 R/S · Emerald · FRLG wordings per version from PokeAPI, era-true abilities from the [`pret/pokeemerald`](https://github.com/pret/pokeemerald) tables
- Game data (stats, abilities, evolutions, genera) from [PokeAPI](https://pokeapi.co/)
- Wild encounter tables, fishing groups, in-game trades and Game Corner prizes from the `pret` decompilations (`pokered`, `pokeyellow` for Kanto; `pokegold` / `pokesilver` / `pokecrystal` for Johto + Kanto; `pokeruby` / `pokeemerald` / `pokefirered` for Hoenn + Kanto/Sevii) — see `tools/build-locations.py`, `tools/build-locations-gen2.py` and `tools/build-locations-gen3.py`
- Gen-3 moves, items, abilities and natures parsed from the `pret` decompiles (`pokeruby`, `pokeemerald`, `pokefirered`) — see `tools/build-gen3-moves.py`, `tools/build-items-gen3.py`, `tools/build-gen3-abilities.py`
- [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) (OFL) + [Vazirmatn](https://github.com/rastikerdar/vazirmatn) (OFL)
- Persian translations: names, genera, dex entries, abilities and UI — hand-written for this project

## ⚠️ Disclaimer

This is a fan-made, non-commercial educational project. Pokémon and Pokémon character names are trademarks of Nintendo, Creatures Inc. and GAME FREAK inc.
