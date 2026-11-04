#!/usr/bin/env python3
"""Pokédex Plus — Phase 4: the LOCATION DEX data for Generation I.

Sources of truth (fetched into tools/loc-cache/, refresh with --refetch):
  pret/pokered     wild grass/water tables (Red & Blue halves of the
                   IF DEF(_RED)/IF DEF(_BLUE) blocks), Super-Rod fishing
                   groups, in-game trades, Game Corner prizes      (R/B)
  pret/pokeyellow  the same for Yellow (its own tables, per-route
                   Super-Rod slots with 40/30/20/10 chances)        (Y)

Historical accuracy (per project philosophy):
  · GREEN (Japan) — Bulbapedia: "Listed under the Green header is Japanese
    Green and international Blue, which have the same Pokémon distribution
    as each other." The international Red/Blue ROMs kept the Japanese
    Red/Green wild tables (every Japanese-Blue change — wild Jynx/Lickitung,
    Kangaskhan/Tauros as trades-only, Raticate/Clefairy/Rapidash in Cerulean
    Cave, Ditto in Rock Tunnel — is absent from pokered), so the dex shows
    Green with the Blue tables and says so in the UI.
  · slot chances are the authentic WildMonEncounterSlotChances shared by
    every Gen-1 game: 51,51,39,25,25,25,13,13,11,3 of 256.
  · Old Rod = Magikarp L5 everywhere; Good Rod = a global 50/50 of
    GOLDEEN L10 / POLIWAG L10 (⅓ bite chance per use).
  · Super Rod: R/B use shared per-map fishing groups (uniform pick); Yellow
    has its own per-route 4-slot tables with 40/30/20/10 % chances.
  · static encounters, gifts, starters, fossils and trade levels are read
    from the map object / script data (Mewtwo L70, Zapdos L50, Snorlax
    L30 ×2, Hitmons L30, Eevee L25, Lapras L15, fossils revive at L30,
    starters L5, the ¥500 Magikarp salesman at the Mt. Moon Poké Center).
  · in-game trades return the received Pokémon at the level of the one
    given (engine/events/in_game_trades.asm), with their in-game nicknames.

Outputs:
  assets/js/locations-gen1.js   LOC1 — every location of Kanto with its
                                encounter tables for all four games
                                (bilingual EN/FA names) + the special
                                ways to obtain Pokémon (starters, gifts,
                                trades, Game Corner, fossils, statics).

Usage:
  python3 tools/build-locations.py             # parse + emit (cache kept)
  python3 tools/build-locations.py --refetch   # re-download pret sources
"""
import argparse
import glob
import json
import os
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CACHE = f'{REPO}/tools/loc-cache'
RAW = 'https://raw.githubusercontent.com'
ORG = {'pokered': 'pret/pokered', 'pokeyellow': 'pret/pokeyellow'}
SLOT_PCT = [51/256*100, 51/256*100, 39/256*100, 25/256*100, 25/256*100,
            25/256*100, 13/256*100, 13/256*100, 11/256*100, 3/256*100]

FETCH = {
  'red': [  # pret/pokered @ master
    ('pokered', 'data/wild/grass_water.asm'),
    ('pokered', 'data/wild/super_rod.asm'),
    ('pokered', 'data/wild/good_rod.asm'),
    ('pokered', 'data/events/trades.asm'),
    ('pokered', 'data/events/prizes.asm'),
    ('pokered', 'data/events/prize_mon_levels.asm'),
    ('pokered', 'constants/pokemon_constants.asm'),
    ('pokered', 'constants/pokedex_constants.asm'),
    ('pokered', 'data/pokemon/dex_order.asm'),
    ('pokered', 'data/maps/objects/PowerPlant.asm'),
    ('pokered', 'data/maps/objects/SeafoamIslandsB4F.asm'),
    ('pokered', 'data/maps/objects/VictoryRoad2F.asm'),
    ('pokered', 'data/maps/objects/CeruleanCaveB1F.asm'),
    ('pokered', 'scripts/Route12.asm'),
    ('pokered', 'scripts/Route16.asm'),
  ],
  'yellow': [
    ('pokeyellow', 'data/wild/grass_water.asm'),
    ('pokeyellow', 'data/wild/super_rod.asm'),
    ('pokeyellow', 'data/wild/good_rod.asm'),
    ('pokeyellow', 'data/events/trades.asm'),
    ('pokeyellow', 'data/events/prizes.asm'),
    ('pokeyellow', 'data/events/prize_mon_levels.asm'),
    ('pokeyellow', 'constants/pokemon_constants.asm'),
    ('pokeyellow', 'constants/pokedex_constants.asm'),
    ('pokeyellow', 'data/pokemon/dex_order.asm'),
    ('pokeyellow', 'data/maps/objects/PowerPlant.asm'),
    ('pokeyellow', 'data/maps/objects/SeafoamIslandsB4F.asm'),
    ('pokeyellow', 'data/maps/objects/VictoryRoad2F.asm'),
    ('pokeyellow', 'data/maps/objects/CeruleanCaveB1F.asm'),
    ('pokeyellow', 'scripts/Route12.asm'),
    ('pokeyellow', 'scripts/Route16.asm'),
  ],
}
WILD_DIR = {'red': 'pokered', 'yellow': 'pokeyellow'}

