import type { Metadata } from "next";
import Link from "next/link";
import Wordmark from "@/components/Wordmark";
import Rail from "@/components/Rail";
import ThemeToggle from "@/components/ThemeToggle";
import ThemeSong from "@/components/ThemeSong";
import NavToggle from "@/components/NavToggle";
import AccountButton from "@/components/AccountButton";
import ClaimBanner from "@/components/ClaimBanner";
import SyncProvider from "@/components/SyncProvider";
import { SessionProvider } from "next-auth/react";
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
    <html lang="en" suppressHydrationWarning>
      <head>
        {/*
          Runs before the first paint: without it a reader who chose dark gets a
          flash of the light page on every navigation, which is worse than not
          offering the choice. Deliberately tiny, inline and dependency-free —
          anything that has to be fetched first is by definition too late.
        */}
        <script
          dangerouslySetInnerHTML={{
            __html:
              "try{var t=localStorage.getItem('listomania:theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t)}catch(e){}",
          }}
        />
      </head>
      <body>
        <SessionProvider>
        <a className="skip" href="#main">
          Skip to content
        </a>
        <header className="topbar">
          <NavToggle />
          <Link className="wmbtn" href="/" aria-label="Listomania — all lists">
            <Wordmark />
          </Link>
          <span className="tag">An encyclopedia of lists</span>
          <AccountButton />
          <ThemeSong />
          <ThemeToggle />
        </header>
        <div className="wrap">
          <Rail />
          <main className="main" id="main">
            <ClaimBanner />
            {children}
          </main>
        </div>
        <SyncProvider />
        </SessionProvider>
      </body>
    </html>
  );
}
