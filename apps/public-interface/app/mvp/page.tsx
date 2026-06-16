import { site } from "@/content/site";
import { Section } from "@/components/Section";

export const metadata = { title: "MVP Study Area — KASAMOR" };

export default function MvpPage() {
  return (
    <>
      <Section eyebrow="Controlled pilot" heading={site.mvp.heading}>
        <p className="lead max-w-prose">{site.mvp.body}</p>
        <ul className="mt-6 space-y-2">
          {site.mvp.points.map((p) => (
            <li key={p} className="flex items-start gap-3 text-earth-charcoal/80">
              <span className="mt-1 h-2 w-2 rounded-full bg-earth-gold" />
              {p}
            </li>
          ))}
        </ul>
      </Section>

      {/* Abstract, non-operational area representation — deliberately not a map. */}
      <Section tinted>
        <div className="card flex flex-col items-center justify-center py-16 text-center">
          <div className="flex h-40 w-40 items-center justify-center rounded-full border-4 border-dashed border-earth-sand">
            <div className="text-center">
              <div className="text-2xl font-bold text-earth-green">~180 km²</div>
              <div className="text-xs uppercase tracking-widest text-earth-goldmuted">
                study area
              </div>
            </div>
          </div>
          <p className="mt-6 max-w-prose text-sm text-earth-charcoal/70">
            This is an abstract representation of the pilot's scale — not a map. KASAMOR
            does not publish precise coordinates, operational points, or sensitive field
            locations. The study area exists to refine and prove the model responsibly.
          </p>
        </div>
      </Section>

      <Section eyebrow="Value" heading={site.value.heading}>
        <p className="lead max-w-prose">{site.value.body}</p>
        <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {site.value.points.map((p) => (
            <div key={p.title} className="card">
              <h3 className="font-semibold text-earth-green">{p.title}</h3>
              <p className="mt-2 text-sm text-earth-charcoal/75">{p.body}</p>
            </div>
          ))}
        </div>
      </Section>
    </>
  );
}
