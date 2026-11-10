import { readdirSync, readFileSync, statSync } from "node:fs";
import { gzipSync } from "node:zlib";
import assert from "node:assert/strict";

const root = new URL("../dist/", import.meta.url);
const files = readdirSync(new URL("assets/", root)).filter((name) => /\.(js|css)$/.test(name));
const assets = files.map((name) => {
  const content = readFileSync(new URL(`assets/${name}`, root));
  return { archivo: name, bytes: content.length, gzip_bytes: gzipSync(content, { level: 5 }).length };
});
const sw = readFileSync(new URL("sw.js", root), "utf8");
assert.ok(!sw.includes("__BUILD_VERSION__"), "Falta versionar el SW");
assert.ok(!sw.includes("__PRECACHE_ASSETS__"), "Falta generar el precache");
const precache = JSON.parse(sw.match(/const BUILD_ASSETS = (\[[^;]*\]);/)[1]);
for (const path of precache) assert.ok(statSync(new URL(path.slice(1), root)).isFile());
assert.ok(precache.some((path) => /DriverApp-.*\.js$/.test(path)), "Falta conductor offline");
assert.ok(precache.some((path) => /Login-.*\.js$/.test(path)), "Falta acceso offline");
assert.ok(!precache.some((path) => /OrdersDay-.*\.js$/.test(path)), "Pedidos no debe precargarse");
console.log(JSON.stringify({
  nota: "Tamaños de artefactos locales; gzip calculado con nivel 5, no transferencia HTTP medida.",
  assets,
  total_bytes: assets.reduce((sum, item) => sum + item.bytes, 0),
  precache,
}, null, 2));
