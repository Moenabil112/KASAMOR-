# KASAMOR — Data Governance & Sensitivity Protocol

Data governance is foundational to KASAMOR. The system handles community-sensitive
field knowledge, and protecting it is a first-class requirement — not an afterthought.

## Sensitivity levels

| Level | Meaning | Example |
|---|---|---|
| `PUBLIC` | Safe for anyone, including the public website. | The ecosystem narrative, the "how it works" loop. |
| `PARTNER` | Shareable with vetted partners under agreement. | Curated concept material, high-level economic framing. |
| `INTERNAL` | KASAMOR operators only. | Field protocols, knowledge chunks, observation summaries. |
| `RESTRICTED` | Tightly held; sensitive field data. | Raw coordinates, photos, voice notes, exact field packets. |
| `HOUSE_OF_EARTH_TRUST_ONLY` | Expert layer only; explicit review gating. | Private research, review decisions, confidence gates. |

Ordering (a surface cleared at level *N* may render data at level ≤ *N*):

```
PUBLIC < PARTNER < INTERNAL < RESTRICTED < HOUSE_OF_EARTH_TRUST_ONLY
```

The machine-readable source of truth is `services/api/models/sensitivity.py`.

## Surface rules

- **Public interface** may render **PUBLIC** content only. PARTNER material is
  hand-curated into public copy when appropriate — never served wholesale. The
  public API ceiling stays at PUBLIC.
- **Internal console** may render up to **INTERNAL** content. It displays a general
  place label only — never raw coordinates or contributor identity.
- **House of Earth Trust** surfaces may access review-only content under explicit
  gating.

## Never-public data

The following must **never** leave the internal boundary, regardless of level:

- Precise coordinates (`lat`, `lon`, `accuracy_m`, full `location`).
- Contributor identities (only anonymous contributor codes exist).
- Raw photos, raw audio, and transcripts.
- Exact field packets and operational target points.
- Community-sensitive observations.

`sensitivity.NEVER_PUBLIC_FIELDS` + `redact_for_public()` provide a defensive
backstop for any serialisation path.

## Geospatial handling

Geospatial reference files (GeoJSON/KML) are ingested as **RESTRICTED descriptors
only**. Raw coordinates are never written into retrievable knowledge chunks or any
public output. The public interface communicates the study area as an *approximate
scale* (~180 km²), never as a map with points.

## AI limitations & human review

- AI output is **assistive and indicative**. It never confirms the presence or
  value of a mineral.
- Every observation summary sets `needs_human_review = true`.
- Confidence is capped at *medium* until the House of Earth Trust reviews and
  decides. Final decisions are recorded via `review_decision.schema.json`.

## Language rules

Use: rural mineral intelligence ecosystem, field knowledge, responsible resource
understanding, AI-supported observation, Field Packet, geo-photo-voice intelligence.

Avoid: gold-detection claims, mining target maps, guaranteed mineral locations,
extraction instructions, public coordinates, speculative reserve language, and
sensational gold-rush framing.
