# -*- coding: utf-8 -*-
"""Pokédex Plus — hand-written bilingual (EN/FA) special ways to obtain
Pokémon in the Gen-3 Hoenn games, consumed by tools/build-locations-gen3.py.

Every entry is verified against the pret disassemblies (map scripts, npc
trade tables, roamer code, setwildbattle levels) — see the phase-5 notes in
tools/gen3-plan.md.  m = [(dex, level)] (level None = trade: the received
mon matches the level of the mon you give).  v = games it applies to.
k = starter / egg / gift / fossil / trade / static / roamer / event.
"""

SPECIALS = [
    # -------- starters --------
    {
        "m": [[252, 5], [255, 5], [258, 5]], "v": ["ruby", "sapphire", "emerald"],
        "k": "starter", "loc": "MAPSEC_LITTLEROOT_TOWN",
        "d": {"en": "Pick one of Professor Birch's starters in his lab after he is chased up Route 101 — TREECKO, TORCHIC or MUDKIP, all Lv 5.",
              "fa": "بعد از اینکه پروفسور برچ را در مسیر ۱۰۱ نجات می‌دهید، در آزمایشگاهش یکی از سه استارتر را انتخاب کنید — تری‌کو، تورچیک یا مادکیپ، همه سطح ۵."},
    },
    # -------- eggs & gifts --------
    {
        "m": [[360, 5]], "v": ["ruby", "sapphire", "emerald"],
        "k": "egg", "loc": "MAPSEC_LAVARIDGE_TOWN",
        "d": {"en": "The old lady by the hot springs hands you an egg — it hatches into WYNAUT.",
              "fa": "پیرزنی کنار چشمه‌های آب گرم یک تخم به شما می‌دهد — از آن وای‌نات بیرون می‌آید."},
    },
    {
        "m": [[351, 25]], "v": ["ruby", "sapphire", "emerald"],
        "k": "gift", "loc": "MAPSEC_ROUTE_119",
        "d": {"en": "Drive Team Aqua/Magma out of the Weather Institute and the scientists reward you with a Lv 25 CASTFORM holding Mystic Water.",
              "fa": "تیم آکوا/ماگما را از مؤسسه‌ی هواشناسی بیرون کنید؛ دانشمندان به پاداش یک کَست‌فرم سطح ۲۵ با «آب عرفانی» می‌دهند."},
    },
    {
        "m": [[374, 5]], "v": ["ruby", "sapphire", "emerald"],
        "k": "gift", "loc": "MAPSEC_MOSSDEEP_CITY",
        "d": {"en": "After becoming Champion, a Poké Ball in Steven's house in Mossdeep City holds a Lv 5 BELDUM.",
              "fa": "بعد از قهرمان شدن، یک توال پوکمون در خانه‌ی استیون در شهر موس‌دیپ یک بلدوم سطح ۵ نگه می‌دارد."},
    },
    # -------- fossils --------
    {
        "m": [[346, 20], [347, 20]], "v": ["ruby", "sapphire"],
        "k": "fossil", "loc": "MAPSEC_RUSTBORO_CITY",
        "d": {"en": "Dig up the ROOT FOSSIL or CLAW FOSSIL in the Route 111 desert — you can keep only one. Devon Corporation revives it into LILEEP or ANORITH (Lv 20).",
              "fa": "در بیابان مسیر ۱۱۱ فسیل ریشه یا فسیل چنگال را بیرون بیاورید — فقط می‌توانید یکی را نگه دارید. شرکت دولِتن آن را به لیلیپ یا آنوریث (سطح ۲۰) زنده می‌کند."},
    },
    {
        "m": [[346, 20], [347, 20]], "v": ["emerald"],
        "k": "fossil", "loc": "MAPSEC_RUSTBORO_CITY",
        "d": {"en": "Mirage Tower (Route 111) holds both fossils; the one you skip later rests in the Desert Underpass. Devon Corp revives them into LILEEP / ANORITH (Lv 20).",
              "fa": "برج سراب (مسیر ۱۱۱) هر دو فسیل را دارد؛ فسیلی که برندارید بعداً در گذرگاه زیر بیابان می‌رود. شرکت دولِتن آن را به لیلیپ/آنوریث (سطح ۲۰) زنده می‌کند."},
    },
    # -------- in-game trades (gIngameTrades) --------
    {
        "m": [[296, None]], "v": ["ruby", "sapphire"],
        "k": "trade", "loc": "MAPSEC_RUSTBORO_CITY",
        "d": {"en": "A trainer in a Rustboro City house wants a SLAKOTH and gives MAKUHITA in return (it joins at your Slakoth's level, holding an X Attack).",
              "fa": "مربی‌ای در خانه‌ای در شهر رستبورو اسلاکوت می‌خواهد و در ازای آن ماکوهیتا می‌دهد (هم‌سطح اسلاکوت شما می‌آید و با «حمله‌ی X»)."},
    },
    {
        "m": [[300, None]], "v": ["ruby", "sapphire"],
        "k": "trade", "loc": "MAPSEC_FORTREE_CITY",
        "d": {"en": "In a Fortree City house, DARRELL trades her SKITTY for a PIKACHU (same level, holding Glitter Mail).",
              "fa": "در خانه‌ای در شهر فورتری، دارل اسکیت‌ی خود را با پیکاچو شما عوض می‌کند (هم‌سطح، با نامه‌ی براق)."},
    },
    {
        "m": [[222, None]], "v": ["ruby", "sapphire"],
        "k": "trade", "loc": "MAPSEC_PACIFIDLOG_TOWN",
        "d": {"en": "In a Pacifidlog Town house, LANE trades her CORSOLA for a BELLOSSOM (same level, holding Tropic Mail).",
              "fa": "در خانه‌ای در شهرک پاسیفیدلاگ، لِین کورسولای خود را با بلوسام شما عوض می‌کند (هم‌سطح، با نامه‌ی استوایی)."},
    },
    {
        "m": [[273, None]], "v": ["emerald"],
        "k": "trade", "loc": "MAPSEC_RUSTBORO_CITY",
        "d": {"en": "In a Rustboro City house, KOBE trades his SEEDOT for a RALTS (same level, holding a Chesto Berry).",
              "fa": "در خانه‌ای در شهر رستبورو، کوبه سیدوت خود را با رالتس شما عوض می‌کند (هم‌سطح، با یک توت چستو)."},
    },
    {
        "m": [[311, None]], "v": ["emerald"],
        "k": "trade", "loc": "MAPSEC_FORTREE_CITY",
        "d": {"en": "In a Fortree City house, ROMAN trades his PLUSLE for a VOLBEAT (same level, holding Wood Mail).",
              "fa": "در خانه‌ای در شهر فورتری، رومن پلاسل خود را با ولبیت شما عوض می‌کند (هم‌سطح، با نامه‌ی چوبی)."},
    },
    {
        "m": [[116, None]], "v": ["emerald"],
        "k": "trade", "loc": "MAPSEC_PACIFIDLOG_TOWN",
        "d": {"en": "In a Pacifidlog Town house, SKYLAR trades his HORSEA for a BAGON (same level, holding Wave Mail).",
              "fa": "در خانه‌ای در شهرک پاسیفیدلاگ، اسکایلر هورسای خود را با بگون شما عوض می‌کند (هم‌سطح، با نامه‌ی موج)."},
    },
    {
        "m": [[52, None]], "v": ["emerald"],
        "k": "trade", "loc": "MAPSEC_BATTLE_FRONTIER",
        "d": {"en": "In the Battle Frontier's lounge, a trainer trades her MEOWTH for a SKITTY (same level, holding Retro Mail).",
              "fa": "در لانژ مرز نبرد، مربی‌ای مئووت خود را با اسکیت‌ی شما عوض می‌کند (هم‌سطح، با نامه‌ی باستانی)."},
    },
    # -------- static battles (setwildbattle, from the map scripts) --------
    {
        # wild_encounter.c: FishingWildEncounter() — CheckFeebas() rolls 50%
        # inside one of 6 hidden tiles (seeded by the Dewford trend) and
        # serves sWildFeebas {20, 25, SPECIES_FEEBAS}; Feebas is NOT in the
        # regular fishing tables of any game.
        "m": [[349, 20]], "v": ["ruby", "sapphire", "emerald"],
        "k": "static", "loc": "MAPSEC_ROUTE_119",
        "d": {"en": "FEEBAS (Lv 20–25) hides in 6 random fishing tiles of this route — 50% bite chance inside a good tile; the tiles reshuffle when the Dewford trendy phrase changes.",
              "fa": "فِیباس (سطح ۲۰–۲۵) در ۶ خانه‌ی ماهیگیری تصادفی این مسیر پنهان است — شانس قلاب‌خوردن ۵۰٪ داخل خانه‌ی خوب؛ با تغییر جمله‌ی مد دولفورد، خانه‌ها جابه‌جا می‌شوند."},
    },
    {
        "m": [[101, 30], [101, 30]], "v": ["ruby"],
        "k": "static", "loc": "MAPSEC_AQUA_HIDEOUT",
        "d": {"en": "Two Lv 30 ELECTRODE stand guard inside the Aqua Hideout's storeroom (B1F) — beat or catch them.",
              "fa": "دو الکترود سطح ۳۰ نگهبان انبار مخفیگاه آکوا هستند (زیرزمین ۱) — آن‌ها را شکست بدهید یا بگیرید."},
    },
    {
        "m": [[101, 30], [101, 30]], "v": ["sapphire"],
        "k": "static", "loc": "MAPSEC_MAGMA_HIDEOUT",
        "d": {"en": "Two Lv 30 ELECTRODE stand guard inside the Magma Hideout's storeroom — beat or catch them.",
              "fa": "دو الکترود سطح ۳۰ نگهبان انبار مخفیگاه ماگما هستند — آن‌ها را شکست بدهید یا بگیرید."},
    },
    {
        "m": [[101, 30], [101, 30]], "v": ["emerald"],
        "k": "static", "loc": "MAPSEC_AQUA_HIDEOUT",
        "d": {"en": "Two Lv 30 ELECTRODE stand guard inside the Aqua Hideout's storeroom (B1F) — beat or catch them.",
              "fa": "دو الکترود سطح ۳۰ نگهبان انبار مخفیگاه آکوا هستند (زیرزمین ۱) — آن‌ها را شکست بدهید یا بگیرید."},
    },
    {
        "m": [[81, 25], [81, 25], [81, 25]], "v": ["ruby", "sapphire", "emerald"],
        "k": "static", "loc": "MAPSEC_NEW_MAUVILLE",
        "d": {"en": "Three Lv 25 VOLTORB pose as generators inside New Mauville — don't mistake them for machines.",
              "fa": "سه ولتورب سطح ۲۵ در نقش ژنراتور در نیو موویل ایستاده‌اند — آن‌ها را با ماشین اشتباه نگیرید."},
    },
    {
        "m": [[352, 30]], "v": ["ruby", "sapphire", "emerald"],
        "k": "static", "loc": "MAPSEC_ROUTE_120",
        "d": {"en": "An invisible KECLEON (Lv 30) blocks the path — the Devon Scope reveals it.",
              "fa": "یک ککلئون نامرئی (سطح ۳۰) جاده را بسته — دامنه‌ی دولِتن آن را آشکار می‌کند."},
    },
    {
        "m": [[185, 40]], "v": ["emerald"],
        "k": "static", "loc": "MAPSEC_BATTLE_FRONTIER",
        "d": {"en": "A Lv 40 SUDOWOODO blocks the path to the Battle Frontier — water it with the Wailmer Pail to start the battle.",
              "fa": "یک سودووودو سطح ۴۰ راه مرز نبرد را بسته — با «سطل وایلمر» آبش بدهید تا نبرد شروع شود."},
    },
    # -------- legendaries (authentic per-game levels) --------
    {
        "m": [[383, 45]], "v": ["ruby"],
        "k": "static", "loc": "MAPSEC_CAVE_OF_ORIGIN",
        "d": {"en": "Maxie awakens GROUDON on Mt. Chimney and the drought ends here: GROUDON (Lv 45) waits at the bottom of the Cave of Origin (B4F) in Sootopolis City.",
              "fa": "مکسی گراودون را در کوه دودکش بیدار می‌کند و خشکسالی اینجا تمام می‌شود: گراودون (سطح ۴۵) در ته غار سرچشمه (زیرزمین ۴) در شهر سووتوپلیس منتظر است."},
    },
    {
        "m": [[382, 45]], "v": ["sapphire"],
        "k": "static", "loc": "MAPSEC_CAVE_OF_ORIGIN",
        "d": {"en": "Archie awakens KYOGRE on Mt. Chimney and the downpour ends here: KYOGRE (Lv 45) waits at the bottom of the Cave of Origin (B4F) in Sootopolis City.",
              "fa": "آرچی کایوگر را در کوه دودکش بیدار می‌کند و باران بی‌پایان اینجا تمام می‌شود: کایوگر (سطح ۴۵) در ته غار سرچشمه (زیرزمین ۴) در شهر سووتوپلیس منتظر است."},
    },
    {
        "m": [[383, 70]], "v": ["emerald"],
        "k": "static", "loc": "MAPSEC_TERRA_CAVE",
        "d": {"en": "After the weather crisis, GROUDON (Lv 70) rests deep in TERRA CAVE — the entrance appears on Route 114 or Route 115 wherever the weatherman's report places it.",
              "fa": "بعد از بحران آب‌وهوا، گراودون (سطح ۷۰) در عمق غار زمینی آرمیده — ورودی غار بسته به گزارش هواشناسی در مسیر ۱۱۴ یا مسیر ۱۱۵ ظاهر می‌شود."},
    },
    {
        "m": [[382, 70]], "v": ["emerald"],
        "k": "static", "loc": "MAPSEC_MARINE_CAVE",
        "d": {"en": "After the weather crisis, KYOGRE (Lv 70) rests deep in MARINE CAVE — dive where the weatherman's report places it (Route 105 or Route 106).",
              "fa": "بعد از بحران آب‌وهوا، کایوگر (سطح ۷۰) در عمق غار دریایی آرمیده — بسته به گزارش هواشناسی در مسیر ۱۰۵ یا مسیر ۱۰۶ شیرجه بزنید."},
    },
    {
        "m": [[384, 70]], "v": ["ruby", "sapphire", "emerald"],
        "k": "static", "loc": "MAPSEC_SKY_PILLAR",
        "d": {"en": "RAYQUAZA (Lv 70) sleeps at the top of Sky Pillar. R/S: it ends the Sootopolis duel; Emerald: after waking it, climb Sky Pillar again to face it.",
              "fa": "رایکوازا (سطح ۷۰) در بالای ستون آسمان خوابیده. در رابی/سافایر نبرد سووتوپلیس را تمام می‌کند؛ در امرالد بعد از بیدار کردنش دوباره از ستون آسمان بالا بروید."},
    },
    {
        "m": [[377, 40]], "v": ["ruby", "sapphire", "emerald"],
        "k": "static", "loc": "MAPSEC_DESERT_RUINS",
        "d": {"en": "Read the braille in the Sealed Chamber (underwater Route 134), then the Desert Ruins on Route 111 open — REGIROCK (Lv 40) inside; walk the pattern the wall describes.",
              "fa": "خط بریل اتاقک مهرشده را بخوانید (زیر آبِ مسیر ۱۳۴) تا ویرانه‌های بیابان در مسیر ۱۱۱ باز شوند — رگی‌راک (سطح ۴۰) درون است؛ الگوی روی دیوار را بپیمایید."},
    },
    {
        "m": [[378, 40]], "v": ["ruby", "sapphire", "emerald"],
        "k": "static", "loc": "MAPSEC_ISLAND_CAVE",
        "d": {"en": "After the Sealed Chamber's braille, the Island Cave on Route 105 opens — REGICE (Lv 40) inside; circle the room as the wall instructs.",
              "fa": "بعد از خط بریل اتاقک مهرشده، غار جزیره در مسیر ۱۰۵ باز می‌شود — رگی‌ایس (سطح ۴۰) درون است؛ طبق دستور دیوار دور اتاق بچرخید."},
    },
    {
        "m": [[379, 40]], "v": ["ruby", "sapphire", "emerald"],
        "k": "static", "loc": "MAPSEC_ANCIENT_TOMB",
        "d": {"en": "After the Sealed Chamber's braille, the Ancient Tomb on Route 120 opens — REGISTEEL (Lv 40) inside; use FLASH exactly as the wall describes.",
              "fa": "بعد از خط بریل اتاقک مهرشده، آرامگاه باستانی در مسیر ۱۲۰ باز می‌شود — رگی‌استیل (سطح ۴۰) درون است؛ درست مثل نوشته‌ی دیوار از «فلش» استفاده کنید."},
    },
    # -------- roaming Latias/Latios --------
    {
        "m": [[381, 40]], "v": ["ruby"], "note": "roam",
        "k": "roamer",
        "d": {"en": "After the TV broadcast, LATIOS (Lv 40) roams every road of Hoenn — it flees each turn; the other twin waits on the Southern Island.",
              "fa": "بعد از پخش تلویزیونی، لاتیوس (سطح ۴۰) در همه‌ی راه‌های هوئن می‌گردد — هر نوبت فرار می‌کند؛ همزادش در جزیره‌ی جنوبی منتظر است."},
    },
    {
        "m": [[380, 40]], "v": ["sapphire"], "note": "roam",
        "k": "roamer",
        "d": {"en": "After the TV broadcast, LATIAS (Lv 40) roams every road of Hoenn — it flees each turn; the other twin waits on the Southern Island.",
              "fa": "بعد از پخش تلویزیونی، لاتیاس (سطح ۴۰) در همه‌ی راه‌های هوئن می‌گردد — هر نوبت فرار می‌کند؛ همزادش در جزیره‌ی جنوبی منتظر است."},
    },
    {
        "m": [[380, 40]], "v": ["emerald"], "note": "roam",
        "k": "roamer",
        "d": {"en": "After becoming Champion, answer Mom's call with \"RED\" — LATIAS (Lv 40) roams all of Hoenn.",
              "fa": "بعد از قهرمان شدن، به تماس مامان «قرمز» جواب بدهید — لاتیاس (سطح ۴۰) در تمام هوئن می‌گردد."},
    },
    {
        "m": [[381, 40]], "v": ["emerald"], "note": "roam",
        "k": "roamer",
        "d": {"en": "After becoming Champion, answer Mom's call with \"BLUE\" — LATIOS (Lv 40) roams all of Hoenn.",
              "fa": "بعد از قهرمان شدن، به تماس مامان «آبی» جواب بدهید — لاتیوس (سطح ۴۰) در تمام هوئن می‌گردد."},
    },
    # -------- ticket events --------
    {
        "m": [[380, 50]], "v": ["ruby"],
        "k": "event", "loc": "MAPSEC_SOUTHERN_ISLAND",
        "d": {"en": "With the EON TICKET (event), the ferry from Lilycove sails to the Southern Island — a Lv 50 LATIAS waits beside a SOUL DEW.",
              "fa": "با «بلیط اون» (ایونت)، کشتی از لیلی‌کو به جزیره‌ی جنوبی می‌رسد — یک لاتیاس سطح ۵۰ کنار «روح شبنم» منتظر است."},
    },
    {
        "m": [[381, 50]], "v": ["sapphire"],
        "k": "event", "loc": "MAPSEC_SOUTHERN_ISLAND",
        "d": {"en": "With the EON TICKET (event), the ferry from Lilycove sails to the Southern Island — a Lv 50 LATIOS waits beside a SOUL DEW.",
              "fa": "با «بلیط اون» (ایونت)، کشتی از لیلی‌کو به جزیره‌ی جنوبی می‌رسد — یک لاتیوس سطح ۵۰ کنار «روح شبنم» منتظر است."},
    },
    {
        "m": [[380, 50], [381, 50]], "v": ["emerald"],
        "k": "event", "loc": "MAPSEC_SOUTHERN_ISLAND",
        "d": {"en": "With the EON TICKET (event), the Southern Island holds the twin you did NOT choose — Lv 50, holding a SOUL DEW.",
              "fa": "با «بلیط اون» (ایونت)، جزیره‌ی جنوبی همان همزادی را دارد که انتخاب نکردید — سطح ۵۰، با «روح شبنم»."},
    },
    {
        "m": [[386, 30]], "v": ["emerald"],
        "k": "event", "loc": "MAPSEC_BIRTH_ISLAND",
        "d": {"en": "With the AURORA TICKET (event), the ferry stops at Birth Island — solving the triangle puzzle summons DEOXYS (Lv 30, Speed forme in Emerald).",
              "fa": "با «بلیط شفق» (ایونت)، کشتی در جزیره‌ی تولد توقف می‌کند — حل معمای مثلث، دئوکسیس را می‌آورد (سطح ۳۰، فرم سرعت در امرالد)."},
    },
    {
        "m": [[151, 30]], "v": ["emerald"],
        "k": "event", "loc": "MAPSEC_FARAWAY_ISLAND",
        "d": {"en": "With the OLD SEA CHART (event), the ferry reaches Faraway Island — MEW (Lv 30) hides in its overgrown maze.",
              "fa": "با «نقشه‌ی دریای قدیمی» (ایونت)، کشتی به جزیره‌ی دورافتاده می‌رسد — مِیو (سطح ۳۰) در بوته‌زارهایش پنهان است."},
    },
    {
        "m": [[249, 70]], "v": ["emerald"],
        "k": "event", "loc": "MAPSEC_NAVEL_ROCK",
        "d": {"en": "With the MYSTIC TICKET (event), the dive path of Navel Rock ends in a chamber holding LUGIA (Lv 70).",
              "fa": "با «بلیط اسرارآمیز» (ایونت)، مسیر شیرجه در صخره‌ی ناول به اتاقی می‌رسد که لوگیا (سطح ۷۰) در آن است."},
    },
    {
        "m": [[250, 70]], "v": ["emerald"],
        "k": "event", "loc": "MAPSEC_NAVEL_ROCK",
        "d": {"en": "With the MYSTIC TICKET (event), the climbing path of Navel Rock ends in a chamber holding HO-OH (Lv 70).",
              "fa": "با «بلیط اسرارآمیز» (ایونت)، مسیر بالا رفتن در صخره‌ی ناول به اتاقی می‌رسد که هو-اوه (سطح ۷۰) در آن است."},
    },
]

