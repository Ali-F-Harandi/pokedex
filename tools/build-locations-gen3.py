#!/usr/bin/env python3
"""Pokédex Plus — Phases 5+6: the LOCATION DEX data for Generation III.

Sources of truth (cached under tools/loc3-cache/, refresh with --refetch):
  pret/pokeruby     wild_encounters.json carries BOTH Ruby and Sapphire
                    via paired headers (Xxx_Ruby / Xxx_Sapphire base labels)
  pret/pokeemerald  wild_encounters.json (gWildMonHeaders only — the
                    Battle Pyramid/Pike groups are post-game facilities)
  pret/pokefirered  wild_encounters.json carries BOTH FireRed and LeafGreen
                    via paired headers (Xxx_FireRed / Xxx_LeafGreen) — the
                    phase-6 Kanto + Sevii set; parsed FRESH (never reused
                    from the gen1 locations data)
  pret map.json     MAP -> region_map_section (MAPSEC identity + names via
                    the region map sections list)
  pret scripts      the specials live in map scripts / trade tables /
                    roamer code — levels curated in tools/loc3-specials.py
                    (Hoenn) and tools/loc3_frlg.py (Kanto/Sevii)

Authentic engine facts encoded here (from the disassemblies):
  · land tables: 12 slots, shared chances 20/20/10/10/10/10/5/5/4/4/1/1
  · water (surf) + rock smash: 5 slots, chances 60/30/5/4/1
  · fishing: per-map 10-slot tables grouped old [70,30] / good [60,20,20] /
    super [40,40,15,4,1]; every cast rolls a 50% bite chance first
    (wild_encounter.c `Random() & 1` — same in FRLG field_player_avatar.c);
    levels roll min..max per slot
  · NO time-of-day tables (Gen 3 dropped day/night wilds)
  · Emerald mass outbreaks (swarms): 5 entries, 50% replacement chance
  · dead data excluded: pokeemerald's CaveOfOrigin_UnusedRubySapphireMap1-3
    wild headers are unreachable (their scripts carry FLAG_UNUSED_RS_*);
    Terra/Marine Caves hold no wild tables — only the Lv 70 static battles
  · Altering Cave (both RSE and FRLG): the 9 headers are Mystery-Gift table
    sets; the default (set 0, all Zubat) is shown, with a note listing the
    swapped species

Outputs:
  assets/js/locations-gen3.js  LOC3 — regions.hoenn (phase 5) and
    regions.kanto (phase 6, FireRed/LeafGreen: Kanto + Sevii Islands) with
    per-game per-room tables, deduped fish tables, specials, bilingual
    notes; the FRLG tables fall back leafgreen -> firered like R/S.

Usage:
  python3 tools/build-locations-gen3.py             # parse + emit
  python3 tools/build-locations-gen3.py --refetch   # re-download pret sources
"""
import argparse
import json
import os
import re
import sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from loc3_names import LOC_NAMES, ROOMS, LOC_POS_OVERRIDES
from loc3_specials import SPECIALS, SWARMS, LOC_NOTES
from loc3_frlg import (LOC_NAMES_FRLG, ROOMS_FRLG, SPECIALS_FRLG,
                       LOC_NOTES_FRLG, UNOWN_SETS, POS_FRLG, FORCE_NOTES_FRLG)

assert os.path.isfile(f'{sys.path[0]}/loc3_names.py')
assert os.path.isfile(f'{sys.path[0]}/loc3_frlg.py')

CACHE = f'{REPO}/tools/loc3-cache'
RUBY = f'{CACHE}/pokeruby'
EMERALD = f'{CACHE}/pokeemerald'
FIRERED = f'{CACHE}/pokefirered'
TARBALLS = {
    'pokeruby':   'https://codeload.github.com/pret/pokeruby/tar.gz/refs/heads/master',
    'pokeemerald': 'https://codeload.github.com/pret/pokeemerald/tar.gz/refs/heads/master',
    'pokefirered': 'https://codeload.github.com/pret/pokefirered/tar.gz/refs/heads/master',
}
GAMES = ['ruby', 'sapphire', 'emerald']
FRLG_GAMES = ['firered', 'leafgreen']
LAND_PCT = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]   # ENCOUNTER_CHANCE_MONS
WATER_PCT = [60, 30, 5, 4, 1]                            # water & rock smash
FISH_PCT = {'o': [70, 30], 'g': [60, 20, 20], 's': [40, 40, 15, 4, 1]}
BITE = 50                                                # Random() & 1
# pokeemerald's CaveOfOrigin_UnusedRubySapphireMap1-3 are unreachable dead
# data in Emerald (Terra/Marine Caves replace them; scripts carry
# FLAG_UNUSED_RS_LEGENDARY_BATTLE_DONE) — exclude their wild headers.
DEAD_MAPS = {
    'MAP_CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP1',
    'MAP_CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP2',
    'MAP_CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP3',
}


