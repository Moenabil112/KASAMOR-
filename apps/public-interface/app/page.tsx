import Link from "next/link";
import { site } from "@/content/site";
import { Section, Diagram } from "@/components/Section";

export default function HomePage() {
  return (
    <>
      {/* 1. Hero */}
      <section className="bg-earth-green text-earth-sandlight">
        <div className="mx-auto max-w-5xl px-6 py-24">
          <p className="eyebrow text-earth-gold">{site.hero.subtitle}</p>
          <h1 className="mt-4 text-5xl font-bold tracking-wide md:text-6xl">
            {site.hero.title}
          </h1>
          <p className="mt-6 max-w-prose text-xl text-earth-sand">{site.hero.line}</p>
          <div className="mt-8 flex gap-4">
            <Link
              href="/ecosystem"
              className="rounded-full bg-earth-gold px-6 py-3 text-sm font-semibold text-earth-deep hover:bg-earth-goldmuted"
            >
              Explore the ecosystem
            </Link>
            <Link
              href="/how-it-works"
              className="rounded-full border border-earth-sand/50 px-6 py-3 text-sm font-semibold hover:bg-earth-deep/40"
            >
              How it works
            </Link>
          </div>
        </div>
      </section>

      {/* 2. What is KASAMOR */}
      <Section eyebrow="Overview" heading={site.whatIs.heading}>
        <p className="lead max-w-prose">{site.whatIs.body}</p>
      </Section>

      {/* 3. The Problem */}
      <Section eyebrow="Why it matters" heading={site.problem.heading} tinted>
        <p className="lead max-w-prose">{site.problem.body}</p>
      </Section>

      {/* 4. The Ecosystem */}
      <Section eyebrow="Five layers" heading={site.ecosystem.heading}>
        <p className="lead max-w-prose">{site.ecosystem.intro}</p>
        <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {site.ecosystem.layers.map((l) => (
            <div key={l.title} className="card">
              <h3 className="font-semibold text-earth-green">{l.title}</h3>
              <p className="mt-2 text-sm text-earth-charcoal/75">{l.body}</p>
            </div>
          ))}
        </div>
      </Section>

      {/* 5. How It Works (flow) */}
      <Section eyebrow="The loop" heading={site.howItWorks.heading} tinted>
        <Diagram nodes={site.howItWorks.steps.map((s) => s.title)} />
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {site.howItWorks.steps.map((s) => (
            <div key={s.title} className="card">
              <h3 className="font-semibold text-earth-green">{s.title}</h3>
              <p className="mt-2 text-sm text-earth-charcoal/75">{s.body}</p>
            </div>
          ))}
        </div>
      </Section>

      {/* 6. House of Earth Trust */}
      <Section eyebrow="Protection & expertise" heading={site.trust.heading}>
        <p className="lead max-w-prose">{site.trust.body}</p>
      </Section>

      {/* 7. Rural Field Intelligence */}
      <Section eyebrow="From the field" heading={site.fieldIntelligence.heading} tinted>
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

      {/* 8. MVP Study Area */}
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

      {/* 9. Development & Economic Value */}
      <Section eyebrow="Value" heading={site.value.heading} tinted>
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

      {/* 10. Partner Call */}
      <Section eyebrow="Join us" heading={site.partners.heading}>
        <p className="lead max-w-prose">{site.partners.body}</p>
        <Link
          href="/partners"
          className="mt-6 inline-block rounded-full bg-earth-green px-6 py-3 text-sm font-semibold text-earth-sandlight hover:bg-earth-deep"
        >
          Partner with KASAMOR
        </Link>
      </Section>
    </>
  );
}
