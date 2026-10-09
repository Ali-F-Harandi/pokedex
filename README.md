# Pokédex Project

**Interactive, fully offline Pokédex apps for every classic Pokémon game — each one styled exactly like its own generation.**

A single-file HTML Pokédex per game: no build tools, no server, no internet required. Just open the file (or the GitHub Pages site) and browse.

> 🌐 **Live demo:** https://ali-f-harandi.github.io/pokedex/

---

## ✅ Currently available

| Game | Generation | File | Status |
|------|-----------|------|--------|
| **Pokémon Emerald** | Gen 3 (Hoenn) | [`emerald.html`](https://ali-f-harandi.github.io/pokedex/emerald.html) | ✅ Available |

### Emerald Dex features
- All **386 Pokémon** (Gen 1–3, National Dex #001–#386)
- Original **Gen-3 / Emerald sprites** (normal **+ shiny**, rendered from a single embedded sprite atlas)
- Detailed info: types, genus, abilities (incl. hidden), height, weight, base stats with bars & total, official flavor text
- **Bilingual: English (primary) + Persian (فارسی)** — full RTL support
- Search by name (EN/FA) or number · Filter by type · Kanto / Johto / Hoenn tabs
- Shiny mode for the whole grid · Legendary/Mythical badges
- 100% offline — data, sprites and pixel font are embedded in **one ~2 MB HTML file**

## 🕹 Landing page

`index.html` is the project landing page: every mainline Pokémon game (Gen 1–9) is listed with its own themed card. **Emerald is live now** — all other games are shown as *Coming Soon* and will be added one by one, each in its own game's authentic style.

## 🗺 Roadmap

- [x] **Emerald (Gen 3)** — available
- [ ] Red / Blue / Yellow (Gen 1) — planned
- [ ] Gold / Silver / Crystal (Gen 2) — planned
- [ ] Ruby / Sapphire, FireRed / LeafGreen (Gen 3) — planned
- [ ] Gen 4–9 — planned

## 🚀 Run locally

No installation needed:

```bash
# clone and open — that's it
git clone https://github.com/Ali-F-Harandi/pokedex.git
cd pokedex
# open index.html or emerald.html in any browser
```

Or just open `emerald.html` directly — everything (data, sprites, font, styles) is inside the file.

## 📁 Project structure

```
pokedex/
├── index.html      ← landing page (game selector, EN/FA)
└── emerald.html    ← Gen-3 Emerald Pokédex (single-file, EN/FA, offline)
```

## 🛠 Built with

- Vanilla HTML/CSS/JS — zero dependencies, zero network calls
- Sprite atlas assembled from [PokeAPI sprites](https://github.com/PokeAPI/sprites) (Gen-3 Emerald set)
- [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) (OFL) embedded for the retro look

## ⚠️ Disclaimer

This is a fan-made, non-commercial educational project. Pokémon and Pokémon character names are trademarks of Nintendo, Creatures Inc. and GAME FREAK inc.
