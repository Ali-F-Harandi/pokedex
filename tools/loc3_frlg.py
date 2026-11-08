# -*- coding: utf-8 -*-
"""Pokédex Plus — hand-written bilingual (EN/FA) data for the Gen-3
KANTO + SEVII (FireRed / LeafGreen) Location Dex, consumed by
tools/build-locations-gen3.py (phase 6).

FRLG's Kanto is a redesign of Gen 1 — its tables are parsed fresh from the
pret/pokefirered decomp; NOTHING is reused from the gen1 locations data.

LOC_NAMES_FRLG: MAPSEC id -> (en, fa, group).  Groups: route / city / cave /
forest / water / safari / island / building.  Persian digits everywhere.
ROOMS_FRLG: wild-map dir name -> (en, fa, ord) room label (None ord = a
single-map location carries no room label).  Rooms sharing a label merge
when their encounter tables are identical.
SPECIALS_FRLG: every entry verified against the pokefirered disassembly —
map scripts (givemon / setwildbattle / seteventmon levels), src/data/
ingame_trades.h, src/roamer.c.  m = [(dex, level)] (level None = trade: the
received mon matches the level of the mon you give).  v = games it applies
to.  k = starter / egg / gift / fossil / trade / static / roamer / event.
POS: hand-assigned list order (map x/y are useless for the many x=0,y=0
cave/sevii sections).
"""

LOC_NAMES_FRLG = {
    # ---------------- Kanto towns & cities ----------------
    "MAPSEC_PALLET_TOWN":       ("Pallet Town",      "شهرک پالت", "city"),
    "MAPSEC_VIRIDIAN_CITY":     ("Viridian City",    "شهر ویریدیان", "city"),
    "MAPSEC_PEWTER_CITY":       ("Pewter City",      "شهر پوئتر", "city"),
    "MAPSEC_CERULEAN_CITY":     ("Cerulean City",    "شهر سرولئان", "city"),
    "MAPSEC_LAVENDER_TOWN":     ("Lavender Town",    "شهرک لاوندر", "city"),
    "MAPSEC_VERMILION_CITY":    ("Vermilion City",   "شهر ورمیلیون", "city"),
    "MAPSEC_CELADON_CITY":      ("Celadon City",     "شهر سِلادون", "city"),
    "MAPSEC_FUCHSIA_CITY":      ("Fuchsia City",     "شهر فوکشیا", "city"),
    "MAPSEC_CINNABAR_ISLAND":   ("Cinnabar Island",  "جزیره سینابار", "city"),
    "MAPSEC_SAFFRON_CITY":      ("Saffron City",     "شهر سافرون", "city"),
    # ---------------- Kanto routes ----------------
    "MAPSEC_ROUTE_1":  ("Route 1",  "مسیر ۱",  "route"),
    "MAPSEC_ROUTE_2":  ("Route 2",  "مسیر ۲",  "route"),
    "MAPSEC_ROUTE_3":  ("Route 3",  "مسیر ۳",  "route"),
    "MAPSEC_ROUTE_4":  ("Route 4",  "مسیر ۴",  "route"),
    "MAPSEC_ROUTE_5":  ("Route 5",  "مسیر ۵",  "route"),
    "MAPSEC_ROUTE_6":  ("Route 6",  "مسیر ۶",  "route"),
    "MAPSEC_ROUTE_7":  ("Route 7",  "مسیر ۷",  "route"),
    "MAPSEC_ROUTE_8":  ("Route 8",  "مسیر ۸",  "route"),
    "MAPSEC_ROUTE_9":  ("Route 9",  "مسیر ۹",  "route"),
    "MAPSEC_ROUTE_10": ("Route 10", "مسیر ۱۰", "route"),
    "MAPSEC_ROUTE_11": ("Route 11", "مسیر ۱۱", "route"),
    "MAPSEC_ROUTE_12": ("Route 12", "مسیر ۱۲", "route"),
    "MAPSEC_ROUTE_13": ("Route 13", "مسیر ۱۳", "route"),
    "MAPSEC_ROUTE_14": ("Route 14", "مسیر ۱۴", "route"),
    "MAPSEC_ROUTE_15": ("Route 15", "مسیر ۱۵", "route"),
    "MAPSEC_ROUTE_16": ("Route 16", "مسیر ۱۶", "route"),
    "MAPSEC_ROUTE_17": ("Route 17", "مسیر ۱۷", "route"),
    "MAPSEC_ROUTE_18": ("Route 18", "مسیر ۱۸", "route"),
    "MAPSEC_ROUTE_19": ("Route 19", "مسیر ۱۹", "route"),
    "MAPSEC_ROUTE_20": ("Route 20", "مسیر ۲۰", "route"),
    "MAPSEC_ROUTE_21": ("Route 21", "مسیر ۲۱", "route"),
    "MAPSEC_ROUTE_22": ("Route 22", "مسیر ۲۲", "route"),
    "MAPSEC_ROUTE_23": ("Route 23", "مسیر ۲۳", "route"),
    "MAPSEC_ROUTE_24": ("Route 24", "مسیر ۲۴", "route"),
    "MAPSEC_ROUTE_25": ("Route 25", "مسیر ۲۵", "route"),
    # ---------------- Kanto caves & landmarks ----------------
    "MAPSEC_VIRIDIAN_FOREST":  ("Viridian Forest",   "جنگل ویریدیان", "forest"),
    "MAPSEC_MT_MOON":          ("Mt. Moon",          "کوه ماه", "cave"),
    "MAPSEC_ROCK_TUNNEL":      ("Rock Tunnel",       "تونل سنگی", "cave"),
    "MAPSEC_DIGLETTS_CAVE":    ("Diglett's Cave",    "غار دیگلت", "cave"),
    "MAPSEC_KANTO_VICTORY_ROAD": ("Victory Road",    "جاده پیروزی", "cave"),
    "MAPSEC_SEAFOAM_ISLANDS":  ("Seafoam Islands",   "جزایر سی‌فوم", "cave"),
    "MAPSEC_CERULEAN_CAVE":    ("Cerulean Cave",     "غار سرولئان", "cave"),
    "MAPSEC_POWER_PLANT":      ("Power Plant",       "نیروگاه", "building"),
    "MAPSEC_POKEMON_TOWER":    ("Pokémon Tower",     "برج پوکمون", "building"),
    "MAPSEC_POKEMON_MANSION":  ("Pokémon Mansion",   "عمارت پوکمون", "building"),
    "MAPSEC_KANTO_SAFARI_ZONE": ("Safari Zone",      "منطقه‌ی سافاری", "safari"),
    "MAPSEC_SILPH_CO":         ("Silph Co.",         "شرکت سیلف", "building"),
    "MAPSEC_S_S_ANNE":         ("S.S. Anne",         "کشتی اس‌اس اَن", "building"),
    "MAPSEC_UNDERGROUND_PATH": ("Underground Path",  "راه زیرزمینی", "building"),
    "MAPSEC_TRAINER_TOWER":    ("Trainer Tower",     "برج مربی‌ها", "building"),
    # ---------------- Sevii Islands (One–Three) ----------------
    "MAPSEC_ONE_ISLAND":      ("One Island",        "جزیره‌ی یک", "island"),
    "MAPSEC_TWO_ISLAND":      ("Two Island",        "جزیره‌ی دو", "island"),
    "MAPSEC_THREE_ISLAND":    ("Three Island",      "جزیره‌ی سه", "island"),
    "MAPSEC_KINDLE_ROAD":     ("Kindle Road",       "جاده کیندل", "island"),
    "MAPSEC_TREASURE_BEACH":  ("Treasure Beach",    "ساحل گنج", "island"),
    "MAPSEC_CAPE_BRINK":      ("Cape Brink",        "دماغه برینک", "island"),
    "MAPSEC_BOND_BRIDGE":     ("Bond Bridge",       "پل باند", "island"),
    "MAPSEC_THREE_ISLE_PORT": ("Three Isle Port",   "بندر جزیره سه", "island"),
    "MAPSEC_MT_EMBER":        ("Mt. Ember",         "کوه امبر", "cave"),
    "MAPSEC_BERRY_FOREST":    ("Berry Forest",      "جنگل توت", "forest"),
    # ---------------- Sevii Islands (Four–Seven) ----------------
    "MAPSEC_FOUR_ISLAND":     ("Four Island",       "جزیره‌ی چهار", "island"),
    "MAPSEC_FIVE_ISLAND":     ("Five Island",       "جزیره‌ی پنج", "island"),
    "MAPSEC_SIX_ISLAND":      ("Six Island",        "جزیره‌ی شش", "island"),
    "MAPSEC_SEVEN_ISLAND":    ("Seven Island",      "جزیره‌ی هفت", "island"),
    "MAPSEC_ICEFALL_CAVE":    ("Icefall Cave",      "غار آبشار یخی", "cave"),
    "MAPSEC_WATER_LABYRINTH": ("Water Labyrinth",   "هزارتوی آبی", "island"),
    "MAPSEC_RESORT_GORGEOUS": ("Resort Gorgeous",   "اقامتگاه گرجیوس", "island"),
    "MAPSEC_FIVE_ISLE_MEADOW": ("Five Isle Meadow", "چمنزار جزیره پنج", "island"),
    "MAPSEC_MEMORIAL_PILLAR": ("Memorial Pillar",   "ستون یادبود", "island"),
    "MAPSEC_OUTCAST_ISLAND":  ("Outcast Island",    "جزیره اوت‌کست", "island"),
    "MAPSEC_GREEN_PATH":      ("Green Path",        "جاده سبز", "island"),
    "MAPSEC_WATER_PATH":      ("Water Path",        "جاده آبی", "island"),
    "MAPSEC_RUIN_VALLEY":     ("Ruin Valley",       "دره‌ی ویرانه‌ها", "island"),
    "MAPSEC_LOST_CAVE":       ("Lost Cave",         "غار گمشده", "cave"),
    "MAPSEC_PATTERN_BUSH":    ("Pattern Bush",      "بوته‌زار نقش‌ها", "forest"),
    "MAPSEC_ALTERING_CAVE":   ("Altering Cave",     "غار دگردیسی", "cave"),
    "MAPSEC_DOTTED_HOLE":     ("Dotted Hole",       "حفره‌ی نقطه‌دار", "cave"),
    "MAPSEC_CANYON_ENTRANCE": ("Canyon Entrance",   "ورودی دره", "island"),
    "MAPSEC_SEVAULT_CANYON":  ("Sevault Canyon",    "دره سِوالت", "island"),
    "MAPSEC_TANOBY_RUINS":    ("Tanoby Ruins",      "ویرانه‌های تانوبی", "island"),
    # ---------------- Tanoby chambers (Unown rooms) ----------------
    "MAPSEC_MONEAN_CHAMBER":  ("Monean Chamber",    "اتاق مونه‌آن", "cave"),
    "MAPSEC_LIPTOO_CHAMBER":  ("Liptoo Chamber",    "اتاق لیپتو", "cave"),
    "MAPSEC_WEEPTH_CHAMBER":  ("Weepth Chamber",    "اتاق ویپث", "cave"),
    "MAPSEC_DILFORD_CHAMBER": ("Dilford Chamber",   "اتاق دیلفورد", "cave"),
    "MAPSEC_SCUFIB_CHAMBER":  ("Scufib Chamber",    "اتاق اسکوفیب", "cave"),
    "MAPSEC_RIXY_CHAMBER":    ("Rixy Chamber",      "اتاق ریکسی", "cave"),
    "MAPSEC_VIAPOIS_CHAMBER": ("Viapois Chamber",   "اتاق ویاپویس", "cave"),
    # ---------------- ticket events ----------------
    "MAPSEC_NAVEL_ROCK":      ("Navel Rock",        "صخره ناول", "island"),
    "MAPSEC_BIRTH_ISLAND":    ("Birth Island",      "جزیره تولد", "island"),
}

