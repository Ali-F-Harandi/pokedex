# -*- coding: utf-8 -*-
"""Pokédex Plus — hand-written bilingual (EN/FA) names for the Gen-3
Location Dex, consumed by tools/build-locations-gen3.py.

LOC_NAMES: MAPSEC id -> (en, fa, group).  Groups: route / city / forest /
cave / water / safari / island / building.  Persian digits everywhere.
ROOMS: wild-map dir name -> (en, fa, ord) room label (None ord = single-map
locations carry no room label).  Rooms sharing a label merge when their
encounter tables are identical (Meteor Falls B1F pair, Magma Hideout 2F/3F).
"""

LOC_NAMES = {
    # ---------------- towns & cities ----------------
    "MAPSEC_LITTLEROOT_TOWN":   ("Littleroot Town",   "شهرک لیتل‌روت", "city"),
    "MAPSEC_LAVARIDGE_TOWN":    ("Lavaridge Town",    "شهرک لاوریج", "city"),
    "MAPSEC_RUSTBORO_CITY":     ("Rustboro City",     "شهر رستبورو", "city"),
    "MAPSEC_FORTREE_CITY":      ("Fortree City",      "شهر فورتری", "city"),
    "MAPSEC_DEWFORD_TOWN":      ("Dewford Town",      "شهرک دیوفورد", "city"),
    "MAPSEC_SLATEPORT_CITY":    ("Slateport City",    "شهر اسلیت‌پورت", "city"),
    "MAPSEC_LILYCOVE_CITY":     ("Lilycove City",     "شهر لیلی‌کو", "city"),
    "MAPSEC_MOSSDEEP_CITY":     ("Mossdeep City",     "شهر موس‌دیپ", "city"),
    "MAPSEC_SOOTOPOLIS_CITY":   ("Sootopolis City",   "شهر سووتوپلیس", "city"),
    "MAPSEC_EVER_GRANDE_CITY":  ("Ever Grande City",  "شهر اِور گراند", "city"),
    "MAPSEC_PACIFIDLOG_TOWN":   ("Pacifidlog Town",   "شهرک پاسیفیدلاگ", "city"),
    "MAPSEC_PETALBURG_CITY":    ("Petalburg City",    "شهر پتالبورگ", "city"),
    # ---------------- routes (land) ----------------
    "MAPSEC_ROUTE_101": ("Route 101", "مسیر ۱۰۱", "route"),
    "MAPSEC_ROUTE_102": ("Route 102", "مسیر ۱۰۲", "route"),
    "MAPSEC_ROUTE_103": ("Route 103", "مسیر ۱۰۳", "route"),
    "MAPSEC_ROUTE_104": ("Route 104", "مسیر ۱۰۴", "route"),
    "MAPSEC_ROUTE_105": ("Route 105", "مسیر ۱۰۵", "route"),
    "MAPSEC_ROUTE_106": ("Route 106", "مسیر ۱۰۶", "route"),
    "MAPSEC_ROUTE_107": ("Route 107", "مسیر ۱۰۷", "route"),
    "MAPSEC_ROUTE_108": ("Route 108", "مسیر ۱۰۸", "route"),
    "MAPSEC_ROUTE_109": ("Route 109", "مسیر ۱۰۹", "route"),
    "MAPSEC_ROUTE_110": ("Route 110", "مسیر ۱۱۰", "route"),
    "MAPSEC_ROUTE_111": ("Route 111", "مسیر ۱۱۱", "route"),
    "MAPSEC_ROUTE_112": ("Route 112", "مسیر ۱۱۲", "route"),
    "MAPSEC_ROUTE_113": ("Route 113", "مسیر ۱۱۳", "route"),
    "MAPSEC_ROUTE_114": ("Route 114", "مسیر ۱۱۴", "route"),
    "MAPSEC_ROUTE_115": ("Route 115", "مسیر ۱۱۵", "route"),
    "MAPSEC_ROUTE_116": ("Route 116", "مسیر ۱۱۶", "route"),
    "MAPSEC_ROUTE_117": ("Route 117", "مسیر ۱۱۷", "route"),
    "MAPSEC_ROUTE_118": ("Route 118", "مسیر ۱۱۸", "route"),
    "MAPSEC_ROUTE_119": ("Route 119", "مسیر ۱۱۹", "route"),
    "MAPSEC_ROUTE_120": ("Route 120", "مسیر ۱۲۰", "route"),
    "MAPSEC_ROUTE_121": ("Route 121", "مسیر ۱۲۱", "route"),
    "MAPSEC_ROUTE_122": ("Route 122", "مسیر ۱۲۲", "route"),
    "MAPSEC_ROUTE_123": ("Route 123", "مسیر ۱۲۳", "route"),
    "MAPSEC_ROUTE_124": ("Route 124", "مسیر ۱۲۴", "route"),
    "MAPSEC_ROUTE_125": ("Route 125", "مسیر ۱۲۵", "route"),
    "MAPSEC_ROUTE_126": ("Route 126", "مسیر ۱۲۶", "route"),
    "MAPSEC_ROUTE_127": ("Route 127", "مسیر ۱۲۷", "route"),
    "MAPSEC_ROUTE_128": ("Route 128", "مسیر ۱۲۸", "route"),
    "MAPSEC_ROUTE_129": ("Route 129", "مسیر ۱۲۹", "route"),
    "MAPSEC_ROUTE_130": ("Route 130", "مسیر ۱۳۰", "route"),
    "MAPSEC_ROUTE_131": ("Route 131", "مسیر ۱۳۱", "route"),
    "MAPSEC_ROUTE_132": ("Route 132", "مسیر ۱۳۲", "route"),
    "MAPSEC_ROUTE_133": ("Route 133", "مسیر ۱۳۳", "route"),
    "MAPSEC_ROUTE_134": ("Route 134", "مسیر ۱۳۴", "route"),
    "MAPSEC_JAGGED_PASS": ("Jagged Pass", "گردنه‌ی دندانه‌دار", "route"),
    # ---------------- forests ----------------
    "MAPSEC_PETALBURG_WOODS": ("Petalburg Woods", "جنگل پتالبورگ", "forest"),
    # ---------------- caves & dungeons ----------------
    "MAPSEC_RUSTURF_TUNNEL":   ("Rusturf Tunnel",    "تونل راسترف", "cave"),
    "MAPSEC_GRANITE_CAVE":     ("Granite Cave",      "غار گرانیت", "cave"),
    "MAPSEC_METEOR_FALLS":     ("Meteor Falls",      "آبشار شهاب‌سنگ", "cave"),
    "MAPSEC_FIERY_PATH":       ("Fiery Path",        "مسیر آتشین", "cave"),
    "MAPSEC_MT_PYRE":          ("Mt. Pyre",          "کوه پایر", "cave"),
    "MAPSEC_SEAFLOOR_CAVERN":  ("Seafloor Cavern",   "غار بستر دریا", "cave"),
    "MAPSEC_CAVE_OF_ORIGIN":   ("Cave of Origin",    "غار سرچشمه", "cave"),
    "MAPSEC_VICTORY_ROAD":     ("Victory Road",      "جاده‌ی پیروزی", "cave"),
    "MAPSEC_SKY_PILLAR":       ("Sky Pillar",        "ستون آسمان", "cave"),
    "MAPSEC_SHOAL_CAVE":       ("Shoal Cave",        "غار کم‌عمق", "cave"),
    "MAPSEC_DESERT_UNDERPASS": ("Desert Underpass",  "گذرگاه زیر بیابان", "cave"),
    "MAPSEC_MIRAGE_TOWER":     ("Mirage Tower",      "برج سراب", "cave"),
    "MAPSEC_ALTERING_CAVE":    ("Altering Cave",     "غار دگرگون", "cave"),
    "MAPSEC_ARTISAN_CAVE":     ("Artisan Cave",      "غار استادکاران", "cave"),
    "MAPSEC_DESERT_RUINS":     ("Desert Ruins",      "ویرانه‌های بیابان", "cave"),
    "MAPSEC_ISLAND_CAVE":      ("Island Cave",       "غار جزیره", "cave"),
    "MAPSEC_ANCIENT_TOMB":     ("Ancient Tomb",      "آرامگاه باستانی", "cave"),
    "MAPSEC_TERRA_CAVE":       ("Terra Cave",        "غار زمینی", "cave"),
    "MAPSEC_MARINE_CAVE":      ("Marine Cave",       "غار دریایی", "cave"),
    # ---------------- underwater ----------------
    "MAPSEC_UNDERWATER_124": ("Underwater Route 124", "زیر آبِ مسیر ۱۲۴", "water"),
    "MAPSEC_UNDERWATER_125": ("Underwater Route 125", "زیر آبِ مسیر ۱۲۵", "water"),
    "MAPSEC_UNDERWATER_126": ("Underwater Route 126", "زیر آبِ مسیر ۱۲۶", "water"),
    # ---------------- safari ----------------
    "MAPSEC_SAFARI_ZONE": ("Safari Zone", "منطقه‌ی سافاری", "safari"),
    # ---------------- islands ----------------
    "MAPSEC_SOUTHERN_ISLAND": ("Southern Island", "جزیره‌ی جنوبی", "island"),
    "MAPSEC_NAVEL_ROCK":      ("Navel Rock",      "صخره‌ی ناول", "island"),
    "MAPSEC_BIRTH_ISLAND":    ("Birth Island",    "جزیره‌ی تولد", "island"),
    "MAPSEC_FARAWAY_ISLAND":  ("Faraway Island",  "جزیره‌ی دورافتاده", "island"),
    # ---------------- buildings ----------------
    "MAPSEC_AQUA_HIDEOUT":    ("Aqua Hideout",     "مخفیگاه آکوا", "building"),
    "MAPSEC_MAGMA_HIDEOUT":   ("Magma Hideout",    "مخفیگاه ماگما", "building"),
    "MAPSEC_NEW_MAUVILLE":    ("New Mauville",     "نیو موویل", "building"),
    "MAPSEC_ABANDONED_SHIP":  ("Abandoned Ship",   "کشتی رهاشده", "building"),
    "MAPSEC_BATTLE_FRONTIER": ("Battle Frontier",  "مرز نبرد", "building"),
}

