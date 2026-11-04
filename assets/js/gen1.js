"use strict";
/* ===== Pokédex Plus — GENERATION I: all four games in one dex (Red · Blue ·
   Green (Japan) · Yellow). Derived from the Red/Blue page; loads gen1-data.js
   (DATA / EVOLUTIONS / SPRITE_SETS) and moves-gen1.js (MD_RB / MD_Y). ===== */
/* sprite sets — PNG files served from assets/sprites/ (paths injected at build time).
   rb = Game Boy mono (DMG/Pocket palettes) · rbc = Red/Blue colorized ·
   yellow = Yellow's redrawn sprites · gold = Game Boy Color (colored). */

/* ===== i18n ===== */
const I18N = {
en:{
  brand_main:"Kanto Pokédex — 151 Pokémon",
  kb_hint:"↑↓ browse · / search", home:"HOME",
  search_ph:"Search name or number...",
  modes:{kanto:"KANTO"},
  showing:"Showing {a} of {b}", no_results:"No Pokémon found",
  pal_mark:"Palette", cry_mark:"Cry", own_mark:"Own", fav_mark:"Fav",
  pal_names:{dmg:"Game Boy", pocket:"Pocket"},
  set_mark:"Sprites", set_names:{rb:"Red/Blue", rbc:"Red/Blue Color", green:"Green (Japan)", y:"Yellow", yc:"Yellow Color"},
  theme_short:{red:"RED", blue:"BLUE", green:"GREEN", yellow:"YELLOW"},
  theme_names:{red:"Pokémon Red", blue:"Pokémon Blue", green:"Pokémon Green (Japan)", yellow:"Pokémon Yellow"},
  theme_tag:{red:"GEN I · RED VERSION", blue:"GEN I · BLUE VERSION", green:"GEN I · GREEN VERSION (JAPAN)", yellow:"GEN I · YELLOW VERSION"},
  chip_mono:"MONO", chip_color:"COLOR",
  text_ver:"Dex text version",
  m_game_tpl:"Game: {v}", m_game:"Game: Red",
  back_mark:"Back", view_front:"Front", view_back:"Back", m_view_tpl:"View: {v}", m_back:"View: Front",
  green_note:"The Japan-only 1996 Green version with its older artwork — the international Red/Blue replaced it with redrawn sprites.",
  m_set:"Sprites: Red/Blue", m_set_tpl:"Sprites: {v}", m_pal:"Palette: Game Boy",
  pal_color_note:"Screen palette — mono sprites only",
  dex_status:"DEX STATUS", seen:"Seen", own:"Owned",
  ht:"HT", wt:"WT",
  prev:"◀ Prev", next:"Next ▶", random:"Random",
  entry_t:"POKéDEX ENTRY", stats_t:"BASE STATS", total:"TOTAL",
  weak_t:"TYPE MATCHUPS", evo_t:"EVOLUTION LINE", data_t:"POKéMON DATA",
  wk4:"Weak ×4", wk2:"Weak ×2", whalf:"Resist ×½", wquarter:"Resist ×¼", wzero:"Immune ×0", wnorm:"Normal damage",
  g1_note:"Authentic Generation I type mechanics.",
  no_evo:"This Pokémon does not evolve.",
  evo_extra:"+{n} more evolution(s) beyond Gen 1",
  evo_unknown:"Data unknown — not seen yet",
  abilities:"Abilities", hidden:"Hidden",
  capture:"Catch rate", capture_hint:"(max 255)", happiness:"Base happiness",
  growth:"Growth rate", exp:"Base exp. yield", egg:"Egg groups", habitat:"Habitat",
  gender:"Gender ratio", genderless:"Genderless",
  legendary:"Legendary", mythical:"Mythical", genb:"GEN {n}",
  page:"{a}/{b}",
  start:"START", menu:"MENU", menu_title:"POKéDEX MENU",
  m_search:"Search", m_random:"Random Pokémon",
  m_cry:"Play cry", m_pal_tpl:"Palette: {v}",
  m_lcd:"Screen: LCD", m_lcd_tpl:"Screen: LCD {v}",
  lcd_mark:"LCD", lcd_on:"ON", lcd_off:"OFF",
  gc_title:"SETTINGS",
  flip_hint:"Tap the sprite: front / back",
  swipe_hint:"swipe: browse · tap: front / back",
  m_fav:"Favorites only", m_sort:"Sort: number", m_reset:"Reset seen / owned",
  m_lang:"Language: English", m_about:"About / help",
  sort_id:"number", sort_name:"name", sort_total:"stats",
  m_sort_tpl:"Sort: {v}",
  about_title:"ABOUT", ok:"OK",
  about_p1:"A fan-made, offline Pokédex covering all 151 Pokémon of Generation I — all four Game Boy games in one dex. Data, sprites, cries and fonts live in local files next to the page — everything runs without internet.",
  about_p2:"",
  about_p3:"Mark Pokémon as Seen (automatic while browsing) and Owned (pokeball button) to fill your dex status, just like the game. The GAME chips (or key T) switch this dex between the four Gen-1 releases: RED and BLUE (the international pair), GREEN (the Japan-only 1996 version with its older artwork) and YELLOW (its own redrawn sprites and its own rewritten dex texts). Within each game the MONO / COLOR chips pick the sprite set, and every dex entry can be read in either the Red/Blue or the Yellow wording with the R/B · YELLOW selector. The Back button (key B) flips to the in-game back side. The HOW TO CATCH section and the Location Dex (key L) show where every Pokémon lives in each of the four games — wild tables, fishing rods, gifts, trades, Game Corner prizes and fixed encounters, read straight from the original game data. Your settings (game, MONO/COLOR, palette, language, sort, last Pokémon) are remembered between visits.",
  foot_disclaimer:"Fan-made, non-commercial project. Pokémon © Nintendo / Creatures Inc. / GAME FREAK inc.",
  foot_offline:"Runs 100% offline · static site", all_games:"All games",
  reset_confirm:"Reset all Seen/Owned progress?",
  reset_done:"Dex progress cleared.",
  base:"base",
  genus_suffix:"POKéMON",
  evo_conds:{level:"Lv. {n}", special:"Special condition", happiness:"Happiness (day)", happiness_night:"Happiness (night)",
    beauty:"High beauty", affection:"High affection", trade:"Trade", trade_item:"Trade holding {i}",
    use_item:"Use {i}", shed:"Lv. 20 + empty slot + Poké Ball", move:"Knows {m}", full:"Level up"},
  evo_base:"Base form",
  units:{m:"m", kg:"kg"},
  types:{normal:"Normal",fire:"Fire",water:"Water",electric:"Electric",grass:"Grass",ice:"Ice",
    fighting:"Fighting",poison:"Poison",ground:"Ground",flying:"Flying",psychic:"Psychic",bug:"Bug",
    rock:"Rock",ghost:"Ghost",dragon:"Dragon"},
  stats:{hp:"HP",atk:"Attack",def:"Defense",spa:"Sp.Atk",spd:"Sp.Def",spe:"Speed"},
  egg_names:{monster:"Monster",water1:"Water 1",water2:"Water 2",water3:"Water 3",bug:"Bug",flying:"Flying",
    ground:"Field",fairy:"Fairy",plant:"Grass",humanshape:"Human-Like",mineral:"Mineral",
    indeterminate:"Amorphous","no-eggs":"Cannot breed",ditto:"Ditto"},
  habitat_names:{cave:"Cave",forest:"Forest",grassland:"Grassland",mountain:"Mountain",rare:"Rare",
    "rough-terrain":"Rough terrain",sea:"Sea",urban:"Urban","waters-edge":"Water's edge"},
  growth_names:{slow:"Slow",medium:"Medium","medium-slow":"Medium-slow",fast:"Fast",
    "slow-then-very-fast":"Erratic","fast-then-very-slow":"Fluctuating"},
  item_names:{"leaf-stone":"Leaf Stone","fire-stone":"Fire Stone","water-stone":"Water Stone",
    "thunder-stone":"Thunder Stone","moon-stone":"Moon Stone","sun-stone":"Sun Stone",
    "kings-rock":"King's Rock","metal-coat":"Metal Coat","dragon-scale":"Dragon Scale",
    "up-grade":"Up-Grade","deep-sea-tooth":"Deep Sea Tooth","deep-sea-scale":"Deep Sea Scale",
    "prism-scale":"Prism Scale","razor-claw":"Razor Claw","razor-fang":"Razor Fang","oval-stone":"Oval Stone"},
  title:"Pokédex — Generation I (Red · Blue · Green · Yellow)"
},
fa:{
  brand_main:"پوکیدکس کانتو — ۱۵۱ پوکمون",
  kb_hint:"↑↓ پیمایش · / جست‌وجو", home:"خانه",
  search_ph:"جست‌وجوی نام یا شماره...",
  modes:{kanto:"کانتو"},
  showing:"نمایش {a} از {b}", no_results:"پوکمونی پیدا نشد",
  pal_mark:"پالت", cry_mark:"صدا", own_mark:"گرفتم", fav_mark:"علاقه",
  pal_names:{dmg:"گیم‌بوی", pocket:"پاکت"},
  set_mark:"اسپرایت", set_names:{rb:"قرمز/آبی", rbc:"قرمز/آبی رنگی", green:"سبز (ژاپن)", y:"زرد", yc:"زرد رنگی"},
  theme_short:{red:"قرمز", blue:"آبی", green:"سبز", yellow:"زرد"},
  theme_names:{red:"پوکمون قرمز", blue:"پوکمون آبی", green:"پوکمون سبز (ژاپن)", yellow:"پوکمون زرد"},
  theme_tag:{red:"نسل ۱ · نسخه‌ی قرمز", blue:"نسل ۱ · نسخه‌ی آبی", green:"نسل ۱ · نسخه‌ی سبز (ژاپن)", yellow:"نسل ۱ · نسخه‌ی زرد"},
  chip_mono:"تک‌رنگ", chip_color:"رنگی",
  text_ver:"نسخه‌ی متن پوکیدکس",
  m_game_tpl:"بازی: {v}", m_game:"بازی: قرمز",
  back_mark:"پشت", view_front:"جلو", view_back:"پشت", m_view_tpl:"نمایش: {v}", m_back:"نمایش: جلو",
  green_note:"نسخه‌ی سبزِ ۱۹۹۶ که فقط در ژاپن منتشر شد و طراحی‌های قدیمی‌تری دارد — قرمز/آبی جهانی جای آن را با اسپرایت‌های بازطراحی‌شده پر کرد.",
  m_set:"اسپرایت‌ها: قرمز/آبی", m_set_tpl:"اسپرایت‌ها: {v}", m_pal:"پالت: گیم‌بوی",
  pal_color_note:"پالت صفحه — فقط برای اسپرایت تک‌رنگ",
  dex_status:"وضعیت پوکیدکس", seen:"دیده‌شده", own:"گرفته‌شده",
  ht:"قد", wt:"وزن",
  prev:"◀ قبلی", next:"بعدی ▶", random:"تصادفی",
  entry_t:"توضیحات پوکیدکس", stats_t:"آمار پایه", total:"مجموع",
  weak_t:"تناسب انواع", evo_t:"زنجیره تکامل", data_t:"داده‌های پوکمون",
  wk4:"ضعف ×۴", wk2:"ضعف ×۲", whalf:"مقاوم ×½", wquarter:"مقاوم ×¼", wzero:"مصون ×۰", wnorm:"آسیب عادی",
  g1_note:"با مکانیک دقیق انواع نسل اول.",
  no_evo:"این پوکمون تکامل ندارد.",
  evo_extra:"+{n} تکامل دیگر در نسل‌های بعدی",
  evo_unknown:"داده نامشخص — هنوز دیده نشده",
  abilities:"توانایی‌ها", hidden:"پنهان",
  capture:"نرخ گرفتن", capture_hint:"(حداکثر ۲۵۵)", happiness:"شادی پایه",
  growth:"سرعت رشد", exp:"امتیاز تجربه پایه", egg:"گروه تخم", habitat:"زیستگاه",
  gender:"نسبت جنسیت", genderless:"بی‌جنس",
  legendary:"افسانه‌ای", mythical:"اسطوره‌ای", genb:"نسل {n}",
  page:"{a}/{b}",
  start:"استارت", menu:"منو", menu_title:"منوی پوکیدکس",
  m_search:"جست‌وجو", m_random:"پوکمون تصادفی",
  m_cry:"پخش صدای پوکمون", m_pal_tpl:"پالت: {v}",
  m_lcd:"نمایشگر: LCD", m_lcd_tpl:"نمایشگر: LCD {v}",
  lcd_mark:"LCD", lcd_on:"روشن", lcd_off:"خاموش",
  gc_title:"تنظیمات",
  flip_hint:"برای جلو/پشت، اسپرایت را لمس کنید",
  swipe_hint:"سویپ: پیمایش پوکمون‌ها · لمس: جلو/پشت",
  m_fav:"فقط علاقه‌مندی‌ها", m_sort:"ترتیب: شماره", m_reset:"بازنشانی دیده/گرفته‌شده",
  m_lang:"زبان: فارسی", m_about:"درباره / راهنما",
  sort_id:"شماره", sort_name:"نام", sort_total:"آمار",
  m_sort_tpl:"ترتیب: {v}",
  about_title:"درباره", ok:"باشه",
  about_p1:"پوکیدکس طرفداری و آفلاین برای هر ۱۵۱ پوکمون نسل اول، با ظاهر پوکیدکس داخل بازی‌های Pokémon Red و Blue. داده‌ها، اسپرایت‌ها، صدای پوکمون‌ها و فونت‌ها در فایل‌های کنار صفحه ذخیره شده‌اند و همه‌چیز بدون اینترنت کار می‌کند.",
  about_p2:"",
  about_p3:"با مرور هر پوکمون، به‌طور خودکار «دیده‌شده» ثبت می‌شود و با دکمه پوکربال می‌توانید آن را «گرفته‌شده» علامت بزنید تا وضعیت پوکیدکس مثل خود بازی پر شود. متن توضیحات مثل بازی صفحه‌ور می‌خورد — روی جعبه متن کلیک کنید. چیپ‌های بازی (یا کلید T) این دکس را بین چهار نسخه‌ی نسل اول جابه‌جا می‌کنند: قرمز و آبی (نسخه‌های جهانی)، سبز (نسخه‌ی ۱۹۹۶ ژاپن با طرح‌های قدیمی‌تر) و زرد (اسپرایت‌های بازطراحی‌شده و متن‌های بازنویسی‌شده‌ی خودش). داخل هر بازی، چیپ‌های تک‌رنگ/رنگی مجموعه اسپرایت را عوض می‌کنند و با انتخابگر R/B · YELLOW می‌توان هر توضیح را با متن قرمز/آبی یا زرد خواند. دکمه پشت (کلید B) اسپرایت را به نمای پشت بازی برمی‌گرداند. بخش «نحوه‌ی به‌دست‌آوردن» و دکس مکان‌ها (کلید L) نشان می‌دهند هر پوکمون در هر چهار بازی کجا زندگی می‌کند — جدول‌های وحشی، ماهیگیری، هدیه‌ها، تبادل‌ها، جوایز گیم‌کرنر و مواجهه‌های ثابت، مستقیم از داده‌های اصلی بازی. تنظیمات شما (بازی، تک‌رنگ/رنگی، پالت، زبان، ترتیب، آخرین پوکمون) بین دیدارها به خاطر سپرده می‌شود.",
  foot_disclaimer:"پروژه‌ای غیرتجاری ساخته‌ی طرفداران. پوکمون © نینتندو / کرچرز / گیم‌فریک.",
  foot_offline:"کاملاً آفلاین · سایت استاتیک", all_games:"همه بازی‌ها",
  reset_confirm:"همه پیشرفت دیده‌شده/گرفته‌شده پاک شود؟",
  reset_done:"پیشرفت پوکیدکس پاک شد.",
  base:"پایه",
  genus_suffix:"",
  evo_conds:{level:"سطح {n}", special:"شرط ویژه", happiness:"شادی بالا (روز)", happiness_night:"شادی بالا (شب)",
    beauty:"زیبایی بالا", affection:"الفتمندی بالا", trade:"تبادل", trade_item:"تبادل با {i}",
    use_item:"استفاده از {i}", shed:"سطح ۲۰ + جای خالی تیم + پوکربال", move:"دانستن حرکت {m}", full:"رهشی سطح"},
  evo_base:"فرم پایه",
  units:{m:"متر", kg:"کیلوگرم"},
  types:{normal:"معمولی",fire:"آتش",water:"آب",electric:"برقی",grass:"گیاهی",ice:"یخی",
    fighting:"جنگی",poison:"سمی",ground:"زمینی",flying:"پروازی",psychic:"روانی",bug:"حشره‌ای",
    rock:"سنگی",ghost:"روحی",dragon:"اژدها"},
  stats:{hp:"جان",atk:"حمله",def:"دفاع",spa:"حمله ویژه",spd:"دفاع ویژه",spe:"سرعت"},
  egg_names:{monster:"هیولا",water1:"آبی ۱",water2:"آبی ۲",water3:"آبی ۳",bug:"حشره",flying:"پروازی",
    ground:"زمینی",fairy:"پری",plant:"گیاهی",humanshape:"انسان‌نما",mineral:"معدنی",
    indeterminate:"نامشخص","no-eggs":"تخم‌گذاری نمی‌کند",ditto:"دیتو"},
  habitat_names:{cave:"غار",forest:"جنگل",grassland:"علفزار",mountain:"کوهستان",rare:"کمیاب",
    "rough-terrain":"منطقه ناهموار",sea:"دریا",urban:"شهری","waters-edge":"کنار آب"},
  growth_names:{slow:"کند",medium:"متوسط","medium-slow":"نسبتاً کند",fast:"سریع",
    "slow-then-very-fast":"بی‌قاعده","fast-then-very-slow":"نوسانی"},
  item_names:{"leaf-stone":"سنگ برگ","fire-stone":"سنگ آتش","water-stone":"سنگ آب",
    "thunder-stone":"سنگ رعد","moon-stone":"سنگ ماه","sun-stone":"سنگ خورشید",
    "kings-rock":"سنگ پادشاهی","metal-coat":"پوشش فلزی","dragon-scale":"فلس اژدها",
    "up-grade":"ارتقاگر","deep-sea-tooth":"دندان دریای عمیق","deep-sea-scale":"فلس دریای عمیق",
    "prism-scale":"فلس منشوری","razor-claw":"پنجه تیز","razor-fang":"دندان تیز","oval-stone":"سنگ بیضی"},
  title:"پوکیدکس — نسل ۱ (قرمز · آبی · سبز · زرد)"
}};

