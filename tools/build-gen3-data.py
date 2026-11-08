#!/usr/bin/env python3
"""Build assets/js/gen3-data.js — the unified Generation III data (phase 1).

Sources (the sources of record):
  · assets/js/emerald.js            — legacy donor: 386 Pokémon (stats, types,
    HT/WT, egg groups, capture, happiness, growth, habitat, gender,
    legendary/mythical, FA names, FA genus) + the Emerald-wording dex texts
    in EN and FA. The donor file itself is NEVER edited.
  · tools/gen3-cache/species/*.json — PokeAPI species (cached): per-version EN
    flavor texts for ruby / sapphire / emerald / firered / leafgreen.
  · tools/gen3-cache/species_info.h — pokeemerald disassembly: the ERA-TRUE
    ability slots (Gen 3 has no hidden abilities; Treecko has only Overgrow,
    Deoxys only Pressure — later-gen anachronisms from PokeAPI are dropped).
  · tools/gen3-fa-rs.json           — hand-written Persian, R/S wording group
    (one FA text per species; the gen2 family pattern: flavor_fa served both
    Gold and Silver wordings).
  · Deoxys formes: per-cartridge stats from PokeAPI pokemon-forms
    (R/S=Normal, FIRERED=Attack, LEAFGREEN=Defense, EMERALD=Speed).

Output layout mirrors gen2-data.js: DATA (386) + SPRITE_SETS + EVOLUTIONS.
EN dex texts are split into GBA-style pages of 4 lines.
"""
import json, os, re

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CACHE = f'{REPO}/tools/gen3-cache'
DONOR = f'{REPO}/assets/js/emerald.js'
FA_RS = f'{REPO}/tools/gen3-fa-rs.json'
OUT = f'{REPO}/assets/js/gen3-data.js'

# --------------------------------------------------------------- helpers
def donor_json(name):
    src = open(DONOR, encoding='utf-8').read()
    i = src.find(f'const {name} = ')
    m = re.search(r'[\[{]', src[i:])
    start = i + m.start()
    closer = ']' if src[start] == '[' else '}'
    nxt = src.find('\nconst ', start)
    end = src.rfind(closer, start, nxt)
    return json.loads(src[start:end + 1])

def norm(t):
    return re.sub(r'\s+', ' ', t.replace('\u00ad', '')).strip()

def wrap_pages(text, chars=26, lines=4):
    """GBA dex style: pages of `lines` wrapped lines."""
    words = text.split(' ')
    rows, cur = [], ''
    for w in words:
        if cur and len(cur) + 1 + len(w) > chars:
            rows.append(cur)
            cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur:
        rows.append(cur)
    pages = [rows[i:i + lines] for i in range(0, len(rows), lines)]
    return pages

# --------------------------------------------------------------- sources
donor_data = donor_json('DATA')
donor_evo = donor_json('EVOLUTIONS')
fa_rs = json.load(open(FA_RS, encoding='utf-8'))

species = {}
for i in range(1, 387):
    sp = json.load(open(f'{CACHE}/species/{i}.json'))
    species[i] = sp

sp_h = open(f'{CACHE}/species.h', encoding='utf-8').read()
species_const = {m.group(1): int(m.group(2))
                 for m in re.finditer(r'#define (SPECIES_[A-Z0-9_]+) (\d+)', sp_h)}
si = open(f'{CACHE}/species_info.h', encoding='utf-8').read()
abil_by_name = {}
for b in re.split(r'\n    \[SPECIES_', si)[1:]:
    nm = b.split(']')[0]
    m = re.search(r'\.abilities\s*=\s*\{(.*?)\}', b, re.S)
    if not m:
        continue
    slots = [s for s in re.findall(r'ABILITY_[A-Z0-9_]+', m.group(1)) if s != 'ABILITY_NONE']
    abil_by_name[nm] = [s[8:].lower().replace('_', '-') for s in slots]

era_abilities = {}
for i in range(1, 387):
    key = species[i]['name'].upper().replace('-', '_')
    if key in abil_by_name:
        era_abilities[i] = abil_by_name[key]

# Deoxys per-cartridge formes (PokeAPI pokemon-forms, verified 2026-11)
DEOXYS_FORMES = {
    'fr': {'label': 'attack',  'stats': {'hp': 50, 'atk': 180, 'def': 20,  'spa': 180, 'spd': 20,  'spe': 150}, 'sprite': 10013},
    'lg': {'label': 'defense', 'stats': {'hp': 50, 'atk': 70,  'def': 160, 'spa': 70,  'spd': 160, 'spe': 90},  'sprite': 10014},
    'em': {'label': 'speed',   'stats': {'hp': 50, 'atk': 95,  'def': 90,  'spa': 95,  'spd': 90,  'spe': 180}, 'sprite': 10015},
}

LEGENDARY = {144, 145, 146, 150, 243, 244, 245, 249, 250, 377, 378, 379, 380, 381, 382, 383, 384}
MYTHICAL = {151, 251, 385}

