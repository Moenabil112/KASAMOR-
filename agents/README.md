# KASAMOR AI Agents

Six provider-agnostic agent **specifications**. Each file defines the agent's
role, input/output schemas, safety constraints, sensitivity constraints, and
human-escalation rules. They are deliberately implementation-neutral: no agent
hardcodes a single AI provider.

| # | Agent | Purpose |
|---|---|---|
| 1 | `knowledge_retrieval_agent.md` | Retrieve sensitivity-cleared base knowledge to answer questions. |
| 2 | `field_packet_intake_agent.md` | Validate & normalize a submitted Field Packet. |
| 3 | `photo_quality_agent.md` | Judge photo suitability (analysis vs documentation). |
| 4 | `voice_to_knowledge_agent.md` | Turn voice notes into structured field knowledge. |
| 5 | `geo_photo_voice_fusion_agent.md` | Fuse location + photo + voice + knowledge into an observation summary. |
| 6 | `house_of_earth_trust_review_agent.md` | Prepare a human review brief for experts. |

## Execution
For the MVP these run as **deterministic mocks** implemented in
`services/agent-orchestrator/` (so the system works with no API keys). The mock
registry maps each agent id to a function with the same input/output contract,
ready to be swapped for live model calls (`KASAMOR_AGENT_MODE=live`) later.

## Universal rules (apply to every agent)
- Never claim that an observation or image **confirms** the presence or value of a mineral.
- Never output raw coordinates, contributor identities, or extraction instructions.
- Always surface AI limitations and defer high-stakes calls to the House of Earth Trust.
