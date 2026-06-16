import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t border-earth-sand/60 bg-earth-green text-earth-sandlight">
      <div className="mx-auto max-w-5xl px-6 py-12">
        <div className="flex flex-col gap-6 md:flex-row md:justify-between">
          <div className="max-w-prose">
            <div className="text-lg font-bold tracking-widest">KASAMOR</div>
            <p className="mt-2 text-sm text-earth-sand">
              A rural mineral intelligence ecosystem for responsible resource
              understanding in remote regions.
            </p>
          </div>
          <nav className="flex flex-col gap-2 text-sm">
            <Link href="/ecosystem" className="hover:text-earth-gold">The ecosystem</Link>
            <Link href="/how-it-works" className="hover:text-earth-gold">How it works</Link>
            <Link href="/mvp" className="hover:text-earth-gold">MVP study area</Link>
            <Link href="/partners" className="hover:text-earth-gold">Partner with us</Link>
          </nav>
        </div>
        <p className="mt-10 text-xs text-earth-sand/70">
          This public interface shares only general, non-sensitive information. It
          never exposes precise coordinates, operational points, raw field data, or
          community-sensitive details. Images and observations are documentation —
          they do not confirm the presence or value of any mineral.
        </p>
      </div>
    </footer>
  );
}