def ensure_repos(refetch):
    os.makedirs(CACHE, exist_ok=True)
    import tarfile, urllib.request, shutil
    for name, url in TARBALLS.items():
        dest = f'{CACHE}/{name}'
        if os.path.isdir(dest) and not refetch:
            continue
        print(f'fetching {name}…')
        tar = f'{CACHE}/{name}.tar.gz'
        urllib.request.urlretrieve(url, tar)
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        with tarfile.open(tar) as tf:
            tf.extractall(CACHE)
        os.rename(f'{CACHE}/{name}-master', dest)


def load_mapdirs(root):
    """MAP constant -> (dir name, region_map_section)."""
    import glob
    m = {}
    for f in glob.glob(f'{root}/data/maps/*/map.json'):
        d = json.load(open(f))
        m[d.get('id')] = (os.path.basename(os.path.dirname(f)), d.get('region_map_section'))
    return m


def load_sections(root):
    """MAPSEC -> (pretty EN name, x, y)."""
    d = json.load(open(f'{root}/src/data/region_map/region_map_sections.json'))['map_sections']
    return {s['id']: (s['name'], s.get('x'), s.get('y')) for s in d}


def load_species(root):
    """SPECIES_* constant -> internal id (explicit numeric values; BOTH
    pokeemerald and pokeruby use internal Hoenn-ordered ids — POOCHYENA 286,
    WURMPLE 290, DEOXYS 410 — so the national table below is required)."""
    out = {}
    txt = open(f'{root}/include/constants/species.h', errors='replace').read()
    for name, val in re.findall(r'#define SPECIES_([A-Z0-9_]+)\s+(\d+)', txt):
        if name == 'NONE':
            continue
        out[f'SPECIES_{name}'] = int(val)
    return out


def load_national(root):
    """SPECIES_* constant name -> national dex number (1..386).
    pokeruby: gSpeciesToNationalPokedexNum[] with `NATIONAL_DEX_X, //
    SPECIES_Y` pairs + explicit NATIONAL_DEX defines.
    pokeemerald: sSpeciesToNationalPokedexNum[] designated initializers
    `[SPECIES_X - 1] = NATIONAL_DEX_Y` + the NATIONAL_DEX_* enum order in
    constants/pokedex.h."""
    txt = open(f'{root}/include/constants/species.h', errors='replace').read()
    national = {f'SPECIES_{n}': int(v) for n, v in
                re.findall(r'#define NATIONAL_DEX_([A-Z0-9_]+)\s+(\d+)', txt)}
    if not national:  # pokeemerald: enum order == national order
        pdx = open(f'{root}/include/constants/pokedex.h', errors='replace').read()
        i = pdx.find('enum {')
        j = pdx.find('};', i)
        names = re.findall(r'NATIONAL_DEX_([A-Z0-9_]+)', pdx[i:j])
        national = {f'SPECIES_{n}': idx for idx, n in enumerate(names) if n != 'NONE'}
    src = os.path.basename(root) == 'pokeemerald' and 'src/pokemon.c' or 'src/pokemon_1.c'
    arr = open(f'{root}/{src}', errors='replace').read()
    out = {}
    # pokeruby pairs: `NATIONAL_DEX_Y, // SPECIES_X` (last line has no comma)
    for y, x in re.findall(r'NATIONAL_DEX_([A-Z0-9_]+)\s*,?\s*//\s*SPECIES_([A-Z0-9_]+)', arr):
        if f'SPECIES_{y}' in national:
            out[f'SPECIES_{x}'] = national[f'SPECIES_{y}']
    # pokeemerald: `SPECIES_TO_NATIONAL(NAME)` = SPECIES_NAME -> NATIONAL_DEX_NAME
    for x in re.findall(r'SPECIES_TO_NATIONAL\(([A-Z0-9_]+)\)', arr):
        if f'SPECIES_{x}' in national:
            out[f'SPECIES_{x}'] = national[f'SPECIES_{x}']
    # pokeemerald designated initializers (future-proof)
    for x, y in re.findall(r'\[SPECIES_([A-Z0-9_]+)\s*-\s*1\]\s*=\s*NATIONAL_DEX_([A-Z0-9_]+)', arr):
        if f'SPECIES_{y}' in national:
            out[f'SPECIES_{x}'] = national[f'SPECIES_{y}']
    return {k: v for k, v in out.items() if 1 <= v <= 386}


