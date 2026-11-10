import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { runInNewContext } from "node:vm";

function worker() {
  const handlers = {};
  const records = new Map();
  const deleted = [];
  const cache = {
    addAll: async (requests) => requests.forEach((request) => records.set(new URL(request.url).pathname, new Response("shell"))),
    match: async (request) => records.get(typeof request === "string" ? request : new URL(request.url).pathname),
    put: async (request, response) => records.set(new URL(request.url).pathname, response),
  };
  let network = async () => new Response("network", { headers: { "Content-Type": "application/javascript" } });
  const clients = [{ postMessage: (message) => clients.messages.push(message) }];
  clients.messages = [];
  runInNewContext(readFileSync(new URL("../public/sw.js", import.meta.url), "utf8"), {
    self: {
      location: { origin: "https://eco.test" },
      addEventListener: (name, handler) => { handlers[name] = handler; },
      clients: { claim: async () => {}, matchAll: async () => clients },
    },
    caches: {
      open: async () => cache,
      keys: async () => ["eco-shell-v1", "unrelated-cache", "eco-shell-__BUILD_VERSION__"],
      delete: async (key) => { deleted.push(key); },
    },
    Request: class extends Request { constructor(url, init) { super(new URL(url, "https://eco.test"), init); } },
    Response, URL, fetch: (...args) => network(...args),
  });
  const invoke = async (name, properties = {}) => {
    const waits = [];
    let response;
    handlers[name]({ ...properties, waitUntil: (promise) => waits.push(promise), respondWith: (promise) => { response = promise; } });
    await Promise.all(waits);
    return response;
  };
  return { invoke, records, deleted, clients, setNetwork: (implementation) => { network = implementation; } };
}

test("activation deletes only old application caches", async () => {
  const sw = worker();
  await sw.invoke("activate");
  assert.deepEqual(sw.deleted, ["eco-shell-v1"]);
});

test("API, authenticated requests, mutations and external tiles bypass caching", async () => {
  const sw = worker();
  for (const request of [
    new Request("https://eco.test/api/v1/pedidos"),
    new Request("https://eco.test/assets/private.js", { headers: { Authorization: "Bearer token" } }),
    new Request("https://eco.test/assets/file.js", { method: "POST" }),
    new Request("https://tiles.test/image.png"),
  ]) assert.equal(await sw.invoke("fetch", { request }), undefined);
  assert.equal(sw.records.size, 0);
});

test("public assets are reused; errors, private responses and HTML fallbacks are not stored", async () => {
  const sw = worker();
  const request = new Request("https://eco.test/assets/main-hash.js");
  const first = await sw.invoke("fetch", { request });
  assert.equal(await first.text(), "network");
  sw.setNetwork(async () => { throw new Error("offline"); });
  assert.equal(await (await sw.invoke("fetch", { request })).text(), "network");
  for (const response of [new Response("error", { status: 404 }),
    new Response("private", { headers: { "Cache-Control": "private" } }),
    new Response("html", { headers: { "Content-Type": "text/html" } })]) {
    sw.setNetwork(async () => response);
    await sw.invoke("fetch", { request: new Request("https://eco.test/assets/missing.js") });
    assert.equal(sw.records.has("/assets/missing.js"), false);
  }
});

test("offline navigation falls back to the installed shell and sync keeps its work alive", async () => {
  const sw = worker();
  await sw.invoke("install");
  sw.setNetwork(async () => { throw new Error("offline"); });
  const request = { url: "https://eco.test/conductor", method: "GET", mode: "navigate", headers: new Headers() };
  assert.equal(await (await sw.invoke("fetch", { request })).text(), "shell");
  await sw.invoke("sync", { tag: "eco-deliveries" });
  assert.equal(sw.clients.messages[0].type, "sync-deliveries");
});