/* ===== defensive type chart — authentic Generation I (incl. famous R/B quirks:
   Ghost x0 vs Psychic (the Gen-1 bug), Bug x2 vs Poison, Poison x2 vs Bug, no Dark/Steel) ===== */
const CHART = {
  normal:{rock:.5,ghost:0},
  fire:{fire:.5,water:.5,grass:2,ice:2,bug:2,rock:.5,dragon:.5},
  water:{fire:2,water:.5,grass:.5,ground:2,rock:2,dragon:.5},
  electric:{water:2,electric:.5,grass:.5,ground:0,flying:2,dragon:.5},
  grass:{fire:.5,water:2,grass:.5,poison:.5,ground:2,flying:.5,bug:.5,rock:2,dragon:.5},
  ice:{water:.5,grass:2,ice:.5,ground:2,flying:2,dragon:2},
  fighting:{normal:2,ice:2,poison:.5,flying:.5,psychic:.5,rock:2,ghost:0},
  poison:{grass:2,poison:.5,ground:.5,bug:2,rock:.5,ghost:.5},
  ground:{fire:2,electric:2,grass:.5,poison:2,flying:0,bug:.5,rock:2},
  flying:{electric:.5,grass:2,fighting:2,bug:2,rock:.5},
  psychic:{fighting:.5,poison:2,psychic:.5},
  bug:{fire:.5,grass:2,fighting:.5,poison:2,flying:.5,psychic:2,ghost:.5},
  rock:{fire:2,ice:2,fighting:.5,flying:2,bug:2,ground:.5},
  ghost:{normal:0,psychic:0,ghost:2},
  dragon:{dragon:2}
};
const TYPE_ORDER = ["normal","fire","water","electric","grass","ice","fighting","poison","ground","flying","psychic","bug","rock","ghost","dragon"];
const TYPE_COLOR = {normal:"#A8A77A",fire:"#EE8130",water:"#6390F0",electric:"#F7D02C",grass:"#7AC74C",ice:"#96D9D6",fighting:"#C22E28",poison:"#A33EA1",ground:"#E2BF65",flying:"#A98FF3",psychic:"#F95587",bug:"#A6B91A",rock:"#B6A136",ghost:"#735797",dragon:"#6F35FC"};
const STAT_COLOR = {hp:"#f0a030",atk:"#e05038",def:"#4890d0",spa:"#a870d8",spd:"#58b868",spe:"#f0d048"};
const ABIL_FA = {"pickup":"جمع‌آوری","plus":"مثبت","poison-heal":"درمان زهر","poison-point":"نقطه زهر","poison-touch":"لمس زهر","prankster":"شیطنت‌گر","pressure":"فشار","protean":"تغییرپذیر","pure-power":"قدرت خالص","quick-feet":"پاهای سریع","rain-dish":"پارچ باران","rattled":"هراسان","reckless":"بی‌پروا","regenerator":"بازسازی‌گر","rivalry":"رقابت","rock-head":"سر سنگی","rough-skin":"پوست خشن","run-away":"گریز","sand-force":"نیروی شن","sand-rush":"تعجیل شن","sand-stream":"جریان شن","sand-veil":"پرده شن","sap-sipper":"شیره‌خوار","scrappy":"جسور","serene-grace":"لطف آرام","shadow-tag":"برچسب سایه","shed-skin":"ریختن پوست","sheer-force":"نیروی خشمگین","shell-armor":"زره پوسته","shield-dust":"گرد سپر","simple":"ساده","skill-link":"پیوند مهارت","sniper":"تیرانداز","snow-cloak":"پرده برف","solar-power":"توان خورشیدی","solid-rock":"سنگ محکم","soundproof":"دافع صدا","speed-boost":"افزایش سرعت","stall":"دیرکرد","static":"بار الکتریکی","adaptability":"انطباق‌پذیری","aftermath":"پیامد","air-lock":"قفل هوا","analytic":"تحلیل‌گر","anger-point":"نقطه‌ی خشم","anticipation":"پیش‌بینی","arena-trap":"تله‌ی زمین","battle-armor":"زره‌ی نبرد","big-pecks":"سینه‌ی پهن","blaze":"شعله‌ور","chlorophyll":"کلروفیل","clear-body":"بدن صاف","cloud-nine":"آسمان صاف","color-change":"تغییررنگ","competitive":"رقابت‌جو","compound-eyes":"چشم مرکب","contrary":"وارونه","cursed-body":"بدن نفرین‌شده","cute-charm":"جذابیت","damp":"نمناک","defiant":"سرکش","download":"بارگیری","drizzle":"باران","drought":"خشکسالی","dry-skin":"پوست خشک","early-bird":"بیدارباش زود","effect-spore":"اسپور اثر","filter":"فیلتر","flame-body":"بدن آتشین","flash-fire":"آتش سریع","forecast":"پیش‌بینی","forewarn":"پیش‌آگاهی","friend-guard":"محافظ دوست","frisk":"جست‌وجوگر","gluttony":"شکم‌بارگی","guts":"شجاعت","harvest":"برداشت محصول","healer":"درمانگر","heavy-metal":"فلز سنگین","honey-gather":"جمع‌آوری عسل","huge-power":"قدرت عظیم","hustle":"تلاشگر","hydration":"آب‌رسانی","hyper-cutter":"برنده برتر","ice-body":"بدن یخی","illuminate":"نورافکن","immunity":"ایمنی","imposter":"تقلیدگر","infiltrator":"نفوذگر","inner-focus":"تمرکز درونی","insomnia":"بی‌خوابی","intimidate":"ترساندن","iron-fist":"مشت آهنی","justified":"عادلانه","keen-eye":"چشم تیزبین","leaf-guard":"محافظ برگ","levitate":"شناور","light-metal":"فلز سبک","lightning-rod":"میله برق‌گیر","limber":"منعطف","liquid-ooze":"چسب مایع","magic-bounce":"انعکاس جادویی","magic-guard":"محافظ جادویی","magma-armor":"زره ماگما","magnet-pull":"آهنربای قوی","marvel-scale":"فلس شگفت‌انگیز","minus":"منفی","mold-breaker":"شکننده قالب","moody":"مزاج متغیر","moxie":"اعتماد به نفس","multiscale":"مولتی‌اسکیل","natural-cure":"درمان طبیعی","neutralizing-gas":"گاز خنثی‌کننده","no-guard":"بدون گریز","normalize":"نرمال‌سازی","oblivious":"غافل","overcoat":"روکش محافظ","overgrow":"رشد افراطی","own-tempo":"ریتم خود","pickpocket":"دزدی","steadfast":"پایداری","stench":"بوی بد","sticky-hold":"چسبندگی","storm-drain":"جاذبه آب","sturdy":"استحکام","suction-cups":"کفچسب","super-luck":"بخت فوق‌العاده","swarm":"توده","swift-swim":"شنا سریع","synchronize":"همگام‌سازی","tangled-feet":"پاهای گره‌خورده","technician":"تکنسین","telepathy":"تلپاتی","thick-fat":"چربی ضخیم","tinted-lens":"عدسی رنگی","torrent":"سیلاب","toxic-boost":"تقویت سمی","trace":"پیگیری","truant":"غیبت","unaware":"ناخودآگاه","unburden":"رهایی","unnerve":"بی‌قراری","vital-spirit":"روح حیاتی","volt-absorb":"جذب برق","water-absorb":"جذب آب","water-veil":"پرده آب","weak-armor":"زره شکننده","white-smoke":"دود سفید","wind-rider":"سوار باد","wonder-guard":"محافظت شگفت‌انگیز","wonder-skin":"پوست شگفت‌انگیز"};

