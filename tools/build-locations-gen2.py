#!/usr/bin/env python3
"""Pokédex Plus — Phase 5: the LOCATION DEX data for Generation II.

Sources of truth (cached under tools/loc2-cache/, refresh with --refetch):
  pret/pokecrystal  wild grass/surf (morning/day/night), fish groups,
                    headbutt trees, swarm tables, map fish-group attrs,
                    npc trades, game-corner prizes, static battles   (C)
  pret/pokegold     the same files carry BOTH G/S via IF DEF(_GOLD) /
                    ELIF DEF(_SILVER) blocks (pokered-style)         (G/S)

Authentic engine facts encoded here (from the disassembly):
  · grass tables have NUM_GRASSMON = 7 slots; slot chances are the shared
    GrassMonProbTable 30/30/20/10/5/4/1 (%), per time of day, with the
    map's own morn/day/nite encounter rates
  · water (surf) tables have NUM_WATERMON = 3 slots, chances 60/30/10;
    the engine adds +0..+4 to the listed level (35/30/20/10 % ladder)
  · fishing is per fish group: bite chance + Old/Good/Super rod tables
    with cumulative `percent` thresholds (picked when Random <= thr);
    some Good/Super slots read TimeFishGroups — morning+day share one
    species/level, night has its own
  · headbutt/rock-smash share the TreeMons mechanic: each map has a tree
    set; each set has a common and a rare table whose `db %` weights
    pick the species; TREEMON_SET_ROCK is used when smashing rocks
  · swarms: Crystal replaces a map's grass for the day (Yanma Route 35,
    Dunsparce Dark Cave) and swaps the fish group (Qwilfish Route 32);
    Gold/Silver only have the two fishing swarms (Qwilfish Route 32,
    Remoraid Route 44) — their swarm-grass files are dead data (no
    script ever calls StoreSwarmMapIndices), so they are excluded here
  · the Bug-Catching Contest uses ContestMons (% weights, level ranges);
    the -1 VENOMOTH row is an engine fallback that never triggers —
    Venomoth is NOT catchable in the contest
  · static battles (loadwildmon in map scripts) and gifts (givepoke,
    GiveShuckle special) are curated below with authentic levels and
    version splits: Lugia 70/40/60, Ho-Oh 40/70/60 (G/S/C), Snorlax 50,
    Red Gyarados 30, Sudowoodo 20, Lapras 20 (Friday), Tyrogue 10,
    Eevee 20, Shuckle 15, Dratini: Goldenrod Game Corner 10 (G/S) /
    Dragon Shrine 15 (C), the Crystal-only Odd Egg, roaming
    Raikou/Entei/Suicune (G/S: all three roam; Crystal: Raikou/Entei
    roam, Suicune waits on Tin Tower 1F).

Outputs:
  assets/js/locations-gen2.js   LOC2 — every location of Johto & Kanto with
                                its encounter tables for all three games
                                (bilingual EN/FA names) + the special ways
                                to obtain Pokémon (starters, eggs, gifts,
                                trades, corners, statics, roamers, event).

Usage:
  python3 tools/build-locations-gen2.py             # parse + emit
  python3 tools/build-locations-gen2.py --refetch   # re-download pret sources
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CACHE = f'{REPO}/tools/loc2-cache'
GOLD = f'{CACHE}/pokegold-master'          # carries G/S via version IFs
CRY = f'{CACHE}/pokecrystal-master'
TARBALLS = {
    'pokegold':    'https://codeload.github.com/pret/pokegold/tar.gz/refs/heads/master',
    'pokecrystal': 'https://codeload.github.com/pret/pokecrystal/tar.gz/refs/heads/master',
}
GAMES = ['gold', 'silver', 'crystal']
GRASS_PCT = [30, 30, 20, 10, 5, 4, 1]     # GrassMonProbTable
WATER_PCT = [60, 30, 10]                  # WaterMonProbTable


def rd(root, relpath):
    return open(f'{root}/{relpath}', errors='replace').read()


# ---------------------------------------------------------------- fetch ----
def ensure_repos(refetch):
    os.makedirs(CACHE, exist_ok=True)
    for name, url in TARBALLS.items():
        dstdir = f'{CACHE}/{name}-master'
        if os.path.isdir(dstdir) and not refetch:
            continue
        dst = f'{CACHE}/{name}.tar.gz'
        if refetch or not os.path.exists(dst):
            print(f'  fetching {name} ...')
            urllib.request.urlretrieve(url, dst)
        subprocess.run(['tar', 'xzf', dst, '-C', CACHE], check=True)

# ------------------------------------------------------- species mapping ----
def build_species():
    """internal constant -> dex id (Gen 2 internal ids = dex ids for all 251).
    The `; NN` comments are HEX (CHIKORITA ; 98 = 0x98 = 152)."""
    consts = {}
    for line in rd(GOLD, 'constants/pokemon_constants.asm').splitlines():
        m = re.match(r'\s*const\s+([A-Z_0-9]+)\s*;\s*([0-9A-Fa-f]+)\s*$', line)
        if m:
            v = int(m.group(2), 16)
            if 1 <= v <= 251:
                consts[m.group(1)] = v
    assert consts.get('BULBASAUR') == 1 and consts.get('CHIKORITA') == 152 \
        and consts.get('CELEBI') == 251 and consts.get('SENTRET') == 161 \
        and consts.get('YANMA') == 193 and consts.get('UNOWN') == 201 \
        and consts.get('DUNSPARCE') == 206 and consts.get('QWILFISH') == 211 \
        and consts.get('REMORAID') == 223 and consts.get('SUICUNE') == 245, 'species map broken'
    return consts

# ------------------------------------------------------- version helpers ----
def walk_versions(lines):
    """yield (game_or_None, line) — None = applies to every game of the file.
    gold files: IF DEF(_GOLD) / ELIF DEF(_SILVER) / ENDC; crystal files have
    no version blocks."""
    ctx = None
    for raw in lines:
        s = raw.strip()
        if re.match(r'IF\s+DEF\(_GOLD\)', s):
            ctx = 'gold'; continue
        if re.match(r'ELIF\s+DEF\(_SILVER\)', s):
            ctx = 'silver'; continue
        if s.startswith('ENDC'):
            ctx = None; continue
        yield ctx, raw

# -------------------------------------------------------- grass / water ----
def parse_wild_file(text, spmap, games):
    """-> {const: {game: table}}. grass table {'m','d','n': {'r':pct,'s':[[id,lvl]×7]}}
    water table {'wr':pct,'w':[[id,lo]×3]}. Lines outside IFs apply to all
    games in `games`; IF DEF(_GOLD)/ELIF DEF(_SILVER) bodies to one each."""
    out = {}
    state = {'kind': None, 'const': None, 'tkey': None, 'rates': []}

    def new_def(kind, const):
        state.update(kind=kind, const=const, tkey=None, rates=[],
                     cur={g: ({'w': []} if kind == 'water' else {}) for g in games})

    def targets(ctx):
        if ctx is None:
            return list(games)
        return [ctx] if ctx in games else []

    def emit(kind):
        const = state['const']
        for g, tb in state['cur'].items():
            if kind == 'grass':
                for t in ('m', 'd', 'n'):
                    if t in tb and len(tb[t]['s']) != 7:
                        sys.exit(f'!! grass {const} {g} {t}: {len(tb[t]["s"])} slots')
                if not any(t in tb for t in ('m', 'd', 'n')):
                    continue          # version branch absent (e.g. gold-only def)
            else:
                if 'wr' not in tb:
                    continue          # version branch absent
                if len(tb['w']) != 3:
                    sys.exit(f'!! water {const} {g}: {len(tb["w"])} slots')
            out.setdefault(const, {})[g] = tb

    for ctx, raw in walk_versions(text.splitlines()):
        s = raw.strip()
        m = re.match(r'def_(grass|water)_wildmons\s+([A-Z_0-9]+)', s)
        if m:
            new_def(m.group(1), m.group(2))
            continue
        kind = state['kind']
        if kind is None:
            continue
        m = re.match(r'db\s+(.+?)\s*;\s*encounter rates', s)
        if m and kind == 'grass':
            state['rates'] = [int(re.match(r'(\d+)', x.strip()).group(1))
                              for x in m.group(1).split(',')]
            continue
        m = re.match(r'db\s+(\d+)\s*percent\s*;\s*encounter rate', s)
        if m and kind == 'water':
            r = int(m.group(1))
            for g in targets(ctx):
                state['cur'][g]['wr'] = r
            continue
        m = re.match(r';\s*(morn|day|nite)', s)
        if m and kind == 'grass':
            tkey = {'morn': 'm', 'day': 'd', 'nite': 'n'}[m.group(1)]
            idx = {'m': 0, 'd': 1, 'n': 2}[tkey]
            state['tkey'] = tkey
            for g in targets(ctx):
                state['cur'][g][tkey] = {'r': state['rates'][idx], 's': []}
            continue
        if s.startswith('end_'):
            emit(kind)
            state.update(kind=None, const=None, tkey=None)
            continue
        m = re.match(r'db\s+(\d+)\s*,\s*([A-Z_0-9]+)', s)
        if m and kind:
            sp = m.group(2)
            if sp not in spmap:
                sys.exit(f'!! unknown species {sp} in {state["const"]}')
            lvl = int(m.group(1))
            for g in targets(ctx):
                tb = state['cur'][g]
                if kind == 'grass':
                    if state['tkey'] and state['tkey'] in tb:
                        tb[state['tkey']]['s'].append([spmap[sp], lvl])
                elif 'w' in tb:
                    # the engine adds +0..+4 to the listed surf level
                    tb['w'].append([spmap[sp], lvl])
    return out


def parse_all_wild(spmap):
    res = {g: {} for g in GAMES}
    src = rd(GOLD, 'data/wild/johto_grass.asm') + '\n' + rd(GOLD, 'data/wild/kanto_grass.asm')
    gg = parse_wild_file(src, spmap, ['gold', 'silver'])
    src = rd(GOLD, 'data/wild/johto_water.asm') + '\n' + rd(GOLD, 'data/wild/kanto_water.asm')
    gw = parse_wild_file(src, spmap, ['gold', 'silver'])
    src = rd(CRY, 'data/wild/johto_grass.asm') + '\n' + rd(CRY, 'data/wild/kanto_grass.asm')
    cg = parse_wild_file(src, spmap, ['crystal'])
    src = rd(CRY, 'data/wild/johto_water.asm') + '\n' + rd(CRY, 'data/wild/kanto_water.asm')
    cw = parse_wild_file(src, spmap, ['crystal'])
    for d in (gg, gw, cg, cw):
        for const, per in d.items():
            for g, tb in per.items():
                slot = res[g].setdefault(const, {})
                slot.update(tb)          # grass (m/d/n) + water (wr/w) merge
    return res

# ------------------------------------------------------------- fishing ----
def parse_pct(tok):
    """'50 percent + 1' -> int(50*255/100)+1 (the pokeasm `percent` macro)."""
    m = re.match(r'(\d+)\s*percent(?:\s*\+\s*(\d+))?', tok.strip())
    return int(m.group(1)) * 255 // 100 + int(m.group(2) or 0)


def parse_fish(spmap):
    """-> 13 groups: {'bite':pct, 'o':[[id,lvl,pct]...], 'g':..., 's':...}.
    fish.asm is identical across G/S/C — parse once from pokegold.
    `time_group N` slots become 5-length rows [day id, day lvl, nite id,
    nite lvl, %] (TimeFishGroups: morning+day share the first pair)."""
    text = rd(GOLD, 'data/wild/fish.asm')
    timetbl = {}
    m = re.search(r'^TimeFishGroups:\s*$(.*)', text, re.M | re.S)
    for row in re.findall(r'db\s+([A-Z_0-9]+),\s*(\d+),\s*([A-Z_0-9]+),\s*(\d+)\s*;', m.group(1)):
        timetbl[len(timetbl)] = {'d': [spmap[row[0]], int(row[1])],
                                 'n': [spmap[row[2]], int(row[3])]}
    m = re.search(r'^FishGroups:\s*$(.*?)^\.\w+_Old:', text, re.M | re.S)
    gnames = re.findall(r'fishgroup\s+(.+?),\s*\.(\w+)_Old', m.group(1))
    bite_by_name, order = {}, []
    for bite, name in gnames:
        bite_by_name[name] = parse_pct(bite)
        order.append(name)
    body = text[m.end(1):]
    tabs = {}
    for m2 in re.finditer(r'^\.(\w+)_(Old|Good|Super):\s*$(.*?)(?=^\.\w+_(?:Old|Good|Super):|^TimeFishGroups:|\Z)', body, re.M | re.S):
        name, rod, blk = m2.group(1), m2.group(2).lower(), m2.group(3)
        rows, prev = [], -1
        for line in blk.splitlines():
            s = line.strip()
            m3 = re.match(r'db\s+(\d+)\s*percent(?:\s*\+\s*(\d+))?\s*,\s*time_group\s+(\d+)', s)
            if m3:
                thr = int(m3.group(1)) * 255 // 100 + int(m3.group(2) or 0)
                rows.append(('t', int(m3.group(3)), round((thr - prev) / 256 * 100, 1)))
                prev = thr
                continue
            m3 = re.match(r'db\s+(\d+)\s*percent(?:\s*\+\s*(\d+))?\s*,\s*([A-Z_0-9]+)\s*,\s*(\w+)', s)
            if not m3:
                continue
            thr = int(m3.group(1)) * 255 // 100 + int(m3.group(2) or 0)
            pct = round((thr - prev) / 256 * 100, 1)
            prev = thr
            rows.append((spmap[m3.group(3)], int(m3.group(4)), pct))
        tabs[(name, rod)] = rows
    groups = []
    rod_key = {'o': 'old', 'g': 'good', 's': 'super'}
    for name in order:
        g = {'bite': bite_by_name[name]}
        for rod in ('o', 'g', 's'):
            rows = []
            for r in tabs[(name, rod_key[rod])]:
                if r[0] == 't':
                    tt = timetbl[r[1]]
                    d, n = tt['d'], tt['n']
                    rows.append([d[0], d[1], n[0], n[1], r[2]])
                else:
                    rows.append([r[0], r[1], r[2]])
            g[rod] = rows
        groups.append(g)
    assert len(groups) == 13, len(groups)
    assert groups[0]['o'] == [[129, 10, 70.3], [129, 10, 14.8], [98, 10, 14.8]], groups[0]['o']
    return groups

FISHGROUP_CONST = {}     # FISHGROUP_* -> 1-based value; FishGroups[] index = value - 1

def fishgroup_index():
    global FISHGROUP_CONST
    for line in rd(GOLD, 'constants/map_data_constants.asm').splitlines():
        m = re.match(r'\s*const\s+(FISHGROUP_[A-Z_0-9]+)\s*$', line)
        if m:
            FISHGROUP_CONST[m.group(1)] = len(FISHGROUP_CONST)
    assert FISHGROUP_CONST.get('FISHGROUP_NONE') == 0 \
        and FISHGROUP_CONST.get('FISHGROUP_SHORE') == 1 \
        and FISHGROUP_CONST.get('FISHGROUP_QWILFISH') == 11 \
        and FISHGROUP_CONST.get('FISHGROUP_REMORAID') == 12 \
        and FISHGROUP_CONST.get('FISHGROUP_QWILFISH_NO_SWARM') == 13, FISHGROUP_CONST
    return FISHGROUP_CONST

# ----------------------------------------------------- map fish groups ----
def parse_fish_attrs(game):
    """map const -> FishGroups[] index, from data/maps/maps.asm 8th `map` field."""
    root = CRY if game == 'crystal' else GOLD
    text = rd(root, 'data/maps/maps.asm')
    n2c = {}
    for m in re.finditer(r'map_attributes (\w+),\s*([A-Z_0-9]+),', rd(root, 'data/maps/attributes.asm')):
        n2c[m.group(1)] = m.group(2)
    out = {}
    for line in text.splitlines():
        m = re.match(r'\s*map\s+(\w+),\s*[A-Z_0-9]+,\s*\w+,\s*[A-Z_0-9]+,\s*[A-Z_0-9]+,\s*(?:TRUE|FALSE),\s*[A-Z_0-9]+,\s*(FISHGROUP_[A-Z_0-9]+)', line)
        if m:
            const = n2c.get(m.group(1))
            if const:
                out[const] = FISHGROUP_CONST.get(m.group(2), 1) - 1
    return out

# ------------------------------------------------------ headbutt / rocks ----
def parse_treemon_sets(game, spmap):
    """-> {set: {game: {'c':[[id,lvl,pct]...], 'r':[...]}}}. Version-aware:
    gold and silver get separate rows from pokegold's IF/ELIF blocks."""
    root = CRY if game == 'crystal' else GOLD
    text = rd(root, 'data/wild/treemons.asm')
    sets = {}
    for m in re.finditer(r'^TreeMonSet_(\w+):\s*$(.*?)(?=^TreeMonSet_\w+:|\Z)', text, re.M | re.S):
        name, blk = m.group(1), m.group(2)
        per = {g: {'c': [], 'seen_sep': False}
               for g in (['gold', 'silver'] if game != 'crystal' else ['crystal'])}
        for ctx, raw in walk_versions(blk.splitlines()):
            tgts = list(per.keys()) if ctx is None else ([ctx] if ctx in per else [])
            s = raw.strip()
            if re.match(r'db\s+-1\s*$', s):
                for tg in tgts:
                    per[tg]['seen_sep'] = True
                continue          # `db -1` separates common|rare (or terminates)
            m2 = re.match(r'db\s+(-?\d+)\s*,\s*([A-Z_0-9]+)\s*,\s*(\d+)', s)
            if not m2:
                continue
            pct, sp, lvl = int(m2.group(1)), m2.group(2), int(m2.group(3))
            if sp not in spmap:
                sys.exit(f'!! unknown tree species {sp}')
            for tg in tgts:
                key = 'c' if not per[tg]['seen_sep'] else 'r'
                per[tg].setdefault(key, []).append([spmap[sp], lvl, pct])
        sets[name] = {}
        for tg, d in per.items():
            rare = d.get('r', [])
            sets[name][tg] = {'c': d['c'], 'r': rare if rare else d['c']}
    return sets


