# Pokédex Project

**Interactive, fully offline Pokédex apps for classic Pokémon games — each one styled exactly like the dex inside its own game.**

Every dex shares one structure and feature set; only the theme changes per game. Pages are small HTML entries that load their CSS, JS, sprites, cries and fonts from local files in `assets/` — no build step, no server, no internet required.

> 🌐 **Live site:** https://ali-f-harandi.github.io/pokedex/
>
> ▶️ **Emerald dex (Gen 3):** https://ali-f-harandi.github.io/pokedex/emerald.html
>
> ▶️ **Red/Blue dex (Gen 1):** https://ali-f-harandi.github.io/pokedex/red-blue.html
>
> ▶️ **Yellow dex (Gen 1):** https://ali-f-harandi.github.io/pokedex/yellow.html
>
> ▶️ **Gold/Silver dex (Gen 2):** https://ali-f-harandi.github.io/pokedex/goldsilver.html

---

## ✅ Currently available

| Game | Generation | File | Status |
|------|-----------|------|--------|
| **Pokémon Emerald** | Gen 3 (Hoenn) | [`emerald.html`](https://ali-f-harandi.github.io/pokedex/emerald.html) | ✅ Available |
| **Pokémon Red/Blue** | Gen 1 (Kanto) | [`red-blue.html`](https://ali-f-harandi.github.io/pokedex/red-blue.html) | ✅ Available |
| **Pokémon Yellow** | Gen 1 (Kanto) | [`yellow.html`](https://ali-f-harandi.github.io/pokedex/yellow.html) | ✅ Available |
| **Pokémon Gold/Silver** | Gen 2 (Johto) | [`goldsilver.html`](https://ali-f-harandi.github.io/pokedex/goldsilver.html) | ✅ Available |

### Emerald Dex — features

- All **386 Pokémon** (Gen 1–3, National Dex #001–#386)
- UI faithful to the **in-game Pokémon Emerald Pokédex**: cream screen, red `POKé DEX` badge, red selection bar with pointer arrow, sprite card, `DEX STATUS` counters, `START · MENU` button
- **Dex modes** like the game: `NATIONAL / KANTO / JOHTO / HOENN`
- **Animated battle sprites** — Emerald was the first game to animate its battle sprites; all 386 authentic animations are included as lossless WebP, with a toggle (START menu / `Anim` button / key `A`)
- Emerald sprites **normal + shiny** (single local sprite atlas)
- Detail view: dex entry, base stats with colored bars, gen-3-accurate **type matchups**, full **evolution line** with conditions, abilities (incl. hidden), catch rate, happiness, growth rate, egg groups, habitat, gender ratio
- Search (EN/FA/number) · type filter chips · sort · favorites · random · seen/owned tracking (saved in browser)
- Keyboard: `↑ ↓ ← →` browse · `/` search · `S` shiny · `A` anim · `R` random · `Esc` close · deep links (`emerald.html#025`)

### Red/Blue Dex — features

- All **151 Kanto Pokémon**, same structure and feature set as the Emerald dex, themed after the Game Boy era in a restrained way (gray shell, DMG-tinted screen — no console gimmicks)
- **Two authentic sprite sets**, switchable from the sprite card or the START menu:
  - `R/B` — original Game Boy monochrome sprites, in **DMG green** and **Pocket gray** screen palettes
  - `COLOR` — the very same Red/Blue sprites, colorized
- **Authentic Red/Blue cries** for all 151 Pokémon (local OGG files)
- Pokédex entries transcribed from the [`pret/pokered`](https://github.com/pret/pokered) decompilation: original 2-page text, authentic categories, in-game imperial HT/WT
- Authentic **Gen-1 type chart** — including the famous R/B quirks (Ghost ×0 vs Psychic, Bug ×2 vs Poison)
- Entry text flips pages like the original · seen/owned tracking · cries playable from the side menu

### Yellow Dex — features

- A **dedicated Pokédex for Pokémon Yellow**, with the same structure as the Emerald and Red/Blue dexes and its own yellow-accented Game Boy theme
- **Yellow's own dex entries** — Yellow rewrote all 151 entry texts; they are transcribed from the [`pret/pokeyellow`](https://github.com/pret/pokeyellow) decompilation (original 2-page text, authentic categories, in-game HT/WT), not reused from Red/Blue
- **Yellow's own sprites**, switchable from the sprite card or the START menu:
  - `Y` — the Yellow-version Game Boy sprites in monochrome, in **DMG green** and **Pocket gray** palettes
  - `COLOR` — the same Yellow sprites, colorized
- Includes the anime-famous **yellow Pikachu** sprite and every other redrawn version-specific sprite
- **Authentic Gen-1 cries** (shared local OGG files) · entry page-flipping · seen/owned tracking
- Authentic **Gen-1 type chart** — the same mechanics Yellow used

### Gold/Silver Dex — features

- A **dedicated Pokédex for Pokémon Gold & Silver** (all **251 Johto + Kanto Pokémon**), same structure as the other dexes, themed after the Game Boy Color era with a **Gold accent**
- **Each version's own in-game sprites**, switchable from the sprite card or the START menu:
  - `GOLD` — Gold's own sprites
  - `SILVER` — Silver's own sprites (Gold and Silver redrew many of them)
- **Shiny sprites** for every Pokémon — shiny Pokémon were introduced in this generation (`Shiny` button, START menu or key `S`)
- **Both versions' dex entry texts**: Gold and Silver rewrote most entries — small `GOLD` / `SILVER` buttons on the entry box switch between the two authentic texts (EN); the box still flips pages like the original
- The **Palette/Version button** recolors the whole dex between Gold and Silver accents
- Counters split like the game: **Kanto / Johto / Total** seen & owned
- Authentic **Gen-2 type chart** — Dark & Steel types included, `Ghost ×2 vs Psychic` fixed
- **Authentic cries** for all 251 (local OGG files) · seen/owned tracking · full detail grid (catch rate, happiness, growth, egg groups, habitat, gender)

### All dexes

- **Bilingual: English (primary) + Persian (فارسی)** — full RTL, Persian digits, translated names/types/entries/abilities/evolutions
- **100% offline** — all data, sprites, cries and fonts are plain local files next to each page
- Landing page (`index.html`) is **game-neutral**: one catalog item per game — complementary pairs like Red/Blue or Ruby/Sapphire share a single item

## 🏠 Landing page

`index.html` is the project hub (dark neutral theme, not tied to any single game). Every mainline Pokémon game (Gen 1–9) is listed with its own colored card; **Emerald**, **Red/Blue**, **Yellow** and **Gold/Silver** are live now, everything else is *Coming Soon* and will follow one by one. Bilingual EN/FA.

## 🗺 Roadmap

- [x] **Emerald (Gen 3)** — available
- [x] **Red / Blue (Gen 1)** — available
- [x] **Yellow (Gen 1)** — available (Yellow's own sprites and Yellow's own dex entries)
- [x] **Gold / Silver (Gen 2)** — available (both versions' sprites + shiny, both versions' dex texts)
- [ ] Crystal (Gen 2), Ruby / Sapphire, FireRed / LeafGreen (Gen 3) — next
- [ ] Gen 4–9 — planned

## 🚀 Run locally

No installation needed:

```bash
git clone https://github.com/Ali-F-Harandi/pokedex.git
cd pokedex
# open index.html (or emerald.html / red-blue.html / yellow.html / goldsilver.html) directly in any browser —
# everything works offline, even over file://
```

## 📁 Project structure

```
pokedex/
├── index.html                  ← game-neutral landing page (catalog + roadmap, EN/FA)
├── emerald.html                ← Gen-3 Emerald dex entry page
├── red-blue.html               ← Gen-1 Red/Blue dex entry page
├── yellow.html                 ← Gen-1 Yellow dex entry page
├── goldsilver.html             ← Gen-2 Gold/Silver dex entry page
└── assets/
    ├── css/                    ← one stylesheet per page (emerald / redblue / yellow / goldsilver / landing)
    ├── js/                     ← data + logic per page (emerald / redblue / yellow / goldsilver / landing)
    ├── fonts/                  ← Press Start 2P + Vazirmatn (woff2, OFL)
    ├── img/                    ← favicon, Emerald sprite atlas, featured-card images
    ├── sprites/
    │   ├── gen3-emerald-anim/  ← 386 animated battle sprites (lossless WebP)
    │   ├── gen1-rb-dmg/        ← Red/Blue Game Boy mono, DMG green palette
    │   ├── gen1-rb-pocket/     ← Red/Blue Game Boy mono, Pocket gray palette
    │   ├── gen1-rb-color/      ← Red/Blue sprites, colorized
    │   ├── gen1-y-dmg/         ← Yellow Game Boy mono, DMG green palette
    │   ├── gen1-y-pocket/      ← Yellow Game Boy mono, Pocket gray palette
    │   ├── gen1-yellow/        ← Yellow sprites, colorized
    │   ├── gen2-gold/          ← Gold's own sprites (251)
    │   ├── gen2-silver/        ← Silver's own sprites (251)
    │   ├── gen2-gold-shiny/    ← Gold shiny variants (251)
    │   └── gen2-silver-shiny/  ← Silver shiny variants (251)
    └── audio/cries/            ← 251 authentic cries (ogg, shared by all Gen-1/2 dexes)
```

Each HTML page is tiny (6–12 KB) and pulls in its own CSS/JS plus the shared `assets/` folder. Adding a new game dex = one more HTML entry + one CSS + one JS + a sprite folder — everything else is reused.

## 🛠 Built with

- Vanilla HTML/CSS/JS — zero dependencies, zero network calls
- Sprites from the [PokeAPI sprites](https://github.com/PokeAPI/sprites) project:
  - `generation-iii/emerald` — static + animated battle sprites (Emerald)
  - `generation-i/red-blue` — Red/Blue sprites (mono conversions + colored originals)
  - `generation-i/yellow` — Yellow sprites (mono conversions + colored originals)
  - `generation-ii/gold` + `generation-ii/silver` (+ `shiny`) — each version's own sprites (Gold/Silver)
- Pokédex entry texts, categories and in-game HT/WT from the [`pret/pokered`](https://github.com/pret/pokered) and [`pret/pokeyellow`](https://github.com/pret/pokeyellow) decompilations; Gold/Silver EN texts per version from PokeAPI
- Game data (stats, abilities, evolutions, genera) from [PokeAPI](https://pokeapi.co/)
- [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) (OFL) + [Vazirmatn](https://github.com/rastikerdar/vazirmatn) (OFL)
- Persian translations: names, genera, dex entries, abilities and UI — hand-written for this project

## ⚠️ Disclaimer

This is a fan-made, non-commercial educational project. Pokémon and Pokémon character names are trademarks of Nintendo, Creatures Inc. and GAME FREAK inc.
