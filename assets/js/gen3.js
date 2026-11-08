"use strict";
/* ===== Pokédex Plus — GENERATION III: all five games in one dex (Ruby ·
   Sapphire · Emerald · FireRed · LeafGreen). Derived from the Gen-2 dex;
   loads gen3-data.js (DATA / EVOLUTIONS / SPRITE_SETS rs/em/frlg). The
   Gen-3 signature is era-authentic: abilities have NO hidden slots (the
   stat split and hidden abilities did not exist yet), Deoxys's forme is
   tied to the cartridge (R/S=Normal, FIRERED=Attack, LEAFGREEN=Defense,
   EMERALD=Speed), and Emerald keeps the series' animated battle sprites.
   Moves, items and locations join in later phases — every section is
   guarded with typeof checks until its data file is wired in. ===== */
/* sprites — GBA-native colored banks: rs = Ruby/Sapphire (shared pair),
   em = Emerald (atlas stills + animated battle set), frlg = FireRed/
   LeafGreen (shared pair, carrying the Attack/Defense Deoxys formes). */

/* ===== i18n ===== */
const I18N = {
en:{
  brand_main:"Hoenn Pokédex — 386 Pokémon",
  kb_hint:"↑↓ browse · / search", home:"HOME",
  search_ph:"Search name or number...",
  modes:{hoenn:"HOENN"},
  showing:"Showing {a} of {b}", no_results:"No Pokémon found",
  shiny_mark:"✦ Shiny", cry_mark:"Cry", own_mark:"Own", fav_mark:"Fav",
  on:"ON", off:"OFF",
  set_mark:"Sprites",
  theme_short:{ruby:"RUBY", sapphire:"SAPPHIRE", emerald:"EMERALD", firered:"FIRERED", leafgreen:"LEAFGREEN"},
  theme_names:{ruby:"Pokémon Ruby", sapphire:"Pokémon Sapphire", emerald:"Pokémon Emerald", firered:"Pokémon FireRed", leafgreen:"Pokémon LeafGreen"},
  theme_tag:{ruby:"GEN III · RUBY VERSION", sapphire:"GEN III · SAPPHIRE VERSION", emerald:"GEN III · EMERALD VERSION", firered:"GEN III · FIRERED VERSION", leafgreen:"GEN III · LEAFGREEN VERSION"},
  text_ver:"Dex text version",
  m_game_tpl:"Game: {v}", m_game:"Game: Ruby",
  back_mark:"Back", view_front:"Front", view_back:"Back", m_view_tpl:"View: {v}", m_back:"View: Front",
  emerald_note:"Emerald — its own dex texts, its animated battle sprites (the ANIM chip) and the Speed-forme Deoxys.",
  m_shiny_tpl:"Shiny sprites: {v}", m_shiny:"Shiny sprites: OFF",
  shiny_note:"Shiny Pokémon existed in Gen 3 — hunt the rare color variants.",
  m_anim_tpl:"Animated sprites: {v}", m_anim:"Animated sprites: OFF",
  anim_mark:"Anim",
  anim_back_note:"Emerald only animated its front sprites — the back view is always static",
  anim_other_note:"Animated sprites are Emerald's — switch to EMERALD for them",
  dex_status:"DEX STATUS", seen:"Seen", own:"Owned",
  ht:"HT", wt:"WT",
  prev:"◀ Prev", next:"Next ▶", random:"Random",
  entry_t:"POKéDEX ENTRY", stats_t:"BASE STATS", total:"TOTAL",
  weak_t:"TYPE MATCHUPS", evo_t:"EVOLUTION LINE", data_t:"POKéMON DATA",
  wk4:"Weak ×4", wk2:"Weak ×2", whalf:"Resist ×½", wquarter:"Resist ×¼", wzero:"Immune ×0", wnorm:"Normal damage",
  g3_note:"Authentic Generation III type mechanics.",
  no_evo:"This Pokémon does not evolve.",
  evo_extra:"+{n} more evolution(s) beyond Gen 3",
  evo_unknown:"Data unknown — not seen yet",
  abilities:"Abilities", hidden:"Hidden",
  ability_note:"Gen-3 ability slots, straight from the pokeemerald disassembly — no hidden abilities existed yet.",
  capture:"Catch rate", capture_hint:"(max 255)", happiness:"Base happiness",
  growth:"Growth rate", exp:"Base exp. yield", egg:"Egg groups", habitat:"Habitat",
  gender:"Gender ratio", genderless:"Genderless",
  legendary:"Legendary", mythical:"Mythical", genb:"GEN {n}",
  forme_t:"CARTRIDGE FORME",
  forme_note:"Deoxys takes a different forme on every Gen-3 cartridge: Normal on Ruby/Sapphire, Attack on FireRed, Defense on LeafGreen and Speed on Emerald — stats and sprite follow the selected game.",
  page:"{a}/{b}",
  start:"START", menu:"MENU", menu_title:"POKéDEX MENU",
  m_search:"Search", m_random:"Random Pokémon",
  m_cry:"Play cry", m_shiny_tpl:"Shiny sprites: {v}",
  m_anim_tpl:"Animated sprites: {v}",
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
  about_p1:"A fan-made, offline Pokédex covering all 386 Pokémon of Generation III — the five Game Boy Advance games in one dex. Data, sprites, cries and fonts live in local files next to the page — everything runs without internet.",
  about_p2:"",
  about_p3:"Mark Pokémon as Seen (automatic while browsing) and Owned (pokeball button) to fill your dex status, just like the game. The GAME chips (or key T) switch this dex between the five Gen-3 releases: RUBY and SAPPHIRE (the 2002 pair, sharing a cartridge's sprite bank but each with its own dex texts), EMERALD (its own texts, its animated battle sprites — the ANIM chip — and the Speed-forme Deoxys) and FIRERED / LEAFGREEN (the Kanto remakes with their own sprite bank and texts). The ✦ SHINY chip shows the rare color variants and the Back button (key B) flips to the in-game back side. Every dex entry can be read in the wording of the game you pick with the R/S · EMERALD · FRLG selector — Sapphire and LeafGreen get their own button wherever their texts differ. Deoxys is the era trick: its forme, stats and sprite change with the selected cartridge, exactly like the real games. Your settings (game, shiny, animated, language, sort, last Pokémon) are remembered between visits.",
  foot_disclaimer:"Fan-made, non-commercial project. Pokémon © Nintendo / Creatures Inc. / GAME FREAK inc.",
  foot_offline:"Runs 100% offline · static site", all_games:"All games",
  reset_confirm:"Reset all Seen/Owned progress?",
  reset_done:"Dex progress cleared.",
  base:"base",
  genus_suffix:"POKéMON",
  evo_conds:{level:"Lv. {n}", special:"Special condition", happiness:"Happiness", beauty:"High beauty",
    trade:"Trade", trade_item:"Trade holding {i}", use_item:"Use {i}",
    shed:"Lv. 20 + empty slot + Poké Ball", move:"Knows {m}", full:"Level up"},
  evo_base:"Base form",
  units:{m:"m", kg:"kg"},
  types:{normal:"Normal",fire:"Fire",water:"Water",electric:"Electric",grass:"Grass",ice:"Ice",
    fighting:"Fighting",poison:"Poison",ground:"Ground",flying:"Flying",psychic:"Psychic",bug:"Bug",
    rock:"Rock",ghost:"Ghost",dragon:"Dragon",dark:"Dark",steel:"Steel"},
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
  title:"Pokédex — Generation III (Ruby · Sapphire · Emerald · FireRed · LeafGreen)"
},
fa:{
  brand_main:"پوکیدکس هوئن — ۳۸۶ پوکمون",
  kb_hint:"↑↓ پیمایش · / جست‌وجو", home:"خانه",
  search_ph:"جست‌وجوی نام یا شماره...",
  modes:{hoenn:"هوئن"},
  showing:"نمایش {a} از {b}", no_results:"پوکمونی پیدا نشد",
  shiny_mark:"✦ شاینی", cry_mark:"صدا", own_mark:"گرفتم", fav_mark:"علاقه",
  on:"روشن", off:"خاموش",
  set_mark:"اسپرایت",
  theme_short:{ruby:"یاقوت", sapphire:"یاقوت کبود", emerald:"زمرد", firered:"آتشین", leafgreen:"برگ سبز"},
  theme_names:{ruby:"پوکمون یاقوت", sapphire:"پوکمون یاقوت کبود", emerald:"پوکمون زمرد", firered:"پوکمون آتشین قرمز", leafgreen:"پوکمون برگ سبز"},
  theme_tag:{ruby:"نسل ۳ · نسخه‌ی یاقوت", sapphire:"نسل ۳ · نسخه‌ی یاقوت کبود", emerald:"نسل ۳ · نسخه‌ی زمرد", firered:"نسل ۳ · نسخه‌ی آتشین قرمز", leafgreen:"نسل ۳ · نسخه‌ی برگ سبز"},
  text_ver:"نسخه‌ی متن پوکیدکس",
  m_game_tpl:"بازی: {v}", m_game:"بازی: یاقوت",
  back_mark:"پشت", view_front:"جلو", view_back:"پشت", m_view_tpl:"نمایش: {v}", m_back:"نمایش: جلو",
  emerald_note:"زمرد — متن‌های پوکیدکس خودش، اسپرایت‌های متحرک نبردش (چیپ ANIM) و دِآوکس فرم سرعت.",
  m_shiny_tpl:"اسپرایت شاینی: {v}", m_shiny:"اسپرایت شاینی: خاموش",
  shiny_note:"پوکمون‌های شاینی در نسل ۳ هم بودند — واریانت‌های رنگی کمیاب را شکار کنید.",
  m_anim_tpl:"اسپرایت متحرک: {v}", m_anim:"اسپرایت متحرک: خاموش",
  anim_mark:"انیمیشن",
  anim_back_note:"زمرد فقط اسپرایت‌های جلو را متحرک می‌کرد — نمای پشت همیشه ثابت است",
  anim_other_note:"اسپرایت متحرک مال زمرد است — برای دیدنش به EMERALD بروید",
  dex_status:"وضعیت پوکیدکس", seen:"دیده‌شده", own:"گرفته‌شده",
  ht:"قد", wt:"وزن",
  prev:"◀ قبلی", next:"بعدی ▶", random:"تصادفی",
  entry_t:"توضیحات پوکیدکس", stats_t:"آمار پایه", total:"مجموع",
  weak_t:"تناسب انواع", evo_t:"زنجیره تکامل", data_t:"داده‌های پوکمون",
  wk4:"ضعف ×۴", wk2:"ضعف ×۲", whalf:"مقاوم ×½", wquarter:"مقاوم ×¼", wzero:"مصون ×۰", wnorm:"آسیب عادی",
  g3_note:"با مکانیک دقیق انواع نسل سوم.",
  no_evo:"این پوکمون تکامل ندارد.",
  evo_extra:"+{n} تکامل دیگر در نسل‌های بعدی",
  evo_unknown:"داده نامشخص — هنوز دیده نشده",
  abilities:"توانایی‌ها", hidden:"پنهان",
  ability_note:"جایگاه‌های توانایی نسل ۳، مستقیم از دیساسمبل pokeemerald — هنوز توانایی پنهانی وجود نداشت.",
  capture:"نرخ گرفتن", capture_hint:"(حداکثر ۲۵۵)", happiness:"شادی پایه",
  growth:"سرعت رشد", exp:"امتیاز تجربه پایه", egg:"گروه تخم", habitat:"زیستگاه",
  gender:"نسبت جنسیت", genderless:"بی‌جنس",
  legendary:"افسانه‌ای", mythical:"اسطوره‌ای", genb:"نسل {n}",
  forme_t:"فرم کارتریج",
  forme_note:"دِآوکس روی هر کارتریج نسل ۳ فرم متفاوتی می‌گیرد: عادی روی یاقوت/یاقوت کبود، حمله روی آتشین قرمز، دفاع روی برگ سبز و سرعت روی زمرد — آمار و اسپرایت با بازی انتخاب‌شده عوض می‌شود.",
  page:"{a}/{b}",
  start:"استارت", menu:"منو", menu_title:"منوی پوکیدکس",
  m_search:"جست‌وجو", m_random:"پوکمون تصادفی",
  m_cry:"پخش صدای پوکمون", m_shiny_tpl:"اسپرایت شاینی: {v}",
  m_anim_tpl:"اسپرایت متحرک: {v}",
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
  about_p1:"پوکیدکس طرفداری و آفلاین برای هر ۳۸۶ پوکمون نسل سوم — هر پنج بازی گیم‌بوی ادونس در یک پوکیدکس واحد. داده‌ها، اسپرایت‌ها، صدای پوکمون‌ها و فونت‌ها در فایل‌های کنار صفحه ذخیره شده‌اند و همه‌چیز بدون اینترنت کار می‌کند.",
  about_p2:"",
  about_p3:"با مرور هر پوکمون، به‌طور خودکار «دیده‌شده» ثبت می‌شود و با دکمه پوکربال می‌توانید آن را «گرفته‌شده» علامت بزنید تا وضعیت پوکیدکس مثل خود بازی پر شود. چیپ‌های بازی (یا کلید T) این دکس را بین پنج نسخه‌ی نسل سوم جابه‌جا می‌کنند: یاقوت و یاقوت کبود (جفت ۲۰۰۲ که بانک اسپرایت کارتریج خودشان را شریک‌اند ولی هرکدام متن‌های پوکیدکس خودشان را دارند)، زمرد (متن‌های خودش، اسپرایت‌های متحرک نبردش — چیپ ANIM — و دِآوکس فرم سرعت) و آتشین قرمز / برگ سبز (بازسازی کانتو با بانک اسپرایت و متن‌های خودشان). چیپ ✦ شاینی واریانت‌های رنگی کمیاب را نشان می‌دهد و دکمه پشت (کلید B) اسپرایت را به نمای پشت بازی برمی‌گرداند. هر توضیح را می‌توان با انتخابگر R/S · EMERALD · FRLG با متن بازی دلخواه خواند — هر جا متن سیلورِ این نسل، یعنی یاقوت کبود یا برگ سبز، متفاوت باشد دکمه‌ی خودش را می‌گیرد. دِآوکس ترفند این نسل است: فرم، آمار و اسپرایتش با کارتریج انتخاب‌شده عوض می‌شود؛ درست مثل خود بازی‌ها. تنظیمات شما (بازی، شاینی، متحرک، زبان، ترتیب، آخرین پوکمون) بین دیدارها به خاطر سپرده می‌شود.",
  foot_disclaimer:"پروژه‌ای غیرتجاری ساخته‌ی طرفداران. پوکمون © نینتندو / کرچرز / گیم‌فریک.",
  foot_offline:"کاملاً آفلاین · سایت استاتیک", all_games:"همه بازی‌ها",
  reset_confirm:"همه پیشرفت دیده‌شده/گرفته‌شده پاک شود؟",
  reset_done:"پیشرفت پوکیدکس پاک شد.",
  base:"پایه",
  genus_suffix:"",
  evo_conds:{level:"سطح {n}", special:"شرط ویژه", happiness:"شادی بالا", beauty:"زیبایی بالا",
    trade:"تبادل", trade_item:"تبادل با {i}", use_item:"استفاده از {i}",
    shed:"سطح ۲۰ + جای خالی تیم + پوکربال", move:"دانستن حرکت {m}", full:"رهشی سطح"},
  evo_base:"فرم پایه",
  units:{m:"متر", kg:"کیلوگرم"},
  types:{normal:"معمولی",fire:"آتش",water:"آب",electric:"برقی",grass:"گیاهی",ice:"یخی",
    fighting:"جنگی",poison:"سمی",ground:"زمینی",flying:"پروازی",psychic:"روانی",bug:"حشره‌ای",
    rock:"سنگی",ghost:"روحی",dragon:"اژدها",dark:"تاریک",steel:"فولادی"},
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
  title:"پوکیدکس — نسل ۳ (یاقوت · یاقوت کبود · زمرد · آتشین قرمز · برگ سبز)"
}};