def load_encounters(root, species, mapdirs):
    """game -> {map: {land/surf/rk/fish raw tables}}."""
    groups = json.load(open(f'{root}/src/data/wild_encounters.json'))['wild_encounter_groups']
    g0 = [g for g in groups if g.get('for_maps') and g['label'] == 'gWildMonHeaders'][0]
    out = {}
    for e in g0['encounters']:
        mc = e['map']
        if mc in DEAD_MAPS or mc not in mapdirs:
            continue
        tb = {}
        for key, k in [('land_mons', 'land'), ('water_mons', 'surf'), ('rock_smash_mons', 'rk'), ('fishing_mons', 'fish')]:
            if key not in e:
                continue
            mons = [[species[m['species']], m['min_level'], m['max_level']]
                    for m in e[key]['mons'] if m['species'] in species]
            if mons:
                tb[k] = {'r': e[key]['encounter_rate'], 'mons': mons}
        if tb:
            out[mc] = tb
    return out


def split_rs(raw):
    """unused — parse_rs_with_labels does the R/S pairing."""
    return {}, {}


def parse_rs_with_labels(root, species, mapdirs):
    groups = json.load(open(f'{root}/src/data/wild_encounters.json'))['wild_encounter_groups']
    g0 = [g for g in groups if g.get('for_maps') and g['label'] == 'gWildMonHeaders'][0]
    tables = {'ruby': {}, 'sapphire': {}}
    for e in g0['encounters']:
        mc = e['map']
        if mc not in mapdirs:
            continue
        game = 'sapphire' if '_Sapphire' in e.get('base_label', '') else 'ruby'
        tb = {}
        for key, k in [('land_mons', 'land'), ('water_mons', 'surf'), ('rock_smash_mons', 'rk'), ('fishing_mons', 'fish')]:
            if key not in e:
                continue
            mons = [[species[m['species']], m['min_level'], m['max_level']]
                    for m in e[key]['mons'] if m['species'] in species]
            if mons:
                tb[k] = {'r': e[key]['encounter_rate'], 'mons': mons}
        if tb:
            tables[game][mc] = tb
    return tables


def fish_key(rows):
    return json.dumps(rows)


def parse_frlg_with_labels(root, species, mapdirs):
    """game -> {map: {land/surf/rk/fish raw tables}} — pokefirered pairs
    FireRed/LeafGreen via base_label suffixes, exactly like pokeruby."""
    groups = json.load(open(f'{root}/src/data/wild_encounters.json'))['wild_encounter_groups']
    g0 = [g for g in groups if g.get('for_maps') and g['label'] == 'gWildMonHeaders'][0]
    tables = {'firered': {}, 'leafgreen': {}}
    for e in g0['encounters']:
        mc = e['map']
        if mc not in mapdirs:
            continue
        game = 'leafgreen' if '_LeafGreen' in e.get('base_label', '') else 'firered'
        tb = {}
        for key, k in [('land_mons', 'land'), ('water_mons', 'surf'), ('rock_smash_mons', 'rk'), ('fishing_mons', 'fish')]:
            if key not in e:
                continue
            mons = [[species[m['species']], m['min_level'], m['max_level']]
                    for m in e[key]['mons'] if m['species'] in species]
            if mons:
                tb[k] = {'r': e[key]['encounter_rate'], 'mons': mons}
        if tb:
            tables[game][mc] = tb
    return tables


