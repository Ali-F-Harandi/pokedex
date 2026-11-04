"use strict";
/* Pokédex Plus — MOVES module (Phase 2)
   ============================================================
   Loaded AFTER the page script (redblue/yellow/goldsilver/crystal.js),
   the shared names file (moves-fa.js → MOVE_INFO) and this page's
   data file (moves-rb|yellow|gs|crystal.js → MD).

   Adds:
     · MOVES section in the Pokémon detail pane — the learnset of
       THIS game, grouped by method (level-up / TM·HM / egg / tutor)
       with learn levels and TM numbers. Rows open the move card.
     · Moves Dex overlay — every move of this game, bilingual,
       search + type + class filters, authentic in-game description
       (Gen 2) / effect wording (Gen 1) and "who can learn it" chips
       that jump straight to a Pokémon.
     · TM/HM list overlay — the authentic machine list of this game.
     · Two START-menu entries (Moves Dex / TM·HM list).

   Historical accuracy (per project philosophy):
     · power / type / accuracy / PP come from the pret decompiles
       (pokered / pokegold) — e.g. Gust & Karate Chop are NORMAL in
       Gen 1, Rock Throw is 65% accurate in Gen 1.
     · physical/special is derived from the move TYPE (Gen 1-2 rule).
     · Struggle's "???" type badge for Curse matches the games.
     · Gen-1 games had no move text: the wording shown is labelled
       as the Gold/Silver text.
*/