def parse_treemon_maps(game):
    """map const -> TREEMON_SET_* name"""
    root = CRY if game == 'crystal' else GOLD
    out = {}
    for line in rd(root, 'data/wild/treemon_maps.asm').splitlines():
        m = re.match(r'\s*treemon_map\s+([A-Z_0-9]+)\s*,\s*TREEMON_SET_(\w+)', line.strip())
        if m:
            out[m.group(1)] = m.group(2)
    return out

# --------------------------------------------------------------- swarm ----
def parse_swarm(game, spmap):
    """-> {const: grass-table} for crystal (map_id format), {} for G/S —
    the G/S swarm grass/water files are dead data: no script in Gold/Silver
    ever calls StoreSwarmMapIndices (only the two fishing swarms are
    triggerable there), so they must not surface as obtainable."""
    if game != 'crystal':
        return {}
    text = rd(CRY, 'data/wild/swarm_grass.asm')
    out, const, tkey, rates = {}, None, None, []
    for raw in text.splitlines():
        s = raw.strip()
        m = re.match(r'map_id\s+([A-Z_0-9]+)', s)
        if m:
            const, tkey, rates = m.group(1), None, []
            continue
        m = re.match(r'db\s+(.+?)\s*;\s*encounter rates', s)
        if m and const:
            rates = [int(re.match(r'(\d+)', x.strip()).group(1)) for x in m.group(1).split(',')]
            continue
        m = re.match(r';\s*(morn|day|nite)', s)
        if m and const:
            tkey = {'morn': 'm', 'day': 'd', 'nite': 'n'}[m.group(1)]
            out.setdefault(const, {})[tkey] = {'r': rates[{'m': 0, 'd': 1, 'n': 2}[tkey]], 's': []}
            continue
        m = re.match(r'db\s+(\d+)\s*,\s*([A-Z_0-9]+)', s)
        if m and const and tkey:
            out[const][tkey]['s'].append([spmap[m.group(2)], int(m.group(1))])
    for const, tb in out.items():
        for t in ('m', 'd', 'n'):
            if t in tb and len(tb[t]['s']) != 7:
                sys.exit(f'!! crystal swarm {const} {t}: {len(tb[t]["s"])} slots')
    return out

