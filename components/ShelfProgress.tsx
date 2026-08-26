"use client";

import StrokeBar from "./StrokeBar";
import { useProgress, listId } from "@/lib/progress";
import type { Shelf } from "@/lib/content";

export default function ShelfProgress({ shelf }: { shelf: Shelf }) {
  const { count } = useProgress();
  const done = shelf.lists.reduce((n, l) => n + count(listId(shelf.slug, l.slug)), 0);
  const total = shelf.lists.reduce((n, l) => n + l.rows.length, 0);
  // A shelf can legitimately hold no lists — between one list being retired and
  // its replacement landing. Dividing by zero there printed "NaN %".
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  return (
    <div className="prog">
      <div className="row">
        <span className="big">
          {done} / {total}
        </span>
        <span className="pct">{pct}%</span>
      </div>
      <StrokeBar color={shelf.mark} pct={pct} height={17} />
    </div>
  );
}
