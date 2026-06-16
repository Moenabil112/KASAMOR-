// Knowledge-base module: types + bundled mock data fallback.

export interface KnowledgeSummary {
  document_count: number;
  chunk_count: number;
  domains: Record<string, number>;
  sensitivity_counts: Record<string, number>;
  document_types: Record<string, number>;
  ingested: boolean;
}

export interface SearchResult {
  chunk_id: string;
  source_file: string;
  section_title: string | null;
  knowledge_domain: string | null;
  sensitivity_level: string | null;
  score: number;
  snippet: string;
}

// Mirrors a typical ingestion of the clean base knowledge package.
export const mockKnowledgeSummary: KnowledgeSummary = {
  document_count: 23,
  chunk_count: 176,
  domains: {
    concept: 47,
    economic: 36,
    field: 31,
    technical: 23,
    academic: 17,
    governance: 9,
    partner: 6,
    risk: 5,
    geospatial: 2,
  },
  sensitivity_counts: { PARTNER: 87, INTERNAL: 87, RESTRICTED: 2 },
  document_types: {
    master_concept: 1,
    academic_blueprint: 1,
    field_protocol: 1,
    technical_blueprint: 1,
    governance: 1,
    geospatial: 2,
    figure: 6,
  },
  ingested: true,
};

const MOCK_CHUNKS: SearchResult[] = [
  {
    chunk_id: "KSM-KB-0026",
    source_file: "01_KASAMOR_Master_Concept_and_Ecosystem_Architecture.docx",
    section_title: "House of Earth Trust Block",
    knowledge_domain: "concept",
    sensitivity_level: "PARTNER",
    score: 11.3,
    snippet:
      "The House of Earth Trust is the expert and evidence layer. It preserves geological memory, private research, maps, expert review and the confidence gate for all field findings.",
  },
  {
    chunk_id: "KSM-KB-0041",
    source_file: "03_KASAMOR_Field_Intelligence_Operating_Protocol.docx",
    section_title: "Stakeholders",
    knowledge_domain: "field",
    sensitivity_level: "INTERNAL",
    score: 9.8,
    snippet:
      "Rural contributors capture voice, photos, location and seasonal observation. Reviewers and local partners interact around evidence and learning.",
  },
];

export function mockSearch(query: string) {
  const q = query.toLowerCase();
  const results = MOCK_CHUNKS.filter(
    (c) =>
      c.snippet.toLowerCase().includes(q) ||
      (c.section_title ?? "").toLowerCase().includes(q) ||
      q.length < 3
  );
  return {
    query,
    result_count: results.length || MOCK_CHUNKS.length,
    results: results.length ? results : MOCK_CHUNKS,
  };
}
