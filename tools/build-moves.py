#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pokédex Plus — Phase 2 build tool: moves data for the Gen-1/2 dexes.

Regenerates (idempotent, cached network fetches):
  assets/js/moves-fa.js          shared move names + descriptions (EN + FA)
  assets/js/moves-rb.js          Red/Blue      move stats + learnsets + TM/HM list
  assets/js/moves-yellow.js      Yellow        move stats + learnsets + TM/HM list
  assets/js/moves-gs.js          Gold/Silver   move stats + learnsets + TM/HM list
  assets/js/moves-crystal.js     Crystal       move stats + learnsets + TM/HM list

Sources (authentic-first, like every other data set in this project):
  · move stats (power / type / accuracy / PP) come from the pret
    decompiles — data/moves/moves.asm of pokered (Gen 1, 165 moves)
    and pokegold (Gen 2, 251 moves). This keeps every generation-1
    quirk intact: Gust/Karate Chop/Bite are NORMAL, Sand Attack is
    NORMAL, Rock Throw is 65% accurate, Barrier has 30 PP, …
  · TM/HM lists come from the same decompiles (item_constants.asm) and
    are cross-checked against PokéAPI's machine table for all four
    version groups.
  · learnsets (level-up / machine / egg / tutor per version group)
    come from the PokéAPI GraphQL endpoint.
  · move display names and the authentic Gold/Silver/Crystal in-game
    descriptions come from PokéAPI.
  · Persian names/descriptions: tools/moves-fa.py (hand-maintained).

The UI files assets/js/moves-module.js, assets/css/moves.css and the
page integrations are hand-written and are NOT touched by this tool.

