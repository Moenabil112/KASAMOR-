import { getKnowledgeSummary } from "@/modules/api-client";
import { Badge } from "@/components/Badge";
import { KnowledgeSearch } from "./search";

export default async function KnowledgeBasePage() {
  const summary = await getKnowledgeSummary();

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-earth-green">Knowledge Base</h1>
        <p className="mt-1 text-sm text-earth-charcoal/70">
          Ingested from the latest clean base knowledge package.
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <div className="card">
          <div className="text-3xl font-bold text-earth-green">{summary.document_count}</div>
          <div className="text-sm text-earth-charcoal/70">Documents</div>
        </div>
        <div className="card">
          <div className="text-3xl font-bold text-earth-green">{summary.chunk_count}</div>
          <div className="text-sm text-earth-charcoal/70">Chunks</div>
        </div>
        <div className="card">
          <div className="text-3xl font-bold text-earth-green">
            {Object.keys(summary.domains).length}
          </div>
          <div className="text-sm text-earth-charcoal/70">Knowledge domains</div>
        </div>
        <div className="card">
          <div className="text-3xl font-bold text-earth-green">
            {Object.keys(summary.sensitivity_counts).length}
          </div>
          <div className="text-sm text-earth-charcoal/70">Sensitivity levels</div>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <div className="card">
          <h2 className="font-semibold text-earth-green">Chunks by domain</h2>
          <ul className="mt-3 space-y-1 text-sm">
            {Object.entries(summary.domains).map(([k, v]) => (
              <li key={k} className="flex justify-between border-b border-earth-sand/50 py-1">
                <span className="capitalize">{k}</span>
                <span className="font-mono">{v as number}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h2 className="font-semibold text-earth-green">Chunks by sensitivity</h2>
          <ul className="mt-3 space-y-2 text-sm">
            {Object.entries(summary.sensitivity_counts).map(([k, v]) => (
              <li key={k} className="flex items-center justify-between">
                <Badge value={k} />
                <span className="font-mono">{v as number}</span>
              </li>
            ))}
          </ul>
          <p className="mt-4 text-xs text-earth-charcoal/60">
            Geospatial references are indexed as RESTRICTED descriptors only — no raw
            coordinates are stored in retrievable chunks.
          </p>
        </div>
      </div>

      <KnowledgeSearch />
    </div>
  );
}
