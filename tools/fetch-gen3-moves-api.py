#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch PokeAPI move data (ids 1..354) into a compact cache for the Gen-3 moves build.

Output: tools/gen3-cache/moves-api.json  ({id: {name, en, flavor:{vg: text}}})
VGs kept: ruby-sapphire, emerald, firered-leafgreen (the Gen-3 version groups).
"""
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "gen3-cache", "moves-api.json")
VGS = ("ruby-sapphire", "emerald", "firered-leafgreen")


def clean(s):
    s = re.sub(r"\xad\s*", "", s)
    s = re.sub(r"[\n\r\f]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def main():
    out = {}
    if os.path.exists(CACHE):
        out = json.load(open(CACHE, encoding="utf-8"))
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for i in range(start, 355):
        if str(i) in out and all(v in out[str(i)]["flavor"] for v in VGS):
            continue
        url = f"https://pokeapi.co/api/v2/move/{i}/"
        for attempt in range(5):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "pokedex-plus/1.0"})
                d = json.loads(urllib.request.urlopen(req, timeout=30).read())
                break
            except Exception as e:  # noqa: BLE001
                print(f"  retry {i}: {e}", flush=True)
                time.sleep(2 + attempt)
        else:
            raise RuntimeError(f"fetch failed: {url}")
        flavor = {}
        for f in d.get("flavor_text_entries", []):
            if f["language"]["name"] != "en":
                continue
            vg = f["version_group"]["name"]
            if vg in VGS and vg not in flavor:
                flavor[vg] = clean(f["flavor_text"])
        en_name = d["name"]
        for nm in d.get("names", []):
            if nm["language"]["name"] == "en":
                en_name = nm["name"]
                break
        out[str(i)] = {"name": d["name"], "en": en_name, "flavor": flavor}
        if i % 25 == 0:
            json.dump(out, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
            print(f"  ..{i}", flush=True)
        time.sleep(0.12)
    json.dump(out, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    # coverage report
    missing = [(i, v) for i in map(str, range(1, 355)) for v in VGS if v not in out[i]["flavor"]]
    print(f"cached {len(out)} moves; missing wordings: {missing if missing else 'NONE'}")


if __name__ == "__main__":
    main()