# Hand-assigned list order (map x/y collapse many x=0,y=0 sections to the
# same corner).  Kanto north-to-south, then Sevii One→Seven, then events.
POS_FRLG = {
    "MAPSEC_PALLET_TOWN": 10, "MAPSEC_ROUTE_1": 20, "MAPSEC_VIRIDIAN_CITY": 30,
    "MAPSEC_ROUTE_2": 40, "MAPSEC_VIRIDIAN_FOREST": 50, "MAPSEC_PEWTER_CITY": 60,
    "MAPSEC_ROUTE_3": 70, "MAPSEC_MT_MOON": 80, "MAPSEC_ROUTE_4": 90,
    "MAPSEC_CERULEAN_CITY": 100, "MAPSEC_ROUTE_24": 110, "MAPSEC_ROUTE_25": 120,
    "MAPSEC_CERULEAN_CAVE": 130, "MAPSEC_ROUTE_5": 140, "MAPSEC_ROUTE_6": 150,
    "MAPSEC_SAFFRON_CITY": 160, "MAPSEC_SILPH_CO": 170, "MAPSEC_ROUTE_7": 180,
    "MAPSEC_ROUTE_8": 190, "MAPSEC_ROUTE_9": 200, "MAPSEC_ROCK_TUNNEL": 210,
    "MAPSEC_ROUTE_10": 220, "MAPSEC_POWER_PLANT": 230, "MAPSEC_LAVENDER_TOWN": 240,
    "MAPSEC_POKEMON_TOWER": 250, "MAPSEC_ROUTE_11": 260, "MAPSEC_UNDERGROUND_PATH": 270,
    "MAPSEC_VERMILION_CITY": 280, "MAPSEC_S_S_ANNE": 290, "MAPSEC_DIGLETTS_CAVE": 300,
    "MAPSEC_ROUTE_12": 310, "MAPSEC_ROUTE_13": 320, "MAPSEC_ROUTE_14": 330,
    "MAPSEC_ROUTE_15": 340, "MAPSEC_FUCHSIA_CITY": 350, "MAPSEC_KANTO_SAFARI_ZONE": 360,
    "MAPSEC_ROUTE_16": 370, "MAPSEC_ROUTE_17": 380, "MAPSEC_ROUTE_18": 390,
    "MAPSEC_ROUTE_19": 400, "MAPSEC_ROUTE_20": 410, "MAPSEC_SEAFOAM_ISLANDS": 420,
    "MAPSEC_CINNABAR_ISLAND": 430, "MAPSEC_ROUTE_21": 440, "MAPSEC_POKEMON_MANSION": 450,
    "MAPSEC_ROUTE_22": 460, "MAPSEC_ROUTE_23": 470, "MAPSEC_KANTO_VICTORY_ROAD": 480,
    "MAPSEC_CELADON_CITY": 495, "MAPSEC_ONE_ISLAND": 500, "MAPSEC_KINDLE_ROAD": 510, "MAPSEC_MT_EMBER": 520,
    "MAPSEC_TREASURE_BEACH": 530, "MAPSEC_TWO_ISLAND": 540, "MAPSEC_CAPE_BRINK": 550,
    "MAPSEC_THREE_ISLAND": 560, "MAPSEC_BOND_BRIDGE": 570, "MAPSEC_THREE_ISLE_PORT": 580,
    "MAPSEC_BERRY_FOREST": 590, "MAPSEC_FOUR_ISLAND": 600, "MAPSEC_ICEFALL_CAVE": 610,
    "MAPSEC_FIVE_ISLAND": 620, "MAPSEC_WATER_LABYRINTH": 630, "MAPSEC_RESORT_GORGEOUS": 640,
    "MAPSEC_FIVE_ISLE_MEADOW": 650, "MAPSEC_MEMORIAL_PILLAR": 660, "MAPSEC_OUTCAST_ISLAND": 670,
    "MAPSEC_LOST_CAVE": 680, "MAPSEC_GREEN_PATH": 690, "MAPSEC_SIX_ISLAND": 700,
    "MAPSEC_WATER_PATH": 710, "MAPSEC_PATTERN_BUSH": 720, "MAPSEC_ALTERING_CAVE": 730,
    "MAPSEC_DOTTED_HOLE": 740, "MAPSEC_RUIN_VALLEY": 750, "MAPSEC_SEVEN_ISLAND": 760,
    "MAPSEC_CANYON_ENTRANCE": 770, "MAPSEC_SEVAULT_CANYON": 780, "MAPSEC_TANOBY_RUINS": 790,
    "MAPSEC_MONEAN_CHAMBER": 800, "MAPSEC_LIPTOO_CHAMBER": 810, "MAPSEC_WEEPTH_CHAMBER": 820,
    "MAPSEC_DILFORD_CHAMBER": 830, "MAPSEC_SCUFIB_CHAMBER": 840, "MAPSEC_RIXY_CHAMBER": 850,
    "MAPSEC_VIAPOIS_CHAMBER": 860, "MAPSEC_TRAINER_TOWER": 870,
    "MAPSEC_NAVEL_ROCK": 900, "MAPSEC_BIRTH_ISLAND": 910,
}