# --------------------------------------------------------------- assemble
out = []
missing = {'abilities': [], 'fa_rs': [], 'versions': []}
for d in donor_data:
    i = d['id']
    sp = species[i]
    texts = {}
    for f in sp['flavor_text_entries']:
        if f['language']['name'] == 'en':
            texts[f['version']['name']] = norm(f['flavor_text'])
    for v in ('ruby', 'sapphire', 'emerald', 'firered', 'leafgreen'):
        if v not in texts:
            missing['versions'].append((i, v))
    donor_em = norm(d['flavor'])
    em = texts.get('emerald', donor_em)
    rec = {
        'id': i, 'name': d['name'], 'display': d['display'], 'fa': d['fa'],
        'genus': d['genus'], 'genus_fa': d['genus_fa'], 'gen': d['gen'],
        'types': d['types'], 'stats': d['stats'],
        'height_dm': round(d['height'] * 10), 'weight_hg': round(d['weight'] * 10),
        'abilities': era_abilities.get(i, []),
        'baseExp': d['baseExp'], 'capture': d['capture'], 'happiness': d['happiness'],
        'growth': d['growth'], 'egg': d['egg'], 'genderRate': d['genderRate'],
        'habitat': d.get('habitat'),
        'legendary': i in LEGENDARY, 'mythical': i in MYTHICAL,
        'trs': wrap_pages(texts['ruby']),
        'tem': wrap_pages(em),
        'tfr': wrap_pages(texts['firered']),
        'flavor_fa': d['flavor_fa'],
        'fa_rs': fa_rs[str(i)],
    }
    if texts['sapphire'] != texts['ruby']:
        rec['ts'] = wrap_pages(texts['sapphire'])
    if texts['leafgreen'] != texts['firered']:
        rec['tlg'] = wrap_pages(texts['leafgreen'])
    if i == 386:
        rec['formes'] = DEOXYS_FORMES
    if not rec['abilities']:
        missing['abilities'].append(i)
    out.append(rec)

assert not missing['versions'], missing['versions'][:5]
assert not missing['abilities'], missing['abilities'][:10]
assert len(out) == 386

# --------------------------------------------------------------- sprites
def bank(prefix, extra=None):
    b = {
        'label': prefix,
        'color': True,
        'files': {'normal': f'assets/sprites/{prefix}/__ID__.png',
                  'shiny': f'assets/sprites/{prefix}-shiny/__ID__.png'},
        'back': {'normal': f'assets/sprites/{prefix}-back/__ID__.png',
                 'shiny': f'assets/sprites/{prefix}-back-shiny/__ID__.png'},
    }
    if extra:
        b.update(extra)
    return b

# rs/frlg banks are shared by the cartridge pairs; forme ids (10013-10015)
# live inside the same folders. Emerald: atlas stills + the anim webp set;
# its back view reuses the R/S bank (pokeemerald's back sprites are
# byte-identical to pokeruby's — verified against both disassemblies).
SPRITE_SETS = {
    'rs': bank('gen3-rs'),
    'em': bank('gen3-emerald', {
        'anim': 'assets/sprites/gen3-emerald-anim/__ID__.webp',
        'back': {'normal': 'assets/sprites/gen3-rs-back/__ID__.png',
                 'shiny': 'assets/sprites/gen3-rs-back-shiny/__ID__.png'},
    }),
    'frlg': bank('gen3-frlg'),
}

def js(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))

header = '''"use strict";
/* ===== Pokédex Plus — GENERATION III data (Ruby · Sapphire · Emerald ·
   FireRed · LeafGreen). Generated by tools/build-gen3-data.py — do not edit
   by hand. 386 Pokémon; trs/ts/tem/tfr/tlg = the Ruby(+shared Sapphire),
   Sapphire-only, Emerald, FireRed(+shared LeafGreen) and LeafGreen-only dex
   texts (EN pages of 4 GBA-style lines); fa_rs = Persian R/S wording,
   flavor_fa = Persian Emerald wording (the FRLG Persian wording lands with
   the phase-2 run — FA mode falls back to EN until then, the gen2 pattern).
   abilities are the ERA-TRUE Gen-3 slots from the pokeemerald disassembly —
   no hidden abilities existed yet. Deoxys rides the cartridge:
   formes.fr/lg/em carry the per-game stats + sprite ids. SPRITE_SETS
   rs/em/frlg = GBA sprite banks with shiny + back variants; em.anim =
   Emerald's animated battle set. ===== */
const DATA = '''

body = (
    js(out)
    + ';\nconst SPRITE_SETS = ' + js(SPRITE_SETS) + ';\n'
    + 'const EVOLUTIONS = ' + js(donor_evo) + ';\n'
)

open(OUT, 'w', encoding='utf-8').write(header + body)
print(f'gen3-data.js written: {os.path.getsize(OUT)} bytes, {len(out)} pokémon')
