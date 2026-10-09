# Pokédex Project

**Interactive, fully offline Pokédex apps for classic Pokémon games — each one styled exactly like the dex inside its own game.**

Every dex shares one structure and feature set; only the theme changes per game. Pages are small HTML entries that load their CSS, JS, sprites, cries and fonts from local files in `assets/` — no build step, no server, no internet required.

> 🌐 **Live site:** https://ali-f-harandi.github.io/pokedex/
>
> ▶️ **Emerald dex (Gen 3):** https://ali-f-harandi.github.io/pokedex/emerald.html
>
> ▶️ **Red/Blue dex (Gen 1):** https://ali-f-harandi.github.io/pokedex/red-blue.html

---

## ✅ Currently available

| Game | Generation | File | Status |
|------|-----------|------|--------|
| **Pokémon Emerald** | Gen 3 (Hoenn) | [`emerald.html`](https://ali-f-harandi.github.io/pokedex/emerald.html) | ✅ Available |
| **Pokémon Red/Blue** | Gen 1 (Kanto) | [`red-blue.html`](https://ali-f-harandi.github.io/pokedex/red-blue.html) | ✅ Available |

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
- **Four authentic sprite sets**, switchable from the sprite card or the START menu:
  - `R/B` — original Game Boy monochrome sprites, in **DMG green** and **Pocket gray** screen palettes
  - `COLOR` — the very same Red/Blue sprites, colorized
  - `YELLOW` — the redrawn sprites from Pokémon **Yellow**, the enhanced Gen-1 version (colored)
  - `GBC` — colored sprites from Pokémon **Gold** (Game Boy Color era)
- **Authentic Red/Blue cries** for all 151 Pokémon (local OGG files)
- Pokédex entries transcribed from the [`pret/pokered`](https://github.com/pret/pokered) decompilation: original 2-page text, authentic categories, in-game imperial HT/WT
- Authentic **Gen-1 type chart** — including the famous R/B quirks (Ghost ×0 vs Psychic, Bug ×2 vs Poison)
- Entry text flips pages like the original · seen/owned tracking · cries playable from the side menu

### Both dexes

- **Bilingual: English (primary) + Persian (فارسی)** — full RTL, Persian digits, translated names/types/entries/abilities/evolutions
- **100% offline** — all data, sprites, cries and fonts are plain local files next to each page
- Landing page (`index.html`) is **game-neutral**: one catalog item per game — complementary pairs like Red/Blue or Ruby/Sapphire share a single item

## 🏠 Landing page

`index.html` is the project hub (dark neutral theme, not tied to any single game). Every mainline Pokémon game (Gen 1–9) is listed with its own colored card; **Emerald** and **Red/Blue** are live now, everything else is *Coming Soon* and will follow one by one. Bilingual EN/FA.

## 🗺 Roadmap

- [x] **Emerald (Gen 3)** — available
- [x] **Red / Blue (Gen 1)** — available (Yellow sprites included; Yellow's own dex may come later)
- [ ] Ruby / Sapphire, FireRed / LeafGreen (Gen 3) — next
- [ ] Gold / Silver / Crystal (Gen 2) — planned
- [ ] Gen 4–9 — planned

## 🚀 Run locally

No installation needed:

```bash
git clone https://github.com/Ali-F-Harandi/pokedex.git
cd pokedex
# open index.html (or emerald.html / red-blue.html) directly in any browser —
# everything works offline, even over file://
```

## 📁 Project structure

```
pokedex/
├── index.html                  ← game-neutral landing page (catalog + roadmap, EN/FA)
├── emerald.html                ← Gen-3 Emerald dex entry page
├── red-blue.html               ← Gen-1 Red/Blue dex entry page
└── assets/
    ├── css/                    ← one stylesheet per page (emerald / redblue / landing)
    ├── js/                     ← data + logic per page (emerald / redblue / landing)
    ├── fonts/                  ← Press Start 2P + Vazirmatn (woff2, OFL)
    ├── img/                    ← favicon, Emerald sprite atlas, featured-card images
    ├── sprites/
    │   ├── gen3-emerald-anim/  ← 386 animated battle sprites (lossless WebP)
    │   ├── gen1-rb-dmg/        ← Red/Blue Game Boy mono, DMG green palette
    │   ├── gen1-rb-pocket/     ← Red/Blue Game Boy mono, Pocket gray palette
    │   ├── gen1-rb-color/      ← Red/Blue sprites, colorized
    │   ├── gen1-yellow/        ← Yellow sprites (colored)
    │   └── gen1-gold/          ← Gold sprites (Game Boy Color)
    └── audio/cries/            ← 151 authentic Red/Blue cries (ogg)
```

Each HTML page is tiny (6–12 KB) and pulls in its own CSS/JS plus the shared `assets/` folder. Adding a new game dex = one more HTML entry + one CSS + one JS + a sprite folder — everything else is reused.

## 🛠 Built with

- Vanilla HTML/CSS/JS — zero dependencies, zero network calls
- Sprites from the [PokeAPI sprites](https://github.com/PokeAPI/sprites) project:
  - `generation-iii/emerald` — static + animated battle sprites (Emerald)
  - `generation-i/red-blue` + `generation-i/yellow` — Gen-1 sprites (mono conversions + colored originals)
  - `generation-ii/gold` — Gen-1 Pokémon as seen in Gold (GBC color)
- Pokédex entry texts, categories and in-game HT/WT from the [`pret/pokered`](https://github.com/pret/pokered) decompilation
- Game data (stats, abilities, evolutions, genera) from [PokeAPI](https://pokeapi.co/)
- [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) (OFL) + [Vazirmatn](https://github.com/rastikerdar/vazirmatn) (OFL)
- Persian translations: names, genera, dex entries, abilities and UI — hand-written for this project

## ⚠️ Disclaimer

This is a fan-made, non-commercial educational project. Pokémon and Pokémon character names are trademarks of Nintendo, Creatures Inc. and GAME FREAK inc.
