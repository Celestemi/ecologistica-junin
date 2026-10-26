import type { ActiveRoute } from "../types";

const DB = "eco-driver-offline-v1";
const STORE = "records";

type RecordValue = { key: string; value: unknown };
export type PendingDelivery = {
  id: string;
  userId: number;
  orderCode: string;
  deliveredAt: string;
  attempts: number;
  lastError?: string;
};

function key(userId: number, name: string) { return `${userId}:${name}`; }

function database(): Promise<IDBDatabase> {
  return new Promise<IDBDatabase>((resolve, reject) => {
    const request = indexedDB.open(DB, 1);
    request.onupgradeneeded = () => request.result.createObjectStore(STORE, { keyPath: "key" });
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

async function get<T>(recordKey: string): Promise<T | null> {
  const db = await database();
  return new Promise<T | null>((resolve, reject) => {
    const tx = db.transaction(STORE, "readonly");
    const request = tx.objectStore(STORE).get(recordKey);
    request.onsuccess = () => resolve((request.result as RecordValue | undefined)?.value as T ?? null);
    request.onerror = () => reject(request.error);
  }).finally(() => db.close());
}

async function put(recordKey: string, value: unknown): Promise<void> {
  const db = await database();
  return new Promise<void>((resolve, reject) => {
    const tx = db.transaction(STORE, "readwrite");
    tx.objectStore(STORE).put({ key: recordKey, value });
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  }).finally(() => db.close());
}

export async function cacheRoute(userId: number, route: ActiveRoute): Promise<void> {
  await put(key(userId, "route"), route);
}
export async function cacheValue(userId: number, name: string, value: unknown): Promise<void> { await put(key(userId, name), value); }
export async function cachedValue<T>(userId: number, name: string): Promise<T | null> { return get<T>(key(userId, name)); }
export async function cachedRoute(userId: number): Promise<ActiveRoute | null> { return get<ActiveRoute>(key(userId, "route")); }
export async function pendingDeliveries(userId: number): Promise<PendingDelivery[]> { return (await get<PendingDelivery[]>(key(userId, "deliveries"))) ?? []; }
export async function enqueueDelivery(item: PendingDelivery): Promise<void> {
  const items = await pendingDeliveries(item.userId);
  if (!items.some((current) => current.id === item.id)) { items.push(item); await put(key(item.userId, "deliveries"), items); }
}
export async function replacePendingDeliveries(userId: number, items: PendingDelivery[]): Promise<void> { await put(key(userId, "deliveries"), items); }
export async function completedDeliveryCodes(userId: number): Promise<string[]> { return (await get<string[]>(key(userId, "completed"))) ?? []; }
export async function markDeliveryCompleted(userId: number, orderCode: string): Promise<void> {
  const codes = await completedDeliveryCodes(userId);
  if (!codes.includes(orderCode)) await put(key(userId, "completed"), [...codes, orderCode]);
}
export async function clearOfflineData(): Promise<void> {
  const db = await database();
  await new Promise<void>((resolve, reject) => { const tx = db.transaction(STORE, "readwrite"); tx.objectStore(STORE).clear(); tx.oncomplete = () => resolve(); tx.onerror = () => reject(tx.error); });
  db.close();
}
