"use strict";
/* Pokédex Plus — LOCATION DEX module, GENERATION II (gen2.html).
   ============================================================
   Loaded AFTER locations-gen2.js (LOC2). Sister of gen1's
   locations-module.js — same LocUI global and same API surface
   (openDex / closeDex / applyLang / sectionHTML / wire /
   renderSection / syncGame), rendered against Gen 2's richer
   encounter model:

     · per-game tables with a fallback chain (silver→gold,
       crystal→silver-or-gold; explicit null = truly no wilds)
     · grass in three time-of-day tables (MORN / DAY / NITE),
       7 slots at the shared 30/30/20/10/5/4/1 chances
     · surf: 3 slots, the engine rolls +0..+4 over the listed level
     · fishing per fish group (Old/Good/Super rods with authentic
       slot percentages; some slots differ by night — TimeFishGroups)
     · headbutt trees & rock smash (common/rare tree sets)
     · swarms (grass: Crystal's Yanma/Dunsparce; fishing: Qwilfish
       on Route 32, Remoraid on Route 44 in G/S)
     · the Bug-Catching Contest at the National Park
     · specials: starters, Mystery/Odd eggs, gifts, in-game trades,
       Game Corner prizes, statics, roaming beasts, the Celebi event

   Everything user-visible is bilingual EN/FA (LI table below). */

