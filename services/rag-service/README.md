# RAG Service

Local-first, dependency-free knowledge retrieval for KASAMOR.

## Files
- `ingest.py` — thin wrapper around `scripts/ingest_base_knowledge.py`.
- `chunking.py` — shared section-splitting and chunking helpers.
- `retrieval.py` — sensitivity-aware keyword retrieval over `knowledge_chunks.jsonl`.

## Usage
```bash
# 1. Ingest (produces data/extracted-knowledge/knowledge_chunks.jsonl)
python3 scripts/ingest_base_knowledge.py --zip /path/to/package.zip

# 2. Query
python3 services/rag-service/retrieval.py "role of the House of Earth Trust"
```

## Retrieval model
`search(query, knowledge_domain=None, max_sensitivity="INTERNAL", top_k=5)` returns
scored chunks. A caller cleared at `max_sensitivity` only sees chunks at that level
or lower (PUBLIC < PARTNER < INTERNAL < RESTRICTED < HOUSE_OF_EARTH_TRUST_ONLY).

## Not included yet
- Embeddings / vector search. `VectorStoreAdapter` marks the seam where a
  `pgvector` or `Qdrant` backend plugs in (selected via `KASAMOR_VECTOR_BACKEND`).
