"use strict";
/* Pokédex Plus — ITEM DEX module (Phase 3)
   ============================================================
   Loaded AFTER items-data.js (ITEMS + ITEM_CATS) on the Gen-1/2 dex
   pages. The page declares itself BEFORE this file runs:

     window.ITEM_DEX_CONFIG = {
       games: "by" | "gc",       // which releases this page covers
       label: "R/B/Y",           // shown in the overlay head
       gen:   1 | 2,             // which price column to show
       icons: "gb" | "color"     // default icon style
     };

   Adds:
     · START-menu entry + `I` key: the ITEM DEX overlay
     · Grid of every bag item of that game (machines stay in the TM/HM
       list) — search EN/FA, category chips, GB/COLOR icon toggle
     · Item cards: authentic in-game name (EN + FA), bag pocket, buy and
       sell price of that game, the authentic G/S/C description (EN + FA),
       hold badge and a per-game availability row

   Historical accuracy (per project philosophy):
     · item lists, names, prices, pockets and hold flags come from the
       pret decompiles (pokered / pokecrystal)
     · Gen-1 games had no item descriptions — the wording shown is
       labelled as the Gold/Silver/Crystal text; Gen-1-only items say so
     · prices differ between generations (HYPER POTION: ¥1500 in R/B,
       ¥1200 in G/S/C) — each page shows its own generation's price
     · a dozen items never had a menu icon anywhere (GS BALL, EGG
       TICKET, …) — a dashed placeholder chip is shown instead
*/

