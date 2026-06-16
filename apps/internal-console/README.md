# KASAMOR Internal Console

Internal operating console for the Rural Mineral Intelligence Ecosystem
(Next.js 14 · TypeScript · Tailwind CSS).

## Pages
| Route | Shows |
|---|---|
| `/` | Operating overview (knowledge + packet + review counts). |
| `/knowledge-base` | Ingested document/chunk counts, domains, sensitivity, mock search. |
| `/field-packets` | List of field packets with status. |
| `/field-packets/[id]` | Packet metadata, photo/voice metadata, AI summary, decision options. |
| `/review` | House of Earth Trust review cards with decision buttons. |
| `/reports` | Generate + download a Markdown Field Packet report. |

## Run
```bash
npm install
npm run dev        # http://localhost:3001
```

Set `NEXT_PUBLIC_API_BASE_URL` to point at the FastAPI service (default
`http://localhost:8000`). If the API is unreachable, the console **falls back to
bundled mock data** so it can be demoed standalone.

## Safety
This is an INTERNAL surface. Raw coordinates and contributor identities are never
displayed — location is shown only as a general place label, and the API enforces
sensitivity gating server-side.