/* ===== helpers ===== */
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const pad3 = n => String(n).padStart(3, "0");
const faD = n => String(n).replace(/[0-9]/g, d => "۰۱۲۳۴۵۶۷۸۹"[+d]).replace(/\./g,"٫").replace(/%/g,"٪");
const num = n => state.lang === "fa" ? faD(n) : String(n);
const t = k => { const v = k.split(".").reduce((o,p)=>o&&o[p], I18N[state.lang]); return v === undefined ? k : v; };
const tpl = (s, obj) => s.replace(/\{(\w+)\}/g, (_,k)=> obj[k] !== undefined ? obj[k] : "{"+k+"}");
const PMAP = {};
DATA.forEach(p => PMAP[p.id] = p);
const total = p => p.stats.hp + p.stats.atk + p.stats.def + p.stats.spa + p.stats.spd + p.stats.spe;
const MODE_RANGE = { kanto:[1,151] };

/* sprites: selected set; the DMG/Pocket palette only applies to the mono set */
function spriteURL(id, pal, back){
  const set = SPRITE_SETS[state.set] || SPRITE_SETS.rb;
  const bank = (back && set.back) ? set.back : set.files;
  if (set.color) return bank[id] || bank[String(id)] || "";
  const files = bank[pal || state.pal] || {};
  return files[id] || files[String(id)] || "";
}
function cryURL(id){
  return "assets/audio/cries/" + id + ".ogg";
}
function ballIcon(kind){ /* owned | seen */
  if (kind === "owned") return '<svg class="ball" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5" fill="#f8f8f0" stroke="#28283a" stroke-width="2"/><path d="M3 12a9.5 9.5 0 0 1 18 0z" fill="#e04038" stroke="#28283a" stroke-width="1.6"/><rect x="2.5" y="10.6" width="19" height="2.8" fill="#28283a"/><circle cx="12" cy="12" r="3.4" fill="#f8f8f0" stroke="#28283a" stroke-width="1.8"/><circle cx="12" cy="12" r="1.4" fill="#cfd8d3"/></svg>';
  return '<svg class="ball" viewBox="0 0 24 24" style="filter:grayscale(1) opacity(.45)"><circle cx="12" cy="12" r="9.5" fill="#f8f8f0" stroke="#28283a" stroke-width="2"/><path d="M3 12a9.5 9.5 0 0 1 18 0z" fill="#e04038" stroke="#28283a" stroke-width="1.6"/><rect x="2.5" y="10.6" width="19" height="2.8" fill="#28283a"/><circle cx="12" cy="12" r="3.4" fill="#f8f8f0" stroke="#28283a" stroke-width="1.8"/></svg>';
}
const ICON = {
  star:'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6.3 6.9.8-5.1 4.7 1.4 6.8L12 17.2 5.9 20.6l1.4-6.8L2.2 9.1l6.9-.8z"/></svg>',
  dice:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="4"/><circle cx="8.5" cy="8.5" r="1.6" fill="currentColor" stroke="none"/><circle cx="15.5" cy="8.5" r="1.6" fill="currentColor" stroke="none"/><circle cx="8.5" cy="15.5" r="1.6" fill="currentColor" stroke="none"/><circle cx="15.5" cy="15.5" r="1.6" fill="currentColor" stroke="none"/></svg>',
  left:'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14.5 5l-7 7 7 7 1.8-1.8L11.1 12l5.2-5.2z"/></svg>',
  right:'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M9.5 5l7 7-7 7-1.8-1.8L12.9 12 7.7 6.8z"/></svg>'
};

