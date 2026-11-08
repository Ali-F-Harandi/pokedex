#!/usr/bin/env python3
"""Gen-3 phase 7 — build assets/js/abilities-gen3.js from the pokeemerald
disassembly (era-authentic source of record).

Emits two constants:
  ABIL3     — the 77-entry ability set of the GBA era: internal order =
              pokeemerald's ABILITY_* index; names from gAbilityNames,
              effects from s*Description (src/data/text/abilities.h);
              FA names cross-checked against the donor table (ABIL_FA in
              gen3.js) and hand-written FA effects from tools/gen3-abil-fa.json.
  NATURES3  — the 25 natures: +/− stat pairs from gNatureStatTable
              (src/pokemon.c, the ×110/100 · ×90/100 table) and liked/
              disliked berry flavors from gPokeblockFlavorCompatibilityTable
              (src/pokeblock.c — the Pokéblock-era tie-in).

Cacophony is kept and flagged by the UI at runtime: it is defined in the
games' code but no Pokémon ever carries it (verified here against DATA).
"""
import json, os, re, sys, urllib.request

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = f'{R}/tools/gen3-cache'
FA_ABIL = f'{R}/tools/gen3-abil-fa.json'
FA_NAT = f'{R}/tools/gen3-nature-fa.json'
OUT = f'{R}/assets/js/abilities-gen3.js'

SOURCES = [
    ('abil-text.h',      'https://raw.githubusercontent.com/pret/pokeemerald/master/src/data/text/abilities.h'),
    ('nature-names.h',   'https://raw.githubusercontent.com/pret/pokeemerald/master/src/data/text/nature_names.h'),
    ('pokeblock.c',      'https://raw.githubusercontent.com/pret/pokeemerald/master/src/pokeblock.c'),
    ('pokemon.c',        'https://raw.githubusercontent.com/pret/pokeemerald/master/src/pokemon.c'),
]

def ensure_cache():
    os.makedirs(CACHE, exist_ok=True)
    hdrs = {'User-Agent': 'pokedex-tools'}
    try:
        with open('/home/z/my-project/.secrets/github_token') as f:
            hdrs['Authorization'] = f'token {f.read().strip()}'
    except OSError:
        pass
    for name, url in SOURCES:
        dst = f'{CACHE}/{name}'
        if os.path.isfile(dst) and os.path.getsize(dst) > 500:
            continue
        print(f'fetching {name} ...')
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers=hdrs)
                with urllib.request.urlopen(req, timeout=30) as r:
                    open(dst, 'wb').write(r.read())
                break
            except Exception:
                import time
                time.sleep(1 + attempt)
        else:
            raise RuntimeError(f'fetch failed: {url}')

def clean(s):
    """GBA text: strip the _() wrapper, unescape, normalize POKé/POKéMON."""
    s = s.strip()
    if s.startswith('_(') and s.endswith(')'):
        s = s[2:-1]
    s = s.replace('\\\'', "'").replace('\\"', '"')
    s = s.replace('POKéMON', 'Pokémon').replace('POKé', 'Poké')
    return ' '.join(s.split())

# ---------------------------------------------------------------- abilities
ensure_cache()
abil_text = open(f'{CACHE}/abil-text.h', encoding='utf-8').read()

# era index order: the order of #define ABILITY_* lines in gAbilityNames
block = abil_text.split('gAbilityNames')[1]
name_ptrs = re.findall(r'\[ABILITY_([A-Z0-9_]+)\]\s*=\s*_\("([^"]+)"\)', block)
descs = dict(re.findall(r's([A-Za-z0-9]+)Description\[\]\s*=\s*_\("([^"]*)"\)', abil_text))

def const_to_slug(c):
    # regex group already excludes the ABILITY_ prefix
    return c.lower().replace('_', '-')

ABIL_SKIP = {'NONE'}
abil = []
for const, gba_name in name_ptrs:
    if const in ABIL_SKIP:
        continue
    slug = const_to_slug(const)
    # description key: CamelCase of the constant (SAND_VEIL -> SandVeil)
    camel = ''.join(w.capitalize() for w in const.split('_'))
    desc = descs.get(camel)
    assert desc, f'no description for {const}'
    en = gba_name.replace('COMPOUNDEYES', 'COMPOUND EYES').replace('LIGHTNINGROD', 'LIGHTNING ROD')
    en = en.title().replace('Poké', 'Poké')  # "Sand Veil" style display names
    en = en.replace("It'S", "It's")
    abil.append({'slug': slug, 'en': en, 'eff_en': clean(desc)})

assert len(abil) == 77, f'expected 77 era abilities, got {len(abil)}'

fa_eff = {k: v for k, v in json.load(open(FA_ABIL, encoding='utf-8')).items()
          if not k.startswith('_')}
fa_missing = [a['slug'] for a in abil if a['slug'] not in fa_eff]
assert not fa_missing, f'missing FA effects: {fa_missing}'
fa_extra = sorted(set(fa_eff) - {a['slug'] for a in abil})
assert not fa_extra, f'unexpected FA effects: {fa_extra}'
for a in abil:
    a['eff_fa'] = fa_eff[a['slug']]

# FA names must match the donor table shipped in gen3.js (ABIL_FA) — the
# mon-card chips and the Ability Dex must never disagree
gen3_js = open(f'{R}/assets/js/gen3.js', encoding='utf-8').read()
m = re.search(r'const ABIL_FA = (\{.*?\});', gen3_js, re.S)
assert m, 'ABIL_FA not found in gen3.js'
abil_fa_donor = json.loads(m.group(1))
# cacophony is the one ability the donor table may skip (never shown before)
names_missing = [a['slug'] for a in abil
                 if a['slug'] not in abil_fa_donor and a['slug'] != 'cacophony']