# ---------------------------------------------------------------- fetch ----
def fetch_all(refresh):
    os.makedirs(CACHE, exist_ok=True)

    def get(repo, path):
        dst = f'{CACHE}/{repo}__{path.replace("/", "__")}'
        if not refresh and os.path.exists(dst):
            return dst
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        url = f'{RAW}/{ORG[repo]}/master/{path}'
        try:
            urllib.request.urlretrieve(url, dst)
            return dst
        except Exception as e:
            print(f'  !! failed {url}: {e}', file=sys.stderr)
            return None

    # base files first (pointer tables live among them)
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(get, r, p) for grp in FETCH.values() for (r, p) in grp]
        base = [f.result() for f in futs]
    if any(b is None for b in base):
        sys.exit('fetch failed — check network / rate limits')
    # discover wild map files from the pointer tables
    extra = []
    for repo in ('pokered', 'pokeyellow'):
        gw = open(f'{CACHE}/{repo}__data__wild__grass_water.asm').read()
        fids = {lb[:-8] for lb in re.findall(r'dw\s+(\w+WildMons)', gw)} - {'Nothing'}
        with ThreadPoolExecutor(max_workers=8) as ex:
            futs = [ex.submit(get, repo, f'data/wild/maps/{fid}.asm') for fid in fids]
            for f in futs:
                r = f.result()
                if r:
                    extra.append(r)
    if len(extra) < 100:
        sys.exit(f'too few wild map files fetched ({len(extra)})')
    print(f'  fetched {len(base) + len(extra)} files into {CACHE}')


def cache_path(repo, path):
    return f'{CACHE}/{repo}__{path.replace("/", "__")}'

# ------------------------------------------------------- species mapping ----
def build_species(repo):
    """internal constant name -> national dex id"""
    consts = {}
    for line in open(cache_path(repo, 'constants/pokemon_constants.asm')):
        m = re.match(r'\s*const\s+([A-Z_0-9]+)\s*;\s*\$([0-9A-Fa-f]+)', line)
        if m:
            consts[m.group(1)] = int(m.group(2), 16)   # the file states the id: ; $01
    dex = {}
    for line in open(cache_path(repo, 'constants/pokedex_constants.asm')):
        m = re.match(r'\s*const\s+DEX_([A-Z_0-9]+)\s*;\s*(\d+)', line)
        if m:
            dex['DEX_' + m.group(1)] = int(m.group(2))
    internal2dex = []
    for line in open(cache_path(repo, 'data/pokemon/dex_order.asm')):
        m = re.match(r'\s*db\s+(DEX_\w+|0)\b', line)
        if m:
            internal2dex.append(dex[m.group(1)] if m.group(1) in dex else 0)
    out = {}
    for name, iid in consts.items():
        if 0 <= iid - 1 < len(internal2dex):
            out[name] = internal2dex[iid - 1]
    assert out.get('RHYDON') == 112 and out.get('BULBASAUR') == 1 and out.get('MEW') == 151 and out.get('PIDGEY') == 16 and out.get('BELLSPROUT') == 69 and out.get('TAUROS') == 128, out
    return out

