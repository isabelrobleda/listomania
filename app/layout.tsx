import type { Metadata } from "next";
import Link from "next/link";
import Wordmark from "@/components/Wordmark";
import Rail from "@/components/Rail";
import "./globals.css";

const SITE = "https://listomania-nine.vercel.app";

const DESCRIPTION =
  "Canons, crowd tallies and things to get through — kept as lists you can actually work your way down.";

export const metadata: Metadata = {
  // Lets every page's relative OG image and canonical URL resolve properly.
  metadataBase: new URL(SITE),
  title: {
    default: "Listomania — an encyclopedia of lists",
    template: "%s",
  },
  description: DESCRIPTION,
  applicationName: "Listomania",
  openGraph: {
    title: "Listomania",
    description: DESCRIPTION,
    url: SITE,
    siteName: "Listomania",
    type: "website",
    locale: "en",
  },
  twitter: {
    card: "summary_large_image",
    title: "Listomania",
    description: DESCRIPTION,
  },
  robots: { index: true, follow: true },
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
