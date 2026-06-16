import { site } from "@/content/site";
import { Section, Diagram } from "@/components/Section";

export const metadata = { title: "How It Works — KASAMOR" };

export default function HowItWorksPage() {
  return (
    <>
      <Section eyebrow="The loop" heading={site.howItWorks.heading}>
        <p className="lead max-w-prose">
          KASAMOR follows one repeatable cycle. Each step adds structure and care,
          and nothing becomes a conclusion without expert review.
        </p>
        <div className="mt-8">
          <Diagram nodes={site.howItWorks.steps.map((s) => s.title)} />
        </div>
      </Section>

      <Section tinted>
        <ol className="space-y-6">
          {site.howItWorks.steps.map((s, i) => (
            <li key={s.title} className="card flex gap-5">
              <div className="text-3xl font-bold text-earth-gold">{i + 1}</div>
              <div>
                <h3 className="text-lg font-semibold text-earth-green">{s.title}</h3>
                <p className="mt-1 text-sm text-earth-charcoal/75">{s.body}</p>
              </div>
            </li>
          ))}
        </ol>
      </Section>

      <Section eyebrow="A note on AI" heading="AI assists — it never decides">
        <p className="lead max-w-prose">
          Artificial intelligence helps structure observations and draft indicative
          summaries. It does not confirm the presence or value of any mineral, and it
          does not replace human judgement. Confidence is set by the House of Earth
          Trust, and sensitive information is never exposed.
        </p>
      </Section>
    </>
  );
}
