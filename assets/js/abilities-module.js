"use strict";
/* Pokédex Plus — ABILITY DEX module, GENERATION III (gen3.html).
   ============================================================
   Gen-3's fourth dex, next to Moves (M) / Items (I) / Locations (L):
   the era-authentic ability set of the GBA games, opened with the Y
   key, the START menu, or by tapping an ability chip on a Pokémon's
   page. Loaded AFTER abilities-gen3.js (ABIL3 + NATURES3) and
   gen3-data.js (DATA — the per-mon slots it cross-references).

   The card pair is era-true and Era-wide: every Gen-3 cartridge reads
   the same ability assignments (there was no per-game difference —
   the stat split and hidden abilities did not exist yet), so one list
   serves RUBY through LEAFGREEN. Cacophony is kept in the list with
   an honest note: the games define it but no Pokémon carries it.

   Everything user-visible is bilingual EN/FA (AI table below). */

const AbilityUI = (() => {

  /* ================= i18n ================= */
  const AI = {
    en: {
      dex_t: "ABILITY DEX", close: "Close",
      search_ph: "Search an ability…", no_results: "No abilities found.",
      count: "{a} abilities", era_note: "The complete Gen-3 ability set, straight from the pokeemerald disassembly — every game of this era reads the same list.",
      unused: "Defined in the games' code, but no Pokémon of this era carries it.",
      slot1: "First ability", slot2: "Second ability",
      users_t: "POKéMON WITH THIS ABILITY", users_none: "No Pokémon has this ability.",
      mons: "{a} Pokémon", menu_abilities: "Ability Dex",
      effect_t: "EFFECT"
    },
    fa: {
      dex_t: "دکس توانایی", close: "بستن",
      search_ph: "جست‌وجوی توانایی…", no_results: "توانایی‌ای پیدا نشد.",
      count: "{a} توانایی", era_note: "مجموعه‌ی کامل توانایی‌های نسل ۳، مستقیم از دیساسمبل pokeemerald — همه‌ی بازی‌های این نسل همین فهرست را دارند.",
      unused: "در کد بازی‌ها تعریف شده، اما هیچ پوکمونی در این نسل آن را ندارد.",
      slot1: "توانایی اول", slot2: "توانایی دوم",
      users_t: "پوکمون‌های دارای این توانایی", users_none: "هیچ پوکمونی این توانایی را ندارد.",
      mons: "{a} پوکمون", menu_abilities: "دکس توانایی",
      effect_t: "اثر"
    }
  };
  const lang = () => (typeof state !== "undefined" && state.lang) || "en";
  const t = k => AI[lang()][k] !== undefined ? AI[lang()][k] : AI.en[k];
  const tpl = (s, o) => s.replace(/\{(\w+)\}/g, (_, k) => o[k] !== undefined ? o[k] : "{" + k + "}");
  const faD = n => String(n).replace(/[0-9]/g, d => "۰۱۲۳۴۵۶۷۸۹"[+d]);
  const num = n => lang() === "fa" ? faD(n) : String(n);
  const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

  /* ================= data ================= */
  if (typeof ABIL3 === "undefined") {
    return { openDex(){}, closeDex(){}, applyLang(){} };
  }
  const BY_SLUG = {};
  ABIL3.forEach(a => { BY_SLUG[a.slug] = a; });
  /* per-ability users straight from the dex DATA: slot 1 / slot 2 */
  const USERS = {};
  ABIL3.forEach(a => { USERS[a.slug] = { s1: [], s2: [] }; });
  if (typeof DATA !== "undefined") {
    for (const p of DATA) {
      (p.abilities || []).forEach((slug, i) => {
        if (!USERS[slug]) return;
        (i === 0 ? USERS[slug].s1 : USERS[slug].s2).push(p.id);
      });
    }
  }
  const userCount = slug => USERS[slug].s1.length + USERS[slug].s2.length;

  function abilName(a){
    return lang() === "fa" && a.name_fa ? a.name_fa : a.en;
  }
  function abilNameAlt(a){
    return lang() === "fa" ? a.en : (a.name_fa || "");
  }
  function abilEffect(a){
    return lang() === "fa" ? a.eff_fa : a.eff_en;
  }
  function pmap(id){ try { return typeof DATA !== "undefined" ? DATA[id - 1] : null; } catch (e) { return null; } }
  function monName(id){
    const p = pmap(id);
    if (!p) return "#" + id;
    return lang() === "fa" && p.fa ? p.fa : p.display;
  }
  function sprImg(id, cls){
    let url = "";
    try { url = spriteURL(id); } catch (e) { url = ""; }
    if (!url) return "";
    return '<img class="' + cls + '" src="' + url + '" alt="" loading="lazy" onerror="this.style.display=\'none\'">';
  }

  /* ================= overlay ================= */
  const view = { q: "", ab: null };
  let el = null;
  function ensureOverlay(){
    if (el) return;
    const w = document.createElement("div");
    w.id = "abilWrap"; w.className = "hidden";
    w.innerHTML =
      '<div id="abilBox" role="dialog" aria-modal="true">' +
        '<div class="ab-head"><span id="abHeadT"></span>' +
          '<button class="it-close" id="abClose" title="Close">✕</button></div>' +
        '<div class="ab-sub" id="abSub"></div>' +
        '<div class="ab-body" id="abBody"></div>' +
      "</div>";
    document.body.appendChild(w);
    el = { wrap: w, head: w.querySelector("#abHeadT"), sub: w.querySelector("#abSub"), body: w.querySelector("#abBody") };
    w.addEventListener("click", e => { if (e.target === w) closeDex(); });
    w.querySelector("#abClose").addEventListener("click", closeDex);
    document.addEventListener("keydown", e => {
      if (e.key === "Escape" && !w.classList.contains("hidden")){ e.stopPropagation(); closeDex(); }
      else if (!e.target.matches("input,select,textarea") && e.key.toLowerCase() === "y" &&
               w.classList.contains("hidden") && !menuOpenSafe()) openDex();
    }, true);
  }
  function menuOpenSafe(){ try { return typeof menuOpen === "function" ? menuOpen() : false; } catch (err) { return false; } }

  function openDex(slug){
    ensureOverlay();
    view.ab = slug && BY_SLUG[slug] ? slug : null;
    el.wrap.classList.remove("hidden");
    renderDex();
  }
  function closeDex(){ if (el) el.wrap.classList.add("hidden"); }

  /* ---------- list view ---------- */
  function renderDex(){
    el.head.textContent = t("dex_t");
    if (view.ab && BY_SLUG[view.ab]){ renderAbil(BY_SLUG[view.ab]); return; }
    el.sub.innerHTML = '<input id="abQ" type="search" autocomplete="off" spellcheck="false" placeholder="' + esc(t("search_ph")) + '">';
    el.sub.querySelector("#abQ").value = view.q;
    el.sub.querySelector("#abQ").addEventListener("input", e => { view.q = e.target.value; renderList(); });
    renderList();
  }
  function renderList(){
    const q = view.q.trim().toLowerCase();
    const arr = ABIL3.filter(a => {
      if (!q) return true;
      return (a.en + " " + a.slug + " " + a.name_fa + " " + a.eff_en).toLowerCase().indexOf(q) !== -1;
    });
    el.body.innerHTML =
      '<div class="it-count">' + esc(tpl(t("count"), { a: num(arr.length) })) + "</div>" +
      '<div class="ab-grid">' + arr.map(a =>
        '<button class="abcard" data-ab="' + a.slug + '">' +
          '<span class="ab-nm"><b>' + esc(abilName(a)) + "</b>" +
            (abilNameAlt(a) ? "<i>" + esc(abilNameAlt(a)) + "</i>" : "") + "</span>" +
          '<span class="ab-eff">' + esc(abilEffect(a)) + "</span>" +
          '<span class="ab-meta">' + num(userCount(a.slug)) + "</span>" +
        "</button>").join("") + "</div>" +
      (arr.length ? "" : '<div class="mv-note">' + esc(t("no_results")) + "</div>") +
      '<div class="mv-note">' + esc(t("era_note")) + "</div>";
    el.body.querySelectorAll(".abcard").forEach(c =>
      c.addEventListener("click", () => { view.ab = c.dataset.ab; renderDex(); }));
    const first = el.body.querySelector(".abcard");
    if (first) first.focus();
  }

  /* ---------- ability view: effect + slot-1/slot-2 mon lists ---------- */
  function renderAbil(a){
    el.head.textContent = t("dex_t");
    el.sub.innerHTML =
      '<button class="it-back" id="abBack">◂ ' + esc(t("dex_t")) + "</button>";
    el.sub.querySelector("#abBack").addEventListener("click", () => { view.ab = null; renderDex(); });
    const n = userCount(a.slug);
    let h =
      '<div class="ab-ltitle"><b>' + esc(abilName(a)) + "</b>" +
        (abilNameAlt(a) ? "<i>" + esc(abilNameAlt(a)) + "</i>" : "") + "</div>" +
      '<div class="ab-effbig"><span class="ab-eff-k">' + esc(t("effect_t")) + "</span>" +
        '<p class="d-fa">' + esc(a.eff_fa) + "</p>" +
        '<p class="d-en">' + esc(a.eff_en) + "</p></div>";
    if (!n){
      h += '<div class="mv-note ab-unused">' + esc(t("unused")) + "</div>";
    } else {
      const chips = ids => ids.map(id =>
        '<button class="ab-mon" data-id="' + id + '" title="' + esc(monName(id)) + '">' +
          sprImg(id, "ab-spr") + "<span>" + esc(monName(id)) + "</span></button>").join("");
      if (USERS[a.slug].s1.length)
        h += '<div class="ab-sec"><div class="ab-sec-t">' + esc(t("slot1")) +
          ' <i>' + esc(tpl(t("mons"), { a: num(USERS[a.slug].s1.length) })) + "</i></div>" +
          '<div class="ab-mons">' + chips(USERS[a.slug].s1) + "</div></div>";
      if (USERS[a.slug].s2.length)
        h += '<div class="ab-sec"><div class="ab-sec-t">' + esc(t("slot2")) +
          ' <i>' + esc(tpl(t("mons"), { a: num(USERS[a.slug].s2.length) })) + "</i></div>" +
          '<div class="ab-mons">' + chips(USERS[a.slug].s2) + "</div></div>";
      h += '<div class="mv-note">' + esc(t("users_t")) + "</div>";
    }
    el.body.innerHTML = h;
    el.body.querySelectorAll(".ab-mon").forEach(b => b.addEventListener("click", () => {
      closeDex();
      try { select(parseInt(b.dataset.id, 10)); } catch (e) {}
    }));
  }

  /* ================= START menu + language ================= */
  function injectMenu(){
    const pop = document.getElementById("menuPop");
    if (!pop || pop.querySelector("[data-act=abildex]")) return;
    const ref = pop.querySelector("[data-act=locdex]") || pop.querySelector(".m-sep");
    const b = document.createElement("button");
    b.className = "m-item"; b.dataset.act = "abildex";
    b.innerHTML = '<span class="mi">&#127919;</span><span class="ab-menu-l" data-key="menu_abilities"></span>';
    pop.insertBefore(b, ref ? ref.nextSibling : null);
    pop.addEventListener("click", e => {
      const it = e.target.closest(".m-item");
      if (it && it.dataset.act === "abildex") openDex();
    });
  }
  function applyLang(){
    document.querySelectorAll(".ab-menu-l").forEach(s => { s.textContent = t(s.dataset.key); });
    const c = document.getElementById("abClose");
    if (c) c.title = t("close");
    if (el && !el.wrap.classList.contains("hidden")) renderDex();
  }
  injectMenu();
  ensureOverlay();

  return { openDex, closeDex, applyLang };
})();