Run:  python3 tools/build-moves.py [--refresh]
"""
import argparse
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
JS = os.path.join(ROOT, "assets", "js")
CACHE = os.path.join(HERE, "moves-cache")
GQL = "https://beta.pokeapi.co/graphql/v1beta"
PRET = "https://raw.githubusercontent.com/pret"

sys.path.insert(0, HERE)
from moves_fa import MOVES_FA, MOVES_DESC_FA   # noqa: E402

VGS = {1: "red-blue", 2: "yellow", 3: "gold-silver", 4: "crystal"}
GAMES = [
    (1, "moves-rb.js", 1, "red-blue", "RED/BLUE"),
    (2, "moves-yellow.js", 1, "yellow", "YELLOW"),
    (3, "moves-gs.js", 2, "gold-silver", "GOLD/SILVER"),
    (4, "moves-crystal.js", 2, "crystal", "CRYSTAL"),
]
TYPE_FIX = {"psychic_type": "psychic", "curse_type": "unknown"}

REFRESH = False


# ------------------------------------------------------------------ fetch utils
def http_get(url, data=None, headers=None, retries=4):
    last = None
    for _ in range(retries):
        try:
            req = urllib.request.Request(url, data=data,
                                         headers=headers or {"User-Agent": "pokedex-plus/1.0"})
            return urllib.request.urlopen(req, timeout=40).read()
        except Exception as e:
            last = e
    raise RuntimeError(f"fetch failed {url}: {last}")


def fetch_cached(url, key):
    os.makedirs(CACHE, exist_ok=True)
    cf = os.path.join(CACHE, key)
    if not REFRESH and os.path.exists(cf) and os.path.getsize(cf) > 0:
        with open(cf, "rb") as f:
            return f.read()
    blob = http_get(url)
    with open(cf, "wb") as f:
        f.write(blob)
    return blob


def gql(query):
    raw = http_get(GQL, data=json.dumps({"query": query}).encode(),
                   headers={"Content-Type": "application/json",
                            "User-Agent": "pokedex-plus/1.0"})
    out = json.loads(raw)
    if out.get("errors"):
        raise RuntimeError(f"graphql errors: {out['errors'][:3]}")
    return out["data"]


# ------------------------------------------------------------------ pret tables
def pret_move_constants(repo):
    src = fetch_cached(f"{PRET}/{repo}/master/constants/move_constants.asm",
                       f"{repo}_move_constants.asm").decode()
    order = re.findall(r"^\s*const\s+([A-Z_][A-Z0-9_]*)(?:\s*;.*)?$", src, re.M)
    return {name: i for i, name in enumerate(order)}


def pret_move_table(repo):
    src = fetch_cached(f"{PRET}/{repo}/master/data/moves/moves.asm",
                       f"{repo}_moves.asm").decode()
    consts = pret_move_constants(repo)
    rows = re.findall(
        r"^\s*move\s+([A-Z_][A-Z0-9_]*),\s*[A-Z_0-9]+,\s*(\d+|-),\s*([A-Z_]+),\s*(\d+)\s*,\s*(\d+)",
        src, re.M)
    return {consts[name]: [mtype.lower(), int(power), int(acc), int(pp)]
            for name, power, mtype, acc, pp in rows}


def pret_tmhm(repo):
    src = fetch_cached(f"{PRET}/{repo}/master/constants/item_constants.asm",
                       f"{repo}_item_constants.asm").decode()
    consts = pret_move_constants(repo)
    tm_part = re.search(r"DEF TM01 EQU const_value(.*?)(?:DEF NUM_TMS|ASSERT NUM_TMS)", src, re.S)
    hm_part = re.search(r"DEF HM01 EQU const_value(.*?)DEF NUM_HMS", src, re.S)
    tms = re.findall(r"add_tm\s+([A-Z_][A-Z0-9_]*)", tm_part.group(1))
    hms = re.findall(r"add_hm\s+([A-Z_][A-Z0-9_]*)", hm_part.group(1))
    return [consts[n] for n in tms], [consts[n] for n in hms]


# ------------------------------------------------------------------ pokeapi
def clean_flavor(s):
    """The G/S/C flavor text carries soft hyphens (U+00AD) where the game
    broke a word across lines — rejoin the word, then squeeze whitespace."""
    s = re.sub(r"\xad\s*", "", s)  # rejoin words the game hyphen-split across lines
    return re.sub(r"\s+", " ", s).strip()


def fetch_move_names():
    data = gql('{ m: pokemon_v2_move(where: {id: {_lte: 251}}, order_by: {id: asc}) { id name } }')
    return {m["id"]: m["name"] for m in data["m"]}


def fetch_move_flavor():
    """EN display name + Gold/Silver (= Crystal) in-game description per move."""
    data = gql("""query {
      f: pokemon_v2_moveflavortext(
        where: {language_id: {_eq: 9}, version_group_id: {_eq: 3}}, order_by: {move_id: asc}) {
        move_id flavor_text
      }
      n: pokemon_v2_movename(where: {language_id: {_eq: 9}, move_id: {_lte: 251}}) {
        move_id name
      }
    }""")
    desc = {f["move_id"]: clean_flavor(f["flavor_text"]) for f in data["f"]}
    disp = {n["move_id"]: n["name"] for n in data["n"]}
    return disp, desc


def fetch_machines():
    data = gql("""query {
      machines: pokemon_v2_machine(where: {version_group_id: {_lte: 4}}) {
        move_id version_group_id
        item: pokemon_v2_item { name }
      }
    }""")
    out = {}
    for m in data["machines"]:
        out.setdefault(m["version_group_id"], []).append((m["item"]["name"], m["move_id"]))
    for vg in out:
        out[vg].sort()
    return out


def fetch_learnsets():
    rows = {}
    for lo, hi in [(1, 84), (85, 168), (169, 251)]:
        data = gql("""query {
          p: pokemon_v2_pokemon(where: {id: {_gte: %d, _lte: %d}}) {
            id
            moves: pokemon_v2_pokemonmoves(where: {version_group_id: {_in: [1,2,3,4]}}) {
              level version_group_id move_id method: move_learn_method_id
            }
          }
        }""" % (lo, hi))
        for p in data["p"]:
            rows[p["id"]] = p["moves"]
    return rows


# ------------------------------------------------------------------ build
def js_str(s):
    return json.dumps(s, ensure_ascii=False)


def main():
    global REFRESH
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="ignore the fetch cache")
    args = ap.parse_args()
    REFRESH = args.refresh

    print("== pret move tables ==")
    moves_gen1 = pret_move_table("pokered")
    moves_gen2 = pret_move_table("pokegold")
    rb_tm, rb_hm = pret_tmhm("pokered")
    gs_tm, gs_hm = pret_tmhm("pokegold")
    assert len(moves_gen1) == 165 and len(moves_gen2) == 251
    assert (len(rb_tm), len(rb_hm)) == (50, 5) and (len(gs_tm), len(gs_hm)) == (50, 7)
    print(f"  gen1 {len(moves_gen1)} moves, gen2 {len(moves_gen2)} moves, TM/HM lists ok")

    print("== PokéAPI: names, flavor, machines ==")
    slugs = fetch_move_names()
    disp, desc = fetch_move_flavor()
    api_machines = fetch_machines()
    api_tm = {vg: {int(n[2:]): m for n, m in rows if n.startswith("tm")}
              for vg, rows in api_machines.items()}
    api_hm = {vg: {int(n[2:]): m for n, m in rows if n.startswith("hm")}
              for vg, rows in api_machines.items()}
    for vg, tms, hms in [(1, rb_tm, rb_hm), (2, rb_tm, rb_hm), (3, gs_tm, gs_hm), (4, gs_tm, gs_hm)]:
        assert api_tm[vg] == {i + 1: m for i, m in enumerate(tms)}, f"TM mismatch vg{vg}"
        assert api_hm[vg] == {i + 1: m for i, m in enumerate(hms)}, f"HM mismatch vg{vg}"
    print("  TM/HM lists cross-checked against PokéAPI ✓")

    print("== PokéAPI: learnsets ==")
    raw = fetch_learnsets()
    learn = {}
    for pid, rows in raw.items():
        per = {}
        for r in rows:
            meth = r["method"]
            if meth not in (1, 2, 3, 4):
                continue  # 5 = stadium surfing pikachu (not in the GB cartridges)
            b = per.setdefault(r["version_group_id"], {"lv": [], "tm": [], "egg": [], "tutor": []})
            if meth == 1:
                b["lv"].append([r["level"], r["move_id"]])
            elif meth == 4:
                b["tm"].append(r["move_id"])
            elif meth == 2:
                b["egg"].append(r["move_id"])
            else:
                b["tutor"].append(r["move_id"])
        for b in per.values():
            b["lv"].sort(key=lambda x: (x[0], x[1]))
        learn[pid] = per

    print("== sanity ==")
    for i in range(1, 252):
        s = slugs[i]
        assert s in MOVES_FA, f"missing FA name: {s}"
        assert s in MOVES_DESC_FA, f"missing FA description: {s}"
        assert desc.get(i), f"missing G/S description: {s}"
        assert disp.get(i), f"missing EN display name: {s}"
    problems = []
    for pid, per in learn.items():
        for vg, b in per.items():
            tset = set(rb_tm + rb_hm) if vg in (1, 2) else set(gs_tm + gs_hm)
            for mv in b["tm"]:
                if mv not in tset:
                    problems.append(f"p{pid} vg{vg}: machine move {mv} not in TM/HM list")
    assert not problems, problems[:5]
    print(f"  {len(learn)} pokemon learnsets validated")

    print("== write assets ==")
    parts = ['"use strict";\n',
             '/* Pokédex Plus — move names & descriptions (shared, all Gen-1/2 moves).\n',
             '   Generated by tools/build-moves.py — do not edit by hand.\n',
             '   Entry: [EN name, FA name, EN description (Gold/Silver in-game text), FA description].\n',
             '   Gen-1 games had no move text; the description is used there as the "effect" wording. */\n',
             'const MOVE_INFO = {\n']
    for i in range(1, 252):
        s = slugs[i]
        parts.append(f'  {js_str(s)}:[{js_str(disp[i])},{js_str(MOVES_FA[s])},'
                     f'{js_str(desc[i])},{js_str(MOVES_DESC_FA[s])}],\n')
    parts.append("};\n")
    with open(os.path.join(JS, "moves-fa.js"), "w", encoding="utf-8") as f:
        f.write("".join(parts))
    print("  moves-fa.js")

    for vg, fname, gen, game, label in GAMES:
        n_moves = 165 if gen == 1 else 251
        mv_lines = []
        for i in range(1, n_moves + 1):
            tp, power, acc, pp = (moves_gen1 if gen == 1 else moves_gen2)[i]
            tp = TYPE_FIX.get(tp, tp)
            mv_lines.append(f'    {i}:[{js_str(slugs[i])},{js_str(tp)},{power},{acc},{pp}],')
        tm = api_tm[vg] if vg in api_tm else {}
        hm = api_hm[vg] if vg in api_hm else {}
        # prefer the pret order (same values, guaranteed order)
        tm_list = rb_tm if vg in (1, 2) else gs_tm
        hm_list = rb_hm if vg in (1, 2) else gs_hm
        tm = {i + 1: m for i, m in enumerate(tm_list)}
        hm = {i + 1: m for i, m in enumerate(hm_list)}
        learn_lines = []
        for pid in range(1, 252):
            b = learn.get(pid, {}).get(vg)
            if not b:
                continue
            lv = ",".join(f'[{l},{m}]' for l, m in b["lv"])
            tms = ",".join(str(m) for m in b["tm"])
            egg = ",".join(str(m) for m in b["egg"])
            tut = ",".join(str(m) for m in b["tutor"])
            learn_lines.append(
                f'    {pid}:{{lv:[{lv}],tm:[{tms}],egg:[{egg}],tutor:[{tut}]}},')
        js = f""""use strict";
/* Pokédex Plus — moves data for {label} (Generation {gen}).
   Generated by tools/build-moves.py from the pret decompiles
   (pokered / pokegold move tables = authentic power/type/accuracy/PP)
   and PokéAPI learnsets — do not edit by hand. */
const MD = {{
  game: {js_str(game)}, gen: {gen}, label: {js_str(label)},
  /* move id -> [slug, type, power, accuracy, pp] */
  moves: {{
{chr(10).join(mv_lines)}
  }},
  /* TM / HM number -> move id (authentic machine list of this game) */
  tm: {{ {",".join(f'{k}:{v}' for k, v in sorted(tm.items()))} }},
  hm: {{ {",".join(f'{k}:{v}' for k, v in sorted(hm.items()))} }},
  /* pokemon id -> learnset in this game */
  learn: {{
{chr(10).join(learn_lines)}
  }}
}};
"""
        with open(os.path.join(JS, fname), "w", encoding="utf-8") as f:
            f.write(js)
        print(f"  {fname}: {n_moves} moves / {len(learn_lines)} learnsets")
    print("== done ==")


if __name__ == "__main__":
    main()
