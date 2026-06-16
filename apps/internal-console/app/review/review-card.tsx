"use client";

import { useState } from "react";
import { Badge } from "@/components/Badge";
import { REVIEW_DECISIONS } from "@/modules/field-packets/data";

export function ReviewCard({ packet }: { packet: any }) {
  const [decision, setDecision] = useState<string | null>(packet.review_decision ?? null);

  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <span className="font-mono text-sm text-earth-goldmuted">{packet.field_packet_id}</span>
        <Badge value={decision ? "decided" : packet.review_status} />
      </div>
      <h3 className="mt-1 font-semibold text-earth-green">{packet.place_label}</h3>
      <p className="mt-1 text-xs text-earth-charcoal/60">
        Contributor {packet.contributor_code} · {packet.observation_date ?? "no date"}
      </p>

      <p className="mt-3 text-xs text-earth-charcoal/70">
        AI limitations apply: indicators are qualitative field context, not confirmation
        of mineral presence or value.
      </p>

      <div className="mt-4">
        <div className="mb-2 text-xs font-medium uppercase tracking-wide text-earth-charcoal/60">
          Decision
        </div>
        <div className="flex flex-wrap gap-2">
          {REVIEW_DECISIONS.map((d) => (
            <button
              key={d}
              onClick={() => setDecision(d)}
              className={`rounded border px-3 py-1.5 text-sm transition ${
                decision === d
                  ? "border-earth-green bg-earth-green text-earth-sandlight"
                  : "border-earth-sand bg-white text-earth-charcoal/80 hover:border-earth-goldmuted"
              }`}
            >
              {d.replaceAll("_", " ")}
            </button>
          ))}
        </div>
        {decision && (
          <p className="mt-3 text-sm text-earth-green">
            Recorded decision: <span className="font-semibold">{decision}</span>{" "}
            <span className="text-xs text-earth-charcoal/50">
              (demo — persisting decisions is a later sprint)
            </span>
          </p>
        )}
      </div>
    </div>
  );
}
