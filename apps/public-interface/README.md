# KASAMOR Public Interface

The public / partner-facing explainable interface for KASAMOR
(Next.js 14 · TypeScript · Tailwind CSS).

## Pages
| Route | Purpose |
|---|---|
| `/` | Hero + the full KASAMOR story (10 sections). |
| `/ecosystem` | The five-layer ecosystem and field intelligence. |
| `/how-it-works` | The Capture → Replicate loop; AI's assistive role. |
| `/mvp` | The ~180 km² controlled pilot (abstract scale, no map). |
| `/partners` | Partner call for academic / technical / development / responsible-resource partners. |

## Run
```bash
npm install
npm run dev        # http://localhost:3000
```

## Design direction
Earth tones — deep green, sand, charcoal, muted gold — calm spacing, strong
typography, light abstract diagrams. No aggressive mining visuals, no gold-rush
language.

## Safety (hard rules)
- **PUBLIC content only.** All copy lives in `content/site.ts`.
- No operational map, no coordinates, no raw field data, no community-sensitive details.
- No gold-detection claims; images are documentation, never confirmation of value.
- No long R&D document dump — concise, explanatory narrative only.