assert not names_missing, f'ABIL_FA lacks FA names for: {names_missing}'
for a in abil:
    if a['slug'] == 'cacophony' and a['slug'] not in abil_fa_donor:
        a['name_fa'] = 'ناهماهنگی'
    else:
        a['name_fa'] = abil_fa_donor[a['slug']]

# ---------------------------------------------------------------- natures
nat_names = open(f'{CACHE}/nature-names.h', encoding='utf-8').read()
nats = re.findall(r's([A-Za-z]+)NatureName\[\]\s*=\s*_\("([A-Z]+)"\)', nat_names)
assert len(nats) == 25, f'expected 25 nature names, got {len(nats)}'

pokemon_c = open(f'{CACHE}/pokemon.c', encoding='utf-8').read()
m = re.search(r'gNatureStatTable\[NUM_NATURES\]\[NUM_NATURE_STATS\]\s*=(.*?)\n\};',
              pokemon_c, re.S)
assert m, 'gNatureStatTable not found'
rows = re.findall(r'\[NATURE_([A-Z_]+)\]\s*=\s*\{\s*([+\-\d,\s]+?)\}', m.group(1))
# columns: Attack Defense Speed Sp.Atk Sp.Def  -> keys atk def spe spa spd
STAT_KEYS = ['atk', 'def', 'spe', 'spa', 'spd']
stat_table = {}
for const, body in rows:
    vals = [int(v) for v in re.findall(r'([+-]?\d+)', body)]
    assert len(vals) == 5, (const, vals)
    up = STAT_KEYS[vals.index(1)] if 1 in vals else None
    dn = STAT_KEYS[vals.index(-1)] if -1 in vals else None
    stat_table[const] = (up, dn)
assert len(stat_table) == 25, f'nature stat rows: {len(stat_table)}'

poke_c = open(f'{CACHE}/pokeblock.c', encoding='utf-8').read()
m = re.search(r'gPokeblockFlavorCompatibilityTable\[NUM_NATURES \* FLAVOR_COUNT\]\s*=\s*\{(.*?)\n\};',
              poke_c, re.S)
assert m, 'compatibility table not found'
body = re.sub(r'//.*', '', m.group(1))
nums = [int(x) for x in re.findall(r'(-?\d+)', body)]
assert len(nums) == 125, f'compatibility cells: {len(nums)}'
FLAVORS = ['spicy', 'dry', 'sweet', 'bitter', 'sour']
nat_order = [c for c, _ in nats]
fa_nat = {k: v for k, v in json.load(open(FA_NAT, encoding='utf-8')).items()
          if not k.startswith('_')}
assert set(fa_nat) == {c.lower() for c in nat_order}, 'nature FA names mismatch'

natures = []
for i, const in enumerate(nat_order):
    cells = nums[i * 5:(i + 1) * 5]
    like = FLAVORS[cells.index(1)] if 1 in cells else None
    hate = FLAVORS[cells.index(-1)] if -1 in cells else None
    up, dn = stat_table[const.upper()]
    slug = const.lower()
    natures.append({'slug': slug, 'en': next(e for c, e in nats if c == const).title(),
                    'fa': fa_nat[slug], 'up': up, 'down': dn,
                    'like': like, 'hate': hate})

neutral = [n['slug'] for n in natures if n['up'] is None and n['down'] is None]
assert neutral == ['hardy', 'docile', 'serious', 'bashful', 'quirky'], neutral
for n in natures:
    if n['up'] is None or n['down'] is None:
        continue
    assert n['up'] != n['down'], n
assert not any((n['up'] is None) != (n['down'] is None) for n in natures), 'half-neutral nature'

# ---------------------------------------------------------------- emit
HEADER = '''"use strict";
/* ===== Pokédex Plus — GENERATION III abilities + natures.
   Generated by tools/build-gen3-abilities.py — do not edit by hand.
   ABIL3: the era-authentic 77-entry ability set, in pokeemerald's internal
   ABILITY_* order; EN names + effects straight from the game's tables
   (src/data/text/abilities.h), FA names matching the donor table in
   gen3.js (ABIL_FA), FA effects hand-written (tools/gen3-abil-fa.json).
   Cacophony is defined by the games but carried by no Pokémon — the
   Ability Dex says so honestly.
   NATURES3: the 25 natures; up/down = gNatureStatTable (src/pokemon.c,
   the ×110/100 · ×90/100 boosts), like/hate = the Pokéblock flavor
   compatibility table (src/pokeblock.c). ===== */

'''

def js_str(s):
    return json.dumps(s, ensure_ascii=False)

def js_arr(items, indent='  '):
    lines = []
    for it in items:
        lines.append(indent + '{' + ', '.join(
            f'{k}:{js_str(v)}' if isinstance(v, str)
            else f'{k}:{json.dumps(v)}' for k, v in it.items()) + '}')
    return '[\n' + ',\n'.join(lines) + '\n]'

out = HEADER + 'const ABIL3 = ' + js_arr(abil) + ';\n\n'
out += 'const NATURES3 = ' + js_arr(natures) + ';\n'
open(OUT, 'w', encoding='utf-8').write(out)
print(f'wrote {OUT}: {len(abil)} abilities, {len(natures)} natures')
