import { execFileSync } from "node:child_process";
import { readFileSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { build } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// Uses Git sources in memory: the working tree is never rewritten.
// Valid for baseline 2716fd5, whose build config uses these same two plugins.
const revision = process.argv[2] || "2716fd5";
const root = fileURLToPath(new URL("../", import.meta.url)).replaceAll("\\", "/");
await build({
  configFile: false,
  root,
  publicDir: false,
  plugins: [{
    name: "git-baseline-source",
    enforce: "pre",
    load(id) {
      const normalized = id.replaceAll("\\", "/").split("?")[0];
      if (!normalized.startsWith(`${root}src/`)) return null;
      const relative = normalized.slice(root.length);
      return execFileSync("git", ["show", `${revision}:${relative}`], { cwd: root, encoding: "utf8" });
    },
  }, react(), tailwindcss()],
  build: { outDir: "dist/baseline", emptyOutDir: true },
});
const assets = readdirSync(new URL("../dist/baseline/assets/", import.meta.url))
  .filter((name) => /\.(js|css)$/.test(name))
  .map((name) => ({ archivo: name, bytes: readFileSync(new URL(`../dist/baseline/assets/${name}`, import.meta.url)).length }));
console.log(JSON.stringify({ revision, nota: "Build comparativo local; no es una medición del navegador.", assets }, null, 2));
