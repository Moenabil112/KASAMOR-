export function Section({
  eyebrow,
  heading,
  children,
  tinted,
}: {
  eyebrow?: string;
  heading?: string;
  children: React.ReactNode;
  tinted?: boolean;
}) {
  return (
    <section className={tinted ? "bg-white/40" : ""}>
      <div className="section">
        {eyebrow && <p className="eyebrow">{eyebrow}</p>}
        {heading && (
          <h2 className="mt-2 text-2xl font-bold text-earth-green md:text-3xl">{heading}</h2>
        )}
        <div className="mt-5">{children}</div>
      </div>
    </section>
  );
}

export function Diagram({ nodes }: { nodes: string[] }) {
  // A calm, abstract flow diagram — no maps, no coordinates.
  return (
    <div className="flex flex-wrap items-center gap-3">
      {nodes.map((n, i) => (
        <div key={n} className="flex items-center gap-3">
          <span className="rounded-full border border-earth-sand bg-earth-sandlight px-4 py-2 text-sm font-medium text-earth-green">
            {n}
          </span>
          {i < nodes.length - 1 && <span className="text-earth-goldmuted">→</span>}
        </div>
      ))}
    </div>
  );
}