# wild-map dir -> (en, fa, ord).  None ord entries never occur here: every
# multi-room section below lists all of its wild dirs.
ROOMS_FRLG = {
    # Mt. Moon
    "MtMoon_1F":  ("1F",  "طبقه همکف", 1),
    "MtMoon_B1F": ("B1F", "زیرزمین ۱", 11),
    "MtMoon_B2F": ("B2F", "زیرزمین ۲", 12),
    # Mt. Ember
    "MtEmber_Exterior":        ("Outside", "بیرون کوه", 0),
    "MtEmber_SummitPath_1F":   ("Summit Path 1F", "جاده قله — همکف", 1),
    "MtEmber_SummitPath_2F":   ("Summit Path 2F", "جاده قله — طبقه ۲", 2),
    "MtEmber_SummitPath_3F":   ("Summit Path 3F", "جاده قله — طبقه ۳", 3),
    "MtEmber_RubyPath_1F":     ("Ruby Path 1F",  "جاده یاقوت — همکف", 4),
    "MtEmber_RubyPath_B1F":    ("Ruby Path B1F", "جاده یاقوت — زیرزمین ۱", 11),
    "MtEmber_RubyPath_B1F_Stairs": ("Ruby Path B1F (stairs)", "جاده یاقوت — زیرزمین ۱ (پله‌ها)", 11),
    "MtEmber_RubyPath_B2F":    ("Ruby Path B2F", "جاده یاقوت — زیرزمین ۲", 12),
    "MtEmber_RubyPath_B2F_Stairs": ("Ruby Path B2F (stairs)", "جاده یاقوت — زیرزمین ۲ (پله‌ها)", 12),
    "MtEmber_RubyPath_B3F":    ("Ruby Path B3F", "جاده یاقوت — زیرزمین ۳", 13),
    # Kanto Safari Zone
    "SafariZone_Center": ("Center", "بخش مرکزی", 1),
    "SafariZone_East":   ("East",   "بخش شرقی", 2),
    "SafariZone_North":  ("North",  "بخش شمالی", 3),
    "SafariZone_West":   ("West",   "بخش غربی", 4),
    # Kanto Victory Road
    "VictoryRoad_1F": ("1F",  "همکف", 1),
    "VictoryRoad_2F": ("2F",  "طبقه ۲", 2),
    "VictoryRoad_3F": ("3F",  "طبقه ۳", 3),
    # Rock Tunnel
    "RockTunnel_1F":  ("1F",  "همکف", 1),
    "RockTunnel_B1F": ("B1F", "زیرزمین", 11),
    # Pokémon Tower (wild floors only)
    "PokemonTower_3F": ("3F", "طبقه ۳", 3),
    "PokemonTower_4F": ("4F", "طبقه ۴", 4),
    "PokemonTower_5F": ("5F", "طبقه ۵", 5),
    "PokemonTower_6F": ("6F", "طبقه ۶", 6),
    "PokemonTower_7F": ("7F", "طبقه ۷", 7),
    # Pokémon Mansion
    "PokemonMansion_1F":  ("1F",  "همکف", 1),
    "PokemonMansion_2F":  ("2F",  "طبقه ۲", 2),
    "PokemonMansion_3F":  ("3F",  "طبقه ۳", 3),
    "PokemonMansion_B1F": ("B1F", "زیرزمین", 11),
    # Seafoam Islands
    "SeafoamIslands_1F":  ("1F",  "همکف", 1),
    "SeafoamIslands_B1F": ("B1F", "زیرزمین ۱", 11),
    "SeafoamIslands_B2F": ("B2F", "زیرزمین ۲", 12),
    "SeafoamIslands_B3F": ("B3F", "زیرزمین ۳", 13),
    "SeafoamIslands_B4F": ("B4F", "زیرزمین ۴", 14),
    # Cerulean Cave
    "CeruleanCave_1F":  ("1F",  "همکف", 1),
    "CeruleanCave_2F":  ("2F",  "طبقه ۲", 2),
    "CeruleanCave_B1F": ("B1F", "زیرزمین", 11),
    # Icefall Cave
    "FourIsland_IcefallCave_Entrance": ("Entrance", "ورودی", 0),
    "FourIsland_IcefallCave_1F":       ("1F",  "همکف", 1),
    "FourIsland_IcefallCave_B1F":      ("B1F", "زیرزمین", 11),
    "FourIsland_IcefallCave_Back":     ("Back", "انتهای غار", 20),
    # Lost Cave
    **{f"FiveIsland_LostCave_Room{i}": (f"Room {i}", f"اتاق {i}", i) for i in range(1, 15)},
    # Route 21 (sea, two halves)
    "Route21_North": ("North", "شمال", 1),
    "Route21_South": ("South", "جنوب", 2),
}