def build_kanto():
    """Phase 6: the FireRed/LeafGreen region set — Kanto + Sevii Islands,
    parsed fresh from pokefirered (never reused from the gen1 data)."""
    fr_mapdirs = load_mapdirs(FIRERED)
    # pokefirered's SPECIES_* constants ARE national-dex numbers (1..386)
    fr_species = load_species(FIRERED)

    tables = parse_frlg_with_labels(FIRERED, fr_species, fr_mapdirs)

    fishpool, fishidx = [], {}
    def put_fish(rows):
        key = fish_key(rows)
        if key not in fishidx:
            fishidx[key] = len(fishpool)
            fishpool.append({'o': rows[0:2], 'g': rows[2:5], 's': rows[5:10]})
        return fishidx[key]

    # ---- group maps by MAPSEC per game, build rooms ----
    secmaps = {g: {} for g in FRLG_GAMES}
    for g, tab in tables.items():
        for mc, tb in tab.items():
            _, sec = fr_mapdirs.get(mc, (None, None))
            if not sec:
                continue
            secmaps[g].setdefault(sec, []).append((mc, tb))

    locs = {}
    for g in FRLG_GAMES:
        for sec, entries in secmaps[g].items():
            loc = locs.setdefault(sec, {'t': {}})
            rooms = []
            for mc, tb in sorted(entries):
                dirn = fr_mapdirs.get(mc, (None, None))[0]
                label = ROOMS_FRLG.get(dirn, (None, None, None))
                rl = label[0] or ''
                rm = {'rm': rl, 'rml': label[2] if label[0] else 0,
                      'en': label[0], 'fa': label[1],
                      'dir': dirn, 'tb': tb}
                if label[0] is None:
                    rm['rm'] = ''
                rooms.append(rm)
            merged = []
            for rm in sorted(rooms, key=lambda x: (x['rml'], x['dir'])):
                same = next((m for m in merged if m['en'] == rm['en']), None)
                if same and fish_key(same['tb']) == fish_key(rm['tb']):
                    continue  # identical table, same label — merge
                merged.append(rm)
            out = []
            for rm in merged:
                tb = rm['tb']
                blk = {'rm': rm['en'], 'rmf': rm['fa']}
                if 'land' in tb:
                    blk['land'] = {'r': tb['land']['r'], 's': tb['land']['mons']}
                if 'surf' in tb:
                    blk['surf'] = {'r': tb['surf']['r'], 'w': tb['surf']['mons']}
                if 'rk' in tb:
                    blk['rk'] = {'r': tb['rk']['r'], 's2': tb['rk']['mons']}
                if 'fish' in tb:
                    blk['f'] = put_fish(tb['fish']['mons'])
                out.append(blk)
            loc['t'][g] = out

    # ---- FR/LG dedupe: leafgreen table omitted when identical to firered
    # (module falls back leafgreen -> firered) ----
    dedup_keys = set()
    for sec, loc in locs.items():
        t = loc['t']
        if 'firered' in t and 'leafgreen' in t and fish_key(t['firered']) == fish_key(t['leafgreen']):
            del t['leafgreen']
            dedup_keys.add(sec)

    # ---- assemble locations (special-only sections come from the
    # specials' loc anchors; Unown chambers carry their letter-set note;
    # FORCE_NOTES add wild-free Sevii towns for region coverage) ----
    sp_secs = {s['loc'] for s in SPECIALS_FRLG if s.get('loc')}
    all_secs = set(locs.keys()) | sp_secs | set(FORCE_NOTES_FRLG)
    missing = sorted(s for s in all_secs if s not in LOC_NAMES_FRLG)
    if missing:
        sys.exit('missing bilingual FRLG names for: ' + ', '.join(missing))
    no_pos = sorted(s for s in all_secs if s not in POS_FRLG)
    if no_pos:
        sys.exit('missing list order for: ' + ', '.join(no_pos))

    out_locs = []
    for sec in sorted(all_secs, key=lambda s: POS_FRLG[s]):
        en, fa, grp = LOC_NAMES_FRLG[sec]
        loc = locs.get(sec, {'t': {}})
        t = {}
        for g in FRLG_GAMES:
            if g in loc['t']:
                t[g] = loc['t'][g]
            elif any(sp.get('loc') == sec and g in sp['v'] for sp in SPECIALS_FRLG):
                t[g] = None if sec not in dedup_keys else loc['t'].get('firered')
            # else: no key — can't happen for FRLG (both games share the map)
        exists = {g: (g in t) for g in FRLG_GAMES}
        ent = {'id': sec, 'en': en, 'fa': fa, 'g': grp, 'o': POS_FRLG[sec], 'ex': exists, 't': t}
        note = dict(LOC_NOTES_FRLG.get(sec) or {})
        fn = FORCE_NOTES_FRLG.get(sec)
        if fn:
            note = {'en': (note.get('en') + ' ' + fn['en']) if note.get('en') else fn['en'],
                    'fa': (note.get('fa') + ' ' + fn['fa']) if note.get('fa') else fn['fa']}
        if sec in UNOWN_SETS:
            unl = 'Unown live here (Lv 25): ' + UNOWN_SETS[sec][0]
            unf = 'آن‌کون‌های این اتاق (سطح ۲۵): ' + UNOWN_SETS[sec][1]
            note = {'en': (note.get('en') + ' ' + unl) if note.get('en') else unl,
                    'fa': (note.get('fa') + ' ' + unf) if note.get('fa') else unf}
        if note:
            ent['note'] = note
        out_locs.append(ent)

    sp_out = [{'m': s['m'], 'v': s['v'], 'k': s['k'], **({'loc': s['loc']} if 'loc' in s else {}),
               'd': s['d'],
               **({'note': s['note']} if 'note' in s else {})}
              for s in SPECIALS_FRLG]

    return {'games': FRLG_GAMES, 'locs': out_locs, 'fish': fishpool,
            'sp': sp_out, 'swarms': []}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--refetch', action='store_true')
    args = ap.parse_args()
    ensure_repos(args.refetch)

    em_mapdirs = load_mapdirs(EMERALD)
    sections = load_sections(EMERALD)
    em_species = load_national(EMERALD)
    rb_species = load_national(RUBY)
    rb_mapdirs = load_mapdirs(RUBY)

    em = load_encounters(EMERALD, em_species, em_mapdirs)
    rs = parse_rs_with_labels(RUBY, rb_species, rb_mapdirs)
    gametables = {'ruby': rs['ruby'], 'sapphire': rs['sapphire'], 'emerald': em}

    # ---- fish table dedup (shared pool).  A fish table is the engine's
    # 10-slot row list, grouped by rod: [0:2] old, [2:5] good, [5:10] super.
    # Stored as {o,g,s} — the shape the module renders. ----
    fishpool, fishidx = [], {}
    def put_fish(rows):
        key = fish_key(rows)
        if key not in fishidx:
            fishidx[key] = len(fishpool)
            fishpool.append({'o': rows[0:2], 'g': rows[2:5], 's': rows[5:10]})
        return fishidx[key]

    # ---- group maps by MAPSEC per game, build rooms (each repo resolves
    # its own map constants: MAP_MAGMA_HIDEOUT_1F maps to EVIL_TEAM_HIDEOUT
    # in pokeruby but to MAPSEC_MAGMA_HIDEOUT in pokeemerald) ----
    secmaps = {g: {} for g in GAMES}
    gmdirs = {'ruby': rb_mapdirs, 'sapphire': rb_mapdirs, 'emerald': em_mapdirs}
    for g, tables in gametables.items():
        for mc, tb in tables.items():
            _, sec = gmdirs[g].get(mc, (None, None))
            if not sec:
                continue
            secmaps[g].setdefault(sec, []).append((mc, tb))

    locs = {}
    for g in GAMES:
        for sec, entries in secmaps[g].items():
            loc = locs.setdefault(sec, {'t': {}})
            # group by room label; merge identical tables under one label
            rooms = []
            for mc, tb in sorted(entries):
                dirn = gmdirs[g].get(mc, (None, None))[0]
                label = ROOMS.get(dirn, (None, None, None))
                rl = label[0] or ''
                rm = {'rm': rl, 'rml': label[2] if label[0] else 0,
                      'en': label[0], 'fa': label[1],
                      'dir': dirn, 'tb': tb}
                if label[0] is None:
                    rm['rm'] = ''
                rooms.append(rm)
            merged = []
            for rm in sorted(rooms, key=lambda x: (x['rml'], x['dir'])):
                same = next((m for m in merged if m['en'] == rm['en']), None)
                if same and fish_key(same['tb']) == fish_key(rm['tb']):
                    continue  # identical table, same label — merge
                merged.append(rm)
            out = []
            for rm in merged:
                tb = rm['tb']
                blk = {'rm': rm['en'], 'rmf': rm['fa']}
                if 'land' in tb:
                    blk['land'] = {'r': tb['land']['r'], 's': tb['land']['mons']}
                if 'surf' in tb:
                    blk['surf'] = {'r': tb['surf']['r'], 'w': tb['surf']['mons']}
                if 'rk' in tb:
                    blk['rk'] = {'r': tb['rk']['r'], 's2': tb['rk']['mons']}
                if 'fish' in tb:
                    blk['f'] = put_fish(tb['fish']['mons'])
                out.append(blk)
            loc['t'][g] = out

    # ---- R/S dedupe (gen2 rule): sapphire table omitted when identical to
    # ruby — the module falls back sapphire -> ruby ----
    dedup_keys = set()
    for sec, loc in locs.items():
        t = loc['t']
        if 'ruby' in t and 'sapphire' in t and fish_key(t['ruby']) == fish_key(t['sapphire']):
            del t['sapphire']
            dedup_keys.add(sec)

    # ---- assemble locations with names/groups/order ----
    used = set(locs.keys()) | set(LOC_POS_OVERRIDES.keys())
    special_only = ['MAPSEC_AQUA_HIDEOUT', 'MAPSEC_MAGMA_HIDEOUT', 'MAPSEC_TERRA_CAVE',
                    'MAPSEC_MARINE_CAVE', 'MAPSEC_SOUTHERN_ISLAND', 'MAPSEC_NAVEL_ROCK',
                    'MAPSEC_BIRTH_ISLAND', 'MAPSEC_FARAWAY_ISLAND', 'MAPSEC_BATTLE_FRONTIER',
                    'MAPSEC_LITTLEROOT_TOWN', 'MAPSEC_LAVARIDGE_TOWN', 'MAPSEC_RUSTBORO_CITY',
                    'MAPSEC_FORTREE_CITY', 'MAPSEC_DESERT_RUINS', 'MAPSEC_ISLAND_CAVE',
                    'MAPSEC_ANCIENT_TOMB']
    all_secs = set(locs.keys()) | set(special_only)
    missing = sorted(s for s in all_secs if s not in LOC_NAMES)
    if missing:
        sys.exit('missing bilingual names for: ' + ', '.join(missing))
    dead_pos = [s for s in all_secs if s not in sections]
    order_extra = {s: i for i, s in enumerate(sorted(dead_pos))} if dead_pos else {}

    out_locs = []
    for sec in all_secs:
        en, fa, grp = LOC_NAMES[sec]
        loc = locs.get(sec, {'t': {}})
        # a special-only loc "exists" only in the games that reference it;
        # deduped sapphire keys are OMITTED (module falls back to ruby) —
        # explicit null = the game has the area but truly no wilds there
        t = {}
        for g in GAMES:
            has_rooms = g in loc['t']
            has_sp = any(sp.get('loc') == sec and g in sp['v'] for sp in SPECIALS)
            if has_rooms:
                t[g] = loc['t'][g]
            elif has_sp and (sec not in dedup_keys):
                t[g] = None
            # else: no key — the area doesn't exist in this game
        if not t:
            continue
        # exists-flag: which games actually contain this area (deduped
        # sapphire exists too — it reads ruby's tables)
        exists = {}
        for g in GAMES:
            has_rooms = g in loc['t'] or (g == 'sapphire' and sec in dedup_keys and 'ruby' in loc['t'])
            has_sp = any(sp.get('loc') == sec and g in sp['v'] for sp in SPECIALS)
            exists[g] = bool(has_rooms or has_sp)
        name, _, _ = sections.get(sec, ('?', None, None))
        x, y = None, None
        if sec in LOC_POS_OVERRIDES:
            x, y = LOC_POS_OVERRIDES[sec]
        else:
            _, x, y = sections.get(sec, ('?', None, None))
        o = (y or 0) * 1000 + (x or 0) * 10
        if sec in order_extra:
            o += order_extra[sec]
        ent = {'id': sec, 'en': en, 'fa': fa, 'g': grp, 'o': o, 'ex': exists, 't': t}
        if sec in LOC_NOTES:
            ent['note'] = LOC_NOTES[sec]
        out_locs.append(ent)
    out_locs.sort(key=lambda l: (l['o'], l['id']))

    # ---- specials (ids already curated; roamers carry no loc) ----
    sp_out = [{'m': s['m'], 'v': s['v'], 'k': s['k'], **({'loc': s['loc']} if 'loc' in s else {}),
               'd': s['d'],
               **({'note': s['note']} if 'note' in s else {})}
              for s in SPECIALS]

    doc = {
        'games': GAMES,
        'landPct': LAND_PCT,
        'waterPct': WATER_PCT,
        'fishPct': FISH_PCT,
        'bite': BITE,
        'regions': {
            'hoenn': {'games': ['ruby', 'sapphire', 'emerald'],
                      'locs': out_locs, 'fish': fishpool, 'sp': sp_out,
                      'swarms': SWARMS},
            'kanto': build_kanto(),   # phase 6: FireRed / LeafGreen (Kanto + Sevii)
        },
    }

    js = json.dumps(doc, ensure_ascii=False, separators=(',', ':'))
    header = (
        '"use strict";\n'
        '/* Pokédex Plus — GENERATION III location & encounter data (gen3.html).\n'
        '   Generated by tools/build-locations-gen3.py from the pret decompiles\n'
        '   (pokeruby = Ruby + Sapphire paired headers, pokeemerald, pokefirered\n'
        '   = FireRed + LeafGreen paired headers) — do not edit by hand.\n'
        '   regions.hoenn (R/S/E) + regions.kanto (FR/LG: Kanto + Sevii) carry\n'
        '   the same shapes: land {r, s: 12 slots [id, min, max]} with shared\n'
        '   landPct (20/20/10/10/10/10/5/5/4/4/1/1); surf {r, w: 5 slots} + rk\n'
        '   {r, s2} share waterPct (60/30/5/4/1); f = fish-table index (fish\n'
        '   tables {o:[2], g:[3], s:[5]} carry rows [id, min, max] with shared\n'
        '   fishPct per rod: old 70/30, good 60/20/20, super 40/40/15/4/1;\n'
        '   bite 50% — the engine rolls `Random() & 1` per bite round).\n'
        '   Levels roll min..max.\n'
        '   A paired version\'s identical table is OMITTED (sapphire reads\n'
        '   ruby, leafgreen reads firered); null = the game has the area but\n'
        '   no wilds there; missing game key = the area does not exist in that\n'
        '   game (ex tells which games contain it).\n'
        '   sp: special ways to obtain (starters, egg, gift, fossil, trades,\n'
        '   statics, roamers, ticket events) with authentic levels from the\n'
        '   pret scripts; swarms: Emerald TV mass outbreaks (50%). */\n'
        'const LOC3 = '
    )
    out = f'{REPO}/assets/js/locations-gen3.js'
    open(out, 'w', encoding='utf-8').write(header + js + ';\n')
    n_rooms = sum(len(b) for l in out_locs for b in l['t'].values() if b)
    k = doc['regions']['kanto']
    k_rooms = sum(len(b) for l in k['locs'] for b in l['t'].values() if b)
    print(f'hoenn: {len(out_locs)} locs, {len(fishpool)} fish, {len(sp_out)} specials, {len(SWARMS)} swarms, {n_rooms} rooms')
    print(f'kanto: {len(k["locs"])} locs, {len(k["fish"])} fish, {len(k["sp"])} specials, {k_rooms} rooms')
    print(f'wrote {out} ({os.path.getsize(out)} bytes)')


if __name__ == '__main__':
    main()
