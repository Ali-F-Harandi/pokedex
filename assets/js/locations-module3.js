"use strict";
/* Pokédex Plus — LOCATION DEX module, GENERATION III (gen3.html).
   ============================================================
   Loaded AFTER locations-gen3.js (LOC3). Sister of gen1/gen2's
   location modules — same LocUI global and same API surface
   (openDex / closeDex / applyLang / sectionHTML / wire /
   renderSection / syncGame), rendered against Gen 3's encounter
   model:

     · per-game per-room tables: land (12 slots at the shared
       20/20/10/10/10/10/5/5/4/4/1/1 chances), surf + rock smash
       (5 slots at 60/30/5/4/1), fishing per map (old 70/30,
       good 60/20/20, super 40/40/15/4/1 — every cast rolls a
       50% bite chance first, wild_encounter.c `Random() & 1`)
     · levels roll min..max per slot (no Gen-2 +0..+4 spread)
     · NO time-of-day tabs — Gen 3 dropped day/night wilds
     · underwater surf tables (Underwater Routes 124/125/126)
     · Emerald TV mass outbreaks (swarms, 50% replacement)
     · specials: starters, egg, gifts, fossil, in-game trades,
       statics (authentic levels from the scripts), roaming
       Latis, ticket events
     · version locks straight from the paired headers: Groudon
       never shows on the Sapphire dex, R/S dedupe omits the
       Sapphire table when identical to Ruby

   Regions: ruby/sapphire/emerald -> LOC3.regions.hoenn (phase 5);
   FireRed/LeafGreen -> LOC3.regions.kanto (lands in phase 6 —
   while null, the section and the START-menu entry stay hidden).

   Everything user-visible is bilingual EN/FA (LI table below). */