# Sections with no wild tables of their own (Saffron Dojo + museum, Silph
# Co.'s Lapras floor, the Underground Path trade, the two ticket islands)
# are pulled in automatically: the builder collects the loc anchors of
# SPECIALS_FRLG.  No hard-coded special-only set is needed here.

SPECIALS_FRLG = [
    # -------- starter (Oak's briefcase, Oak's Lab — Pallet Town) --------
    {
        "m": [[1, 5], [4, 5], [7, 5]], "v": ["firered", "leafgreen"],
        "k": "starter", "loc": "MAPSEC_PALLET_TOWN",
        "d": {"en": "Professor Oak stops you on Route 22's edge and lets you pick one of the three Poké Balls on his lab table — BULBASAUR, CHARMANDER or SQUIRTLE, all Lv 5.",
              "fa": "پروفسور اُک سر مسیر ۲۲ جلوی شما را می‌گیرد و اجازه می‌دهد یکی از سه توال پوکمون روی میز آزمایشگاهش را انتخاب کنید — بولباسور، چارمندر یا اسکوئرتل، همه سطح ۵."},
    },
    # -------- gifts --------
    {
        "m": [[133, 25]], "v": ["firered", "leafgreen"],
        "k": "gift", "loc": "MAPSEC_CELADON_CITY",
        "d": {"en": "A man in the Condominiums' roof room (the building behind the Celadon Hotel) gives you a Lv 25 EEVEE — his only one; it cannot evolve into Espeon/Umbreon in Gen 3.",
              "fa": "مردی در اتاق پشت‌بام آپارتمان‌ها (ساختمان پشت هتل سِلادون) یک ایوی سطح ۲۵ به شما می‌دهد — تنها ایوی او؛ در نسل ۳ به اِسپئون/آمبرئون تکامل نمی‌کند."},
    },
    {
        "m": [[131, 25]], "v": ["firered", "leafgreen"],
        "k": "gift", "loc": "MAPSEC_SILPH_CO",
        "d": {"en": "After clearing Rocket out of Silph Co., a worker on the 7th floor gives you a Lv 25 LAPRAS — one per game.",
              "fa": "بعد از بیرون کردن تیم راکت از شرکت سیلف، کارگری در طبقه‌ی ۷ یک لاپراس سطح ۲۵ به شما می‌دهد — در هر نسخه یکی."},
    },
    {
        "m": [[106, 25], [107, 25]], "v": ["firered", "leafgreen"],
        "k": "gift", "loc": "MAPSEC_SAFFRON_CITY",
        "d": {"en": "Beat the Karate Master of the Fighting Dojo next to Saffron's gym — choose one prize: HITMONLEE or HITMONCHAN (Lv 25).",
              "fa": "استاد کاراته‌ی دوجوی مبارزه در کنار سالن سافرون را شکست بدهید — یکی از دو جایزه را انتخاب کنید: هیتمن‌لی یا هیتمن‌چان (سطح ۲۵)."},
    },
    {
        "m": [[175, 5]], "v": ["firered", "leafgreen"],
        "k": "egg", "loc": "MAPSEC_WATER_LABYRINTH",
        "d": {"en": "An old man on the Water Labyrinth (between Five Island and Resort Gorgeous) hands you an egg for keeping a small party — it hatches into TOGEPI.",
              "fa": "پیرمردی در هزارتوی آبی (بین جزیره پنج و اقامتگاه گرجیوس) به خاطر کم‌بودن گروهتان یک تخم به شما می‌دهد — از آن توگپی بیرون می‌آید."},
    },
    # -------- fossils (Mt. Moon choice + Old Amber; Cinnabar Lab revives at Lv 5) --------
    {
        "m": [[138, 5], [140, 5]], "v": ["firered", "leafgreen"],
        "k": "fossil", "loc": "MAPSEC_CINNABAR_ISLAND",
        "d": {"en": "The super nerd in Mt. Moon gives the HELIX or DOME fossil (you keep only one); the Cinnabar Lab scientist revives it into OMANYTE or KABUTO (Lv 5).",
              "fa": "سوپر نِرد داخل کوه ماه فسیل هلیکس یا دام را می‌دهد (فقط یکی را نگه می‌دارید)؛ دانشمند آزمایشگاه سینابار آن را به اومانییت یا کابوتو (سطح ۵) زنده می‌کند."},
    },
    {
        "m": [[142, 5]], "v": ["firered", "leafgreen"],
        "k": "fossil", "loc": "MAPSEC_PEWTER_CITY",
        "d": {"en": "The scientist in the back of Pewter's Museum of Science hands you OLD AMBER — the Cinnabar Lab revives it into AERODACTYL (Lv 5).",
              "fa": "دانشمند پشت موزه‌ی علوم پوئتر کهربای قدیمی را به شما می‌دهد — آزمایشگاه سینابار آن را به آئروداکتیل (سطح ۵) زنده می‌کند."},
    },
    # -------- the Magikarp salesman (verified: Route 4 Poké Center, ₽500) --------
    {
        "m": [[129, 5]], "v": ["firered", "leafgreen"],
        "k": "gift", "loc": "MAPSEC_ROUTE_4",
        "d": {"en": "The con man in the Route 4 Poké Center sells a MAGIKARP (Lv 5) for ₽500 — the same deal he ran in Gen 1.",
              "fa": "کلاهبردار داخل مرکز پوکمون مسیر ۴ یک ماجیکارپ (سطح ۵) را ۵۰۰ پوک‌دولار می‌فروشد — همان معامله‌ی نسل ۱."},
    },
    # -------- Celadon Game Corner prizes (script levels; FR/LG differ).
    # One entry per species so every prize mon's HOW TO CATCH lists it. --------
    {
        "m": [[63, 9]], "v": ["firered"],
        "k": "gift", "loc": "MAPSEC_CELADON_CITY",
        "d": {"en": "Celadon Game Corner prize room: ABRA for 180 coins (Lv 9). The FR lineup: CLEFAIRY 500 (Lv 8), DRATINI 2,800 (Lv 18), SCYTHER 5,500 (Lv 25), PORYGON 9,999 (Lv 26).",
              "fa": "اتاق جایزه‌ی کازینو سِلادون: ابرا با ۱۸۰ سکه (سطح ۹). فهرست فایررد: کلی‌فری ۵۰۰ (سطح ۸)، دراتینی ۲٬۸۰۰ (سطح ۱۸)، سایتر ۵٬۵۰۰ (سطح ۲۵)، پوریگون ۹٬۹۹۹ (سطح ۲۶)."},
    },
    {
        "m": [[63, 7]], "v": ["leafgreen"],
        "k": "gift", "loc": "MAPSEC_CELADON_CITY",
        "d": {"en": "Celadon Game Corner prize room: ABRA for 120 coins (Lv 7). The LG lineup: CLEFAIRY 750 (Lv 12), PINSIR 2,500 (Lv 18), DRATINI 4,600 (Lv 24), PORYGON 9,999 (Lv 18).",
              "fa": "اتاق جایزه‌ی کازینو سِلادون: ابرا با ۱۲۰ سکه (سطح ۷). فهرست لیف‌گرین: کلی‌فری ۷۵۰ (سطح ۱۲)، پینسیر ۲٬۵۰۰ (سطح ۱۸)، دراتینی ۴٬۶۰۰ (سطح ۲۴)، پوریگون ۹٬۹۹۹ (سطح ۱۸)."},
    },
    {
        "m": [[35, 8]], "v": ["firered"],
        "k": "gift", "loc": "MAPSEC_CELADON_CITY",
        "d": {"en": "Celadon Game Corner prize room: CLEFAIRY for 500 coins (Lv 8) in FireRed (LeafGreen charges 750 for a Lv 12 one).",
              "fa": "اتاق جایزه‌ی کازینو سِلادون: کلی‌فری با ۵۰۰ سکه (سطح ۸) در فایررد (لیف‌گرین با ۷۵۰ سکه و سطح ۱۲ می‌فروشد)."},
    },
    {
        "m": [[35, 12]], "v": ["leafgreen"],
        "k": "gift", "loc": "MAPSEC_CELADON_CITY",
        "d": {"en": "Celadon Game Corner prize room: CLEFAIRY for 750 coins (Lv 12) in LeafGreen (FireRed charges 500 for a Lv 8 one).",
              "fa": "اتاق جایزه‌ی کازینو سِلادون: کلی‌فری با ۷۵۰ سکه (سطح ۱۲) در لیف‌گرین (فایررد با ۵۰۰ سکه و سطح ۸ می‌فروشد)."},
    },
    {
        "m": [[147, 18]], "v": ["firered"],
        "k": "gift", "loc": "MAPSEC_CELADON_CITY",
        "d": {"en": "Celadon Game Corner prize room: DRATINI for 2,800 coins (Lv 18) in FireRed (LeafGreen charges 4,600 for a Lv 24 one) — the same Dratini the Safari's Super Rod hooks.",
              "fa": "اتاق جایزه‌ی کازینو سِلادون: دراتینی با ۲٬۸۰۰ سکه (سطح ۱۸) در فایررد (لیف‌گرین با ۴٬۶۰۰ سکه و سطح ۲۴ می‌فروشد) — همان دراتینی که سوپر راد سافاری می‌گیرد."},
    },
    {
        "m": [[147, 24]], "v": ["leafgreen"],
        "k": "gift", "loc": "MAPSEC_CELADON_CITY",
        "d": {"en": "Celadon Game Corner prize room: DRATINI for 4,600 coins (Lv 24) in LeafGreen (FireRed charges 2,800 for a Lv 18 one) — the same Dratini the Safari's Super Rod hooks.",
              "fa": "اتاق جایزه‌ی کازینو سِلادون: دراتینی با ۴٬۶۰۰ سکه (سطح ۲۴) در لیف‌گرین (فایررد با ۲٬۸۰۰ سکه و سطح ۱۸ می‌فروشد) — همان دراتینی که سوپر راد سافاری می‌گیرد."},
    },
    {
        "m": [[123, 25]], "v": ["firered"],
        "k": "gift", "loc": "MAPSEC_CELADON_CITY",
        "d": {"en": "Celadon Game Corner prize room: SCYTHER for 5,500 coins (Lv 25) — FireRed exclusive (LeafGreen's counterpart prize is PINSIR).",
              "fa": "اتاق جایزه‌ی کازینو سِلادون: سایتر با ۵٬۵۰۰ سکه (سطح ۲۵) — ویژه‌ی فایررد (جایزه‌ی مقابل در لیف‌گرین پینسیر است)."},
    },
    {
        "m": [[127, 18]], "v": ["leafgreen"],
        "k": "gift", "loc": "MAPSEC_CELADON_CITY",
        "d": {"en": "Celadon Game Corner prize room: PINSIR for 2,500 coins (Lv 18) — LeafGreen exclusive (FireRed's counterpart prize is SCYTHER).",
              "fa": "اتاق جایزه‌ی کازینو سِلادون: پینسیر با ۲٬۵۰۰ سکه (سطح ۱۸) — ویژه‌ی لیف‌گرین (جایزه‌ی مقابل در فایررد سایتر است)."},
    },
    {
        "m": [[137, 26]], "v": ["firered"],
        "k": "gift", "loc": "MAPSEC_CELADON_CITY",
        "d": {"en": "Celadon Game Corner prize room: PORYGON for 9,999 coins (Lv 26) in FireRed — both versions charge the full 9,999; LeafGreen hands out a Lv 18 one.",
              "fa": "اتاق جایزه‌ی کازینو سِلادون: پوریگون با ۹٬۹۹۹ سکه (سطح ۲۶) در فایررد — هر دو نسخه ۹٬۹۹۹ سکه می‌گیرند؛ لیف‌گرین یک پوریگون سطح ۱۸ می‌دهد."},
    },
    {
        "m": [[137, 18]], "v": ["leafgreen"],
        "k": "gift", "loc": "MAPSEC_CELADON_CITY",
        "d": {"en": "Celadon Game Corner prize room: PORYGON for 9,999 coins (Lv 18) in LeafGreen — both versions charge the full 9,999; FireRed hands out a Lv 26 one.",
              "fa": "اتاق جایزه‌ی کازینو سِلادون: پوریگون با ۹٬۹۹۹ سکه (سطح ۱۸) در لیف‌گرین — هر دو نسخه ۹٬۹۹۹ سکه می‌گیرند؛ فایررد یک پوریگون سطح ۲۶ می‌دهد."},
    },
    # -------- in-game trades (pokefirered src/data/ingame_trades.h + scripts) --------
    {
        "m": [[122, None]], "v": ["firered", "leafgreen"],
        "k": "trade", "loc": "MAPSEC_ROUTE_2",
        "d": {"en": "Reyley in the Route 2 gate house trades her MIMIEN the MR. MIME for an ABRA.",
              "fa": "رِیلی در خانه‌ی کناری مسیر ۲ میمیِنِ مستر مایم خود را با ابرا عوض می‌کند."},
    },
    {
        "m": [[124, None]], "v": ["firered", "leafgreen"],
        "k": "trade", "loc": "MAPSEC_CERULEAN_CITY",
        "d": {"en": "Dontae in a Cerulean City house trades ZYNX the JYNX for a POLIWHIRL.",
              "fa": "دونتِی در خانه‌ای در شهر سرولئان زینکس جینکس خود را با پالی‌ویرل عوض می‌کند."},
    },
    {
        "m": [[29, None]], "v": ["firered"],
        "k": "trade", "loc": "MAPSEC_UNDERGROUND_PATH",
        "d": {"en": "Saige in the Underground Path (North Entrance) trades her MS. NIDO the NIDORAN♀ for a NIDORAN♂.",
              "fa": "سیج در راه زیرزمینی (ورودی شمالی) خانم نیدوی خود (نیدورن ماده) را با یک نیدورن نر عوض می‌کند."},
    },
    {
        "m": [[32, None]], "v": ["leafgreen"],
        "k": "trade", "loc": "MAPSEC_UNDERGROUND_PATH",
        "d": {"en": "Saige in the Underground Path (North Entrance) trades her MR. NIDO the NIDORAN♂ for a NIDORAN♀.",
              "fa": "سیج در راه زیرزمینی (ورودی شمالی) آقای نیدوی خود (نیدورن نر) را با یک نیدورن ماده عوض می‌کند."},
    },
    {
        "m": [[83, None]], "v": ["firered", "leafgreen"],
        "k": "trade", "loc": "MAPSEC_VERMILION_CITY",
        "d": {"en": "Elyssa in a Vermilion City house trades CH'DING the FARFETCH'D for a SPEAROW — it holds a STICK.",
              "fa": "الیسا در خانه‌ای در شهر ورمیلیون چدینگ فارفچ‌د خود را با یک اسپارو عوض می‌کند — با «چوب» در دست."},
    },
    {
        "m": [[30, None]], "v": ["firered"],
        "k": "trade", "loc": "MAPSEC_ROUTE_11",
        "d": {"en": "Turner in the Route 11 gate (2F) trades NINA the NIDORINA for a NIDORINO.",
              "fa": "ترنر در دروازه‌ی مسیر ۱۱ (طبقه ۲) نینای خود (نیدورینا) را با نیدورینو عوض می‌کند."},
    },
    {
        "m": [[33, None]], "v": ["leafgreen"],
        "k": "trade", "loc": "MAPSEC_ROUTE_11",
        "d": {"en": "Turner in the Route 11 gate (2F) trades NINO the NIDORINO for a NIDORINA.",
              "fa": "ترنر در دروازه‌ی مسیر ۱۱ (طبقه ۲) نینوی خود (نیدورینو) را با نیدورینا عوض می‌کند."},
    },
    {
        "m": [[108, None]], "v": ["firered"],
        "k": "trade", "loc": "MAPSEC_ROUTE_18",
        "d": {"en": "Haden in the Route 18 gate (2F) trades MARC the LICKITUNG for a GOLDUCK.",
              "fa": "هایدن در دروازه‌ی مسیر ۱۸ (طبقه ۲) مارک لیکی‌تانگ خود را با گلداک عوض می‌کند."},
    },
    {
        "m": [[108, None]], "v": ["leafgreen"],
        "k": "trade", "loc": "MAPSEC_ROUTE_18",
        "d": {"en": "Haden in the Route 18 gate (2F) trades MARC the LICKITUNG for a SLOWBRO.",
              "fa": "هایدن در دروازه‌ی مسیر ۱۸ (طبقه ۲) مارک لیکی‌تانگ خود را با اسلوبرو عوض می‌کند."},
    },
    {
        "m": [[101, None]], "v": ["firered", "leafgreen"],
        "k": "trade", "loc": "MAPSEC_CINNABAR_ISLAND",
        "d": {"en": "Clifton in the Cinnabar Lab lounge trades ESPHERE the ELECTRODE for a RAICHU.",
              "fa": "کلیفتون در نشیمن آزمایشگاه سینابار اسفیر الکترود خود را با رایچو عوض می‌کند."},
    },
    {
        "m": [[114, None]], "v": ["firered", "leafgreen"],
        "k": "trade", "loc": "MAPSEC_CINNABAR_ISLAND",
        "d": {"en": "Norma in the Cinnabar Lab lounge trades TANGENY the TANGELA for a VENONAT — it holds STARDUST.",
              "fa": "نورما در نشیمن آزمایشگاه سینابار تنگنی تانگلا خود را با ونونات عوض می‌کند — با «غبار ستاره»."},
    },
    {
        "m": [[86, None]], "v": ["firered", "leafgreen"],
        "k": "trade", "loc": "MAPSEC_CINNABAR_ISLAND",
        "d": {"en": "Garett in the Cinnabar Lab's experiment room trades SEELOR the SEEL for a PONYTA.",
              "fa": "گرت در اتاق آزمایش آزمایشگاه سینابار سیلور سیل خود را با پونی‌تا عوض می‌کند."},
    },
    # -------- static battles (setwildbattle levels from the map scripts) --------
    {
        "m": [[150, 70]], "v": ["firered", "leafgreen"],
        "k": "static", "loc": "MAPSEC_CERULEAN_CAVE",
        "d": {"en": "MEWTWO (Lv 70) waits at the bottom of the cave (B1F) — the cave opens only after Celio's machine links with Hoenn.",
              "fa": "میوتو (سطح ۷۰) در انتهای غار (زیرزمین) منتظر است — غار فقط بعد از اتصال دستگاه سِلیو به هوئن باز می‌شود."},
    },
    {
        "m": [[144, 50]], "v": ["firered", "leafgreen"],
        "k": "static", "loc": "MAPSEC_SEAFOAM_ISLANDS",
        "d": {"en": "ARTICUNO (Lv 50) perches on B4F — push the boulders into the current to dam the water and reach it.",
              "fa": "آرتیکونو (سطح ۵۰) در زیرزمین ۴ نشسته — صخره‌ها را داخل جریان بیندازید تا آب سد شود و به آن برسید."},
    },
    {
        "m": [[145, 50]], "v": ["firered", "leafgreen"],
        "k": "static", "loc": "MAPSEC_POWER_PLANT",
        "d": {"en": "ZAPDOS (Lv 50) roosts at the far end of the plant.",
              "fa": "زاپدوس (سطح ۵۰) در انتهای نیروگاه لانه کرده است."},
    },
    {
        "m": [[101, 34]], "v": ["firered", "leafgreen"],
        "k": "static", "loc": "MAPSEC_POWER_PLANT",
        "d": {"en": "Two Lv 34 ELECTRODE pose as Poké Balls inside the plant — beat or catch them.",
              "fa": "دو الکترود سطح ۳۴ خود را به شکل توال پوکمون جا زده‌اند — آن‌ها را شکست بدهید یا بگیرید."},
    },
    {
        "m": [[146, 50]], "v": ["firered", "leafgreen"],
        "k": "static", "loc": "MAPSEC_MT_EMBER",
        "d": {"en": "MOLTRES (Lv 50) sits at the summit — FRLG moved it here from Victory Road.",
              "fa": "مولترس (سطح ۵۰) روی قله نشسته — در فایررد/لیف‌گرین از جاده پیروزی به اینجا منتقل شده است."},
    },
    {
        "m": [[143, 30]], "v": ["firered", "leafgreen"],
        "k": "static", "loc": "MAPSEC_ROUTE_12",
        "d": {"en": "A sleeping SNORLAX (Lv 30) blocks the road — wake it with the POKé FLUTE and battle it. One of only two in the game.",
              "fa": "یک اسنورلاکس خوابیده (سطح ۳۰) راه را بسته — با فلوت پوکمون بیدارش کنید و با آن بجنگید. یکی از تنها دو عدد در کل بازی."},
    },
    {
        "m": [[143, 30]], "v": ["firered", "leafgreen"],
        "k": "static", "loc": "MAPSEC_ROUTE_16",
        "d": {"en": "The second sleeping SNORLAX (Lv 30) blocks Cycling Road's gate — same POKé FLUTE routine.",
              "fa": "اسنورلاکس خواب دوم (سطح ۳۰) دروازه‌ی جاده دوچرخه را بسته — همان کار فلوت پوکمون."},
    },
    {
        "m": [[97, 30]], "v": ["firered", "leafgreen"],
        "k": "static", "loc": "MAPSEC_BERRY_FOREST",
        "d": {"en": "The HYPNO (Lv 30) that kidnapped Lostelle lurks in the Berry Forest's deepest grove — beat or catch it.",
              "fa": "هیپنویی که لاستل را ربوده بود در عمیق‌ترین گوشه‌ی جنگل توت کمین کرده — شکستش بدهید یا بگیرید."},
    },
    # -------- roaming beast (src/roamer.c: starter decides the species) --------
    {
        "m": [[243, 50], [244, 50], [245, 50]], "v": ["firered", "leafgreen"],
        "k": "roamer", "note": "roam",
        "d": {"en": "After Celio's Network Machine links with Hoenn (deliver the RUBY from Mt. Ember), one legendary beast roams Kanto's grass routes — WHICH one depends on your starter: SQUIRTLE → RAIKOU, CHARMANDER → SUICUNE, BULBASAUR → ENTEI (Lv 50).",
              "fa": "بعد از اتصال دستگاه سِلیو به هوئن (تحویل یاقوت کوه امبر)، یکی از سه هیولای افسانه‌ای در مسیرهای علفزار کانتو می‌گردد — کدام؟ بستگی به استارتر شما دارد: اسکوئرتل ← رایکو، چارمندر ← سوئیکون، بولباسور ← انتی (سطح ۵۰)."},
    },
    # -------- ticket events --------
    {
        "m": [[249, 70]], "v": ["firered", "leafgreen"],
        "k": "event", "loc": "MAPSEC_NAVEL_ROCK",
        "d": {"en": "With the MYSTIC TICKET (event), the ferry from Vermilion docks at Navel Rock — the descending path ends in LUGIA (Lv 70), the climbing path in HO-OH (Lv 70).",
              "fa": "با «بلیط اسرارآمیز» (ایونت)، کشتی از ورمیلیون به صخره ناول می‌رسد — مسیر پایین‌رو به لوگیا (سطح ۷۰) و مسیر بالارو به هو-اوه (سطح ۷۰) می‌رسد."},
    },
    {
        "m": [[250, 70]], "v": ["firered", "leafgreen"],
        "k": "event", "loc": "MAPSEC_NAVEL_ROCK",
        "d": {"en": "Navel Rock's summit chamber holds HO-OH (Lv 70) — same MYSTIC TICKET ferry as Lugia's abyss below.",
              "fa": "اتاق قله‌ی صخره ناول هو-اوه (سطح ۷۰) را نگه می‌دارد — همان بلیط اسرارآمیزِ کشتی که به لوگیای اعماق هم می‌رسد."},
    },
    {
        "m": [[386, 30]], "v": ["firered"],
        "k": "event", "loc": "MAPSEC_BIRTH_ISLAND",
        "d": {"en": "With the AURORA TICKET (event), the ferry stops at Birth Island — solving the triangle puzzle summons DEOXYS (Lv 30) in its ATTACK forme in FireRed.",
              "fa": "با «بلیط شفق» (ایونت)، کشتی در جزیره تولد پهلو می‌گیرد — حل پازل مثلث، دِاکسیس (سطح ۳۰) را در فرم حمله در فایررد احضار می‌کند."},
    },
    {
        "m": [[386, 30]], "v": ["leafgreen"],
        "k": "event", "loc": "MAPSEC_BIRTH_ISLAND",
        "d": {"en": "With the AURORA TICKET (event), the ferry stops at Birth Island — solving the triangle puzzle summons DEOXYS (Lv 30) in its DEFENSE forme in LeafGreen.",
              "fa": "با «بلیط شفق» (ایونت)، کشتی در جزیره تولد پهلو می‌گیرد — حل پازل مثلث، دِاکسیس (سطح ۳۰) را در فرم دفاع در لیف‌گرین احضار می‌کند."},
    },
]

