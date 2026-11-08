#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Gen-3 moves data files for gen3.html.

Sources (all cached under tools/gen3-cache/ by fetch-gen3-moves-*.py):
  pret pokeemerald / pokeruby / pokefirered  — battle stats, learnsets,
      TM/HM compat, tutor learnsets, contest data (era-true, per game)
  tools/gen3-cache/moves-api.json            — PokeAPI EN names + per-version
      flavor texts (ruby-sapphire / emerald / firered-leafgreen)
  assets/js/moves-fa.js                      — reused FA names (ids 1..251
      where the EN name is unchanged)
  tools/gen3-moves-fa.json                   — hand-written FA names for the
      rest + hand-written FA descriptions keyed by the EN wording
      (wordings deduped across the three games by the key itself)

Emits:
  assets/js/moves-gen3.js   — MD_RS + MD_EM + MD_FRLG + var MD (gen2 merge pattern)
  assets/js/moves-fa-gen3.js — var MOVE_INFO (names + Emerald-wording base text)
  tools/gen3-moves-wordings.json — the unique EN wordings (FA workflow input)
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "gen3-cache")
JS = os.path.join(HERE, "..", "assets", "js")

GAMES = ("em", "rs", "frlg")
GAME_META = {
    "rs":   {"game": "rs",    "label": "RUBY/SAPPHIRE",     "vg": "ruby-sapphire",    "file_moves": "rs_battle_moves.c",   "file_const": "rs_moves_const.h",   "file_species": "rs_species.h",   "file_lu_ptr": "rs_lu_pointers.h",   "file_lu": "rs_level_up_learnsets.h",   "file_egg": "rs_egg_moves.h",   "file_tmhm": "rs_tmhm_learnsets.h",   "file_tutor": None,                    "file_contest": "rs_contest_moves.h"},
    "em":   {"game": "emerald", "label": "EMERALD",         "vg": "emerald",          "file_moves": "em_battle_moves.h",   "file_const": "em_moves_const.h",   "file_species": "species.h",      "file_lu_ptr": "em_lu_pointers.h",   "file_lu": "em_level_up_learnsets.h",   "file_egg": "em_egg_moves.h",   "file_tmhm": "em_tmhm_learnsets.h",   "file_tutor": "em_tutor_learnsets.h",  "file_contest": "em_contest_moves.h"},
    "frlg": {"game": "frlg",  "label": "FIRERED/LEAFGREEN", "vg": "firered-leafgreen", "file_moves": "frlg_battle_moves.h", "file_const": "frlg_moves_const.h", "file_species": "frlg_species.h", "file_lu_ptr": "frlg_lu_pointers.h", "file_lu": "frlg_level_up_learnsets.h", "file_egg": "frlg_egg_moves.h", "file_tmhm": "frlg_tmhm_learnsets.h", "file_tutor": "frlg_tutor_learnsets.h", "file_contest": None},
}
TYPES = {"normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison",
         "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel",
         "unknown"}
# Gen-3 Curse is TYPE_MYSTERY — the repo's "???" convention
TYPE_ALIAS = {"mystery": "unknown"}
# pret (Gen-3 era) slug vs modern PokeAPI slug — same move, renamed later
MOVE_RENAMES = {136: ("hi-jump-kick", "high-jump-kick"),
                185: ("faint-attack", "feint-attack"),
                265: ("smelling-salt", "smelling-salts")}
CONTEST_CATS = {"COOL": 0, "BEAUTY": 1, "CUTE": 2, "SMART": 3, "TOUGH": 4}

def rd(name):
    with open(os.path.join(CACHE, name), encoding="utf-8") as f:
        return f.read()

def norm(name):
    """normalize a pret constant slug for comparisons: MOVE_SOLARBEAM -> solarmove key"""
    return re.sub(r"[^A-Z0-9]", "", name.upper())

