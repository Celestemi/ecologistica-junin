import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig, type Plugin } from "vite";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

// Precache only the shell and driver dependency graph, keeping other pages lazy.
function offlineShell(): Plugin {
  return {
    name: "eco-offline-shell",
    apply: "build" as const,
    generateBundle(_options, bundle) {
      const source = readFileSync(new URL("./public/sw.js", import.meta.url), "utf8");
      const hash = createHash("sha256").update(source);
      hash.update(readFileSync(new URL("./public/manifest.webmanifest", import.meta.url)));
      const precache = new Set<string>();
      const visit = (fileName: string) => {
        if (precache.has(`/${fileName}`)) return;
        const item = bundle[fileName];
        if (!item) return;
        precache.add(`/${fileName}`);
        if (item.type === "chunk") item.imports.forEach(visit);
      };
      for (const fileName of Object.keys(bundle).sort()) {
        const item = bundle[fileName];
        hash.update(fileName).update(item.type === "chunk" ? item.code : item.source);
        if (item.type === "chunk" && (item.isEntry || item.name === "DriverApp" || item.name === "Login")) visit(fileName);
        if (fileName.startsWith("assets/") && !fileName.endsWith(".js")) visit(fileName);
      }
      this.emitFile({
        type: "asset",
        fileName: "sw.js",
        source: source.replace("__BUILD_VERSION__", hash.digest("hex").slice(0, 16))
          .replace("/* __PRECACHE_ASSETS__ */ []", JSON.stringify([...precache])),
      });
    },
  };
}

export default defineConfig({
  plugins: [react(), tailwindcss(), offlineShell()],
  server: {
    port: 5173,
    proxy: {
      "/api": "http://127.0.0.1:8000",
      "/ws": {
        target: "ws://127.0.0.1:8000",
        ws: true,
      },
    },
  },
});