LOC_NOTES_FRLG = {
    "MAPSEC_KANTO_SAFARI_ZONE": {
        "en": "FRLG Safari rules: 30 Safari Balls and 600 steps per visit — no step-burn trick with bait; the four zones share one clock.",
        "fa": "قوانین سافاری در فایررد/لیف‌گرین: در هر بازدید ۳۰ توال سافاری و ۶۰۰ قدم دارید — ترفند خسته کردن با طعمه کارایی ندارد؛ چهار بخش یک ساعت مشترک دارند.",
    },
    "MAPSEC_ALTERING_CAVE": {
        "en": "Altering Cave's 9 tables are Mystery-Gift/e-Reader swaps: Zubat (L 10) by default; event data swaps all 12 slots to Mareep (7), Pineco (23), Houndour (16), Teddiursa (22), Aipom (22), Shuckle (22), Stantler (22) or Smeargle (22). Without the event, it stays Zubat-only.",
        "fa": "۹ جدول غار دگردیسی سوآپ‌های گیفت مرموز/ای‌ریدر هستند: پیش‌فرض زوبات (سطح ۱۰)؛ دیتای ایونت هر ۱۲ خانه را به مریپ (۷)، پینکو (۲۳)، هاون‌دور (۱۶)، تدی‌ورسا (۲۲)، آیپام (۲۲)، شاکل (۲۲)، استنتر (۲۲) یا اسمیرگل (۲۲) عوض می‌کند. بدون ایونت، فقط زوبات دارید.",
    },
    "MAPSEC_MT_EMBER": {
        "en": "Behind the Ruby Path's B2F, Team Rocket guards the RUBY gem that powers Celio's Network Machine — delivering it opens Cerulean Cave and sends a legendary beast roaming Kanto.",
        "fa": "پشت زیرزمین ۲ جاده یاقوت، تیم راکت از نگین «یاقوت» که دستگاه سِلیو را روشن می‌کند محافظت می‌کند — تحویل آن غار سرولئان را باز می‌کند و یکی از هیولاهای افسانه‌ای را در کانتو سرگردان می‌کند.",
    },
    "MAPSEC_CERULEAN_CAVE": {
        "en": "The strongest wild habitat in Kanto (Lv 46–67 land) — opens only after the Network Machine runs; Mewtwo waits on B1F.",
        "fa": "قوی‌ترین زیستگاه وحشی کانتو (سطح ۴۶–۶۷ در خشکی) — فقط بعد از راه‌اندازی دستگاه شبکه باز می‌شود؛ موتو در زیرزمین منتظر است.",
    },
    "MAPSEC_TRAINER_TOWER": {
        "en": "The tower itself holds no wild Pokémon — only the sea in front of it does. Inside is the speed-run ladder (best time is recorded on the record board).",
        "fa": "خود برج هیچ پوکمون وحشی ندارد — فقط دریای جلویش دارد. داخل برج مسابقه‌ی سرعتی است (بهترین زمان روی تابلوی رکورد ثبت می‌شود).",
    },
    "MAPSEC_BIRTH_ISLAND": {
        "en": "The triangle puzzle must be solved in a strict push order — each correct step makes the triangle glow red-hot; one wrong step resets it. Deoxys's forme rides the cartridge: FIRERED = Attack, LEAFGREEN = Defense.",
        "fa": "پازل مثلث باید با ترتیب دقیقی هل داده شود — هر قدم درست، مثلث را سرخ‌داغ می‌کند؛ یک قدم اشتباه همه را ریست می‌کند. فرم دِاکسیس به کارتریج بسته است: فایررد = حمله، لیف‌گرین = دفاع.",
    },
}

