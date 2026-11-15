(function () {
  "use strict";

  var V = window.VISTO;
  var RO = window.VISTO_RO;
  var LANG_KEY = "visto.lang";
  var LANGS = ["en", "ro"];
  var page = document.body.getAttribute("data-page") || "";

  // ---------- icons (stroke icons, 24x24) ----------
  var ICON_PATHS = {
    search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
    close: '<path d="M6 6l12 12M18 6 6 18"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    grid: '<rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5"/>',
    folder: '<path d="M3.5 7.5a2 2 0 0 1 2-2h4l2 2.5h7a2 2 0 0 1 2 2v7.5a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"/>',
    layers: '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 12.5 9 5 9-5"/><path d="m3 16.5 9 5 9-5"/>',
    heart: '<path d="M12 20s-7.5-4.6-7.5-10.1A4.4 4.4 0 0 1 12 7a4.4 4.4 0 0 1 7.5 2.9C19.5 15.4 12 20 12 20z"/>',
    briefcase: '<rect x="3.5" y="7" width="17" height="12.5" rx="2"/><path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7M3.5 12.5h17"/>',
    monitor: '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M12 16v4M8 20h8"/>',
    refresh: '<path d="M20 11a8 8 0 0 0-14.3-4.9L4 8"/><path d="M4 4v4h4"/><path d="M4 13a8 8 0 0 0 14.3 4.9L20 16"/><path d="M20 20v-4h-4"/>',
    zap: '<path d="M13 3 5 13.5h6L10 21l8-10.5h-6z"/>',
    shield: '<path d="M12 3 5 6v5.5c0 4.3 3 8 7 9.5 4-1.5 7-5.2 7-9.5V6z"/><path d="m9 12 2 2 4-4"/>',
    mail: '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="m4 7.5 8 6 8-6"/>',
    message: '<path d="M5 5h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-8l-5 4v-4H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z"/>',
    handshake: '<path d="m11 17 2 2a1.4 1.4 0 0 0 2-2"/><path d="m14 14 2.5 2.5a1.4 1.4 0 0 0 2-2l-3.9-3.9a2.8 2.8 0 0 0-4 0l-.9.9a1.4 1.4 0 0 1-2-2l2.8-2.8a3.9 3.9 0 0 1 4.6-.7l.5.3a3 3 0 0 0 2.2.4L21 6"/><path d="m21 15-1-1M3 6l1.2.5a3 3 0 0 0 2.2.1L9 5.5"/><path d="m3 15 6.5 6.5a1.4 1.4 0 0 0 2-2L8 16"/>',
    copy: '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/>'
  };
  function icon(name, cls) {
    return '<svg class="icon ' + (cls || "") + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICON_PATHS[name] + "</svg>";
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // ---------- language ----------
  function storageGet(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function storageSet(k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* private mode */ } }

  function initialLang() {
    var q = new URLSearchParams(window.location.search).get("lang");
    if (LANGS.indexOf(q) >= 0) return q;
    var saved = storageGet(LANG_KEY);
    if (LANGS.indexOf(saved) >= 0) return saved;
    var nav = (navigator.language || "en").toLowerCase();
    return nav.indexOf("ro") === 0 ? "ro" : "en";
  }
  var lang = initialLang();
  function t(obj) { return obj[lang] || obj.en; }

  // English originals captured from the HTML once, so English exists in one place.
  var originals = new Map();
  function applyStrings() {
    document.documentElement.lang = lang;
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (!originals.has(el)) originals.set(el, el.innerHTML);
      el.innerHTML = lang === "ro" && RO[key] ? RO[key] : originals.get(el);
    });
    document.querySelectorAll("[data-i18n-attr]").forEach(function (el) {
      el.getAttribute("data-i18n-attr").split(";").forEach(function (pair) {
        var parts = pair.split(":"); var attr = parts[0]; var key = parts[1];
        var store = "i18nOrig" + attr.replace(/[^a-z]/gi, "");
        if (el.dataset[store] === undefined) el.dataset[store] = el.getAttribute(attr) || "";
        el.setAttribute(attr, lang === "ro" && RO[key] ? RO[key] : el.dataset[store]);
      });
    });
    var titleKey = document.body.getAttribute("data-title-key");
    if (titleKey) {
      if (!originals.has("title")) originals.set("title", document.title);
      document.title = lang === "ro" && RO[titleKey] ? RO[titleKey] : originals.get("title");
    }
    var meta = document.querySelector('meta[name="description"]');
    var descKey = document.body.getAttribute("data-desc-key");
    if (meta && descKey) {
      if (!originals.has("desc")) originals.set("desc", meta.content);
      meta.content = lang === "ro" && RO[descKey] ? RO[descKey] : originals.get("desc");
    }
    document.querySelectorAll(".lang-switch button").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.lang === lang));
    });
  }
  function setLang(next) {
    if (next === lang || LANGS.indexOf(next) < 0) return;
    lang = next;
    storageSet(LANG_KEY, lang);
    var url = new URL(window.location.href);
    if (lang === "en") url.searchParams.delete("lang"); else url.searchParams.set("lang", lang);
    window.history.replaceState(null, "", url);
    render();
  }

  // ---------- header + footer ----------
  var NAV = [
    { id: "home", href: "index.html", key: "nav.home", label: "Home" },
    { id: "apps", href: "apps.html", key: "nav.apps", label: "Our Apps" },
    { id: "about", href: "about.html", key: "nav.about", label: "About" },
    { id: "contact", href: "contact.html", key: "nav.contact", label: "Contact" }
  ];
  function navLinks(cls) {
    return NAV.map(function (n) {
      var cur = n.id === page ? ' aria-current="page"' : "";
      return '<a class="' + cls + '" href="' + n.href + '"' + cur + ' data-i18n="' + n.key + '">' + n.label + "</a>";
    }).join("");
  }
  function langSwitch() {
    return '<div class="lang-switch" role="group" aria-label="Language" data-i18n-attr="aria-label:nav.lang">' +
      LANGS.map(function (l) { return '<button type="button" data-lang="' + l + '" aria-pressed="false">' + l.toUpperCase() + "</button>"; }).join("") +
      "</div>";
  }
  function buildHeader() {
    var host = document.getElementById("site-header");
    if (!host) return;
    host.innerHTML =
      '<div class="header-inner">' +
        '<a class="brand" href="index.html"><img src="assets/logo/visto-v-128.png" width="40" height="33" alt=""><span>Visto Apps</span></a>' +
        '<nav class="nav-pill" aria-label="Main">' + navLinks("nav-link") + "</nav>" +
        '<div class="header-actions">' + langSwitch() +
          '<button class="circle-btn search-btn" type="button" aria-label="Search apps" data-i18n-attr="aria-label:nav.search">' + icon("search") + "</button>" +
          '<button class="circle-btn menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mobile-menu" data-i18n-attr="aria-label:nav.menu">' + icon("menu") + "</button>" +
        "</div>" +
      "</div>" +
      '<div class="search-bar glass" hidden><form action="apps.html" role="search">' + icon("search") +
        '<input type="search" name="q" autocomplete="off" placeholder="Search by name or feature" aria-label="Search apps" data-i18n-attr="placeholder:apps.search;aria-label:nav.search"></form></div>' +
      '<div class="mobile-menu glass" id="mobile-menu" hidden><nav aria-label="Main">' + navLinks("mobile-link") + "</nav>" + langSwitch() + "</div>";
  }
  function buildFooter() {
    var host = document.getElementById("site-footer");
    if (!host) return;
    host.innerHTML =
      '<div class="footer-inner">' +
        '<a class="brand brand--footer" href="index.html"><img src="assets/logo/visto-v-128.png" width="36" height="30" alt=""><span>Visto Apps</span></a>' +
        '<p class="footer-tagline" data-i18n="footer.tagline">Thoughtfully designed<br>mobile applications.</p>' +
        '<nav class="footer-nav" aria-label="Footer">' + navLinks("footer-link") + "</nav>" +
        '<nav class="footer-legal-nav" aria-label="Legal">' +
          '<a class="footer-link" href="privacy.html"' + (page === "privacy" ? ' aria-current="page"' : "") + ' data-i18n="footer.privacy">Privacy Policy</a>' +
          '<a class="footer-link" href="terms.html"' + (page === "terms" ? ' aria-current="page"' : "") + ' data-i18n="footer.terms">Terms of Use</a>' +
        "</nav>" +
      "</div>" +
      '<p class="footer-legal">© ' + new Date().getFullYear() + ' Visto Apps. <span data-i18n="footer.legal">Apple, the Apple logo and iPhone are trademarks of Apple Inc.</span></p>';
  }

  function bindHeader() {
    var header = document.getElementById("site-header");
    if (!header) return;
    var menuBtn = header.querySelector(".menu-btn");
    var menu = header.querySelector(".mobile-menu");
    var searchBtn = header.querySelector(".search-btn");
    var bar = header.querySelector(".search-bar");
    var input = bar.querySelector("input");

    function closeAll() {
      menu.hidden = true; menuBtn.setAttribute("aria-expanded", "false"); menuBtn.innerHTML = icon("menu");
      if (!(document.getElementById("app-grid") && query)) bar.hidden = true;
    }
    menuBtn.addEventListener("click", function () {
      var open = menu.hidden;
      closeAll();
      if (open) { menu.hidden = false; menuBtn.setAttribute("aria-expanded", "true"); menuBtn.innerHTML = icon("close"); }
    });
    searchBtn.addEventListener("click", function () {
      var open = bar.hidden;
      closeAll();
      if (open) { bar.hidden = false; input.focus(); }
    });
    var onAppsPage = !!document.getElementById("app-grid");
    if (onAppsPage) {
      input.value = query;
      input.addEventListener("input", function () {
        query = input.value.trim();
        var url = new URL(window.location.href);
        if (query) url.searchParams.set("q", query); else url.searchParams.delete("q");
        window.history.replaceState(null, "", url);
        renderApps();
      });
      if (query) { bar.hidden = false; }
    }
    bar.querySelector("form").addEventListener("submit", function (e) {
      e.preventDefault();
      if (onAppsPage) { input.blur(); return; }
      var q = input.value.trim();
      var url = "apps.html" + (q ? "?q=" + encodeURIComponent(q) : "");
      if (lang === "ro") url += (q ? "&" : "?") + "lang=ro";
      window.location.href = url;
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeAll(); });
    document.addEventListener("click", function (e) {
      if (!header.contains(e.target)) closeAll();
    });
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }
  function bindLangSwitches() {
    document.querySelectorAll(".lang-switch button").forEach(function (b) {
      b.addEventListener("click", function () { setLang(b.dataset.lang); });
    });
  }
  // Keep ?lang=ro on internal links so the choice survives without storage.
  function decorateLinks() {
    document.querySelectorAll('a[href$=".html"], a[href*=".html?"]').forEach(function (a) {
      if (!a.dataset.baseHref) a.dataset.baseHref = a.getAttribute("href");
      var base = a.dataset.baseHref;
      if (lang === "ro") a.setAttribute("href", base + (base.indexOf("?") >= 0 ? "&" : "?") + "lang=ro");
      else a.setAttribute("href", base);
    });
  }

  // ---------- apps ----------
  var bySlug = {};
  V.apps.forEach(function (a) { bySlug[a.slug] = a; });
  function appStyle(a) { return "--c1:" + a.colors[0] + ";--c2:" + a.colors[1]; }
  function appLinkLabel(a) { return esc(a.name + ", " + (lang === "ro" ? RO["app.open"] : "Open in the App Store")); }
  function categoryOf(a) { return V.categories.filter(function (c) { return c.id === a.category; })[0]; }

  function heroCard(a, i) {
    return '<a class="hero-card" style="' + appStyle(a) + '" data-pos="' + i + '" href="' + a.store + '" target="_blank" rel="noopener" aria-label="' + appLinkLabel(a) + '">' +
      '<span class="hero-card__head"><img class="app-icon" src="assets/icons/' + a.slug + '.webp" width="64" height="64" alt="">' +
      '<span><span class="hero-card__name">' + esc(a.name) + '</span><span class="hero-card__sub">' + esc(t(a.subtitle)) + "</span></span></span>" +
      '<img class="hero-card__phone" src="assets/phones/' + a.slug + "-hero-" + lang + '.webp" width="900" height="' + PHONE_H + '" alt="">' +
      "</a>";
  }
  function tile(a) {
    return '<li><a class="app-tile" style="' + appStyle(a) + '" href="' + a.store + '" target="_blank" rel="noopener" aria-label="' + appLinkLabel(a) + '">' +
      '<img class="app-icon" src="assets/icons/' + a.slug + '.webp" width="80" height="80" alt="" loading="lazy">' +
      '<span class="app-tile__name">' + esc(a.name) + '</span><span class="app-tile__sub">' + esc(t(a.subtitle)) + "</span></a></li>";
  }
  function card(a) {
    var c = categoryOf(a);
    return '<li class="app-card-wrap" data-category="' + a.category + '"><a class="app-card" style="' + appStyle(a) + '" href="' + a.store + '" target="_blank" rel="noopener" aria-label="' + appLinkLabel(a) + '">' +
      '<span class="app-card__head"><img class="app-icon" src="assets/icons/' + a.slug + '.webp" width="64" height="64" alt="" loading="lazy">' +
        '<span class="app-card__titles"><span class="app-card__name">' + esc(a.name) + '</span><span class="app-card__sub">' + esc(t(a.subtitle)) + "</span></span>" +
        '<span class="arrow-dot">' + icon("arrow") + "</span></span>" +
      '<span class="app-card__text">' + esc(t(a.text)) + "</span>" +
      '<span class="chip">' + icon(c.icon) + esc(t(c.label)) + "</span>" +
      '<img class="app-card__phone" src="assets/phones/' + a.slug + "-" + lang + '.webp" width="900" height="' + PHONE_H + '" alt="" loading="lazy">' +
      "</a></li>";
  }
  var PHONE_H = 1139;

  function renderHome() {
    var heroHost = document.getElementById("hero-cards");
    if (heroHost) heroHost.innerHTML = V.hero.map(function (s, i) { return heroCard(bySlug[s], i); }).join("");
    document.querySelectorAll("[data-featured-tiles]").forEach(function (host) {
      host.innerHTML = V.featured.map(function (s) { return tile(bySlug[s]); }).join("");
    });
    document.querySelectorAll("[data-app-count]").forEach(function (el) { el.textContent = String(V.apps.length); });
  }

  // Apps page: filters + search
  var activeFilter = "all";
  var query = new URLSearchParams(window.location.search).get("q") || "";
  function matches(a) {
    if (activeFilter !== "all" && a.category !== activeFilter) return false;
    if (!query) return true;
    var hay = [a.name, a.subtitle.en, a.subtitle.ro, a.text.en, a.text.ro].join(" ").toLowerCase()
      .normalize("NFD").replace(/[̀-ͯ]/g, "");
    var q = query.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
    return q.split(/\s+/).every(function (w) { return hay.indexOf(w) >= 0; });
  }
  function renderApps() {
    var grid = document.getElementById("app-grid");
    if (!grid) return;
    var filters = document.getElementById("app-filters");
    var all = [{ id: "all", icon: "grid", label: { en: "All Apps", ro: RO["apps.all"] } }].concat(V.categories);
    filters.innerHTML = all.map(function (c) {
      var n = c.id === "all" ? V.apps.length : V.apps.filter(function (a) { return a.category === c.id; }).length;
      return '<button type="button" class="filter" data-filter="' + c.id + '" aria-pressed="' + (c.id === activeFilter) + '">' +
        icon(c.icon) + "<span>" + esc(t(c.label)) + ' <span class="filter__count">(' + n + ")</span></span></button>";
    }).join("");
    filters.querySelectorAll(".filter").forEach(function (b) {
      b.addEventListener("click", function () { activeFilter = b.dataset.filter; renderApps(); });
    });
    var list = V.apps.filter(matches);
    grid.innerHTML = list.map(card).join("");
    var empty = document.getElementById("app-empty");
    if (empty) empty.hidden = list.length > 0;
  }
  // ---------- contact ----------
  function renderContact() {
    document.querySelectorAll("[data-email]").forEach(function (el) {
      var subjectKey = el.getAttribute("data-subject-key");
      var subject = subjectKey ? (lang === "ro" ? RO[subjectKey] : el.getAttribute("data-subject")) : "";
      el.setAttribute("href", "mailto:" + V.email + (subject ? "?subject=" + encodeURIComponent(subject) : ""));
    });
    document.querySelectorAll("[data-email-text]").forEach(function (el) { el.textContent = V.email; });
  }
  function bindCopy() {
    var btn = document.getElementById("copy-email");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var label = btn.querySelector("[data-i18n]");
      var done = function () {
        label.textContent = lang === "ro" ? RO["contact.card.copied"] : "Address copied";
        setTimeout(function () { applyStrings(); }, 2000);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(V.email).then(done, function () {});
    });
  }

  // ---------- reveal on scroll ----------
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function bindReveal() {
    var els = document.querySelectorAll(".reveal");
    if (reduceMotion || !("IntersectionObserver" in window)) { els.forEach(function (e) { e.classList.add("is-in"); }); return; }
    els.forEach(function (e) { if (e.getBoundingClientRect().top < window.innerHeight) e.classList.add("is-in"); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    els.forEach(function (e) { io.observe(e); });
  }

  // ---------- render ----------
  function render() {
    renderHome();
    renderApps();
    renderContact();
    applyStrings();
    decorateLinks();
  }

  var backdrop = document.querySelector(".backdrop");
  if (backdrop && !backdrop.firstChild) backdrop.innerHTML = '<div class="backdrop__core"></div>';
  buildHeader();
  buildFooter();
  document.querySelectorAll("[data-icon]").forEach(function (el) { el.innerHTML = icon(el.getAttribute("data-icon")); });
  render();
  bindHeader();
  bindLangSwitches();
  bindCopy();
  bindReveal();
  document.documentElement.classList.add("js-ready");
})();