# --------------------------------------------------------------- contest ----
def parse_contest(spmap):
    text = rd(GOLD, 'data/wild/bug_contest_mons.asm')
    m = re.search(r'^ContestMons:\s*$(.*)', text, re.M | re.S)
    rows = []
    for line in m.group(1).splitlines():
        mm = re.match(r'\s*db\s+(-?\d+)\s*,\s*([A-Z_0-9]+)\s*,\s*(\d+)\s*,\s*(\d+)', line)
        if not mm:
            continue
        pct = int(mm.group(1))
        if pct < 0:
            continue      # the -1 VENOMOTH fallback never triggers
        rows.append([spmap[mm.group(2)], int(mm.group(3)), int(mm.group(4)), pct])
    assert sum(r[3] for r in rows) == 100 and len(rows) == 10, rows
    return rows

# ---------------------------------------------------------------- trades ----
def parse_trades(game, spmap):
    """-> [{give, get, nick, map}] — locations from `trade NPC_TRADE_X` in maps."""
    root = CRY if game == 'crystal' else GOLD
    tconst = {}
    for line in rd(root, 'constants/npc_trade_constants.asm').splitlines():
        m = re.match(r'\s*const\s+NPC_TRADE_([A-Z_0-9]+)\s*;', line)
        if m:
            tconst[m.group(1)] = len(tconst)
    place = {}
    for fname in os.listdir(f'{root}/maps'):
        if not fname.endswith('.asm'):
            continue
        src = rd(root, f'maps/{fname}')
        for m in re.finditer(r'trade\s+NPC_TRADE_([A-Z_0-9]+)', src):
            place[tconst.get(m.group(1))] = fname[:-4]
    rows, idx = [], 0
    for m in re.finditer(r'npctrade\s+TRADE_DIALOGSET_\w+,\s*([A-Z_0-9]+),\s*([A-Z_0-9]+),\s*"([^"]+)"', rd(root, 'data/events/npc_trades.asm')):
        rows.append({'give': spmap[m.group(1)], 'get': spmap[m.group(2)],
                     'nick': m.group(3), 'map': place.get(idx, '')})
        idx += 1
    return rows