def parse_move_consts(name):
    out = {}
    for m in re.finditer(r"#define (MOVE_\w+) (\d+)", rd(name)):
        mid = int(m.group(2))
        if 1 <= mid <= 354:
            out[mid] = m.group(1)[5:]
    assert len(out) == 354, f"{name}: {len(out)} move ids"
    return out

SLUG_CONST = {"nidoran-f": "NIDORAN_F", "nidoran-m": "NIDORAN_M", "mr-mime": "MR_MIME",
              "farfetchd": "FARFETCHD", "ho-oh": "HO_OH", "deoxys-normal": "DEOXYS"}

def slug_to_const(slug):
    if slug in SLUG_CONST:
        return SLUG_CONST[slug]
    return slug.upper().replace("-", "_")

def parse_species(name):
    """{internal_id: CONST} — all ids (Hoenn species sit at internal 387..410;
    the 252..276 gap holds dummy OLD_UNOWN_* placeholders that never map)."""
    out = {}
    for m in re.finditer(r"#define SPECIES_(\w+) (\d+)", rd(name)):
        out.setdefault(int(m.group(2)), m.group(1))
    return out

def parse_battle_moves(name, move_ids):
    txt = rd(name)
    out = {}
    for m in re.finditer(r"\[MOVE_(\w+)\]\s*=\s*\{(.*?)\},?", txt, re.S):
        mv, body = m.group(1), m.group(2)
        mid = next((i for i, n in move_ids.items() if n == mv), None)
        if mid is None:
            continue
        def field(f):
            mm = re.search(r"\." + f + r"\s*=\s*(-?\w+)", body)
            return mm.group(1) if mm else None
        tp = field("type")
        raw = tp[5:].lower() if tp and tp.startswith("TYPE_") else None
        raw = TYPE_ALIAS.get(raw, raw)
        assert raw in TYPES, f"{name}/{mv}: bad type {tp}"
        out[mid] = {
            "type": raw,
            "power": int(field("power") or 0),
            "acc": int(field("accuracy") or 0),
            "pp": int(field("pp") or 0),
            "priority": int(field("priority") or 0),
        }
    assert len(out) == 354, f"{name}: {len(out)} battle moves"
    return out

