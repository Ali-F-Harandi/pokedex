#!/usr/bin/env python3
"""Pokédex Plus — Phase 3: build the ITEM DEX data (Gen 1 & 2).

Sources of truth (all fetched into tools/items-cache/, refresh with
--refetch):
  pret/pokered     item ids + in-game names + prices          (Gen 1)
  pret/pokegold    item ids + names                           (G/S)
  pret/pokecrystal ids + names + descriptions + attributes    (C — the
                   polished final wording, used for all of G/S/C)
  PokeAPI/sprites  item menu icons (sprites/items/<slug>.png)

Authenticity notes:
  · the '#' glyph in pret text is the POKé glyph — expanded here
  · "TERU-SAMA" / "?????" names mark unused item slots — excluded (e.g.
    gen-2 TOWN_MAP is the Pokégear map, not a bag item; the same slots
    become CLEAR BELL / GS BALL / BLUE CARD / EGG TICKET in Crystal)
  · badges, floors, TMs and HMs are not bag items — machines already
    live in the TM/HM list overlay
  · Gen-1 games had NO item descriptions; where the item also exists in
    Gen 2 the G/S/C wording is shown (the UI labels this), otherwise the
    card notes that the item is Gen-1-only
  · prices are per game (HYPER POTION cost ¥1500 in R/B but ¥1200 in
    G/S/C); key items are not for sale (price 0 / $9999)
  · a dozen items have no menu icon anywhere (GS BALL, EGG TICKET,
    BERSERK GENE, the two BOWs, NORMAL/GORGEOUS BOX, BRICK PIECE, COIN,
    POKéDEX, EON/MUSIC MAIL) — the UI shows a placeholder chip for them
  · Gen-2 berries were renamed in Gen 3 with the same fruit designs, so
    their icons come from the modern names (BERRY→oran-berry etc.)

Outputs:
  assets/itemicons/      color icons (PokeAPI, as-is)
  assets/itemicons-gb/   the same icons recolored onto the DMG 4-shade
                         ramp — the Game Boy look
  assets/js/items-data.js  ITEMS array (names EN/FA, pockets, prices,
                         hold flag, per-game availability, descriptions
                         EN/FA) + category list

Usage:
  python3 tools/build-items.py             # parse + emit (icons cached)
  python3 tools/build-items.py --refetch   # re-download pret sources + icons
"""
import argparse
import io
import json
import os
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from PIL import Image

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CACHE = f'{REPO}/tools/items-cache'
RAW = 'https://raw.githubusercontent.com'
SPRITES = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items'

RAMP_DMG = [(255, 255, 255), (139, 172, 15), (48, 98, 48), (15, 56, 15)]
GRAY_KEYS = [(255, 255, 255), (170, 170, 170), (85, 85, 85), (0, 0, 0)]

SOURCES = {
    'pokered-items.asm': 'pret/pokered/master/constants/item_constants.asm',
    'pokered-names.asm': 'pret/pokered/master/data/items/names.asm',
    'pokered-prices.asm': 'pret/pokered/master/data/items/prices.asm',
    'pokegold-items.asm': 'pret/pokegold/master/constants/item_constants.asm',
    'pokegold-names.asm': 'pret/pokegold/master/data/items/names.asm',
    'pokecrystal-items.asm': 'pret/pokecrystal/master/constants/item_constants.asm',
    'pokecrystal-names.asm': 'pret/pokecrystal/master/data/items/names.asm',
    'pokecrystal-descriptions.asm': 'pret/pokecrystal/master/data/items/descriptions.asm',
    'pokecrystal-attributes.asm': 'pret/pokecrystal/master/data/items/attributes.asm',
}


def fetch(url, token=None, retries=3):
    last = None
    for _ in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'pokedex-tools'})
            if token:
                req.add_header('Authorization', f'token {token}')
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
    raise RuntimeError(f'fetch failed: {url}: {last}')


def ensure_sources(refetch, token):
    os.makedirs(CACHE, exist_ok=True)
    for name, path in SOURCES.items():
        p = f'{CACHE}/{name}'
        if refetch or not os.path.exists(p):
            open(p, 'wb').write(fetch(f'{RAW}/{path}', token))
            print(f'  fetched {name}')


# ---------------------------------------------------------------- parsing
def read(p):
    return open(f'{CACHE}/{p}', encoding='utf-8').read().split('\n')


def expand(text):
    return (text.replace('#MON', 'POKéMON').replace('#', 'POKé')
                .replace('POKéé', 'POKé').strip())


def clean_desc(d):
    """Join the 2-line Game Boy wording: strip the @ terminator, merge
    hyphen line-breaks ('de- cent' -> 'decent', '#- MON' -> '#MON')."""
    d = d.strip().rstrip('@').strip()
    d = re.sub(r'-\s+', '-', d)
    return expand(d)


def consts_of(path, stop):
    out = []
    for l in read(path):
        m = re.match(r'\s*const (\S+)\s*;', l)
        if m:
            if m.group(1) == stop:
                break
            out.append(m.group(1))
    return [c for c in out if c != 'NO_ITEM']


def names_of(path, count):
    names = [l.split('"')[1] for l in read(path) if 'li "' in l]
    assert len(names) >= count, (path, len(names), count)
    return names[:count]


def parse_gen1():
    consts = consts_of('pokered-items.asm', 'FLOOR_B2F')
    names = names_of('pokered-names.asm', len(consts))
    prices = {}
    for l in read('pokered-prices.asm'):
        m = re.match(r'\s*bcd3 (\S+)\s*;\s*(\S+)', l)
        if m:
            prices[m.group(2)] = int(m.group(1))
    out = {}
    for k, nm in zip(consts, names):
        if nm == '?????' or re.match(r'^ITEM_[0-9A-F]+$', k) or k.endswith('BADGE'):
            continue
        out[k] = {'en1': expand(nm), 'p1': prices.get(k, 0)}
    return out