/* ===== state ===== */
const store = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k) || "null"); return v === null ? d : v; } catch(e){ return d; } };
const save = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch(e){} };
const state = {
  lang: store("pkd_lang", "en") === "fa" ? "fa" : "en",
  sel: 25, q: "", mode: "kanto", type: null,
  pal: store("pkd_g1_pal", "dmg") === "pocket" ? "pocket" : "dmg",
  theme: ["red","blue","green","yellow"].indexOf(store("pkd_g1_theme", "red")) !== -1 ? store("pkd_g1_theme", "red") : "red",
  set: ["rb","rbc","green","y","yc"].indexOf(store("pkd_g1_set", "rb")) !== -1 ? store("pkd_g1_set", "rb") : "rb",
  text: store("pkd_g1_text", null) === "y" ? "y" : (store("pkd_g1_text", null) === "rb" ? "rb" : null),
  back: store("pkd_g1_back", "front") === "back",
  lcd: store("pkd_g1_lcd", false) === true,
  favOnly: store("pkd_g1_favonly", false) === true,
  sort: ["id","name","total"].indexOf(store("pkd_g1_sort", "id")) !== -1 ? store("pkd_g1_sort", "id") : "id",
  page: 1,
  favs: new Set(store("pkd_g1_favs", [])),
  seen: new Set(store("pkd_g1_seen", [])),
  own:  new Set(store("pkd_g1_own", []))
};
const isMobile = () => window.matchMedia("(max-width:860px)").matches;

/* ===== GAME THEMES — which of the four Gen-1 games the dex is "running" =====
   set family: red/blue share the international sprites; green (Japan) is
   mono-only; yellow has its own redrawn sprites + its own dex texts. */
const THEMES = {
  red:    { sets:["rb","rbc"], def:"rb",    text:"rb", moves:"MD_RB", cls:"theme-red" },
  blue:   { sets:["rb","rbc"], def:"rb",    text:"rb", moves:"MD_RB", cls:"theme-blue" },
  green:  { sets:["green"],    def:"green", text:"rb", moves:"MD_RB", cls:"theme-green" },
  yellow: { sets:["y","yc"],   def:"y",     text:"y",  moves:"MD_Y",  cls:"theme-yellow" }
};
const THEME_ORDER = ["red","blue","green","yellow"];
function activeMoves(){ try { return MD_RB && MD_Y ? (THEMES[state.theme].moves === "MD_Y" ? MD_Y : MD_RB) : null; } catch(e){ return null; } }
function applyTheme(){
  const th = THEMES[state.theme] || THEMES.red;
  document.body.classList.remove("theme-red","theme-blue","theme-green","theme-yellow");
  document.body.classList.add(th.cls);
  /* switching games keeps the user's MONO/COLOR preference when the new
     game has both sets (green is mono-only) — pkd_g1_color */
  if (th.sets.indexOf(state.set) === -1){
    const pref = store("pkd_g1_color", null);
    let pick = th.def;
    if (pref === "color" || pref === "mono"){
      const match = th.sets.filter(s => (SPRITE_SETS[s].color === true) === (pref === "color"));
      if (match.length) pick = match[0];
    }
    state.set = pick;
    save("pkd_g1_set", state.set);
  }
  /* dex text follows the game unless the reader picked a wording explicitly */
  if (state.text === null) state.text = th.text;
  if (typeof MovesUI !== "undefined"){
    const md = activeMoves();
    if (md) MovesUI.setGame(md);
  }
  const t1 = document.querySelector("#topbar .t1");
  if (t1) t1.textContent = t("theme_tag." + state.theme);
}
function toggleTheme(th){
  if (!THEMES[th] || th === state.theme) return;
  state.theme = th;
  save("pkd_g1_theme", th);
  /* state.text: null = follow each game's own wording; an explicit R/B ·
     YELLOW choice is remembered across games (pkd_g1_text) */
  if (store("pkd_g1_text", null) === null) state.text = null;
  state.page = 1;
  applyTheme();
  renderThemeRow(); renderSetRow();
  renderSpritePane(); renderDetail();
  refreshMenuLabels();
  if (typeof LocUI !== "undefined" && LocUI.syncGame) LocUI.syncGame();
}
function cycleTheme(){
  const i = THEME_ORDER.indexOf(state.theme);
  toggleTheme(THEME_ORDER[(i + 1) % THEME_ORDER.length]);
}

