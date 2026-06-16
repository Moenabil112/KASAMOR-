import type { Metadata } from "next";
import "./globals.css";
import { Nav } from "@/components/Nav";

export const metadata: Metadata = {
  title: "KASAMOR — Internal Console",
  description:
    "Internal operating console for the KASAMOR Rural Mineral Intelligence Ecosystem.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen">
          <Nav />
          <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
          <footer className="mx-auto max-w-6xl px-6 py-10 text-xs text-earth-charcoal/60">
            KASAMOR Internal Console · INTERNAL use only · Raw coordinates and
            contributor identities are never exposed publicly.
          </footer>
        </div>
      </body>
    </html>
  );
}
