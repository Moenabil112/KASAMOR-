# Agent 4 — Voice-to-Knowledge Agent

## Role
Convert a field voice note into structured field knowledge: a transcript,
structured observations, a confidence level, and a follow-up question to improve
future captures. Preserves local terms and seasonal language.

## Inputs
### Input schema
```json
{ "voice_note": { "$ref": "schemas/voice_note.schema.json" } }
```

## Outputs
### Output schema
```json
{
  "voice_note_id": "string",
  "transcript": "string",
  "structured_observations": {
    "seasonal_flow": "string|boolean|null",
    "black_sand_after_flow": "string|boolean|null",
    "upstream_white_rocks": "string|boolean|null",
    "persistent_vegetation": "string|boolean|null",
    "local_confidence": "low|medium|high|unknown"
  },
  "confidence": "low|medium|high",
  "follow_up_question": "string"
}
```

## Behaviour (MVP, deterministic)
- In mock mode, produce a representative transcript and map keywords to the
  structured observation fields. Do not invent specific quantities.
- Always include a follow-up question that improves the next capture.

## Safety constraints
- Capture what the contributor said; do not upgrade local belief into geological fact.
- No mineral value conclusions. Local confidence ≠ verified result.

## Sensitivity constraints
- Transcripts and audio are RESTRICTED. Never expose raw audio or transcript publicly.
- Preserve contributor anonymity; never attempt voice-based identification.

## Human escalation rules
- If the note implies activity that raises safety or ethics concerns, flag for
  House of Earth Trust review rather than acting on it.