# Wild-map dir name -> (room label EN, room label FA, room order).
# Locations whose MAPSEC owns exactly one wild map get no room label.
ROOMS = {
    "MeteorFalls_1F_1R":        ("1F (room 1)",         "طبقه‌ی ۱ (اتاق ۱)", 21),
    "MeteorFalls_1F_2R":        ("1F (room 2)",         "طبقه‌ی ۱ (اتاق ۲)", 22),
    "MeteorFalls_B1F_1R":       ("B1F (room 1)",        "زیرزمین ۱ (اتاق ۱)", 31),
    "MeteorFalls_B1F_2R":       ("B1F (room 2)",        "زیرزمین ۱ (اتاق ۲)", 32),
    "MeteorFalls_StevensCave":  ("Steven's Cave",       "غار استیون", 40),
    "GraniteCave_1F":           ("1F",                  "طبقه‌ی ۱", 10),
    "GraniteCave_B1F":          ("B1F",                 "زیرزمین ۱", 20),
    "GraniteCave_B2F":          ("B2F",                 "زیرزمین ۲", 30),
    "GraniteCave_StevensRoom":  ("Steven's Room",       "اتاق استیون", 40),
    "MtPyre_1F":                ("1F",                  "طبقه‌ی ۱", 10),
    "MtPyre_2F":                ("2F",                  "طبقه‌ی ۲", 20),
    "MtPyre_3F":                ("3F",                  "طبقه‌ی ۳", 30),
    "MtPyre_4F":                ("4F",                  "طبقه‌ی ۴", 40),
    "MtPyre_5F":                ("5F",                  "طبقه‌ی ۵", 50),
    "MtPyre_6F":                ("6F",                  "طبقه‌ی ۶", 60),
    "MtPyre_Exterior":          ("Outdoors",            "بیرون", 70),
    "MtPyre_Summit":            ("Summit",              "قله", 80),
    "CaveOfOrigin_Entrance":    ("Entrance",            "ورودی", 10),
    "CaveOfOrigin_1F":          ("1F",                  "طبقه‌ی ۱", 20),
    "CaveOfOrigin_B1F":         ("B1F",                 "زیرزمین ۱", 30),
    "CaveOfOrigin_B2F":         ("B2F",                 "زیرزمین ۲", 40),
    "CaveOfOrigin_B3F":         ("B3F",                 "زیرزمین ۳", 50),
    "VictoryRoad_1F":           ("1F",                  "طبقه‌ی ۱", 10),
    "VictoryRoad_B1F":          ("B1F",                 "زیرزمین ۱", 20),
    "VictoryRoad_B2F":          ("B2F",                 "زیرزمین ۲", 30),
    "SeafloorCavern_Entrance":  ("Entrance",            "ورودی", 10),
    "SeafloorCavern_Room1":     ("Room 1",              "اتاق ۱", 11),
    "SeafloorCavern_Room2":     ("Room 2",              "اتاق ۲", 12),
    "SeafloorCavern_Room3":     ("Room 3",              "اتاق ۳", 13),
    "SeafloorCavern_Room4":     ("Room 4",              "اتاق ۴", 14),
    "SeafloorCavern_Room5":     ("Room 5",              "اتاق ۵", 15),
    "SeafloorCavern_Room6":     ("Room 6",              "اتاق ۶", 16),
    "SeafloorCavern_Room7":     ("Room 7",              "اتاق ۷", 17),
    "SeafloorCavern_Room8":     ("Room 8",              "اتاق ۸", 18),
    "SkyPillar_1F":             ("1F",                  "طبقه‌ی ۱", 10),
    "SkyPillar_3F":             ("3F",                  "طبقه‌ی ۳", 30),
    "SkyPillar_5F":             ("5F",                  "طبقه‌ی ۵", 50),
    "ShoalCave_LowTideEntranceRoom": ("Entrance (low tide)", "ورودی (جزر)", 10),
    "ShoalCave_LowTideStairsRoom":   ("Stairs (low tide)",   "پلکان (جزر)", 20),
    "ShoalCave_LowTideIceRoom":      ("Ice room (low tide)", "اتاق یخی (جزر)", 30),
    "ShoalCave_LowTideInnerRoom":    ("Inner room (low tide)", "اتاق درونی (جزر)", 40),
    "ShoalCave_LowTideLowerRoom":    ("Lower room (low tide)", "اتاق پایین (جزر)", 50),
    "SafariZone_North":         ("North area",          "بخش شمالی", 10),
    "SafariZone_Northeast":     ("Northeast area",      "بخش شمال‌شرقی", 21),
    "SafariZone_Northwest":     ("Northwest area",      "بخش شمال‌غربی", 22),
    "SafariZone_South":         ("South area",          "بخش جنوبی", 30),
    "SafariZone_Southeast":     ("Southeast area",      "بخش جنوب‌شرقی", 41),
    "SafariZone_Southwest":     ("Southwest area",      "بخش جنوب‌غربی", 42),
    "NewMauville_Entrance":     ("Entrance",            "ورودی", 10),
    "NewMauville_Inside":       ("Inside",              "درون", 20),
    "AbandonedShip_HiddenFloorCorridors": ("Hidden floor corridors", "راهروهای طبقه‌ی پنهان", 10),
    "AbandonedShip_Rooms_B1F":  ("Rooms B1F",           "اتاق‌های زیرزمین ۱", 20),
    "MagmaHideout_1F":          ("1F",                  "طبقه‌ی ۱", 10),
    "MagmaHideout_2F_1R":       ("2F",                  "طبقه‌ی ۲", 20),
    "MagmaHideout_2F_2R":       ("2F",                  "طبقه‌ی ۲", 20),
    "MagmaHideout_2F_3R":       ("2F",                  "طبقه‌ی ۲", 20),
    "MagmaHideout_3F_1R":       ("3F",                  "طبقه‌ی ۳", 30),
    "MagmaHideout_3F_2R":       ("3F",                  "طبقه‌ی ۳", 30),
    "MagmaHideout_3F_3R":       ("3F",                  "طبقه‌ی ۳", 30),
    "MagmaHideout_4F":          ("4F",                  "طبقه‌ی ۴", 40),
    "MirageTower_1F":           ("1F",                  "طبقه‌ی ۱", 10),
    "MirageTower_2F":           ("2F",                  "طبقه‌ی ۲", 20),
    "MirageTower_3F":           ("3F",                  "طبقه‌ی ۳", 30),
    "MirageTower_4F":           ("4F",                  "طبقه‌ی ۴", 40),
    "ArtisanCave_1F":           ("1F",                  "طبقه‌ی ۱", 10),
    "ArtisanCave_B1F":          ("B1F",                 "زیرزمین ۱", 20),
}

# Position bumps so special-only locations sort next to their real-world spot
# (order key = y * 1000 + x * 10, same key the region map gives the others).
LOC_POS_OVERRIDES = {
    "MAPSEC_AQUA_HIDEOUT":    (18, 3),    # Lilycove harbor side
    "MAPSEC_MAGMA_HIDEOUT":   (6, 3),     # Jagged Pass side
    "MAPSEC_TERRA_CAVE":      (0, 2),     # appears on Route 115 (or 114)
    "MAPSEC_MARINE_CAVE":     (0, 10),    # appears on Route 105 (or 106)
    "MAPSEC_SOUTHERN_ISLAND": (21, 10),   # off Route 130
    "MAPSEC_NAVEL_ROCK":      (25, 12),   # off Route 134, east
    "MAPSEC_BIRTH_ISLAND":    (26, 12),   # off Route 134, far east
    "MAPSEC_FARAWAY_ISLAND":  (18, 11),   # west of Route 131
    "MAPSEC_BATTLE_FRONTIER": (25, 12),   # east of Route 128/134
}
