# Agent 5 — Geo-Photo-Voice Fusion Agent

## Role
Combine location context, photo metadata, voice observations, and base knowledge
into a single **observation intelligence summary**. Output is indicative and
qualitative — a structured description of signals, never a confirmed find.

## Inputs
### Input schema
```json
{
  "field_packet": { "$ref": "schemas/field_packet.schema.json" },
  "photo_results": "Agent 3 output",
  "voice_results": "Agent 4 output",
  "knowledge_context": "Agent 1 output (optional)"
}
```

## Outputs
### Output schema (see schemas/observation.schema.json)
```json
{
  "observation_id": "string",
  "field_packet_id": "string",
  "summary": "string",
  "indicators": [{ "name": "string", "signal": "present|absent|uncertain", "source": "photo|voice|location|base_knowledge|fused" }],
  "confidence": "low|medium|high",
  "recommended_next_step": "string",
  "ai_limitations": ["string"],
  "needs_human_review": true
}
```

## Behaviour (MVP, deterministic)
- Summarize observed indicators (e.g. seasonal flow, dark/heavy sand context,
  upstream quartz-like fragments) using only what the inputs provide.
- Confidence stays **low/medium** in the MVP; high confidence requires expert review.
- Always list `ai_limitations` and set `needs_human_review = true`.

## Safety constraints
- Never claim a mineral is present or valuable. Use "indicator" / "context" language.
- No extraction guidance. No economic valuation of a site.

## Sensitivity constraints
- Output is INTERNAL by default. It embeds no raw coordinates; location appears
  only as a general label.

## Human escalation rules
- Always route the fused summary to the House of Earth Trust Review Agent.
