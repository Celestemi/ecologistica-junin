const PREFIX = "eco-shell-";
const CACHE = `${PREFIX}__BUILD_VERSION__`;
const BUILD_ASSETS = /* __PRECACHE_ASSETS__ */ [];
const SHELL = ["/", "/manifest.webmanifest", ...BUILD_ASSETS];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(
    SHELL.map((url) => new Request(url, { cache: "reload" })),
  )));
  // Existing tabs finish with their current build before an update activates.
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter((key) => key.startsWith(PREFIX) && key !== CACHE)
      .map((key) => caches.delete(key)));
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== "GET" || url.origin !== self.location.origin
      || request.headers.has("Authorization")) return;

  const shellPath = url.pathname === "/" || ["/ingresar", "/conductor", "/seguimiento", "/pedidos", "/flota", "/auditoria"]
    .some((path) => url.pathname === path || url.pathname.startsWith(`${path}/`));
  if (request.mode === "navigate" && shellPath) {
    event.respondWith(fetch(request).catch(async () => {
      const cache = await caches.open(CACHE);
      const shell = await cache.match("/");
      return shell || Response.error();
    }));
    return;
  }

  // Only public build assets are eligible; APIs and map tiles bypass this cache.
  if (!url.pathname.startsWith("/assets/") && url.pathname !== "/manifest.webmanifest") return;
  const response = (async () => {
    const cache = await caches.open(CACHE);
    const cached = await cache.match(request);
    if (cached) return cached;
    const fresh = await fetch(request);
    if (fresh.ok && !fresh.redirected && !fresh.headers.get("Content-Type")?.includes("text/html")
        && !/no-store|private/i.test(fresh.headers.get("Cache-Control") || "")) {
      await cache.put(request, fresh.clone());
    }
    return fresh;
  })();
  event.respondWith(response);
  event.waitUntil(response.then(() => undefined).catch(() => undefined));
});

self.addEventListener("sync", (event) => {
  if (event.tag !== "eco-deliveries") return;
  event.waitUntil(self.clients.matchAll({ type: "window" }).then((clients) => {
    clients.forEach((client) => client.postMessage({ type: "sync-deliveries" }));
  }));
});