# -------------------------------------------------------- location names ----
def loc_meta():
    """(id, en, fa, group, order) for every Kanto location the dex shows."""
    L = []
    def add(fid, en, fa, g, o): L.append((fid, en, fa, g, o))
    add('Route1','Route 1','مسیر ۱','route',110)
    add('Route2','Route 2','مسیر ۲','route',120)
    add('ViridianForest','Viridian Forest','جنگل ویریدین','forest',125)
    add('Route3','Route 3','مسیر ۳','route',130)
    add('MtMoon1F','Mt. Moon 1F','کوه ماه — طبقه ۱','cave',140)
    add('MtMoonB1F','Mt. Moon B1F','کوه ماه — زیرزمین ۱','cave',141)
    add('MtMoonB2F','Mt. Moon B2F','کوه ماه — زیرزمین ۲','cave',142)
    add('Route4','Route 4','مسیر ۴','route',150)
    add('Route24','Route 24','مسیر ۲۴','route',160)
    add('Route25','Route 25','مسیر ۲۵','route',165)
    add('Route5','Route 5','مسیر ۵','route',170)
    add('Route6','Route 6','مسیر ۶','route',180)
    add('Route7','Route 7','مسیر ۷','route',190)
    add('Route8','Route 8','مسیر ۸','route',200)
    add('Route9','Route 9','مسیر ۹','route',210)
    add('RockTunnel1F','Rock Tunnel 1F','تونل سنگی — طبقه ۱','cave',215)
    add('RockTunnelB1F','Rock Tunnel B1F','تونل سنگی — زیرزمین','cave',216)
    add('Route10','Route 10','مسیر ۱۰','route',220)
    add('PowerPlant','Power Plant','نیروگاه','building',225)
    add('Route11','Route 11','مسیر ۱۱','route',230)
    add('Route12','Route 12','مسیر ۱۲','route',240)
    add('Route13','Route 13','مسیر ۱۳','route',250)
    add('Route14','Route 14','مسیر ۱۴','route',255)
    add('Route15','Route 15','مسیر ۱۵','route',260)
    add('Route16','Route 16','مسیر ۱۶','route',270)
    add('Route17','Route 17','مسیر ۱۷','route',275)
    add('Route18','Route 18','مسیر ۱۸','route',280)
    add('SafariZoneCenter','Safari Zone — Center','منطقه سافاری — مرکز','forest',290)
    add('SafariZoneEast','Safari Zone — East','منطقه سافاری — شرق','forest',291)
    add('SafariZoneNorth','Safari Zone — North','منطقه سافاری — شمال','forest',292)
    add('SafariZoneWest','Safari Zone — West','منطقه سافاری — غرب','forest',293)
    add('Route19','Route 19 (sea)','مسیر ۱۹ (دریا)','route',300)
    add('Route20','Route 20 (sea)','مسیر ۲۰ (دریا)','route',305)
    add('SeafoamIslands1F','Seafoam Islands 1F','جزایر سی‌فوم — طبقه ۱','cave',310)
    add('SeafoamIslandsB1F','Seafoam Islands B1F','جزایر سی‌فوم — زیرزمین ۱','cave',311)
    add('SeafoamIslandsB2F','Seafoam Islands B2F','جزایر سی‌فوم — زیرزمین ۲','cave',312)
    add('SeafoamIslandsB3F','Seafoam Islands B3F','جزایر سی‌فوم — زیرزمین ۳','cave',313)
    add('SeafoamIslandsB4F','Seafoam Islands B4F','جزایر سی‌فوم — زیرزمین ۴','cave',314)
    add('PokemonMansion1F','Pokémon Mansion 1F','عمارت پوکمون — طبقه ۱','building',320)
    add('PokemonMansion2F','Pokémon Mansion 2F','عمارت پوکمون — طبقه ۲','building',321)
    add('PokemonMansion3F','Pokémon Mansion 3F','عمارت پوکمون — طبقه ۳','building',322)
    add('PokemonMansionB1F','Pokémon Mansion B1F','عمارت پوکمون — زیرزمین','building',323)
    add('Route21','Route 21','مسیر ۲۱','route',330)
    add('Route22','Route 22','مسیر ۲۲','route',100)
    add('Route23','Route 23','مسیر ۲۳','route',340)
    add('VictoryRoad1F','Victory Road 1F','جاده پیروزی — طبقه ۱','cave',350)
    add('VictoryRoad2F','Victory Road 2F','جاده پیروزی — طبقه ۲','cave',351)
    add('VictoryRoad3F','Victory Road 3F','جاده پیروزی — طبقه ۳','cave',352)
    add('DiglettsCave',"Diglett's Cave",'غار دیگلت','cave',360)
    add('PokemonTower1F','Pokémon Tower 1F','برج پوکمون — طبقه ۱','building',370)
    add('PokemonTower2F','Pokémon Tower 2F','برج پوکمون — طبقه ۲','building',371)
    add('PokemonTower3F','Pokémon Tower 3F','برج پوکمون — طبقه ۳','building',372)
    add('PokemonTower4F','Pokémon Tower 4F','برج پوکمون — طبقه ۴','building',373)
    add('PokemonTower5F','Pokémon Tower 5F','برج پوکمون — طبقه ۵','building',374)
    add('PokemonTower6F','Pokémon Tower 6F','برج پوکمون — طبقه ۶','building',375)
    add('PokemonTower7F','Pokémon Tower 7F','برج پوکمون — طبقه ۷','building',376)
    add('CeruleanCave1F','Cerulean Cave 1F','غار سرولین — طبقه ۱','cave',380)
    add('CeruleanCave2F','Cerulean Cave 2F','غار سرولین — طبقه ۲','cave',381)
    add('CeruleanCaveB1F','Cerulean Cave B1F','غار سرولین — زیرزمین','cave',382)
    # cities & other fishing spots
    add('PalletTown','Pallet Town','شهرک پالت','city',10)
    add('ViridianCity','Viridian City','شهر ویریدین','city',105)
    add('PewterCity','Pewter City','شهر پیوتر','city',128)
    add('CeruleanCity','Cerulean City','شهر سرولین','city',155)
    add('VermilionCity','Vermilion City','شهر ورمیلیون','city',185)
    add('LavenderTown','Lavender Town','شهرک لاوندر','city',232)
    add('CeladonCity','Celadon City','شهر سلادون','city',195)
    add('FuchsiaCity','Fuchsia City','شهر فوشیا','city',285)
    add('CinnabarIsland','Cinnabar Island','جزیره سینابار','city',315)
    add('SaffronCity','Saffron City','شهر سافرون','city',205)
    add('CeruleanGym','Cerulean Gym','جیم سرولین','building',158)
    add('VermilionDock','Vermilion Dock','اسکله ورمیلیون','building',186)
    return {m[0]: m for m in L}