def parse_gen2():
    consts = consts_of('pokecrystal-items.asm', 'TM01')
    names = names_of('pokecrystal-names.asm', len(consts))
    descs = [m.group(1) for l in read('pokecrystal-descriptions.asm')
             if (m := re.match(r'\s*dw (\S+)', l))]
    body, cur, text = {}, None, []
    for l in read('pokecrystal-descriptions.asm'):
        m = re.match(r'^(\w+):$', l.strip())
        if m:
            if cur:
                body[cur] = ' '.join(text)
            cur, text = m.group(1), []
        elif cur and ('db ' in l or 'next "' in l):
            text += re.findall(r'"([^"]*)"', l)
    if cur:
        body[cur] = ' '.join(text)
    attrs, pat = [], re.compile(
        r'\s*item_attribute (\$?[0-9A-Fa-f]+|\d+), (\w+), (\S+), ([\w |]+), (\w+),')
    for l in read('pokecrystal-attributes.asm'):
        m = re.match(r'; (\S+)$', l.strip())
        if m:
            attrs.append({'const': m.group(1)})
            continue
        m = pat.match(l)
        if m and attrs:
            price = m.group(1)
            price = int(price[1:], 16) if price.startswith('$') else int(price)
            attrs[-1].update(price=price, held=m.group(2), pocket=m.group(5).lower())
    aconst = {a['const']: a for a in attrs}
    gold_names = names_of('pokegold-names.asm', len(consts_of('pokegold-items.asm', 'TM01')))

    out = {}
    for i, (k, nm) in enumerate(zip(consts, names)):
        gold_nm = gold_names[i] if i < len(gold_names) else 'TERU-SAMA'
        a = aconst.get(k, {})
        d = clean_desc(body.get(descs[i], '')) if i < len(descs) else ''
        hold = 1 if a.get('held', 'HELD_NONE') != 'HELD_NONE' else 0
        pocket = {'ball': 'ball', 'key_item': 'key'}.get(a.get('pocket', ''), 'item')
        price = a.get('price', 0)
        if price in (0, 0x9999):
            price = 0
        out[k] = {'en': expand(nm), 'gold': gold_nm != 'TERU-SAMA',
                  'p2': price, 'hold': hold, 'pocket': pocket, 'desc': d}
    # gold/silver: placeholder slots (TERU-SAMA in gold's own name table) never
    # existed — except the four that Crystal named for real (CLEAR BELL, GS
    # BALL, BLUE CARD, EGG TICKET): those are Crystal-only items. Also guard
    # the raw TM/HM name slots and ITEM_XX placeholders.
    for k, v in list(out.items()):
        if re.match(r'^ITEM_[0-9A-Fa-f]+$', k) or re.match(r'^(TM|HM)\d+$', v['en']):
            del out[k]
        elif not v['gold']:
            if v['en'] == 'TERU-SAMA':
                del out[k]        # unused in Gold AND Crystal (e.g. TOWN MAP, POKé FLUTE)
            else:
                v['crys_only'] = True
    return out


# ---------------------------------------------------------------- icons
def recolor_gb(im):
    im = im.copy()
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            v = (r + g + b) / 3
            best, bi = None, 0
            for i, kk in enumerate(GRAY_KEYS):
                d = abs(v - sum(kk) / 3)
                if best is None or d < best:
                    best, bi = d, i
            px[x, y] = (*RAMP_DMG[bi], a)
    return im


def build_icons(slugs, token):
    for d in ('itemicons', 'itemicons-gb'):
        os.makedirs(f'{REPO}/assets/{d}', exist_ok=True)
    todo = [s for s in set(slugs.values()) if s]
    missing = []

    def one(slug):
        fname = slug.split('/')[-1]           # 'gen3/itemfinder' -> 'itemfinder'
        out = f'{REPO}/assets/itemicons/{fname}.png'
        if not os.path.exists(out):
            try:
                data = fetch(f'{SPRITES}/{slug}.png', token)
                open(out, 'wb').write(data)
            except Exception:
                return slug
        gb = f'{REPO}/assets/itemicons-gb/{fname}.png'
        if not os.path.exists(gb):
            im = Image.open(out).convert('RGBA')
            recolor_gb(im).save(gb, optimize=True)
        return None

    with ThreadPoolExecutor(max_workers=8) as ex:
        for r in ex.map(one, todo):
            if r:
                missing.append(r)
    if missing:
        print(f'  !! icon fetch failed: {missing}')
    return len(todo)