/* ===== defensive type chart — identical to Gen 2's (the next change was
   Gen 5); Dark & Steel present, Ghost ×2 vs Psychic, Steel does NOT
   resist Dark/Ghost yet ===== */
const CHART = {
  normal:{rock:.5,ghost:0,steel:.5},
  fire:{fire:.5,water:.5,grass:2,ice:2,bug:2,rock:.5,dragon:.5,steel:2},
  water:{fire:2,water:.5,grass:.5,ground:2,rock:2,dragon:.5},
  electric:{water:2,electric:.5,grass:.5,ground:0,flying:2,dragon:.5},
  grass:{fire:.5,water:2,grass:.5,poison:.5,ground:2,flying:.5,bug:.5,rock:2,dragon:.5,steel:.5},
  ice:{fire:.5,water:.5,grass:2,ice:.5,ground:2,flying:2,dragon:2,steel:.5},
  fighting:{normal:2,ice:2,poison:.5,flying:.5,psychic:.5,bug:.5,rock:2,ghost:0,dark:2,steel:2},
  poison:{grass:2,poison:.5,ground:.5,rock:.5,ghost:.5,steel:0},
  ground:{fire:2,electric:2,grass:.5,poison:2,flying:0,bug:.5,rock:2,steel:2},
  flying:{electric:.5,grass:2,fighting:2,bug:2,rock:.5,steel:.5},
  psychic:{fighting:2,poison:2,psychic:.5,dark:0,steel:.5},
  bug:{fire:.5,grass:2,fighting:.5,poison:.5,flying:.5,psychic:2,ghost:.5,dark:2,steel:.5},
  rock:{fire:2,ice:2,fighting:.5,ground:.5,flying:2,bug:2,steel:.5},
  ghost:{normal:0,psychic:2,ghost:2,dark:.5,steel:1},
  dragon:{dragon:2,steel:.5},
  dark:{fighting:.5,psychic:2,ghost:2,dark:.5,steel:1},
  steel:{fire:.5,water:.5,electric:.5,ice:2,rock:2,steel:.5}
};
const TYPE_ORDER = ["normal","fire","water","electric","grass","ice","fighting","poison","ground","flying","psychic","bug","rock","ghost","dragon","dark","steel"];
const TYPE_COLOR = {normal:"#A8A77A",fire:"#EE8130",water:"#6390F0",electric:"#F7D02C",grass:"#7AC74C",ice:"#96D9D6",fighting:"#C22E28",poison:"#A33EA1",ground:"#E2BF65",flying:"#A98FF3",psychic:"#F95587",bug:"#A6B91A",rock:"#B6A136",ghost:"#735797",dragon:"#6F35FC",dark:"#705746",steel:"#B7B7CE"};
const STAT_COLOR = {hp:"#f0a030",atk:"#e05038",def:"#4890d0",spa:"#a870d8",spd:"#58b868",spe:"#f0d048"};
/* FA ability names — the era list rides the donor's table (verified: every
   one of the 76 Gen-3 abilities has an entry) */
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
const MODE_RANGE = { hoenn:[1,386] };
/* Deoxys rides the cartridge: per-game stats + forme sprite id.
   The stats remap applies on all three games that carry a special forme;
   the sprite remap only on FR/LG — the emerald bank already stores the
   Speed forme under 386.png (built by tools/build-gen3-sprites.py). */
