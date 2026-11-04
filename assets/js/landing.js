"use strict";
/* ================= games catalog — one item per game; complementary pairs share one ================= */
const GAMES = [
  {gen:1, g:"GEN 1", region:{en:"Kanto",fa:"کانتو"}, items:[
    {id:"gen1", en:"Pokémon Red · Blue · Green · Yellow", fa:"پوکمون قرمز · آبی · سبز · زرد", c:["#c8433c","#3d6ab8"], href:"gen1.html", active:true}
  ]},
  {gen:2, g:"GEN 2", region:{en:"Johto",fa:"جوتو"}, items:[
    {id:"goldsilver", en:"Pokémon Gold/Silver", fa:"پوکمون طلایی و نقره‌ای", c:["#d8a028","#8a94a8"], href:"goldsilver.html", active:true},
    {id:"crystal",     en:"Pokémon Crystal",     fa:"پوکمون کریستال",         c:["#7ec8d8","#3a7a8c"], href:"crystal.html", active:true}
  ]},
  {gen:3, g:"GEN 3", region:{en:"Hoenn",fa:"هوئن"}, items:[
    {id:"rubysapphire", en:"Pokémon Ruby/Sapphire", fa:"پوکمون یاقوت و یاقوت کبود", c:["#d84048","#3870c8"]},
    {id:"emerald",       en:"Pokémon Emerald",        fa:"پوکمون زمرد",               c:["#48a858","#1b632c"], href:"emerald.html", active:true},
    {id:"frlg",          en:"FireRed/LeafGreen",      fa:"آتشین قرمز و برگ سبز",      c:["#e86a3a","#58b868"]}
  ]},
  {gen:4, g:"GEN 4", region:{en:"Sinnoh",fa:"سینو"}, items:[
    {id:"diamondpearl", en:"Pokémon Diamond/Pearl", fa:"پوکمون الماس و مروارید", c:["#68a8d8","#d890b0"]},
    {id:"platinum",      en:"Pokémon Platinum",       fa:"پوکمون پلاتین",           c:["#b8c0cc","#5a6470"]},
    {id:"hgss",          en:"HeartGold/SoulSilver",   fa:"قلب طلایی و روح نقره‌ای",  c:["#e8b040","#9aa5b8"]}
  ]},
  {gen:5, g:"GEN 5", region:{en:"Unova",fa:"یونوف"}, items:[
    {id:"blackwhite",   en:"Pokémon Black/White",     fa:"پوکمون سیاه و سفید",   c:["#3a3f4a","#d8dce4"]},
    {id:"black2white2", en:"Pokémon Black 2/White 2", fa:"پوکمون سیاه ۲ و سفید ۲", c:["#2a2f3a","#a0a4b0"]}
  ]},
  {gen:6, g:"GEN 6", region:{en:"Kalos",fa:"کالوس"}, items:[
    {id:"xy",   en:"Pokémon X/Y",                 fa:"پوکمون ایکس و وای",       c:["#3858a8","#c83848"]},
    {id:"oras", en:"Omega Ruby/Alpha Sapphire",   fa:"امگا یاقوت و آلفا یاقوت کبود", c:["#c03038","#2860b8"]}
  ]},
  {gen:7, g:"GEN 7", region:{en:"Alola",fa:"آلولا"}, items:[
    {id:"sunmoon", en:"Pokémon Sun/Moon",       fa:"پوکمون خورشید و ماه", c:["#f09030","#4868b0"]},
    {id:"usum",    en:"Ultra Sun/Ultra Moon",   fa:"فراخورشید و فراماه",   c:["#f0a028","#3858a0"]}
  ]},
  {gen:8, g:"GEN 8", region:{en:"Galar",fa:"گالار"}, items:[
    {id:"swordshield", en:"Pokémon Sword/Shield",           fa:"پوکمون شمشیر و سپر",        c:["#3898b8","#c84858"]},
    {id:"bdsp",        en:"Brilliant Diamond/Shining Pearl", fa:"الماس درخشان و مروارید درخشان", c:["#58a0d0","#c890b8"]},
    {id:"arceus",      en:"Legends: Arceus",                 fa:"افسانه‌ها: آرسیوس",          c:["#b0a890","#5e584a"]}
  ]},
  {gen:9, g:"GEN 9", region:{en:"Paldea",fa:"پالدیا"}, items:[
    {id:"scarletviolet", en:"Pokémon Scarlet/Violet", fa:"پوکمون سرخ و بنفش", c:["#d84a3a","#7850b8"]}
  ]}
];