const LocUI = (() => {

  /* ================= i18n ================= */
  const LI = {
    en: {
      dex_t: "LOCATION DEX", sec_t: "HOW TO CATCH", close: "Close", back: "◂ BACK",
      search_ph: "Search a location…", no_results: "No locations found.",
      count: "{a} locations", all: "ALL",
      regions: { j: "JOHTO", k: "KANTO" },
      groups: { route: "Routes", city: "Cities & towns", cave: "Caves", forest: "Forests", building: "Buildings" },
      games: { gold: "GOLD", silver: "SILVER", crystal: "CRYSTAL" },
      times: { m: "MORN", d: "DAY", n: "NITE" },
      grass: "GRASS", surf: "SURF",
      rods: { o: "OLD ROD", g: "GOOD ROD", s: "SUPER ROD" },
      hb: "HEADBUTT", rk: "ROCK SMASH", sw: "SWARM", ct: "BUG CONTEST",
      rate_tpl: "ENCOUNTER RATE {r}/255 ≈ {p}% per step",
      bite_tpl: "bite chance ≈ {p}%",
      wild_t: "IN THE WILD", special_t: "SPECIAL WAYS", evo_t: "BY EVOLUTION",
      none_t: "NOT IN THIS GAME",
      none_note: "This Pokémon cannot be obtained in {g} alone — it lives in {list}. Trade with a friend!",
      none_nowhere: "No normal encounter exists in any of the three games — event/trade only.",
      lvl: "Lv {n}", lvl_rng: "Lv {a}–{b}",
      common: "common", rare: "rare", pct_of: "{p}%",
      menu_locations: "Location Dex", all_locations: "ALL LOCATIONS",
      kinds: { starter: "STARTER", egg: "EGG", gift: "GIFT", trade: "TRADE", corner: "GAME CORNER",
               static: "FIXED", roamer: "ROAMING", event: "EVENT" },
      evo_start: "start from", evo_of: "evolves from",
      conds: { level: "Lv {n}", trade: "Trade", use_item: "Use {i}", happiness: "Happy{t}",
               happiness_day: " (day)", happiness_night: " (night)", beauty: "Beauty {n}",
               shed: "empty party slot + Poké Ball", special: "Special" },
      items: { "fire-stone": "Fire Stone", "water-stone": "Water Stone", "thunder-stone": "Thunder Stone",
               "leaf-stone": "Leaf Stone", "moon-stone": "Moon Stone", "sun-stone": "Sun Stone",
               "kings-rock": "King's Rock", "metal-coat": "Metal Coat", "dragon-scale": "Dragon Scale",
               "up-grade": "Up-Grade", "deep-sea-tooth": "Deep Sea Tooth", "deep-sea-scale": "Deep Sea Scale" },
      unown_note: "The Ruins of Alph walls hold UNOWN — which letters appear depends on how many of the four puzzle chambers you have solved.",
      contest_note: "Bug-Catching Contest (Tue/Thu/Sat): free entry, 20 Park Balls, 20 minutes — you keep only ONE Pokémon.",
      headbutt_note: "Shaking trees: the common table (10%/50% trigger on ordinary trees); trees of the rare kind pull from the rare table 80% of the time.",
      rock_note: "Smashing the breakable rocks can also find Shuckle (10%).",
      swarm_note: "Phone-call swarms replace this map's tables for the day — answer the trainer's call, then come back.",
      fish_note: "Every cast first rolls the bite chance, then picks a slot from the table.",
      surf_note: "Surfing levels roll +0 to +4 over the listed level.",
      friday_note: "appears on Fridays only",
      roam_note: "flees every turn — weaken it fast, or throw a fast Ball first",
      oldrod_note: "Old Rod hooks Magikarp Lv 10 in every water — anywhere you can fish.",
      legend_note: "Save before fighting a one-time legendary — if it faints, it never returns!"
    },
    fa: {
      dex_t: "دکس مکان‌ها", sec_t: "نحوه‌ی به‌دست‌آوردن", close: "بستن", back: "◂ بازگشت",
      search_ph: "جست‌وجوی مکان…", no_results: "مکانی پیدا نشد.",
      count: "{a} مکان", all: "همه",
      regions: { j: "جوتو", k: "کانتو" },
      groups: { route: "مسیرها", city: "شهرها", cave: "غارها", forest: "جنگل‌ها", building: "ساختمان‌ها" },
      games: { gold: "طلایی", silver: "نقره‌ای", crystal: "کریستال" },
      times: { m: "صبح", d: "روز", n: "شب" },
      grass: "علفزار", surf: "سفر با سرف",
      rods: { o: "نیود قدیمی", g: "نیود معمولی", s: "سوپر راد" },
      hb: "کله‌زدن به درخت", rk: "شکستن سنگ", sw: "هجوم", ct: "مسابقه‌ی حشرات",
      rate_tpl: "نرخ مواجهه {r}/255 ≈ {p}٪ در هر قدم",
      bite_tpl: "شانس قلاب‌خوردن ≈ {p}٪",
      wild_t: "در طبیعت", special_t: "راه‌های ویژه", evo_t: "با تکامل",
      none_t: "در این نسخه نیست",
      none_note: "این پوکمون در نسخه‌ی {g} به‌تنهایی به دست نمی‌آید — در {list} زندگی می‌کند. با دوستتان تبادل کنید!",
      none_nowhere: "در هیچ‌کدام از سه نسخه مواجهه‌ی عادی ندارد — فقط ایونت/تبادل.",
      lvl: "سطح {n}", lvl_rng: "سطح {a}–{b}",
      common: "معمولی", rare: "نادر", pct_of: "{p}٪",
      menu_locations: "دکس مکان‌ها", all_locations: "همه‌ی مکان‌ها",
      kinds: { starter: "استارتر", egg: "تخم", gift: "هدیه", trade: "تبادل", corner: "گیم‌کرنر",
               static: "مواجهه‌ی ثابت", roamer: "سرگردان", event: "ایونت" },
      evo_start: "شروع از", evo_of: "تکامل از",
      conds: { level: "سطح {n}", trade: "تبادل", use_item: "استفاده از {i}", happiness: "خوشحالی{t}",
               happiness_day: " (روز)", happiness_night: " (شب)", beauty: "زیبایی {n}",
               shed: "یک جای خالی در گروه + پوک‌بال", special: "شرط ویژه" },
      items: { "fire-stone": "سنگ آتش", "water-stone": "سنگ آب", "thunder-stone": "سنگ رعد",
               "leaf-stone": "سنگ برگ", "moon-stone": "سنگ ماه", "sun-stone": "سنگ خورشید",
               "kings-rock": "سنگ پادشاه", "metal-coat": "پوشش فلزی", "dragon-scale": "پوسته‌ی اژدها",
               "up-grade": "ارتقاگر", "deep-sea-tooth": "دندان اعماق", "deep-sea-scale": "پوسته‌ی اعماق" },
      unown_note: "دیوارهای ویرانه‌های الف پر از آنان‌اون است — اینکه کدام حرف‌ها ظاهر شوند به تعداد معما‌هایی بستگی دارد که حل کرده‌اید.",
      contest_note: "مسابقه‌ی گرفتن حشرات (سه‌شنبه/پنج‌شنبه/شنبه): رایگان — ۲۰ توال پارک و ۲۰ دقیقه وقت دارید و فقط یک پوکمون نگه می‌دارید.",
      headbutt_note: "تکاندن درخت‌ها: درخت‌های معمولی جدول معمولی را می‌دهند؛ درخت‌های نادر ۸۰٪ مواقع جدول نادر را.",
      rock_note: "شکستن سنگ‌های ترک‌خورده می‌تواند شاکل هم پیدا کند (۱۰٪).",
      swarm_note: "هجوم تلفنی جدول‌های این مکان را برای یک روز عوض می‌کند — تماس مربی را جواب بدهید و برگردید.",
      fish_note: "هر بار قلاب انداختن اول شانس قلاب‌خوردن را می‌رولد و بعد یک خانه از جدول را انتخاب می‌کند.",
      surf_note: "سطوح سرف ۰ تا ۴ بیشتر از سطح نوشته‌شده می‌شوند.",
      friday_note: "فقط روزهای جمعه ظاهر می‌شود",
      roam_note: "هر نوبت فرار می‌کند — سریع ضعیفش کنید یا اول یک توال تند بیندازید",
      oldrod_note: "نیود قدیمی در هر آبی ماگیکارپ سطح ۱۰ می‌گیرد — هر جا که ماهیگیری بشود.",
      legend_note: "قبل از نبرد با هر هیولای یک‌بارمصرف ذخیره کنید — اگر قوی شود، دیگر برنمی‌گردد!"
    }
  };

  if (typeof LOC2 === "undefined") return { applyLang(){}, openDex(){}, closeDex(){}, syncGame(){} };

  /* ================= helpers ================= */
  const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const faD = n => String(n).replace(/[0-9]/g, d => "۰۱۲۳۴۵۶۷۸۹"[+d]).replace(/%/g, "٪");
  const lang = () => (typeof state !== "undefined" && state.lang) || "en";
  const num = n => lang() === "fa" ? faD(n) : String(n);
  const t = k => { const v = k.split(".").reduce((o, p) => o && o[p], LI[lang()]); return v === undefined ? (k.split(".").reduce((o, p) => o && o[p], LI.en) || k) : v; };
  const tpl = (s, o) => s.replace(/\{(\w+)\}/g, (_, k) => o[k] !== undefined ? num(o[k]) : "{" + k + "}");
  const GAMES = LOC2.games || ["gold", "silver", "crystal"];
  const GRASS_PCT = LOC2.grassPct || [30, 30, 20, 10, 5, 4, 1];
  const WATER_PCT = [60, 30, 10];
  const SPREAD = LOC2.waterSpread || 4;
  const gameOf = () => { try { return (GAMES.indexOf(state.theme) !== -1 ? state.theme : GAMES[0]); } catch (e) { return GAMES[0]; } };
  function pmap(id){ try { return PMAP[id]; } catch (e) { return null; } }
  function monName(id){
    const p = pmap(id);
    if (!p) return "#" + id;
    return lang() === "fa" && p.fa ? p.fa : p.display;
  }
  function sprImg(id, cls){
    let url = "";
    try { url = spriteURL(id); } catch (e) { url = ""; }
    if (!url) return '<span class="lc-sprph"></span>';
    return '<img class="' + cls + '" src="' + url + '" alt="" loading="lazy" onerror="this.style.display=\'none\'">';
  }
  const pctS = p => tpl(t("pct_of"), { p: (p >= 9.95 ? Math.round(p) : p.toFixed(1)).toString().replace(/\.0$/, "") });

  /* per-game table with the builder's fallback chain */
  function tblGame(loc, g){
    const tt = loc.t || {};
    if (g === "crystal"){
      if (tt.c !== undefined) return tt.c;
      return tt.s !== undefined ? tt.s : (tt.g || null);
    }
    if (g === "silver"){
      if (tt.s !== undefined) return tt.s;
      return tt.g || null;
    }
    return tt.g || null;
  }
  function tbTime(tb, k){ return tb ? (tb[k] || tb.m || null) : null; }

  /* tree sets: per-game rows with a gold fallback */
  function treePer(set, g){
    const sets = LOC2.trees[set] || {};
    if (sets[g]) return sets[g];
    for (const x of GAMES) if (sets[x]) return sets[x];
    return { c: [], r: [] };
  }

  /* ================= indexes ================= */
  /* WILD[g][species] = [{loc, m:{method:1}, lo, hi}] — one entry per
     (location, species) with the union of methods it appears through */
  const WILD = { gold: {}, silver: {}, crystal: {} };
  const LOCS = LOC2.locs;
  (function buildWild(){
    const push = (g, sp, loc, m, lo, hi) => {
      if (!sp) return;
      const arr = (WILD[g][sp] = WILD[g][sp] || []);
      let e = null;
      for (const x of arr) if (x.loc.id === loc.id){ e = x; break; }
      if (!e){ e = { loc, m: {}, lo: 999, hi: 0 }; arr.push(e); }
      e.m[m] = 1;
      e.lo = Math.min(e.lo, lo);
      e.hi = Math.max(e.hi, hi);
    };
    for (const loc of LOCS){
      for (const g of GAMES){
        const tb = tblGame(loc, g);
        if (!tb) continue;
        for (const k of ["m", "d", "n"]){
          const gt = tbTime(tb, k);
          if (gt && gt.s) gt.s.forEach(e => push(g, e[0], loc, "g", e[1], e[1]));
        }
        if (tb.swg) for (const k of ["m", "d", "n"]){
          const st = tbTime(tb.swg, k);
          if (st && st.s) st.s.forEach(e => push(g, e[0], loc, "sw", e[1], e[1]));
        }
        if (tb.w) tb.w.forEach(e => push(g, e[0], loc, "w", e[1], e[1] + SPREAD));
        for (const [mm, gi] of [["f", tb.f], ["sw", tb.swf]]){
          if (gi === undefined || gi === null) continue;
          const fg = LOC2.fish[gi];
          if (!fg) continue;
          for (const rod of ["o", "g", "s"]){
            (fg[rod] || []).forEach(r => {
              if (r.length === 5){
                push(g, r[0], loc, mm, r[1], r[1]);   // day variant
                push(g, r[2], loc, mm, r[3], r[3]);   // night variant
              } else {
                push(g, r[0], loc, mm, r[1], r[1]);
              }
            });
          }
        }
        for (const [mm, key] of [["hb", "hb"], ["rk", "rk"]]){
          if (!tb[key] || !LOC2.trees[tb[key]]) continue;
          const per = treePer(tb[key], g);
          (per.c || []).forEach(r => push(g, r[0], loc, mm, r[1], r[1]));
          (per.r || []).forEach(r => push(g, r[0], loc, mm, r[1], r[1]));
        }
        if (tb.ct && LOC2.contest) LOC2.contest.forEach(r => push(g, r[0], loc, "ct", r[1], r[2]));
      }
    }
  })();

  /* SP[id] = [specials], SPLOC[locId] = [specials] */
  const SP = {}, SPLOC = {};
  LOC2.sp.forEach(s => {
    (s.m || []).forEach(m => (SP[m[0]] = SP[m[0]] || []).push(s));
    if (s.loc) (SPLOC[s.loc] = SPLOC[s.loc] || []).push(s);
  });

  /* direct availability per game (wild + every non-event special) */
  const DIRECT = {};
  for (const g of GAMES){
    const set = new Set();
    Object.keys(WILD[g]).forEach(id => set.add(+id));
    LOC2.sp.forEach(s => { if (s.v.indexOf(g) !== -1 && s.k !== "event") (s.m || []).forEach(m => set.add(m[0])); });
    DIRECT[g] = set;
  }
  function evoEdges(){ try { return EVOLUTIONS.chains; } catch (e) { return {}; } }
  function preEvos(id){
    const out = [];
    for (const ch of Object.values(evoEdges()))
      for (const e of ch.edges) if (e.to === id && e.from <= 251 && e.to <= 251) out.push(e);
    return out;
  }
  function obtainable(g, id, seen){
    if (DIRECT[g].has(id)) return true;
    seen = seen || {};
    if (seen[id]) return false;
    seen[id] = 1;
    return preEvos(id).some(e => obtainable(g, e.from, seen));
  }
  function evoPath(g, id){
    if (DIRECT[g].has(id)) return null;
    for (const e of preEvos(id)){
      const p = evoPath(g, e.from);
      if (p !== null || DIRECT[g].has(e.from)){
        const base = p || [{ id: e.from }];
        return base.concat([{ id, cond: e.cond }]);
      }
    }
    return null;
  }
  function condText(c){
    if (!c) return t("conds.special");
    if (c.t === "level") return tpl(t("conds.level"), { n: c.lvl });
    if (c.t === "trade") return t("conds.trade");
    if (c.t === "use-item") return tpl(t("conds.use_item"), { i: t("items." + c.item) });
    if (c.t === "happiness") return tpl(t("conds.happiness"),
      { t: c.time === "day" ? t("conds.happiness_day") : c.time === "night" ? t("conds.happiness_night") : "" });
    if (c.t === "beauty") return tpl(t("conds.beauty"), { n: c.val });
    if (c.t === "shed") return t("conds.shed");
    return t("conds.special");
  }

  /* ================= detail-pane section ================= */
  let secGame = null;   /* null = follow the page theme */
  function methodLabel(m){
    if (m === "g") return t("grass");
    if (m === "w") return t("surf");
    if (m === "f") return t("rods.s");
    if (m === "sw") return t("sw");
    if (m === "hb") return t("hb");
    if (m === "rk") return t("rk");
    if (m === "ct") return t("ct");
    return m;
  }
  function sectionHTML(p){
    if (!secGame) secGame = gameOf();
    const g = secGame;
    const wild = (WILD[g][p.id] || []).slice().sort((a, b) => a.loc.o - b.loc.o);
    const spec = (SP[p.id] || []).filter(s => s.v.indexOf(g) !== -1);
    const path = evoPath(g, p.id);
    const chips = GAMES.map(x =>
      '<button class="lchip' + (g === x ? " on" : "") + '" data-lg="' + x + '">' + esc(t("games." + x)) + "</button>").join("");
    let h = '<div class="sec lc-sec" id="locSec">' +
      '<div class="sec-t"><span>' + esc(t("sec_t")) + '</span>' +
        '<button class="mv-all" data-locopen="dex">' + esc(t("all_locations")) + "</button></div>" +
      '<div class="lchips">' + chips + "</div>";

    if (wild.length){
      h += '<div class="lc-sub">' + esc(t("wild_t")) + "</div>";
      wild.forEach(w => {
        const badges = Object.keys(w.m).map(m =>
          '<span class="lcb lcb-' + m + '">' + esc(methodLabel(m)) + "</span>").join("");
        const lvl = w.lo === w.hi ? tpl(t("lvl"), { n: w.lo }) : tpl(t("lvl_rng"), { a: w.lo, b: w.hi });
        h += '<button class="lrow" data-loc="' + w.loc.id + '">' +
          '<span class="lrow-b">' + badges + "</span>" +
          '<span class="lrow-nm"><b>' + esc(w.loc[lang() === "fa" ? "fa" : "en"]) + "</b>" +
            "<i>" + esc(w.loc[lang() === "fa" ? "en" : "fa"]) + "</i></span>" +
          '<span class="lrow-lv">' + esc(lvl) + "</span>" +
          "</button>";
      });
    }

    if (spec.length){
      h += '<div class="lc-sub">' + esc(t("special_t")) + "</div>";
      spec.forEach(s => {
        const sl = s.loc ? LOCS.find(x => x.id === s.loc) : null;
        const locName = sl ? sl[lang() === "fa" ? "fa" : "en"] : "";
        h += '<div class="lrow flat sp">' +
          '<span class="lcb lcb-' + s.k + '">' + esc(t("kinds." + s.k)) + "</span>" +
          '<span class="lrow-det">' +
            (locName ? '<b class="lc-det-loc">' + esc(locName) + "</b> — " : "") +
            esc(s.d[lang() === "fa" ? "fa" : "en"]) +
          (s.loc ? ' <button class="lrow-go" data-loc="' + s.loc + '">▸</button>' : "") + "</span></div>";
      });
    }

    if (path){
      h += '<div class="lc-sub">' + esc(t("evo_t")) + '</div><div class="lc-evo">';
      path.forEach((step, i) => {
        if (i > 0) h += '<span class="lc-evo-c">▸ ' + esc(condText(step.cond)) + "</span>";
        h += '<button class="lc-evo-m' + (step.id === p.id ? " cur" : "") + '" data-id="' + step.id + '">' +
          sprImg(step.id, "lc-spr") + "<span>" + esc(monName(step.id)) + "</span></button>";
      });
      h += "</div>";
    }

    const obtainableWays = spec.filter(s => s.k !== "event");
    if (!wild.length && !obtainableWays.length && !path){
      const others = GAMES.filter(x => obtainable(x, p.id));
      h += '<div class="lc-none">' + esc(t("none_t")) + "</div>" +
        '<div class="mv-note">' + esc(others.length
          ? tpl(t("none_note"), { g: t("games." + g), list: others.map(x => t("games." + x)).join(lang() === "fa" ? "، " : " / ") })
          : t("none_nowhere")) + "</div>";
    }
    h += "</div>";
    return h;
  }
  function wire(p){
    const sec = document.getElementById("locSec");
    if (!sec) return;
    sec.querySelectorAll(".lchip").forEach(b => b.addEventListener("click", () => {
      secGame = b.dataset.lg; renderSection(p);
    }));
    const open = sec.querySelector("[data-locopen]");
    if (open) open.addEventListener("click", () => openDex());
    sec.querySelectorAll("[data-loc]").forEach(b => b.addEventListener("click", () => openDex(b.dataset.loc)));
    sec.querySelectorAll(".lc-evo-m").forEach(b => b.addEventListener("click", () => {
      try { select(parseInt(b.dataset.id, 10)); } catch (e) {}
    }));
  }
  function renderSection(p){
    const sec = document.getElementById("locSec");
    if (!sec) return;
    sec.outerHTML = sectionHTML(p);
    wire(p);
  }
  function syncGame(){ secGame = null; }

  /* ================= overlay ================= */
  const view = { loc: null, q: "", grp: null, reg: null, game: null, time: "m" };
  let el = null;
  function ensureOverlay(){
    if (el) return;
    const w = document.createElement("div");
    w.id = "locWrap"; w.className = "hidden";
    w.innerHTML =
      '<div id="locBox" role="dialog" aria-modal="true">' +
        '<div class="lc-head"><span id="lcHeadT"></span>' +
          '<button class="it-close" id="lcClose" title="Close">✕</button></div>' +
        '<div class="lc-viewbar" id="lcViewbar"></div>' +
        '<div class="lc-sub2" id="lcSub"></div>' +
        '<div class="lc-body" id="lcBody"></div>' +
      "</div>";
    document.body.appendChild(w);
    el = { wrap: w, head: w.querySelector("#lcHeadT"), viewbar: w.querySelector("#lcViewbar"),
           sub: w.querySelector("#lcSub"), body: w.querySelector("#lcBody") };
    w.addEventListener("click", e => { if (e.target === w) closeDex(); });
    w.querySelector("#lcClose").addEventListener("click", closeDex);
    document.addEventListener("keydown", e => {
      if (e.key === "Escape" && !w.classList.contains("hidden")){ e.stopPropagation(); closeDex(); }
      else if (!e.target.matches("input,select,textarea") && e.key.toLowerCase() === "l" &&
               w.classList.contains("hidden") && !menuOpenSafe()) openDex();
    }, true);
  }
  function menuOpenSafe(){ try { return typeof menuOpen === "function" ? menuOpen() : false; } catch (err) { return false; } }

  function openDex(locId){
    ensureOverlay();
    if (!view.game) view.game = gameOf();
    view.loc = locId || null;
    el.wrap.classList.remove("hidden");
    renderDex();
  }
  function closeDex(){ if (el) el.wrap.classList.add("hidden"); }

  /* ---------- list view ---------- */
  function renderDex(){
    if (!view.game) view.game = gameOf();
    el.head.textContent = t("dex_t") + " · " + t("games." + view.game);
    const groups = ["all"].concat(Object.keys(LI.en.groups));
    el.viewbar.innerHTML =
      '<button class="it-chip' + (!view.reg ? " on" : "") + '" data-r="">' + esc(t("all")) + "</button>" +
      ["j", "k"].map(r => '<button class="it-chip' + (view.reg === r ? " on" : "") + '" data-r="' + r + '">' +
        esc(t("regions." + r)) + "</button>").join("") +
      '<span class="lc-gap"></span>' +
      groups.map(c => '<button class="it-chip' + ((view.grp === c || (c === "all" && !view.grp)) ? " on" : "") +
        '" data-g="' + c + '">' + esc(c === "all" ? t("all") : t("groups." + c)) + "</button>").join("") +
      '<span class="lc-gap"></span>' +
      GAMES.map(g => '<button class="it-chip gchip' + (view.game === g ? " on" : "") + '" data-gm="' + g + '">' +
        esc(t("games." + g)) + "</button>").join("");
    el.viewbar.querySelectorAll(".it-chip[data-r]").forEach(b => b.addEventListener("click", () => {
      view.reg = b.dataset.r || null; renderDex();
    }));
    el.viewbar.querySelectorAll(".it-chip[data-g]").forEach(b => b.addEventListener("click", () => {
      view.grp = b.dataset.g === "all" ? null : b.dataset.g; renderDex();
    }));
    el.viewbar.querySelectorAll(".gchip").forEach(b => b.addEventListener("click", () => {
      view.game = b.dataset.gm; view.time = "m"; renderDex();
    }));
    if (view.loc){ renderLoc(view.loc); return; }
    el.sub.innerHTML = '<input id="lcQ" type="search" autocomplete="off" spellcheck="false" placeholder="' + esc(t("search_ph")) + '">';
    el.sub.querySelector("#lcQ").value = view.q;
    el.sub.querySelector("#lcQ").addEventListener("input", e => { view.q = e.target.value; renderList(); });
    renderList();
  }
  function locSpecies(loc, g){
    const tb = tblGame(loc, g);
    if (!tb) return [];
    const set = new Set();
    for (const k of ["m", "d", "n"]){
      const gt = tbTime(tb, k);
      if (gt && gt.s) gt.s.forEach(e => set.add(e[0]));
    }
    if (tb.w) tb.w.forEach(e => set.add(e[0]));
    for (const gi of [tb.f, tb.swf]){
      if (gi === undefined || gi === null) continue;
      const fg = LOC2.fish[gi];
      if (fg) for (const rod of ["o", "g", "s"]) (fg[rod] || []).forEach(r => { set.add(r[0]); if (r.length === 5) set.add(r[2]); });
    }
    for (const key of ["hb", "rk"]){
      if (tb[key] && LOC2.trees[tb[key]]){
        const per = treePer(tb[key], g);
        (per.c || []).forEach(r => set.add(r[0]));
        (per.r || []).forEach(r => set.add(r[0]));
      }
    }
    if (tb.ct && LOC2.contest) LOC2.contest.forEach(r => set.add(r[0]));
    return [...set];
  }
  function renderList(){
    const q = view.q.trim().toLowerCase();
    const arr = LOCS.filter(l => {
      if (view.reg && l.r !== view.reg) return false;
      if (view.grp && l.g !== view.grp) return false;
      if (q && (l.en + " " + l.fa).toLowerCase().indexOf(q) === -1) return false;
      return true;
    });
    el.body.innerHTML =
      '<div class="it-count">' + esc(tpl(t("count"), { a: arr.length })) + "</div>" +
      '<div class="lc-grid">' + arr.map(loc => {
        const sp = locSpecies(loc, view.game).length;
        const tb = tblGame(loc, view.game) || {};
        const meth = [];
        for (const k of ["m", "d", "n"]){
          const gt = tbTime(tb, k);
          if (gt && gt.s && gt.s.length && meth.indexOf("g") === -1) meth.push("g");
        }
        if (tb.w && tb.w.length) meth.push("w");
        if (tb.f !== undefined && tb.f !== null) meth.push("f");
        if (tb.hb) meth.push("hb");
        if (tb.rk) meth.push("rk");
        if (tb.ct) meth.push("ct");
        if (tb.swf !== undefined && tb.swf !== null || tb.swg) meth.push("sw");
        const mi = meth.map(m => '<i class="lc-mi lc-mi-' + m + '"></i>').join("");
        const hasSp = (SPLOC[loc.id] || []).some(s => s.v.indexOf(view.game) !== -1);
        return '<button class="lcard" data-loc="' + loc.id + '">' +
          '<span class="lcard-nm"><b>' + esc(loc[lang() === "fa" ? "fa" : "en"]) + "</b>" +
            "<i>" + esc(loc[lang() === "fa" ? "en" : "fa"]) + "</i></span>" +
          '<span class="lcard-meta">' + mi +
            '<b class="lc-n">' + num(sp) + "</b>" +
            (hasSp ? '<span class="lc-star">★</span>' : "") + "</span>" +
        "</button>";
      }).join("") + "</div>" +
      (arr.length ? "" : '<div class="it-note">' + esc(t("no_results")) + "</div>") +
      '<div class="it-note">' + esc(t("oldrod_note")) + "</div>";
    el.body.querySelectorAll(".lcard").forEach(c =>
      c.addEventListener("click", () => { view.loc = c.dataset.loc; renderDex(); }));
    const first = el.body.querySelector(".lcard");
    if (first) first.focus();
  }

  /* ---------- location view ---------- */
  function encRows(entries, pcts){
    const a = {};
    entries.forEach((e, i) => {
      const pc = pcts ? pcts[i] : (e[2] !== undefined ? 100 / entries.length : 100 / entries.length);
      const hi = e[2] !== undefined && e[2] > e[1] ? e[2] : e[1];
      const s = a[e[0]] = a[e[0]] || { pct: 0, lo: 999, hi: 0 };
      s.pct += pc; s.lo = Math.min(s.lo, e[1]); s.hi = Math.max(s.hi, hi);
    });
    return Object.keys(a).map(Number).sort((x, y) => a[y].pct - a[x].pct).map(id => {
      const s = a[id];
      const lvl = s.lo === s.hi ? tpl(t("lvl"), { n: s.lo }) : tpl(t("lvl_rng"), { a: s.lo, b: s.hi });
      return '<button class="lrow mon" data-id="' + id + '">' +
        sprImg(id, "lc-spr") +
        '<span class="lrow-nm"><b>' + esc(monName(id)) + "</b></span>" +
        '<span class="lrow-lv">' + esc(lvl) + "</span>" +
        '<span class="lrow-pc">' + esc(pctS(s.pct)) + "</span>" +
      "</button>";
    }).join("");
  }
  function rodRows(rows){
    return rows.map(r => {
      if (r.length === 5){
        const day = monName(r[0]) + " " + tpl(t("lvl"), { n: r[1] });
        const nite = monName(r[2]) + " " + tpl(t("lvl"), { n: r[3] });
        return '<div class="lrow flat"><span class="lrow-nm"><b>' + esc(day) + '</b> <i class="lc-tsep">·</i> <b>' + esc(nite) + "</b></span>" +
          '<span class="lrow-pc">' + esc(pctS(r[4])) + "</span></div>";
      }
      return '<div class="lrow flat"><span class="lrow-nm"><b>' + esc(monName(r[0])) + " " + esc(tpl(t("lvl"), { n: r[1] })) + "</b></span>" +
        '<span class="lrow-pc">' + esc(pctS(r[2])) + "</span></div>";
    }).join("");
  }
  function treeBlock(set, g){
    const per = treePer(set, g);
    let h = "";
    if (per.c && per.c.length)
      h += '<div class="lc-sub2b">' + esc(t("common")) + '</div><div class="lc-rows">' +
        encRows(per.c.map(r => [r[0], r[1]]), per.c.map(r => r[2])) + "</div>";
    if (per.r && per.r.length && JSON.stringify(per.r) !== JSON.stringify(per.c))
      h += '<div class="lc-sub2b">' + esc(t("rare")) + '</div><div class="lc-rows">' +
        encRows(per.r.map(r => [r[0], r[1]]), per.r.map(r => r[2])) + "</div>";
    return h;
  }
  function renderLoc(locId){
    const loc = LOCS.find(l => l.id === locId);
    if (!loc){ view.loc = null; renderDex(); return; }
    const g = view.game;
    const tb = tblGame(loc, g) || {};
    el.viewbar.innerHTML =
      '<button class="it-back" id="lcBack">' + esc(t("back")) + "</button>" +
      '<span class="lc-gap"></span>' +
      GAMES.map(x => '<button class="it-chip gchip' + (g === x ? " on" : "") + '" data-gm="' + x + '">' +
        esc(t("games." + x)) + "</button>").join("");
    el.viewbar.querySelector("#lcBack").addEventListener("click", () => { view.loc = null; renderDex(); });
    el.viewbar.querySelectorAll(".gchip").forEach(b => b.addEventListener("click", () => {
      view.game = b.dataset.gm; view.time = "m"; renderDex();
    }));
    let h = '<div class="lc-ltitle"><b>' + esc(loc[lang() === "fa" ? "fa" : "en"]) + "</b>" +
      "<i>" + esc(loc[lang() === "fa" ? "en" : "fa"]) + "</i>" +
      '<span class="lcb lc-reg">' + esc(t("regions." + loc.r)) + "</span></div>";

    /* grass with time-of-day tabs */
    const timeKeys = ["m", "d", "n"].filter(k => { const gt = tbTime(tb, k); return gt && gt.s && gt.s.length; });
    if (timeKeys.length){
      const tk = timeKeys.indexOf(view.time) !== -1 ? view.time : timeKeys[0];
      const gt = tbTime(tb, tk);
      h += '<div class="lc-sub">' + esc(t("grass")) +
        ' <i class="lc-rate">' + esc(tpl(t("rate_tpl"), { r: gt.r, p: Math.round(gt.r / 255 * 100) })) + "</i></div>";
      if (timeKeys.length > 1)
        h += '<div class="lc-times">' + timeKeys.map(k =>
          '<button class="it-chip tchip' + (k === tk ? " on" : "") + '" data-t="' + k + '">' +
          esc(t("times." + k)) + "</button>").join("") + "</div>";
      h += '<div class="lc-rows">' + encRows(gt.s, GRASS_PCT) + "</div>";
    }

    /* phone-call swarm grass replacement (Crystal) */
    if (tb.swg){
      const stKeys = ["m", "d", "n"].filter(k => { const st = tbTime(tb.swg, k); return st && st.s && st.s.length; });
      if (stKeys.length){
        const stk = stKeys.indexOf(view.time) !== -1 ? view.time : stKeys[0];
        const st = tbTime(tb.swg, stk);
        h += '<div class="lc-sub">' + esc(t("sw")) +
          ' <i class="lc-rate">' + esc(tpl(t("rate_tpl"), { r: st.r, p: Math.round(st.r / 255 * 100) })) + "</i></div>";
        if (stKeys.length > 1)
          h += '<div class="lc-times">' + stKeys.map(k =>
            '<button class="it-chip tchip sw' + (k === stk ? " on" : "") + '" data-t="' + k + '">' +
            esc(t("times." + k)) + "</button>").join("") + "</div>";
        h += '<div class="lc-rows">' + encRows(st.s, GRASS_PCT) + "</div>" +
          '<div class="mv-note">' + esc(t("swarm_note")) + "</div>";
      }
    }

    /* surf */
    if (tb.w && tb.w.length){
      h += '<div class="lc-sub">' + esc(t("surf")) + ' <i class="lc-rate">' +
        esc(tpl(t("rate_tpl"), { r: tb.wr, p: Math.round(tb.wr / 255 * 100) })) + "</i></div>" +
        '<div class="lc-rows">' + encRows(tb.w.map(e => [e[0], e[1], e[1] + SPREAD]), WATER_PCT) + "</div>" +
        '<div class="mv-note">' + esc(t("surf_note")) + "</div>";
    }

    /* fishing (normal + swarm fish group) */
    for (const [key, isSw] of [["f", false], ["swf", true]]){
      const gi = tb[key];
      if (gi === undefined || gi === null) continue;
      const fg = LOC2.fish[gi];
      if (!fg) continue;
      h += '<div class="lc-sub">' + (isSw ? esc(t("sw")) : "") + "</div>";
      for (const rod of ["o", "g", "s"]){
        if (!(fg[rod] || []).length) continue;
        h += '<div class="lc-sub2b">' + esc(t("rods." + rod)) +
          ' <i class="lc-rate">' + esc(tpl(t("bite_tpl"), { p: Math.round(fg.bite / 256 * 100) })) + "</i></div>" +
          '<div class="lc-rows">' + rodRows(fg[rod]) + "</div>";
      }
      h += '<div class="mv-note">' + esc(t("fish_note")) + "</div>";
      if (isSw) h += '<div class="mv-note">' + esc(t("swarm_note")) + "</div>";
    }

    /* headbutt / rock smash */
    if (tb.hb && LOC2.trees[tb.hb])
      h += '<div class="lc-sub">' + esc(t("hb")) + "</div>" + treeBlock(tb.hb, g) +
        '<div class="mv-note">' + esc(t("headbutt_note")) + "</div>";
    if (tb.rk && LOC2.trees[tb.rk])
      h += '<div class="lc-sub">' + esc(t("rk")) + "</div>" + treeBlock(tb.rk, g) +
        '<div class="mv-note">' + esc(t("rock_note")) + "</div>";

    /* bug-catching contest */
    if (tb.ct && LOC2.contest)
      h += '<div class="lc-sub">' + esc(t("ct")) + "</div>" +
        '<div class="lc-rows">' + encRows(LOC2.contest.map(r => [r[0], r[1], r[2]]), LOC2.contest.map(r => r[3])) + "</div>" +
        '<div class="mv-note">' + esc(t("contest_note")) + "</div>";

    /* specials at this location */
    const sps = (SPLOC[loc.id] || []).filter(s => s.v.indexOf(g) !== -1);
    if (sps.length){
      h += '<div class="lc-sub">' + esc(t("special_t")) + "</div>" + '<div class="lc-rows">';
      sps.forEach(s => {
        const mons = (s.m || []).map(m => m[0]).map(id =>
          '<button class="lc-spmon" data-id="' + id + '" title="' + esc(monName(id)) + '">' +
            sprImg(id, "lc-spr sm") + "<span>" + esc(monName(id)) + "</span></button>").join("");
        h += '<div class="lrow flat sp">' +
          '<span class="lrow-mons">' + mons + "</span>" +
          '<span class="lcb lcb-' + s.k + '">' + esc(t("kinds." + s.k)) + "</span>" +
          '<span class="lrow-det">' + esc(s.d[lang() === "fa" ? "fa" : "en"]) +
          (s.note === "friday" ? ' <i class="lc-note2">' + esc(t("friday_note")) + "</i>" : "") +
          (s.note === "roam" ? ' <i class="lc-note2">' + esc(t("roam_note")) + "</i>" : "") +
          "</span></div>";
      });
      h += "</div>";
      h += '<div class="mv-note">' + esc(t("legend_note")) + "</div>";
    }

    /* per-location notes */
    if (/RUINS_OF_ALPH/.test(loc.id) && locSpecies(loc, g).indexOf(201) !== -1)
      h += '<div class="mv-note">' + esc(t("unown_note")) + "</div>";

    el.sub.innerHTML = "";
    el.body.innerHTML = h;
    el.body.querySelectorAll(".tchip").forEach(b => b.addEventListener("click", () => {
      view.time = b.dataset.t; renderLoc(locId);
    }));
    el.body.querySelectorAll(".lrow.mon, .lc-spmon").forEach(r => r.addEventListener("click", () => {
      closeDex();
      try { select(parseInt(r.dataset.id, 10)); } catch (e) {}
    }));
  }

  /* ================= START menu + language ================= */
  function injectMenu(){
    const pop = document.getElementById("menuPop");
    if (!pop || pop.querySelector("[data-act=locdex]")) return;
    const ref = pop.querySelector("[data-act=itemsdex]") || pop.querySelector(".m-sep");
    const b = document.createElement("button");
    b.className = "m-item"; b.dataset.act = "locdex";
    b.innerHTML = '<span class="mi">&#128205;</span><span class="lc-menu-l" data-key="menu_locations"></span>';
    pop.insertBefore(b, ref ? ref.nextSibling : null);
    pop.addEventListener("click", e => {
      const it = e.target.closest(".m-item");
      if (it && it.dataset.act === "locdex") openDex();
    });
  }
  function applyLang(){
    document.querySelectorAll(".lc-menu-l").forEach(s => { s.textContent = t(s.dataset.key); });
    const c = document.getElementById("lcClose");
    if (c) c.title = t("close");
    if (el && !el.wrap.classList.contains("hidden")) renderDex();
  }
  injectMenu();
  ensureOverlay();

  return { openDex, closeDex, applyLang, sectionHTML, wire, renderSection, syncGame };
})();
