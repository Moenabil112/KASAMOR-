// Shared API client for the internal console.
// Gracefully falls back to bundled mock data when the API is unreachable, so the
// console can be demoed independently of the Python service.

import { mockKnowledgeSummary, mockSearch } from "./knowledge-base/data";
import { mockFieldPackets, mockPacketDetail } from "./field-packets/data";

export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function tryFetch<T>(path: string, init?: RequestInit): Promise<T | null> {
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      ...init,
      cache: "no-store",
      // Short timeout-ish behaviour via AbortController.
      signal: AbortSignal.timeout?.(2500),
    });
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

export async function getKnowledgeSummary() {
  return (await tryFetch<any>("/knowledge/summary")) ?? mockKnowledgeSummary;
}

export async function searchKnowledge(query: string) {
  const live = await tryFetch<any>("/knowledge/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, max_sensitivity: "INTERNAL", top_k: 5 }),
  });
  return live ?? mockSearch(query);
}

export async function getFieldPackets() {
  return (await tryFetch<any[]>("/field-packets")) ?? mockFieldPackets;
}

export async function getFieldPacket(id: string) {
  return (await tryFetch<any>(`/field-packets/${id}`)) ?? mockPacketDetail(id);
}

export async function dataSource(): Promise<"live" | "mock"> {
  const live = await tryFetch<any>("/health");
  return live ? "live" : "mock";
}
