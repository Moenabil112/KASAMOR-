# Agent Orchestrator

Runs the six KASAMOR agents as a provider-agnostic pipeline. The MVP ships a
**deterministic mock backend** so everything works without API keys.

## Files
- `registry.py` — agent-id → callable map, backend selection, `run_pipeline()`.
- `agents/mock_agents.py` — deterministic mock implementations of all six agents.
- `workflows/field_packet_workflow.py` — declarative stage description.

## Pipeline (default)
```
field_packet_intake → photo_quality → voice_to_knowledge
       → geo_photo_voice_fusion → house_of_earth_trust_review
```

## Run
```bash
python3 services/agent-orchestrator/registry.py
```

## Backend selection
`KASAMOR_AGENT_MODE=mock` (default) uses `MOCK_REGISTRY`. A future `live` mode
registers the same agent ids with real, provider-agnostic model calls — no
changes needed in the API or report generator.