def parse_contest_em(move_ids):
    """pokeemerald: named-field gContestMoves + named gContestEffects."""
    txt = rd(GAME_META["em"]["file_contest"])
    eff_appeal = {}
    for m in re.finditer(r"\[CONTEST_EFFECT_(\w+)\]\s*=\s*\{(.*?)\},?", txt, re.S):
        body = m.group(2)
        ap = re.search(r"\.appeal\s*=\s*(\d+)", body)
        jm = re.search(r"\.jam\s*=\s*(\d+)", body)
        eff_appeal[m.group(1)] = (int(ap.group(1)) // 10, int(jm.group(1)) // 10)
    assert len(eff_appeal) >= 48, f"em effects: {len(eff_appeal)}"
    out = {}
    for m in re.finditer(r"\[MOVE_(\w+)\]\s*=\s*\{(.*?)\},?", txt, re.S):
        mv, body = m.group(1), m.group(2)
        mid = next((i for i, n in move_ids.items() if n == mv), None)
        if mid is None:
            continue
        eff = re.search(r"\.effect\s*=\s*CONTEST_EFFECT_(\w+)", body)
        cat = re.search(r"\.contestCategory\s*=\s*CONTEST_CATEGORY_(\w+)", body)
        if not (eff and cat):
            continue
        ap, jm = eff_appeal[eff.group(1)]
        out[mid] = [CONTEST_CATS[cat.group(1)], ap, jm]
    return out

def parse_contest_rs(move_ids):
    """pokeruby: compact per-move lines '{EFFECT, CATEGORY, combo, {...}}, // MOVE'
       plus positional gContestEffects '{type, appeal, jam}, // NAME'."""
    txt = rd(GAME_META["rs"]["file_contest"])
    eff_block = re.search(r"const struct ContestEffect gContestEffects\[\] = \{(.*?)\};", txt, re.S)
    assert eff_block, "rs gContestEffects not found"
    eff_appeal = {}
    for line in eff_block.group(1).splitlines():
        mm = re.match(r"\s*\{\s*\d+\s*,\s*(\d+)\s*,\s*(\d+)\s*\}\s*,?\s*//\s*(?:CONTEST_EFFECT_)?(\w+)", line)
        if mm:
            eff_appeal[mm.group(3)] = (int(mm.group(1)) // 10, int(mm.group(2)) // 10)
    assert len(eff_appeal) >= 48, f"rs effects: {len(eff_appeal)}"
    mv_block = re.search(r"const struct ContestMove gContestMoves\[\] = \{(.*?)\};", txt, re.S)
    assert mv_block, "rs gContestMoves not found"
    out = {}
    for line in mv_block.group(1).splitlines():
        mm = re.match(r"\s*\{\s*CONTEST_EFFECT_(\w+)\s*,\s*CONTEST_CATEGORY_(\w+)\s*,.*\}\s*,?\s*//\s*(\w+)\s*$", line)
        if not mm:
            continue
        mid = next((i for i, n in move_ids.items() if n == mm.group(3)), None)
        if mid is None:
            continue
        ap, jm = eff_appeal[mm.group(1)]
        out[mid] = [CONTEST_CATS[mm.group(2)], ap, jm]
    return out

def parse_level_up(meta, species_ids, national, move_ids):
    """species_ids: {internal_id: CONST}. national: {const: national_id}.
    Returns {national_id: [[lvl, moveId], ...]} (ids — the module indexes MD.moves)."""
    by_norm = {norm(n): i for i, n in move_ids.items()}
    ptr = rd(meta["file_lu_ptr"])
    if "[SPECIES_" in ptr:
        tbl_of = {}
        for m in re.finditer(r"\[SPECIES_(\w+)\]\s*=\s*(s\w+LevelUpLearnset|NULL)", ptr):
            tbl_of[m.group(1)] = None if m.group(2) == "NULL" else m.group(2)
    else:
        # pokeruby: positional array, index = internal species id (0 = NONE placeholder)
        rows = [l.strip().rstrip(",") for l in ptr.splitlines()
                if l.strip().startswith(("s", "g", "NULL"))]
        tbl_of = {species_ids[i]: (None if r == "NULL" else r)
                  for i, r in enumerate(rows) if i in species_ids}
    assert len(tbl_of) >= 386, f"{meta['file_lu_ptr']}: {len(tbl_of)} pointers"
    lu = rd(meta["file_lu"])
    tables = {}
    for m in re.finditer(r"(?:static )?const u16 ((?:s|g)\w*LevelUpLearnset)\[\] = \{(.*?)LEVEL_UP_END", lu, re.S):
        rows = []
        for mm in re.finditer(r"LEVEL_UP_MOVE\(\s*(\d+)\s*,\s*MOVE_(\w+)\)", m.group(2)):
            mid = by_norm.get(norm(mm.group(2)))
            assert mid, f"{meta['file_lu']}: unknown move {mm.group(2)}"
            rows.append([int(mm.group(1)), mid])
        tables[m.group(1)] = rows
    out = {}
    for sid, sp in species_ids.items():
        nat = national.get(norm(sp))
        if nat is None:
            continue          # dummy placeholder species (OLD_UNOWN_*, etc.)
        t = tbl_of.get(sp)
        if t is None:
            continue
        out[nat] = tables[t]
    return out

def parse_egg(meta, move_ids, national):
    txt = rd(meta["file_egg"])
    by_norm = {norm(n): i for i, n in move_ids.items()}
    sp_by_norm = {norm(s): nat for s, nat in national.items()}
    out = {}
    for m in re.finditer(r"egg_moves\((\w+),((?:[^)\]])*)\)", txt, re.S):
        sid = sp_by_norm.get(norm(m.group(1)))
        if sid is None:
            continue
        moves = [by_norm[norm(x)] for x in re.findall(r"MOVE_(\w+)", m.group(2))]
        out[sid] = moves
    return out

def parse_tmhm_rs_frlg(meta, move_ids, national):
    """TMHM(TM06_TOXIC) tokens: explicit machine numbers."""
    txt = rd(meta["file_tmhm"])
    by_norm = {norm(n): i for i, n in move_ids.items()}
    machines = {}          # ("tm"|"hm", num) -> move id
    out = {}
    for m in re.finditer(r"\[SPECIES_(\w+)\]\s*=\s*TMHM_LEARNSET\((.*?)\)\s*,", txt, re.S):
        sid = species_ids_from_token(m.group(1), national)
        if sid is None:
            continue
        moves = []
        for t in re.finditer(r"TMHM\(\s*(TM|HM)(\d+)_(\w+)\s*\)", m.group(2)):
            kind, num_, mv = t.group(1).lower(), int(t.group(2)), t.group(3)
            mid = by_norm.get(norm(mv))
            assert mid, f"{meta['file_tmhm']}: unknown move {mv}"
            machines.setdefault((kind, num_), mid)
            assert machines[(kind, num_)] == mid, f"{meta['file_tmhm']}: machine conflict {kind}{num_}"
            moves.append(mid)
        out[sid] = sorted(set(moves))
    return out, machines

def species_ids_from_token(token, national):
    return national.get(norm(token))

def parse_tmhm_em(meta, move_ids, national):
    """emerald: FOREACH_TM/FOREACH_HM order = machine numbers; per-species .NAME = TRUE."""
    tms = re.search(r"#define FOREACH_TM\(F\) \\\s*(.*?)\n\n", rd("em_tms_hms.h"), re.S).group(1)
    hms = re.search(r"#define FOREACH_HM\(F\) \\\s*(.*?)\n\n", rd("em_tms_hms.h"), re.S).group(1)
    by_norm = {norm(n): i for i, n in move_ids.items()}
    machines = {}
    for kind, block in (("tm", tms), ("hm", hms)):
        for i, mv in enumerate(re.findall(r"F\((\w+)\)", block), 1):
            mid = by_norm[norm(mv)]
            machines[(kind, i)] = mid
    assert len([k for k in machines if k[0] == "tm"]) == 50 and len([k for k in machines if k[0] == "hm"]) == 8
    txt = rd(meta["file_tmhm"])
    out = {}
    for m in re.finditer(r"\[SPECIES_(\w+)\]\s*=\s*\{\s*\.learnset\s*=\s*\{(.*?)\}\s*\}", txt, re.S):
        sid = species_ids_from_token(m.group(1), national)
        if sid is None:
            continue
        flags = set(re.findall(r"\.(\w+)\s*=\s*TRUE", m.group(2)))
        moves = set()
        for (kind, num_), mid in machines.items():
            mv_name = next(n for i, n in move_ids.items() if i == mid)
            if norm(mv_name) in flags:
                moves.add(mid)
        out[sid] = sorted(moves)
    return out, machines

def parse_tutor(meta, move_ids, national):
    txt = rd(meta["file_tutor"])
    by_norm = {norm(n): i for i, n in move_ids.items()}
    out = {}
    # entries: [SPECIES_X] = (TUTOR(MOVE_A) | ...) or 0 — emerald wraps in parens,
    # firered doesn't; split on the [SPECIES_*] markers and collect the tokens.
    marks = list(re.finditer(r"\[SPECIES_(\w+)\]\s*=", txt))
    for i, m in enumerate(marks):
        seg = txt[m.end(): marks[i + 1].start() if i + 1 < len(marks) else m.end() + 4000]
        moves = sorted({by_norm[norm(x)] for x in re.findall(r"TUTOR\(MOVE_(\w+)\)", seg)})
        sid = national.get(norm(m.group(1)))
        if sid and moves:
            out[sid] = moves
    return out

def js_str(s):
    return json.dumps(s, ensure_ascii=False)

def build():
    api = json.load(open(os.path.join(CACHE, "moves-api.json"), encoding="utf-8"))
    nat_slugs = json.load(open(os.path.join(CACHE, "national-slugs.json"), encoding="utf-8"))
    national_const = {norm(slug_to_const(s)): int(i) for i, s in nat_slugs.items()}
    assert len(national_const) == 386
    move_ids, battle, contest, lu, egg, tmhm, tutor = {}, {}, {}, {}, {}, {}, {}
    machines_all = {}
    for g in GAMES:
        meta = GAME_META[g]
        move_ids[g] = parse_move_consts(meta["file_const"])
        battle[g] = parse_battle_moves(meta["file_moves"], move_ids[g])
        # era cross-check: pret slug vs PokeAPI slug (3 modern renames allowed:
        # Hi Jump Kick/High Jump Kick, Faint Attack/Feint Attack, Smelling Salt/Smelling Salts)
        for mid in range(1, 355):
            p = norm(move_ids[g][mid])
            a = norm(api[str(mid)]["name"]).upper()
            assert p == a or (mid in MOVE_RENAMES and norm(MOVE_RENAMES[mid][0]) == p and norm(MOVE_RENAMES[mid][1]) == norm(api[str(mid)]["name"]).upper()), \
                f"{g}: id {mid}: pret {move_ids[g][mid]} != api {api[str(mid)]['name']}"
        species = parse_species(meta["file_species"])
        lu[g] = parse_level_up(meta, species, national_const, move_ids[g])
        print(f"{g}: level-up species {len(lu[g])}/386")
        egg[g] = parse_egg(meta, move_ids[g], national_const)
        print(f"{g}: egg-move species {len(egg[g])}")
        if g == "em":
            tmhm[g], machines_all[g] = parse_tmhm_em(meta, move_ids[g], national_const)
        else:
            tmhm[g], machines_all[g] = parse_tmhm_rs_frlg(meta, move_ids[g], national_const)
        tmc = [k for k in machines_all[g] if k[0] == "tm"]
        hmc = [k for k in machines_all[g] if k[0] == "hm"]
        assert len(tmc) == 50 and len(hmc) == 8, f"{g}: machines tm={len(tmc)} hm={len(hmc)}"
        print(f"{g}: TM/HM compat species {len(tmhm[g])}; 50 TMs + 8 HMs OK")
        tutor[g] = parse_tutor(meta, move_ids[g], national_const) if meta["file_tutor"] else {}
        print(f"{g}: tutor species {len(tutor[g])}" + (" (no tutors — correct for R/S)" if g == "rs" else ""))
        contest[g] = parse_contest_em(move_ids[g]) if g == "em" else (parse_contest_rs(move_ids[g]) if g == "rs" else None)
        if contest[g]:
            print(f"{g}: contest moves {len(contest[g])}")
        else:
            print(f"{g}: no contest data (FRLG — authentic)")

    # ---- per-game desc (base = Emerald wording; store only diffs) ----
    flavor = {g: {mid: api[str(mid)]["flavor"][GAME_META[g]["vg"]] for mid in range(1, 355)} for g in GAMES}
    base = flavor["em"]
    desc = {}
    for g in GAMES:
        desc[g] = {mid: flavor[g][mid] for mid in range(1, 355) if flavor[g][mid] != base[mid]}
    print("desc diffs vs Emerald: rs", len(desc["rs"]), "frlg", len(desc["frlg"]))

    # ---- wording dump for the FA workflow (deduped by string) ----
    words = sorted({w for g in GAMES for w in flavor[g].values()})
    json.dump(words, open(os.path.join(HERE, "gen3-moves-wordings.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"unique EN wordings: {len(words)} -> tools/gen3-moves-wordings.json")

    # ---- FA names: reuse moves-fa.js where the EN name is unchanged ----
    fa_src = open(os.path.join(JS, "moves-fa.js"), encoding="utf-8").read()
    fa_names = {}
    for m in re.finditer(r'"([a-z0-9-]+)":\s*\["([^"]+)",\s*"([^"]+)"', fa_src):
        fa_names[m.group(1)] = (m.group(2), m.group(3))   # slug -> (EN, FA)
    fa_name_map = {}                                     # mid -> FA
    reuse, todo = 0, []
    for mid in range(1, 355):
        slug = api[str(mid)]["name"]
        en = api[str(mid)]["en"]
        hit = fa_names.get(slug)
        if hit and re.sub(r"[^a-z0-9]", "", hit[0].lower()) == re.sub(r"[^a-z0-9]", "", en.lower()):
            fa_name_map[mid] = hit[1]
            reuse += 1
        else:
            todo.append((mid, slug, en))
    print(f"FA names reused {reuse}/354; hand-written needed: {len(todo)}")
    json.dump([{"id": t[0], "slug": t[1], "en": t[2]} for t in todo],
              open(os.path.join(HERE, "gen3-moves-names-todo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    fa_file = os.path.join(HERE, "gen3-moves-fa.json")
    fa = json.load(open(fa_file, encoding="utf-8")) if os.path.exists(fa_file) else {}
    missing_fa_names = [t for t in todo if str(t[0]) not in fa.get("names", {})]
    missing_fa_words = [w for w in words if w not in fa.get("desc", {})]
    if missing_fa_names or missing_fa_words:
        print(f"FA pending: {len(missing_fa_names)} names, {len(missing_fa_words)} wordings — "
              f"fill tools/gen3-moves-fa.json (names: {{id: fa}}, desc: {{en wording: fa}})")
        if "--fa-required" in sys.argv:
            sys.exit("FA data incomplete")
        return
    print(f"FA complete: {len(fa.get('names', {}))} names, {len(fa.get('desc', {}))} wordings")

    def md_for(g):
        meta = GAME_META[g]
        moves = {}
        for mid in range(1, 355):
            b = battle[g][mid]
            moves[mid] = [api[str(mid)]["name"], b["type"], b["power"], b["acc"], b["pp"], b["priority"]]
        tm = {n: machines_all[g][("tm", n)] for n in range(1, 51)}
        hm = {n: machines_all[g][("hm", n)] for n in range(1, 9)}
        learn = {}
        for sid in range(1, 387):
            e = {"lv": lu[g].get(sid, []), "tm": tmhm[g].get(sid, []),
                 "egg": egg[g].get(sid, []), "tutor": tutor[g].get(sid, [])}
            if e["lv"] or e["tm"] or e["egg"] or e["tutor"]:
                learn[sid] = e
        d = {"game": meta["game"], "gen": 3, "label": meta["label"],
             "moves": moves, "tm": tm, "hm": hm, "learn": learn}
        if desc[g]:
            d["desc"] = desc[g]
        if contest[g]:
            d["contest"] = contest[g]
        return d

    parts = []
    consts, cidx = {}, [0]
    def intern(s):
        if s not in consts:
            cidx[0] += 1
            consts[s] = f"D{cidx[0]}"
        return consts[s]
    for g in GAMES:
        meta = GAME_META[g]
        d = md_for(g)
        dg = d.pop("desc", {})
        arrs = []
        arrs.append(f'game:{js_str(d["game"])},gen:3,label:{js_str(d["label"])}')
        arrs.append("moves:{" + ",".join(f'{mid}:{json.dumps(v, ensure_ascii=False, separators=(",", ":"))}' for mid, v in sorted(d["moves"].items())) + "}")
        arrs.append("tm:{" + ",".join(f'"{n}":{t}' for n, t in sorted(d["tm"].items(), key=lambda x: x[0])) + "}")
        arrs.append("hm:{" + ",".join(f'"{n}":{h}' for n, h in sorted(d["hm"].items(), key=lambda x: x[0])) + "}")
        learn_parts = []
        for sid in sorted(d["learn"]):
            e = d["learn"][sid]
            learn_parts.append(f'{sid}:{{lv:{json.dumps(e["lv"], separators=(",", ":"))},tm:{json.dumps(e["tm"], separators=(",", ":"))},egg:{json.dumps(e["egg"], separators=(",", ":"))},tutor:{json.dumps(e["tutor"], separators=(",", ":"))}}}')
        arrs.append("learn:{" + ",".join(learn_parts) + "}")
        if dg:
            arrs.append("desc:{" + ",".join(f'{mid}:[{intern(dg[mid])},{intern(fa["desc"][dg[mid]])}]' for mid in sorted(dg)) + "}")
        if d.get("contest"):
            arrs.append("contest:{" + ",".join(f'{mid}:{json.dumps(v, separators=(",", ":"))}' for mid, v in sorted(d["contest"].items())) + "}")
        name = {"rs": "MD_RS", "em": "MD_EM", "frlg": "MD_FRLG"}[g]
        kw = "var" if g == "em" else "const"
        parts.append(f"/* ===== {meta['label']} ===== */\n{kw} {name} = {{\n  " + ",\n  ".join(arrs) + "\n};")

    header = (
        '"use strict";\n'
        "/* Pokédex Plus — merged Gen-3 moves data (gen3.html).\n"
        "   Generated by tools/build-gen3-moves.py from the pret decompiles\n"
        "   (pokeemerald / pokeruby / pokefirered) + PokeAPI flavor texts — do not edit by hand.\n"
        "   MD_RS = Ruby/Sapphire (contest data incl.), MD_EM = Emerald (its own tutors,\n"
        "   contest), MD_FRLG = FireRed/LeafGreen (no contests — authentic). `var MD`\n"
        "   points at the ACTIVE game and is swapped by MovesUI.setGame() on theme change.\n"
        "   desc: only wordings that differ from the Emerald base (moves-fa-gen3.js);\n"
        "   moves: [slug, type, power, accuracy, pp, priority]. contest: {moveId:[category,\n"
        "   appeal hearts, jam hearts]} (R/S/E only). */\n\n"
    )
    # ---- moves-fa-gen3.js: var MOVE_INFO = {slug:[EN, FA, EN-base, FA-base]} ----
    info_rows = []
    for mid in range(1, 355):
        slug = api[str(mid)]["name"]
        en = api[str(mid)]["en"]
        fa_name = fa["names"].get(str(mid)) or fa_name_map.get(mid)
        assert fa_name, f"missing FA name for {mid} {slug}"
        base_en, base_fa_w = base[mid], fa["desc"][base[mid]]
        info_rows.append(f'{js_str(slug)}:[{js_str(en)},{js_str(fa_name)},{intern(base_en)},{intern(base_fa_w)}]')
    open(os.path.join(JS, "moves-fa-gen3.js"), "w", encoding="utf-8").write(
        '"use strict";\n'
        "/* Pokédex Plus — Gen-3 move names & base descriptions (gen3.html).\n"
        "   Generated by tools/build-gen3-moves.py — do not edit by hand.\n"
        "   Entry: [EN name, FA name, EN description (Emerald in-game wording), FA description].\n"
        "   Per-game wording diffs live in moves-gen3.js (MD_RS/MD_EM/MD_FRLG .desc).\n"
        "   The Gen-1/Gen-2 shared moves-fa.js is untouched — this file serves gen3 only. */\n"
        "var MOVE_INFO = {\n  " + ",\n  ".join(info_rows) + "\n};\n")
    consts_js = "".join(f"const {name_} = {js_str(s)};\n" for s, name_ in consts.items())
    tail = "\nvar MD = MD_RS; /* default theme: RUBY — gen3.js swaps on theme change */\n"
    open(os.path.join(JS, "moves-gen3.js"), "w", encoding="utf-8").write(
        header + consts_js + "\n" + "\n\n".join(parts) + "\n" + tail)
    print("WROTE assets/js/moves-gen3.js + assets/js/moves-fa-gen3.js")

if __name__ == "__main__":
    build()