/* name display per language */
function dispName(p){ return state.lang === "fa" && p.fa ? p.fa : p.display; }
function dispGenus(p){
  if (state.lang === "fa") return p.genus_fa || p.genus;
  return (p.cat || p.genus || "") + " " + t("genus_suffix");
}
function dispAbility(name){
  if (state.lang === "fa"){ const k = name.toLowerCase().replace(/\s+/g,"-"); if (ABIL_FA[k]) return ABIL_FA[k]; }
  return name.replace(/-/g," ").replace(/\b\w/g, c=>c.toUpperCase());
}
function dispItem(n){
  const map = I18N[state.lang].item_names;
  return map[n] || n.replace(/-/g," ").replace(/\b\w/g, c=>c.toUpperCase());
}
function typeName(x){ return I18N[state.lang].types[x] || x; }
function statName(k){ return I18N[state.lang].stats[k] || k; }

/* ===== filtering ===== */
function filtered(){
  const [lo, hi] = MODE_RANGE[state.mode];
  let arr = DATA.filter(p => {
    if (p.id < lo || p.id > hi) return false;
    if (state.type && p.types.indexOf(state.type) === -1) return false;
    if (state.favOnly && !state.favs.has(p.id)) return false;
    if (state.q){
      const q = state.q.trim().toLowerCase();
      if (q){
        if (/^[0-9\u06F0-\u06F9]+$/.test(q)){
          const n = parseInt(q.replace(/[\u06F0-\u06F9]/g, d => "۰۱۲۳۴۵۶۷۸۹".indexOf(d)), 10);
          if (String(p.id) !== String(n) && !pad3(p.id).startsWith(String(n)) && !String(p.id).startsWith(String(n))) return false;
        } else {
          const hay = (p.display + " " + p.name + " " + (p.fa || "")).toLowerCase();
          if (hay.indexOf(q) === -1) return false;
        }
      }
    }
    return true;
  });
  if (state.sort === "name") arr = arr.slice().sort((a,b)=> a.display.localeCompare(b.display));
  else if (state.sort === "total") arr = arr.slice().sort((a,b)=> total(b)-total(a) || a.id-b.id);
  else arr = arr.slice().sort((a,b)=> a.id-b.id);
  return arr;
}

/* ===== tabs (single KANTO dex, like the game) ===== */
function renderTabs(){
  $("#tabs").innerHTML = ["kanto"].map(m =>
    '<button class="tab' + (state.mode===m?" on":"") + '" data-m="' + m + '">' + t("modes."+m) + '</button>'
  ).join("");
}

/* ===== type chips ===== */
function renderChips(){
  $("#typeRow").innerHTML = TYPE_ORDER.map(tp =>
    '<span class="chip T-' + tp + (state.type===tp?" on":"") + '" data-t="' + tp + '" title="' + esc(typeName(tp)) + '">' + esc(typeName(tp)) + '</span>'
  ).join("");
}

/* ===== list ===== */
function rowHtml(p){
  const sel = p.id === state.sel ? " sel" : "";
  const fav = state.favs.has(p.id) ? '<span class="fav-star">★</span>' : "";
  const seen = state.seen.has(p.id), own = state.own.has(p.id);
  const ball = own ? ballIcon("owned") : (seen ? ballIcon("seen") : "");
  const dots = p.types.map(tp => '<i class="dot" style="background:' + TYPE_COLOR[tp] + '" title="' + esc(typeName(tp)) + '"></i>').join("");
  return '<li class="row' + sel + '" data-id="' + p.id + '">' +
    '<span class="bicon">' + ball + '</span>' +
    '<span class="no">' + num(p.id) + '</span>' +
    '<span class="nm"><bdi>' + esc(dispName(p)) + '</bdi>' + fav + '</span>' +
    '<span class="tw">' + dots + '</span></li>';
}
function renderList(){
  const arr = filtered();
  $("#countLabel").textContent = tpl(t("showing"), {a:num(arr.length), b:num(DATA.length)});
  $("#list").innerHTML = arr.length ? arr.map(rowHtml).join("") : '<li class="empty">' + esc(t("no_results")) + '</li>';
}
function scrollSelIntoView(){
  const el = document.querySelector('.row[data-id="' + state.sel + '"]');
  const list = $("#list");
  if (!el || !list) return;
  const top = el.getBoundingClientRect().top - list.getBoundingClientRect().top + list.scrollTop;
  list.scrollTop = Math.max(0, top - (list.clientHeight - el.offsetHeight) / 2);
}

/* ===== counters ===== */
function renderCounters(){
  let s = 0, o = 0, n = 0;
  for (let i = 1; i <= 151; i++){ if (PMAP[i]){ n++; if (state.seen.has(i)) s++; if (state.own.has(i)) o++; } }
  $("#cntRows").innerHTML =
    '<div class="cRow"><span class="reg">' + esc(t("modes.kanto")) + '</span>' +
    '<span class="vals">' + esc(t("seen")) + ' <b>' + num(s) + '</b> · ' + esc(t("own")) + ' <b>' + num(o) + '</b> / ' + num(n) + '</span></div>';
}

/* ===== weaknesses ===== */
function weaknesses(types){
  const out = { "4":[], "2":[], "0.5":[], "0.25":[], "0":[] };
  for (const atk of Object.keys(CHART)){
    let m = 1;
    for (const d of types) m *= (CHART[atk][d] === undefined ? 1 : CHART[atk][d]);
    if (out[String(m)]) out[String(m)].push(atk);
  }
  return out;
}
function wkHtml(p){
  const w = weaknesses(p.types);
  const groups = [["4","wk4","x4"],["2","wk2","x2"],["0.5","whalf","half"],["0.25","wquarter","quarter"],["0","wzero","zero"]];
  let h = "";
  for (const [k, key, cls] of groups){
    if (!w[k].length) continue;
    h += '<div class="wk-group"><span class="wk-label ' + cls + '">' + esc(t(key)) + '</span>' +
      w[k].map(tp => '<span class="tmini T-' + tp + '">' + esc(typeName(tp)) + '</span>').join("") + '</div>';
  }
  if (!h) h = '<div class="wk-group"><span class="wk-label" style="color:#5c8a72">' + esc(t("wnorm")) + '</span></div>';
  return h + '<div class="wk-note">' + esc(t("g1_note")) + '</div>';
}

/* ===== evolution ===== */
function condText(c){
  if (!c) return t("evo_conds.full");
  const ec = t("evo_conds");
  switch (c.t){
    case "level": return c.lvl ? tpl(ec.level, {n: num(c.lvl)}) : ec.special;
    case "happiness": return ec.happiness;
    case "beauty": return ec.beauty;
    case "affection": return ec.affection;
    case "trade": return c.item ? tpl(ec.trade_item, {i: dispItem(c.item)}) : ec.trade;
    case "use-item": return tpl(ec.use_item, {i: dispItem(c.item)});
    case "shed": return ec.shed;
    default: return c.move ? tpl(ec.move, {m: c.move.replace(/-/g," ")}) : ec.special;
  }
}
function evoHtml(p){
  const cid = EVOLUTIONS.bySpecies[p.id];
  if (!cid) return "";
  const ch = EVOLUTIONS.chains[cid];
  const members = ch.members.filter(m => m <= 151 && PMAP[m]);
  const extra = ch.members.length - members.length;
  if (members.length < 2) return '<div class="evoNote">' + esc(t("no_evo")) + '</div>';
  const root = ch.members[0];
  const caps = {};
  for (const e of ch.edges) if (caps[e.to] === undefined) caps[e.to] = e.cond;
  const depth = {}; depth[root] = 0;
  const queue = [root];
  while (queue.length){
    const cur = queue.shift();
    for (const e of ch.edges){
      if (e.from === cur && depth[e.to] === undefined){ depth[e.to] = depth[cur] + 1; queue.push(e.to); }
    }
  }
  const byD = {};
  for (const m of members){ const d = depth[m] === undefined ? 0 : depth[m]; (byD[d] = byD[d] || []).push(m); }
  let h = '<div class="evo-wrap">';
  const ds = Object.keys(byD).map(Number).sort((a,b)=>a-b);
  ds.forEach((d, i) => {
    if (i > 0) h += '<div class="evoLink">▼</div>';
    h += '<div class="evoRow">' + byD[d].map(mid => {
      const q = PMAP[mid];
      const cap = mid === root ? t("evo_base") : condText(caps[mid]);
      return '<div class="evo' + (mid === state.sel ? " cur" : "") + '" data-id="' + mid + '">' +
        '<div class="espr"><img src="' + spriteURL(mid) + '" alt="' + esc(q.display) + '"></div>' +
        '<div class="en">' + esc(dispName(q)) + '</div>' +
        '<div class="ec">' + esc(cap) + '</div></div>';
    }).join("") + '</div>';
  });
  if (extra > 0) h += '<div class="evoNote">' + tpl(t("evo_extra"), {n: num(extra)}) + '</div>';
  h += '</div>';
  return h;
}