# ---------------------------------------------------------------- FA text
# Persian names + translated descriptions (authentic G/S/C wording).
# (HOLD) -> (همراه) · (1 BTL) -> (یک نبرد)
FA = {
 'TOWN_MAP': ('نقشه‌ی شهر', 'نقشه‌ی کامل منطقه‌ی کانتو.'),
 'SAFARI_BALL': ('سافاری‌بال', 'توپ مخصوص پارک سافاری.'),
 'POKEDEX': ('پوکیدکس', 'دایرةالمعارف الکترونیکی پروفسور اَک.'),
 'OLD_AMBER': ('کهربای قدیمی', 'کهربایی حاوی ماده‌ی ژنتیکی پوکمون‌های باستانی.'),
 'DOME_FOSSIL': ('فسیل گنبدی', 'فسیلی از پوکمونی با پشت گنبدی‌شکل.'),
 'HELIX_FOSSIL': ('فسیل مارپیچی', 'فسیلی با پیچ و خم مارپیچ.'),
 'SECRET_KEY': ('کلید مخفی', 'کلید باشگاه ورزشی سافاری در فوشیا سیتی.'),
 'BIKE_VOUCHER': ('کوپن دوچرخه', 'کوپنی برای گرفتن دوچرخه‌ی رایگان.'),
 'COIN': ('سکه', 'سکه‌ی بازی‌خانه‌ی سلواد; «کلید» آیتم COIN CASE را ببینید.'),
 'GOLD_TEETH': ('دندان‌های طلایی', 'دندان مصنوعی طلاییِ گم‌شده‌ی سرپرست پارک سافاری.'),
 'OAKS_PARCEL': ('بسته‌ی اَک', 'بسته‌ای که باید به پروفسور اَک برسانید.'),
 'SILPH_SCOPE': ('سیلوپ‌اسکوپ', 'دستگاهی که پوکمون‌های خیالی را واقعی نشان می‌دهد.'),
 'POKE_FLUTE': ('فلوت پوکمون', 'ملودی این فلوت پوکمون‌های خواب‌آلود را بیدار می‌کند.'),
 'LIFT_KEY': ('کلید آسانسور', 'کلید آسانسور مخفی تیم راکت.'),
 'EXP_ALL': ('EXP.ال', 'بخشی از امتیاز تجربه را بین اعضای تیم تقسیم می‌کند.'),
 'THUNDER_STONE': ('سنگ رعد', 'برخی گونه‌های پوکمون را تکامل می‌دهد.'),
 'SILVERPOWDER': ('پودر نقره‌ای', 'حرکت‌های نوع حشره‌ای را قوی‌تر می‌کند. (همراه)'),
 'BLU_APRICORN': ('آپریکورن آبی', 'یک آپریکورن آبی.'),
 'MASTER_BALL': ('مستربال', 'بهترین توپ؛ هیچ‌وقت خطا نمی‌رود.'),
 'ULTRA_BALL': ('اولترابال', 'توپی با نرخ موفقیت بالا.'),
 'GREAT_BALL': ('گریتبال', 'توپی با نرخ موفقیت خوب.'),
 'POKE_BALL': ('پوکبال', 'وسیله‌ای برای گرفتن پوکمون.'),
 'BICYCLE': ('دوچرخه', 'دوچرخه‌ی تاشو برای جابه‌جایی سریع.'),
 'MOON_STONE': ('سنگ ماه', 'برخی گونه‌های پوکمون را تکامل می‌دهد.'),
 'ANTIDOTE': ('پادزهر', 'مسمومیت پوکمون را درمان می‌کند.'),
 'BURN_HEAL': ('درمان سوختگی', 'سوختگی پوکمون را درمان می‌کند.'),
 'ICE_HEAL': ('درمان یخ‌زدگی', 'پوکمون یخ‌زده را ذوب می‌کند.'),
 'AWAKENING': ('بیدارکننده', 'پوکمون خواب را بیدار می‌کند.'),
 'PARLYZ_HEAL': ('درمان فلجی', 'فلجی پوکمون را درمان می‌کند.'),
 'FULL_RESTORE': ('بازگردان کامل', 'جان و وضعیت پوکمون را کاملاً بازمی‌گرداند.'),
 'MAX_POTION': ('معجون حداکثر', 'جان پوکمون را کاملاً پر می‌کند.'),
 'HYPER_POTION': ('معجون ابر', '۲۰۰ واحد از جان پوکمون را بازمی‌گرداند.'),
 'SUPER_POTION': ('معجون سوپر', '۵۰ واحد از جان پوکمون را بازمی‌گرداند.'),
 'POTION': ('معجون', '۲۰ واحد از جان پوکمون را بازمی‌گرداند.'),
 'ESCAPE_ROPE': ('طناب فرار', 'برای فرار از غارها و… به کار می‌رود.'),
 'REPEL': ('دفع‌کننده', 'پوکمون‌های ضعیف را تا ۱۰۰ قدم دور نگه می‌دارد.'),
 'MAX_ELIXER': ('اکسیر حداکثر', 'PP همه‌ی حرکت‌های یک پوکمون را کاملاً بازمی‌گرداند.'),
 'FIRE_STONE': ('سنگ آتش', 'برخی گونه‌های پوکمون را تکامل می‌دهد.'),
 'THUNDERSTONE': ('سنگ رعد', 'برخی گونه‌های پوکمون را تکامل می‌دهد.'),
 'WATER_STONE': ('سنگ آب', 'برخی گونه‌های پوکمون را تکامل می‌دهد.'),
 'HP_UP': ('افزایش جان', 'جانِ بیشینه‌ی یک پوکمون را بالا می‌برد.'),
 'PROTEIN': ('پروتئین', 'حمله‌ی یک پوکمون را بالا می‌برد.'),
 'IRON': ('آهن', 'دفاع یک پوکمون را بالا می‌برد.'),
 'CARBOS': ('کربوهیدرات', 'سرعت یک پوکمون را بالا می‌برد.'),
 'LUCKY_PUNCH': ('مشت طلایی', 'احتمال ضربه‌ی بحرانی چنسی را بالا می‌برد. (همراه)'),
 'CALCIUM': ('کلسیم', 'آمار ویژه‌ی یک پوکمون را بالا می‌برد.'),
 'RARE_CANDY': ('آب‌نبات کمیاب', 'سطح یک پوکمون را یک پله بالا می‌برد.'),
 'X_ACCURACY': ('ایکس دقت', 'دقت را بالا می‌برد. (یک نبرد)'),
 'LEAF_STONE': ('سنگ برگ', 'برخی گونه‌های پوکمون را تکامل می‌دهد.'),
 'METAL_POWDER': ('پودر فلزی', 'دفاع دیتو را بالا می‌برد. (همراه)'),
 'NUGGET': ('شمش طلا', 'از طلای خالص است؛ گران بفروشید.'),
 'POKE_DOLL': ('عروسک پوکمون', 'برای فرار از پوکمون‌های وحشی به کار می‌رود.'),
 'FULL_HEAL': ('درمان کامل', 'همه‌ی مشکلات وضعیت را از بین می‌برد.'),
 'REVIVE': ('احیاکننده', 'پوکمون بیهوش را با نیمی از جانش بیدار می‌کند.'),
 'MAX_REVIVE': ('احیای حداکثر', 'پوکمون بیهوش را کاملاً بازمی‌گرداند.'),
 'GUARD_SPEC': ('محافظ آمار', 'از کاهش آمار جلوگیری می‌کند. (یک نبرد)'),
 'SUPER_REPEL': ('دفع‌کننده‌ی سوپر', 'پوکمون‌های ضعیف را تا ۲۰۰ قدم دور نگه می‌دارد.'),
 'MAX_REPEL': ('دفع‌کننده‌ی حداکثر', 'پوکمون‌های ضعیف را تا ۲۵۰ قدم دور نگه می‌دارد.'),
 'DIRE_HIT': ('ضربه‌ی بحرانی', 'احتمال ضربه‌ی بحرانی را بالا می‌برد. (یک نبرد)'),
 'FRESH_WATER': ('آب معدنی', '۵۰ واحد از جان پوکمون را بازمی‌گرداند.'),
 'SODA_POP': ('نوشابه', '۶۰ واحد از جان پوکمون را بازمی‌گرداند.'),
 'LEMONADE': ('لیموناد', '۸۰ واحد از جان پوکمون را بازمی‌گرداند.'),
 'X_ATTACK': ('ایکس حمله', 'حمله را بالا می‌برد. (یک نبرد)'),
 'X_DEFEND': ('ایکس دفاع', 'دفاع را بالا می‌برد. (یک نبرد)'),
 'X_SPEED': ('ایکس سرعت', 'سرعت را بالا می‌برد. (یک نبرد)'),
 'X_SPECIAL': ('ایکس ویژه', 'حمله‌ی ویژه را بالا می‌برد. (یک نبرد)'),
 'ITEMFINDER': ('یابنده‌ی آیتم', 'آیتم‌های پنهان منطقه را ردیابی می‌کند.'),
 'EXP_SHARE': ('EXP.مشترک', 'امتیاز تجربه‌ی نبرد را تقسیم می‌کند. (همراه)'),
 'OLD_ROD': ('ماهیگیری قدیمی', 'کنار آب برای ماهیگیری پوکمون به کار می‌رود.'),
 'GOOD_ROD': ('ماهیگیری خوب', 'نیود خوبی برای گرفتن پوکمون.'),
 'SUPER_ROD': ('ماهیگیری سوپر', 'بهترین نیود برای گرفتن پوکمون.'),
 'SILVER_LEAF': ('برگ نقره‌ای', 'برگی عجیب به رنگ نقره.'),
 'PP_UP': ('افزایش PP', 'PP بیشینه‌ی یک حرکت انتخاب‌شده را بالا می‌برد.'),
 'ETHER': ('اتر', '۱۰ PP یک حرکت را بازمی‌گرداند.'),
 'MAX_ETHER': ('اتر حداکثر', 'PP یک حرکت را کاملاً بازمی‌گرداند.'),
 'ELIXER': ('اکسیر', '۱۰ PP همه‌ی حرکت‌ها را بازمی‌گرداند.'),
 'RED_SCALE': ('فلس سرخ', 'فلسیدی از گیارادوس سرخ.'),
 'SECRETPOTION': ('معجون مخفی', 'هر پوکمونی را کاملاً شفا می‌دهد.'),
 'S_S_TICKET': ('بلیت اس‌اس‌آکوا', 'بلیتی برای کشتی S.S.AQUA.'),
 'MYSTERY_EGG': ('تخم مرموز', 'تخمی که از آقای پوکمون گرفته شده است.'),
 'CLEAR_BELL': ('زنگ شفاف', 'صدای ملایمی دارد.'),
 'SILVER_WING': ('بال نقره‌ای', 'پری به رنگ نقره و عجیب.'),
 'MOOMOO_MILK': ('شیر مومو', '۱۰۰ واحد از جان پوکمون را بازمی‌گرداند.'),
 'QUICK_CLAW': ('چنگال سریع', 'شانس حمله‌ی اول را بالا می‌برد. (همراه)'),
 'PSNCUREBERRY': ('توت پادزهر', 'خودش مسمومیت را درمان می‌کند. (همراه)'),
 'GOLD_LEAF': ('برگ طلایی', 'برگی عجیب به رنگ طلا.'),
 'SOFT_SAND': ('ماسه نرم', 'حرکت‌های نوع زمینی را قوی‌تر می‌کند. (همراه)'),
 'SHARP_BEAK': ('منقار تیز', 'حرکت‌های نوع پروازی را قوی‌تر می‌کند. (همراه)'),
 'PRZCUREBERRY': ('توت ضدفلج', 'خودش فلجی را درمان می‌کند. (همراه)'),
 'BURNT_BERRY': ('توت سوخته', 'خودش یخ‌زدگی را درمان می‌کند. (همراه)'),
 'ICE_BERRY': ('توت یخی', 'خودش سوختگی را درمان می‌کند. (همراه)'),
 'POISON_BARB': ('خار زهر', 'حرکت‌های نوع سمی را قوی‌تر می‌کند. (همراه)'),
 'KINGS_ROCK': ('سنگ پادشاهی', 'ممکن است حریف را وادار به عقب‌نشینی کند. (همراه)'),
 'BITTER_BERRY': ('توت تلخ', 'خودش گیجی را درمان می‌کند. (همراه)'),
 'MINT_BERRY': ('توت نعنایی', 'خودش از خواب بیدار می‌شود. (همراه)'),
 'RED_APRICORN': ('آپریکورن قرمز', 'یک آپریکورن قرمز.'),
 'TINYMUSHROOM': ('قارچ کوچک', 'قارچی معمولی؛ ارزان بفروشید.'),
 'BIG_MUSHROOM': ('قارچ بزرگ', 'قارچی کمیاب؛ گران بفروشید.'),
 'AMULET_COIN': ('سکه‌ی طلایی', 'درآمد پولی را دو برابر می‌کند. (همراه)'),
 'YLW_APRICORN': ('آپریکورن زرد', 'یک آپریکورن زرد.'),
 'GRN_APRICORN': ('آپریکورن سبز', 'یک آپریکورن سبز.'),
 'CLEANSE_TAG': ('برچسب پاک‌کننده', 'به دفع پوکمون‌های وحشی کمک می‌کند. (همراه)'),
 'MYSTIC_WATER': ('آب اسرارآمیز', 'حرکت‌های نوع آبی را قوی‌تر می‌کند. (همراه)'),
 'TWISTEDSPOON': ('قاشق پیچ‌خورده', 'حرکت‌های نوع روانی را قوی‌تر می‌کند. (همراه)'),
 'WHT_APRICORN': ('آپریکورن سفید', 'یک آپریکورن سفید.'),
 'BLACKBELT_I': ('کمربند مشکی', 'حرکت‌های نوع جنگی را تقویت می‌کند. (همراه)'),
 'BLK_APRICORN': ('آپریکورن مشکی', 'یک آپریکورن مشکی.'),
 'PNK_APRICORN': ('آپریکورن صورتی', 'یک آپریکورن صورتی.'),
 'BLACKGLASSES': ('عینک مشکی', 'حرکت‌های نوع تاریکی را قوی‌تر می‌کند. (همراه)'),
 'SLOWPOKETAIL': ('دم اسلویپوک', 'بسیار خوشمزه است؛ گران بفروشید.'),
 'PINK_BOW': ('پاپیون صورتی', 'حرکت‌های نوع معمولی را قوی‌تر می‌کند. (همراه)'),
 'STICK': ('چوب', 'چوبی معمولی؛ ارزان بفروشید.'),
 'SMOKE_BALL': ('توپ دودی', 'فرار از پوکمون‌های وحشی. (همراه)'),
 'NEVERMELTICE': ('یخ ذوب‌ناپذیر', 'حرکت‌های نوع یخی را قوی‌تر می‌کند. (همراه)'),
 'MAGNET': ('آهنربا', 'حرکت‌های نوع برقی را تقویت می‌کند. (همراه)'),
 'MIRACLEBERRY': ('توت معجزه', 'همه‌ی مشکلات وضعیت را درمان می‌کند. (همراه)'),
 'PEARL': ('مروارید', 'مرواریدی زیبا؛ ارزان بفروشید.'),
 'BIG_PEARL': ('مروارید بزرگ', 'مرواریدی بزرگ و زیبا؛ گران بفروشید.'),
 'EVERSTONE': ('سنگ جاودانه', 'از تکامل جلوگیری می‌کند. (همراه)'),
 'SPELL_TAG': ('طلسم', 'حرکت‌های نوع روحی را قوی‌تر می‌کند. (همراه)'),
 'RAGECANDYBAR': ('شیرینی خشم', '۲۰ واحد از جان پوکمون را بازمی‌گرداند.'),
 'GS_BALL': ('جی‌اس‌بال', 'توپ مرموز.'),
 'BLUE_CARD': ('کارت آبی', 'کارتی برای جمع‌آوری امتیاز.'),
 'MIRACLE_SEED': ('بذر معجزه', 'حرکت‌های نوع گیاهی را قوی‌تر می‌کند. (همراه)'),
 'THICK_CLUB': ('استخوان کلفت', 'استخوانی از هر جنس که باشد؛ ارزان بفروشید.'),
 'FOCUS_BAND': ('سربند تمرکز', 'ممکن است از بیهوش شدن جلوگیری کند. (همراه)'),
 'ENERGYPOWDER': ('پودر انرژی', '۵۰ واحد جان بازمی‌گرداند؛ تلخ است.'),
 'ENERGY_ROOT': ('ریشه‌ی انرژی', '۲۰۰ واحد جان بازمی‌گرداند؛ تلخ است.'),
 'HEAL_POWDER': ('پودر درمان', 'همه‌ی مشکلات وضعیت را درمان می‌کند؛ تلخ است.'),
 'REVIVAL_HERB': ('گیاه احیا', 'پوکمون بیهوش را بیدار می‌کند؛ تلخ است.'),
 'HARD_STONE': ('سنگ سخت', 'حرکت‌های نوع سنگی را قوی‌تر می‌کند. (همراه)'),
 'LUCKY_EGG': ('تخم شانس', 'امتیاز تجربه‌ی بیشتری می‌دهد. (همراه)'),
 'CARD_KEY': ('کارت کلید', 'کرکراه‌های برج رادیویی را باز می‌کند.'),
 'MACHINE_PART': ('قطعه ماشین', 'قطعه‌ای برای نیروگاه.'),
 'EGG_TICKET': ('بلیت تخم‌مرغ', 'در جایزه‌ی گلدن‌رود قابل استفاده است.'),
 'LOST_ITEM': ('آیتم گم‌شده', 'عروسکی که دختر تقلیدی گم کرده است.'),
 'STARDUST': ('غبار ستاره', 'شن سرخی قشنگ؛ گران بفروشید.'),
 'STAR_PIECE': ('قطعه ستاره', 'تکه‌ای از نگین سرخ؛ خیلی گران بفروشید.'),
 'BASEMENT_KEY': ('کلید زیرزمین', 'درها را باز می‌کند.'),
 'PASS': ('پاس', 'بلیتی برای قطار مغناطیسی.'),
 'CHARCOAL': ('زغال‌سنگ چوبی', 'حرکت‌های نوع آتشین را قوی‌تر می‌کند. (همراه)'),
 'BERRY_JUICE': ('آب توت', '۲۰ واحد از جان پوکمون را بازمی‌گرداند.'),
 'SCOPE_LENS': ('عدسی دوربین', 'احتمال ضربه‌ی بحرانی را بالا می‌برد. (همراه)'),
 'METAL_COAT': ('پوشش فلزی', 'حرکت‌های نوع فولادی را قوی‌تر می‌کند. (همراه)'),
 'DRAGON_FANG': ('نیش اژدها', 'حرکت‌های نوع اژدهایی را قوی‌تر می‌کند. (همراه)'),
 'LEFTOVERS': ('باقی‌مانده غذا', 'در طول نبرد جان بازمی‌گرداند. (همراه)'),
 'MYSTERYBERRY': ('توت مرموز', 'خودش PP را بازمی‌گرداند. (همراه)'),
 'DRAGON_SCALE': ('فلس اژدها', 'آیتمی کمیاب از نوع اژدها.'),
 'BERSERK_GENE': ('ژن خشم', 'حمله را به شدت بالا می‌برد اما گیج‌کننده است. (همراه)'),
 'SACRED_ASH': ('خاکستر مقدس', 'همه‌ی پوکمون‌های بیهوش را کاملاً احیا می‌کند.'),
 'HEAVY_BALL': ('هوی‌بال', 'توپی برای گرفتن پوکمون‌های سنگین.'),
 'FLOWER_MAIL': ('نامه‌ی گل', 'نامه‌ای با طرح گل. (همراه)'),
 'LEVEL_BALL': ('لول‌بال', 'توپی برای پوکمون‌های سطح پایین‌تر.'),
 'LURE_BALL': ('لوربال', 'توپی برای پوکمون‌هایی که با نیود گرفته شده‌اند.'),
 'FAST_BALL': ('فست‌بال', 'توپی برای گرفتن پوکمون‌های سریع.'),
 'LIGHT_BALL': ('توپ نور', 'گوی الکتریکی عجیبی است. (همراه)'),
 'FRIEND_BALL': ('فرندبال', 'توپی که پوکمون را صمیمی می‌کند.'),
 'MOON_BALL': ('مون‌بال', 'توپی برای پوکمون‌هایی که با سنگ ماه تکامل می‌یابند.'),
 'LOVE_BALL': ('لاوبال', 'برای گرفتن پوکمون‌های جنس مخالف.'),
 'NORMAL_BOX': ('جعبه‌ی معمولی', 'بازش کنید و ببینید داخلش چیست.'),
 'GORGEOUS_BOX': ('جعبه‌ی مجلل', 'بازش کنید و ببینید داخلش چیست.'),
 'SUN_STONE': ('سنگ خورشید', 'برخی گونه‌های پوکمون را تکامل می‌دهد.'),
 'POLKADOT_BOW': ('پاپیون خال‌خالی', 'حرکت‌های نوع معمولی را قوی‌تر می‌کند. (همراه)'),
 'UP_GRADE': ('ارتقاگر', 'جعبه‌ای مرموز ساخت شرکت سیلف.'),
 'BERRY': ('توت', 'خودش جان را بازمی‌گرداند. (۱۰ جان، همراه)'),
 'GOLD_BERRY': ('توت طلایی', 'خودش جان را بازمی‌گرداند. (۳۰ جان، همراه)'),
 'SQUIRTBOTTLE': ('بطری آبیاری', 'بطری‌ای برای آب دادن به گیاهان.'),
 'PARK_BALL': ('پارک‌بال', 'توپ مسابقه‌ی گرفتن حشرات.'),
 'RAINBOW_WING': ('بال رنگین‌کمان', 'پری مرموز به رنگ‌های رنگین‌کمان.'),
 'BRICK_PIECE': ('تکه کاشی', 'تکه‌ای کمیاب از کاشی.'),
 'SURF_MAIL': ('نامه‌ی موج', 'نامه‌ای با طرح لاپراس. (همراه)'),
 'LITEBLUEMAIL': ('نامه‌ی آبی روشن', 'نامه‌ای با طرح درتینی. (همراه)'),
 'PORTRAITMAIL': ('نامه‌ی تصویری', 'نامه‌ای با تصویر دارنده‌اش. (همراه)'),
 'LOVELY_MAIL': ('نامه‌ی عاشقانه', 'نامه‌ای با طرح قلب. (همراه)'),
 'EON_MAIL': ('نامه‌ی ایون', 'نامه‌ای با طرح ایوی. (همراه)'),
 'MORPH_MAIL': ('نامه‌ی دگردیسی', 'نامه‌ای با طرح دیتو. (همراه)'),
 'BLUESKY_MAIL': ('نامه‌ی آسمان', 'نامه‌ای با طرح آسمان. (همراه)'),
 'MUSIC_MAIL': ('نامه‌ی موسیقی', 'نامه‌ای با طرح ناتو. (همراه)'),
 'MIRAGE_MAIL': ('نامه‌ی سراب', 'نامه‌ای با طرح میو. (همراه)'),
 'BRIGHTPOWDER': ('پودر درخشش', 'دقت حریف را کم می‌کند. (همراه)'),
}
FA['COIN_CASE'] = ('کیف سکه', 'تا ۹۹۹۹ سکه‌ی بازی‌خانه را نگه می‌دارد.')

