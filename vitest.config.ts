import { defineConfig } from "vitest/config";

export default defineConfig({
  cacheDir: "AUDITORIA/CORRECCIONES_EVIDENCIAS/runtime/vite",
  test: {
    outputFile: { json: "AUDITORIA/CORRECCIONES_EVIDENCIAS/frontend-results.json" },
    environment: "node",
    include: ["src/**/*.test.{ts,tsx}"],
    coverage: {
      provider: "v8",
      thresholds: { lines: 80 },
      reporter: ["text", "lcov", "json-summary"],
      reportsDirectory: "coverage/frontend",
      include: ["src/**/*.{ts,tsx}"],
      exclude: ["src/**/*.test.{ts,tsx}", "src/**/*.d.ts"],
    },
  },
});