/* ===== sprite pane ===== */
function renderSpritePane(){
  const p = PMAP[state.sel];
  if (!p) return;
  const img = $("#sprImg");
  img.src = spriteURL(p.id, null, state.back);
  img.alt = dispName(p);
  $("#sprNo").textContent = "#" + pad3(p.id);
  $("#sprName").textContent = dispName(p);
  $("#sprTypes").innerHTML = p.types.map(tp =>
    '<span class="tbadge T-' + tp + '">' + esc(typeName(tp)) + '</span>').join("");
  renderSetRow();
  $("#btnPal").disabled = SPRITE_SETS[state.set].color === true;
  $("#btnPal").title = SPRITE_SETS[state.set].color ? t("pal_color_note") : t("pal_mark");
  $("#btnBack").classList.toggle("on", state.back);
  $("#btnBack").setAttribute("aria-pressed", state.back ? "true" : "false");
  $("#btnBack").title = tpl(t("m_view_tpl"), {v: t(state.back ? "view_back" : "view_front")});
  $("#sprBox").title = t("flip_hint");
  const gn = $("#setNote");
  if (gn){ gn.classList.toggle("hidden", state.theme !== "green"); gn.textContent = t("green_note"); }
  $("#htVal").textContent = num((p.height_dm / 10).toFixed(1)) + " " + t("units.m");
  $("#wtVal").textContent = num((p.weight_hg / 10).toFixed(1)) + " " + t("units.kg");
  const ownB = $("#btnOwn"), favB = $("#btnFav");
  ownB.classList.toggle("on", state.own.has(p.id));
  ownB.querySelector("span").textContent = state.own.has(p.id) ? t("own") : t("own_mark");
  favB.classList.toggle("on", state.favs.has(p.id));
}

/* ===== sprite set (MONO / COLOR within the active game) ===== */
function toggleSet(s){
  if (!SPRITE_SETS[s]) return;
  if (THEMES[state.theme].sets.indexOf(s) === -1) return;   /* other games' sets live behind their theme */
  state.set = s;
  save("pkd_g1_set", state.set);
  save("pkd_g1_color", SPRITE_SETS[s].color ? "color" : "mono");   /* remembered across games */
  renderSpritePane();
  renderDetail();
  /* item icons ride the same MONO/COLOR switch as the sprites */
  if (typeof ItemsUI !== "undefined" && ItemsUI.syncIcons) ItemsUI.syncIcons();
}
/* hint for the Item Dex: which icon style matches the active sprite set */
window.__itemIconHint = function(){
  try { return SPRITE_SETS[state.set] && SPRITE_SETS[state.set].color ? "color" : "gb"; }
  catch(e){ return "gb"; }
};
function renderThemeRow(){
  const el = $("#themeRow");
  if (!el) return;
  const chip = th =>
    '<button class="tchip' + (state.theme === th ? " on" : "") + '" data-th="' + th +
    '" title="' + esc(t("theme_names." + th)) + '"><span class="dot"></span>' + esc(t("theme_short." + th)) + '</button>';
  /* RED + BLUE share one cartridge group (same game, different colour);
     GREEN (Japan) and YELLOW get a group of their own */
  el.innerHTML =
    '<div class="gcGroup">' + chip("red") + chip("blue") + '</div>' +
    '<div class="gcGroup">' + chip("green") + '</div>' +
    '<div class="gcGroup">' + chip("yellow") + '</div>';
}
function renderSetRow(){
  const el = $("#setRow");
  if (!el) return;
  el.innerHTML = THEMES[state.theme].sets.map(s =>
    '<button class="setchip' + (state.set === s ? " on" : "") + '" data-set="' + s +
    '" title="' + esc(t("set_names." + s)) + '">' +
    esc(SPRITE_SETS[s].color ? t("chip_color") : t("chip_mono")) + '</button>'
  ).join("");
}

/* ===== front / back view ===== */
function toggleBack(){
  state.back = !state.back;
  save("pkd_g1_back", state.back ? "back" : "front");
  renderSpritePane();
  renderDetail();
}
/* ===== detail ===== */
function statCls(v){ return v < 50 ? " low" : v < 80 ? " mid" : ""; }
function flavorPages(p){
  const yl = state.text === "y";
  const a = yl ? p.ey1 : p.e1, b = yl ? p.ey2 : p.e2;
  if (state.lang === "fa"){
    const fa = yl ? p.flavor_fa_y : p.flavor_fa;
    return fa ? [fa] : [((a) || []).join(" ")];
  }
  const pgs = [];
  if (a && a.length) pgs.push(a.join(" "));
  if (b && b.length) pgs.push(b.join(" "));
  return pgs.length ? pgs : [""];
}
function renderDetail(){
  const p = PMAP[state.sel];
  if (!p) return;
  const pages = flavorPages(p);
  if (state.page > pages.length) state.page = 1;
  const pg = Math.min(state.page, pages.length);
  const multi = pages.length > 1 && state.lang === "en";
  const flavorHtml = '<div class="flavor' + (multi ? " paged" : "") + '" id="flavorBox">' +
    esc(pages[pg - 1] || "") +
    (multi ? '<span class="pgno">' + tpl(t("page"), {a:num(pg), b:num(pages.length)}) + '</span>' : '') +
    '</div>';
  const T = total(p);
  const curText = state.text || THEMES[state.theme].text;   /* null = follow the game's own wording */
  const statRows = ["hp","atk","def","spa","spd","spe"].map(k =>
    '<div class="statrow"><span class="stat-l">' + esc(statName(k)) + '</span>' +
    '<span class="stat-track"><span class="stat-fill" style="width:' + Math.min(100, p.stats[k]/1.6) + '%;background:linear-gradient(90deg,' + STAT_COLOR[k] + 'cc,' + STAT_COLOR[k] + ')"></span></span>' +
    '<span class="stat-v">' + num(p.stats[k]) + '</span></div>').join("");

  let gender;
  if (p.genderRate < 0) gender = esc(t("genderless"));
  else {
    const fp = p.genderRate / 8 * 100, mp = 100 - fp;
    gender = '<span class="gbar"><span class="m" style="width:' + mp + '%"></span><span class="f" style="width:' + fp + '%"></span></span>' +
      '<span class="glegend">♂ ' + num(mp.toFixed(1)) + ' — ♀ ' + num(fp.toFixed(1)) + '</span>';
  }
  const abils = p.abilities.map(a =>
    '<span class="abchip" title="' + esc(a.name) + '">' + esc(dispAbility(a.name)) +
    (a.hidden ? '<span class="hid">' + esc(t("hidden")) + '</span>' : '') + '</span>').join("");

  const eggLine = p.egg.map(e => t("egg_names."+e) || e).join(state.lang === "fa" ? "، " : ", ");
  const badges =
    '<span class="tagchip tag-gen">' + esc(tpl(t("genb"), {n: num(1)})) + '</span>' +
    (p.legendary ? '<span class="tagchip tag-legend">' + esc(t("legendary")) + '</span>' : '') +
    (p.mythical ? '<span class="tagchip tag-mythic">' + esc(t("mythical")) + '</span>' : '');

  $("#detailPane").innerHTML =
    '<div class="dhead">' +
      '<span class="dnm">' + esc(dispName(p)) + '</span>' +
      '<span class="dno">#' + pad3(p.id) + '</span>' +
      '<span class="dgenus">' + esc(dispGenus(p)) + '</span>' +
      '<span class="dbadges">' + badges + '</span>' +
    '</div>' +

    '<div class="sec"><div class="sec-t"><span>' + esc(t("entry_t")) + '</span>' +
      '<span class="verSel" role="group" aria-label="' + esc(t("text_ver")) + '" title="' + esc(t("text_ver")) + '">' +
        '<button class="vbtn' + (curText === "rb" ? " on" : "") + '" data-txt="rb">R/B</button>' +
        '<button class="vbtn' + (curText === "y" ? " on" : "") + '" data-txt="y">YELLOW</button>' +
      '</span></div>' + flavorHtml + '</div>' +

    '<div class="sec"><div class="sec-t">' + esc(t("stats_t")) + '</div>' + statRows +
      '<div class="statrow total"><span class="stat-l">' + esc(t("total")) + '</span>' +
      '<span class="stat-track"><span class="stat-fill" style="width:' + Math.min(100, T/7.8) + '%;background:linear-gradient(90deg,#e8a61388,#e8a613)"></span></span>' +
      '<span class="stat-v">' + num(T) + '</span></div></div>' +

    '<div class="sec"><div class="sec-t">' + esc(t("weak_t")) + '</div>' + wkHtml(p) + '</div>' +

    '<div class="sec"><div class="sec-t">' + esc(t("evo_t")) + '</div>' + evoHtml(p) + '</div>' +

    '<div class="sec"><div class="sec-t">' + esc(t("data_t")) + '</div><div class="igrid">' +
      '<div class="item"><div class="k">' + esc(t("abilities")) + '</div><div class="v">' + abils + '</div></div>' +
      '<div class="item"><div class="k">' + esc(t("capture")) + '</div><div class="v">' + num(p.capture) + ' <small>' + esc(t("capture_hint")) + '</small></div></div>' +
      '<div class="item"><div class="k">' + esc(t("happiness")) + '</div><div class="v">' + num(p.happiness) + '</div></div>' +
      '<div class="item"><div class="k">' + esc(t("exp")) + '</div><div class="v">' + num(p.baseExp) + '</div></div>' +
      '<div class="item"><div class="k">' + esc(t("growth")) + '</div><div class="v">' + esc(t("growth_names."+p.growth) || p.growth) + '</div></div>' +
      '<div class="item"><div class="k">' + esc(t("egg")) + '</div><div class="v">' + esc(eggLine) + '</div></div>' +
      (p.habitat ? '<div class="item"><div class="k">' + esc(t("habitat")) + '</div><div class="v">' + esc(t("habitat_names."+p.habitat) || p.habitat) + '</div></div>' : '') +
      '<div class="item wide"><div class="k">' + esc(t("gender")) + '</div><div class="v">' + gender + '</div></div>' +
    '</div></div>' +

        (typeof MovesUI !== "undefined" ? MovesUI.sectionHTML(p) : "") +

        (typeof LocUI !== "undefined" && LocUI.sectionHTML ? LocUI.sectionHTML(p) : "") +

    '<div class="d-nav">' +
      '<button class="btn" id="bPrev">' + ICON.left + ' <span>' + esc(t("prev")) + '</span></button>' +
      '<button class="btn" id="bNext"><span>' + esc(t("next")) + '</span> ' + ICON.right + '</button>' +
      '<button class="btn sec" id="bRand">' + ICON.dice + ' <span>' + esc(t("random")) + '</span></button>' +
    '</div>';

  const cf = $("#cardFlavor");
  if (cf){
    cf.dataset.pgs = String(pages.length);
    cf.innerHTML =
      '<div class="cfTop"><span class="cfGenus">' + esc(dispGenus(p)) + '</span>' +
      (multi ? '<span class="pgno">' + tpl(t("page"), {a:num(pg), b:num(pages.length)}) + '</span>' : '') +
      '</div><div class="cfTxt">' + esc(pages[pg - 1] || "") + '</div>';
  }
  $("#bPrev").addEventListener("click", () => next(-1));
  $("#bNext").addEventListener("click", () => next(1));
  $("#bRand").addEventListener("click", randomPick);
  const fb = $("#flavorBox");
  if (fb && multi) fb.addEventListener("click", () => { state.page = state.page >= pages.length ? 1 : state.page + 1; renderDetail(); });
  document.querySelectorAll("#detailPane [data-txt]").forEach(el =>
    el.addEventListener("click", () => { state.text = el.dataset.txt; save("pkd_g1_text", state.text); renderDetail(); }));
  document.querySelectorAll("#detailPane .evo").forEach(el =>
    el.addEventListener("click", () => select(parseInt(el.dataset.id, 10))));
  if (typeof MovesUI !== "undefined") MovesUI.wire(p);
  if (typeof LocUI !== "undefined" && LocUI.wire) LocUI.wire(p);

}

