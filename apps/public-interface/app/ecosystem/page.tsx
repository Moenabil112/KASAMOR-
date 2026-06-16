import { site } from "@/content/site";
import { Section } from "@/components/Section";

export const metadata = { title: "The Ecosystem — KASAMOR" };

export default function EcosystemPage() {
  return (
    <>
      <Section eyebrow="The ecosystem" heading="A responsible knowledge loop">
        <p className="lead max-w-prose">{site.ecosystem.intro}</p>
      </Section>

      <Section tinted>
        <div className="grid gap-6 md:grid-cols-2">
          {site.ecosystem.layers.map((l, i) => (
            <div key={l.title} className="card flex gap-4">
              <div className="text-2xl font-bold text-earth-gold">{i + 1}</div>
              <div>
                <h3 className="font-semibold text-earth-green">{l.title}</h3>
                <p className="mt-2 text-sm text-earth-charcoal/75">{l.body}</p>
              </div>
            </div>
          ))}
        </div>
      </Section>

      <Section eyebrow="Field intelligence" heading={site.fieldIntelligence.heading}>
        <p className="lead max-w-prose">{site.fieldIntelligence.body}</p>
        <div className="mt-6 flex flex-wrap gap-2">
          {site.fieldIntelligence.chips.map((c) => (
            <span
              key={c}
              className="rounded-full border border-earth-sand bg-white/70 px-4 py-1.5 text-sm text-earth-green"
            >
              {c}
            </span>
          ))}
        </div>
      </Section>

      <Section eyebrow="Protection & expertise" heading={site.trust.heading} tinted>
        <p className="lead max-w-prose">{site.trust.body}</p>
      </Section>
    </>
  );
}
