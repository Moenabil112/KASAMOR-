import type { Metadata } from "next";
import "../styles/globals.css";
import { SiteNav } from "@/components/SiteNav";
import { Footer } from "@/components/Footer";

export const metadata: Metadata = {
  title: "KASAMOR — Rural Mineral Intelligence Ecosystem",
  description:
    "KASAMOR is a knowledge ecosystem that helps remote communities turn field knowledge, voice, photos, and seasonal observation into responsible, AI-supported resource understanding — reviewed by the House of Earth Trust.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <SiteNav />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