/* ================= i18n ================= */
const I18N = {
en:{
  brand:"POKéDEX PROJECT", brand_sub:"ONE DEX PER GAME",
  hero_title:'THE POKéDEX <span class="accent">PROJECT</span>',
  hero_sub:"A growing collection of offline, in-game-style Pokédexes — every Pokémon game gets its own dex, and complementary pairs like Red/Blue share one. Generation I is all four Game Boy games in a single dex. Pick a game and start exploring.",
  fact1:"<b>386</b> Pokémon available", fact2:"<b>2</b> languages · EN / FA",
  fact3:"<b>100%</b> offline · static site", fact4:"<b>19</b> games planned",
  featured_kick:"● AVAILABLE NOW",
  featured_title:"POKéMON EMERALD — GEN 3 DEX",
  featured_desc:"The full in-game Pokédex experience of Pokémon Emerald: all 386 Pokémon of Generations I-III with Emerald-style sprites — including the game's animated battle sprites — dex entries, stats, type matchups and evolutions, styled after the dex inside the game itself.",
  fm1:"Emerald visual style", fm2:"Normal + Shiny sprites", fm3:"Animated battle sprites", fm4:"Seen / Owned tracking",
  featured2_kick:"● AVAILABLE NOW",
  featured2_title:"GENERATION I — RED · BLUE · GREEN · YELLOW",
  featured2_desc:"All four Gen-1 games in one dex: switch the GAME chips between Pokémon Red, Blue, the Japan-only 1996 Green and Yellow — each with its own theme, its own sprites (Game Boy mono DMG/Pocket + colorized sets, front & back) and its own dex texts, with every entry readable in either the Red/Blue or the Yellow wording. Moves and learnsets follow the selected game, plus authentic cries and the same structure as the Emerald dex.",
  fm5:"Four game themes in one page", fm6:"Every Gen-1 sprite set + back sprites", fm7:"R/B and Yellow texts, selectable", fm8:"Moves per game",
  featured4_kick:"● AVAILABLE NOW",
  featured4_title:"POKéMON GOLD & SILVER — GEN 2 DEX",
  featured4_desc:"The in-game Pokédex of Pokémon Gold and Silver: all 251 Johto + Kanto Pokémon with each version's own front and back sprites — plus their shiny variants, introduced in this very generation — both versions' dex texts side by side, the GOLD/SILVER theme toggle, authentic cries and the same structure as the Emerald dex.",
  fm13:"Game Boy Color visual style", fm14:"Gold + Silver sprites (+ Shiny + back)", fm15:"Both versions' dex texts", fm16:"Same structure as Emerald",
  featured5_kick:"● AVAILABLE NOW",
  featured5_title:"POKéMON CRYSTAL — GEN 2 DEX",
  featured5_desc:"The in-game Pokédex of Pokémon Crystal: all 251 Johto + Kanto Pokémon with Crystal's own front and back sprites, shiny variants and its fully rewritten dex entries — plus the series' very first animated battle sprites, togglable just like the Emerald dex, with authentic cries and the same structure.",
  fm17:"Game Boy Color (Crystal) visual style", fm18:"Crystal sprites (+ Shiny + back)", fm19:"Animated battle sprites — a series first", fm20:"Crystal's rewritten dex entries",
  play:"▶ OPEN DEX",
  games_t:"GAME CATALOG", games_s:"Every Pokémon game gets its own dex — Generation I is all four Game Boy games in one; complementary pairs like Gold/Silver share one item.", games_cnt:"4 / 19 RELEASED",
  gen_label:"GENERATION {n} · {r}",
  status_ok:"PLAY NOW", status_soon:"COMING SOON", meta_fmt:"{r} region",
  roadmap_t:"ROADMAP",
  roadmap_p1:"This project grows game by game. Each new Pokédex is rebuilt to match its own game — the UI style of that era, the regional dex of that version, the sprites and entry texts of that release. Emerald is the first one; more will follow.",
  step1_t:"Emerald (Gen 3)", step1_d:"The in-game Emerald dex for all 386 Pokémon of Gens I-III — live now.",
  step2_t:"Generation I (Red · Blue · Green · Yellow)", step2_d:"All four Game Boy games of 1996-99 in one dex — four themes, every sprite set, both text versions and per-game moves — live now.",
  step3_t:"Gold/Silver & Crystal (Gen 2)", step3_d:"Gold/Silver with both versions' sprites, texts and shiny variants; Crystal with its animated sprites — live now.",
  step4_t:"Next games", step4_d:"Ruby/Sapphire and more — one dex per game, each faithful to its original look.",
  foot1:"Fan-made, non-commercial project. Pokémon © Nintendo / Creatures Inc. / GAME FREAK inc.",
  foot2:"No game assets are redistributed; sprites are rendered from open data via PokeAPI. Pages run 100% offline.",
  title:"Pokédex Project — Classic Pokémon Dexes, Game by Game"
},
fa:{
  brand:"پروژه پوکیدکس", brand_sub:"برای هر بازی یک پوکیدکس",
  hero_title:'پروژه <span class="accent">پوکیدکس</span>',
  hero_sub:"مجموعه‌ای در حال رشد از پوکیدکس‌های آفلاین با ظاهر داخل بازی — برای هر بازی پوکمون یک پوکیدکس، و نسخه‌های مکمل مثل قرمز/آبی یک آیتم مشترک دارند. نسل اول هر چهار بازی گیم‌بوی را در یک پوکیدکس واحد دارد. یک بازی را انتخاب کنید و شروع کنید.",
  fact1:"<b>۳۸۶</b> پوکمون موجود", fact2:"<b>۲</b> زبان · فارسی/انگلیسی",
  fact3:"<b>۱۰۰٪</b> آفلاین · سایت استاتیک", fact4:"<b>۱۹</b> بازی در برنامه",
  featured_kick:"● هم‌اکنون موجود است",
  featured_title:"پوکمون زمرد — پوکیدکس نسل ۳",
  featured_desc:"تجربه کامل پوکیدکس داخل بازی Pokémon Emerald: هر ۳۸۶ پوکمون نسل‌های ۱ تا ۳ با اسپرایت‌های سبک زمرد — همراه با انیمیشن‌های نبردی خود بازی — توضیحات پوکیدکس، آمار، تناسب انواع و تکامل‌ها — دقیقاً با ظاهر پوکیدکس داخل خود بازی.",
  fm1:"ظاهر سبک زمرد", fm2:"اسپرایت عادی + براق", fm3:"اسپرایت‌های متحرک نبرد", fm4:"ثبت دیده‌شده / گرفته‌شده",
  featured2_kick:"● هم‌اکنون موجود است",
  featured2_title:"نسل اول — قرمز · آبی · سبز · زرد",
  featured2_desc:"هر چهار بازی نسل اول در یک پوکیدکس: با چیپ‌های بازی بین پوکمون قرمز، آبی، سبزِ فقط‌ژاپنی ۱۹۹۶ و زرد جابه‌جا شوید — هر کدام با تم، اسپرایت‌های (تک‌رنگ DMG/پاکت + رنگی، جلو و پشت) و متن‌های پوکیدکس خودش، و هر توضیح را می‌توان با متن قرمز/آبی یا زرد خواند. حرکت‌ها و روش یادگیری هم از همان بازی دنبال می‌شوند — به‌همراه صدای اصلی پوکمون‌ها و همان ساختار پوکیدکس زمرد.",
  fm5:"چهار تم بازی در یک صفحه", fm6:"همه اسپرایت‌های نسل ۱ + پشت", fm7:"متن‌های قرمز/آبی و زرد، قابل انتخاب", fm8:"حرکت‌ها به تفکیک بازی",
  featured4_kick:"● هم‌اکنون موجود است",
  featured4_title:"پوکمون گلد و سیلور — پوکیدکس نسل ۲",
  featured4_desc:"پوکیدکس داخل بازی‌های Pokémon Gold و Silver: هر ۲۵۱ پوکمون جوهدو + کانتو با اسپرایت‌های جلو و پشتِ مخصوص هر نسخه — به‌همراه واریانت‌های براق (شاینی) که دقیقاً در همین نسل معرفی شدند — متن‌های داکس هر دو نسخه کنار هم، تاگل تم گلد/سیلور، صدای اصلی پوکمون‌ها و همان ساختار پوکیدکس زمرد.",
  fm13:"ظاهر گیم‌بوی کالر", fm14:"اسپرایت گلد + سیلور (+ شاینی + پشت)", fm15:"متن داکس هر دو نسخه", fm16:"همان ساختار پوکیدکس زمرد",
  featured5_kick:"● هم‌اکنون موجود است",
  featured5_title:"پوکمون کریستال — پوکیدکس نسل ۲",
  featured5_desc:"پوکیدکس داخل بازی Pokémon Crystal: هر ۲۵۱ پوکمون جوهدو + کانتو با اسپرایت‌های جلو و پشتِ خود کریستال، واریانت‌های براق و متن‌های داکس کاملاً بازنویسی‌شده‌ی آن — به‌همراه نخستین اسپرایت‌های متحرک نبرد در تاریخ این سری، با تاگلی مثل پوکیدکس زمرد، صدای اصلی پوکمون‌ها و همان ساختار.",
  fm17:"ظاهر گیم‌بوی کالر (کریستال)", fm18:"اسپرایت کریستال (+ شاینی + پشت)", fm19:"اسپرایت‌های متحرک نبرد — اولین در سری", fm20:"متن‌های بازنویسی‌شده‌ی کریستال",
  play:"▶ ورود به پوکیدکس",
  games_t:"فهرست بازی‌ها", games_s:"برای هر بازی پوکمون یک پوکیدکس ساخته می‌شود — نسل اول هر چهار بازی گیم‌بوی را در یک صفحه دارد؛ نسخه‌های مکمل مثل گلد/سیلور یک آیتم مشترک دارند.", games_cnt:"۴ از ۱۹ منتشر شده",
  gen_label:"نسل {n} · {r}",
  status_ok:"هم‌اکنون بازی کنید", status_soon:"به‌زودی", meta_fmt:"منطقه {r}",
  roadmap_t:"نقشه راه",
  roadmap_p1:"این پروژه بازی‌به‌بازی بزرگ می‌شود. هر پوکیدکس جدید از نو و مطابق همان بازی ساخته می‌شود — استایل رابط کاربری همان دوران، پوکیدکس منطقه‌ای همان نسخه، و اسپرایت‌ها و متن‌های همان انتشار. زمرد اولین است؛ بقیه هم می‌آیند.",
  step1_t:"زمرد (نسل ۳)", step1_d:"پوکیدکس داخل بازی زمرد برای هر ۳۸۶ پوکمون نسل‌های ۱ تا ۳ — هم‌اکنون فعال است.",
  step2_t:"نسل اول (قرمز · آبی · سبز · زرد)", step2_d:"هر چهار بازی گیم‌بوی ۱۹۹۶ تا ۹۹ در یک پوکیدکس — چهار تم، همه مجموعه‌های اسپرایت، هر دو نسخه متن و حرکت‌های هر بازی — هم‌اکنون فعال است.",
  step3_t:"گلد/سیلور و کریستال (نسل ۲)", step3_d:"گلد/سیلور با اسپرایت، متن و واریانت براق هر دو نسخه؛ کریستال با اسپرایت‌های متحرکش — هم‌اکنون فعال است.",
  step4_t:"بازی‌های بعدی", step4_d:"یاقوت/یاقوت کبود و بیشتر — برای هر بازی یک پوکیدکس، وفادار به ظاهر اصلی‌اش.",
  foot1:"پروژه‌ای غیرتجاری ساخته‌ی طرفداران. پوکمون © نینتندو / کرچرز / گیم‌فریک.",
  foot2:"هیچ دارایی بازی توزیع نمی‌شود؛ اسپرایت‌ها از داده باز PokeAPI رندر شده‌اند. صفحه‌ها کاملاً آفلاین اجرا می‌شوند.",
  title:"پروژه پوکیدکس — پوکیدکس کلاسیک برای هر بازی"
}};

