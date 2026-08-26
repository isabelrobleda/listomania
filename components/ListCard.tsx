"use client";

import Link from "next/link";
import StrokeBar from "./StrokeBar";
import { useProgress, useSaved, listId } from "@/lib/progress";
import { KIND_MEANING, type List, type Shelf } from "@/lib/content";

export default function ListCard({ shelf, list }: { shelf: Shelf; list: List }) {
  const { count } = useProgress();
  const { count: savedCount } = useSaved();
  const id = listId(shelf.slug, list.slug);
  const done = count(id);
  const pct = Math.round((done / list.rows.length) * 100);

  return (
    <Link className="card" href={`/${shelf.slug}/${list.slug}`}>
      <span className="kicker">
        <span className="kind" title={KIND_MEANING[list.kind]}>
          {list.kind}
        </span>
        {shelf.name}
      </span>
      <h3>{list.title}</h3>
      <span className="desc">{list.desc}</span>
      <StrokeBar color={shelf.mark} pct={list.noTick ? 0 : pct} />
      <span className="meta">
        {list.noTick ? (
          <>
            <span>{list.rows.length.toLocaleString()} to pick from</span>
            <span>{savedCount(id) || 0} saved</span>
          </>
        ) : (
          <>
            <span>
              {done} / {list.rows.length} {list.verb}
            </span>
            <span>{pct}%</span>
          </>
        )}
      </span>
    </Link>
  );
}
