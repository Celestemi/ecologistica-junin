import "fake-indexeddb/auto";
import { beforeEach, describe, expect, it } from "vitest";
import {
  cacheRoute,
  cacheValue,
  cachedRoute,
  cachedValue,
  clearOfflineData,
  completedDeliveryCodes,
  enqueueDelivery,
  markDeliveryCompleted,
  pendingDeliveries,
  replacePendingDeliveries,
  type PendingDelivery,
} from "./offline";
import type { ActiveRoute } from "../types";

const delivery: PendingDelivery = {
  id: "operation-1",
  userId: 7,
  orderCode: "PED-001",
  deliveredAt: "2026-10-27T14:00:00-05:00",
  attempts: 0,
};

describe("offline IndexedDB repository", () => {
  beforeEach(async () => {
    await clearOfflineData();
  });

  it("stores generic values and isolates them by user", async () => {
    await cacheValue(7, "theme", { dark: true });
    await expect(cachedValue(7, "theme")).resolves.toEqual({ dark: true });
    await expect(cachedValue(8, "theme")).resolves.toBeNull();
  });

  it("stores and retrieves the active route", async () => {
    const route = { id: 10, placa: "ABC-123" } as unknown as ActiveRoute;
    await cacheRoute(7, route);
    await expect(cachedRoute(7)).resolves.toEqual(route);
  });

  it("queues deliveries idempotently and supports replacement", async () => {
    await expect(pendingDeliveries(7)).resolves.toEqual([]);
    await enqueueDelivery(delivery);
    await enqueueDelivery({ ...delivery, attempts: 9 });
    await expect(pendingDeliveries(7)).resolves.toEqual([delivery]);

    const replacement = [{ ...delivery, id: "operation-2", orderCode: "PED-002" }];
    await replacePendingDeliveries(7, replacement);
    await expect(pendingDeliveries(7)).resolves.toEqual(replacement);
  });

  it("marks completed order codes without duplicates", async () => {
    await expect(completedDeliveryCodes(7)).resolves.toEqual([]);
    await markDeliveryCompleted(7, "PED-001");
    await markDeliveryCompleted(7, "PED-001");
    await markDeliveryCompleted(7, "PED-002");
    await expect(completedDeliveryCodes(7)).resolves.toEqual(["PED-001", "PED-002"]);
  });

  it("clears every cached record", async () => {
    await cacheValue(7, "value", 1);
    await enqueueDelivery(delivery);
    await clearOfflineData();
    await expect(cachedValue(7, "value")).resolves.toBeNull();
    await expect(pendingDeliveries(7)).resolves.toEqual([]);
  });
});
