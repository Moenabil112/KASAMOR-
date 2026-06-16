// KASAMOR public content. PUBLIC sensitivity only.
// Structured English-first; the object shape is ready for an `ar` variant later.
// NOTHING here exposes coordinates, target points, raw field data, or claims that
// images can confirm mineral value.

export const site = {
  name: "KASAMOR",
  tagline: "Rural Mineral Intelligence Ecosystem",
  hero: {
    title: "KASAMOR",
    subtitle: "Rural Mineral Intelligence Ecosystem",
    line: "From field knowledge to AI-supported rural resource intelligence.",
  },

  whatIs: {
    heading: "What is KASAMOR?",
    body: "KASAMOR is a knowledge ecosystem for remote communities. It helps people document, structure, and responsibly understand the natural mineral resources within their own environment — combining local field knowledge, mobile photos, voice notes, seasonal observation, geospatial context, and expert-backed review.",
  },

  problem: {
    heading: "The Problem",
    body: "Rural mineral activity often depends on scattered knowledge, informal observation, and limited access to structured tools. Valuable local experience is rarely recorded, rarely connected to expert insight, and rarely turned into something a community can learn from over time.",
  },

  ecosystem: {
    heading: "The Ecosystem",
    intro: "KASAMOR connects five layers into one responsible knowledge loop.",
    layers: [
      {
        title: "Community knowledge",
        body: "Local names, seasonal memory, and traditional observation are treated as primary evidence.",
      },
      {
        title: "Mobile voice & photos",
        body: "Contributors capture what they see and know using simple phones — voice notes and field photos.",
      },
      {
        title: "AI field intelligence",
        body: "AI helps structure observations into consistent, comparable field knowledge. It assists; it never decides.",
      },
      {
        title: "House of Earth Trust",
        body: "An expert review layer that protects sensitive knowledge and gates confidence before anything is acted on.",
      },
      {
        title: "Responsible resource understanding",
        body: "The goal is understanding and stewardship — not speculation, not extraction targeting.",
      },
    ],
  },

  howItWorks: {
    heading: "How It Works",
    steps: [
      { title: "Capture", body: "Contributors record voice, photos, location context, and seasonal observation." },
      { title: "Structure", body: "Observations become a Field Packet — one consistent, structured record." },
      { title: "Interpret", body: "AI produces an indicative observation summary grounded in base knowledge." },
      { title: "Review", body: "The House of Earth Trust reviews evidence and decides next steps." },
      { title: "Learn", body: "Each reviewed packet improves shared understanding of the area." },
      { title: "Replicate", body: "The same model is repeated in new remote regions." },
    ],
  },

  trust: {
    heading: "House of Earth Trust",
    body: "The House of Earth Trust is the ecosystem's expert and protection layer. It preserves geological memory and private research, reviews field evidence, sets confidence levels, and ensures sensitive information is never exposed. No observation becomes a conclusion without human, expert-backed review.",
  },

  fieldIntelligence: {
    heading: "Rural Field Intelligence",
    body: "Field intelligence is built from many simple signals: voice notes in local dialects, photos with context, general location, local place names, seasonal flow, and sediment and rock documentation. Together they form a richer, more reliable picture than any single observation.",
    chips: [
      "Voice notes",
      "Field photos",
      "General location",
      "Local place names",
      "Seasonal observation",
      "Sediment documentation",
      "Rock context",
    ],
  },

  mvp: {
    heading: "MVP Study Area",
    body: "The first KASAMOR pilot focuses on a controlled study area of approximately 180 km². It is a learning ground for the model — not a target map. The public interface deliberately shows no precise coordinates, no operational points, and no sensitive field locations.",
    points: [
      "Approx. 180 km² controlled pilot area",
      "Used to refine capture, structuring, and review",
      "No sensitive coordinates are ever published",
    ],
  },

  value: {
    heading: "Development & Economic Value",
    body: "By turning scattered observation into structured knowledge, KASAMOR helps reduce randomness in the field and supports better, safer decisions.",
    points: [
      { title: "Reduce randomness", body: "Replace guesswork with structured, comparable field evidence." },
      { title: "Improve field decisions", body: "Give reviewers and communities a clearer basis for next steps." },
      { title: "Support rural livelihoods", body: "Build knowledge-based value around local experience." },
      { title: "Create repeatable systems", body: "Produce data systems that can be reused across regions." },
    ],
  },

  partners: {
    heading: "Partner Call",
    body: "KASAMOR welcomes academic, technical, development, and responsible-resource partners who share its commitment to community benefit, data protection, and responsible resource understanding.",
    audiences: [
      { title: "Academic", body: "Geoscience, social science, and rural development researchers." },
      { title: "Technical", body: "AI, geospatial, and data-engineering collaborators." },
      { title: "Development", body: "Organisations supporting knowledge-based rural livelihoods." },
      { title: "Responsible resource", body: "Partners committed to ethical, transparent resource stewardship." },
    ],
  },
};

export type Site = typeof site;