# map constants that are not plain wild-map labels -> location id
CONST2LOC = {
  'PALLET_TOWN':'PalletTown','VIRIDIAN_CITY':'ViridianCity','PEWTER_CITY':'PewterCity',
  'CERULEAN_CITY':'CeruleanCity','LAVENDER_TOWN':'LavenderTown','VERMILION_CITY':'VermilionCity',
  'CELADON_CITY':'CeladonCity','FUCHSIA_CITY':'FuchsiaCity','CINNABAR_ISLAND':'CinnabarIsland',
  'INDIGO_PLATEAU':'VictoryRoad3F','SAFFRON_CITY':'SaffronCity',
  'CERULEAN_GYM':'CeruleanGym','VERMILION_DOCK':'VermilionDock',
  # pointer-table rows that carry no map-constant comment (seafoam / cave / safari …)
  'SEAFOAM_ISLANDS_1F':'SeafoamIslands1F','SEAFOAM_ISLANDS_B1F':'SeafoamIslandsB1F',
  'SEAFOAM_ISLANDS_B2F':'SeafoamIslandsB2F','SEAFOAM_ISLANDS_B3F':'SeafoamIslandsB3F',
  'SEAFOAM_ISLANDS_B4F':'SeafoamIslandsB4F','CERULEAN_CAVE_1F':'CeruleanCave1F',
  'CERULEAN_CAVE_2F':'CeruleanCave2F','CERULEAN_CAVE_B1F':'CeruleanCaveB1F',
  'SAFARI_ZONE_CENTER':'SafariZoneCenter','SAFARI_ZONE_EAST':'SafariZoneEast',
  'SAFARI_ZONE_NORTH':'SafariZoneNorth','SAFARI_ZONE_WEST':'SafariZoneWest',
  'ROCK_TUNNEL_B1F':'RockTunnelB1F','POKEMON_MANSION_2F':'PokemonMansion2F',
  'POKEMON_MANSION_3F':'PokemonMansion3F','POKEMON_MANSION_B1F':'PokemonMansionB1F',
  'VICTORY_ROAD_3F':'VictoryRoad3F','ROUTE_19':'Route19','ROUTE_20':'Route20',
}

# --------------------------------------------------------- wild map parse ----
def parse_wild_map(path, spmap, variants=('red','blue')):
    """-> {variant: {'g':[[id,lvl]x10]|None, 'gr':rate, 'w':..., 'wr':rate}}"""
    slots = {v: {'g': [], 'w': []} for v in variants}
    rate = {v: {'g': 0, 'w': 0} for v in variants}
    active = None       # 'g' or 'w'
    stack = []          # which variants the current IF block applies to
    for line in open(path):
        s = line.strip()
        m = re.match(r'def_(grass|water)_wildmons\s+(\d+)', s)
        if m:
            active = m.group(1)[0]
            for v in variants: rate[v][active] = int(m.group(2))
            continue
        if s.startswith('end_grass_wildmons') or s.startswith('end_water_wildmons'):
            active = None
            continue
        m = re.match(r'IF DEF\(_(RED|BLUE)\)', s)
        if m:
            stack.append(m.group(1).lower())
            continue
        if s.startswith('ENDC'):
            if stack: stack.pop()
            continue
        if s.startswith('ELSE'):
            if stack: stack[-1] = 'blue' if stack[-1] == 'red' else 'red'
            continue
        m = re.match(r'db\s+(\d+)\s*,\s*([A-Z_0-9]+)', s)
        if m and active:
            entry = [spmap[m.group(2)], int(m.group(1))]
            who = [stack[-1]] if stack else list(variants)
            for v in who:
                slots[v][active].append(list(entry))
    out = {}
    for v in variants:
        g = slots[v]['g'] if rate[v]['g'] else None
        w = slots[v]['w'] if rate[v]['w'] else None
        if g is not None and len(g) != 10:
            print(f'  !! {os.path.basename(path)} {v}: grass has {len(g)} slots', file=sys.stderr)
        out[v] = {'g': g, 'gr': rate[v]['g'], 'w': w, 'wr': rate[v]['w']}
    return out

# ------------------------------------------------------------ rods parse ----
def parse_super_rod_rb(path, spmap):
    """-> {const: [[id,lvl], ...]} uniform groups"""
    groups, const2group = {}, {}
    cur = None
    for line in open(path):
        s = line.strip()
        m = re.match(r'dbw\s+([A-Z_0-9]+),\s*\.(\w+)', s)
        if m:
            const2group[m.group(1)] = m.group(2)
            continue
        m = re.match(r'\.(\w+):', s)
        if m:
            cur = m.group(1)
            groups[cur] = []
            continue
        m = re.match(r'db\s+(\d+)\s*,\s*([A-Z_0-9]+)', s)
        if m and cur:
            groups[cur].append([spmap[m.group(2)], int(m.group(1))])
    return {c: groups[g] for c, g in const2group.items()}

def parse_super_rod_y(path, spmap):
    """-> {const: [[id,lvl,pct]x4]} (40/30/20/10)"""
    out = {}
    for line in open(path):
        s = line.strip()
        m = re.match(r'db\s+([A-Z_0-9]+),\s+(.+)$', s)
        if not m: continue
        vals = re.findall(r'([A-Z_0-9]+),\s*(\d+)', m.group(2))
        if len(vals) != 4: continue
        pct = [40, 30, 20, 10]
        out[m.group(1)] = [[spmap[sp], int(lv), pct[i]] for i, (sp, lv) in enumerate(vals)]
    return out

