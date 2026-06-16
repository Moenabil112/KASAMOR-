import Link from "next/link";
import { getKnowledgeSummary, getFieldPackets, dataSource } from "@/modules/api-client";

export default async function OverviewPage() {
  const [summary, packets, source] = await Promise.all([
    getKnowledgeSummary(),
    getFieldPackets(),
    dataSource(),
  ]);

  const cards = [
    { label: "Documents ingested", value: summary.document_count, href: "/knowledge-base" },
    { label: "Knowledge chunks", value: summary.chunk_count, href: "/knowledge-base" },
    { label: "Field packets", value: packets.length, href: "/field-packets" },
    {
      label: "Pending review",
      value: packets.filter((p: any) => p.review_status === "pending").length,
      href: "/review",
    },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-earth-green">Operating Overview</h1>
        <p className="mt-1 text-sm text-earth-charcoal/70">
          Internal console for the KASAMOR Rural Mineral Intelligence Ecosystem.
          Data source:{" "}
          <span className="font-semibold">
            {source === "live" ? "live API" : "bundled mock data"}
          </span>
          .
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {cards.map((c) => (
          <Link key={c.label} href={c.href} className="card transition hover:shadow-md">
            <div className="text-3xl font-bold text-earth-green">{c.value}</div>
            <div className="mt-1 text-sm text-earth-charcoal/70">{c.label}</div>
          </Link>
        ))}
      </div>

      <div className="card">
        <h2 className="font-semibold text-earth-green">Pipeline</h2>
        <p className="mt-2 text-sm text-earth-charcoal/70">
          Field Packet → Intake → Photo Quality → Voice-to-Knowledge → Geo-Photo-Voice
          Fusion → House of Earth Trust review card → Markdown report. Agents run as
          deterministic mocks in the MVP (no API keys required).
        </p>
      </div>
    </div>
  );
}
