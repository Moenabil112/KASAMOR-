"use client";

import { useState } from "react";
import { API_BASE } from "@/modules/api-client";

function mockMarkdown(id: string): string {
  return `# KASAMOR Field Packet Report

**Field Packet ID:** ${id}
**Place label:** Seasonal drainage sector near study-area ridge
**Observation date:** 2026-05-12

## Photo quality summary
3 photo(s): 1× accepted, 2× needs_retake.

## Voice observation summary
1 voice note(s). Reported field cues: seasonal_flow, black_sand_after_flow, upstream_white_rocks.

## AI observation summary
Qualitative field indicators only — not a confirmation of any mineral or its value.

## Recommended next action
Schedule a structured field revisit to re-document the dark sand with a reference scale.

> _Sensitivity note:_ INTERNAL. General place label only — no raw coordinates,
> no contributor identity. AI output is assistive, not authoritative.
`;
}

export function ReportExporter({ packets }: { packets: any[] }) {
  const [selected, setSelected] = useState(packets[0]?.field_packet_id ?? "KSM-FP-0001");
  const [markdown, setMarkdown] = useState<string>("");
  const [busy, setBusy] = useState(false);
  const [source, setSource] = useState<"live" | "mock" | "">("");

  async function generate() {
    setBusy(true);
    try {
      const res = await fetch(`${API_BASE}/reports/field-packet/${selected}`, {
        method: "POST",
        signal: AbortSignal.timeout?.(2500),
      });
      if (res.ok) {
        const data = await res.json();
        setMarkdown(data.markdown);
        setSource("live");
      } else {
        throw new Error("api");
      }
    } catch {
      setMarkdown(mockMarkdown(selected));
      setSource("mock");
    } finally {
      setBusy(false);
    }
  }

  function download() {
    const blob = new Blob([markdown], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${selected}_report.md`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="space-y-4">
      <div className="card flex flex-wrap items-end gap-3">
        <label className="text-sm">
          <span className="mb-1 block text-earth-charcoal/60">Field packet</span>
          <select
            value={selected}
            onChange={(e) => setSelected(e.target.value)}
            className="rounded border border-earth-sand bg-white px-3 py-2 text-sm"
          >
            {packets.map((p: any) => (
              <option key={p.field_packet_id} value={p.field_packet_id}>
                {p.field_packet_id} — {p.place_label}
              </option>
            ))}
          </select>
        </label>
        <button
          onClick={generate}
          className="rounded bg-earth-green px-4 py-2 text-sm font-medium text-earth-sandlight hover:bg-earth-deep"
        >
          {busy ? "Generating…" : "Generate report"}
        </button>
        {markdown && (
          <button
            onClick={download}
            className="rounded border border-earth-goldmuted px-4 py-2 text-sm font-medium text-earth-goldmuted hover:bg-earth-gold/10"
          >
            Download .md
          </button>
        )}
        {source && (
          <span className="text-xs text-earth-charcoal/50">
            source: {source === "live" ? "live API" : "mock"}
          </span>
        )}
      </div>

      {markdown && (
        <pre className="card overflow-x-auto whitespace-pre-wrap text-sm text-earth-charcoal/90">
          {markdown}
        </pre>
      )}
    </div>
  );
}