/* ===== cries ===== */
let cryAudio = null;
function playCry(){
  const url = cryURL(state.sel);
  if (!url) return;
  try {
    if (cryAudio){ cryAudio.pause(); }
    cryAudio = new Audio(url);
    cryAudio.volume = 0.6;
    cryAudio.play();
    const b = $("#btnCry");
    b.classList.add("on");
    setTimeout(() => b.classList.remove("on"), 900);
  } catch(e){}
}

/* ===== selection ===== */
function markSeen(id){
  if (!state.seen.has(id)){
    state.seen.add(id);
    save("pkd_g1_seen", [...state.seen]);
  }
}
function select(id, opts){
  state.sel = id;
  state.page = 1;
  save("pkd_g1_sel", id);
  markSeen(id);
  renderList();
  renderSpritePane();
  renderDetail();
  renderCounters();
  if (!opts || opts.scroll !== false) scrollSelIntoView();
  try { history.replaceState(null, "", "#" + id); } catch(e){}
}
function next(dir){
  const arr = filtered();
  if (!arr.length) return;
  let i = arr.findIndex(p => p.id === state.sel);
  if (i === -1) i = 0; else i = (i + dir + arr.length) % arr.length;
  select(arr[i].id);
}
function randomPick(){
  let arr = filtered();
  if (arr.length < 2) arr = DATA;
  let id;
  do { id = arr[Math.floor(Math.random() * arr.length)].id; } while (arr.length > 1 && id === state.sel);
  select(id);
}
function toggleOwn(){
  const id = state.sel;
  if (state.own.has(id)) state.own.delete(id); else state.own.add(id);
  save("pkd_g1_own", [...state.own]);
  renderList(); renderSpritePane(); renderCounters();
}
function toggleFav(){
  const id = state.sel;
  if (state.favs.has(id)) state.favs.delete(id); else state.favs.add(id);
  save("pkd_g1_favs", [...state.favs]);
  renderList(); renderSpritePane();
}

/* ===== palette (Game Boy / Pocket — mono set only) ===== */
function applyPalette(){
  document.body.classList.toggle("pocket", state.pal === "pocket");
}
function togglePalette(){
  if (SPRITE_SETS[state.set].color) return;   /* colored sets ignore the screen palette */
  state.pal = state.pal === "dmg" ? "pocket" : "dmg";
  save("pkd_g1_pal", state.pal);
  applyPalette();
  renderSpritePane();
  renderDetail();
}
/* ===== LCD screen shader (optional, per-visitor) ===== */
function applyLcd(){
  document.body.classList.toggle("lcd-on", state.lcd === true);
  const b = $("#btnLcd");
  if (b){
    b.classList.toggle("on", state.lcd === true);
    b.setAttribute("aria-pressed", state.lcd ? "true" : "false");
  }
  const tx = $("#lcdTxt");
  if (tx) tx.textContent = state.lcd ? t("lcd_on") : t("lcd_off");
}
function toggleLcd(){
  state.lcd = !state.lcd;
  save("pkd_g1_lcd", state.lcd);
  applyLcd();
  refreshMenuLabels();
}
/* ===== sprite set cycling (menu) — within the active game ===== */
function cycleSet(){
  const order = THEMES[state.theme].sets;
  const i = order.indexOf(state.set);
  toggleSet(order[(i + 1) % order.length]);
}

/* ===== menu popup ===== */
function openMenu(){
  $("#menuPop").classList.remove("hidden");
  $("#menuScrim").classList.remove("hidden");
  refreshMenuLabels();
}
function closeMenu(){
  $("#menuPop").classList.add("hidden");
  $("#menuScrim").classList.add("hidden");
}
function menuOpen(){ return !$("#menuPop").classList.contains("hidden"); }
function refreshMenuLabels(){
  $("#menuPop [data-act=sort] span:last-child").textContent = tpl(t("m_sort_tpl"), {v: t("sort_"+state.sort)});
  $("#menuPop [data-act=lang] span:last-child").textContent = state.lang === "en" ? t("m_lang") : "Language: English";
  $("#menuPop [data-act=set] span:last-child").textContent = tpl(t("m_set_tpl"), {v: t("set_names."+state.set)});
  $("#menuPop [data-act=game] span:last-child").textContent = tpl(t("m_game_tpl"), {v: t("theme_short."+state.theme)});
  $("#menuPop [data-act=back] span:last-child").textContent = tpl(t("m_view_tpl"), {v: t(state.back ? "view_back" : "view_front")});

  $("#menuPop [data-act=pal] span:last-child").textContent = tpl(t("m_pal_tpl"), {v: t("pal_names."+state.pal)});
  $("#menuPop [data-act=lcd] span:last-child").textContent = tpl(t("m_lcd_tpl"), {v: state.lcd ? t("lcd_on") : t("lcd_off")});
  $("#menuPop [data-act=fav]").classList.toggle("on", state.favOnly);
}