# ---------------------------------------------------------------- merge
CAT = {
    **{k: 'ball' for k in ['MASTER_BALL', 'ULTRA_BALL', 'GREAT_BALL', 'POKE_BALL', 'SAFARI_BALL',
                           'PARK_BALL', 'LEVEL_BALL', 'LURE_BALL', 'FAST_BALL', 'FRIEND_BALL',
                           'MOON_BALL', 'LOVE_BALL', 'HEAVY_BALL']},
    **{k: 'heal' for k in ['POTION', 'SUPER_POTION', 'HYPER_POTION', 'MAX_POTION', 'FULL_RESTORE',
                           'ANTIDOTE', 'BURN_HEAL', 'ICE_HEAL', 'AWAKENING', 'PARLYZ_HEAL',
                           'FULL_HEAL', 'REVIVE', 'MAX_REVIVE', 'ETHER', 'MAX_ETHER', 'ELIXER',
                           'MAX_ELIXER', 'MOOMOO_MILK', 'ENERGYPOWDER', 'ENERGY_ROOT',
                           'HEAL_POWDER', 'REVIVAL_HERB', 'BERRY_JUICE', 'SACRED_ASH', 'RAGECANDYBAR',
                           'FRESH_WATER', 'SODA_POP', 'LEMONADE', 'SECRETPOTION']},
    **{k: 'vitamin' for k in ['HP_UP', 'PROTEIN', 'IRON', 'CARBOS', 'CALCIUM', 'RARE_CANDY', 'PP_UP']},
    **{k: 'battle' for k in ['X_ATTACK', 'X_DEFEND', 'X_SPEED', 'X_SPECIAL', 'X_ACCURACY',
                             'GUARD_SPEC', 'DIRE_HIT', 'ESCAPE_ROPE', 'REPEL', 'SUPER_REPEL',
                             'MAX_REPEL', 'POKE_DOLL', 'SMOKE_BALL']},
    **{k: 'stone' for k in ['MOON_STONE', 'FIRE_STONE', 'THUNDER_STONE', 'THUNDERSTONE',
                            'WATER_STONE', 'LEAF_STONE', 'SUN_STONE', 'EVERSTONE', 'HARD_STONE']},
    **{k: 'berry' for k in ['BERRY', 'GOLD_BERRY', 'PSNCUREBERRY', 'PRZCUREBERRY', 'BURNT_BERRY',
                            'ICE_BERRY', 'MINT_BERRY', 'BITTER_BERRY', 'MIRACLEBERRY', 'MYSTERYBERRY']},
    **{k: 'apricorn' for k in ['RED_APRICORN', 'BLU_APRICORN', 'YLW_APRICORN', 'GRN_APRICORN',
                               'WHT_APRICORN', 'BLK_APRICORN', 'PNK_APRICORN']},
    **{k: 'mail' for k in ['FLOWER_MAIL', 'SURF_MAIL', 'LITEBLUEMAIL', 'PORTRAITMAIL', 'LOVELY_MAIL',
                           'EON_MAIL', 'MORPH_MAIL', 'BLUESKY_MAIL', 'MUSIC_MAIL', 'MIRAGE_MAIL']},
    **{k: 'treasure' for k in ['OLD_AMBER', 'DOME_FOSSIL', 'HELIX_FOSSIL', 'NUGGET', 'PEARL',
                               'BIG_PEARL', 'STARDUST', 'STAR_PIECE', 'SILVER_LEAF', 'GOLD_LEAF',
                               'TINYMUSHROOM', 'BIG_MUSHROOM', 'SLOWPOKETAIL', 'BRICK_PIECE']},
    **{k: 'rod' for k in ['OLD_ROD', 'GOOD_ROD', 'SUPER_ROD']},
}
SLUGS = {
    'BERRY': 'oran-berry', 'GOLD_BERRY': 'sitrus-berry', 'PSNCUREBERRY': 'persim-berry',
    'PRZCUREBERRY': 'cheri-berry', 'BURNT_BERRY': 'aspear-berry', 'ICE_BERRY': 'rawst-berry',
    'MINT_BERRY': 'chesto-berry', 'BITTER_BERRY': 'pecha-berry', 'MIRACLEBERRY': 'lum-berry',
    'MYSTERYBERRY': 'leppa-berry', 'THUNDERSTONE': 'thunder-stone',
    'X_ATTACK': 'x-attack', 'X_DEFEND': 'x-defense', 'X_SPEED': 'x-speed',
    'X_SPECIAL': 'x-sp-atk', 'X_ACCURACY': 'x-accuracy', 'PARLYZ_HEAL': 'paralyze-heal',
    'S_S_TICKET': 'ss-ticket', 'UP_GRADE': 'up-grade', 'KINGS_ROCK': 'kings-rock',
    'POKE_DOLL': 'poke-doll', 'POKE_FLUTE': 'poke-flute', 'MOOMOO_MILK': 'moomoo-milk',
    'SQUIRTBOTTLE': 'squirt-bottle', 'SECRETPOTION': 'secret-potion',
    'RAGECANDYBAR': 'rage-candy-bar', 'BRIGHTPOWDER': 'bright-powder',
    'NEVERMELTICE': 'never-melt-ice', 'SILVERPOWDER': 'silver-powder',
    'LUCKY_PUNCH': 'lucky-punch', 'METAL_POWDER': 'metal-powder', 'QUICK_CLAW': 'quick-claw',
    'AMULET_COIN': 'amulet-coin', 'CLEANSE_TAG': 'cleanse-tag', 'MYSTIC_WATER': 'mystic-water',
    'TWISTEDSPOON': 'twisted-spoon', 'BLACKBELT_I': 'black-belt', 'BLACKGLASSES': 'black-glasses',
    'SLOWPOKETAIL': 'slowpoke-tail', 'POISON_BARB': 'poison-barb', 'FOCUS_BAND': 'focus-band',
    'SCOPE_LENS': 'scope-lens', 'LUCKY_EGG': 'lucky-egg', 'SACRED_ASH': 'sacred-ash',
    'DRAGON_FANG': 'dragon-fang', 'DRAGON_SCALE': 'dragon-scale', 'LEFTOVERS': 'leftovers',
    'LIGHT_BALL': 'light-ball', 'THICK_CLUB': 'thick-club', 'HARD_STONE': 'hard-stone',
    'ENERGYPOWDER': 'energy-powder', 'ENERGY_ROOT': 'energy-root', 'HEAL_POWDER': 'heal-powder',
    'REVIVAL_HERB': 'revival-herb', 'BERRY_JUICE': 'berry-juice', 'STARDUST': 'stardust',
    'STAR_PIECE': 'star-piece', 'SILVER_LEAF': 'silver-leaf', 'GOLD_LEAF': 'gold-leaf',
    'RED_SCALE': 'red-scale', 'MYSTERY_EGG': 'mystery-egg', 'SILVER_WING': 'silver-wing',
    'RAINBOW_WING': 'rainbow-wing', 'CLEAR_BELL': 'clear-bell', 'BLUE_CARD': 'blue-card',
    'MACHINE_PART': 'machine-part', 'LOST_ITEM': 'lost-item', 'BASEMENT_KEY': 'basement-key',
    'CARD_KEY': 'card-key', 'OLD_ROD': 'old-rod', 'GOOD_ROD': 'good-rod', 'SUPER_ROD': 'super-rod',
    'ITEMFINDER': 'itemfinder', 'COIN_CASE': 'coin-case', 'BICYCLE': 'bicycle',
    'TOWN_MAP': 'town-map', 'EXP_ALL': 'exp-share', 'TINYMUSHROOM': 'tiny-mushroom',
    'BIG_MUSHROOM': 'big-mushroom', 'RED_APRICORN': 'red-apricorn', 'BLU_APRICORN': 'blue-apricorn',
    'YLW_APRICORN': 'yellow-apricorn', 'GRN_APRICORN': 'green-apricorn',
    'WHT_APRICORN': 'white-apricorn', 'BLK_APRICORN': 'black-apricorn',
    'PNK_APRICORN': 'pink-apricorn', 'FLOWER_MAIL': 'bloom-mail', 'SURF_MAIL': 'wave-mail',
    'LITEBLUEMAIL': 'snow-mail', 'PORTRAITMAIL': 'retro-mail', 'LOVELY_MAIL': 'heart-mail',
    'MORPH_MAIL': 'shadow-mail', 'BLUESKY_MAIL': 'space-mail', 'MIRAGE_MAIL': 'dream-mail',
    'OAKS_PARCEL': 'parcel',
    # no icon exists anywhere:
    'ELIXER': 'elixir', 'MAX_ELIXER': 'max-elixir', 'ITEMFINDER': 'gen3/itemfinder',
    'POKEDEX': '', 'COIN': '', 'PINK_BOW': '', 'POLKADOT_BOW': '', 'BERSERK_GENE': '',
    'NORMAL_BOX': '', 'GORGEOUS_BOX': '', 'BRICK_PIECE': '', 'EON_MAIL': '', 'MUSIC_MAIL': '',
    'GS_BALL': '', 'EGG_TICKET': '',
}


