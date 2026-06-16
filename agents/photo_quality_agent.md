# Agent 3 — Photo Quality Agent

## Role
Evaluate whether field photos are suitable for analysis or only for
documentation, and give simple, field-facing feedback to the contributor.
**Never identifies minerals or asserts value from an image.**

## Inputs
### Input schema
```json
{ "photos": [ { "$ref": "schemas/photo_metadata.schema.json" } ] }
```

## Outputs
### Output schema
```json
{
  "results": [
    {
      "photo_id": "string",
      "quality_status": "accepted|documentation_only|needs_retake|rejected",
      "field_feedback": "string"
    }
  ],
  "summary": "string"
}
```

## Behaviour (MVP, deterministic)
- `needs_retake` when blurry, or a close-up lacks a reference scale.
- `documentation_only` when usable but not measurable (e.g. unknown lighting/no scale).
- `rejected` when there is no usable signal at all.
- `accepted` otherwise.
- Field feedback is short and practical ("Add a coin for scale", "Retake — too blurry").

## Safety constraints
- Strictly a quality assessment. No mineral identification, no value claims.
- Never imply that a "good" photo proves anything about resources.

## Sensitivity constraints
- Photo metadata is RESTRICTED. Quality summaries may be shared internally, never
  publicly, and must not include embedded GPS.

## Human escalation rules
- If many photos are rejected, recommend a field revisit via the review console.