def parse_good_rod(path, spmap):
    mons = []
    for line in open(path):
        m = re.match(r'\s*db\s+(\d+)\s*,\s*([A-Z_0-9]+)', line)
        if m: mons.append([spmap[m.group(2)], int(m.group(1))])
    return mons

# ---------------------------------------------------------- trades/prizes ----
def parse_trades(path, spmap):
    out = []
    for line in open(path):
        m = re.match(r'\s*npctrade\s+([A-Z_0-9]+),\s*([A-Z_0-9]+),\s*\w+,\s*"([^"]+)"\s*;\s*(.*)', line)
        if m:
            give, get, nick, note = m.groups()
            if 'unused' in note: continue
            out.append({'give': spmap[give], 'get': spmap[get], 'nick': nick, 'src': note.strip()})
    return out

TRADE_PLACES = {
  'ROUTE_11_GATE_2F':        ('Route11', 'Route 11 (gate 2F)', 'مسیر ۱۱ (دروازه، طبقه ۲)'),
  'ROUTE_2_TRADE_HOUSE':     ('Route2', 'Route 2 (house)', 'مسیر ۲ (خانه)'),
  'CINNABAR_LAB_FOSSIL_ROOM':('CinnabarIsland', 'Cinnabar Lab (fossil room)', 'آزمایشگاه سینابار (اتاق فسیل)'),
  'VERMILION_TRADE_HOUSE':   ('VermilionCity', 'Vermilion City (house)', 'شهر ورمیلیون (خانه)'),
  'ROUTE_18_GATE_2F':        ('Route18', 'Route 18 (gate 2F)', 'مسیر ۱۸ (دروازه، طبقه ۲)'),
  'CERULEAN_TRADE_HOUSE':    ('CeruleanCity', 'Cerulean City (house)', 'شهر سرولین (خانه)'),
  'CINNABAR_LAB_TRADE_ROOM': ('CinnabarIsland', 'Cinnabar Lab (trade room)', 'آزمایشگاه سینابار (اتاق تبادل)'),
  'UNDERGROUND_PATH_ROUTE_5':('Route5', 'Underground Path (Route 5)', 'مسیر زیرزمینی (مسیر ۵)'),
}

def parse_prizes(path, levels_path, spmap):
    """Game Corner: -> {variant: [{mon, level, price}]} for the RED/BLUE halves."""
    data = {'red': [], 'blue': []}
    section, is_cost, cur_var = None, False, None
    entries, costs, lvls = {'red': [], 'blue': []}, {'red': [], 'blue': []}, {'red': {}, 'blue': {}}
    for line in open(path):
        s = line.strip()
        m = re.match(r'PrizeMenu(Mon1|Mon2|TMs)Entries:', s)
        if m: section, is_cost, cur_var = m.group(1), False, None; continue
        m = re.match(r'PrizeMenu(Mon1|Mon2|TMs)Cost:', s)
        if m: section, is_cost, cur_var = m.group(1), True, None; continue
        if s.startswith('Prize') or s.startswith('NoThanks'):
            section, cur_var = None, None; continue
        m = re.match(r'IF DEF\(_(RED|BLUE)\)', s)
        if m: cur_var = m.group(1).lower(); continue
        if s.startswith('ENDC'): cur_var = None; continue
        if not section or section == 'TMs': continue
        who = [cur_var] if cur_var else ['red', 'blue']
        m = re.match(r'db\s+([A-Z_0-9]+)', s)
        if m and not is_cost:
            if m.group(1) in spmap:
                for v in who: entries[v].append(spmap[m.group(1)])
        m = re.match(r'bcd2\s+(\d+)', s)
        if m and is_cost:
            for v in who: costs[v].append(int(m.group(1)))
    cur_var = None
    for line in open(levels_path):
        s = line.strip()
        m = re.match(r'IF DEF\(_(RED|BLUE)\)', s)
        if m: cur_var = m.group(1).lower(); continue
        if s.startswith('ENDC'): cur_var = None; continue
        m = re.match(r'db\s+([A-Z_0-9]+),\s*(\d+)', s)
        if m:
            who = [cur_var] if cur_var else ['red', 'blue']
            for v in who: lvls[v][spmap[m.group(1)]] = int(m.group(2))
    for v in ('red', 'blue'):
        for mon, cost in zip(entries[v], costs[v]):
            data[v].append({'mon': mon, 'price': cost, 'lvl': lvls[v].get(mon, 0)})
    return data

# --------------------------------------------------------------- statics ----
def parse_statics(repo, spmap):
    """object_event overworld encounters + the two Snorlax scripts."""
    out = []
    files = ['data/maps/objects/PowerPlant.asm', 'data/maps/objects/SeafoamIslandsB4F.asm',
             'data/maps/objects/VictoryRoad2F.asm', 'data/maps/objects/CeruleanCaveB1F.asm']
    for f in files:
        for line in open(cache_path(repo, f)):
            m = re.search(r'object_event\s+.*TEXT_\w+,\s*([A-Z_0-9]+),\s*(\d+)\s*$', line.strip())
            if m and not m.group(1).startswith('OPP'):
                out.append({'file': f.split('/')[-1][:-4], 'mon': spmap[m.group(1)], 'lvl': int(m.group(2))})
    for f in ('scripts/Route12.asm', 'scripts/Route16.asm'):
        src = open(cache_path(repo, f)).read()
        m = re.search(r'ld a,\s*SNORLAX\s*\n\s*ld \[wCurOpponent\], a\s*\n\s*ld a,\s*(\d+)', src)
        if m:
            out.append({'file': f.split('/')[-1][:-4], 'mon': spmap['SNORLAX'], 'lvl': int(m.group(1))})
    return out

