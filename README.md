# Pokédex Project

**Interactive, fully offline Pokédex apps for classic Pokémon games — each one styled exactly like the dex inside its own game.**

Every dex shares one structure and feature set; only the theme changes per game. Pages are small HTML entries that load their CSS, JS, sprites, cries and fonts from local files in `assets/` — no build step, no server, no internet required.

> 🌐 **Live site:** https://ali-f-harandi.github.io/pokedex/
>
> ▶️ **Emerald dex (Gen 3):** https://ali-f-harandi.github.io/pokedex/emerald.html
>
> ▶️ **Generation I dex — Red · Blue · Green · Yellow in one page:** https://ali-f-harandi.github.io/pokedex/gen1.html
>
> ▶️ **Gold/Silver dex (Gen 2):** https://ali-f-harandi.github.io/pokedex/goldsilver.html
>
> ▶️ **Crystal dex (Gen 2):** https://ali-f-harandi.github.io/pokedex/crystal.html

---

## ✅ Currently available

| Game | Generation | File | Status |
|------|-----------|------|--------|
| **Pokémon Emerald** | Gen 3 (Hoenn) | [`emerald.html`](https://ali-f-harandi.github.io/pokedex/emerald.html) | ✅ Available |
| **Generation I — Red · Blue · Green · Yellow** | Gen 1 (Kanto) | [`gen1.html`](https://ali-f-harandi.github.io/pokedex/gen1.html) | ✅ Available |
| **Pokémon Gold/Silver** | Gen 2 (Johto) | [`goldsilver.html`](https://ali-f-harandi.github.io/pokedex/goldsilver.html) | ✅ Available |
| **Pokémon Crystal** | Gen 2 (Johto) | [`crystal.html`](https://ali-f-harandi.github.io/pokedex/crystal.html) | ✅ Available |

(`red-blue.html` and `yellow.html` now redirect to `gen1.html` — the whole generation lives in one dex.)

### Emerald Dex — features

- All **386 Pokémon** (Gen 1–3, National Dex #001–#386)
- UI faithful to the **in-game Pokémon Emerald Pokédex**: cream screen, red `POKé DEX` badge, red selection bar with pointer arrow, sprite card, `DEX STATUS` counters, `START · MENU` button
- **Dex modes** like the game: `NATIONAL / KANTO / JOHTO / HOENN`
- **Animated battle sprites** — Emerald was the first game to animate its battle sprites; all 386 authentic animations are included as lossless WebP, with a toggle (START menu / `Anim` button / key `A`)
- Emerald sprites **normal + shiny** (single local sprite atlas)
- Detail view: dex entry, base stats with colored bars, gen-3-accurate **type matchups**, full **evolution line** with conditions, abilities (incl. hidden), catch rate, happiness, growth rate, egg groups, habitat, gender ratio
- Search (EN/FA/number) · type filter chips · sort · favorites · random · seen/owned tracking (saved in browser)
- Keyboard: `↑ ↓ ← →` browse · `/` search · `S` shiny · `A` anim · `R` random · `Esc` close · deep links (`emerald.html#025`)

### Generation I Dex — features (Red · Blue · Green · Yellow in one page)

- All **151 Kanto Pokémon** and **all four Gen-1 games in a single dex**, themed after the Game Boy era — each game repaints the whole console like its own cartridge
- **GAME theme switcher** (sprite-card chips, START menu or key `T`) between the four releases — each theme repaints the **cartridge-coloured shell, header, footer, accents and page glow** (Red / Blue / Green / Yellow) and swaps in that game's data:
  - **RED** / **BLUE** — the international 1998 pair sharing one sprite set: `MONO` (Game Boy monochrome, **DMG green** / **Pocket gray** palettes) and `COLOR` (the same sprites colorized)
  - **GREEN** — the **Japan-only 1996 version** with its older artwork (mono only, as the game was), with a short historical note
  - **YELLOW** — its own gold shell, its own redrawn sprites (`MONO` + `COLOR`), its own dex texts and its own moves
- **Touch-friendly browsing** — on phones, big round arrows flank the Pokémon and **swiping the sprite** goes to the next/previous one (like a slider); the arrows keep their physical direction in the Persian (RTL) layout too
- **Paper-white sprite backdrop** — every sprite (and evolution sprite) sits on a light card so even the palest sprites read clearly; the LCD screen keeps its authentic green
- **Back sprites for every Pokémon in every set** — the `Back` button, START menu or key `B` flips to the in-game back side; international backs are rendered at the games' authentic 2× scale, matching the Japan Green backs pixel-for-pixel
- **Dex-text version selector**: Yellow rewrote **all 151** entries — small `R/B` / `YELLOW` buttons on the entry box switch between the authentic Red/Blue and Yellow texts (the choice follows the active game and can be overridden anytime)
- **Moves follow the selected game** — the learnset panel, Moves Dex and TM/HM list switch between the Red/Blue and Yellow data with the theme
- **Authentic Gen-1 cries** (local OGG files); Pokédex entries transcribed from the [`pret/pokered`](https://github.com/pret/pokered) and [`pret/pokeyellow`](https://github.com/pret/pokeyellow) decompilations (original 2-page texts, authentic categories); authentic **Gen-1 type chart** (Ghost ×0 vs Psychic, Bug ×2 vs Poison quirks included); page-flipping entries; seen/owned tracking

### Gold/Silver Dex — features

- A **dedicated Pokédex for Pokémon Gold & Silver** (all **251 Johto + Kanto Pokémon**), same structure as the other dexes, themed after the Game Boy Color era: a **grape-purple Game Boy Color shell** with the multicolor `GAME BOY COLOR` wordmark and POWER led on the bezel, plus a **Gold accent**
- **Each version's own in-game sprites**, switchable from the sprite card or the START menu:
  - `GOLD` — Gold's own sprites
  - `SILVER` — Silver's own sprites (Gold and Silver redrew many of them)
- **Shiny sprites** for every Pokémon — shiny Pokémon were introduced in this generation (`Shiny` button, START menu or key `S`)
- **Back sprites** for every Pokémon, normal **and** shiny — `Back` button, START menu or key `B`
- **Both versions' dex entry texts**: Gold and Silver rewrote most entries — small `GOLD` / `SILVER` buttons on the entry box switch between the two authentic texts (EN); the box still flips pages like the original
- The **Palette/Version button** recolors the whole dex between Gold and Silver accents
- Counters split like the game: **Kanto / Johto / Total** seen & owned
- Authentic **Gen-2 type chart** — Dark & Steel types included, `Ghost ×2 vs Psychic` fixed
- **Authentic cries** for all 251 (local OGG files) · seen/owned tracking · full detail grid (catch rate, happiness, growth, egg groups, habitat, gender)

### Crystal Dex — features

- A **dedicated Pokédex for Pokémon Crystal** (all **251 Johto + Kanto Pokémon**), same structure as the other dexes, with its own **teal Game Boy Color shell** and Crystal's **ice-blue accent**
- **Crystal's own in-game sprites** — Crystal redrew the Gen-2 sprites again — with **shiny variants** (`Shiny` button or key `S`)
- **Animated battle sprites** — Crystal introduced the series' very first animated Pokémon sprites; all 251 authentic animations are included as lossless WebP with a toggle (`Anim` button, START menu or key `A`), exactly like the Emerald dex
- **Back sprites** for every Pokémon, normal and shiny — static, exactly like the game (Crystal only animated its fronts); `Back` button, START menu or key `B`
- **Crystal's rewritten dex entries** — Crystal rewrote every single entry text (all 251 differ from both Gold and Silver); the box flips pages like the original
- Counters split like the game: **Kanto / Johto / Total** seen & owned · authentic **Gen-2 type chart** · authentic cries · seen/owned tracking · full detail grid

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

### All dexes

- **Bilingual: English (primary) + Persian (فارسی)** — full RTL, Persian digits, translated names/types/entries/abilities/evolutions
- **Moves everywhere (Gen-1/2 dexes)** — per-game learnset panel, Moves Dex (`M`), TM/HM list — see the *Moves & learnsets* section above
- **Item Dex everywhere (Gen-1/2 dexes)** — every bag item of the game with icons, prices and bilingual descriptions (`I`) — see the *Item Dex* section above
- **100% offline** — all data, sprites, cries and fonts are plain local files next to each page
- Landing page (`index.html`) is **game-neutral**: one catalog item per game — Generation I is all four Game Boy games in one item; complementary pairs like Gold/Silver or Ruby/Sapphire share a single item

## 🏠 Landing page

`index.html` is the project hub (dark neutral theme, not tied to any single game). Every mainline Pokémon game (Gen 1–9) is listed with its own colored card; **Emerald**, the **Generation I dex** (Red · Blue · Green · Yellow in one page), **Gold/Silver** and **Crystal** are live now, everything else is *Coming Soon* and will follow one by one. Bilingual EN/FA.

## 🗺 Roadmap

- [x] **Emerald (Gen 3)** — available
- [x] **Red / Blue (Gen 1)** — available
- [x] **Yellow (Gen 1)** — available (Yellow's own sprites and Yellow's own dex entries)
- [x] **Gold / Silver (Gen 2)** — available (both versions' sprites + shiny, both versions' dex texts, Game Boy Color shell)
- [x] **Crystal (Gen 2)** — available (Crystal's own sprites + shiny, animated battle sprites, fully rewritten dex entries)
- [x] **Back sprites everywhere + Japan-only Green set** (Pokédex Plus, Phase 1)
- [x] **Moves & learnsets per game (Pokédex Plus, Phase 2)** — per-game move data, learnset panel, Moves Dex & TM/HM lists on all Gen-1/2 dexes
- [ ] Ruby / Sapphire, FireRed / LeafGreen (Gen 3)
- [ ] Gen 4–9 — planned

## 🚀 Run locally

No installation needed:

```bash
git clone https://github.com/Ali-F-Harandi/pokedex.git
cd pokedex
# open index.html (or emerald.html / red-blue.html / yellow.html / goldsilver.html / crystal.html) directly in any browser —
# everything works offline, even over file://
```

## 📁 Project structure

```
pokedex/
├── index.html                  ← game-neutral landing page (catalog + roadmap, EN/FA)
├── emerald.html                ← Gen-3 Emerald dex entry page
├── gen1.html                   ← Generation I dex — Red · Blue · Green · Yellow in one page
├── red-blue.html               ← redirect → gen1.html
├── yellow.html                 ← redirect → gen1.html
├── goldsilver.html             ← Gen-2 Gold/Silver dex entry page
├── crystal.html                ← Gen-2 Crystal dex entry page
└── assets/
    ├── css/                    ← one stylesheet per page (emerald / redblue / yellow / goldsilver / crystal / landing)
    ├── js/                     ← data + logic per page (emerald / redblue / yellow / goldsilver / crystal / landing)
    ├── fonts/                  ← Press Start 2P + Vazirmatn (woff2, OFL)
    ├── img/                    ← favicon, Emerald sprite atlas, featured-card images
    ├── sprites/
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
    └── audio/cries/            ← 251 authentic cries (ogg, shared by all Gen-1/2 dexes)
```

Each HTML page is tiny (6–12 KB) and pulls in its own CSS/JS plus the shared `assets/` folder. Adding a new game dex = one more HTML entry + one CSS + one JS + a sprite folder — everything else is reused.

## 🛠 Built with

- Vanilla HTML/CSS/JS — zero dependencies, zero network calls
- Sprites from the [PokeAPI sprites](https://github.com/PokeAPI/sprites) project:
  - `generation-iii/emerald` — static + animated battle sprites (Emerald)
  - `generation-i/red-blue` — Red/Blue sprites (mono conversions + colored originals, front + back)
  - `generation-i/red-green-japan` — the Japan-only Green version's older artwork (front + back)
  - `generation-i/yellow` — Yellow sprites (mono conversions + colored originals, front + back)
  - `generation-ii/gold` + `generation-ii/silver` (+ `shiny`, + back sprites) — each version's own sprites (Gold/Silver)
  - `generation-ii/crystal` (+ `shiny` + `animated` + back sprites) — Crystal's own static and animated sprites
- Pokédex entry texts, categories and in-game HT/WT from the [`pret/pokered`](https://github.com/pret/pokered) and [`pret/pokeyellow`](https://github.com/pret/pokeyellow) decompilations; Gold/Silver/Crystal EN texts per version from PokeAPI
- Game data (stats, abilities, evolutions, genera) from [PokeAPI](https://pokeapi.co/)
- [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) (OFL) + [Vazirmatn](https://github.com/rastikerdar/vazirmatn) (OFL)
- Persian translations: names, genera, dex entries, abilities and UI — hand-written for this project

## ⚠️ Disclaimer

This is a fan-made, non-commercial educational project. Pokémon and Pokémon character names are trademarks of Nintendo, Creatures Inc. and GAME FREAK inc.