const ItemsUI = (() => {

  /* ================= i18n ================= */
  const II18N = {
    en: {
      dex_t: "ITEM DEX", close: "Close", back: "◂ BACK",
      search_ph: "Search an item…", no_results: "No items found.",
      count: "{a} items", all: "ALL",
      cats: { ball: "Balls", heal: "Medicine", vitamin: "Vitamins", battle: "Battle",
              stone: "Stones", berry: "Berries", apricorn: "Apricorns", held: "Held items",
              mail: "Mail", treasure: "Treasures", rod: "Rods", key: "Key items", misc: "Misc" },
      pockets: { ball: "BALLS", item: "ITEMS", key: "KEY ITEMS" },
      buy: "BUY", sell: "SELL", not_sold: "NOT FOR SALE",
      desc_t: "DESCRIPTION",
      no_desc_g1: "Generation I items had no in-game descriptions.",
      g1_only: "This item exists only in Generation I.",
      hold_mark: "HOLD", games_t: "APPEARS IN",
      g_names: { b: "RED/BLUE", y: "YELLOW", g: "GOLD/SILVER", c: "CRYSTAL" },
      icons_gb: "ICONS: GB", icons_color: "ICONS: COLOR",
      menu_items: "Item Dex", tm_note: "Machines (TMs & HMs) live in the TM/HM list of the Moves Dex.",
      gen1_note: "Prices are the Red/Blue prices of this page's generation."
    },
    fa: {
      dex_t: "دکس آیتم", close: "بستن", back: "◂ بازگشت",
      search_ph: "جست‌وجوی آیتم…", no_results: "آیتمی پیدا نشد.",
      count: "{a} آیتم", all: "همه",
      cats: { ball: "توپ‌ها", heal: "داروها", vitamin: "ویتامین‌ها", battle: "نبرد",
              stone: "سنگ‌ها", berry: "توت‌ها", apricorn: "آپریکورن‌ها", held: "آیتم‌های همراه",
              mail: "نامه‌ها", treasure: "گنجینه‌ها", rod: "ماهیگیری", key: "آیتم‌های کلیدی", misc: "متفرقه" },
      pockets: { ball: "توپ‌ها", item: "آیتم‌ها", key: "کلیدی" },
      buy: "خرید", sell: "فروش", not_sold: "فروشی نیست",
      desc_t: "توضیحات",
      no_desc_g1: "آیتم‌های نسل اول در بازی توضیح نداشتند.",
      g1_only: "این آیتم فقط در نسل اول وجود دارد.",
      hold_mark: "همراه", games_t: "موجود در",
      g_names: { b: "قرمز/آبی", y: "زرد", g: "گلد/سیلور", c: "کریستال" },
      icons_gb: "آیکون: گیم‌بوی", icons_color: "آیکون: رنگی",
      menu_items: "دکس آیتم", tm_note: " ماشین‌ها (TM و HM) در لیست TM/HM دکس حرکت‌ها هستند.",
      gen1_note: "قیمت‌ها مربوط به نسل همین صفحه است."
    }
  };

  const CFG = window.ITEM_DEX_CONFIG || null;
  if (!CFG || typeof ITEMS === "undefined") {
    return { applyLang(){} };
  }

  /* ================= helpers ================= */
  const store = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k) || "null"); return v === null ? d : v; } catch(e){ return d; } };
  const save = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch(e){} };
  const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const faD = n => String(n).replace(/[0-9]/g, d => "۰۱۲۳۴۵۶۷۸۹"[+d]);
  const lang = () => (typeof state !== "undefined" && state.lang) || "en";
  const num = n => lang() === "fa" ? faD(n) : String(n);
  const t = k => k.split(".").reduce((o,p)=>o&&o[p], II18N[lang()]) || k.split(".").reduce((o,p)=>o&&o[p], II18N.en);
  const tpl = (s,o) => s.replace(/\{(\w+)\}/g, (_,k)=> o[k] !== undefined ? o[k] : "{"+k+"}");

  const view = { item: null, q: "", cat: null, icons: store("pkd_itemicons", CFG.icons) };
  const itemsOfGame = ITEMS.filter(it => CFG.games.split("").some(g => it.g.indexOf(g) !== -1));

  function priceOf(it){ return CFG.gen === 1 ? it.p1 : it.p2; }
  function iconPath(it){
    if (!it.i) return "";
    return (view.icons === "gb" ? "assets/itemicons-gb/" : "assets/itemicons/") + it.i + ".png";
  }
  /* icon <img> — in COLOR mode an item without a coloured icon
     falls back to its GB icon (like sprites: colour when it has it) */
  function iconImg(it, cls){
    if (!it.i) return '<span class="ph"></span>';
    if (view.icons !== "gb"){
      return '<img class="' + cls + '" src="' + iconPath(it) + '" data-gb="assets/itemicons-gb/' + it.i + '.png"' +
        ' onerror="this.onerror=null;this.src=this.dataset.gb" alt="">';
    }
    return '<img class="' + cls + '" src="' + iconPath(it) + '" alt="">';
  }
  function nameEN(it){
    if (lang() === "fa") return it.en;
    return (CFG.gen === 1 && it.en1) ? it.en1 : it.en;
  }
  function nameFA(it){ return it.fa || it.en; }

  /* ================= overlay chrome ================= */
  let el = null;
  function ensureOverlay(){
    if (el) return;
    const w = document.createElement("div");
    w.id = "itemsWrap"; w.className = "hidden";
    w.innerHTML =
      '<div id="itemsBox" role="dialog" aria-modal="true">' +
        '<div class="it-head"><span id="itHeadT"></span>' +
          '<button class="it-close" id="itClose" title="Close">✕</button></div>' +
        '<div class="it-sub" id="itSub"></div>' +
        '<div class="it-body" id="itBody"></div>' +
      "</div>";
    document.body.appendChild(w);
    el = { wrap: w, head: w.querySelector("#itHeadT"), sub: w.querySelector("#itSub"), body: w.querySelector("#itBody") };
    w.addEventListener("click", e => { if (e.target === w) closeDex(); });
    w.querySelector("#itClose").addEventListener("click", closeDex);
    document.addEventListener("keydown", e => {
      if (e.key === "Escape" && !w.classList.contains("hidden")){ e.stopPropagation(); closeDex(); }
      else if (!e.target.matches("input,select,textarea") && e.key.toLowerCase() === "i" &&
               w.classList.contains("hidden") && !menuOpenSafe()) openDex();
    }, true);
  }
  function menuOpenSafe(){ try { return typeof menuOpen === "function" ? menuOpen() : false; } catch (err){ return false; } }

  function openDex(){
    ensureOverlay();
    syncIcons(true);          /* icons follow the page's sprite colour mode */
    el.wrap.classList.remove("hidden");
    renderDex();
  }
  function closeDex(){ if (el) el.wrap.classList.add("hidden"); }
  /* icon style follows the MONO/COLOR sprite switch of the page
     (pages set window.__itemIconHint; others keep their default) */
  function syncIcons(quiet){
    if (typeof window.__itemIconHint !== "function") return;
    const v = window.__itemIconHint();
    if ((v === "gb" || v === "color") && v !== view.icons){
      view.icons = v;
      save("pkd_itemicons", v);
      if (!quiet && el && !el.wrap.classList.contains("hidden")) renderDex();
    }
  }

  /* ================= list view ================= */
  function renderDex(){
    el.head.textContent = t("dex_t") + " · " + CFG.label;
    /* controls */
    const cats = ["all"].concat(ITEM_CATS.filter(c => itemsOfGame.some(it => it.cat === c)));
    el.sub.innerHTML =
      '<input id="itQ" type="search" autocomplete="off" spellcheck="false" placeholder="' + esc(t("search_ph")) + '">' +
      '<div class="it-chiprow">' +
        cats.map(c => '<button class="it-chip' + (view.cat === c || (c === "all" && !view.cat) ? " on" : "") +
          '" data-c="' + c + '">' + esc(c === "all" ? t("all") : t("cats." + c)) + "</button>").join("") +
        '<button class="it-style" id="itStyle">' + esc(view.icons === "gb" ? t("icons_gb") : t("icons_color")) + "</button>" +
      "</div>";
    el.sub.querySelector("#itQ").value = view.q;
    el.sub.querySelector("#itQ").addEventListener("input", e => {
      view.q = e.target.value; renderList();
    });
    el.sub.querySelectorAll(".it-chip").forEach(b => b.addEventListener("click", () => {
      view.cat = b.dataset.c === "all" ? null : b.dataset.c; renderDex();
    }));
    el.sub.querySelector("#itStyle").addEventListener("click", () => {
      view.icons = view.icons === "gb" ? "color" : "gb";
      save("pkd_itemicons", view.icons);
      renderDex();
    });
    renderList();
  }

  function renderList(){
    const q = view.q.trim().toLowerCase();
    let arr = itemsOfGame.filter(it => {
      if (view.cat && it.cat !== view.cat) return false;
      if (q && (it.en + " " + (it.en1 || "") + " " + it.fa).toLowerCase().indexOf(q) === -1) return false;
      return true;
    });
    el.body.innerHTML =
      '<div class="it-count">' + esc(tpl(t("count"), {a: num(arr.length)})) + "</div>" +
      (view.item ? '<button class="it-back" id="itBack">' + esc(t("back")) + "</button>" : "") +
      '<div class="igrid">' + arr.map(cardHtml).join("") + "</div>" +
      (arr.length ? "" : '<div class="it-note">' + esc(t("no_results")) + "</div>") +
      '<div class="it-note">' + esc(t("tm_note")) + "</div>";
    if (view.item){
      el.body.querySelector("#itBack").addEventListener("click", () => { view.item = null; renderDex(); });
    }
    el.body.querySelectorAll(".icard").forEach(c =>
      c.addEventListener("click", () => { view.item = c.dataset.k; renderDex(); }));
    const first = el.body.querySelector(".icard");
    if (first) first.focus();
  }

  function cardHtml(it){
    return '<button class="icard" data-k="' + it.k + '">' +
      '<span class="icard-top">' +
        '<span class="icard-ic">' + iconImg(it, "icn") + "</span>" +
        '<span class="icard-nm">' +
          '<span class="icard-en">' + esc(nameEN(it)) + "</span>" +
          '<span class="icard-fa">' + esc(nameFA(it)) + "</span>" +
        "</span>" +
      "</span>" +
      '<span class="icard-meta">' +
        '<span class="it-price">' + (priceOf(it) ? "¥" + num(priceOf(it)) : esc(t("not_sold"))) + "</span>" +
        '<span class="it-pk-badge ' + it.pk + '">' + esc(t("pockets." + it.pk)) + "</span>" +
      "</span>" +
    "</button>";
  }

  /* ================= detail view ================= */
  function renderDetail(it){
    const p = priceOf(it);
    const sell = p ? Math.floor(p / 2) : 0;
    /* availability chips — only the games this dex covers
       (the Gen-1 dex shows RED/BLUE and YELLOW, never Gen-2 games) */
    const gChips = ["b","y","g","c"].filter(g => CFG.games.indexOf(g) !== -1).map(g =>
      '<span class="id-gchip' + (it.g.indexOf(g) !== -1 ? " on" : "") + '">' + esc(t("g_names." + g)) + "</span>").join("");
    const descHtml = it.d
      ? '<div class="id-desc"><div class="mv-sec-t">' + esc(t("desc_t")) + "</div>" +
        '<p class="d-fa">' + esc(it.fa2) + "</p>" +
        '<p class="d-en">' + esc(it.d) + "</p></div>"
      : '<div class="id-desc"><div class="mv-sec-t">' + esc(t("desc_t")) + "</div>" +
        '<p class="d-fa" style="margin:0;color:var(--ink-faint)">' + esc(t("g1_only") ) + " " + esc(t("no_desc_g1")) + "</p></div>";
    el.body.innerHTML =
      '<button class="it-back" id="itBack">' + esc(t("back")) + "</button>" +
      '<div class="id-card">' +
        '<div class="id-head">' +
          '<span class="id-ic">' + iconImg(it, "icn") + "</span>" +
          '<span class="id-name">' +
            '<span class="mv-fa big">' + esc(nameFA(it)) + "</span>" +
            '<span class="mv-en big">' + esc(nameEN(it)) + "</span>" +
          "</span>" +
          '<span class="id-meta">' +
            '<span class="it-cat">' + esc(t("cats." + it.cat)) + "</span>" +
            (it.hold ? '<span class="it-hold">' + esc(t("hold_mark")) + "</span>" : "") +
            '<span class="it-pk-badge ' + it.pk + '">' + esc(t("pockets." + it.pk)) + "</span>" +
          "</span>" +
        "</div>" +
        '<div class="id-stats">' +
          '<span class="id-stat"><i>' + esc(t("buy")) + "</i><b>" + (p ? "¥" + num(p) : "—") + "</b></span>" +
          '<span class="id-stat"><i>' + esc(t("sell")) + "</i><b>" + (sell ? "¥" + num(sell) : "—") + "</b></span>" +
        "</div>" +
        descHtml +
        '<div class="mv-sec-t">' + esc(t("games_t")) + "</div>" +
        '<div class="id-games">' + gChips + "</div>" +
      "</div>";
    el.body.querySelector("#itBack").addEventListener("click", () => { view.item = null; renderDex(); });
  }

  /* patch renderList to route to the detail view */
  const _renderList = renderList;
  renderList = function(){
    if (view.item){
      const it = ITEMS.find(x => x.k === view.item);
      if (it){ renderDetail(it); return; }
      view.item = null;
    }
    _renderList();
  };

  /* ================= START menu + language ================= */
  function injectMenu(){
    const pop = document.getElementById("menuPop");
    if (!pop || pop.querySelector("[data-act=itemsdex]")) return;
    const sep = pop.querySelector(".m-sep") || pop.querySelector("[data-act=reset]");
    const b = document.createElement("button");
    b.className = "m-item"; b.dataset.act = "itemsdex";
    b.innerHTML = '<span class="mi">&#128230;</span><span class="it-menu-l" data-key="menu_items"></span>';
    pop.insertBefore(b, sep);
    pop.addEventListener("click", e => {
      const it = e.target.closest(".m-item");
      if (it && it.dataset.act === "itemsdex") openDex();
    });
  }
  function applyLang(){
    document.querySelectorAll(".it-menu-l").forEach(s => { s.textContent = t(s.dataset.key); });
    const c = document.getElementById("itClose");
    if (c) c.title = t("close");
    if (el && !el.wrap.classList.contains("hidden")) renderDex();
  }
  injectMenu();
  ensureOverlay();   /* register the I-key shortcut before the first open */

  return { openDex, closeDex, applyLang, syncIcons };
})();
