import type { Metadata } from "next";
import Link from "next/link";
import Wordmark from "@/components/Wordmark";
import Rail from "@/components/Rail";
import "./globals.css";

export const metadata: Metadata = {
  title: "Listomania — an encyclopedia of lists",
  description:
    "Canons, crowd tallies and things to get through — kept as lists you can actually work your way down.",
  openGraph: {
    title: "Listomania",
    description: "An encyclopedia of lists.",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <a className="skip" href="#main">
          Skip to content
        </a>
        <header className="topbar">
          <Link className="wmbtn" href="/" aria-label="Listomania — all lists">
            <Wordmark />
          </Link>
          <span className="tag">An encyclopedia of lists</span>
        </header>
        <div className="wrap">
          <Rail />
          <main className="main" id="main">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
