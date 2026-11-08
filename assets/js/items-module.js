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
      pockets: { ball: "BALLS", item: "ITEMS", key: "KEY ITEMS", berry: "BERRIES" },
      buy: "BUY", sell: "SELL", not_sold: "NOT FOR SALE",
      desc_t: "DESCRIPTION",
      no_desc_g1: "Generation I items had no in-game descriptions.",
      g1_only: "This item exists only in Generation I.",
      hold_mark: "HOLD", games_t: "APPEARS IN",
      g_names: { b: "RED/BLUE", y: "YELLOW", g: "GOLD/SILVER", c: "CRYSTAL",
                 r: "RUBY", s: "SAPPHIRE", e: "EMERALD", f: "FIRERED", l: "LEAFGREEN" },
      g_groups: { rs: "R/S", e: "EMERALD", frlg: "FRLG" },
      icons_gb: "ICONS: GB", icons_color: "ICONS: COLOR",
      menu_items: "Item Dex", tm_note: "Machines (TMs & HMs) live in the TM/HM list of the Moves Dex.",
      gen1_note: "Prices are the Red/Blue prices of this page's generation.",
      icons_note: "The Gen-3 games had color item art everywhere — the icons are always the color menu icons, with no GB switch.",
      wording_of: "{g} wording",
      price_in: "{g} price",
      fl_t: "FLAVORS", firm_t: "FIRMNESS",
      fl: { spicy: "SPICY", dry: "DRY", sweet: "SWEET", bitter: "BITTER", sour: "SOUR" },
      firm: { very_soft: "Very soft", soft: "Soft", hard: "Hard", very_hard: "Very hard",
              super_hard: "Super hard", unknown: "Unknown (E-Reader berry)" }
    },
    fa: {
      dex_t: "دکس آیتم", close: "بستن", back: "◂ بازگشت",
      search_ph: "جست‌وجوی آیتم…", no_results: "آیتمی پیدا نشد.",
      count: "{a} آیتم", all: "همه",
      cats: { ball: "توپ‌ها", heal: "داروها", vitamin: "ویتامین‌ها", battle: "نبرد",
              stone: "سنگ‌ها", berry: "توت‌ها", apricorn: "آپریکورن‌ها", held: "آیتم‌های همراه",
              mail: "نامه‌ها", treasure: "گنجینه‌ها", rod: "ماهیگیری", key: "آیتم‌های کلیدی", misc: "متفرقه" },
      pockets: { ball: "توپ‌ها", item: "آیتم‌ها", key: "کلیدی", berry: "توت‌ها" },
      buy: "خرید", sell: "فروش", not_sold: "فروشی نیست",
      desc_t: "توضیحات",
      no_desc_g1: "آیتم‌های نسل اول در بازی توضیح نداشتند.",
      g1_only: "این آیتم فقط در نسل اول وجود دارد.",
      hold_mark: "همراه", games_t: "موجود در",
      g_names: { b: "قرمز/آبی", y: "زرد", g: "گلد/سیلور", c: "کریستال",
                 r: "یاقوت", s: "یاقوت کبود", e: "زمرد", f: "آتشین", l: "برگ سبز" },
      g_groups: { rs: "یاقوت/یاقوت کبود", e: "زمرد", frlg: "آتشین/برگ سبز" },
      icons_gb: "آیکون: گیم‌بوی", icons_color: "آیکون: رنگی",
      menu_items: "دکس آیتم", tm_note: " ماشین‌ها (TM و HM) در لیست TM/HM دکس حرکت‌ها هستند.",
      gen1_note: "قیمت‌ها مربوط به نسل همین صفحه است.",
      icons_note: "بازی‌های نسل سوم همه‌جا آیتم رنگی داشتند — آیکون‌ها همیشه آیکون منوی رنگی‌اند و کلید گیم‌بوی ندارند.",
      wording_of: "واژگان {g}",
      price_in: "قیمت در {g}",
      fl_t: "طعم‌ها", firm_t: "سختی",
      fl: { spicy: "تندی", dry: "خشکی", sweet: "شیرینی", bitter: "تلخی", sour: "ترشی" },
      firm: { very_soft: "خیلی نرم", soft: "نرم", hard: "سخت", very_hard: "خیلی سخت",
              super_hard: "فوق‌سخت", unknown: "نامعلوم (توت ای‌ریدر)" }
    }
  };

  const CFG = window.ITEM_DEX_CONFIG || null;
  if (!CFG || typeof ITEMS === "undefined") {
    return { applyLang(){}, setGroup(){} };
  }
  /* Gen 3: item art was always color — no GB/COLOR switch. The page
     declares CFG.fixed = "color" and CFG.gen = 3. */
  const IS_G3 = CFG.gen === 3;

  /* ================= helpers ================= */
  const store = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k) || "null"); return v === null ? d : v; } catch(e){ return d; } };
  const save = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch(e){} };
  const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const faD = n => String(n).replace(/[0-9]/g, d => "۰۱۲۳۴۵۶۷۸۹"[+d]);
  const lang = () => (typeof state !== "undefined" && state.lang) || "en";
  const num = n => lang() === "fa" ? faD(n) : String(n);
  const t = k => k.split(".").reduce((o,p)=>o&&o[p], II18N[lang()]) || k.split(".").reduce((o,p)=>o&&o[p], II18N.en);
  const tpl = (s,o) => s.replace(/\{(\w+)\}/g, (_,k)=> o[k] !== undefined ? o[k] : "{"+k+"}");

  const view = { item: null, q: "", cat: null,
                 icons: CFG.fixed ? CFG.fixed : store("pkd_itemicons", CFG.icons),
                 group: CFG.activeGroup || null };
  const itemsOfGame = ITEMS.filter(it => CFG.games.split("").some(g => it.g.indexOf(g) !== -1));

  /* price of the ACTIVE cartridge group (gen 3: rs | e | frlg — the page
     swaps it on theme change via ItemsUI.setGroup) */
  function activeGroup(){
    if (!IS_G3) return null;
    return view.group || "rs";
  }
  function priceOf(it){
    if (IS_G3){
      const grp = activeGroup();
      if (it.p && typeof it.p === "object") return it.p[grp] !== undefined ? it.p[grp] : 0;
      return it.p1 || 0;
    }
    return CFG.gen === 1 ? it.p1 : it.p2;
  }
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
    if (!CFG.fixed) syncIcons(true);   /* icon style follows the page (gen 1/2 only) */
    el.wrap.classList.remove("hidden");
    renderDex();
  }
  function closeDex(){ if (el) el.wrap.classList.add("hidden"); }
  /* icon style follows the MONO/COLOR sprite switch of the page
     (pages set window.__itemIconHint; gen 3 is fixed-color and ignores it) */
  function syncIcons(quiet){
    if (CFG.fixed) return;
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
        (CFG.fixed ? "" :
          '<button class="it-style" id="itStyle">' + esc(view.icons === "gb" ? t("icons_gb") : t("icons_color")) + "</button>") +
      "</div>";
    el.sub.querySelector("#itQ").value = view.q;
    el.sub.querySelector("#itQ").addEventListener("input", e => {
      view.q = e.target.value; renderList();
    });
    el.sub.querySelectorAll(".it-chip").forEach(b => b.addEventListener("click", () => {
      view.cat = b.dataset.c === "all" ? null : b.dataset.c; renderDex();
    }));
    if (!CFG.fixed){
      el.sub.querySelector("#itStyle").addEventListener("click", () => {
        view.icons = view.icons === "gb" ? "color" : "gb";
        save("pkd_itemicons", view.icons);
        renderDex();
      });
    }
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
      '<div class="it-note">' + esc(t("tm_note")) + "</div>" +
      (CFG.fixed ? '<div class="it-note">' + esc(t("icons_note")) + "</div>" : "");
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
  /* the wording the ACTIVE cartridge reads (falls back to the first
     group the item exists in, labelled honestly) */
  function wordingOf(it){
    const groups = Object.keys(it.d);           /* rs, e, frlg — insertion order */
    const grp = IS_G3 ? (activeGroup() || groups[0]) : groups[0];
    if (it.d[grp]) return { grp: grp, text: it.d[grp], own: true };
    return { grp: groups[0], text: it.d[groups[0]], own: false };
  }
  function faWordingOf(it, grp){
    if (!it.f) return null;
    if (it.f[grp]) return it.f[grp];
    const first = Object.keys(it.f)[0];
    return it.f[first];
  }
  function flavorRow(it){
    const fl = it.fl;
    if (!fl) return "";
    const keys = ["spicy","dry","sweet","bitter","sour"];
    return '<div class="id-flavors"><div class="mv-sec-t">' + esc(t("fl_t")) + "</div>" +
      keys.map(k =>
        '<div class="id-fl"><span class="id-fl-k">' + esc(t("fl." + k)) + "</span>" +
        '<span class="id-fl-bar"><i style="width:' + Math.round(fl[k] / 40 * 100) + '%"></i></span>' +
        '<span class="id-fl-v">' + num(fl[k]) + "</span></div>").join("") +
      (it.firm ? '<div class="id-fl id-firm"><span class="id-fl-k">' + esc(t("firm_t")) + "</span>" +
        '<span class="id-fl-v">' + esc(t("firm." + it.firm)) + "</span></div>" : "") +
      "</div>";
  }
  function renderDetail(it){
    const sell = p => p ? Math.floor(p / 2) : 0;
    let statsHtml = "";
    let descHtml = "";
    let gamesHtml = "";
    if (IS_G3){
      /* buy/sell per cartridge GROUP — each cart keeps its own price */
      const groups = ["rs", "e", "frlg"].filter(g =>
        it.p && it.p[g] !== undefined);
      statsHtml = groups.map(g =>
        '<div class="id-statrow">' +
          '<span class="id-stat-g">' + esc(t("g_groups." + g)) + "</span>" +
          '<span class="id-stat"><i>' + esc(t("buy")) + "</i><b>" +
            (it.p[g] ? "¥" + num(it.p[g]) : "—") + "</b></span>" +
          '<span class="id-stat"><i>' + esc(t("sell")) + "</i><b>" +
            (sell(it.p[g]) ? "¥" + num(sell(it.p[g])) : "—") + "</b></span>" +
        "</div>").join("");
      /* per-game availability chips — only the five Gen-3 games */
      const codes = ["r","s","e","f","l"].filter(g => CFG.games.indexOf(g) !== -1);
      gamesHtml = codes.map(g =>
        '<span class="id-gchip' + (it.g.indexOf(g) !== -1 ? " on" : "") + '">' +
        esc(t("g_names." + g)) + "</span>").join("");
      /* the cartridge's own wording */
      const w = wordingOf(it);
      const fa = faWordingOf(it, w.grp) || "";
      const lbl = w.own ? "" :
        '<div class="id-wording">' + esc(tpl(t("wording_of"), {g: t("g_groups." + w.grp)})) + "</div>";
      descHtml = '<div class="id-desc"><div class="mv-sec-t">' + esc(t("desc_t")) + "</div>" + lbl +
        '<p class="d-fa">' + esc(fa) + "</p>" +
        '<p class="d-en">' + esc(w.text) + "</p></div>";
    } else {
      const p = priceOf(it);
      statsHtml =
        '<span class="id-stat"><i>' + esc(t("buy")) + "</i><b>" + (p ? "¥" + num(p) : "—") + "</b></span>" +
        '<span class="id-stat"><i>' + esc(t("sell")) + "</i><b>" + (sell(p) ? "¥" + num(sell(p)) : "—") + "</b></span>";
      /* availability chips — only the games this dex covers
         (the Gen-1 dex shows RED/BLUE and YELLOW, never Gen-2 games) */
      const gChips = ["b","y","g","c"].filter(g => CFG.games.indexOf(g) !== -1).map(g =>
        '<span class="id-gchip' + (it.g.indexOf(g) !== -1 ? " on" : "") + '">' + esc(t("g_names." + g)) + "</span>").join("");
      gamesHtml = gChips;
      descHtml = it.d
        ? '<div class="id-desc"><div class="mv-sec-t">' + esc(t("desc_t")) + "</div>" +
          '<p class="d-fa">' + esc(it.fa2) + "</p>" +
          '<p class="d-en">' + esc(it.d) + "</p></div>"
        : '<div class="id-desc"><div class="mv-sec-t">' + esc(t("desc_t")) + "</div>" +
          '<p class="d-fa" style="margin:0;color:var(--ink-faint)">' + esc(t("g1_only") ) + " " + esc(t("no_desc_g1")) + "</p></div>";
    }
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
        '<div class="id-stats' + (IS_G3 ? " id-stats-g3" : "") + '">' + statsHtml + "</div>" +
        descHtml +
        flavorRow(it) +
        '<div class="mv-sec-t">' + esc(t("games_t")) + "</div>" +
        '<div class="id-games">' + gamesHtml + "</div>" +
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
  /* the ACTIVE cartridge group (rs | e | frlg) — gen3.js calls this on
     every theme change, like MovesUI.setGame; the overlay re-renders if open */
  function setGroup(grp){
    if (!IS_G3 || !grp || grp === view.group) return;
    view.group = grp;
    if (el && !el.wrap.classList.contains("hidden")) renderDex();
  }
  injectMenu();
  ensureOverlay();   /* register the I-key shortcut before the first open */

  return { openDex, closeDex, applyLang, syncIcons, setGroup };
})();