# ------------------------------------------------------- game corners ----
def parse_corner(game, spmap):
    """-> [{'mon','lvl','price','map','v'}] for Goldenrod + Celadon prize
    rooms. G/S Goldenrod splits at runtime via checkver (labels .Gold_* /
    .Silver_*): Gold gets Ekans, Silver gets Sandshrew; Abra + Dratini are
    shared. Unlabeled vendors apply to every game of the file."""
    root = CRY if game == 'crystal' else GOLD
    games = ['gold', 'silver'] if game != 'crystal' else ['crystal']
    per_game = {g: [] for g in games}
    for fmap in ('GoldenrodGameCorner', 'CeladonGameCornerPrizeRoom'):
        src = open(f'{root}/maps/{fmap}.asm', errors='replace').read()
        prices = {}
        for m in re.finditer(r'DEF\s+([A-Z_0-9]+)_COINS\s+EQU\s+(\d+)', src):
            prices[m.group(1)] = int(m.group(2))
        stacks = {g: [] for g in games}
        cur = None                 # runtime version branch (.Gold_* / .Silver_*)
        for ctx, line in walk_versions(src.splitlines()):
            s = line.strip()
            mlab = re.match(r'\.(Gold|Silver)_\w+:', s)
            if mlab:
                cur = mlab.group(1).lower()
            elif re.match(r'\.(?!Gold_|Silver_)\w+:', s):
                cur = None         # a non-version dotted label ends the branch
            if cur is not None and cur not in stacks:
                cur = None
            tgts = [cur] if cur else ([ctx] if ctx in stacks else list(stacks.keys()))
            m1 = re.match(r'checkcoins\s+([A-Z_0-9]+)_COINS', s)
            if m1:
                for tg in tgts:
                    stacks[tg].append(m1.group(1))
                continue
            m2 = re.match(r'givepoke\s+([A-Z_0-9]+),\s*(\d+)', s)
            if m2:
                for tg in tgts:
                    if stacks[tg]:
                        key = stacks[tg].pop()
                        if key in prices and m2.group(1) in spmap:
                            per_game[tg].append({'mon': spmap[m2.group(1)],
                                                 'lvl': int(m2.group(2)),
                                                 'price': prices[key], 'map': fmap})
                continue
            if s.startswith('takecoins'):
                for tg in tgts:
                    stacks[tg] = []
    # merge identical prizes that every game of the file offers
    out = []
    for g in games:
        for p in per_game[g]:
            for e in out:
                if (e['map'], e['mon'], e['lvl'], e['price']) == (p['map'], p['mon'], p['lvl'], p['price']) \
                        and g not in e['v'] and len(e['v']) < len(games):
                    e['v'].append(g)
                    break
            else:
                out.append(dict(p, v=[g]))
    return out