# Unown letter sets per chamber (src/wild_encounter.c sUnownLetterSlots —
# chamber order = Monean, Liptoo, Weepth, Dilford, Scufib, Rixy, Viapois;
# 12 land slots, chances 20/20/10/10/10/10/5/5/4/4/1/1).
UNOWN_SETS = {
    "MAPSEC_MONEAN_CHAMBER":  ("A ×11 + ?", "A ×۱۱ + ?"),
    "MAPSEC_LIPTOO_CHAMBER":  ("C D H U O", "C D H U O"),
    "MAPSEC_WEEPTH_CHAMBER":  ("N S I E", "N S I E"),
    "MAPSEC_DILFORD_CHAMBER": ("P L J R Q", "P L J R Q"),
    "MAPSEC_SCUFIB_CHAMBER":  ("Y T G F K", "Y T G F K"),
    "MAPSEC_RIXY_CHAMBER":    ("V W X M B", "V W X M B"),
    "MAPSEC_VIAPOIS_CHAMBER": ("Z ×11 + !", "Z ×۱۱ + !"),
}

# Sevii towns with no wild tables of their own and no anchored special —
# force-included for region coverage (the plan's Four–Seven sweep), each
# with an honest, factual note about what the town actually hosts.
FORCE_NOTES_FRLG = {
    "MAPSEC_TWO_ISLAND": {
        "en": "No wild Pokémon on the town itself. The old lady on Cape Brink above the town teaches the ultimate moves (FRENZY PLANT / BLAST BURN / HYDRO CANNON) to a fully-evolved Kanto starter with max friendship.",
        "fa": "خود شهر هیچ پوکمون وحشی ندارد. پیرزن دماغه برینک در بالای شهر، حرکات نهایی (فرنزی پلنت / بلاست برن / هیدرو کانن) را به استارتر تکامل‌یافته‌ی کانتو با خوشحالی کامل یاد می‌دهد."},
    "MAPSEC_THREE_ISLAND": {
        "en": "No wild Pokémon on the town itself. Lostelle, the mayor's daughter, is missing toward Berry Forest — a HYPNO lurks in its deepest grove.",
        "fa": "خود شهر هیچ پوکمون وحشی ندارد. لاستل، دختر شهردار، سمت جنگل توت گم شده — یک هیپنو در عمیق‌ترین گوشه‌ی آن کمین کرده است."},
    "MAPSEC_SIX_ISLAND": {
        "en": "No wild Pokémon on the town itself — it is the gateway to Altering Cave, Dotted Hole and Ruin Valley; the SAPPHIRE gem lies inside Dotted Hole.",
        "fa": "خود شهر هیچ پوکمون وحشی ندارد — دروازه‌ی غار دگردیسی، حفره‌ی نقطه‌دار و دره‌ی ویرانه‌ها است؛ نگین «یاقوت کبود» داخل حفره‌ی نقطه‌دار پنهان است."},
    "MAPSEC_SEVEN_ISLAND": {
        "en": "No wild Pokémon on the town itself — it is the gateway to the Tanoby Ruins: seven chambers of UNOWN scattered over the islets south of the town.",
        "fa": "خود شهر هیچ پوکمون وحشی ندارد — دروازه‌ی ویرانه‌های تانوبی است: هفت اتاق آن‌کون در جزیره‌های جنوب شهر پراکنده‌اند."},
}

