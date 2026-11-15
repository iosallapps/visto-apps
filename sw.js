/* Visto Apps service worker. VERSION is written by tools/build.py on every build. */
const VERSION = "927618afe2";
const CORE = "visto-core-" + VERSION;
const RUNTIME = "visto-runtime-" + VERSION;
const PRECACHE = [
  "/", "/apps.html", "/about.html", "/contact.html",
  "/assets/fonts/instrument-serif.woff2", "/assets/fonts/instrument-serif-italic.woff2", "/assets/fonts/inter.woff2",
  "/assets/logo/visto-v-128.png", "/assets/bg/home.webp", "/assets/bg/home-wide.webp"
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CORE).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CORE && k !== RUNTIME).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

function isPage(req, url) {
  return req.mode === "navigate" || url.pathname.endsWith(".html") || url.pathname.endsWith("/");
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  if (isPage(req, url)) {
    // Pages: network first so edits show up, cache as the fallback (offline, slow network).
    event.respondWith(
      fetch(req).then((res) => {
        const copy = res.clone();
        caches.open(RUNTIME).then((c) => c.put(req, copy));
        return res;
      }).catch(() => caches.match(req, { ignoreSearch: true }).then((r) => r || caches.match("/")))
    );
    return;
  }

  // Versioned CSS/JS, fonts and images: cache first, they never change under the same URL.
  event.respondWith(
    caches.match(req).then((hit) => hit || fetch(req).then((res) => {
      if (res.ok) { const copy = res.clone(); caches.open(RUNTIME).then((c) => c.put(req, copy)); }
      return res;
    }))
  );
});