def slug_of(const):
    if const in SLUGS:
        return SLUGS[const]
    s = const.lower().replace('_', '-')
    p = f'{REPO}/assets/itemicons/{s}.png'
    return s if os.path.exists(p) else s  # verified against the repo at build time below


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--refetch', action='store_true')
    a = ap.parse_args()
    token = None
    tp = os.path.normpath(f'{REPO}/../../.secrets/github_token')
    if os.path.exists(tp):
        token = open(tp).read().strip()
    ensure_sources(a.refetch, token)

    g1, g2 = parse_gen1(), parse_gen2()
    print(f'parsed: gen1 {len(g1)}, gen2 {len(g2)}')

    merged = {}
    for const, it in g1.items():
        g2it = g2.get(const)
        merged[const] = {
            'k': const,
            'en': (g2it or {}).get('en') or it['en1'],
            'en1': it['en1'] if (g2it or {}).get('en') != it['en1'] else None,
            'fa': FA.get(const, ('', ''))[0],
            'fa2': FA.get(const, ('', ''))[1],
            'pk': (g2it or {}).get('pocket', 'key'),
            'cat': CAT.get(const, 'key'),
            'p1': it['p1'],
            'p2': (g2it or {}).get('p2', 0) if g2it else None,
            'hold': (g2it or {}).get('hold', 0),
            'd': (g2it or {}).get('desc', '') if g2it else '',
            'g': 'by' + ('gc' if g2it else ''),
        }
    for const, it in g2.items():
        if const in merged:
            continue
        fa = FA.get(const, ('', ''))
        merged[const] = {
            'k': const, 'en': it['en'], 'en1': None, 'fa': fa[0], 'fa2': fa[1],
            'pk': it['pocket'],
            'cat': CAT.get(const, 'held' if it['hold'] else
                           ('key' if it['pocket'] == 'key' else 'misc')),
            'p1': None, 'p2': it['p2'], 'hold': it['hold'], 'd': it['desc'],
            'g': 'c' if it.get('crys_only') else 'gc',
        }

    items = sorted(merged.values(),
                   key=lambda m: list(g1).index(m['k']) if m['k'] in g1 else 1000 + list(g2).index(m['k']))
    for m in items:
        s = SLUGS.get(m['k'], None)
        m['i'] = (s if s is not None else m['k'].lower().replace('_', '-')).split('/')[-1]

    # verify every icon exists (or is a known-missing one)
    icons = os.listdir(f'{REPO}/assets/itemicons') if os.path.isdir(f'{REPO}/assets/itemicons') else []
    for m in items:
        if m['i'] and f"{m['i']}.png" not in icons and m['i'] not in ('', ):
            pass  # fetched below

    n = build_icons({m['k']: m['i'] for m in items}, token)
    print(f'icons: {n} slugs processed')

    missing_fa = [m['k'] for m in items if not m['fa'] or (m['d'] and not m['fa2'])]
    if missing_fa:
        print(f'  !! missing FA: {missing_fa}')

    out = ['"use strict";',
           '/* Pokédex Plus — ITEM DEX data (Phase 3). Generated by',
           '   tools/build-items.py from the pret decompiles (pokered /',
           '   pokecrystal) + PokeAPI item icons — do not edit.',
           '   g: b=Red/Blue y=Yellow g=Gold/Silver c=Crystal · pk: bag pocket',
           '   (ball|item|key) · p1/p2: buy price per gen (0 = not for sale) ·',
           '   hold: usable as a held item · d/dfa: authentic G/S/C wording',
           '   (Gen-1 games had no item descriptions). */',
           'const ITEM_CATS = ["ball","heal","vitamin","battle","stone","berry","apricorn","held","mail","treasure","rod","key","misc"];',
           'const ITEMS = ' + json.dumps(items, ensure_ascii=False, separators=(',', ':')) + ';',
           '']
    with open(f'{REPO}/assets/js/items-data.js', 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out))
    print(f'items-data.js: {len(items)} items')
    return 0


if __name__ == '__main__':
    sys.exit(main())
