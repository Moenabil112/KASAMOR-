import { getFieldPackets } from "@/modules/api-client";
import { ReviewCard } from "./review-card";

export default async function ReviewPage() {
  const packets = await getFieldPackets();
  const pending = packets.filter((p: any) => p.review_status !== "decided");

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-earth-green">House of Earth Trust — Review</h1>
        <p className="mt-1 text-sm text-earth-charcoal/70">
          Human review of field evidence. AI output is assistive and indicative only;
          the decision rests with the Trust.
        </p>
      </div>

      {pending.length === 0 && (
        <div className="card text-sm text-earth-charcoal/70">Nothing pending review.</div>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        {pending.map((p: any) => (
          <ReviewCard key={p.field_packet_id} packet={p} />
        ))}
      </div>
    </div>
  );
}
