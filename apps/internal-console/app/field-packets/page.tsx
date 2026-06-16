import Link from "next/link";
import { getFieldPackets } from "@/modules/api-client";
import { Badge } from "@/components/Badge";

export default async function FieldPacketsPage() {
  const packets = await getFieldPackets();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-earth-green">Field Packets</h1>
        <p className="mt-1 text-sm text-earth-charcoal/70">
          Structured rural observation packages. Coordinates are RESTRICTED and never
          shown here — only a general place label.
        </p>
      </div>

      <div className="card overflow-x-auto p-0">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-earth-sand bg-earth-sand/30 text-earth-green">
            <tr>
              <th className="px-4 py-3">Packet</th>
              <th className="px-4 py-3">Contributor</th>
              <th className="px-4 py-3">Place label</th>
              <th className="px-4 py-3">Date</th>
              <th className="px-4 py-3">Review status</th>
              <th className="px-4 py-3">Decision</th>
            </tr>
          </thead>
          <tbody>
            {packets.map((p: any) => (
              <tr key={p.field_packet_id} className="border-b border-earth-sand/40 hover:bg-earth-sand/10">
                <td className="px-4 py-3">
                  <Link
                    href={`/field-packets/${p.field_packet_id}`}
                    className="font-mono text-earth-goldmuted hover:underline"
                  >
                    {p.field_packet_id}
                  </Link>
                </td>
                <td className="px-4 py-3 font-mono text-xs">{p.contributor_code}</td>
                <td className="px-4 py-3">{p.place_label ?? "—"}</td>
                <td className="px-4 py-3">{p.observation_date ?? "—"}</td>
                <td className="px-4 py-3">
                  <Badge value={p.review_status} />
                </td>
                <td className="px-4 py-3">{p.review_decision ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
