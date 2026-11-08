#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch the Gen-3 pret sources needed for the moves build into tools/gen3-cache/."""
import os
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "gen3-cache")
PRET = "https://raw.githubusercontent.com/pret"

FILES = [
    # (repo, path, cache-name)
    ("pokeemerald", "src/data/battle_moves.h", "em_battle_moves.h"),
    ("pokeemerald", "src/data/contest_moves.h", "em_contest_moves.h"),
    ("pokeemerald", "src/data/pokemon/level_up_learnsets.h", "em_level_up_learnsets.h"),
    ("pokeemerald", "src/data/pokemon/egg_moves.h", "em_egg_moves.h"),
    ("pokeemerald", "src/data/pokemon/tmhm_learnsets.h", "em_tmhm_learnsets.h"),
    ("pokeemerald", "src/data/pokemon/tutor_learnsets.h", "em_tutor_learnsets.h"),
    ("pokeemerald", "include/constants/tms_hms.h", "em_tms_hms.h"),
    ("pokeemerald", "src/item.c", "em_item.c"),
    ("pokeemerald", "include/constants/moves.h", "em_moves_const.h"),
    ("pokeemerald", "include/constants/contest.h", "em_contest_const.h"),
    ("pokeruby", "src/data/battle_moves.c", "rs_battle_moves.c"),
    ("pokeruby", "src/data/contest_moves.h", "rs_contest_moves.h"),
    ("pokeruby", "src/data/pokemon/level_up_learnsets.h", "rs_level_up_learnsets.h"),
    ("pokeruby", "src/data/pokemon/egg_moves.h", "rs_egg_moves.h"),
    ("pokeruby", "src/data/pokemon/tmhm_learnsets.h", "rs_tmhm_learnsets.h"),
    ("pokeruby", "src/item.c", "rs_item.c"),
    ("pokeruby", "include/constants/moves.h", "rs_moves_const.h"),
    ("pokefirered", "src/data/battle_moves.h", "frlg_battle_moves.h"),
    ("pokefirered", "src/data/pokemon/level_up_learnsets.h", "frlg_level_up_learnsets.h"),
    ("pokefirered", "src/data/pokemon/egg_moves.h", "frlg_egg_moves.h"),
    ("pokefirered", "src/data/pokemon/tmhm_learnsets.h", "frlg_tmhm_learnsets.h"),
    ("pokefirered", "src/data/pokemon/tutor_learnsets.h", "frlg_tutor_learnsets.h"),
    ("pokefirered", "src/item.c", "frlg_item.c"),
    ("pokefirered", "include/constants/moves.h", "frlg_moves_const.h"),
]

os.makedirs(CACHE, exist_ok=True)
for repo, path, name in FILES:
    dst = os.path.join(CACHE, name)
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        print(f"  cached {name}")
        continue
    url = f"{PRET}/{repo}/master/{path}"
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "pokedex-plus/1.0"})
            blob = urllib.request.urlopen(req, timeout=40).read()
            open(dst, "wb").write(blob)
            print(f"  fetched {name} ({len(blob)} B)")
            break
        except Exception as e:  # noqa: BLE001
            print(f"  retry {name}: {e}")
            time.sleep(2)
    else:
        raise RuntimeError(f"fetch failed: {url}")
print("done")
