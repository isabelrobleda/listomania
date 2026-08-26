"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { shelves } from "@/lib/content";
import { useProgress, listId } from "@/lib/progress";

const SOON = ["Television", "Talks & video", "Restaurants"];

export default function Rail() {
  const pathname = usePathname();
  const { count } = useProgress();

  const shelfCount = (slug: string) => {
    const shelf = shelves.find((s) => s.slug === slug)!;
    return shelf.lists.reduce((n, l) => n + count(listId(slug, l.slug)), 0);
  };
  const shelfTotal = (slug: string) => {
    const shelf = shelves.find((s) => s.slug === slug)!;
    return shelf.lists.reduce((n, l) => n + l.rows.length, 0);
  };

  return (
    <nav className="rail" aria-label="Shelves">
      <Link className="navb" href="/" aria-current={pathname === "/" ? "true" : undefined}>
        <span className="swatch" style={{ background: "var(--ink)" }} />
        Everything
      </Link>

      <div className="railsec">Shelves</div>
      {shelves.map((s) => (
        <Link
          key={s.slug}
          className="navb"
          href={`/${s.slug}`}
          aria-current={pathname.startsWith(`/${s.slug}`) ? "true" : undefined}
        >
          <span className="swatch" style={{ background: s.mark }} />
          {s.name}
          <span className="ct">
            {shelfCount(s.slug)}/{shelfTotal(s.slug)}
          </span>
        </Link>
      ))}

      <div className="railsec">Coming next</div>
      {SOON.map((name) => (
        <span className="navb soon" key={name}>
          <span className="swatch" style={{ background: "transparent" }} />
          {name}
        </span>
      ))}
    </nav>
  );
}