const FORME_STATS = { firered:"fr", leafgreen:"lg", emerald:"em" };
const FORME_GAME = { firered:"fr", leafgreen:"lg" };
function statsOf(p){
  const fk = FORME_STATS[state.theme];
  if (p.formes && fk && p.formes[fk]) return p.formes[fk].stats;
  return p.stats;
}
const total = p => { const s = statsOf(p); return s.hp + s.atk + s.def + s.spa + s.spd + s.spe; };

/* sprites: the active game's GBA bank; ✦ SHINY swaps to the shiny variant.
   SPRITE_SETS folders are path templates with __ID__ (built by
   tools/build-gen3-data.py). Deoxys's forme sprite rides the cartridge:
   Normal=386 (rs bank), Attack=10013 / Defense=10014 (frlg bank),
   Speed=386.png in the emerald bank (already the Speed forme). */
function spriteId(p){
  const fk = FORME_GAME[state.theme];
  return (p.formes && fk && p.formes[fk]) ? p.formes[fk].sprite : p.id;
}
function spriteURL(id, back){
  const set = SPRITE_SETS[state.set] || SPRITE_SETS.rs;
  const bank = (back && set.back) ? set.back : set.files;
  const tpl = bank[state.shiny ? "shiny" : "normal"];
  return tpl ? tpl.replace("__ID__", String(spriteId(PMAP[id] || {id}))) : "";
}
function animURL(id){
  const set = SPRITE_SETS[state.set];
  return (set && set.anim) ? set.anim.replace("__ID__", String(spriteId(PMAP[id] || {id}))) : "";
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
const G3_GAMES = ["ruby","sapphire","emerald","firered","leafgreen"];
const state = {
  lang: store("pkd_lang", "en") === "fa" ? "fa" : "en",
  sel: 252, q: "", mode: "hoenn", type: null,
  theme: G3_GAMES.indexOf(store("pkd_g3_theme", "ruby")) !== -1 ? store("pkd_g3_theme", "ruby") : "ruby",
  set: ["rs","em","frlg"].indexOf(store("pkd_g3_set", "rs")) !== -1 ? store("pkd_g3_set", "rs") : "rs",
  text: ["rs","s","em","fr","lg"].indexOf(store("pkd_g3_text", "")) !== -1 ? store("pkd_g3_text", "") : null,
  shiny: store("pkd_g3_shiny", false) === true,
  anim: store("pkd_g3_anim", false) === true,
  back: store("pkd_g3_back", "front") === "back",
  lcd: store("pkd_g3_lcd", false) === true,
  favOnly: store("pkd_g3_favonly", false) === true,
  sort: ["id","name","total"].indexOf(store("pkd_g3_sort", "id")) !== -1 ? store("pkd_g3_sort", "id") : "id",
  page: 1,
  favs: new Set(store("pkd_g3_favs", [])),
  seen: new Set(store("pkd_g3_seen", [])),
  own:  new Set(store("pkd_g3_own", []))
};
const isMobile = () => window.matchMedia("(max-width:860px)").matches;

/* ===== GAME THEMES — which of the five Gen-3 games the dex is "running" =====
   Each pair shares a cartridge's sprite bank (like the real carts) but every
   game reads its own dex texts; Emerald adds the animated battle sprites. */
const THEMES = {
  ruby:      { sets:["rs"],   def:"rs",   text:"rs", cls:"theme-ruby",      anim:false },
  sapphire:  { sets:["rs"],   def:"rs",   text:"rs", cls:"theme-sapphire",  anim:false },
  emerald:   { sets:["em"],   def:"em",   text:"em", cls:"theme-emerald",   anim:true },
  firered:   { sets:["frlg"], def:"frlg", text:"fr", cls:"theme-firered",   anim:false },
  leafgreen: { sets:["frlg"], def:"frlg", text:"fr", cls:"theme-leafgreen", anim:false }
};
const THEME_ORDER = ["ruby","sapphire","emerald","firered","leafgreen"];
function applyTheme(){
  const th = THEMES[state.theme] || THEMES.ruby;
  document.body.classList.remove("theme-ruby","theme-sapphire","theme-emerald","theme-firered","theme-leafgreen");
  document.body.classList.add(th.cls);
  /* the sprite set IS the cartridge's bank — it follows the theme */
  if (th.sets.indexOf(state.set) === -1){
    state.set = th.def;
    save("pkd_g3_set", state.set);
  }
  /* dex text follows the game unless the reader picked a wording explicitly */
  if (state.text === null) state.text = th.text;
  const t1 = document.querySelector("#topbar .t1");
  if (t1) t1.textContent = t("theme_tag." + state.theme);
}
/* the wording this game reads by default (sapphire/lg get their own only
   where their texts actually differ — never invented) */
function effText(p){
  if (state.text){
    if (state.text === "s" && !p.ts) return "rs";
    if (state.text === "lg" && !p.tlg) return "fr";
    return state.text;
  }
  if (state.theme === "sapphire" && p.ts) return "s";
  if (state.theme === "leafgreen" && p.tlg) return "lg";
  return THEMES[state.theme].text === "em" ? "em" : THEMES[state.theme].text === "fr" ? "fr" : "rs";
}
function toggleTheme(th){
  if (!THEMES[th] || th === state.theme) return;
  state.theme = th;
  save("pkd_g3_theme", th);
  /* state.text: null = follow each game's own wording; an explicit choice
     is remembered (pkd_g3_text) */
  if (store("pkd_g3_text", "") === "") state.text = null;
  /* animated sprites belong to Emerald alone */
  if (th !== "emerald" && state.anim){
    state.anim = false;
    save("pkd_g3_anim", false);
  }
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
  return (p.genus || "").replace(/\s*Pokémon\s*$/i, "") + " " + t("genus_suffix");
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

/* ===== tabs (single HOENN dex, like the game) ===== */
function renderTabs(){
  $("#tabs").innerHTML = ["hoenn"].map(m =>
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
  for (let i = 1; i <= 386; i++){ if (PMAP[i]){ n++; if (state.seen.has(i)) s++; if (state.own.has(i)) o++; } }
  $("#cntRows").innerHTML =
    '<div class="cRow"><span class="reg">' + esc(t("modes.hoenn")) + '</span>' +
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
  return h + '<div class="wk-note">' + esc(t("g3_note")) + '</div>';
}

/* ===== evolution ===== */
function condText(c){
  if (!c) return t("evo_conds.full");
  const ec = t("evo_conds");
  switch (c.t){
    case "level": return c.lvl ? tpl(ec.level, {n: num(c.lvl)}) : ec.special;
    case "happiness": return ec.happiness;
    case "beauty": return ec.beauty;
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
  const members = ch.members.filter(m => m <= 386 && PMAP[m]);
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
  /* Emerald's animated battle sprites: front view only, never shiny —
     the shiny variant and the back view stay static (authentic Emerald) */
  const useAnim = state.anim && !state.shiny && !state.back && state.set === "em" && !!animURL(p.id);
  img.src = useAnim ? animURL(p.id) : spriteURL(p.id, state.back);
  img.alt = dispName(p);
  $("#sprNo").textContent = "#" + pad3(p.id);
  /* bilingual name — ONLY the Pokémon's name carries both languages (FA main
     + EN beneath, or EN main + FA beneath); everything else stays monolingual */
  const nameAlt = state.lang === "fa" ? p.display : (p.fa || "");
  $("#sprName").innerHTML = "<bdi>" + esc(dispName(p)) + "</bdi>" +
    (nameAlt ? '<span class="altName"><bdi>' + esc(nameAlt) + "</bdi></span>" : "");
  $("#sprTypes").innerHTML = p.types.map(tp =>
    '<span class="tbadge T-' + tp + '">' + esc(typeName(tp)) + '</span>').join("");
  renderSetRow();
  const shinyB = $("#btnShiny"), animB = $("#btnAnim");
  shinyB.classList.toggle("on", state.shiny);
  shinyB.setAttribute("aria-pressed", state.shiny ? "true" : "false");
  shinyB.title = t("shiny_note");
  animB.disabled = state.theme !== "emerald" || state.back === true;
  animB.title = state.theme !== "emerald" ? t("anim_other_note") : (state.back ? t("anim_back_note") : tpl(t("m_anim_tpl"), {v: state.anim ? t("on") : t("off")}));
  animB.classList.toggle("on", state.anim && state.theme === "emerald");
  animB.setAttribute("aria-pressed", state.anim && state.theme === "emerald" ? "true" : "false");
  $("#btnBack").classList.toggle("on", state.back);
  $("#btnBack").setAttribute("aria-pressed", state.back ? "true" : "false");
  $("#btnBack").title = tpl(t("m_view_tpl"), {v: t(state.back ? "view_back" : "view_front")});
  $("#sprBox").title = t("flip_hint");
  const gn = $("#setNote");
  if (gn){ gn.classList.toggle("hidden", state.theme !== "emerald"); gn.textContent = t("emerald_note"); }
  $("#htVal").textContent = num((p.height_dm / 10).toFixed(1)) + " " + t("units.m");
  $("#wtVal").textContent = num((p.weight_hg / 10).toFixed(1)) + " " + t("units.kg");
  const ownB = $("#btnOwn"), favB = $("#btnFav");
  ownB.classList.toggle("on", state.own.has(p.id));
  ownB.querySelector("span").textContent = state.own.has(p.id) ? t("own") : t("own_mark");
  favB.classList.toggle("on", state.favs.has(p.id));
}
function toggleShiny(){
  state.shiny = !state.shiny;
  save("pkd_g3_shiny", state.shiny);
  renderSpritePane();
  renderDetail();
}
function toggleAnim(){
  if (state.theme !== "emerald") return;   /* animated sprites are Emerald's */
  state.anim = !state.anim;
  save("pkd_g3_anim", state.anim);
  renderSpritePane();
  renderDetail();
}
/* hint for the Item Dex (lands in phase 4): Gen-3 sprites are always COLOR;
   the equivalent retro switch is the LCD shader, same as gen2 */
window.__itemIconHint = function(){
  try { return state.lcd ? "gb" : "color"; }
  catch(e){ return "color"; }
};
function renderThemeRow(){
  const el = $("#themeRow");
  if (!el) return;
  const chip = th =>
    '<button class="tchip' + (state.theme === th ? " on" : "") + '" data-th="' + th +
    '" title="' + esc(t("theme_names." + th)) + '"><span class="dot"></span>' + esc(t("theme_short." + th)) + '</button>';
  /* RUBY + SAPPHIRE share one cartridge group, EMERALD its own,
     FIRERED + LEAFGREEN share one — the real Gen-3 cartridge pairs */
  el.innerHTML =
    '<div class="gcGroup">' + chip("ruby") + chip("sapphire") + '</div>' +
    '<div class="gcGroup">' + chip("emerald") + '</div>' +
    '<div class="gcGroup">' + chip("firered") + chip("leafgreen") + '</div>';
}
/* the sprite-options row inside SETTINGS: ✦ SHINY + ▶ ANIM (Emerald only) */
function renderSetRow(){
  const el = $("#setRow");
  if (!el) return;
  const isE = state.theme === "emerald";
  el.innerHTML =
    '<button class="setchip' + (state.shiny ? " on" : "") + '" id="chipShiny" aria-pressed="' + (state.shiny ? "true" : "false") + '" title="' + esc(t("shiny_note")) + '">' + esc(t("shiny_mark")) + '</button>' +
    (isE
      ? '<button class="setchip' + (state.anim ? " on" : "") + '" id="chipAnim" aria-pressed="' + (state.anim ? "true" : "false") + '" title="' + esc(t("anim_back_note")) + '">' + esc(t("anim_mark")) + '</button>'
      : '<span class="gcLab" title="' + esc(t("anim_other_note")) + '" style="opacity:.55">' + esc(t("anim_mark")) + '</span>');
}
function toggleBack(){
  state.back = !state.back;
  save("pkd_g3_back", state.back ? "back" : "front");
  renderSpritePane();
  renderDetail();
}

/* ===== detail ===== */
function statCls(v){ return v < 50 ? " low" : v < 80 ? " mid" : ""; }
function flavorPages(p){
  /* the era wordings: trs = the shared Ruby/Sapphire text (ts = Sapphire's
     own where it differs), tem = Emerald, tfr = FireRed (tlg = LeafGreen's
     own where it differs). Persian follows the wording GROUP — the gen2
     family pattern — and falls back to the EN text until its FA lands. */
  const cur = effText(p);
  const src = cur === "em" ? p.tem : cur === "fr" ? p.tfr : cur === "lg" ? (p.tlg || p.tfr) : cur === "s" ? (p.ts || p.trs) : p.trs;
  const fa = cur === "em" ? p.flavor_fa : cur === "fr" || cur === "lg" ? (p.fa_frlg || null) : p.fa_rs;
  if (state.lang === "fa"){
    return [fa || ((src && src[0]) || []).join(" ")];
  }
  const pgs = (src || []).map(lines => lines.join(" ")).filter(x => x);
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
  const S = statsOf(p), T = total(p);
  const curText = effText(p);
  const statRows = ["hp","atk","def","spa","spd","spe"].map(k =>
    '<div class="statrow"><span class="stat-l">' + esc(statName(k)) + '</span>' +
    '<span class="stat-track"><span class="stat-fill" style="width:' + Math.min(100, S[k]/1.6) + '%;background:linear-gradient(90deg,' + STAT_COLOR[k] + 'cc,' + STAT_COLOR[k] + ')"></span></span>' +
    '<span class="stat-v">' + num(S[k]) + '</span></div>').join("");

  let gender;
  if (p.genderRate < 0) gender = esc(t("genderless"));
  else {
    const fp = p.genderRate / 8 * 100, mp = 100 - fp;
    gender = '<span class="gbar"><span class="m" style="width:' + mp + '%"></span><span class="f" style="width:' + fp + '%"></span></span>' +
      '<span class="glegend">♂ ' + num(mp.toFixed(1)) + ' — ♀ ' + num(fp.toFixed(1)) + '</span>';
  }
  /* era-authentic abilities: 1-2 slots, NO hidden chip (it did not exist) */
  const abils = p.abilities.map(a =>
    '<span class="abchip" title="' + esc(a) + '">' + esc(dispAbility(a)) + '</span>').join("") +
    '<span class="wk-note">' + esc(t("ability_note")) + '</span>';

  const eggLine = p.egg.map(e => t("egg_names."+e) || e).join(state.lang === "fa" ? "، " : ", ");
  const badges =
    '<span class="tagchip tag-gen">' + esc(tpl(t("genb"), {n: num(3)})) + '</span>' +
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
        (p.ts
          ? '<button class="vbtn' + (curText === "rs" ? " on" : "") + '" data-txt="rs">RUBY</button>' +
            '<button class="vbtn' + (curText === "s" ? " on" : "") + '" data-txt="s">SAPPHIRE</button>'
          : '<button class="vbtn' + (curText === "rs" || curText === "s" ? " on" : "") + '" data-txt="rs">R/S</button>') +
        '<button class="vbtn' + (curText === "em" ? " on" : "") + '" data-txt="em">EMERALD</button>' +
        (p.tlg
          ? '<button class="vbtn' + (curText === "fr" ? " on" : "") + '" data-txt="fr">FIRERED</button>' +
            '<button class="vbtn' + (curText === "lg" ? " on" : "") + '" data-txt="lg">LEAFGREEN</button>'
          : '<button class="vbtn' + (curText === "fr" || curText === "lg" ? " on" : "") + '" data-txt="fr">FRLG</button>') +
      '</span></div>' + flavorHtml + '</div>' +

    (p.formes ? '<div class="sec"><div class="sec-t">' + esc(t("forme_t")) + '</div>' +
      '<div class="wk-note">' + esc(t("forme_note")) + '</div>' +
      '<div class="formeRow">' +
        '<span class="tagchip' + (state.theme === "ruby" || state.theme === "sapphire" ? " tag-gen" : "") + '">R/S · ' + esc(t("view_front")) + '</span>' +
        '<span class="tagchip' + (state.theme === "firered" ? " tag-gen" : "") + '">FIRERED · ' + esc(t("formes.fr.label")) + '</span>' +
        '<span class="tagchip' + (state.theme === "leafgreen" ? " tag-gen" : "") + '">LEAFGREEN · ' + esc(t("formes.lg.label")) + '</span>' +
        '<span class="tagchip' + (state.theme === "emerald" ? " tag-gen" : "") + '">EMERALD · ' + esc(t("formes.em.label")) + '</span>' +
      '</div></div>' : '') +

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

    (typeof MovesUI !== "undefined" && MovesUI.sectionHTML ? MovesUI.sectionHTML(p) : "") +

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
    el.addEventListener("click", () => { state.text = el.dataset.txt; save("pkd_g3_text", state.text); renderDetail(); }));
  document.querySelectorAll("#detailPane .evo").forEach(el =>
    el.addEventListener("click", () => select(parseInt(el.dataset.id, 10))));
  if (typeof MovesUI !== "undefined" && MovesUI.wire) MovesUI.wire(p);
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
    save("pkd_g3_seen", [...state.seen]);
  }
}
function select(id, opts){
  state.sel = id;
  state.page = 1;
  save("pkd_g3_sel", id);
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
  save("pkd_g3_own", [...state.own]);
  renderList(); renderSpritePane(); renderCounters();
}
function toggleFav(){
  const id = state.sel;
  if (state.favs.has(id)) state.favs.delete(id); else state.favs.add(id);
  save("pkd_g3_favs", [...state.favs]);
  renderList(); renderSpritePane();
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
  if (typeof ItemsUI !== "undefined" && ItemsUI.syncIcons) ItemsUI.syncIcons();
}
function toggleLcd(){
  state.lcd = !state.lcd;
  save("pkd_g3_lcd", state.lcd);
  applyLcd();
  refreshMenuLabels();
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
  $("#menuPop [data-act=game] span:last-child").textContent = tpl(t("m_game_tpl"), {v: t("theme_short."+state.theme)});
  $("#menuPop [data-act=back] span:last-child").textContent = tpl(t("m_view_tpl"), {v: t(state.back ? "view_back" : "view_front")});
  $("#menuPop [data-act=shiny] span:last-child").textContent = tpl(t("m_shiny_tpl"), {v: state.shiny ? t("on") : t("off")});
  $("#menuPop [data-act=anim] span:last-child").textContent = tpl(t("m_anim_tpl"), {v: state.anim && state.theme === "emerald" ? t("on") : t("off")});
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
  if (typeof MovesUI !== "undefined" && MovesUI.applyLang) MovesUI.applyLang();
  if (typeof ItemsUI !== "undefined" && ItemsUI.applyLang) ItemsUI.applyLang();
  if (typeof LocUI !== "undefined" && LocUI.applyLang) LocUI.applyLang();
}
function toggleLang(){
  state.lang = state.lang === "en" ? "fa" : "en";
  save("pkd_lang", state.lang);
  applyLang();
}

/* ===== sort cycle ===== */
function cycleSort(){
  state.sort = state.sort === "id" ? "name" : state.sort === "name" ? "total" : "id";
  save("pkd_g3_sort", state.sort);
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
    save("pkd_g3_favonly", state.favOnly);
    $("#favBtn").classList.toggle("on", state.favOnly);
    renderList();
  });
  $("#randBtn").addEventListener("click", randomPick);
  $("#langBtn").addEventListener("click", toggleLang);
  $("#btnBack").addEventListener("click", toggleBack);
  $("#btnShiny").addEventListener("click", toggleShiny);
  $("#btnAnim").addEventListener("click", toggleAnim);
  $("#btnCry").addEventListener("click", playCry);
  $("#btnLcd").addEventListener("click", toggleLcd);
  $("#setRow").addEventListener("click", e => {
    const c = e.target.closest(".setchip");
    if (!c) return;
    if (c.id === "chipShiny") toggleShiny();
    else if (c.id === "chipAnim") toggleAnim();
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
    else if (act === "game") cycleTheme();
    else if (act === "shiny") toggleShiny();
    else if (act === "anim") toggleAnim();
    else if (act === "lcd") toggleLcd();
    else if (act === "back") toggleBack();
    else if (act === "fav"){ state.favOnly = !state.favOnly; save("pkd_g3_favonly", state.favOnly); $("#favBtn").classList.toggle("on", state.favOnly); renderList(); }
    else if (act === "sort") cycleSort();
    else if (act === "lang") toggleLang();
    else if (act === "reset"){
      if (confirm(t("reset_confirm"))){
        state.seen.clear(); state.own.clear();
        save("pkd_g3_seen", []); save("pkd_g3_own", []);
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
    else if (e.key.toLowerCase() === "s"){ toggleShiny(); }
    else if (e.key.toLowerCase() === "a"){ toggleAnim(); }
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
  if (h >= 1 && h <= 386 && PMAP[h]) state.sel = h;
  else { const s = parseInt(store("pkd_g3_sel", 252), 10); if (s >= 1 && s <= 386 && PMAP[s]) state.sel = s; }
  $("#favBtn").classList.toggle("on", state.favOnly);
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
