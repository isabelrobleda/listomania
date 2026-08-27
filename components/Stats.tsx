"use client";

import { shelves, totals } from "@/lib/content";
import { useProgress, listId } from "@/lib/progress";

/**
 * Only the two counts that stay small. "Items" and "Marked off" run to four
 * digits and were the widest things on the page — a number that big reads as a
 * headline whether or not it deserves to be one.
 */
export default function Stats() {
  const t = totals();

  const cells: [number, string][] = [
    [t.shelves, "Shelves"],
    [t.lists, "Lists"],
  ];

  return (
    <div className="stats">
      {cells.map(([n, label]) => (
        <div className="stat" key={label}>
          <div className="n">{n.toLocaleString()}</div>
          <div className="l">{label}</div>
        </div>
      ))}
    </div>
  );
}

export function ShelfCount({ slug }: { slug: string }) {
  const { count } = useProgress();
  const shelf = shelves.find((s) => s.slug === slug)!;
  const done = shelf.lists.reduce((n, l) => n + count(listId(slug, l.slug)), 0);
  const total = shelf.lists.reduce((n, l) => n + l.rows.length, 0);
  return (
    <span className="shelfmeta">
      {shelf.lists.length} list{shelf.lists.length > 1 ? "s" : ""} · {done}/{total}
    </span>
  );
}
