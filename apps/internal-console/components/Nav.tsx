import Link from "next/link";

const links = [
  { href: "/", label: "Overview" },
  { href: "/knowledge-base", label: "Knowledge Base" },
  { href: "/field-packets", label: "Field Packets" },
  { href: "/review", label: "Review" },
  { href: "/reports", label: "Reports" },
];

export function Nav() {
  return (
    <header className="border-b border-earth-sand bg-earth-green text-earth-sandlight">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-3">
          <span className="text-lg font-bold tracking-wide">KASAMOR</span>
          <span className="hidden text-xs uppercase tracking-widest text-earth-sand sm:inline">
            Internal Console
          </span>
        </Link>
        <nav className="flex gap-4 text-sm">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className="rounded px-2 py-1 hover:bg-earth-deep/40"
            >
              {l.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