# --------------------------------------------------------- location meta ----
def loc_meta():
    """(const -> [en, fa, group, region, order]) for every location the dex shows."""
    L = {}
    def add(k, en, fa, grp, reg, o):
        L[k] = [en, fa, grp, reg, o]

    # ---- Johto — cities & towns
    add('NEW_BARK_TOWN', 'New Bark Town', 'شهرک نیوبارک', 'city', 'j', 10)
    add('CHERRYGROVE_CITY', 'Cherrygrove City', 'شهر چری‌گرو', 'city', 'j', 20)
    add('VIOLET_CITY', 'Violet City', 'شهر وایولت', 'city', 'j', 30)
    add('AZALEA_TOWN', 'Azalea Town', 'شهرک آزالیا', 'city', 'j', 40)
    add('GOLDENROD_CITY', 'Goldenrod City', 'شهر گلدنراد', 'city', 'j', 50)
    add('ECRUTEAK_CITY', 'Ecruteak City', 'شهر اکروتاک', 'city', 'j', 60)
    add('OLIVINE_CITY', 'Olivine City', 'شهر الیوین', 'city', 'j', 70)
    add('CIANWOOD_CITY', 'Cianwood City', 'شهر سیان‌وود', 'city', 'j', 80)
    add('MAHOGANY_TOWN', 'Mahogany Town', 'شهرک ماهوگانی', 'city', 'j', 90)
    add('BLACKTHORN_CITY', 'Blackthorn City', 'شهر بلک‌ثورن', 'city', 'j', 100)
    add('LAKE_OF_RAGE', 'Lake of Rage', 'دریاچه‌ی خشم', 'city', 'j', 105)
    # ---- Johto — routes
    add('ROUTE_29', 'Route 29', 'مسیر ۲۹', 'route', 'j', 110)
    add('ROUTE_30', 'Route 30', 'مسیر ۳۰', 'route', 'j', 115)
    add('ROUTE_31', 'Route 31', 'مسیر ۳۱', 'route', 'j', 120)
    add('ROUTE_32', 'Route 32', 'مسیر ۳۲', 'route', 'j', 125)
    add('ROUTE_33', 'Route 33', 'مسیر ۳۳', 'route', 'j', 130)
    add('ROUTE_34', 'Route 34', 'مسیر ۳۴', 'route', 'j', 135)
    add('ROUTE_35', 'Route 35', 'مسیر ۳۵', 'route', 'j', 140)
    add('ROUTE_36', 'Route 36', 'مسیر ۳۶', 'route', 'j', 145)
    add('ROUTE_37', 'Route 37', 'مسیر ۳۷', 'route', 'j', 150)
    add('ROUTE_38', 'Route 38', 'مسیر ۳۸', 'route', 'j', 155)
    add('ROUTE_39', 'Route 39', 'مسیر ۳۹', 'route', 'j', 160)
    add('ROUTE_40', 'Route 40', 'مسیر ۴۰', 'route', 'j', 165)
    add('ROUTE_41', 'Route 41', 'مسیر ۴۱', 'route', 'j', 170)
    add('ROUTE_42', 'Route 42', 'مسیر ۴۲', 'route', 'j', 175)
    add('ROUTE_43', 'Route 43', 'مسیر ۴۳', 'route', 'j', 180)
    add('ROUTE_44', 'Route 44', 'مسیر ۴۴', 'route', 'j', 185)
    add('ROUTE_45', 'Route 45', 'مسیر ۴۵', 'route', 'j', 190)
    add('ROUTE_46', 'Route 46', 'مسیر ۴۶', 'route', 'j', 195)
    # ---- Johto — towers, ruins, buildings
    add('SPROUT_TOWER_2F', 'Sprout Tower 2F', 'برج جوانه — طبقه ۲', 'building', 'j', 200)
    add('SPROUT_TOWER_3F', 'Sprout Tower 3F', 'برج جوانه — طبقه ۳', 'building', 'j', 205)
    add('BURNED_TOWER_1F', 'Burned Tower 1F', 'برج سوخته — طبقه ۱', 'building', 'j', 210)
    add('BURNED_TOWER_B1F', 'Burned Tower B1F', 'برج سوخته — زیرزمین', 'building', 'j', 215)
    add('TIN_TOWER_1F', 'Tin Tower 1F', 'برج قلع — طبقه ۱', 'building', 'j', 218)
    for i, nm in enumerate(['2F', '3F', '4F', '5F', '6F', '7F', '8F', '9F']):
        fa_floor = {'2F': 'طبقه ۲', '3F': 'طبقه ۳', '4F': 'طبقه ۴', '5F': 'طبقه ۵',
                    '6F': 'طبقه ۶', '7F': 'طبقه ۷', '8F': 'طبقه ۸', '9F': 'طبقه ۹'}[nm]
        add(f'TIN_TOWER_{nm}', f'Tin Tower {nm}', f'برج قلع — {fa_floor}', 'building', 'j', 220 + i * 5)
    add('TIN_TOWER_ROOF', 'Tin Tower Roof', 'پشت‌بام برج قلع', 'building', 'j', 257)
    add('RUINS_OF_ALPH_OUTSIDE', 'Ruins of Alph — Outside', 'ویرانه‌های الف — بیرون', 'building', 'j', 260)
    add('RUINS_OF_ALPH_INNER_CHAMBER', 'Ruins of Alph — Inner Chamber', 'ویرانه‌های الف — تالار درونی', 'building', 'j', 265)
    add('NATIONAL_PARK', 'National Park', 'پارک ملی', 'forest', 'j', 270)
    add('TEAM_ROCKET_BASE_B1F', 'Team Rocket Base B1F', 'پایگاه تیم راکت — زیرزمین ۱', 'building', 'j', 400)
    add('TEAM_ROCKET_BASE_B2F', 'Team Rocket Base B2F', 'پایگاه تیم راکت — زیرزمین ۲', 'building', 'j', 405)
    add('DRAGON_SHRINE', 'Dragon Shrine', 'زیارتگاه اژدها', 'building', 'j', 415)
    # ---- Johto — caves & forests
    add('UNION_CAVE_1F', 'Union Cave 1F', 'غار اتحاد — طبقه ۱', 'cave', 'j', 275)
    add('UNION_CAVE_B1F', 'Union Cave B1F', 'غار اتحاد — زیرزمین ۱', 'cave', 'j', 280)
    add('UNION_CAVE_B2F', 'Union Cave B2F', 'غار اتحاد — زیرزمین ۲', 'cave', 'j', 285)
    add('SLOWPOKE_WELL_B1F', 'Slowpoke Well B1F', 'چاه اسلوپوک — زیرزمین ۱', 'cave', 'j', 290)
    add('SLOWPOKE_WELL_B2F', 'Slowpoke Well B2F', 'چاه اسلوپوک — زیرزمین ۲', 'cave', 'j', 295)
    add('ILEX_FOREST', 'Ilex Forest', 'جنگل ایلیکس', 'forest', 'j', 300)
    add('DARK_CAVE_VIOLET_ENTRANCE', 'Dark Cave — Violet Entrance', 'غار تاریک — ورودی وایولت', 'cave', 'j', 305)
    add('DARK_CAVE_BLACKTHORN_ENTRANCE', 'Dark Cave — Blackthorn Entrance', 'غار تاریک — ورودی بلک‌ثورن', 'cave', 'j', 310)
    add('MOUNT_MORTAR_1F_OUTSIDE', 'Mt. Mortar — 1F Exterior', 'کوه مورتار — بیرون طبقه ۱', 'cave', 'j', 315)
    add('MOUNT_MORTAR_1F_INSIDE', 'Mt. Mortar — 1F Interior', 'کوه مورتار — درون طبقه ۱', 'cave', 'j', 320)
    add('MOUNT_MORTAR_2F_INSIDE', 'Mt. Mortar — 2F Interior', 'کوه مورتار — درون طبقه ۲', 'cave', 'j', 325)
    add('MOUNT_MORTAR_B1F', 'Mt. Mortar B1F', 'کوه مورتار — زیرزمین', 'cave', 'j', 330)
    add('ICE_PATH_1F', 'Ice Path 1F', 'مسیر یخی — طبقه ۱', 'cave', 'j', 335)
    add('ICE_PATH_B1F', 'Ice Path B1F', 'مسیر یخی — زیرزمین ۱', 'cave', 'j', 340)
    add('ICE_PATH_B2F_MAHOGANY_SIDE', 'Ice Path B2F — Mahogany Side', 'مسیر یخی — زیرزمین ۲ (سمت ماهوگانی)', 'cave', 'j', 345)
    add('ICE_PATH_B2F_BLACKTHORN_SIDE', 'Ice Path B2F — Blackthorn Side', 'مسیر یخی — زیرزمین ۲ (سمت بلک‌ثورن)', 'cave', 'j', 350)
    add('ICE_PATH_B3F', 'Ice Path B3F', 'مسیر یخی — زیرزمین ۳', 'cave', 'j', 355)
    add('WHIRL_ISLAND_NW', 'Whirl Islands NW', 'جزایر گردباد — شمال‌غرب', 'cave', 'j', 360)
    add('WHIRL_ISLAND_NE', 'Whirl Islands NE', 'جزایر گردباد — شمال‌شرق', 'cave', 'j', 365)
    add('WHIRL_ISLAND_SW', 'Whirl Islands SW', 'جزایر گردباد — جنوب‌غرب', 'cave', 'j', 370)
    add('WHIRL_ISLAND_SE', 'Whirl Islands SE', 'جزایر گردباد — جنوب‌شرق', 'cave', 'j', 375)
    add('WHIRL_ISLAND_CAVE', 'Whirl Islands — Inner Cave', 'جزایر گردباد — غار درونی', 'cave', 'j', 380)
    add('WHIRL_ISLAND_B1F', 'Whirl Islands B1F', 'جزایر گردباد — زیرزمین ۱', 'cave', 'j', 385)
    add('WHIRL_ISLAND_B2F', 'Whirl Islands B2F', 'جزایر گردباد — زیرزمین ۲', 'cave', 'j', 390)
    add('WHIRL_ISLAND_LUGIA_CHAMBER', 'Whirl Islands — Lugia Chamber', 'جزایر گردباد — لانه‌ی لوگیا', 'cave', 'j', 395)
    add('DRAGONS_DEN_B1F', "Dragon's Den B1F", 'لانه‌ی اژدها — زیرزمین', 'cave', 'j', 410)
    add('SILVER_CAVE_OUTSIDE', 'Silver Cave — Outside', 'غار نقره — بیرون', 'forest', 'j', 420)
    add('SILVER_CAVE_ROOM_1', 'Silver Cave — Room 1', 'غار نقره — تالار ۱', 'cave', 'j', 425)
    add('SILVER_CAVE_ROOM_2', 'Silver Cave — Room 2', 'غار نقره — تالار ۲', 'cave', 'j', 430)
    add('SILVER_CAVE_ROOM_3', 'Silver Cave — Room 3', 'غار نقره — تالار ۳', 'cave', 'j', 435)
    add('SILVER_CAVE_ITEM_ROOMS', 'Silver Cave — Item Rooms', 'غار نقره — اتاق‌های اشیا', 'cave', 'j', 440)
    # ---- Kanto
    add('PALLET_TOWN', 'Pallet Town', 'شهرک پالت', 'city', 'k', 500)
    add('ROUTE_1', 'Route 1', 'مسیر ۱', 'route', 'k', 505)
    add('ROUTE_2', 'Route 2', 'مسیر ۲', 'route', 'k', 510)
    add('VIRIDIAN_CITY', 'Viridian City', 'شهر ویریدین', 'city', 'k', 515)
    add('PEWTER_CITY', 'Pewter City', 'شهر پیوتر', 'city', 'k', 517)
    add('ROUTE_3', 'Route 3', 'مسیر ۳', 'route', 'k', 520)
    add('ROUTE_4', 'Route 4', 'مسیر ۴', 'route', 'k', 525)
    add('MOUNT_MOON', 'Mt. Moon', 'کوه ماه', 'cave', 'k', 530)
    add('ROUTE_5', 'Route 5', 'مسیر ۵', 'route', 'k', 535)
    add('ROUTE_6', 'Route 6', 'مسیر ۶', 'route', 'k', 540)
    add('VERMILION_CITY', 'Vermilion City', 'شهر ورمیلیون', 'city', 'k', 545)
    add('DIGLETTS_CAVE', "Diglett's Cave", 'غار دیگلت', 'cave', 'k', 550)
    add('ROUTE_7', 'Route 7', 'مسیر ۷', 'route', 'k', 555)
    add('ROUTE_8', 'Route 8', 'مسیر ۸', 'route', 'k', 560)
    add('ROCK_TUNNEL_1F', 'Rock Tunnel 1F', 'تونل سنگی — طبقه ۱', 'cave', 'k', 565)
    add('ROCK_TUNNEL_B1F', 'Rock Tunnel B1F', 'تونل سنگی — زیرزمین', 'cave', 'k', 570)
    add('ROUTE_9', 'Route 9', 'مسیر ۹', 'route', 'k', 575)
    add('ROUTE_10_NORTH', 'Route 10 (North)', 'مسیر ۱۰ (شمال)', 'route', 'k', 580)
    add('POWER_PLANT', 'Power Plant', 'نیروگاه', 'building', 'k', 582)
    add('ROUTE_11', 'Route 11', 'مسیر ۱۱', 'route', 'k', 585)
    add('ROUTE_12', 'Route 12', 'مسیر ۱۲', 'route', 'k', 590)
    add('ROUTE_13', 'Route 13', 'مسیر ۱۳', 'route', 'k', 595)
    add('ROUTE_14', 'Route 14', 'مسیر ۱۴', 'route', 'k', 600)
    add('ROUTE_15', 'Route 15', 'مسیر ۱۵', 'route', 'k', 605)
    add('ROUTE_16', 'Route 16', 'مسیر ۱۶', 'route', 'k', 610)
    add('ROUTE_17', 'Route 17', 'مسیر ۱۷', 'route', 'k', 615)
    add('ROUTE_18', 'Route 18', 'مسیر ۱۸', 'route', 'k', 620)
    add('FUCHSIA_CITY', 'Fuchsia City', 'شهر فوشیا', 'city', 'k', 625)
    add('ROUTE_19', 'Route 19 (sea)', 'مسیر ۱۹ (دریا)', 'route', 'k', 630)
    add('ROUTE_20', 'Route 20 (sea)', 'مسیر ۲۰ (دریا)', 'route', 'k', 632)
    add('CINNABAR_ISLAND', 'Cinnabar Island', 'جزیره سینابار', 'city', 'k', 635)
    add('ROUTE_21', 'Route 21', 'مسیر ۲۱', 'route', 'k', 640)
    add('ROUTE_22', 'Route 22', 'مسیر ۲۲', 'route', 'k', 645)
    add('ROUTE_24', 'Route 24', 'مسیر ۲۴', 'route', 'k', 650)
    add('ROUTE_25', 'Route 25', 'مسیر ۲۵', 'route', 'k', 655)
    add('CERULEAN_CITY', 'Cerulean City', 'شهر سرولین', 'city', 'k', 660)
    add('ROUTE_26', 'Route 26', 'مسیر ۲۶', 'route', 'k', 665)
    add('ROUTE_27', 'Route 27', 'مسیر ۲۷', 'route', 'k', 670)
    add('TOHJO_FALLS', 'Tohjo Falls', 'آبشار توجو', 'cave', 'k', 675)
    add('ROUTE_28', 'Route 28', 'مسیر ۲۸', 'route', 'k', 680)
    add('VICTORY_ROAD', 'Victory Road', 'جاده پیروزی', 'cave', 'k', 685)
    add('CELADON_CITY', 'Celadon City', 'شهر سلادون', 'city', 'k', 690)
    return L

