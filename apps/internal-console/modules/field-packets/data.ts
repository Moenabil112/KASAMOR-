// Field-packets module: types + bundled mock data fallback.

export interface FieldPacketSummary {
  field_packet_id: string;
  contributor_code: string;
  place_label: string | null;
  review_status: string;
  review_decision: string | null;
  observation_date: string | null;
}

export interface FieldPacketDetail extends FieldPacketSummary {
  seasonal_context: string;
  photos: string[];
  voice_notes: string[];
  local_notes: string[];
  sediment_observations?: string[];
  rock_observations?: string[];
  water_drainage_observations?: string[];
  observation_tags: string[];
  ai_summary: string | null;
}

export const mockFieldPackets: FieldPacketSummary[] = [
  {
    field_packet_id: "KSM-FP-0001",
    contributor_code: "FIELD-001",
    place_label: "Seasonal drainage sector near study-area ridge",
    review_status: "pending",
    review_decision: null,
    observation_date: "2026-05-12",
  },
];

export function mockPacketDetail(id: string): FieldPacketDetail {
  return {
    field_packet_id: id,
    contributor_code: "FIELD-001",
    place_label: "Seasonal drainage sector near study-area ridge",
    review_status: "pending",
    review_decision: null,
    observation_date: "2026-05-12",
    seasonal_context: "after_rain",
    photos: ["KSM-PH-0001", "KSM-PH-0002", "KSM-PH-0003"],
    voice_notes: ["KSM-VN-0001"],
    local_notes: [
      "Water flows strongly here for a few days after heavy rain, then dries.",
      "Elders call this stretch the dark-sand bend.",
    ],
    sediment_observations: [
      "Dark heavy sand collects in the inner bend of the channel after flow.",
    ],
    rock_observations: ["White quartz-like fragments scattered along the upstream slope."],
    water_drainage_observations: ["Single seasonal channel draining the ridge."],
    observation_tags: ["black_sand", "quartz_context", "seasonal_drainage", "after_rain"],
    ai_summary: null,
  };
}

// Photo / voice metadata for the detail page (documentation only — never claims).
export const mockPhotoMeta = [
  { photo_id: "KSM-PH-0001", photo_type: "site_context", quality_status: "accepted" },
  { photo_id: "KSM-PH-0002", photo_type: "sediment_closeup", quality_status: "needs_retake" },
  { photo_id: "KSM-PH-0003", photo_type: "black_sand_closeup", quality_status: "documentation_only" },
];

export const mockVoiceMeta = [
  {
    voice_note_id: "KSM-VN-0001",
    language_or_dialect: "local_dialect",
    transcription_status: "pending",
  },
];

export const REVIEW_DECISIONS = [
  "accepted",
  "needs_more_photos",
  "needs_field_revisit",
  "needs_sample",
  "low_priority",
  "rejected",
] as const;
