// Agent-runs module: ordered MVP pipeline used by the console + API.
export const AGENT_PIPELINE = [
  { id: "field_packet_intake_agent", label: "Field Packet Intake" },
  { id: "photo_quality_agent", label: "Photo Quality" },
  { id: "voice_to_knowledge_agent", label: "Voice-to-Knowledge" },
  { id: "geo_photo_voice_fusion_agent", label: "Geo-Photo-Voice Fusion" },
  { id: "house_of_earth_trust_review_agent", label: "House of Earth Trust Review" },
] as const;
