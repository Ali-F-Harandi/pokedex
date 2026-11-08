"use strict";
/* ================= games catalog — one item per game; complementary pairs share one ================= */
const GAMES = [
  {gen:1, g:"GEN 1", region:{en:"Kanto",fa:"کانتو"}, items:[
    {id:"gen1", en:"Pokémon Red · Blue · Green · Yellow", fa:"پوکمون قرمز · آبی · سبز · زرد", c:["#c8433c","#3d6ab8"], href:"gen1.html", active:true}
  ]},
  {gen:2, g:"GEN 2", region:{en:"Johto",fa:"جوتو"}, items:[
    {id:"gen2", en:"Pokémon Gold · Silver · Crystal", fa:"پوکمون طلایی · نقره‌ای · کریستال", c:["#d8a028","#4ab8c4"], href:"gen2.html", active:true}
  ]},
  {gen:3, g:"GEN 3", region:{en:"Hoenn",fa:"هوئن"}, items:[
    {id:"gen3", en:"Pokémon Ruby · Sapphire · Emerald · FireRed · LeafGreen", fa:"پوکمون یاقوت · یاقوت کبود · زمرد · آتشین قرمز · برگ سبز", c:["#d84048","#38a868"], href:"gen3.html", active:true}
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
  hero_sub:"A growing collection of offline, in-game-style Pokédexes — one dex per generation, and complementary pairs share one. Generation I is all four Game Boy games in a single dex; Generation II is all three Game Boy Color games in one; Generation III is all five Game Boy Advance games in one. Pick a game and start exploring.",
  fact1:"<b>386</b> Pokémon available", fact2:"<b>2</b> languages · EN / FA",
  fact3:"<b>100%</b> offline · static site", fact4:"<b>19</b> games planned",
  featured_kick:"● AVAILABLE NOW",
  featured_title:"GENERATION III — RUBY · SAPPHIRE · EMERALD · FIRERED · LEAFGREEN",
  featured_desc:"All five Gen-3 games in one dex, on the Game Boy Advance: switch the GAME chips between Pokémon Ruby, Sapphire, Emerald, FireRed and LeafGreen — each with its own theme, its own GBA sprites (front & back, shiny on every set) and its own dex texts, readable in the R/S, Emerald, FireRed or LeafGreen wording. Gen 3's own signatures are era-true: abilities with no hidden slots (they did not exist yet), Deoxys whose forme, stats and sprite change with the cartridge — Normal on R/S, Attack on FireRed, Defense on LeafGreen, Speed on Emerald — and Emerald's animated battle sprites on the ANIM chip. Authentic cries and the same structure as the Gen-1/Gen-2 dexes.",
  fm1:"Five game themes in one page", fm2:"R/S + Emerald + FRLG sprite banks (+ Shiny + back)", fm3:"Emerald's animated battle sprites", fm4:"Deoxys: per-cartridge formes, like the real games",
  featured2_kick:"● AVAILABLE NOW",
  featured2_title:"GENERATION I — RED · BLUE · GREEN · YELLOW",
  featured2_desc:"All four Gen-1 games in one dex: switch the GAME chips between Pokémon Red, Blue, the Japan-only 1996 Green and Yellow — each with its own theme, its own sprites (Game Boy mono DMG/Pocket + colorized sets, front & back) and its own dex texts, with every entry readable in either the Red/Blue or the Yellow wording. Moves and learnsets follow the selected game, and the Item Dex and the Location Dex (every Kanto location with per-game encounter tables) plus a HOW TO CATCH section on every Pokémon round it off — authentic cries and the same structure as the Emerald dex.",
  fm5:"Four game themes in one page", fm6:"Every Gen-1 sprite set + back sprites", fm7:"R/B and Yellow texts, selectable", fm8:"Moves + Item & Location Dex per game",
  featured4_kick:"● AVAILABLE NOW",
  featured4_title:"GENERATION II — GOLD · SILVER · CRYSTAL",
  featured4_desc:"All three Gen-2 games in one dex, one console generation later: switch the GAME chips between Pokémon Gold, Silver and Crystal — each with its own theme, its own GBC sprites (front & back) and its own dex texts, readable in the Gold, Silver or Crystal wording. Gen 2's own additions are all here: shiny variants on every set (introduced in this very generation), the series' first animated battle sprites on the Crystal set, Dark and Steel types with authentic Gen-2 type mechanics, and a Game Boy Color shell for the whole dex — authentic cries and the same structure as the Gen-1 dex.",
  fm13:"Three game themes in one page", fm14:"Gold + Silver + Crystal sprites (+ Shiny + back)", fm15:"Animated battle sprites — a series first", fm16:"Game Boy Color shell, same structure as Gen 1",
  play:"▶ OPEN DEX",
  games_t:"GAME CATALOG", games_s:"Every Pokémon game gets its own dex — Generation I is all four Game Boy games in one; Generation II is all three Game Boy Color games in one; Generation III is all five Game Boy Advance games in one.", games_cnt:"3 / 19 RELEASED",
  gen_label:"GENERATION {n} · {r}",
  status_ok:"PLAY NOW", status_soon:"COMING SOON", meta_fmt:"{r} region",
  roadmap_t:"ROADMAP",
  roadmap_p1:"This project grows game by game. Each new Pokédex is rebuilt to match its own game — the UI style of that era, the regional dex of that version, the sprites and entry texts of that release. Emerald is the first one; more will follow.",
  step1_t:"Emerald (Gen 3)", step1_d:"The in-game Emerald dex for all 386 Pokémon of Gens I-III — live now.",
  step2_t:"Generation I (Red · Blue · Green · Yellow)", step2_d:"All four Game Boy games of 1996-99 in one dex — four themes, every sprite set, both text versions and per-game moves — live now.",
  step3_t:"Generation II (Gold · Silver · Crystal)", step3_d:"All three Gen-2 games in one Game Boy Color-styled dex — every game's own sprites, texts and theme, shiny variants and the series' first animated sprites — live now.",
  step3b_t:"Generation III (Ruby · Sapphire · Emerald · FireRed · LeafGreen)", step3b_d:"All five Gen-3 games in one Game Boy Advance-styled dex — every game's own sprites, texts and theme, era-true abilities, the cartridge-bound Deoxys formes and Emerald's animated sprites — live now.",
  step4_t:"Next games", step4_d:"Diamond/Pearl and more — one dex per generation, each faithful to its original look.",
  foot1:"Fan-made, non-commercial project. Pokémon © Nintendo / Creatures Inc. / GAME FREAK inc.",
  foot2:"No game assets are redistributed; sprites are rendered from open data via PokeAPI. Pages run 100% offline.",
  title:"Pokédex Project — Classic Pokémon Dexes, Game by Game"
},
fa:{
  brand:"پروژه پوکیدکس", brand_sub:"برای هر بازی یک پوکیدکس",
  hero_title:'پروژه <span class="accent">پوکیدکس</span>',
  hero_sub:"مجموعه‌ای در حال رشد از پوکیدکس‌های آفلاین با ظاهر داخل بازی — برای هر نسل یک پوکیدکس، و نسخه‌های مکمل یک آیتم مشترک دارند. نسل اول هر چهار بازی گیم‌بوی را در یک پوکیدکس دارد، نسل دوم هر سه بازی گیم‌بوی کالر را در یک صفحه و نسل سوم هر پنج بازی گیم‌بوی ادونس را در یک صفحه. یک بازی را انتخاب کنید و شروع کنید.",
  fact1:"<b>۳۸۶</b> پوکمون موجود", fact2:"<b>۲</b> زبان · فارسی/انگلیسی",
  fact3:"<b>۱۰۰٪</b> آفلاین · سایت استاتیک", fact4:"<b>۱۹</b> بازی در برنامه",
  featured_kick:"● هم‌اکنون موجود است",
  featured_title:"نسل سوم — یاقوت · یاقوت کبود · زمرد · آتشین قرمز · برگ سبز",
  featured_desc:"هر پنج بازی نسل سوم در یک پوکیدکس، روی گیم‌بوی ادونس: با چیپ‌های بازی بین پوکمون یاقوت، یاقوت کبود، زمرد، آتشین قرمز و برگ سبز جابه‌جا شوید — هر کدام با تم خودش، اسپرایت‌های GBA خودش (جلو و پشت، شاینی روی همه‌ی مجموعه‌ها) و متن‌های پوکیدکس خودش که با متن R/S، زمرد، آتشین قرمز یا برگ سبز قابل خواندن است. امضاهای خودِ نسل ۳ اصیل‌اند: توانایی‌هایی بدون جایگاه پنهان (هنوز وجود نداشتند)، دِآوکسی که فرم، آمار و اسپرایتش با کارتریج عوض می‌شود — عادی روی R/S، حمله روی آتشین قرمز، دفاع روی برگ سبز، سرعت روی زمرد — و اسپرایت‌های متحرک نبرد زمرد روی چیپ ANIM. صدای اصلی پوکمون‌ها و همان ساختار پوکیدکس‌های نسل ۱ و ۲.",
  fm1:"پنج تم بازی در یک صفحه", fm2:"بانک اسپرایت R/S + زمرد + FRLG (+ شاینی + پشت)", fm3:"اسپرایت‌های متحرک نبرد زمرد", fm4:"دِآوکس: فرم‌های وابسته به کارتریج، مثل خود بازی‌ها",
  featured2_kick:"● هم‌اکنون موجود است",
  featured2_title:"نسل اول — قرمز · آبی · سبز · زرد",
  featured2_desc:"هر چهار بازی نسل اول در یک پوکیدکس: با چیپ‌های بازی بین پوکمون قرمز، آبی، سبزِ فقط‌ژاپنی ۱۹۹۶ و زرد جابه‌جا شوید — هر کدام با تم، اسپرایت‌های (تک‌رنگ DMG/پاکت + رنگی، جلو و پشت) و متن‌های پوکیدکس خودش، و هر توضیح را می‌توان با متن قرمز/آبی یا زرد خواند. حرکت‌ها و روش یادگیری هم از همان بازی دنبال می‌شوند؛ دکس آیتم و دکس مکان‌ها (همه‌ی مکان‌های کانتو با جدول مواجهه‌ی هر بازی) و بخش «نحوه‌ی به‌دست‌آوردن» روی هر پوکمون هم همین‌طور — به‌همراه صدای اصلی پوکمون‌ها و همان ساختار پوکیدکس زمرد.",
  fm5:"چهار تم بازی در یک صفحه", fm6:"همه اسپرایت‌های نسل ۱ + پشت", fm7:"متن‌های قرمز/آبی و زرد، قابل انتخاب", fm8:"حرکت‌ها، دکس آیتم و دکس مکان‌ها به تفکیک بازی",
  featured4_kick:"● هم‌اکنون موجود است",
  featured4_title:"نسل دوم — طلایی · نقره‌ای · کریستال",
  featured4_desc:"هر سه بازی نسل دوم در یک پوکیدکس، یک نسلِ کنسول بالاتر: با چیپ‌های بازی بین پوکمون گلد، سیلور و کریستال جابه‌جا شوید — هر کدام با تم خودش، اسپرایت‌های GBC خودش (جلو و پشت) و متن‌های پوکیدکس خودش که با متن گلد، سیلور یا کریستال قابل خواندن است. اضافه‌های خودِ نسل ۲ هم همه اینجا هستند: واریانت شاینی روی همه مجموعه‌ها (که دقیقاً در همین نسل معرفی شد)، نخستین اسپرایت‌های متحرک نبرد تاریخ سری روی مجموعه کریستال، تایپ‌های تاریک و فولادی با مکانیک اصیل نسل ۲، و بدنه‌ی گیم‌بوی کالر برای کل پوکیدکس — صدای اصلی پوکمون‌ها و همان ساختار پوکیدکس نسل اول.",
  fm13:"سه تم بازی در یک صفحه", fm14:"اسپرایت گلد + سیلور + کریستال (+ شاینی + پشت)", fm15:"اسپرایت متحرک نبرد — اولین در سری", fm16:"بدنه گیم‌بوی کالر، همان ساختار نسل ۱",
  play:"▶ ورود به پوکیدکس",
  games_t:"فهرست بازی‌ها", games_s:"برای هر بازی پوکمون یک پوکیدکس ساخته می‌شود — نسل اول هر چهار بازی گیم‌بوی را در یک صفحه دارد، نسل دوم هر سه بازی گیم‌بوی کالر را و نسل سوم هر پنج بازی گیم‌بوی ادونس را.", games_cnt:"۳ از ۱۹ منتشر شده",
  gen_label:"نسل {n} · {r}",
  status_ok:"هم‌اکنون بازی کنید", status_soon:"به‌زودی", meta_fmt:"منطقه {r}",
  roadmap_t:"نقشه راه",
  roadmap_p1:"این پروژه بازی‌به‌بازی بزرگ می‌شود. هر پوکیدکس جدید از نو و مطابق همان بازی ساخته می‌شود — استایل رابط کاربری همان دوران، پوکیدکس منطقه‌ای همان نسخه، و اسپرایت‌ها و متن‌های همان انتشار. زمرد اولین است؛ بقیه هم می‌آیند.",
  step1_t:"زمرد (نسل ۳)", step1_d:"پوکیدکس داخل بازی زمرد برای هر ۳۸۶ پوکمون نسل‌های ۱ تا ۳ — هم‌اکنون فعال است.",
  step2_t:"نسل اول (قرمز · آبی · سبز · زرد)", step2_d:"هر چهار بازی گیم‌بوی ۱۹۹۶ تا ۹۹ در یک پوکیدکس — چهار تم، همه مجموعه‌های اسپرایت، هر دو نسخه متن و حرکت‌های هر بازی — هم‌اکنون فعال است.",
  step3_t:"نسل دوم (طلایی · نقره‌ای · کریستال)", step3_d:"هر سه بازی نسل دوم در یک پوکیدکس با ظاهر گیم‌بوی کالر — اسپرایت، متن و تم هر بازی، واریانت‌های شاینی و نخستین اسپرایت‌های متحرک سری — هم‌اکنون فعال است.",
  step3b_t:"نسل سوم (یاقوت · یاقوت کبود · زمرد · آتشین قرمز · برگ سبز)", step3b_d:"هر پنج بازی نسل سوم در یک پوکیدکس با ظاهر گیم‌بوی ادونس — اسپرایت، متن و تم هر بازی، توانایی‌های اصیل نسل ۳، فرم‌های وابسته به کارتریجِ دِآوکس و اسپرایت‌های متحرک زمرد — هم‌اکنون فعال است.",
  step4_t:"بازی‌های بعدی", step4_d:"الماس/مروارید و بیشتر — برای هر نسل یک پوکیدکس، وفادار به ظاهر اصلی‌اش.",
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
