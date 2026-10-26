const CACHE = "eco-shell-v1";
const SHELL = ["/", "/conductor", "/manifest.webmanifest"];
self.addEventListener("install", (event) => event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting())));
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  // Las respuestas autenticadas no se guardan en Cache Storage.
  if (event.request.method !== "GET" || url.origin !== self.location.origin || url.pathname.startsWith("/api/") || url.pathname.startsWith("/ws/")) return;
  event.respondWith(caches.match(event.request).then((cached) => cached || fetch(event.request).then((response) => { const copy = response.clone(); caches.open(CACHE).then((cache) => cache.put(event.request, copy)); return response; })));
});
self.addEventListener("sync", (event) => { if (event.tag === "eco-deliveries") self.clients.matchAll({ type: "window" }).then((clients) => clients.forEach((client) => client.postMessage({ type: "sync-deliveries" }))); });