# Emerald mass outbreaks (tv.c sPokeOutbreakSpeciesList + probability 50).
SWARMS = [
    {"id": 273, "lvl": 3,  "loc": "MAPSEC_ROUTE_102", "v": ["emerald"]},   # Seedot
    {"id": 300, "lvl": 8,  "loc": "MAPSEC_ROUTE_116", "v": ["emerald"]},   # Skitty
    {"id": 273, "lvl": 13, "loc": "MAPSEC_ROUTE_117", "v": ["emerald"]},   # Seedot
    {"id": 274, "lvl": 15, "loc": "MAPSEC_ROUTE_114", "v": ["emerald"]},   # Nuzleaf
    {"id": 273, "lvl": 25, "loc": "MAPSEC_ROUTE_120", "v": ["emerald"]},   # Seedot
]

# Per-location bilingual notes (rendered at the bottom of the loc view).
LOC_NOTES = {
    "MAPSEC_ROUTE_119": {
        "en": "FEEBAS: only 6 random fishing tiles of this route hold it (50% bite chance inside a good tile) — the tiles reshuffle when the Dewford trendy phrase changes. Max out a Feebas's beauty to evolve it into MILOTIC.",
        "fa": "فِیباس: فقط ۶ خانه‌ی تصادفی از آب‌های ماهیگیری این مسیر آن را دارند (شانس قلاب‌خوردن ۵۰٪ داخل خانه‌ی خوب) — با تغییر جمله‌ی مد دولفورد، خانه‌ها عوض می‌شوند. زیبایی فِیباس را به بیشینه برسانید تا به میلوتیک تکامل یابد.",
    },
    "MAPSEC_ALTERING_CAVE": {
        "en": "Mystery Gift (e-Reader) can replace this cave's Zubat with Mareep, Pineco, Houndour, Teddiursa, Aipom, Shuckle, Stantler or Smeargle.",
        "fa": "هدیه‌ی مرموز (ای‌ریدر) می‌تواند زوبات این غار را با مریپ، پینکو، هاوندور، تدیوسا، آیپام، شاکل، استنتلر یا اسمیرگل عوض کند.",
    },
    "MAPSEC_SHOAL_CAVE": {
        "en": "Tides: at high tide the lower rooms flood and cannot be entered — wild Pokémon live in the rooms marked \"low tide\".",
        "fa": "مد و جزر: هنگام مد، اتاق‌های پایین پر از آب می‌شوند و راه ندارند — پوکمون‌های وحشی در اتاق‌های «جزر» زندگی می‌کنند.",
    },
}
