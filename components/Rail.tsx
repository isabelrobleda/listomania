"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { shelves } from "@/lib/content";
import { useProgress, useSaved, listId } from "@/lib/progress";

const SOON = ["Television", "Talks & video", "Podcasts"];

export default function Rail() {
  const pathname = usePathname();
  const { count } = useProgress();
  const { count: savedCount } = useSaved();

  /** A shelf whose lists can't be finished (music) has nothing to count toward
   *  a total, so it reports what you've saved instead of what you've done. */
  const tally = (slug: string) => {
    const shelf = shelves.find((s) => s.slug === slug)!;
    const saveOnly = shelf.lists.length > 0 && shelf.lists.every((l) => l.noTick);
    if (saveOnly) {
      const n = shelf.lists.reduce((t, l) => t + savedCount(listId(slug, l.slug)), 0);
      return n > 0 ? `${n} saved` : "";
    }
    const done = shelf.lists.reduce((t, l) => t + count(listId(slug, l.slug)), 0);
    const total = shelf.lists.reduce((t, l) => t + l.rows.length, 0);
    return `${done}/${total}`;
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
          <span className="ct">{tally(s.slug)}</span>
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
