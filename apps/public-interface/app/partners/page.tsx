import { site } from "@/content/site";
import { Section } from "@/components/Section";

export const metadata = { title: "Partners — KASAMOR" };

export default function PartnersPage() {
  return (
    <>
      <Section eyebrow="Join us" heading={site.partners.heading}>
        <p className="lead max-w-prose">{site.partners.body}</p>
      </Section>

      <Section tinted>
        <div className="grid gap-6 md:grid-cols-2">
          {site.partners.audiences.map((a) => (
            <div key={a.title} className="card">
              <h3 className="font-semibold text-earth-green">{a.title}</h3>
              <p className="mt-2 text-sm text-earth-charcoal/75">{a.body}</p>
            </div>
          ))}
        </div>
      </Section>

      <Section eyebrow="Principles" heading="How we work with partners">
        <ul className="space-y-3 text-earth-charcoal/80">
          <li className="flex items-start gap-3">
            <span className="mt-1 h-2 w-2 rounded-full bg-earth-gold" />
            Community benefit and knowledge-based rural livelihoods come first.
          </li>
          <li className="flex items-start gap-3">
            <span className="mt-1 h-2 w-2 rounded-full bg-earth-gold" />
            Sensitive data is protected; nothing operational is published.
          </li>
          <li className="flex items-start gap-3">
            <span className="mt-1 h-2 w-2 rounded-full bg-earth-gold" />
            Expert review by the House of Earth Trust gates every conclusion.
          </li>
          <li className="flex items-start gap-3">
            <span className="mt-1 h-2 w-2 rounded-full bg-earth-gold" />
            The model is designed to be repeatable across remote regions.
          </li>
        </ul>
      </Section>
    </>
  );
}