const LocUI = (() => {

  /* ================= i18n ================= */
  const LI = {
    en: {
      dex_t: "LOCATION DEX", sec_t: "HOW TO CATCH", close: "Close", back: "◂ BACK",
      search_ph: "Search a location…", no_results: "No locations found.",
      count: "{a} locations", all: "ALL",
      regions: { h: "HOENN" },
      groups: { route: "Routes", city: "Cities & towns", cave: "Caves", forest: "Forests",
                water: "Underwater", safari: "Safari Zone", island: "Islands", building: "Buildings" },
      games: { ruby: "RUBY", sapphire: "SAPPHIRE", emerald: "EMERALD", firered: "FIRERED", leafgreen: "LEAFGREEN" },
      grass: "GRASS", surf: "SURF", uw: "UNDERWATER",
      rods: { o: "OLD ROD", g: "GOOD ROD", s: "SUPER ROD" },
      rk: "ROCK SMASH", sw: "SWARM",
      rate_tpl: "ENCOUNTER RATE {r}/255 ≈ {p}% per step",
      bite_tpl: "bite ≈ {p}% · then a rod table",
      wild_t: "IN THE WILD", special_t: "SPECIAL WAYS", evo_t: "BY EVOLUTION",
      none_t: "NOT IN THIS GAME",
      none_note: "This Pokémon cannot be obtained in {g} alone — it lives in {list}. Trade with a friend!",
      none_event: "No normal encounter in Hoenn — only the ticket events listed above.",
      none_nowhere: "Not obtainable in the Hoenn games — trade it in from another Generation III cartridge (FireRed · LeafGreen, or the GameCube games).",
      lvl: "Lv {n}", lvl_rng: "Lv {a}–{b}",
      common: "common", pct_of: "{p}%",
      menu_locations: "Location Dex", all_locations: "ALL LOCATIONS",
      kinds: { starter: "STARTER", egg: "EGG", gift: "GIFT", fossil: "FOSSIL", trade: "TRADE",
               static: "FIXED", roamer: "ROAMING", event: "EVENT" },
      evo_start: "start from", evo_of: "evolves from",
      conds: { level: "Lv {n}", trade: "Trade", use_item: "Use {i}", happiness: "Happy{t}",
               happiness_day: " (day)", happiness_night: " (night)", beauty: "Beauty {n}",
               shed: "empty party slot + Poké Ball", special: "Special" },
      items: { "fire-stone": "Fire Stone", "water-stone": "Water Stone", "thunder-stone": "Thunder Stone",
               "leaf-stone": "Leaf Stone", "moon-stone": "Moon Stone", "sun-stone": "Sun Stone",
               "kings-rock": "King's Rock", "metal-coat": "Metal Coat", "dragon-scale": "Dragon Scale",
               "up-grade": "Up-Grade", "deep-sea-tooth": "Deep Sea Tooth", "deep-sea-scale": "Deep Sea Scale" },
      trade_lvl_note: "joins at the traded-away Pokémon's level",
      swarm_note: "A TV mass outbreak replaces half of this map's grass encounters today (50% per encounter) — check the TV, then hurry: it lasts a day.",
      fish_note: "Every cast first rolls the 50% bite chance, then picks a slot from the rod's table.",
      oldrod_note: "The Old Rod hooks only MAGIKARP — but every fishable water has it.",
      legend_note: "Save before fighting a one-time legendary — if it faints, it never returns!",
      roam_note: "flees every turn — weaken it fast, or throw a fast Ball first",
      not_in_game: "This area does not exist in {g}.",
      no_wilds: "No wild encounters here."
    },
    fa: {
      dex_t: "دکس مکان‌ها", sec_t: "نحوه‌ی به‌دست‌آوردن", close: "بستن", back: "◂ بازگشت",
      search_ph: "جست‌وجوی مکان…", no_results: "مکانی پیدا نشد.",
      count: "{a} مکان", all: "همه",
      regions: { h: "هوئن" },
      groups: { route: "مسیرها", city: "شهرها", cave: "غارها", forest: "جنگل‌ها",
                water: "زیر آب", safari: "منطقه‌ی سافاری", island: "جزیره‌ها", building: "ساختمان‌ها" },
      games: { ruby: "یاقوت", sapphire: "یاقوت کبود", emerald: "زمرد", firered: "آتشین", leafgreen: "برگ سبز" },
      grass: "علفزار", surf: "سفر با سرف", uw: "زیر آب",
      rods: { o: "نیود قدیمی", g: "نیود معمولی", s: "سوپر راد" },
      rk: "شکستن سنگ", sw: "هجوم",
      rate_tpl: "نرخ مواجهه {r}/255 ≈ {p}٪ در هر قدم",
      bite_tpl: "قلاب ≈ {p}٪ · بعد جدول نیود",
      wild_t: "در طبیعت", special_t: "راه‌های ویژه", evo_t: "با تکامل",
      none_t: "در این نسخه نیست",
      none_note: "این پوکمون در نسخه‌ی {g} به‌تنهایی به دست نمی‌آید — در {list} زندگی می‌کند. با دوستتان تبادل کنید!",
      none_event: "در هوئن مواجهه‌ی عادی ندارد — فقط ایونت‌های بلیطی که بالا آمده.",
      none_nowhere: "در نسخه‌های هوئن به دست نمی‌آید — با تبادل از یک کارتریج دیگر نسل ۳ بیاورید (فایررد/لیف‌گرین کانتو یا بازی‌های گیم‌کیوب).",
      lvl: "سطح {n}", lvl_rng: "سطح {a}–{b}",
      common: "معمولی", pct_of: "{p}٪",
      menu_locations: "دکس مکان‌ها", all_locations: "همه‌ی مکان‌ها",
      kinds: { starter: "استارتر", egg: "تخم", gift: "هدیه", fossil: "فسیل", trade: "تبادل",
               static: "مواجهه‌ی ثابت", roamer: "سرگردان", event: "ایونت" },
      evo_start: "شروع از", evo_of: "تکامل از",
      conds: { level: "سطح {n}", trade: "تبادل", use_item: "استفاده از {i}", happiness: "خوشحالی{t}",
               happiness_day: " (روز)", happiness_night: " (شب)", beauty: "زیبایی {n}",
               shed: "یک جای خالی در گروه + پوک‌بال", special: "شرط ویژه" },
      items: { "fire-stone": "سنگ آتش", "water-stone": "سنگ آب", "thunder-stone": "سنگ رعد",
               "leaf-stone": "سنگ برگ", "moon-stone": "سنگ ماه", "sun-stone": "سنگ خورشید",
               "kings-rock": "سنگ پادشاه", "metal-coat": "پوشش فلزی", "dragon-scale": "پوسته‌ی اژدها",
               "up-grade": "ارتقاگر", "deep-sea-tooth": "دندان اعماق", "deep-sea-scale": "پوسته‌ی اعماق" },
      trade_lvl_note: "در سطح پوکمونی که می‌دهید می‌آید",
      swarm_note: "هجوم تلویزیونی امروز نیمی از مواجهه‌های علفزار این مکان را عوض می‌کند (۵۰٪ در هر مواجهه) — تلویزیون را ببینید و عجله کنید: یک روز بیشتر دوام ندارد.",
      fish_note: "هر بار قلاب انداختن اول شانس ۵۰٪ قلاب‌خوردن را می‌رولد و بعد یک خانه از جدول نیود را انتخاب می‌کند.",
      oldrod_note: "نیود قدیمی فقط ماگیکارپ می‌گیرد — ولی هر آبی که ماهیگیری شود آن را دارد.",
      legend_note: "قبل از نبرد با هر هیولای یک‌بارمصرف ذخیره کنید — اگر قوی شود، دیگر برنمی‌گردد!",
      roam_note: "هر نوبت فرار می‌کند — سریع ضعیفش کنید یا اول یک توال تند بیندازید",
      not_in_game: "این مکان در {g} وجود ندارد.",
      no_wilds: "مواجهه‌ی وحشی اینجا ندارد."
    }
  };

  if (typeof LOC3 === "undefined") return { applyLang(){}, openDex(){}, closeDex(){}, syncGame(){} };

  /* ================= helpers ================= */
  const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const faD = n => String(n).replace(/[0-9]/g, d => "۰۱۲۳۴۵۶۷۸۹"[+d]).replace(/%/g, "٪");
  const lang = () => (typeof state !== "undefined" && state.lang) || "en";
  const num = n => lang() === "fa" ? faD(n) : String(n);
  const t = k => { const v = k.split(".").reduce((o, p) => o && o[p], LI[lang()]); return v === undefined ? (k.split(".").reduce((o, p) => o && o[p], LI.en) || k) : v; };
  const tpl = (s, o) => s.replace(/\{(\w+)\}/g, (_, k) => o[k] !== undefined ? num(o[k]) : "{" + k + "}");
  const GAMES = LOC3.games;
  const GRASS_PCT = LOC3.landPct;
  const WATER_PCT = LOC3.waterPct;
  const FISH_PCT = LOC3.fishPct;
  const REGIONS = Object.keys(LOC3.regions).filter(r => LOC3.regions[r]);
  const regionOf = g => {
    for (const r of REGIONS) if (LOC3.regions[r].games.indexOf(g) !== -1) return r;
    return null;
  };
  /* null while the active game's region has no data (FRLG until phase 6) —
     sections stay hidden instead of showing another region's tables */
  const gameOf = () => { try { return regionOf(state.theme) ? state.theme : null; } catch (e) { return null; } };
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

  /* ================= indexes ================= */
  /* per-region data + per-game WILD index: WILD[g][species] =
     [{loc, m:{method:1}, lo, hi}] */
  const DATA = {}, WILD = {};
  for (const r of REGIONS) {
    DATA[r] = LOC3.regions[r];
    for (const g of DATA[r].games) WILD[g] = {};
  }
  function tblGame(loc, g){
    const tt = loc.t || {};
    if (tt[g] !== undefined) return tt[g];
    if (g === "sapphire" && tt.ruby !== undefined) return tt.ruby;   // deduped R/S
    if (g === "leafgreen" && tt.firered !== undefined) return tt.firered;
    return null;
  }
  (function buildWild(){
    const push = (g, sp, loc, m, lo, hi) => {
      if (!sp || !WILD[g]) return;
      const arr = (WILD[g][sp] = WILD[g][sp] || []);
      let e = null;
      for (const x of arr) if (x.loc.id === loc.id){ e = x; break; }
      if (!e){ e = { loc, m: {}, lo: 999, hi: 0 }; arr.push(e); }
      e.m[m] = 1;
      e.lo = Math.min(e.lo, lo);
      e.hi = Math.max(e.hi, hi);
    };
    for (const r of REGIONS){
      const fish = DATA[r].fish;
      for (const loc of DATA[r].locs){
        for (const g of DATA[r].games){
          const rooms = tblGame(loc, g);
          if (!rooms) continue;
          for (const rm of rooms){
            if (rm.land && rm.land.s) rm.land.s.forEach(e => push(g, e[0], loc, "g", e[1], e[2]));
            if (rm.surf && rm.surf.w){
              const m = loc.g === "water" ? "uw" : "w";
              rm.surf.w.forEach(e => push(g, e[0], loc, m, e[1], e[2]));
            }
            if (rm.rk && rm.rk.s2) rm.rk.s2.forEach(e => push(g, e[0], loc, "rk", e[1], e[2]));
            if (rm.f !== undefined && rm.f !== null && fish[rm.f])
              for (const rod of ["o", "g", "s"]) (fish[rm.f][rod] || []).forEach(e => push(g, e[0], loc, "f", e[1], e[2]));
          }
        }
        for (const swm of (DATA[r].swarms || [])){
          for (const g of swm.v) push(g, swm.id, locById(r, swm.loc) || { id: swm.loc }, "sw", swm.lvl, swm.lvl);
        }
      }
    }
  })();
  function locById(r, id){ return DATA[r].locs.find(l => l.id === id) || null; }

  /* SP[id] = [specials] (per region), SPLOC[region:locId] = [specials] */
  const SP = {}, SPLOC = {};
  for (const r of REGIONS){
    SP[r] = {}; SPLOC[r] = {};
    DATA[r].sp.forEach(s => {
      (s.m || []).forEach(m => (SP[r][m[0]] = SP[r][m[0]] || []).push(s));
      if (s.loc) (SPLOC[r][s.loc] = SPLOC[r][s.loc] || []).push(s);
    });
  }

  /* direct availability per game (wild + every non-event special) */
  const DIRECT = {};
  for (const r of REGIONS){
    for (const g of DATA[r].games){
      const set = new Set();
      Object.keys(WILD[g] || {}).forEach(id => set.add(+id));
      DATA[r].sp.forEach(s => { if (s.v.indexOf(g) !== -1 && s.k !== "event") (s.m || []).forEach(m => set.add(m[0])); });
      DIRECT[g] = set;
    }
  }
  function evoEdges(){ try { return EVOLUTIONS.chains; } catch (e) { return {}; } }
  function preEvos(id){
    const out = [];
    for (const ch of Object.values(evoEdges()))
      for (const e of ch.edges) if (e.to === id && e.from <= 386 && e.to <= 386) out.push(e);
    return out;
  }
  function obtainable(g, id, seen){
    if (!WILD[g] || !DIRECT[g]) return false;
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
    if (m === "uw") return t("uw");
    if (m === "f") return t("rods.s");
    if (m === "sw") return t("sw");
    if (m === "rk") return t("rk");
    return m;
  }
  function sectionHTML(p){
    const reg = regionOf(gameOf());
    if (!reg) return "";
    if (!secGame || regionOf(secGame) !== reg) secGame = gameOf();
    const g = secGame;
    const wild = (WILD[g][p.id] || []).slice().sort((a, b) => a.loc.o - b.loc.o);
    const spec = (SP[reg][p.id] || []).filter(s => s.v.indexOf(g) !== -1);
    const path = evoPath(g, p.id);
    const chips = DATA[reg].games.map(x =>
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
        const r = regionOf(gameOf());
        const sl = s.loc ? locById(r, s.loc) : null;
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
      const others = DATA[reg].games.filter(x => x !== g && obtainable(x, p.id));
      const onlyEvents = spec.length > 0;
      h += '<div class="lc-none">' + esc(t("none_t")) + "</div>" +
        '<div class="mv-note">' + esc(others.length
          ? tpl(t("none_note"), { g: t("games." + g), list: others.map(x => t("games." + x)).join(lang() === "fa" ? "، " : " / ") })
          : onlyEvents ? t("none_event") : t("none_nowhere")) + "</div>";
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
  function syncGame(){ secGame = null; updateMenuItem(); }

  /* ================= overlay ================= */
  const view = { loc: null, q: "", grp: null, reg: null, game: null };
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
    const reg = regionOf(gameOf());
    if (!reg) return;                       /* no region data for this game (yet) */
    ensureOverlay();
    if (!view.game || regionOf(view.game) !== reg) view.game = gameOf();
    view.loc = locId || null;
    el.wrap.classList.remove("hidden");
    renderDex();
  }
  function closeDex(){ if (el) el.wrap.classList.add("hidden"); }

  /* ---------- list view ---------- */
  function renderDex(){
    if (!view.game) view.game = gameOf();
    const reg = regionOf(view.game);
    el.head.textContent = t("dex_t") + " · " + t("games." + view.game);
    const groups = ["all"].concat(Object.keys(LI.en.groups));
    const regionChips = REGIONS.length > 1
      ? REGIONS.map(r => '<button class="it-chip' + ((view.reg || reg) === r ? " on" : "") + '" data-reg="' + r + '">' +
          esc(t("regions." + r)) + "</button>").join("") + '<span class="lc-gap"></span>'
      : "";
    el.viewbar.innerHTML =
      regionChips +
      groups.map(c => '<button class="it-chip' + ((view.grp === c || (c === "all" && !view.grp)) ? " on" : "") +
        '" data-g="' + c + '">' + esc(c === "all" ? t("all") : t("groups." + c)) + "</button>").join("") +
      '<span class="lc-gap"></span>' +
      DATA[reg].games.map(g => '<button class="it-chip gchip' + (view.game === g ? " on" : "") + '" data-gm="' + g + '">' +
        esc(t("games." + g)) + "</button>").join("");
    el.viewbar.querySelectorAll(".it-chip[data-g]").forEach(b => b.addEventListener("click", () => {
      view.grp = b.dataset.g === "all" ? null : b.dataset.g; renderDex();
    }));
    el.viewbar.querySelectorAll(".gchip").forEach(b => b.addEventListener("click", () => {
      view.game = b.dataset.gm; renderDex();
    }));
    el.viewbar.querySelectorAll(".it-chip[data-reg]").forEach(b => b.addEventListener("click", () => {
      const r = b.dataset.reg;
      view.reg = r; view.game = LOC3.regions[r].games[0]; view.loc = null; renderDex();
    }));
    if (view.loc){ renderLoc(view.loc); return; }
    el.sub.innerHTML = '<input id="lcQ" type="search" autocomplete="off" spellcheck="false" placeholder="' + esc(t("search_ph")) + '">';
    el.sub.querySelector("#lcQ").value = view.q;
    el.sub.querySelector("#lcQ").addEventListener("input", e => { view.q = e.target.value; renderList(); });
    renderList();
  }
  function locSpecies(loc, g, reg){
    const rooms = tblGame(loc, g);
    if (!rooms) return [];
    const fish = DATA[reg].fish;
    const set = new Set();
    for (const rm of rooms){
      if (rm.land && rm.land.s) rm.land.s.forEach(e => set.add(e[0]));
      if (rm.surf && rm.surf.w) rm.surf.w.forEach(e => set.add(e[0]));
      if (rm.rk && rm.rk.s2) rm.rk.s2.forEach(e => set.add(e[0]));
      if (rm.f !== undefined && rm.f !== null && fish[rm.f])
        for (const rod of ["o", "g", "s"]) (fish[rm.f][rod] || []).forEach(e => set.add(e[0]));
    }
    for (const swm of (DATA[reg].swarms || []))
      if (swm.loc === loc.id && swm.v.indexOf(g) !== -1) set.add(swm.id);
    return [...set];
  }
  function locMethods(loc, g, reg){
    const rooms = tblGame(loc, g);
    if (!rooms) return [];
    const meth = [];
    const add = m => { if (meth.indexOf(m) === -1) meth.push(m); };
    for (const rm of rooms){
      if (rm.land && rm.land.s && rm.land.s.length) add("g");
      if (rm.surf && rm.surf.w && rm.surf.w.length) add(loc.g === "water" ? "uw" : "w");
      if (rm.rk && rm.rk.s2 && rm.rk.s2.length) add("rk");
      if (rm.f !== undefined && rm.f !== null) add("f");
    }
    for (const swm of (DATA[reg].swarms || []))
      if (swm.loc === loc.id && swm.v.indexOf(g) !== -1) add("sw");
    return meth;
  }
  function renderList(){
    const reg = regionOf(view.game);
    const q = view.q.trim().toLowerCase();
    const arr = DATA[reg].locs.filter(l => {
      if (view.grp && l.g !== view.grp) return false;
      if (q && (l.en + " " + l.fa).toLowerCase().indexOf(q) === -1) return false;
      return true;
    });
    el.body.innerHTML =
      '<div class="it-count">' + esc(tpl(t("count"), { a: arr.length })) + "</div>" +
      '<div class="lc-grid">' + arr.map(loc => {
        const sp = locSpecies(loc, view.game, reg).length;
        const meth = locMethods(loc, view.game, reg);
        const mi = meth.map(m => '<i class="lc-mi lc-mi-' + m + '"></i>').join("");
        const hasSp = (SPLOC[reg][loc.id] || []).some(s => s.v.indexOf(view.game) !== -1);
        const exists = loc.ex && loc.ex[view.game] === false;
        return '<button class="lcard" data-loc="' + loc.id + '">' +
          '<span class="lcard-nm"><b>' + esc(loc[lang() === "fa" ? "fa" : "en"]) + "</b>" +
            "<i>" + esc(loc[lang() === "fa" ? "en" : "fa"]) + "</i></span>" +
          '<span class="lcard-meta">' + mi +
            '<b class="lc-n">' + num(sp) + "</b>" +
            (hasSp ? '<span class="lc-star">★</span>' : "") + "</span>" +
          (exists ? '<span class="lc-absent">' + esc(tpl(t("not_in_game"), { g: t("games." + view.game) })) + "</span>" : "") +
        "</button>";
      }).join("") + "</div>" +
      (arr.length ? "" : '<div class="it-note">' + esc(t("no_results")) + "</div>") +
      '<div class="it-note">' + esc(t("oldrod_note")) + "</div>";
    el.body.querySelectorAll(".lcard").forEach(c =>
      c.addEventListener("click", () => { view.loc = c.dataset.loc; renderDex(); }));
    const first = el.body.querySelector(".lcard");
    if (first) first.focus();
  }

  /* ---------- encounter rows ---------- */
  function encRows(entries, pcts){
    const a = {};
    entries.forEach((e, i) => {
      const pc = pcts ? pcts[i] : 100 / entries.length;
      const s = a[e[0]] = a[e[0]] || { pct: 0, lo: 999, hi: 0 };
      s.pct += pc; s.lo = Math.min(s.lo, e[1]); s.hi = Math.max(s.hi, e[2]);
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
  function fishRows(rows, pcts){
    const a = {};
    rows.forEach((e, i) => {
      const s = a[e[0]] = a[e[0]] || { pct: 0, lo: 999, hi: 0 };
      s.pct += pcts[i]; s.lo = Math.min(s.lo, e[1]); s.hi = Math.max(s.hi, e[2]);
    });
    return Object.keys(a).map(Number).sort((x, y) => a[y].pct - a[x].pct).map(id => {
      const s = a[id];
      const lvl = s.lo === s.hi ? tpl(t("lvl"), { n: s.lo }) : tpl(t("lvl_rng"), { a: s.lo, b: s.hi });
      return '<div class="lrow flat"><span class="lrow-mons"></span>' +
        '<span class="lrow-nm"><b>' + esc(monName(id)) + "</b></span>" +
        '<span class="lrow-lv">' + esc(lvl) + "</span>" +
        '<span class="lrow-pc">' + esc(pctS(s.pct)) + "</span>" +
      "</div>";
    }).join("");
  }

  /* ---------- location view ---------- */
  function renderLoc(locId){
    const reg = regionOf(view.game);
    const loc = locById(reg, locId);
    if (!loc){ view.loc = null; renderDex(); return; }
    const g = view.game;
    const rooms = tblGame(loc, g);
    const fish = DATA[reg].fish;
    el.viewbar.innerHTML =
      '<button class="it-back" id="lcBack">' + esc(t("back")) + "</button>" +
      '<span class="lc-gap"></span>' +
      DATA[reg].games.map(x => '<button class="it-chip gchip' + (g === x ? " on" : "") + '" data-gm="' + x + '">' +
        esc(t("games." + x)) + "</button>").join("");
    el.viewbar.querySelector("#lcBack").addEventListener("click", () => { view.loc = null; renderDex(); });
    el.viewbar.querySelectorAll(".gchip").forEach(b => b.addEventListener("click", () => {
      view.game = b.dataset.gm; renderDex();
    }));
    let h = '<div class="lc-ltitle"><b>' + esc(loc[lang() === "fa" ? "fa" : "en"]) + "</b>" +
      "<i>" + esc(loc[lang() === "fa" ? "en" : "fa"]) + "</i>" +
      '<span class="lcb lc-reg">' + esc(t("groups." + loc.g)) + "</span></div>";

    if (loc.ex && loc.ex[g] === false){
      h += '<div class="mv-note">' + esc(tpl(t("not_in_game"), { g: t("games." + g) })) + "</div>";
    } else if (!rooms){
      h += '<div class="mv-note">' + esc(t("no_wilds")) + "</div>";
    } else {
      /* room blocks: land / surf / rock smash / fishing — no time tabs in Gen 3 */
      for (const rm of rooms){
        const rl = rm.rm ? (lang() === "fa" ? rm.rmf : rm.rm) : "";
        if (rl) h += '<div class="lc-sub2b">' + esc(rl) + "</div>";
        if (rm.land && rm.land.s && rm.land.s.length){
          h += '<div class="lc-sub">' + esc(t("grass")) +
            ' <i class="lc-rate">' + esc(tpl(t("rate_tpl"), { r: rm.land.r, p: Math.round(rm.land.r / 255 * 100) })) + "</i></div>" +
            '<div class="lc-rows">' + encRows(rm.land.s, GRASS_PCT) + "</div>";
        }
        if (rm.surf && rm.surf.w && rm.surf.w.length){
          const lbl = loc.g === "water" ? t("uw") : t("surf");
          h += '<div class="lc-sub">' + esc(lbl) +
            ' <i class="lc-rate">' + esc(tpl(t("rate_tpl"), { r: rm.surf.r, p: Math.round(rm.surf.r / 255 * 100) })) + "</i></div>" +
            '<div class="lc-rows">' + encRows(rm.surf.w, WATER_PCT) + "</div>";
        }
        if (rm.rk && rm.rk.s2 && rm.rk.s2.length){
          h += '<div class="lc-sub">' + esc(t("rk")) +
            ' <i class="lc-rate">' + esc(tpl(t("rate_tpl"), { r: rm.rk.r, p: Math.round(rm.rk.r / 255 * 100) })) + "</i></div>" +
            '<div class="lc-rows">' + encRows(rm.rk.s2, WATER_PCT) + "</div>";
        }
        if (rm.f !== undefined && rm.f !== null && fish[rm.f]){
          h += '<div class="lc-sub"></div>';
          for (const rod of ["o", "g", "s"]){
            if (!(fish[rm.f][rod] || []).length) continue;
            h += '<div class="lc-sub2b">' + esc(t("rods." + rod)) +
              ' <i class="lc-rate">' + esc(tpl(t("bite_tpl"), { p: LOC3.bite })) + "</i></div>" +
              '<div class="lc-rows">' + fishRows(fish[rm.f][rod], FISH_PCT[rod]) + "</div>";
          }
          h += '<div class="mv-note">' + esc(t("fish_note")) + "</div>";
        }
      }
    }

    /* Emerald TV mass outbreak */
    const swarms = (DATA[reg].swarms || []).filter(s => s.loc === locId && s.v.indexOf(g) !== -1);
    if (swarms.length){
      h += '<div class="lc-sub">' + esc(t("sw")) + "</div>" + '<div class="lc-rows">';
      swarms.forEach(s => {
        h += '<div class="lrow flat sp">' +
          '<span class="lrow-mons">' +
            '<span class="lc-spmon">' + sprImg(s.id, "lc-spr sm") + "<span>" + esc(monName(s.id)) + "</span></span></span>" +
          '<span class="lcb lcb-sw">' + esc(t("sw")) + "</span>" +
          '<span class="lrow-det">' + esc(tpl(t("lvl"), { n: s.lvl })) + "</span></div>";
      });
      h += "</div>" + '<div class="mv-note">' + esc(t("swarm_note")) + "</div>";
    }

    /* specials at this location */
    const sps = (SPLOC[reg][locId] || []).filter(s => s.v.indexOf(g) !== -1);
    if (sps.length){
      h += '<div class="lc-sub">' + esc(t("special_t")) + "</div>" + '<div class="lc-rows">';
      sps.forEach(s => {
        const mons = (s.m || []).map(m => m[0]).map(id =>
          '<button class="lc-spmon" data-id="' + id + '" title="' + esc(monName(id)) + '">' +
            sprImg(id, "lc-spr sm") + "<span>" + esc(monName(id)) + "</span></button>").join("");
        const isTrade = s.k === "trade";
        h += '<div class="lrow flat sp">' +
          '<span class="lrow-mons">' + mons + "</span>" +
          '<span class="lcb lcb-' + s.k + '">' + esc(t("kinds." + s.k)) + "</span>" +
          '<span class="lrow-det">' + esc(s.d[lang() === "fa" ? "fa" : "en"]) +
          (isTrade ? ' <i class="lc-note2">' + esc(t("trade_lvl_note")) + "</i>" : "") +
          (s.note === "roam" ? ' <i class="lc-note2">' + esc(t("roam_note")) + "</i>" : "") +
          "</span></div>";
      });
      h += "</div>";
      h += '<div class="mv-note">' + esc(t("legend_note")) + "</div>";
    }

    /* per-location notes (Feebas, Altering Cave, Shoal Cave tides) */
    if (loc.note) h += '<div class="mv-note">' + esc(loc.note[lang() === "fa" ? "fa" : "en"]) + "</div>";

    el.sub.innerHTML = "";
    el.body.innerHTML = h;
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
  function updateMenuItem(){
    const b = document.querySelector('#menuPop [data-act=locdex]');
    if (!b) return;
    const has = !!regionOf(gameOf());
    b.style.display = has ? "" : "none";
  }
  function applyLang(){
    document.querySelectorAll(".lc-menu-l").forEach(s => { s.textContent = t(s.dataset.key); });
    updateMenuItem();
    const c = document.getElementById("lcClose");
    if (c) c.title = t("close");
    if (el && !el.wrap.classList.contains("hidden")) renderDex();
  }
  injectMenu();
  ensureOverlay();
  updateMenuItem();

  return { openDex, closeDex, applyLang, sectionHTML, wire, renderSection, syncGame };
})();