# trade NPC houses -> the city shown in the dex
TRADE_MAP2LOC = {
    'GoldenrodDeptStore5F': 'GOLDENROD_CITY',
    'VioletKylesHouse': 'VIOLET_CITY',
    'OlivineTimsHouse': 'OLIVINE_CITY',
    'BlackthornEmysHouse': 'BLACKTHORN_CITY',
    'PewterPokecenter1F': 'PEWTER_CITY',
    'Route14': 'ROUTE_14',
    'PowerPlant': 'POWER_PLANT',
}
CORNER_MAP2LOC = {
    'GoldenrodGameCorner': 'GOLDENROD_CITY',
    'CeladonGameCornerPrizeRoom': 'CELADON_CITY',
}

# ------------------------------------------------------------------ main ----
def main():
    ensure_repos(False)
    spmap = build_species()
    fishgroup_index()
    meta = loc_meta()

    wild = parse_all_wild(spmap)
    fish = parse_fish(spmap)
    attrs = {g: parse_fish_attrs(g) for g in GAMES}
    trees = {g: parse_treemon_sets(g, spmap) for g in GAMES}
    tmaps = {g: parse_treemon_maps(g) for g in GAMES}
    contest = parse_contest(spmap)
    trades = {g: parse_trades(g, spmap) for g in GAMES}
    corners = {g: parse_corner(g, spmap) for g in ('gold', 'crystal')}
    # corners['gold'] already covers both G/S (runtime checkver branches)
    swarm_g = parse_swarm('crystal', spmap)
    # fishing swarms: Route 32 -> Qwilfish_Swarm (all three games),
    # Route 44 -> Remoraid_Swarm (Gold/Silver only — Crystal changed Route 44
    # to FISHGROUP_POND, killing the Remoraid swarm there)
    FISH_SWARM = {'ROUTE_32': {g: 5 for g in GAMES},
                  'ROUTE_44': {'gold': 6, 'silver': 6}}

    names = load_names()

    # ---- specials (curated, verified against the disassembly)
    sp = []
    def add_sp(kind, versions, loc, detail, mons=None, **kw):
        e = {'k': kind, 'v': list(versions), 'loc': loc, 'd': detail}
        if mons: e['m'] = mons
        e.update(kw)
        sp.append(e)
    A = GAMES
    GS = ['gold', 'silver']

    # starters — Prof. Elm's lab, New Bark Town, Lv 5
    add_sp('starter', A, 'NEW_BARK_TOWN',
        {'en': "Starter from Prof. Elm's lab — choose 1 of 3 (Lv 5)",
         'fa': 'استارتر از آزمایشگاه پروفسور اِلم — یکی از ۳ گانه (سطح ۵)'},
        [[152, 5], [155, 5], [158, 5]])
    # the Mystery Egg -> Togepi
    add_sp('egg', A, 'VIOLET_CITY',
        {'en': "The Mystery Egg from Mr. Pokémon (Route 30) — Elm's aide returns it after the Zephyr Badge; hatches a Togepi (Lv 5)",
         'fa': 'تخم مرموز آقای پوکمون (مسیر ۳۰) — بعد از نشان باد، دستیار اِلم آن را پس می‌دهد؛ توجپی از آن بیرون می‌آید (سطح ۵)'},
        [[175, 5]])
    # Crystal-only Odd Egg — the Day-Care man, Route 34
    add_sp('egg', ['crystal'], 'GOLDENROD_CITY',
        {'en': 'The Odd Egg from the Day-Care man (Route 34) — Crystal only; hatches one of Pichu / Cleffa / Igglybuff / Smoochum / Tyrogue / Magby / Elekid with a much higher shiny chance',
         'fa': 'تخم عجیب از مرد پرورش‌دهنده (مسیر ۳۴) — فقط کریستال؛ یکی از پیچو / کلفا / ایگلی‌باف / اسموچام / تایروگ / مگبی / الکیید از آن بیرون می‌آید، با شانس بسیار بیشترِ شاینشدن'},
        [[172, 5], [173, 5], [174, 5], [238, 5], [236, 5], [240, 5], [239, 5]])
    # gifts
    add_sp('gift', A, 'CIANWOOD_CITY',
        {'en': "Shuckle from the Cianwood maniac's house (Lv 15, holds a Berry) — look after it and give it back",
         'fa': 'شاکل از خانه‌ی دیوانه‌ی شهر سیان‌وود (سطح ۱۵، یک سیرپ هم دارد) — نگه‌اش دارید و پس بدهید'},
        [[213, 15]])
    add_sp('gift', A, 'MOUNT_MORTAR_B1F',
        {'en': 'Tyrogue from Black Belt Kiyo in Mt. Mortar B1F (Lv 10) — beat him first',
         'fa': 'تایروگ از کمربند سیاه کِیو در کوه مورتار، زیرزمین (سطح ۱۰) — اول او را شکست دهید'},
        [[236, 10]])
    add_sp('gift', A, 'GOLDENROD_CITY',
        {'en': "Eevee from Bill in his family's house in Goldenrod City (Lv 20)",
         'fa': 'ایوی از بیل در خانه‌ی خانوادگی‌اش در شهر گلدنراد (سطح ۲۰)'},
        [[133, 20]])
    # statics
    add_sp('static', A, 'ROUTE_36',
        {'en': 'The weird tree on Route 36 is actually a Sudowoodo (Lv 20) — water it with the SquirtBottle to battle it',
         'fa': 'درخت عجیب مسیر ۳۶ در واقع یک سودووودو است (سطح ۲۰) — با بطری اسکویتل به آن آب بدهید تا وارد نبرد شوید'},
        [[185, 20]])
    add_sp('static', A, 'LAKE_OF_RAGE',
        {'en': 'The Red Gyarados — the famous forced-shiny encounter (Lv 30)',
         'fa': 'گیارادوس سرخ — مواجهه‌ی مشهورِ همیشه‌شاین (سطح ۳۰)'},
        [[130, 30]])
    add_sp('static', A, 'VERMILION_CITY',
        {'en': 'Snorlax blocking Route 11 — wake it with the Poké Flute radio channel (Lv 50, holds Leftovers)',
         'fa': 'اسنورلکسی جلوی مسیر ۱۱ خوابیده — با کانال رادیوییِ فلوت پوک بیدارش کنید (سطح ۵۰، آوار ماندگی دارد)'},
        [[143, 50]])
    add_sp('static', A, 'UNION_CAVE_B2F',
        {'en': 'Lapras appears at Union Cave B2F on Fridays only (Lv 20)',
         'fa': 'لاپراس فقط روزهای جمعه در غار اتحاد، زیرزمین ۲ ظاهر می‌شود (سطح ۲۰)'},
        [[131, 20]], note='friday')
    add_sp('static', A, 'TEAM_ROCKET_BASE_B2F',
        {'en': 'Three Electrode guarding the Rocket radio signal — fixed Lv 23 battles (you may catch one)',
         'fa': 'سه الکترود نگهبانِ فرستنده‌ی رادیویی راکت — نبردهای ثابت سطح ۲۳ (می‌توانید یکی را بگیرید)'},
        [[101, 23]])
    # roaming beasts
    add_sp('roamer', GS, 'BURNED_TOWER_B1F',
        {'en': 'Raikou roams Johto after you release the three beasts at the Burned Tower (Lv 40) — it flees each turn',
         'fa': 'رایکو بعد از آزاد کردن سه هیولای برج سوخته در جوتو سرگردان می‌شود (سطح ۴۰) — هر نوبت فرار می‌کند'},
        [[243, 40]], note='roam')
    add_sp('roamer', GS, 'BURNED_TOWER_B1F',
        {'en': 'Entei roams Johto after you release the three beasts at the Burned Tower (Lv 40) — it flees each turn',
         'fa': 'انتی بعد از آزاد کردن سه هیولای برج سوخته در جوتو سرگردان می‌شود (سطح ۴۰) — هر نوبت فرار می‌کند'},
        [[244, 40]], note='roam')
    add_sp('roamer', GS, 'BURNED_TOWER_B1F',
        {'en': 'Suicune roams Johto too in Gold & Silver (Lv 40) — it flees each turn',
         'fa': 'سوایکون در طلایی و نقره‌ای هم سرگردان است (سطح ۴۰) — هر نوبت فرار می‌کند'},
        [[245, 40]], note='roam')
    add_sp('roamer', ['crystal'], 'BURNED_TOWER_B1F',
        {'en': 'Raikou roams Johto after the Burned Tower (Lv 40) — it flees each turn',
         'fa': 'رایکو بعد از برج سوخته در جوتو سرگردان می‌شود (سطح ۴۰) — هر نوبت فرار می‌کند'},
        [[243, 40]], note='roam')
    add_sp('roamer', ['crystal'], 'BURNED_TOWER_B1F',
        {'en': 'Entei roams Johto after the Burned Tower (Lv 40) — it flees each turn',
         'fa': 'انتی بعد از برج سوخته در جوتو سرگردان می‌شود (سطح ۴۰) — هر نوبت فرار می‌کند'},
        [[244, 40]], note='roam')
    add_sp('static', ['crystal'], 'TIN_TOWER_1F',
        {'en': 'Crystal: Suicune waits on Tin Tower 1F after the story (Lv 40) — in G/S it roams instead',
         'fa': 'کریستال: سوایکون بعد از داستان در طبقه‌ی ۱ برج قلع منتظر است (سطح ۴۰) — در طلایی/نقره‌ای سرگردان است'},
        [[245, 40]])
    # version legendaries
    add_sp('static', ['gold'], 'WHIRL_ISLAND_LUGIA_CHAMBER',
        {'en': 'Lugia waits in the Whirl Islands (Lv 70 in Gold) — needs the Silver Wing',
         'fa': 'لوگیا در جزایر گردباد منتظر است (در طلایی سطح ۷۰) — بال نقره‌ای لازم است'},
        [[249, 70]])
    add_sp('static', ['silver'], 'WHIRL_ISLAND_LUGIA_CHAMBER',
        {'en': 'Lugia waits in the Whirl Islands (Lv 40 in Silver) — needs the Silver Wing',
         'fa': 'لوگیا در جزایر گردباد منتظر است (در نقره‌ای سطح ۴۰) — بال نقره‌ای لازم است'},
        [[249, 40]])
    add_sp('static', ['crystal'], 'WHIRL_ISLAND_LUGIA_CHAMBER',
        {'en': 'Lugia waits in the Whirl Islands (Lv 60 in Crystal) — needs the Silver Wing and the Tidal Bell',
         'fa': 'لوگیا در جزایر گردباد منتظر است (در کریستال سطح ۶۰) — بال نقره‌ای و زنگ جزر و مد لازم است'},
        [[249, 60]])
    add_sp('static', ['gold'], 'TIN_TOWER_ROOF',
        {'en': 'Ho-Oh waits on the Tin Tower roof (Lv 40 in Gold) — needs the Rainbow Wing',
         'fa': 'هو-اوه روی پشت‌بام برج قلع منتظر است (در طلایی سطح ۴۰) — بال رنگین‌کمان لازم است'},
        [[250, 40]])
    add_sp('static', ['silver'], 'TIN_TOWER_ROOF',
        {'en': 'Ho-Oh waits on the Tin Tower roof (Lv 70 in Silver) — needs the Rainbow Wing',
         'fa': 'هو-اوه روی پشت‌بام برج قلع منتظر است (در نقره‌ای سطح ۷۰) — بال رنگین‌کمان لازم است'},
        [[250, 70]])
    add_sp('static', ['crystal'], 'TIN_TOWER_ROOF',
        {'en': 'Ho-Oh waits on the Tin Tower roof (Lv 60 in Crystal) — needs the Rainbow Wing',
         'fa': 'هو-اوه روی پشت‌بام برج قلع منتظر است (در کریستال سطح ۶۰) — بال رنگین‌کمان لازم است'},
        [[250, 60]])
    # event-only
    add_sp('event', A, 'ILEX_FOREST',
        {'en': 'Celebi — the Ilex Forest shrine event only (Japanese mobile events; Crystal: the GS Ball quest)',
         'fa': 'سلبی — فقط ایونت زیارتگاه جنگل ایلیکس (ایونت‌های موبایل ژاپنی؛ کریستال: ماجرای گوی GS)'},
        [[251, 30]])
    # Crystal's Dragon Shrine quiz
    add_sp('gift', ['crystal'], 'DRAGON_SHRINE',
        {'en': "Dratini from the Dragon Shrine quiz in the Dragon's Den (Lv 15) — answer all questions right",
         'fa': 'درینی از پرسش‌های زیارتگاه اژدها در لانه‌ی اژدها (سطح ۱۵) — به همه‌ی پرسش‌ها درست جواب دهید'},
        [[147, 15]])
    # in-game trades
    PLACES = {
        'GoldenrodDeptStore5F': ('GOLDENROD_CITY', 'Goldenrod Dept. Store 5F', 'فروشگاه بزرگ گلدنراد — طبقه ۵'),
        'VioletKylesHouse': ('VIOLET_CITY', "Violet City (Kyle's house)", 'شهر وایولت (خانه‌ی کایل)'),
        'OlivineTimsHouse': ('OLIVINE_CITY', "Olivine City (Tim's house)", 'شهر الیوین (خانه‌ی تیم)'),
        'BlackthornEmysHouse': ('BLACKTHORN_CITY', "Blackthorn City (Emy's house)", 'شهر بلک‌ثورن (خانه‌ی امی)'),
        'PewterPokecenter1F': ('PEWTER_CITY', 'Pewter Pokémon Center', 'مرکز پوکمون پیوتر'),
        'Route14': ('ROUTE_14', 'Route 14', 'مسیر ۱۴'),
        'PowerPlant': ('POWER_PLANT', 'Power Plant', 'نیروگاه'),
    }
    for game in ('gold', 'crystal'):   # gold's npc_trades covers both G/S
        vers = [game] if game == 'crystal' else GS
        for tr in trades[game]:
            loc, en_pl, fa_pl = PLACES[tr['map']]
            give, get = names['en'][tr['give']], names['en'][tr['get']]
            give_f, get_f = names['fa'][tr['give']], names['fa'][tr['get']]
            add_sp('trade', vers, loc,
                {'en': f'In-game trade at {en_pl} — give {give}, receive {get} (nicknamed {tr["nick"]})',
                 'fa': f'تبادل داخل بازی در {fa_pl} — {give_f} بدهید و {get_f} بگیرید (با لقب {tr["nick"]})'},
                [[tr['get'], None]], give=tr['give'])
    # game-corner prizes
    for p in corners['gold'] + corners['crystal']:
            loc = CORNER_MAP2LOC[p['map']]
            where = 'Goldenrod Game Corner' if p['map'].startswith('Goldenrod') else 'Celadon Game Corner'
            where_f = 'گیم‌کرنر گلدنراد' if p['map'].startswith('Goldenrod') else 'گیم‌کرنر سلادون'
            add_sp('corner', p['v'], loc,
                {'en': f'{where} prize — {p["price"]} coins (Lv {p["lvl"]})',
                 'fa': f'جایزه‌ی {where_f} — {p["price"]} سکه (سطح {p["lvl"]})'},
                [[p['mon'], p['lvl']]], price=p['price'])

    # ---- assemble locations
    used_locs = {s.get('loc') for s in sp if s.get('loc')}
    locs = []
    for const, (en, fa, grp, reg, o) in meta.items():
        per = {}
        for g in GAMES:
            tb = wild.get(g, {}).get(const)
            if tb is None:
                continue
            gi = attrs[g].get(const, 0)
            if gi:
                tb['f'] = gi
            if const in FISH_SWARM and g in FISH_SWARM[const]:
                tb['swf'] = FISH_SWARM[const][g]
            if g == 'crystal' and const in swarm_g:
                tb['swg'] = swarm_g[const]
            # the Bug-Catching Contest replaces National Park's grass
            if const == 'NATIONAL_PARK':
                tb['ct'] = 1
            sname = tmaps[g].get(const)
            if sname:
                if sname == 'Rock':
                    tb['rk'] = sname
                else:
                    tb['hb'] = sname
            per[g] = tb
        # dedupe: a game's table is omitted when it equals the table it would
        # fall back to (silver->gold, crystal->silver-or-gold); explicit null =
        # the game really has no wild data there
        row = {'id': const, 'en': en, 'fa': fa, 'g': grp, 'r': reg, 'o': o}
        emitted = {}
        g = per.get('gold')
        s = per.get('silver')
        c = per.get('crystal')
        if g:
            emitted['g'] = g
        if s is not None and s != g:
            emitted['s'] = s
        elif s is None and g:
            emitted['s'] = None
        s_eff = s if s else g
        if c is not None and c != s_eff:
            emitted['c'] = c
        elif c is None and g:
            emitted['c'] = None
        if emitted:
            row['t'] = emitted
        if emitted or const in used_locs:   # specials-only locations stay too
            locs.append(row)
    locs.sort(key=lambda r: r['o'])
    for s in sp:
        if s.get('loc') and s['loc'] not in {r['id'] for r in locs}:
            sys.exit(f'!! special location missing from meta: {s["loc"]}')

    data = {
        'games': GAMES,
        'grassPct': GRASS_PCT,
        'waterSpread': 4,
        'fish': fish,
        'trees': {name: {g: trees[g][name] for g in GAMES if name in trees[g]}
                  for name in trees['gold']},
        'treeMaps': {g: tmaps[g] for g in GAMES},
        'contest': contest,
        'locs': locs,
        'sp': sp,
    }

    # ---- asserts (authenticity spot checks)
    r29 = next(r for r in locs if r['id'] == 'ROUTE_29')
    assert [161, 3] in r29['t']['g']['m']['s'], r29['t']['g']['m']
    wild_mons = [e[0] for r in locs if r.get('t') for gg in r['t'].values() if gg
                 for t in ('m', 'd', 'n') if gg.get(t) for e in gg[t]['s']]
    assert 152 not in wild_mons and 155 not in wild_mons and 158 not in wild_mons
    gy = next(s for s in sp if s['m'] and s['m'][0][0] == 130)
    assert gy['m'][0][1] == 30 and gy['loc'] == 'LAKE_OF_RAGE'
    ho = {(s['v'][0], s['m'][0][1]) for s in sp if s['m'] and s['m'][0][0] == 250}
    assert ho == {('gold', 40), ('silver', 70), ('crystal', 60)}, ho
    lu = {(s['v'][0], s['m'][0][1]) for s in sp if s['m'] and s['m'][0][0] == 249}
    assert lu == {('gold', 70), ('silver', 40), ('crystal', 60)}, lu
    odd = [s for s in sp if s['k'] == 'egg' and s['v'] == ['crystal']]
    assert odd and len(odd[0]['m']) == 7
    trades_g = [s for s in sp if s['k'] == 'trade' and s['v'] == GS]
    trades_c = [s for s in sp if s['k'] == 'trade' and s['v'] == ['crystal']]
    assert len(trades_g) == 6 and len(trades_c) == 7, (len(trades_g), len(trades_c))
    def corner_mons(game):
        return {s['m'][0][0] for s in sp if s['k'] == 'corner' and game in s['v']}
    assert corner_mons('gold') == {63, 23, 147, 122, 133, 137}, corner_mons('gold')
    assert corner_mons('silver') == {63, 27, 147, 122, 133, 137}, corner_mons('silver')
    assert corner_mons('crystal') == {63, 104, 202, 25, 137, 246}, corner_mons('crystal')
    assert swarm_g and next(r for r in locs if r['id'] == 'ROUTE_35')['t']['c'].get('swg')
    assert next(r for r in locs if r['id'] == 'ROUTE_32')['t']['g'].get('swf') == 5
    assert 'swf' not in next(r for r in locs if r['id'] == 'ROUTE_44')['t'].get('c', {})
    for r in locs:
        assert r['en'] and r['fa'] and r['g'] in ('route', 'city', 'cave', 'forest', 'building')
    for s in sp:
        assert s['d'].get('fa') and s['d'].get('en'), s

    # ---- emit
    out = f'{REPO}/assets/js/locations-gen2.js'
    with open(out, 'w') as f:
        f.write('"use strict";\n')
        f.write('/* Pokédex Plus — GENERATION II location & encounter data (gen2.html).\n')
        f.write('   Generated by tools/build-locations-gen2.py from the pret decompiles\n')
        f.write('   (pokegold = Gold/Silver via version-IFs, pokecrystal = Crystal)\n')
        f.write('   — do not edit by hand.\n')
        f.write('   locs[].t: per-game tables. Grass m/d/n = morning/day/night\n')
        f.write('   {r: rate/255, s: 7 slots}; slot chances = grassPct (30/30/20/10/5/4/1).\n')
        f.write('   Surf wr/w: rate + 3 slots — the engine adds 0..+4 to each level\n')
        f.write('   (waterSpread). f = fish-group index (LOC2.fish: bite %, old/good/super\n')
        f.write('   rod tables with slot %; 5-length rows = [day id, day lvl, nite id,\n')
        f.write('   nite lvl, %] — TimeFishGroups entries). hb/rk = tree set name for\n')
        f.write('   headbutt / rock smash (LOC2.trees[set][game].c/.r with % weights).\n')
        f.write('   Omitted silver/crystal tables fall back to gold; explicit null = the\n')
        f.write('   game really has no wilds there. swg = swarm grass replacement (m/d/n),\n')
        f.write('   swf = swarm fish-group index. ct = Bug-Catching Contest rows\n')
        f.write('   [id, min, max, %]. sp: special ways to obtain (starters, eggs, gifts,\n')
        f.write('   trades, corners, statics, roamers, event) with EN/FA details. */\n')
        f.write('const LOC2 = ')
        f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
        f.write(';\n')
    n_wild = sum(1 for r in locs if r.get('t'))
    print(f'  wrote {out} ({os.path.getsize(out)//1024} KB, {len(locs)} locations, '
          f'{n_wild} with wilds, {len(sp)} special entries)')

# names for trade/corner detail strings — parsed from the app's own gen2-data.js
def load_names():
    src = open(f'{REPO}/assets/js/gen2-data.js').read()
    i = src.find('const DATA = [')
    j = src.find('];', i)
    arr = json.loads(src[i + len('const DATA = '):j + 1])
    return {'en': {p['id']: p['display'] for p in arr},
            'fa': {p['id']: p.get('fa') or p['display'] for p in arr}}

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--refetch', action='store_true')
    args = ap.parse_args()
    ensure_repos(args.refetch)
    main()
