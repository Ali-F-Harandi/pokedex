#!/usr/bin/env python3
"""Pokédex Plus — Gen-3 Phase 4: build the ITEM DEX data (Ruby/Sapphire ·
Emerald · FireRed/LeafGreen).

Sources of truth (cached under tools/items3-cache/):
  pret/pokeruby     src/data/items_en.h + src/data/item_descriptions_en.h
                    (R and S share one cartridge table — same names,
                    prices, pockets, wordings)
  pret/pokeemerald  src/data/items.h + src/data/text/item_descriptions.h
  pret/pokefirered  src/data/items.json (FR and LG share one table)
  pret/*/src/berry.c  the 43 Gen-3 berries: flavors (spicy/dry/sweet/
                    bitter/sour), firmness, size, the two-part wording
  PokeAPI/sprites   color item menu icons (sprites/items/<slug>.png)

Authenticity rules (same family as gen1/gen2 build-items.py):
  · item lists, in-game names, prices and pockets come from the pret
    decompiles — NOT from PokeAPI's modern `cost`
  · every cartridge GROUP keeps its own era-true wording (R/S · Emerald
    · FRLG); identical wordings are deduplicated
  · TMs/HMs stay in the TM/HM list of the Moves Dex; unused "????????"
    slots are dropped
  · Gen-3 games had COLOR item art everywhere — no GB/icon toggle
  · sell price is half the buy price (in-game rule)

Usage:
  python3 tools/build-items-gen3.py           # parse + fetch icons + draft
  python3 tools/build-items-gen3.py --merge   # merge FA json → items-gen3.js
"""
import glob
import json
import os
import re
import sys
import urllib.request

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CACHE = f'{REPO}/tools/items3-cache'
RAW = 'https://raw.githubusercontent.com'
SPRITES = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items'
OUT_JS = f'{REPO}/assets/js/items-gen3.js'
DRAFT = f'{REPO}/tools/items3-draft.json'
FA_FILE = f'{REPO}/tools/gen3-items-fa.json'

SOURCES = {
    'ruby-items.h': 'pret/pokeruby/master/src/data/items_en.h',
    'ruby-desc.h': 'pret/pokeruby/master/src/data/item_descriptions_en.h',
    'em-items.h': 'pret/pokeemerald/master/src/data/items.h',
    'em-desc.h': 'pret/pokeemerald/master/src/data/text/item_descriptions.h',
    'frlg-items.json': 'pret/pokefirered/master/src/data/items.json',
    'ruby-berry.c': 'pret/pokeruby/master/src/berry.c',
    'em-berry.c': 'pret/pokeemerald/master/src/berry.c',
    'frlg-berry.c': 'pret/pokefirered/master/src/berry.c',
    'ruby-const.h': 'pret/pokeruby/master/include/constants/items.h',
    'em-const.h': 'pret/pokeemerald/master/include/constants/items.h',
    'frlg-const.h': 'pret/pokefirered/master/include/constants/items.h',
}


def fetch(url, token=None, retries=3):
    last = None
    for _ in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'pokedex-tools'})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
    raise RuntimeError(f'fetch failed: {url}: {last}')


def ensure_sources(refetch=False):
    os.makedirs(CACHE, exist_ok=True)
    for name, path in SOURCES.items():
        p = f'{CACHE}/{name}'
        if refetch or not os.path.exists(p):
            open(p, 'wb').write(fetch(f'{RAW}/{path}'))
            print(f'  fetched {name}')


def read(p):
    src = open(f'{CACHE}/{p}', encoding='utf-8').read()
    if p.endswith('berry.c'):
        src = english_branch(src)
    return src


def expand(text):
    return (text.replace('{POKEBLOCK}', 'POKéBLOCK')
                .replace('#MON', 'POKéMON').replace('#', 'POKé')
                .replace('POKéé', 'POKé'))