/* ================= state & helpers ================= */
const state = { lang: "en" };
try { if (JSON.parse(localStorage.getItem("pdx_lang") || "null") === "fa") state.lang = "fa"; } catch(e){}
const $ = s => document.querySelector(s);
const t = k => { const v = k.split(".").reduce((o,p)=>o&&o[p], I18N[state.lang]); return v === undefined ? k : v; };
const tpl = (s, o) => s.replace(/\{(\w+)\}/g, (_,k)=> o[k] !== undefined ? o[k] : "{"+k+"}");
const faD = n => String(n).replace(/[0-9]/g, d => "۰۱۲۳۴۵۶۷۸۹"[+d]);
const num = n => state.lang === "fa" ? faD(n) : String(n);

function cardHtml(g, it){
  const active = !!it.active;
  const inner =
    '<span class="strip" style="--c1:' + it.c[0] + ';--c2:' + it.c[1] + '">' +
      '<span class="nm"><bdi>' + (state.lang === "fa" ? it.fa : it.en) + '</bdi></span>' +
      '<span class="nm2">' + g.g + '</span>' +
    '</span>' +
    '<span class="foot">' +
      '<span class="meta">' + tpl(t("meta_fmt"), {r: state.lang === "fa" ? g.region.fa : g.region.en}) + '</span>' +
      '<span class="status ' + (active ? "ok" : "soon") + '">' + (active ? t("status_ok") : t("status_soon")) + '</span>' +
    '</span>';
  return active
    ? '<a class="card active" href="' + it.href + '">' + inner + '</a>'
    : '<div class="card locked">' + inner + '</div>';
}

