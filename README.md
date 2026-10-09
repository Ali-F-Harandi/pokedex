# Pokédex Project

**Interactive, fully offline Pokédex apps for every classic Pokémon game — each one styled exactly like the dex inside its own game.**

A single-file HTML Pokédex per game: no build tools, no server, no internet required. Just open the file (or the GitHub Pages site) and browse.

> 🌐 **Live site:** https://ali-f-harandi.github.io/pokedex/
>
> ▶️ **Emerald dex:** https://ali-f-harandi.github.io/pokedex/emerald.html

---

## ✅ Currently available

| Game | Generation | File | Status |
|------|-----------|------|--------|
| **Pokémon Emerald** | Gen 3 (Hoenn) | [`emerald.html`](https://ali-f-harandi.github.io/pokedex/emerald.html) | ✅ Available |

### Emerald Dex — features

- All **386 Pokémon** (Gen 1–3, National Dex #001–#386)
- UI faithful to the **in-game Pokémon Emerald Pokédex**: cream screen, red `POKé DEX` badge, red selection bar with pointer arrow, sprite card, `DEX STATUS` counters, `START · MENU` button
- **Dex modes** like the game: `NATIONAL / KANTO / JOHTO / HOENN`
- **Seen / Owned tracking** — browsing marks a Pokémon as *Seen* (automatic), the Poké Ball button marks it as *Owned*; live counters per region, saved in your browser
- Original **Gen-3 / Emerald sprites** — normal **+ shiny** (single embedded sprite atlas)
- Detail view: dex entry, base stats with colored bars, gen-3-accurate **type matchups** (×4 / ×2 / ½ / ¼ / immune), full **evolution line** with conditions, abilities (incl. hidden), catch rate, happiness, growth rate, egg groups, habitat, gender ratio
- Search by name (EN/FA) or number · type filter chips · sort by number / name / stats · favorites · random
- **START menu** (in-game style popup): search, random, shiny, favorites, sort, reset progress, language, about
- Keyboard: `↑ ↓ ← →` browse · `/` search · `S` shiny · `R` random · `Esc` close
- Deep links: `emerald.html#025` opens Pokémon #025
- **Bilingual: English (primary) + Persian (فارسی)** — full RTL, Persian digits, translated names/types/entries/abilities/evolutions
- 100% offline — data, sprites and fonts are embedded in **one ~2.3 MB HTML file**

## 🏠 Landing page

`index.html` is the **game-neutral** project hub (dark neutral theme, not tied to any single game): every mainline Pokémon game (Gen 1–9, 35 games) is listed with its own colored card. **Emerald is live now** — all other games are *Coming Soon* and will be added one by one, each faithful to its own game's style, data and sprites. Bilingual EN/FA as well.

## 🗺 Roadmap

- [x] **Emerald (Gen 3)** — available
- [ ] Ruby / Sapphire, FireRed / LeafGreen (Gen 3) — next
- [ ] Red / Blue / Yellow (Gen 1), Gold / Silver / Crystal (Gen 2) — planned
- [ ] Gen 4–9 — planned

## 🚀 Run locally

No installation needed:

```bash
git clone https://github.com/Ali-F-Harandi/pokedex.git
cd pokedex
# open index.html or emerald.html in any browser — works fully offline
```

## 📁 Project structure

```
pokedex/
├── index.html      ← game-neutral landing page (catalog + roadmap, EN/FA)
└── emerald.html    ← Gen-3 Emerald in-game-style Pokédex (single-file, EN/FA, offline)
```

## 🛠 Built with

- Vanilla HTML/CSS/JS — zero dependencies, zero network calls
- Sprites from the [PokeAPI sprites](https://github.com/PokeAPI/sprites) project (Gen-3 Emerald set), packed into one atlas
- Data (stats, entries, abilities, evolutions) from [PokeAPI](https://pokeapi.co/)
- [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) (OFL) + [Vazirmatn](https://github.com/rastikerdar/vazirmatn) (OFL) embedded as woff2

## ⚠️ Disclaimer

This is a fan-made, non-commercial educational project. Pokémon and Pokémon character names are trademarks of Nintendo, Creatures Inc. and GAME FREAK inc.