const MovesUI = (() => {

  /* ================= i18n ================= */
  const MI18N = {
    en: {
      moves_t: "MOVES", all_moves: "ALL MOVES ▸",
      tab_lv: "LEVEL-UP", tab_tm: "TM · HM", tab_egg: "EGG", tab_tutor: "TUTOR",
      dex_t: "MOVES DEX", tm_t: "TM / HM LIST", close: "Close", back: "◂ BACK",
      power: "PWR", acc: "ACC", pp: "PP", level: "Lv.",
      physical: "PHYS", special: "SPEC", class_t: "Class", all: "ALL",
      search_ph: "Search a move…", no_results: "No moves found.",
      desc_t: "DESCRIPTION", effect_t: "EFFECT",
      learned_by: "WHO CAN LEARN IT", n_moves: "{a} moves",
      gen1_note: "The Gen-1 games had no in-game move descriptions.",
      green_note: "The Japan-only Green version follows Red/Blue move data.",
      tutor_note: "Crystal's Move Tutor in Goldenrod City teaches Flamethrower, Thunderbolt and Ice Beam for a price.",
      never_miss: "Never misses", menu_moves: "Moves Dex", menu_tmhm: "TM / HM list",
      unknown_type: "???", from_egg: "via breeding", lv_prefix: "Lv."
    },
    fa: {
      moves_t: "حرکت‌ها", all_moves: "◂ همه حرکت‌ها",
      tab_lv: "با سطح", tab_tm: "TM · HM", tab_egg: "تخم", tab_tutor: "آموزشگار",
      dex_t: "دکس حرکت‌ها", tm_t: "لیست TM / HM", close: "بستن", back: "◂ بازگشت",
      power: "قدرت", acc: "دقت", pp: "PP", level: "سطح",
      physical: "فیزیکی", special: "ویژه", class_t: "دسته", all: "همه",
      search_ph: "جست‌وجوی حرکت…", no_results: "حرکتی پیدا نشد.",
      desc_t: "توضیح", effect_t: "اثر",
      learned_by: "چه کسانی می‌توانند یاد بگیرند؟", n_moves: "{a} حرکت",
      gen1_note: "بازی‌های نسل ۱ توضیح حرکت نداشتند.",
      green_note: "نسخه‌ی سبزِ ژاپنی همان داده‌ی حرکتی قرمز/آبی را دارد.",
      tutor_note: "در کریستال، «معلم حرکت» در شهر گلدن‌راد، حرکت‌های پرتاب شعله، رعد و برق و پرتو یخی را در ازای پول یاد می‌دهد.",
      never_miss: "هرگز خطا نمی‌رود", menu_moves: "دکس حرکت‌ها", menu_tmhm: "لیست TM / HM",
      unknown_type: "؟؟؟", from_egg: "از طریق تخم‌گذاری", lv_prefix: "سطح "
    }
  };
  const mt = k => (MI18N[state.lang] || MI18N.en)[k] || k;

  /* ================= data helpers ================= */
  const SPECIAL = new Set(["fire", "water", "electric", "grass", "ice", "psychic", "dragon", "dark"]);
  const classOf = tp => tp === "unknown" ? null : (SPECIAL.has(tp) ? "special" : "physical");
  const MACH = {};                                    /* moveId -> {kind, num} */
  Object.keys(MD.tm).forEach(n => { MACH[MD.tm[n]] = { kind: "TM", num: +n }; });
  Object.keys(MD.hm).forEach(n => { MACH[MD.hm[n]] = { kind: "HM", num: +n }; });

  const info = s => MOVE_INFO[s] || [s, s, "", ""];
  const mrow = id => MD.moves[id];                    /* [slug, type, power, acc, pp] */
  const mType = id => mrow(id)[1];
  const dispEN = slug => info(slug)[0];
  const dispFA = slug => info(slug)[1];
  const descEN = slug => info(slug)[2];
  const descFA = slug => info(slug)[3];
  const typeName = tp => tp === "unknown" ? mt("unknown_type") : (t("types." + tp) || tp);
  const typeColor = tp => TYPE_COLOR[tp] || "#68A090";
  const fmtPow = p => (p && p > 1) ? num(p) : "—";
  const fmtAcc = (a, tp) => +a > 0 ? num(a) + "%" : (a === 0 ? "∞" : "—");
  const neverMiss = id => +mrow(id)[3] === 0;

  const learnOf = pid => MD.learn[pid] || { lv: [], tm: [], egg: [], tutor: [] };

  /* learned-by cache: moveId -> {lv:[[pid,lvl]], tm:[pid], egg:[pid], tutor:[pid]} */
  const byCache = new Map();
  function learnersOf(mid){
    if (byCache.has(mid)) return byCache.get(mid);
    const out = { lv: [], tm: [], egg: [], tutor: [] };
    Object.keys(MD.learn).forEach(pid => {
      const b = MD.learn[pid]; pid = +pid;
      b.lv.forEach(p => { if (p[1] === mid) out.lv.push([pid, p[0]]); });
      if (b.tm.indexOf(mid) !== -1) out.tm.push(pid);
      if (b.egg.indexOf(mid) !== -1) out.egg.push(pid);
      if (b.tutor.indexOf(mid) !== -1) out.tutor.push(pid);
    });
    out.lv.sort((a, b) => a[1] - b[1] || a[0] - b[0]);
    byCache.set(mid, out);
    return out;
  }

  /* ================= small builders ================= */
  function typeBadge(tp){
    return '<span class="tbadge T-' + tp + ' mv-tb">' + esc(typeName(tp)) + "</span>";
  }
  function classChip(tp){
    const c = classOf(tp);
    if (!c) return '<span class="mv-class unknown">???</span>';
    return '<span class="mv-class ' + c + '" title="' + esc(mt("class_t")) + '">' +
      (c === "physical" ? "⚔ " : "✦ ") + esc(mt(c)) + "</span>";
  }
  function statCells(id){
    const r = mrow(id);
    return '<span class="mv-cell"><i>' + esc(mt("power")) + "</i><b>" + fmtPow(r[2]) + "</b></span>" +
           '<span class="mv-cell"><i>' + esc(mt("acc")) + "</i><b>" + fmtAcc(r[3], r[1]) + "</b></span>" +
           '<span class="mv-cell"><i>' + esc(mt("pp")) + "</i><b>" + num(r[4]) + "</b></span>";
  }
  function moveName(id, big){
    const s = mrow(id)[0];
    const en = dispEN(s), fa = dispFA(s);
    const enEl = '<span class="mv-en' + (big ? " big" : "") + '">' + esc(en.toUpperCase()) + "</span>";
    const faEl = '<span class="mv-fa' + (big ? " big" : "") + '">' + esc(fa) + "</span>";
    return state.lang === "fa"
      ? faEl + '<span class="mv-sub">' + enEl + "</span>"
      : enEl + '<span class="mv-sub">' + faEl + "</span>";
  }

  /* ================= detail-pane section ================= */
  let secTab = "lv";
  function sectionHTML(p){
    const b = learnOf(p.id);
    const counts = { lv: b.lv.length, tm: b.tm.length, egg: b.egg.length, tutor: b.tutor.length };
    const tabs = [["lv", "tab_lv"], ["tm", "tab_tm"], ["egg", "tab_egg"], ["tutor", "tab_tutor"]]
      .filter(x => counts[x[0]] > 0)
      .map(x => '<button class="mtab' + (secTab === x[0] ? " on" : "") + '" data-mt="' + x[0] + '">' +
        esc(mt(x[1])) + ' <i>' + num(counts[x[0]]) + "</i></button>").join("");
    if (!counts[secTab]) secTab = counts.lv ? "lv" : (counts.tm ? "tm" : "lv");
    let rows = "";
    if (secTab === "lv"){
      rows = b.lv.map(x => moveRow(x[1], mt("lv_prefix") + num(x[0]))).join("");
    } else if (secTab === "tm"){
      rows = b.tm.map(m => moveRow(m, machLabel(m))).join("");
    } else if (secTab === "egg"){
      rows = b.egg.map(m => moveRow(m, "🥚")).join("");
    } else {
      rows = b.tutor.map(m => moveRow(m, "🎓")).join("");
    }
    const notes = [];
    if (MD.game === "red-blue") notes.push('<div class="mv-note">' + esc(mt("green_note")) + "</div>");
    if (MD.gen === 1) notes.push('<div class="mv-note">' + esc(mt("gen1_note")) + "</div>");
    return '<div class="sec mv-sec" id="movesSec">' +
      '<div class="sec-t"><span class="mv-sec-title">' + esc(mt("moves_t")) +
        ' <em class="mv-game">' + esc(MD.label) + "</em></span>" +
        '<button class="mv-all" data-mvopen="dex">' + esc(mt("all_moves")) + "</button></div>" +
      '<div class="mtabs">' + tabs + "</div>" +
      '<div class="mv-list">' + (rows || '<div class="mv-note">' + esc(mt("no_results")) + "</div>") + "</div>" +
      notes.join("") +
      "</div>";
  }
  function machLabel(mid){
    const m = MACH[mid];
    return m ? m.kind + num(m.num) : "TM";
  }
  function moveRow(mid, badge){
    const r = mrow(mid);
    return '<button class="mrow" data-mv="' + mid + '">' +
      '<span class="mv-badge">' + esc(badge) + "</span>" +
      '<span class="mv-name">' + moveName(mid) + "</span>" +
      typeBadge(r[1]) + classChip(r[1]) +
      '<span class="mv-stats">' + statCells(mid) + "</span>" +
      "</button>";
  }
  function wire(p){
    const sec = document.getElementById("movesSec");
    if (!sec) return;
    sec.querySelectorAll(".mtab").forEach(b => b.addEventListener("click", () => {
      secTab = b.dataset.mt; renderSection(p);
    }));
    sec.querySelector(".mv-all").addEventListener("click", () => openDex("list"));
    sec.querySelectorAll(".mrow").forEach(r => r.addEventListener("click", () => {
      openDex("detail", +r.dataset.mv);
    }));
  }
  function renderSection(p){
    const sec = document.getElementById("movesSec");
    if (!sec) return;
    sec.outerHTML = sectionHTML(p);
    wire(p);
  }

  /* ================= game switching (gen1.html only) =================
     The merged Gen-1 page swaps the active game's moves data when the
     RED/BLUE/GREEN/YELLOW theme changes. On it, `MD` is a mutable `var`
     (moves-gen1.js) so the swap sticks; single-game pages declare `const
     MD` and simply never call this. */
  function setGame(next){
    if (!next || next === MD) return;
    try { MD = next; } catch(err){ return; }
    Object.keys(MACH).forEach(k => { delete MACH[k]; });
    Object.keys(MD.tm).forEach(n => { MACH[MD.tm[n]] = { kind: "TM", num: +n }; });
    Object.keys(MD.hm).forEach(n => { MACH[MD.hm[n]] = { kind: "HM", num: +n }; });
    byCache.clear();
    secTab = "lv";
    view.mode = "list"; view.q = ""; view.type = null; view.cls = null; view.move = null;
    try { renderSection(typeof select === "function" && typeof state !== "undefined" ? PMAP[state.sel] : undefined); } catch(err){}
    if (isOpen()) renderDex();
  }

  /* ================= overlay ================= */
  const view = { mode: "list", q: "", type: null, cls: null, move: null };
  let el = null;

  function ensureOverlay(){
    if (el) return;
    const w = document.createElement("div");
    w.id = "movesWrap"; w.className = "hidden";
    w.innerHTML =
      '<div id="movesBox" role="dialog" aria-modal="true">' +
        '<div class="mv-head"><span class="mv-head-t" id="mvHeadT"></span>' +
          '<button class="mv-close" id="mvClose" title="Close">✕</button></div>' +
        '<div class="mv-viewbar" id="mvViewbar"></div>' +
        '<div class="mv-sub" id="mvSub"></div>' +
        '<div class="mv-body" id="mvBody"></div>' +
      "</div>";
    document.body.appendChild(w);
    el = {
      wrap: w, head: w.querySelector("#mvHeadT"), viewbar: w.querySelector("#mvViewbar"),
      sub: w.querySelector("#mvSub"), body: w.querySelector("#mvBody")
    };
    w.addEventListener("click", e => { if (e.target === w) closeDex(); });
    w.querySelector("#mvClose").addEventListener("click", closeDex);
    document.addEventListener("keydown", e => {
      if (e.key === "Escape" && !w.classList.contains("hidden")){ e.stopPropagation(); closeDex(); }
      else if (!e.target.matches("input,select,textarea") && e.key.toLowerCase() === "m" &&
               w.classList.contains("hidden") && !menuOpenSafe()) openDex();
    }, true);
  }
  function menuOpenSafe(){
    try { return menuOpen(); } catch (err) { return false; }
  }

  function openDex(mode, moveId){
    ensureOverlay();
    if (mode) view.mode = mode;
    if (moveId) view.move = moveId;
    if (view.mode === "detail" && !view.move) view.mode = "list";
    el.wrap.classList.remove("hidden");
    renderDex();
  }
  function closeDex(){ if (el) el.wrap.classList.add("hidden"); }
  function isOpen(){ return el && !el.wrap.classList.contains("hidden"); }

  function renderDex(){
    el.head.textContent = (view.mode === "tmhm" ? mt("tm_t") : mt("dex_t")) + " · " + MD.label;
    /* view tabs */
    el.viewbar.innerHTML =
      '<button class="mvtab' + (view.mode !== "tmhm" ? " on" : "") + '" data-v="all">☰ ' + esc(mt("dex_t")) + "</button>" +
      '<button class="mvtab' + (view.mode === "tmhm" ? " on" : "") + '" data-v="tmhm">📼 ' + esc(mt("tm_t")) + "</button>";
    el.viewbar.querySelectorAll(".mvtab").forEach(b => b.addEventListener("click", () => {
      view.mode = b.dataset.v === "tmhm" ? "tmhm" : "list";
      if (view.mode === "list" && !view.move) view.mode = "list";
      renderDex();
    }));
    if (view.mode === "tmhm") renderTMHM();
    else if (view.mode === "detail") renderDetail();
    else renderList();
  }

  /* ---------- list view ---------- */
  function renderList(){
    const types = Object.keys(MD.moves).map(id => mType(id))
      .filter((v, i, a) => a.indexOf(v) === i)
      .sort((a, b) => (MD.gen === 1 ? TYPE_ORDER.indexOf(a) - TYPE_ORDER.indexOf(b) : 0));
    const cls = view.cls;
    el.sub.innerHTML =
      '<div class="mv-controls">' +
        '<input id="mvQ" type="search" autocomplete="off" spellcheck="false" placeholder="' + esc(mt("search_ph")) + '">' +
        '<div class="mv-typechips">' +
          '<button class="mchip' + (view.type ? "" : " on") + '" data-t="">' + esc(mt("all")) + "</button>" +
          types.map(tp => '<button class="mchip T-chip-' + tp + (view.type === tp ? " on" : "") +
            '" data-t="' + tp + '"><span style="background:' + typeColor(tp) + '"></span>' + esc(typeName(tp)) + "</button>").join("") +
        "</div>" +
        '<div class="mv-clschips">' +
          ["physical", "special"].map(c =>
            '<button class="mchip' + (cls === c ? " on " + c : "") + '" data-c="' + c + '">' +
            (c === "physical" ? "⚔ " : "✦ ") + esc(mt(c)) + "</button>").join("") +
          (cls ? '<button class="mchip" data-c="">' + esc(mt("all")) + "</button>" : "") +
        "</div>" +
      "</div>";
    const q = el.sub.querySelector("#mvQ");
    q.value = view.q;
    q.addEventListener("input", () => { view.q = q.value; renderCards(); });
    el.sub.querySelectorAll(".mv-typechips .mchip").forEach(b => b.addEventListener("click", () => {
      view.type = b.dataset.t || null; renderList(); q.focus();
    }));
    el.sub.querySelectorAll(".mv-clschips .mchip").forEach(b => b.addEventListener("click", () => {
      view.cls = b.dataset.c || null; renderList(); q.focus();
    }));
    renderCards();
  }
  function renderCards(){
    const ql = view.q.trim().toLowerCase();
    const ids = Object.keys(MD.moves).map(Number).filter(id => {
      const r = mrow(id);
      if (view.type && r[1] !== view.type) return false;
      if (view.cls && classOf(r[1]) !== view.cls) return false;
      if (ql){
        const s = r[0];
        if (s.indexOf(ql) === -1 &&
            dispEN(s).toLowerCase().indexOf(ql) === -1 &&
            dispFA(s).indexOf(view.q.trim()) === -1 &&
            machLabel(id).toLowerCase().indexOf(ql) === -1) return false;
      }
      return true;
    });
    const count = document.createElement("div");
    count.className = "mv-count";
    count.textContent = tplNum(mt("n_moves"), num(ids.length));
    el.body.innerHTML = "";
    el.body.appendChild(count);
    if (!ids.length){
      const n = document.createElement("div"); n.className = "mv-note";
      n.textContent = mt("no_results"); el.body.appendChild(n); return;
    }
    const grid = document.createElement("div");
    grid.className = "mgrid";
    grid.innerHTML = ids.map(id =>
      '<button class="mcard" data-mv="' + id + '">' +
        '<span class="mcard-name">' + moveName(id) + "</span>" +
        '<span class="mcard-meta">' + typeBadge(mType(id)) + classChip(mType(id)) + "</span>" +
        '<span class="mcard-stats">' + statCells(id) + "</span>" +
      "</button>").join("");
    el.body.appendChild(grid);
    grid.querySelectorAll(".mcard").forEach(c => c.addEventListener("click", () => {
      view.move = +c.dataset.mv; view.mode = "detail"; renderDex();
    }));
  }

  /* ---------- TM/HM view ---------- */
  function renderTMHM(){
    el.sub.innerHTML = "";
    const rows = [];
    [["tm", "TM"], ["hm", "HM"]].forEach(pair => {
      Object.keys(MD[pair[0]]).sort((a, b) => +a - +b).forEach(n => {
        const mid = MD[pair[0]][n];
        rows.push('<button class="mrow tmrow" data-mv="' + mid + '">' +
          '<span class="mv-badge mach">' + pair[1] + num(+n) + "</span>" +
          '<span class="mv-name">' + moveName(mid) + "</span>" +
          typeBadge(mType(mid)) + classChip(mType(mid)) +
          '<span class="mv-stats">' + statCells(mid) + "</span></button>");
      });
    });
    el.body.innerHTML =
      '<div class="tmlist">' + rows.join("") + "</div>" +
      (MD.game === "crystal" ? '<div class="mv-note big">' + esc(mt("tutor_note")) + "</div>" : "");
    el.body.querySelectorAll(".mrow").forEach(r => r.addEventListener("click", () => {
      view.move = +r.dataset.mv; view.mode = "detail"; renderDex();
    }));
  }

  /* ---------- move detail view ---------- */
  function renderDetail(){
    const id = view.move, r = mrow(id), slug = r[0];
    el.sub.innerHTML = "";
    const isGen1 = MD.gen === 1;
    const descLabel = isGen1 ? mt("effect_t") : mt("desc_t");
    const lb = learnersOf(id);
    const groups = [];
    const chip = (pid, extra) =>
      '<button class="lchip" data-p="' + pid + '">' + esc(dispName(PMAP[pid])) +
      (extra || "") + "</button>";
    if (lb.lv.length)
      groups.push('<div class="lgroup"><div class="lg-t">' + esc(mt("tab_lv")) + " <i>" + num(lb.lv.length) + "</i></div>" +
        '<div class="lchips">' + lb.lv.map(x => chip(x[0], ' <b class="lv">' + mt("lv_prefix") + num(x[1]) + "</b>")).join("") + "</div></div>");
    if (lb.tm.length)
      groups.push('<div class="lgroup"><div class="lg-t">' + esc(mt("tab_tm")) + " <i>" + num(lb.tm.length) + "</i></div>" +
        '<div class="lchips">' + lb.tm.map(pid => chip(pid)).join("") + "</div></div>");
    if (lb.egg.length)
      groups.push('<div class="lgroup"><div class="lg-t">' + esc(mt("tab_egg")) + " <i>" + num(lb.egg.length) + "</i></div>" +
        '<div class="lchips">' + lb.egg.map(pid => chip(pid)).join("") + "</div></div>");
    if (lb.tutor.length)
      groups.push('<div class="lgroup"><div class="lg-t">' + esc(mt("tab_tutor")) + " <i>" + num(lb.tutor.length) + "</i></div>" +
        '<div class="lchips">' + lb.tutor.map(pid => chip(pid)).join("") + "</div></div>");

    el.body.innerHTML =
      '<button class="mv-back" id="mvBack">◂ ' + esc(mt("back")) + "</button>" +
      '<div class="md-card">' +
        '<div class="md-head">' +
          '<span class="md-no">#' + num(id) + "</span>" +
          '<span class="md-name">' + moveName(id, true) + "</span>" +
          '<span class="md-meta">' + typeBadge(r[1]) + classChip(r[1]) +
            (MACH[id] ? '<span class="mv-badge mach md-mach">' + machLabel(id) + "</span>" : "") + "</span>" +
        "</div>" +
        '<div class="md-stats">' +
          '<div class="md-stat"><i>' + esc(mt("power")) + "</i><b>" + fmtPow(r[2]) + "</b></div>" +
          '<div class="md-stat"><i>' + esc(mt("acc")) + "</i><b>" + (neverMiss(id) ? esc(mt("never_miss")) : fmtAcc(r[3], r[1])) + "</b></div>" +
          '<div class="md-stat"><i>' + esc(mt("pp")) + "</i><b>" + num(r[4]) + "</b></div>" +
        "</div>" +
        '<div class="mv-sec-t">' + esc(descLabel) + "</div>" +
        '<div class="md-desc">' +
          '<p class="d-fa">' + esc(descFA(slug)) + "</p>" +
          '<p class="d-en">' + esc(descEN(slug)) + "</p>" +
        "</div>" +
        (isGen1 ? '<div class="mv-note">' + esc(mt("gen1_note")) + "</div>" : "") +
      "</div>" +
      '<div class="mv-sec-t">' + esc(mt("learned_by")) + "</div>" +
      (groups.length ? groups.join("") : '<div class="mv-note">' + esc(mt("no_results")) + "</div>");
    el.body.querySelector("#mvBack").addEventListener("click", () => {
      view.mode = "list"; renderDex();
    });
    el.body.querySelectorAll(".lchip").forEach(c => c.addEventListener("click", () => {
      closeDex();
      select(+c.dataset.p);
    }));
  }
  function tplNum(s, n){ return s.replace("{a}", n); }

  /* ================= START menu + language ================= */
  function injectMenu(){
    const pop = document.getElementById("menuPop");
    if (!pop || pop.querySelector("[data-act=movesdex]")) return;
    const sep = pop.querySelector(".m-sep") || pop.querySelector("[data-act=reset]");
    const mk = (act, icon, key) => {
      const b = document.createElement("button");
      b.className = "m-item"; b.dataset.act = act;
      b.innerHTML = '<span class="mi">' + icon + '</span><span class="mv-menu-l" data-key="' + key + '"></span>';
      return b;
    };
    const b1 = mk("movesdex", "&#128214;", "menu_moves");
    const b2 = mk("tmhm", "&#128252;", "menu_tmhm");
    pop.insertBefore(b1, sep);
    pop.insertBefore(b2, sep.nextSibling);
    pop.addEventListener("click", e => {
      const it = e.target.closest(".m-item");
      if (!it) return;
      if (it.dataset.act === "movesdex") openDex("list");
      else if (it.dataset.act === "tmhm") openDex("tmhm");
    });
  }
  function applyLang(){
    document.querySelectorAll(".mv-menu-l").forEach(s => { s.textContent = mt(s.dataset.key); });
    const c = document.getElementById("mvClose");
    if (c) c.title = mt("close");
    if (isOpen()) renderDex();
  }
  injectMenu();
  ensureOverlay();   /* register the M-key shortcut before the first open */

  return { sectionHTML, wire, renderSection, setGame, openDex, closeDex, applyLang, learnersOf };
})();