function renderGens(){
  $("#gens").innerHTML = GAMES.map(g =>
    '<div class="sec" style="margin-top:26px">' +
      '<div class="sec-h">' +
        '<span class="st" style="font-size:10.5px">' + tpl(t("gen_label"), {n: num(g.gen), r: state.lang === "fa" ? g.region.fa : g.region.en}) + '</span>' +
      '</div>' +
      '<div class="cards">' + g.items.map(it => cardHtml(g, it)).join("") + '</div>' +
    '</div>').join("");
}

function applyLang(){
  document.documentElement.lang = state.lang;
  document.body.dir = state.lang === "fa" ? "rtl" : "ltr";
  document.body.classList.toggle("fa", state.lang === "fa");
  document.title = t("title");
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const v = t(el.getAttribute("data-i18n"));
    if (typeof v === "string" && v) el.textContent = v;
  });
  document.querySelectorAll("[data-i18n-html]").forEach(el => {
    const v = t(el.getAttribute("data-i18n-html"));
    if (typeof v === "string" && v) el.innerHTML = v;
  });
  $("#langBtn").textContent = state.lang === "en" ? "فارسی" : "English";
  renderGens();
}

$("#langBtn").addEventListener("click", () => {
  state.lang = state.lang === "en" ? "fa" : "en";
  try { localStorage.setItem("pdx_lang", JSON.stringify(state.lang)); } catch(e){}
  applyLang();
});

applyLang();
