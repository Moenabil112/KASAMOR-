import Link from "next/link";
import { getFieldPacket } from "@/modules/api-client";
import { Badge } from "@/components/Badge";
import { mockPhotoMeta, mockVoiceMeta, REVIEW_DECISIONS } from "@/modules/field-packets/data";

export default async function FieldPacketDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const packet = await getFieldPacket(params.id);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Link href="/field-packets" className="text-xs text-earth-goldmuted hover:underline">
            ← All field packets
          </Link>
          <h1 className="mt-1 text-2xl font-bold text-earth-green">
            {packet.field_packet_id}
          </h1>
          <p className="text-sm text-earth-charcoal/70">{packet.place_label}</p>
        </div>
        <Badge value={packet.review_status} />
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <div className="card">
          <h2 className="font-semibold text-earth-green">Packet metadata</h2>
          <dl className="mt-3 space-y-2 text-sm">
            <Row k="Contributor code" v={packet.contributor_code} mono />
            <Row k="Observation date" v={packet.observation_date} />
            <Row k="Seasonal context" v={packet.seasonal_context} />
            <Row k="Location" v="RESTRICTED — not displayed" />
            <Row k="Tags" v={(packet.observation_tags ?? []).join(", ") || "—"} />
          </dl>
        </div>

        <div className="card">
          <h2 className="font-semibold text-earth-green">Field notes</h2>
          <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-earth-charcoal/80">
            {(packet.local_notes ?? []).map((n: string, i: number) => (
              <li key={i}>{n}</li>
            ))}
            {(packet.sediment_observations ?? []).map((n: string, i: number) => (
              <li key={`s${i}`}>{n}</li>
            ))}
            {(packet.rock_observations ?? []).map((n: string, i: number) => (
              <li key={`r${i}`}>{n}</li>
            ))}
          </ul>
        </div>

        <div className="card">
          <h2 className="font-semibold text-earth-green">Photo metadata</h2>
          <ul className="mt-3 space-y-2 text-sm">
            {(packet.photos ?? []).map((pid: string) => {
              const meta = mockPhotoMeta.find((m) => m.photo_id === pid);
              return (
                <li key={pid} className="flex items-center justify-between">
                  <span className="font-mono text-xs">{pid}</span>
                  <span className="text-earth-charcoal/70">{meta?.photo_type ?? "—"}</span>
                  <Badge value={meta?.quality_status} />
                </li>
              );
            })}
            {(packet.photos ?? []).length === 0 && (
              <li className="text-earth-charcoal/60">No photos.</li>
            )}
          </ul>
          <p className="mt-3 text-xs text-earth-charcoal/60">
            Quality assessment is documentation-only and never implies mineral value.
          </p>
        </div>

        <div className="card">
          <h2 className="font-semibold text-earth-green">Voice note metadata</h2>
          <ul className="mt-3 space-y-2 text-sm">
            {(packet.voice_notes ?? []).map((vid: string) => {
              const meta = mockVoiceMeta.find((m) => m.voice_note_id === vid);
              return (
                <li key={vid} className="flex items-center justify-between">
                  <span className="font-mono text-xs">{vid}</span>
                  <span className="text-earth-charcoal/70">
                    {meta?.language_or_dialect ?? "—"}
                  </span>
                  <Badge value={meta?.transcription_status} />
                </li>
              );
            })}
            {(packet.voice_notes ?? []).length === 0 && (
              <li className="text-earth-charcoal/60">No voice notes.</li>
            )}
          </ul>
        </div>
      </div>

      <div className="card">
        <h2 className="font-semibold text-earth-green">AI summary</h2>
        <p className="mt-2 text-sm text-earth-charcoal/80">
          {packet.ai_summary ??
            "Not generated yet. Run the mock agent pipeline (Reports page or POST /agents/run/mock) to produce an indicative, non-confirmatory observation summary."}
        </p>
      </div>

      <div className="card">
        <h2 className="font-semibold text-earth-green">Review decision options</h2>
        <div className="mt-3 flex flex-wrap gap-2">
          {REVIEW_DECISIONS.map((d) => (
            <span
              key={d}
              className="rounded border border-earth-sand bg-white px-3 py-1.5 text-sm text-earth-charcoal/80"
            >
              {d.replaceAll("_", " ")}
            </span>
          ))}
        </div>
        <p className="mt-3 text-xs text-earth-charcoal/60">
          Decisions are recorded by the House of Earth Trust on the Review page.
        </p>
      </div>
    </div>
  );
}

function Row({ k, v, mono }: { k: string; v: any; mono?: boolean }) {
  return (
    <div className="flex justify-between border-b border-earth-sand/40 py-1">
      <dt className="text-earth-charcoal/60">{k}</dt>
      <dd className={mono ? "font-mono text-xs" : ""}>{v ?? "—"}</dd>
    </div>
  );
}