/* ===== language ===== */
function applyLang(){
  document.documentElement.lang = state.lang;
  document.body.dir = state.lang === "fa" ? "rtl" : "ltr";
  document.body.classList.toggle("fa", state.lang === "fa");
  document.title = t("title");
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const k = el.getAttribute("data-i18n");
    const v = t(k);
    if (typeof v === "string" && v) el.textContent = v;
  });
  $("#q").placeholder = t("search_ph");
  $("#langBtn").textContent = state.lang === "en" ? "فارسی" : "English";
  $("#sortBtn").title = tpl(t("m_sort_tpl"), {v: t("sort_"+state.sort)});
  renderTabs(); renderChips(); renderList(); renderThemeRow(); renderSetRow(); renderSpritePane(); renderDetail(); renderCounters();
  refreshMenuLabels();
  applyLcd();
  const t1 = document.querySelector("#topbar .t1");
  if (t1) t1.textContent = t("theme_tag." + state.theme);
  if (typeof MovesUI !== "undefined") MovesUI.applyLang();
  if (typeof ItemsUI !== "undefined") ItemsUI.applyLang();
}
function toggleLang(){
  state.lang = state.lang === "en" ? "fa" : "en";
  save("pkd_lang", state.lang);
  applyLang();
}

/* ===== sort cycle ===== */
function cycleSort(){
  state.sort = state.sort === "id" ? "name" : state.sort === "name" ? "total" : "id";
  save("pkd_g1_sort", state.sort);
  $("#sortBtn").title = tpl(t("m_sort_tpl"), {v: t("sort_"+state.sort)});
  renderList();
}

/* ===== events ===== */
function bind(){
  $("#list").addEventListener("click", e => {
    const row = e.target.closest(".row");
    if (!row) return;
    select(parseInt(row.dataset.id, 10));
  });
  $("#typeRow").addEventListener("click", e => {
    const c = e.target.closest(".chip");
    if (!c) return;
    const tp = c.dataset.t;
    state.type = state.type === tp ? null : tp;
    renderChips(); renderList();
  });
  let deb;
  $("#q").addEventListener("input", e => {
    clearTimeout(deb);
    deb = setTimeout(() => { state.q = e.target.value; renderList(); }, 120);
  });
  $("#sortBtn").addEventListener("click", cycleSort);
  $("#favBtn").addEventListener("click", () => {
    state.favOnly = !state.favOnly;
    save("pkd_g1_favonly", state.favOnly);
    $("#favBtn").classList.toggle("on", state.favOnly);
    renderList();
  });
  $("#randBtn").addEventListener("click", randomPick);
  $("#langBtn").addEventListener("click", toggleLang);
  $("#btnPal").addEventListener("click", togglePalette);
  $("#btnBack").addEventListener("click", toggleBack);
  $("#btnCry").addEventListener("click", playCry);
  $("#btnLcd").addEventListener("click", toggleLcd);
  $("#setRow").addEventListener("click", e => {
    const c = e.target.closest(".setchip");
    if (c) toggleSet(c.dataset.set);
  });
  $("#themeRow").addEventListener("click", e => {
    const c = e.target.closest(".tchip");
    if (c) toggleTheme(c.dataset.th);
  });
  $("#btnOwn").addEventListener("click", toggleOwn);
  $("#btnFav").addEventListener("click", toggleFav);
  $("#startBtn").addEventListener("click", () => menuOpen() ? closeMenu() : openMenu());
  $("#menuScrim").addEventListener("click", closeMenu);
  $("#menuPop").addEventListener("click", e => {
    const it = e.target.closest(".m-item");
    if (!it) return;
    const act = it.dataset.act;
    closeMenu();
    if (act === "search"){ $("#q").focus(); }
    else if (act === "random") randomPick();
    else if (act === "cry") playCry();
    else if (act === "set") cycleSet();
    else if (act === "game") cycleTheme();
    else if (act === "pal") togglePalette();
    else if (act === "lcd") toggleLcd();
    else if (act === "back") toggleBack();
    else if (act === "fav"){ state.favOnly = !state.favOnly; save("pkd_g1_favonly", state.favOnly); $("#favBtn").classList.toggle("on", state.favOnly); renderList(); }
    else if (act === "sort") cycleSort();
    else if (act === "lang") toggleLang();
    else if (act === "reset"){
      if (confirm(t("reset_confirm"))){
        state.seen.clear(); state.own.clear();
        save("pkd_g1_seen", []); save("pkd_g1_own", []);
        markSeen(state.sel);
        renderList(); renderSpritePane(); renderCounters();
      }
    }
    else if (act === "about") $("#aboutWrap").classList.remove("hidden");
  });
  $("#aboutClose").addEventListener("click", () => $("#aboutWrap").classList.add("hidden"));
  $("#aboutOk").addEventListener("click", () => $("#aboutWrap").classList.add("hidden"));
  $("#aboutWrap").addEventListener("click", e => { if (e.target.id === "aboutWrap") $("#aboutWrap").classList.add("hidden"); });
  $("#scrollUp").addEventListener("click", () => $("#list").scrollBy({top:-180, behavior:"smooth"}));
  $("#scrollDown").addEventListener("click", () => $("#list").scrollBy({top:180, behavior:"smooth"}));
  /* mobile: big prev/next arrows beside the sprite */
  $("#mPrev").addEventListener("click", () => next(-1));
  $("#mNext").addEventListener("click", () => next(1));
  /* mobile gestures: swipe = browse, tap on the sprite = flip front/back */
  let lastSwipe = 0;
  (() => {
    const stage = $("#sprStage");
    if (!stage) return;
    let sx = 0, sy = 0, st = 0;
    stage.addEventListener("touchstart", e => {
      const tc = e.changedTouches[0];
      sx = tc.clientX; sy = tc.clientY; st = Date.now();
    }, { passive: true });
    stage.addEventListener("touchend", e => {
      const tc = e.changedTouches[0];
      const dx = tc.clientX - sx, dy = tc.clientY - sy;
      if (Math.abs(dx) > 42 && Math.abs(dx) > Math.abs(dy) * 1.4 && Date.now() - st < 900){
        lastSwipe = Date.now();   /* swallow the click that follows the swipe */
        next(dx < 0 ? 1 : -1);   /* swipe left → next, swipe right → previous */
      }
    }, { passive: true });
  })();
  $("#sprBox").addEventListener("click", () => {
    if (Date.now() - lastSwipe < 500) return;
    toggleBack();
  });
  const cfEl = $("#cardFlavor");
  if (cfEl) cfEl.addEventListener("click", () => {
    const n = parseInt(cfEl.dataset.pgs || "1", 10);
    if (n > 1){ state.page = state.page >= n ? 1 : state.page + 1; renderDetail(); }
  });
  document.addEventListener("keydown", e => {
    if (e.target.matches("input,select,textarea")){
      if (e.key === "Escape") e.target.blur();
      return;
    }
    if (e.key === "Escape"){
      if (menuOpen()) closeMenu();
      $("#aboutWrap").classList.add("hidden");
    }
    else if (e.key === "ArrowDown"){ e.preventDefault(); next(1); }
    else if (e.key === "ArrowUp"){ e.preventDefault(); next(-1); }
    else if (e.key === "ArrowLeft" && !isMobile()){ e.preventDefault(); next(-1); }
    else if (e.key === "ArrowRight" && !isMobile()){ e.preventDefault(); next(1); }
    else if (e.key === "/"){ e.preventDefault(); $("#q").focus(); }
    else if (e.key.toLowerCase() === "c"){ playCry(); }
    else if (e.key.toLowerCase() === "p"){ togglePalette(); }
    else if (e.key.toLowerCase() === "b"){ toggleBack(); }
    else if (e.key.toLowerCase() === "r") randomPick();
    else if (e.key.toLowerCase() === "t") cycleTheme();
  });
}

/* ===== splash & init ===== */
function killSplash(){
  const s = $("#splash");
  if (!s) return;
  s.classList.add("hide");
  setTimeout(() => s.remove(), 500);
}
function init(){
  const h = parseInt((location.hash || "").replace("#",""), 10);
  if (h >= 1 && h <= 151 && PMAP[h]) state.sel = h;
  else { const s = parseInt(store("pkd_g1_sel", 25), 10); if (s >= 1 && s <= 151 && PMAP[s]) state.sel = s; }
  $("#favBtn").classList.toggle("on", state.favOnly);
  applyPalette();
  applyTheme();
  applyLang();
  markSeen(state.sel);
  bind();
  renderList();
  renderSpritePane();
  renderDetail();
  renderCounters();
  scrollSelIntoView();
  try { history.replaceState(null, "", "#" + state.sel); } catch(e){}
  const s = $("#splash");
  if (s){ s.addEventListener("click", killSplash); setTimeout(killSplash, 1300); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => scrollSelIntoView());
  window.addEventListener("load", () => scrollSelIntoView());
}
document.addEventListener("DOMContentLoaded", init);
