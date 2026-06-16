"use client";

import { useState } from "react";
import { searchKnowledge } from "@/modules/api-client";
import { Badge } from "@/components/Badge";

export function KnowledgeSearch() {
  const [query, setQuery] = useState("House of Earth Trust review");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  async function run(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    const data = await searchKnowledge(query);
    setResults(data.results ?? []);
    setSearched(true);
    setLoading(false);
  }

  return (
    <div className="card">
      <h2 className="font-semibold text-earth-green">Search knowledge (mock retrieval)</h2>
      <form onSubmit={run} className="mt-3 flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 rounded border border-earth-sand bg-white px-3 py-2 text-sm"
          placeholder="Ask about the ecosystem, governance, field protocol…"
        />
        <button
          type="submit"
          className="rounded bg-earth-green px-4 py-2 text-sm font-medium text-earth-sandlight hover:bg-earth-deep"
        >
          {loading ? "Searching…" : "Search"}
        </button>
      </form>

      <div className="mt-4 space-y-3">
        {searched && results.length === 0 && (
          <p className="text-sm text-earth-charcoal/60">No matching knowledge found.</p>
        )}
        {results.map((r) => (
          <div key={r.chunk_id} className="rounded border border-earth-sand/60 bg-white/70 p-3">
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs text-earth-charcoal/60">{r.chunk_id}</span>
              <Badge value={r.sensitivity_level} />
            </div>
            <div className="mt-1 text-sm font-medium text-earth-green">
              {r.section_title ?? "Section"}
            </div>
            <p className="mt-1 text-sm text-earth-charcoal/80">{r.snippet}</p>
            <div className="mt-1 text-xs text-earth-charcoal/50">
              {r.source_file} · score {Number(r.score).toFixed(2)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
