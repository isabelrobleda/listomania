"use client";

import { shelves, totals } from "@/lib/content";
import { useProgress, listId } from "@/lib/progress";

export default function Stats() {
  const { count } = useProgress();
  const t = totals();
  const done = shelves.reduce(
    (n, s) => n + s.lists.reduce((m, l) => m + count(listId(s.slug, l.slug)), 0),
    0
  );

  const cells: [number, string][] = [
    [t.shelves, "Shelves"],
    [t.lists, "Lists"],
    [t.items, "Items"],
    [done, "Marked off"],
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