def english_branch(src):
    """Keep only the #ifdef ENGLISH branch of the pret language switch
    (ruby-berry.c ships ENGLISH first, then #elif defined(GERMAN))."""
    a = src.find('#ifdef ENGLISH')
    b = src.find('#elif defined(GERMAN)')
    if a != -1 and b != -1:
        c = src.find('#endif', b)
        if c != -1:
            src = src[:b] + src[c + len('#endif'):]
    return src


def clean_desc(raw):
    """GBA two/three-line wording → one prose line (era wording kept)."""
    t = raw
    t = t.replace('\\l', ' ').replace('\\p', ' ').replace('\\n', ' ')
    t = re.sub(r'\s*\n\s*', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return expand(t)


# --------------------------------------------------------------- parsers
def parse_h_items(path, descmap):
    """pokeruby/pokeemerald gItems[] entries → {id: {...}}
    Both layouts use flat blocks with a .itemId field inside."""
    src = read(path)
    out = {}
    for m in re.finditer(r'\{\s*(\.[a-zA-Z][^{}]*)\}', src, re.S):
        body = m.group(1)
        idm = re.search(r'\.itemId\s*=\s*(ITEM_[A-Z0-9_]+)', body)
        if not idm:
            continue
        iid = idm.group(1)
        nm = re.search(r'\.name\s*=\s*_\(\s*"([^"]*)"', body)
        pr = re.search(r'\.price\s*=\s*(\d+)', body)
        pk = re.search(r'\.pocket\s*=\s*(POCKET_\w+)', body)
        he = re.search(r'\.holdEffect\s*=\s*(HOLD_EFFECT_\w+)', body)
        de = re.search(r'\.description\s*=\s*(\w+)', body)
        out[iid] = {
            'name': nm.group(1) if nm else None,
            'price': int(pr.group(1)) if pr else 0,
            'pocket': pk.group(1) if pk else 'POCKET_ITEMS',
            'hold': bool(he and he.group(1) != 'HOLD_EFFECT_NONE'),
            'desc': descmap.get(de.group(1), '') if de else '',
        }
    return out


def parse_h_descs(path):
    """gItemDescription_X[] / sXxxDesc[] = _("multi\nline") → {sym: text}"""
    src = read(path)
    out = {}
    for m in re.finditer(r'(gItemDescription_\w+|s\w*Desc\w*)\s*\[\]\s*=\s*_\(\s*(.*?)\)\s*;', src, re.S):
        sym, body = m.group(1), m.group(2)
        parts = re.findall(r'"((?:[^"\\]|\\.)*)"', body)
        out[sym] = clean_desc(''.join(parts))
    return out


def parse_frlg():
    d = json.loads(read('frlg-items.json'))['items']
    out = {}
    for it in d:
        iid = it.get('itemId')
        if not iid:
            continue
        out[iid] = {
            'name': it.get('english'),
            'price': int(it.get('price') or 0),
            'pocket': it.get('pocket') or 'POCKET_ITEMS',
            'hold': str(it.get('holdEffect', 'HOLD_EFFECT_NONE')) != 'HOLD_EFFECT_NONE',
            'desc': clean_desc(it.get('description_english') or ''),
        }
    return out


def parse_const_ids(path):
    """ordered item-id defines (numeric order) from a constants header"""
    ids = []
    for line in read(path).split('\n'):
        m = re.match(r'#define (ITEM_[A-Z0-9_]+)\s+(\d+)', line)
        if m:
            ids.append((int(m.group(2)), m.group(1)))
    ids.sort()
    return [i for _, i in ids]


POCKET_MAP = {
    'POCKET_POKE_BALLS': 'ball', 'POCKET_ITEMS': 'item',
    'POCKET_KEY_ITEMS': 'key', 'POCKET_BERRIES': 'berry',
    'POCKET_BERRY_POUCH': 'berry',
    'POCKET_TM_HM': 'tm', 'POCKET_NONE': 'item',
}

FIRMNESS = {
    'BERRY_FIRMNESS_VERY_SOFT': 'very_soft', 'BERRY_FIRMNESS_SOFT': 'soft',
    'BERRY_FIRMNESS_HARD': 'hard', 'BERRY_FIRMNESS_VERY_HARD': 'very_hard',
    'BERRY_FIRMNESS_SUPER_HARD': 'super_hard', 'BERRY_FIRMNESS_UNKNOWN': 'unknown',
    '1': 'very_soft', '2': 'soft', '3': 'hard', '4': 'very_hard', '5': 'super_hard',
}


def parse_berries(path):
    """gBerries[] in order → [{name-const, firmness, size, flavors, desc1, desc2}]"""
    src = read(path)
    blk = src[src.index('gBerries[]'):]
    blk = blk[:blk.index('\n};')] + '\n'
    out = []
    for m in re.finditer(r'\{(.*?)\n\s*\},?\n', blk, re.S):
        b = m.group(1)
        if '.name' not in b:
            continue
        nm = re.search(r'\.name\s*=\s*(NAME_\w+|\w+)', b)
        fi = re.search(r'\.firmness\s*=\s*(BERRY_FIRMNESS_\w+|\d+)', b)
        sz = re.search(r'\.size\s*=\s*(\d+)', b)
        d1 = re.search(r'\.description1\s*=\s*(\w+)', b)
        d2 = re.search(r'\.description2\s*=\s*(\w+)', b)
        fl = {}
        for f in ('spicy', 'dry', 'sweet', 'bitter', 'sour'):
            fm = re.search(r'\.' + f + r'\s*=\s*(\d+)', b)
            fl[f] = int(fm.group(1)) if fm else 0
        out.append({
            'name_const': nm.group(1) if nm else None,
            'firmness': FIRMNESS.get(fi.group(1)) if fi else None,
            'size': int(sz.group(1)) if sz else 0,
            'flavors': fl,
            'd1': d1.group(1) if d1 else '',
            'd2': d2.group(1) if d2 else '',
        })
    return out


def parse_h_descs_loose(path):
    """berry part1/part2 symbols — same file pattern"""
    return parse_h_descs(path)


# --------------------------------------------------------------- icon map
def slug_of(iid, slugset):
    """pret ITEM_X → PokeAPI item slug (shared by icons + berry texts)"""
    core = iid[5:]                      # strip ITEM_
    norm = core.lower().replace('_', '-')
    s = norm
    cands = [s]
    special = {
        'berry': 'oran-berry',              # the generic R/S "BERRY"
        'x-defend': 'x-defense',            # Gen-3 X DEFEND = modern x-defense
        'x-special': 'x-sp-atk',            # Gen-3 X SPECIAL raises SP.ATK
        'nevermeltice': 'never-melt-ice',
        's.s.-ticket': 'ss-ticket',
        'poke-block-case': 'pokeblock-case',
        'poke-block': 'pokeblock',
        'aurora-ticket': 'auroraticket',
        'mystic-ticket': 'mysticticket',
        'itemfinder': 'item-finder',        # may 404 → placeholder chip
    }
    if norm in special:
        cands.insert(0, special[norm])
    for c in cands:
        if c in slugset:
            return c
    return s if s in slugset else None


def fetch_frlg_berry_descs(berry_ids):
    """pokefirered ships the Japanese berry wordings only; the ENGLISH
    FRLG wording for the 43 berries comes from PokeAPI flavor texts
    (version group firered-leafgreen). Cached."""
    cachef = f'{CACHE}/pokeapi-berry-frlg.json'
    if os.path.exists(cachef):
        return json.load(open(cachef, encoding='utf-8'))
    out = {}
    for iid in berry_ids:
        slug = slug_of(iid, {iid[5:].lower().replace('_', '-')})
        slug = slug or iid[5:].lower().replace('_', '-')
        try:
            req = urllib.request.Request(f'https://pokeapi.co/api/v2/item/{slug}',
                                         headers={'User-Agent': 'pokedex-tools'})
            d = json.load(urllib.request.urlopen(req, timeout=60))
        except Exception as ex:  # noqa: BLE001
            print('  pokeapi berry miss:', slug, ex)
            continue
        best = None
        for fe in d.get('flavor_text_entries', []):
            if (fe['language']['name'] == 'en' and
                    fe['version_group']['name'] == 'firered-leafgreen'):
                best = fe.get('flavor_text') or fe.get('text')
                break
        if best:
            out[iid] = clean_desc(best)
    json.dump(out, open(cachef, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return out


def build_icon_map(all_ids, pokeapi_slugs):
    """pret ITEM_X → PokeAPI item slug"""
    slugset = set(pokeapi_slugs)
    m = {}
    misses = []
    for iid in all_ids:
        found = slug_of(iid, slugset)
        m[iid] = found
        if not found:
            misses.append(iid)
    return m, misses


def main():
    ensure_sources()
    ruby = parse_h_items('ruby-items.h', parse_h_descs('ruby-desc.h'))
    em = parse_h_items('em-items.h', parse_h_descs('em-desc.h'))
    frlg = parse_frlg()

    ruby_ids = parse_const_ids('ruby-const.h')
    em_ids = parse_const_ids('em-const.h')
    frlg_ids = parse_const_ids('frlg-const.h')

    # --- berries (43, ordered by item id in every cart) ---
    berry_ids = [i for i in ruby_ids if i.startswith('ITEM_') and i.endswith('_BERRY')
                 and 'FLUTE' not in i]
    berry_ids = [i for i in berry_ids if i in ruby]
    rs_b = parse_berries('ruby-berry.c')
    em_b = parse_berries('em-berry.c')
    fr_b = parse_berries('frlg-berry.c')
    rs_descs_b = parse_h_descs_loose('ruby-berry.c')
    em_descs_b = parse_h_descs_loose('em-berry.c')
    # FRLG EN berry wordings via PokeAPI (pret FRLG file is Japanese-only)
    frlg_berry_en = fetch_frlg_berry_descs(berry_ids)
    print(f'FRLG berry EN wordings: {len(frlg_berry_en)}/{len(berry_ids)}')
    print(f'berries: items={len(berry_ids)} rs={len(rs_b)} em={len(em_b)} frlg={len(fr_b)}')

    berry_extra = {}
    for n, iid in enumerate(berry_ids):
        e = {}
        if n < len(rs_b):
            e['rs'] = rs_b[n]
        if n < len(em_b):
            e['e'] = em_b[n]
        if n < len(fr_b):
            e['frlg'] = fr_b[n]
        berry_extra[iid] = e

    # --- merge the cartridge universe (by item-id string) ---
    all_ids = []
    for lst in (ruby_ids, em_ids, frlg_ids):
        for iid in lst:
            if iid not in all_ids:
                all_ids.append(iid)

    EXCLUDE_NAMES = {'????????', '?????', '???'}
    items = []
    dropped = []
    for iid in all_ids:
        r = ruby.get(iid)
        e = em.get(iid)
        f = frlg.get(iid)
        g = ''.join(ch for ch, x in (('r', r), ('e', e), ('s', r), ('f', f), ('l', f)) if x)
        # ruby table covers R AND S
        if r:
            g = 'rs' + ''.join(ch for ch, x in (('e', e), ('f', f), ('l', f)) if x)
        if not g:
            continue
        base = r or e or f
        nm = base['name'] if base else None
        if not nm or nm in EXCLUDE_NAMES or iid in ('ITEM_NONE',):
            dropped.append(iid)
            continue
        if iid.startswith('ITEM_TM') or iid.startswith('ITEM_HM'):
            continue                     # machines live in the TM/HM list
        rec = {'k': iid, 'en': expand(nm), 'g': g}
        # per-cart name variants
        if e and e['name'] and expand(e['name']) != rec['en']:
            rec['en_e'] = expand(e['name'])
        if f and f['name'] and expand(f['name']) != rec['en']:
            rec['en_f'] = expand(f['name'])
        # prices per group
        p = {}
        for grp, src in (('rs', r), ('e', e), ('frlg', f)):
            if src:
                p[grp] = src['price']
        rec['p'] = p
        # pockets per group (differs only where the bag changed)
        pk = {}
        for grp, src in (('rs', r), ('e', e), ('frlg', f)):
            if src:
                pk[grp] = POCKET_MAP.get(src['pocket'], 'item')
        vals = set(pk.values())
        rec['pk'] = pk.get('rs') or pk.get('e') or pk.get('frlg')
        if len(vals) > 1:
            rec['pk_v'] = {k: v for k, v in pk.items()}
        # hold
        rec['hold'] = 1 if (r and r['hold']) or (e and e['hold']) or (f and f['hold']) else 0
        # descriptions per group (deduped)
        d = {}
        for grp, src in (('rs', r), ('e', e), ('frlg', f)):
            if src and src['desc']:
                d[grp] = src['desc']
        rec['d'] = d
        if iid in berry_extra:
            be = berry_extra[iid]
            fl = {}
            for grp in ('rs', 'e', 'frlg'):
                if grp in be and be[grp].get('flavors'):
                    fl[grp] = be[grp]['flavors']
            if fl:
                vals = list(fl.values())
                # the three cartridges carry the same flavor numbers —
                # collapse to one set (verified at build time)
                if all(v == vals[0] for v in vals):
                    rec['fl'] = vals[0]
                else:
                    rec['fl'] = fl
            fz = {}
            for grp in ('rs', 'e', 'frlg'):
                if grp in be and be[grp].get('firmness'):
                    fz[grp] = be[grp]['firmness']
            if len(set(fz.values())) == 1:
                rec['firm'] = list(fz.values())[0]
            elif fz:
                rec['firm_v'] = fz
            bd = {}
            for grp, src, dmap in (('rs', r, rs_descs_b), ('e', e, em_descs_b)):
                if grp in be:
                    s1, s2 = be[grp].get('d1'), be[grp].get('d2')
                    t = clean_desc((dmap.get(s1, '') + ' ' + dmap.get(s2, '')).strip())
                    if t:
                        bd[grp] = t
            if 'frlg' in be and frlg_berry_en.get(iid):
                bd['frlg'] = frlg_berry_en[iid]
            if bd:
                rec['d'] = bd          # berries: berry-screen wording wins
        items.append(rec)

    print(f'universe: {len(items)} items (dropped unused: {len(dropped)})')
    print('dropped:', dropped)

    # --- icons ---
    import_list = None
    try:
        req = urllib.request.Request('https://pokeapi.co/api/v2/item/?limit=2000',
                                     headers={'User-Agent': 'pokedex-tools'})
        with urllib.request.urlopen(req, timeout=60) as r:
            import_list = json.load(r)['results']
    except Exception as e:  # noqa: BLE001
        print('PokeAPI list fetch failed:', e)
    slugs = [x['name'] for x in import_list] if import_list else None
    icmap = {}
    misses = []
    if slugs:
        icmap, misses = build_icon_map([i['k'] for i in items], slugs)
        print('icon misses:', misses)
    else:
        icmap = {i['k']: None for i in items}

    # download missing color icons
    have = set(os.listdir(f'{REPO}/assets/itemicons'))
    need = sorted({sl for sl in icmap.values() if sl and sl + '.png' not in have})
    print(f'icons to download: {len(need)}')
    for sl in need:
        try:
            data = fetch(f'{SPRITES}/{sl}.png')
            open(f'{REPO}/assets/itemicons/{sl}.png', 'wb').write(data)
        except Exception as e:  # noqa: BLE001
            print('  icon fetch failed:', sl, e)
            icmap = {k: (None if v == sl else v) for k, v in icmap.items()}
    for i in items:
        i['i'] = icmap.get(i['k'])

    # --- categories ---
    HEAL = {'ITEM_POTION', 'ITEM_ANTIDOTE', 'ITEM_BURN_HEAL', 'ITEM_ICE_HEAL',
            'ITEM_AWAKENING', 'ITEM_PARALYZE_HEAL', 'ITEM_FULL_RESTORE',
            'ITEM_MAX_POTION', 'ITEM_HYPER_POTION', 'ITEM_SUPER_POTION',
            'ITEM_FULL_HEAL', 'ITEM_REVIVE', 'ITEM_MAX_REVIVE',
            'ITEM_FRESH_WATER', 'ITEM_SODA_POP', 'ITEM_LEMONADE',
            'ITEM_MOOMOO_MILK', 'ITEM_BERRY_JUICE', 'ITEM_SACRED_ASH',
            'ITEM_ENERGY_POWDER', 'ITEM_ENERGY_ROOT', 'ITEM_HEAL_POWDER',
            'ITEM_REVIVAL_HERB'}
    TREASURE = {'ITEM_NUGGET', 'ITEM_PEARL', 'ITEM_BIG_PEARL', 'ITEM_STARDUST',
                'ITEM_STAR_PIECE', 'ITEM_TINY_MUSHROOM', 'ITEM_BIG_MUSHROOM',
                'ITEM_HEART_SCALE', 'ITEM_SHOAL_SALT', 'ITEM_SHOAL_SHELL',
                'ITEM_SILVER_LEAF', 'ITEM_GOLD_LEAF', 'ITEM_SLOWPOKE_TAIL',
                'ITEM_RED_SHARD', 'ITEM_BLUE_SHARD', 'ITEM_YELLOW_SHARD',
                'ITEM_GREEN_SHARD', 'ITEM_ASH'}

    def categorize(rec):
        iid, pk = rec['k'], rec['pk']
        if pk == 'ball':
            return 'ball'
        if iid.endswith('_BERRY'):
            return 'berry'
        if pk == 'key':
            return 'key'
        if '_MAIL' in iid:
            return 'mail'
        if iid in ('ITEM_OLD_ROD', 'ITEM_GOOD_ROD', 'ITEM_SUPER_ROD'):
            return 'rod'
        if iid in ('ITEM_FIRE_STONE', 'ITEM_WATER_STONE', 'ITEM_THUNDER_STONE',
                   'ITEM_LEAF_STONE', 'ITEM_MOON_STONE', 'ITEM_SUN_STONE'):
            return 'stone'
        if iid in ('ITEM_HP_UP', 'ITEM_PROTEIN', 'ITEM_IRON', 'ITEM_CARBOS',
                   'ITEM_CALCIUM', 'ITEM_ZINC', 'ITEM_RARE_CANDY',
                   'ITEM_PP_UP', 'ITEM_PP_MAX'):
            return 'vitamin'
        if iid in ('ITEM_X_ATTACK', 'ITEM_X_DEFEND', 'ITEM_X_SPEED',
                   'ITEM_X_ACCURACY', 'ITEM_X_SPECIAL', 'ITEM_DIRE_HIT',
                   'ITEM_GUARD_SPEC', 'ITEM_BLUE_FLUTE', 'ITEM_RED_FLUTE',
                   'ITEM_YELLOW_FLUTE', 'ITEM_BLACK_FLUTE', 'ITEM_WHITE_FLUTE',
                   'ITEM_POKE_DOLL', 'ITEM_FLUFFY_TAIL'):
            return 'battle'
        if iid in HEAL:
            return 'heal'
        if iid in TREASURE:
            return 'treasure'
        if rec['hold']:
            return 'held'
        return 'misc'

    for i in items:
        i['cat'] = categorize(i)

    json.dump({'items': items}, open(DRAFT, 'w'), ensure_ascii=False, indent=1)
    print('draft →', DRAFT)

    # stats for the tracker
    from collections import Counter
    print('R/S:', sum(1 for i in items if 'r' in i['g']),
          'EM:', sum(1 for i in items if 'e' in i['g']),
          'FRLG:', sum(1 for i in items if 'f' in i['g']))
    print('cats:', Counter(i['cat'] for i in items))
    distinct = set()
    for i in items:
        distinct.update(i['d'].values())
    print('distinct EN wordings:', len(distinct))


def merge_fa():
    """Merge the hand-written FA files into assets/js/items-gen3.js."""
    items = json.load(open(DRAFT, encoding='utf-8'))['items']

    wordings = {}
    for f in sorted(glob.glob(f'{REPO}/tools/fa3/p*.json')):
        wordings.update(json.load(open(f, encoding='utf-8')))
    names = {}
    for f in (f'{REPO}/tools/fa3/names-reused.json',
              f'{REPO}/tools/fa3/names-extra.json'):
        names.update(json.load(open(f, encoding='utf-8')))

    # --- validation: no silent gaps ---
    gaps = []
    for it in items:
        if it['k'] not in names:
            gaps.append(f"name missing: {it['k']}")
        for grp, en in it['d'].items():
            if en not in wordings:
                gaps.append(f"wording missing ({it['k']}/{grp}): {en[:60]}")
    if gaps:
        print('FA GAPS:')
        for g in gaps[:40]:
            print(' ', g)
        raise SystemExit(f'{len(gaps)} FA gaps — refusing to emit')

    # --- emit ---
    cats = []
    for it in items:
        if it['cat'] not in cats:
            cats.append(it['cat'])
    recs = []
    for it in items:
        r = {'k': it['k'], 'en': it['en'], 'fa': names[it['k']], 'g': it['g'],
             'pk': it['pk'], 'hold': it['hold'], 'cat': it['cat'],
             'p': it['p'], 'd': it['d']}
        if 'pk_v' in it:
            r['pk_v'] = it['pk_v']
        if 'en_e' in it:
            r['en_e'] = it['en_e']
        if 'en_f' in it:
            r['en_f'] = it['en_f']
        # FA wordings per group, keyed like d; groups whose FA equals the
        # first existing group's FA are omitted (dedupe)
        f = {}
        first = None
        for grp in ('rs', 'e', 'frlg'):
            if grp in it['d']:
                fa = wordings[it['d'][grp]]
                if first is None:
                    f[grp] = fa
                    first = fa
                elif fa != first:
                    f[grp] = fa
        if f:
            r['f'] = f
        if 'fl' in it:
            r['fl'] = it['fl']
        if 'firm' in it:
            r['firm'] = it['firm']
        r['i'] = it['i']
        recs.append(r)

    hdr = (
        '"use strict";\n'
        '/* Pokédex Plus — ITEM DEX data (Generation III). Generated by\n'
        '   tools/build-items-gen3.py from the pret decompiles (pokeruby /\n'
        '   pokeemerald / pokefirered) + PokeAPI icons — do not edit.\n'
        '   g: r=RUBY s=SAPPHIRE e=EMERALD f=FIRERED l=LEAFGREEN (R and S\n'
        '   share one cartridge table; F and L share one) · pk: bag pocket\n'
        '   (ball|item|key|berry) · p: buy price per game GROUP\n'
        '   (rs | e | frlg — 0 = not for sale) · d: the cartridge GROUP\'s\n'
        '   own wording · f: FA wordings (groups equal to the first are\n'
        '   omitted) · fl: berry flavors (spicy/dry/sweet/bitter/sour) ·\n'
        '   firm: berry firmness · i: PokeAPI color icon (null = no menu\n'
        '   icon existed in any Gen-3 game — the UI shows a placeholder). */\n'
    )
    js = (hdr + 'const ITEM_CATS = ' + json.dumps(cats) + ';\n'
          + 'const ITEMS = ' + json.dumps(recs, ensure_ascii=False,
                                          separators=(',', ':')) + ';\n')
    open(OUT_JS, 'w', encoding='utf-8').write(js)
    print(f'→ {OUT_JS}: {len(recs)} items, cats={cats}, '
          f'{os.path.getsize(OUT_JS)} bytes')


if __name__ == '__main__':
    if '--merge' in sys.argv:
        merge_fa()
    else:
        main()