# ------------------------------------------------------------------ main ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--refetch', action='store_true')
    args = ap.parse_args()
    os.makedirs(CACHE, exist_ok=True)
    fetch_all(args.refetch)

    spmap = build_species('pokered')
    spmap_y = build_species('pokeyellow')
    meta = loc_meta()

    # --- pointer tables: const -> label -> file
    def pointer_table(repo):
        tbl = {}
        for line in open(cache_path(repo, 'data/wild/grass_water.asm')):
            m = re.match(r'\s*dw\s+(\w+WildMons)\s*;\s*(\w+)', line)
            if m:
                tbl[m.group(2)] = m.group(1)[:-8]   # ROUTE_1 -> Route1
        return tbl
    pt_rb, pt_y = pointer_table('pokered'), pointer_table('pokeyellow')

    # --- wild tables — iterate the cached map files (their filenames are the ids)
    tables = {}          # fileid -> {'red':..., 'blue':..., 'y':...}
    for repo in ('pokered', 'pokeyellow'):
        variants = ('red', 'blue') if repo == 'pokered' else ('yellow',)
        sp = spmap if repo == 'pokered' else spmap_y
        for p in sorted(glob.glob(f'{CACHE}/{repo}__data__wild__maps__*.asm')):
            fid = os.path.basename(p).split('__maps__')[-1][:-4]
            if fid == 'nothing' or fid not in meta: continue
            parsed = parse_wild_map(p, sp, variants)
            slot = tables.setdefault(fid, {})
            if repo == 'pokered':
                slot['red'], slot['blue'] = parsed['red'], parsed['blue']
            else:
                slot['y'] = parsed['yellow']
    # R/B: Routes 19+20 share the SeaRoutes table
    sea = cache_path('pokered', 'data/wild/maps/SeaRoutes.asm')
    if os.path.exists(sea):
        parsed = parse_wild_map(sea, spmap, ('red', 'blue'))
        for fid in ('Route19', 'Route20'):
            if fid in tables:
                tables[fid]['red'], tables[fid]['blue'] = parsed['red'], parsed['blue']

    # --- rods
    sr_rb = parse_super_rod_rb(cache_path('pokered', 'data/wild/super_rod.asm'), spmap)
    sr_y = parse_super_rod_y(cache_path('pokeyellow', 'data/wild/super_rod.asm'), spmap_y)
    good = parse_good_rod(cache_path('pokered', 'data/wild/good_rod.asm'), spmap)
    good_y = parse_good_rod(cache_path('pokeyellow', 'data/wild/good_rod.asm'), spmap_y)
    assert good == good_y == [[118, 10], [60, 10]], (good, good_y)

    def attach_rod(tables, sr, pt, key):
        for const, slots in sr.items():
            fid = CONST2LOC.get(const) or pt.get(const)
            if not fid or fid == 'Nothing' or fid not in meta:
                print(f'  !! super-rod const {const} has no location', file=sys.stderr)
                continue
            t = tables.setdefault(fid, {})
            t[key] = slots

    attach_rod(tables, sr_rb, pt_rb, 'f')
    attach_rod(tables, sr_y, pt_y, 'fy')

    # --- statics (identical in both games — assert that)
    st_rb, st_y = parse_statics('pokered', spmap), parse_statics('pokeyellow', spmap_y)
    assert st_rb == st_y, 'statics differ between R/B and Yellow'

    # --- specials (curated, verified against the disassembly — see header)
    sp = []
    def add_sp(kind, versions, loc, detail, mons=None, **kw):
        e = {'k': kind, 'v': versions, 'loc': loc, 'd': detail}
        if mons: e['m'] = mons
        e.update(kw)
        sp.append(e)
    RBG = ['red', 'blue', 'green']
    ALL = ['red', 'blue', 'green', 'yellow']

    add_sp('starter', RBG, 'PalletTown',
        {'en': "Starter from Prof. Oak's lab — choose 1 of 3 (Lv 5)",
         'fa': 'استارتر از آزمایشگاه پروفسور اوک — یکی از ۳ گانه (سطح ۵)'},
        [[1, 5], [4, 5], [7, 5]])
    add_sp('starter', ['yellow'], 'PalletTown',
        {'en': 'Starter from Prof. Oak (Lv 5) — this Pikachu refuses the Thunder Stone',
         'fa': 'استارتر از پروفسور اوک (سطح ۵) — این پیکاچو سنگ رعد را نمی‌پذیرد'},
        [[25, 5]])
    add_sp('gift', ['yellow'], 'CeruleanCity',
        {'en': 'Gift from Melanie in Cerulean City (Lv 10, needs a happy Pikachu)',
         'fa': 'هدیه از ملانی در شهر سرولین (سطح ۱۰، با پیکاچوی خوشحال)'}, [[1, 10]])
    add_sp('gift', ['yellow'], 'Route24',
        {'en': 'Gift from a boy on Route 24 (Lv 10)', 'fa': 'هدیه از پسری در مسیر ۲۴ (سطح ۱۰)'}, [[4, 10]])
    add_sp('gift', ['yellow'], 'VermilionCity',
        {'en': 'Gift from Officer Jenny in Vermilion City (Lv 10, Thunder Badge)',
         'fa': 'هدیه از افسر جنی در شهر ورمیلیون (سطح ۱۰، نشان رعد)'}, [[7, 10]])
    add_sp('gift', ALL, 'CeladonCity',
        {'en': 'Gift on the top floor of the Celadon Mansion (Lv 25)',
         'fa': 'هدیه در بالاترین طبقه‌ی عمارت سلادون (سطح ۲۵)'}, [[133, 25]])
    add_sp('gift', ALL, 'SaffronCity',
        {'en': 'Gift from a Silph Co. employee, 7F (Lv 15)',
         'fa': 'هدیه از کارمند شرکت سیلف، طبقه ۷ (سطح ۱۵)'}, [[131, 15]])
    add_sp('gift', ALL, 'SaffronCity',
        {'en': 'Fighting Dojo — choose 1: Hitmonlee or Hitmonchan (Lv 30)',
         'fa': 'دوجوی مبارزه — یکی را انتخاب کنید: هیتمونلی یا هیتمونچان (سطح ۳۰)'},
        [[106, 30], [107, 30]])
    add_sp('gift', ALL, 'MtMoon1F',
        {'en': 'Sold for ¥500 by the salesman in the Mt. Moon Pokémon Center (Lv 5)',
         'fa': 'فروشنده‌ی مرکز پوکمون کوه ماه می‌فروشد — ۵۰۰ ین (سطح ۵)'}, [[129, 5]], price=500)
    add_sp('fossil', ALL, 'MtMoonB2F',
        {'en': 'Choose 1 fossil in Mt. Moon: Helix → Omanyte or Dome → Kabuto; revived at the Cinnabar Lab (Lv 30)',
         'fa': 'در کوه ماه یک فسیل انتخاب کنید: هلیکس ← اومایایت یا دام ← کابوتو؛ در آزمایشگاه سینابار زنده می‌شود (سطح ۳۰)'},
        [[138, 30], [140, 30]])
    add_sp('fossil', ALL, 'PewterCity',
        {'en': 'Old Amber from the Pewter Museum scientist → Aerodactyl at the Cinnabar Lab (Lv 30)',
         'fa': 'کهن‌کهربا از دانشمند موزه پیوتر ← ائروداکتیل در آزمایشگاه سینابار (سطح ۳۰)'}, [[142, 30]])
    # statics from the object data
    STATIC_LOC = {'PowerPlant': 'PowerPlant', 'SeafoamIslandsB4F': 'SeafoamIslandsB4F',
                  'VictoryRoad2F': 'VictoryRoad2F', 'CeruleanCaveB1F': 'CeruleanCaveB1F',
                  'Route12': 'Route12', 'Route16': 'Route16'}
    agg = {}
    for s in st_rb:
        agg.setdefault((s['file'], s['mon'], s['lvl']), 0)
        agg[(s['file'], s['mon'], s['lvl'])] += 1
    for (f, mon, lvl), n in sorted(agg.items()):
        en = f'Fixed encounter (Lv {lvl})' + (f' — ×{n}' if n > 1 else '')
        fa = f'مواجهه‌ی ثابت (سطح {lvl})' + (f' — {n} مورد' if n > 1 else '')
        add_sp('static', ALL, STATIC_LOC[f], {'en': en, 'fa': fa}, [[mon, lvl]])
    # Yellow quirk: the starter Pikachu refuses the Thunder Stone, so Raichu
    # cannot be obtained in Yellow without trading (no wild Pikachu either)
    add_sp('evoblock', ['yellow'], None,
        {'en': 'Pikachu refuses the Thunder Stone in Yellow — Raichu only via trade',
         'fa': 'در نسخه‌ی زرد پیکاچو سنگ رعد را نمی‌پذیرد — رایچو فقط با تبادل به دست می‌آید'},
        [[26, None]])
    # Mew — never a normal encounter
    add_sp('event', ALL, None,
        {'en': 'Event distribution / the famous Mew glitch only — no normal wild encounter',
         'fa': 'فقط توزیع ایونتی / گلیچ معروف میو — مواجهه‌ی وحشی عادی ندارد'}, [[151, None]])
    # in-game trades
    for which, repo, mp, vers in (('rb', 'pokered', spmap, RBG), ('y', 'pokeyellow', spmap_y, ['yellow'])):
        for tr in parse_trades(cache_path(repo, 'data/events/trades.asm'), mp):
            place = None
            for k, (loc, en, fa) in TRADE_PLACES.items():
                if k in tr['src']:
                    place = (loc, en, fa); break
            if not place:
                print(f'  !! trade place not found: {tr}', file=sys.stderr); continue
            add_sp('trade', vers, place[0],
                {'en': f'In-game trade at {place[1]} — give {NAME_EN[tr["give"]]}, receive {NAME_EN[tr["get"]]} (same level, nicknamed {tr["nick"]})',
                 'fa': f'تبادل داخل بازی در {place[2]} — {NAME_FA[tr["give"]]} بدهید و {NAME_FA[tr["get"]]} بگیرید (همان سطح، با لقب {tr["nick"]})'},
                [[tr['get'], None]], give=tr['give'])
    # Game Corner prizes
    prizes_rb = parse_prizes(cache_path('pokered', 'data/events/prizes.asm'),
                             cache_path('pokered', 'data/events/prize_mon_levels.asm'), spmap)
    prizes_y = parse_prizes(cache_path('pokeyellow', 'data/events/prizes.asm'),
                            cache_path('pokeyellow', 'data/events/prize_mon_levels.asm'), spmap_y)
    for vers, plist in ((['red'], prizes_rb['red']), (['blue', 'green'], prizes_rb['blue']), (['yellow'], prizes_y['red'])):
        if vers == ['yellow']:
            # pokeyellow prizes.asm has no IF DEF — parse returned them under 'red'
            for entry in plist:
                add_sp('corner', vers, 'CeladonCity',
                    {'en': f'Celadon Game Corner prize — {entry["price"]} coins (Lv {entry["lvl"]})',
                     'fa': f'جایزه‌ی گیم‌کرنر سلادون — {entry["price"]} سکه (سطح {entry["lvl"]})'},
                    [[entry['mon'], entry['lvl']]], price=entry['price'])
        else:
            for entry in plist:
                add_sp('corner', vers, 'CeladonCity',
                    {'en': f'Celadon Game Corner prize — {entry["price"]} coins (Lv {entry["lvl"]})',
                     'fa': f'جایزه‌ی گیم‌کرنر سلادون — {entry["price"]} سکه (سطح {entry["lvl"]})'},
                    [[entry['mon'], entry['lvl']]], price=entry['price'])

    # --- assemble location list
    locs = []
    for fid, (lid, en, fa, grp, order) in meta.items():
        t = tables.get(fid, {})
        row = {'id': lid, 'en': en, 'fa': fa, 'g': grp, 'o': order}
        games = {}
        if 'red' in t or 'blue' in t or 'f' in t:
            for v in ('red', 'blue'):
                d = t.get(v) or {}
                games[v] = {'gr': d.get('gr', 0), 'g': d.get('g'),
                            'wr': d.get('wr', 0), 'w': d.get('w'),
                            'f': t.get('f')}
        if 'y' in t or 'fy' in t:
            d = t.get('y') or {}
            games['yellow'] = {'gr': d.get('gr', 0), 'g': d.get('g'),
                               'wr': d.get('wr', 0), 'w': d.get('w'),
                               'f': t.get('fy')}
        row['t'] = games
        locs.append(row)
    locs.sort(key=lambda r: r['o'])
    # drop locations with no data at all (no wild, no rods, no specials)
    used_locs = {s.get('loc') for s in sp if s.get('loc')}
    keep = []
    for r in locs:
        has_data = any(g.get('g') or g.get('w') or g.get('f') for g in r['t'].values())
        if has_data or r['id'] in used_locs:
            keep.append(r)
    locs = keep

    data = {
        'slot': [round(x, 1) for x in SLOT_PCT],
        'old': [129, 5],
        'good': [[118, 10, 50], [60, 10, 50]],
        'locs': locs,
        'sp': sp,
    }

    # --- emit
    out = f'{REPO}/assets/js/locations-gen1.js'
    with open(out, 'w') as f:
        f.write('"use strict";\n')
        f.write('/* Pokédex Plus — GENERATION I location & encounter data (gen1.html).\n')
        f.write('   Generated by tools/build-locations.py from the pret decompiles\n')
        f.write('   (pokered = Red/Blue + Green-uses-Blue-distribution, pokeyellow = Yellow)\n')
        f.write('   — do not edit by hand.\n')
        f.write('   locs[].t: per-game tables {gr/wr: encounter rate, g: grass 10 slots,\n')
        f.write('   w: surf 10 slots, f: Super-Rod picks (uniform for R/B, pct-tagged for Y)}.\n')
        f.write('   slot: authentic WildMonEncounterSlotChances (applies to every game).\n')
        f.write('   old/good: the global Old/Good Rod tables (Magikarp L5 · Goldeen/Poliwag L10).\n')
        f.write('   sp: special ways to obtain (starters, gifts, trades, corner, fossils,\n')
        f.write('   statics, event) with EN/FA details. */\n')
        f.write('const LOC1 = ')
        f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
        f.write(';\n')
    print(f'  wrote {out} ({os.path.getsize(out)//1024} KB, {len(locs)} locations, {len(sp)} special entries)')

# names for trade detail strings — parsed from the app's own gen1-data.js
def load_names():
    srcd = open(f'{REPO}/assets/js/gen1-data.js').read()
    i = srcd.find('const DATA = [')
    j = srcd.find('];', i)
    arr = json.loads(srcd[i + len('const DATA = '):j + 1])
    en = {p['id']: p['display'].capitalize() if False else p['name'] for p in arr}
    fa = {p['id']: p.get('fa') or p['name'] for p in arr}
    return en, fa
NAME_EN, NAME_FA = load_names()
if __name__ == '__main__':
    pass

if __name__ == '__main__':
    main()
