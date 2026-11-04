"use strict";
/* Pokédex Plus — LOCATION DEX module (Phase 4, Gen 1)
   ============================================================
   Loaded AFTER locations-gen1.js (LOC1) on gen1.html. Adds:
     · a HOW-TO-CATCH section to every Pokémon's detail page —
       wild encounters (grass / surf / Super Rod) with the authentic
       slot chances, every special way (starters, gifts, in-game
       trades, Game Corner, fossils, fixed encounters) and, when a
       Pokémon only comes by evolving, the full evolve path
     · the LOCATION DEX overlay (L key / START menu): every Kanto
       location with its per-game encounter tables — click a Pokémon
       to jump to its dex page, click a location anywhere to open it

   Data authenticity: all tables come from the pret decompiles via
   tools/build-locations.py; GREEN follows the international Blue
   distribution (Bulbapedia-documented); Yellow's Raichu quirk
   (starter Pikachu refuses the Thunder Stone) is honoured. */

const LocUI = (() => {

  /* ================= i18n ================= */
  const LI = {
    en: {
      dex_t: "LOCATION DEX", sec_t: "HOW TO CATCH", close: "Close", back: "◂ BACK",
      search_ph: "Search a location…", no_results: "No locations found.",
      count: "{a} locations", all: "ALL",
      groups: { route: "Routes", city: "Cities & towns", cave: "Caves", forest: "Forests", building: "Buildings" },
      games: { red: "RED", blue: "BLUE", green: "GREEN", yellow: "YELLOW" },
      grass: "GRASS", surf: "SURF", rod: "SUPER ROD", rate_tpl: "ENCOUNTER RATE {r}/255 ≈ {p}% per step",
      wild_t: "IN THE WILD", special_t: "SPECIAL WAYS", evo_t: "BY EVOLUTION", none_t: "NOT IN THIS GAME",
      none_note: "This Pokémon cannot be obtained in {g} alone — it lives in {list}. Trade with a friend!",
      none_nowhere: "No normal encounter exists in any of the four games — event/glitch only.",
      lvl: "Lv {n}", lvl_rng: "Lv {a}–{b}", any_water: "anywhere you can fish",
      old_rod: "OLD ROD", good_rod: "GOOD ROD",
      oldrod_note: "always hooks Magikarp Lv 5 — anywhere you can fish",
      goodrod_note: "Goldeen Lv 10 / Poliwag Lv 10 · 50/50 — anywhere you can fish",
      green_note: "Green (Japan) shares its wild Pokémon distribution with the international Blue — its tables are shown.",
      safari_note: "Safari Zone: pay ¥500, get 500 steps — Pokémon may run away before you catch them.",
      menu_locations: "Location Dex", all_locations: "ALL LOCATIONS",
      kinds: { starter: "STARTER", gift: "GIFT", trade: "TRADE", corner: "GAME CORNER",
               fossil: "FOSSIL", static: "FIXED", event: "EVENT", evoblock: "NOTE" },
      evo_start: "start from", evo_of: "evolves from",
      conds: { level: "Lv {n}", trade: "Trade", use_item: "Use {i}", special: "Special" },
      items: { "leaf-stone": "Leaf Stone", "fire-stone": "Fire Stone", "water-stone": "Water Stone",
               "thunder-stone": "Thunder Stone", "moon-stone": "Moon Stone" },
      rate_short: "rate {r}", pct_of: "{p}%"
    },
    fa: {
      dex_t: "دکس مکان‌ها", sec_t: "نحوه‌ی به‌دست‌آوردن", close: "بستن", back: "◂ بازگشت",
      search_ph: "جست‌وجوی مکان…", no_results: "مکانی پیدا نشد.",
      count: "{a} مکان", all: "همه",
      groups: { route: "مسیرها", city: "شهرها", cave: "غارها", forest: "جنگل‌ها", building: "ساختمان‌ها" },
      games: { red: "قرمز", blue: "آبی", green: "سبز", yellow: "زرد" },
      grass: "علفزار", surf: "سفر با سرف", rod: "سوپر راد", rate_tpl: "نرخ مواجهه {r}/255 ≈ {p}٪ در هر قدم",
      wild_t: "در طبیعت", special_t: "راه‌های ویژه", evo_t: "با تکامل", none_t: "در این نسخه نیست",
      none_note: "این پوکمون در نسخه‌ی {g} به‌تنهایی به دست نمی‌آید — در {list} زندگی می‌کند. با دوستتان تبادل کنید!",
      none_nowhere: "در هیچ‌کدام از چهار نسخه مواجهه‌ی عادی ندارد — فقط ایونت/گلیچ.",
      lvl: "سطح {n}", lvl_rng: "سطح {a}–{b}", any_water: "هر جایی که بشود ماهیگیری کرد",
      old_rod: "نیود قدیمی", good_rod: "نیود معمولی",
      oldrod_note: "همیشه ماگیکارپ سطح ۵ می‌گیرد — هر جایی که بشود ماهیگیری کرد",
      goodrod_note: "گولدین سطح ۱۰ / پلی‌واگ سطح ۱۰ · ۵۰-۵۰ — هر جایی که بشود ماهیگیری کرد",
      green_note: "نسخه‌ی سبز (ژاپن) توزیع پوکمون‌های وحشی‌اش را با آبیِ جهانی شریک است — جدول‌های آبی نمایش داده می‌شود.",
      safari_note: "منطقه‌ی سافاری: ۵۰۰ ین بدهید و ۵۰۰ قدم فرصت دارید — پوکمون‌ها ممکن است قبل از گرفتن فرار کنند.",
      menu_locations: "دکس مکان‌ها", all_locations: "همه‌ی مکان‌ها",
      kinds: { starter: "استارتر", gift: "هدیه", trade: "تبادل", corner: "گیم‌کرنر",
               fossil: "فسیل", static: "مواجهه‌ی ثابت", event: "ایونت", evoblock: "نکته" },
      evo_start: "شروع از", evo_of: "تکامل از",
      conds: { level: "سطح {n}", trade: "تبادل", use_item: "استفاده از {i}", special: "شرط ویژه" },
      items: { "leaf-stone": "سنگ برگ", "fire-stone": "سنگ آتش", "water-stone": "سنگ آب",
               "thunder-stone": "سنگ رعد", "moon-stone": "سنگ ماه" },
      rate_short: "نرخ {r}", pct_of: "{p}٪"
    }
  };

  if (typeof LOC1 === "undefined") return { applyLang(){} };

  /* ================= helpers ================= */
  const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const faD = n => String(n).replace(/[0-9]/g, d => "۰۱۲۳۴۵۶۷۸۹"[+d]).replace(/%/g,"٪");
  const lang = () => (typeof state !== "undefined" && state.lang) || "en";
  const num = n => lang() === "fa" ? faD(n) : String(n);
  const t = k => { const v = k.split(".").reduce((o,p)=>o&&o[p], LI[lang()]); return v === undefined ? k.split(".").reduce((o,p)=>o&&o[p], LI.en) || k : v; };
  const tpl = (s,o) => s.replace(/\{(\w+)\}/g, (_,k)=> o[k] !== undefined ? num(o[k]) : "{"+k+"}");
  const GAMES = ["red","blue","green","yellow"];
  const gameOf = () => { try { return state.theme || "red"; } catch(e){ return "red"; } };
  function tbl(loc, g){ return g === "green" ? loc.t.blue : loc.t[g]; }
  function pmap(id){ try { return PMAP[id]; } catch(e){ return null; } }
  function monName(id){
    const p = pmap(id);
    if (!p) return "#" + id;
    return lang() === "fa" && p.fa ? p.fa : p.display;
  }
  function sprImg(id, cls){
    let url = "";
    try { url = spriteURL(id); } catch(e){ url = ""; }
    if (!url) return '<span class="lc-sprph"></span>';
    return '<img class="' + cls + '" src="' + url + '" alt="" loading="lazy" onerror="this.style.display=\'none\'">';
  }
  const pctS = p => tpl(t("pct_of"), { p: (p >= 9.95 ? Math.round(p) : p.toFixed(1)).toString().replace(/\.0$/,"") });

  /* ================= indexes ================= */
  /* WILD[g][id] = [{loc, m:'g'|'w'|'f', pct, lo, hi}] */
  const WILD = { red:{}, blue:{}, yellow:{} };
  (function buildWild(){
    for (const loc of LOC1.locs){
      for (const g of ["red","blue","yellow"]){
        const tb = tbl(loc, g); if (!tb) continue;
        const push = (m, sp, lo, hi, pc) => {
          (WILD[g][sp] = WILD[g][sp] || []).push({ loc, m, pct: pc, lo, hi });
        };
        const agg = (arr, useSlot) => {
          const a = {};
          arr.forEach((e, i) => {
            const pc = useSlot ? LOC1.slot[i] : (e[2] !== undefined ? e[2] : 100 / arr.length);
            const s = a[e[0]] = a[e[0]] || { pct: 0, lo: 99, hi: 0 };
            s.pct += pc; s.lo = Math.min(s.lo, e[1]); s.hi = Math.max(s.hi, e[1]);
          });
          return a;
        };
        if (tb.g){ const a = agg(tb.g, true);  Object.keys(a).forEach(sp => push("g", +sp, a[sp].lo, a[sp].hi, a[sp].pct)); }
        if (tb.w){ const a = agg(tb.w, true);  Object.keys(a).forEach(sp => push("w", +sp, a[sp].lo, a[sp].hi, a[sp].pct)); }
        if (tb.f){ const a = agg(tb.f, false); Object.keys(a).forEach(sp => push("f", +sp, a[sp].lo, a[sp].hi, a[sp].pct)); }
      }
    }
  })();
  /* global rods */
  const ROD_ANYWHERE = {};
  ROD_ANYWHERE[LOC1.old[0]] = [{ m:"old", pct:100, lo:LOC1.old[1], hi:LOC1.old[1] }];
  LOC1.good.forEach(g => { (ROD_ANYWHERE[g[0]] = ROD_ANYWHERE[g[0]] || []).push({ m:"good", pct:g[2], lo:g[1], hi:g[1] }); });
  /* SP[id] = [specials] and SPLOC[locId] = [specials] */
  const SP = {}, SPLOC = {};
  LOC1.sp.forEach(s => {
    s.m.forEach(m => (SP[m[0]] = SP[m[0]] || []).push(s));
    if (s.loc) (SPLOC[s.loc] = SPLOC[s.loc] || []).push(s);
  });
  /* direct availability per game (wild + rods + specials) */
  const DIRECT = {};
  for (const g of GAMES){
    const set = new Set();
    const src = (g === "green" ? WILD.blue : WILD[g]) || {};
    Object.keys(src).forEach(id => set.add(+id));
    Object.keys(ROD_ANYWHERE).forEach(id => set.add(+id));
    LOC1.sp.forEach(s => { if (s.v.indexOf(g) !== -1 && s.k !== "evoblock") s.m.forEach(m => set.add(m[0])); });
    DIRECT[g] = set;
  }
  const YELLOW_EVO_BLOCK = new Set([26]);   /* Raichu — Pikachu refuses the stone */
  function evoEdges(){                       /* from gen1-data.js EVOLUTIONS */
    try { return EVOLUTIONS.chains; } catch(e){ return {}; }
  }
  function preEvos(id){
    const out = [];
    for (const ch of Object.values(evoEdges()))
      for (const e of ch.edges) if (e.to === id && e.from <= 151) out.push(e);
    return out;
  }
  const OBT = {};
  function obtainable(g, id, seen){
    if (DIRECT[g].has(id)) return true;
    seen = seen || {};
    if (seen[id]) return false;
    seen[id] = 1;
    if (g === "yellow" && YELLOW_EVO_BLOCK.has(id)) return false;
    return preEvos(id).some(e => obtainable(g, e.from, seen));
  }
  function evoPath(g, id){                   /* earliest direct ancestor → id */
    if (DIRECT[g].has(id)) return null;
    if (g === "yellow" && YELLOW_EVO_BLOCK.has(id)) return null;
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
    return t("conds.special");
  }

  /* ================= detail-pane section ================= */
  let secGame = null;   /* null = follow the page theme */
  function sectionHTML(p){
    if (!secGame) secGame = gameOf();
    const g = secGame;
    const wild = ((g === "green" ? WILD.blue : WILD[g]) || {})[p.id] || [];
    const rods = ROD_ANYWHERE[p.id] || [];
    const spec = (SP[p.id] || []).filter(s => s.v.indexOf(g) !== -1);
    const path = evoPath(g, p.id);
    const chips = GAMES.map(x =>
      '<button class="lchip' + (g === x ? " on" : "") + '" data-lg="' + x + '">' + esc(t("games." + x)) + "</button>").join("");
    let h = '<div class="sec lc-sec" id="locSec">' +
      '<div class="sec-t"><span>' + esc(t("sec_t")) + '</span>' +
        '<button class="mv-all" data-locopen="dex">' + esc(t("all_locations")) + "</button></div>" +
      '<div class="lchips">' + chips + "</div>";

    /* --- wild --- */
    if (wild.length || rods.length){
      h += '<div class="lc-sub">' + esc(t("wild_t")) + "</div>";
      const byLoc = {};
      wild.forEach(w => (byLoc[w.loc.id] = byLoc[w.loc.id] || []).push(w));
      Object.keys(byLoc).map(k => byLoc[k]).forEach(ws => {
        const lo = ws.map(w=>w.lo), hi = ws.map(w=>w.hi);
        const lmin = Math.min(...lo), lmax = Math.max(...hi);
        const badges = ws.map(w => '<span class="lcb lcb-' + w.m + '">' + esc(t(w.m === "g" ? "grass" : w.m === "w" ? "surf" : "rod")) + "</span>").join("");
        h += '<button class="lrow" data-loc="' + ws[0].loc.id + '">' +
          '<span class="lrow-b">' + badges + "</span>" +
          '<span class="lrow-nm"><b>' + esc(ws[0].loc[lang() === "fa" ? "fa" : "en"]) + "</b>" +
            '<i>' + esc(ws[0].loc[lang() === "fa" ? "en" : "fa"]) + "</i></span>" +
          '<span class="lrow-lv">' + esc(lmin === lmax ? tpl(t("lvl"), { n: lmin }) : tpl(t("lvl_rng"), { a: lmin, b: lmax })) + "</span>" +
          "</button>";
      });
      rods.forEach(r => {
        h += '<div class="lrow flat">' +
          '<span class="lrow-b"><span class="lcb lcb-' + r.m + '">' + esc(t(r.m === "old" ? "old_rod" : "good_rod")) + "</span></span>" +
          '<span class="lrow-nm"><b>' + esc(t("any_water")) + "</b></span>" +
          '<span class="lrow-lv">' + esc(tpl(t("lvl"), { n: r.lo })) + "</span></div>";
      });
    }

    /* --- specials --- */
    if (spec.length){
      h += '<div class="lc-sub">' + esc(t("special_t")) + "</div>";
      spec.forEach(s => {
        const sl = s.loc ? LOC1.locs.find(x => x.id === s.loc) : null;
        const locName = sl ? sl[lang() === "fa" ? "fa" : "en"] : "";
        h += '<div class="lrow flat sp">' +
          '<span class="lcb lcb-' + s.k + '">' + esc(t("kinds." + s.k)) + "</span>" +
          '<span class="lrow-det">' +
            (locName ? '<b class="lc-det-loc">' + esc(locName) + "</b> — " : "") +
            esc(s.d[lang() === "fa" ? "fa" : "en"]) +
          (s.loc ? ' <button class="lrow-go" data-loc="' + s.loc + '">▸</button>' : "") + "</span></div>";
      });
    }

    /* --- evolution --- */
    if (path){
      h += '<div class="lc-sub">' + esc(t("evo_t")) + '</div><div class="lc-evo">';
      path.forEach((step, i) => {
        if (i > 0) h += '<span class="lc-evo-c">▸ ' + esc(condText(step.cond)) + "</span>";
        h += '<button class="lc-evo-m' + (step.id === p.id ? " cur" : "") + '" data-id="' + step.id + '">' +
          sprImg(step.id, "lc-spr") + "<span>" + esc(monName(step.id)) + "</span></button>";
      });
      h += "</div>";
    }

    /* --- not obtainable --- */
    const obtainableWays = spec.filter(s => s.k !== "evoblock" && s.k !== "event");
    if (!wild.length && !rods.length && !obtainableWays.length && !path){
      const others = GAMES.filter(x => obtainable(x, p.id));
      h += '<div class="lc-none">' + esc(t("none_t")) + "</div>" +
        '<div class="mv-note">' + esc(others.length
          ? tpl(t("none_note"), { g: t("games." + g), list: others.map(x => t("games." + x)).join(lang() === "fa" ? "، " : " / ") })
          : t("none_nowhere")) + "</div>";
    }
    if (g === "green") h += '<div class="mv-note">' + esc(t("green_note")) + "</div>";
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
      try { select(parseInt(b.dataset.id, 10)); } catch(e){}
    }));
  }
  function renderSection(p){
    const sec = document.getElementById("locSec");
    if (!sec) return;
    sec.outerHTML = sectionHTML(p);
    wire(p);
  }
  function syncGame(){ secGame = null; }   /* theme switched → follow again */

  /* ================= overlay ================= */
  const view = { loc: null, q: "", grp: null, game: null };
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
  function menuOpenSafe(){ try { return typeof menuOpen === "function" ? menuOpen() : false; } catch (err){ return false; } }

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
      groups.map(c => '<button class="it-chip' + ((view.grp === c || (c === "all" && !view.grp)) ? " on" : "") +
        '" data-g="' + c + '">' + esc(c === "all" ? t("all") : t("groups." + c)) + "</button>").join("") +
      '<span class="lc-gap"></span>' +
      GAMES.map(g => '<button class="it-chip gchip' + (view.game === g ? " on" : "") + '" data-gm="' + g + '">' +
        esc(t("games." + g)) + "</button>").join("");
    el.viewbar.querySelectorAll(".it-chip[data-g]").forEach(b => b.addEventListener("click", () => {
      view.grp = b.dataset.g === "all" ? null : b.dataset.g; renderDex();
    }));
    el.viewbar.querySelectorAll(".gchip").forEach(b => b.addEventListener("click", () => {
      view.game = b.dataset.gm; renderDex();
    }));
    if (view.loc){ renderLoc(view.loc); return; }
    el.sub.innerHTML = '<input id="lcQ" type="search" autocomplete="off" spellcheck="false" placeholder="' + esc(t("search_ph")) + '">';
    el.sub.querySelector("#lcQ").value = view.q;
    el.sub.querySelector("#lcQ").addEventListener("input", e => { view.q = e.target.value; renderList(); });
    renderList();
  }
  function locSpecies(loc, g){
    const tb = tbl(loc, g); if (!tb) return [];
    const set = new Set();
    (tb.g || []).forEach(e => set.add(e[0]));
    (tb.w || []).forEach(e => set.add(e[0]));
    (tb.f || []).forEach(e => set.add(e[0]));
    return [...set];
  }
  function renderList(){
    const q = view.q.trim().toLowerCase();
    const arr = LOC1.locs.filter(l => {
      if (view.grp && l.g !== view.grp) return false;
      if (q && (l.en + " " + l.fa).toLowerCase().indexOf(q) === -1) return false;
      return true;
    });
    el.body.innerHTML =
      '<div class="it-count">' + esc(tpl(t("count"), { a: arr.length })) + "</div>" +
      '<div class="lc-grid">' + arr.map(loc => {
        const sp = locSpecies(loc, view.game).length;
        const tb = tbl(loc, view.game) || {};
        const meth = ["g","w","f"].filter(k => tb[k] && tb[k].length).map(k =>
          '<i class="lc-mi lc-mi-' + k + '"></i>').join("");
        const hasSp = (SPLOC[loc.id] || []).some(s => s.v.indexOf(view.game) !== -1);
        return '<button class="lcard" data-loc="' + loc.id + '">' +
          '<span class="lcard-nm"><b>' + esc(loc[lang() === "fa" ? "fa" : "en"]) + "</b>" +
            "<i>" + esc(loc[lang() === "fa" ? "en" : "fa"]) + "</i></span>" +
          '<span class="lcard-meta">' + meth +
            '<b class="lc-n">' + num(sp) + "</b>" +
            (hasSp ? '<span class="lc-star">★</span>' : "") + "</span>" +
        "</button>";
      }).join("") + "</div>" +
      (arr.length ? "" : '<div class="it-note">' + esc(t("no_results")) + "</div>") +
      '<div class="it-note">' + esc(view.game === "green" ? t("green_note") : t("oldrod_note")) + "</div>";
    el.body.querySelectorAll(".lcard").forEach(c =>
      c.addEventListener("click", () => { view.loc = c.dataset.loc; renderDex(); }));
    const first = el.body.querySelector(".lcard");
    if (first) first.focus();
  }

  /* ---------- location view ---------- */
  function encRows(arr, useSlot){
    const a = {};
    arr.forEach((e, i) => {
      const pc = useSlot ? LOC1.slot[i] : (e[2] !== undefined ? e[2] : 100 / arr.length);
      const s = a[e[0]] = a[e[0]] || { pct: 0, lo: 99, hi: 0, n: 0 };
      s.pct += pc; s.lo = Math.min(s.lo, e[1]); s.hi = Math.max(s.hi, e[1]); s.n++;
    });
    return Object.keys(a).map(Number).sort((x,y) => a[y].pct - a[x].pct).map(id => {
      const s = a[id];
      return '<button class="lrow mon" data-id="' + id + '">' +
        sprImg(id, "lc-spr") +
        '<span class="lrow-nm"><b>' + esc(monName(id)) + "</b></span>" +
        '<span class="lrow-lv">' + esc(s.lo === s.hi ? tpl(t("lvl"), { n: s.lo }) : tpl(t("lvl_rng"), { a: s.lo, b: s.hi })) + "</span>" +
        '<span class="lrow-pc">' + esc(pctS(s.pct)) + "</span>" +
      "</button>";
    }).join("");
  }
  function renderLoc(locId){
    const loc = LOC1.locs.find(l => l.id === locId);
    if (!loc){ view.loc = null; renderDex(); return; }
    const g = view.game;
    const tb = tbl(loc, g) || {};
    el.viewbar.innerHTML =
      (view.loc ? '<button class="it-back" id="lcBack">' + esc(t("back")) + "</button>" : "") +
      '<span class="lc-gap"></span>' +
      GAMES.map(x => '<button class="it-chip gchip' + (g === x ? " on" : "") + '" data-gm="' + x + '">' +
        esc(t("games." + x)) + "</button>").join("");
    el.viewbar.querySelector("#lcBack").addEventListener("click", () => { view.loc = null; renderDex(); });
    el.viewbar.querySelectorAll(".gchip").forEach(b => b.addEventListener("click", () => {
      view.game = b.dataset.gm; renderDex();
    }));
    let h = '<div class="lc-ltitle"><b>' + esc(loc[lang() === "fa" ? "fa" : "en"]) + "</b>" +
      "<i>" + esc(loc[lang() === "fa" ? "en" : "fa"]) + "</i></div>";
    if (tb.g && tb.g.length)
      h += '<div class="lc-sub">' + esc(t("grass")) + ' <i class="lc-rate">' + esc(tpl(t("rate_tpl"), { r: tb.gr, p: Math.round(tb.gr / 255 * 100) })) + "</i></div>" +
           '<div class="lc-rows">' + encRows(tb.g, true) + "</div>";
    if (tb.w && tb.w.length)
      h += '<div class="lc-sub">' + esc(t("surf")) + ' <i class="lc-rate">' + esc(tpl(t("rate_tpl"), { r: tb.wr, p: Math.round(tb.wr / 255 * 100) })) + "</i></div>" +
           '<div class="lc-rows">' + encRows(tb.w, true) + "</div>";
    if (tb.f && tb.f.length)
      h += '<div class="lc-sub">' + esc(t("rod")) + "</div>" +
           '<div class="lc-rows">' + encRows(tb.f, false) + "</div>";
    if (tb.g || tb.w || tb.f){
      h += '<div class="lc-rodnote">' +
        '<b>' + esc(t("old_rod")) + "</b> " + esc(t("oldrod_note")) + "<br>" +
        '<b>' + esc(t("good_rod")) + "</b> " + esc(t("goodrod_note")) + "</div>";
    }
    const sps = (SPLOC[loc.id] || []).filter(s => s.v.indexOf(g) !== -1);
    if (sps.length){
      h += '<div class="lc-sub">' + esc(t("special_t")) + "</div>" + '<div class="lc-rows">';
      sps.forEach(s => {
        const mons = s.m.map(m => m[0]).map(id =>
          '<button class="lc-spmon" data-id="' + id + '" title="' + esc(monName(id)) + '">' +
            sprImg(id, "lc-spr sm") + "<span>" + esc(monName(id)) + "</span></button>").join("");
        h += '<div class="lrow flat sp">' +
          '<span class="lrow-mons">' + mons + "</span>" +
          '<span class="lcb lcb-' + s.k + '">' + esc(t("kinds." + s.k)) + "</span>" +
          '<span class="lrow-det">' + esc(s.d[lang() === "fa" ? "fa" : "en"]) + "</span></div>";
      });
      h += "</div>";
    }
    if (/SafariZone/.test(loc.id)) h += '<div class="mv-note">' + esc(t("safari_note")) + "</div>";
    if (g === "green") h += '<div class="mv-note">' + esc(t("green_note")) + "</div>";
    el.sub.innerHTML = "";
    el.body.innerHTML = h;
    el.body.querySelectorAll(".lrow.mon").forEach(r => r.addEventListener("click", () => {
      closeDex();
      try { select(parseInt(r.dataset.id, 10)); } catch(e){}
    }));
    el.body.querySelectorAll(".lc-spmon").forEach(r => r.addEventListener("click", () => {
      closeDex();
      try { select(parseInt(r.dataset.id, 10)); } catch(e){}
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
