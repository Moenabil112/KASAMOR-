import Link from "next/link";

const links = [
  { href: "/ecosystem", label: "Ecosystem" },
  { href: "/how-it-works", label: "How it works" },
  { href: "/mvp", label: "MVP" },
  { href: "/partners", label: "Partners" },
];

export function SiteNav() {
  return (
    <header className="sticky top-0 z-10 border-b border-earth-sand/60 bg-earth-sandlight/85 backdrop-blur">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-baseline gap-2">
          <span className="text-lg font-bold tracking-widest text-earth-green">KASAMOR</span>
          <span className="hidden text-[10px] uppercase tracking-[0.2em] text-earth-goldmuted sm:inline">
            Rural Mineral Intelligence
          </span>
        </Link>
        <nav className="flex gap-5 text-sm text-earth-charcoal/80">
          {links.map((l) => (
            <Link key={l.href} href={l.href} className="hover:text-earth-green">
              {l.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
