import { describe, expect, it } from "vitest";
import { buildWindowIso, validateWindowRange } from "./orderWindow";

describe("validateWindowRange", () => {
  it("accepts a valid interval", () => {
    expect(
      validateWindowRange("2026-10-08T09:00:00-05:00", "2026-10-08T12:00:00-05:00"),
    ).toBeNull();
  });

  it("rejects inverted or equal windows", () => {
    expect(
      validateWindowRange("2026-10-08T14:00:00-05:00", "2026-10-08T11:00:00-05:00"),
    ).toMatch(/posterior/i);
    expect(
      validateWindowRange("2026-10-08T11:00:00-05:00", "2026-10-08T11:00:00-05:00"),
    ).toMatch(/posterior/i);
  });
});

describe("buildWindowIso", () => {
  it("builds Lima-offset payloads", () => {
    const built = buildWindowIso("2026-10-08", "09:30", "11:45");
    expect(built?.ventana_inicio).toBe("2026-10-08T09:30:00-05:00");
    expect(built?.ventana_fin).toBe("2026-10-08T11:45:00-05:00");
  });

  it("rejects invalid clock formats", () => {
    expect(buildWindowIso("2026-10-08", "25:00", "11:00")).toBeNull();
  });
});
