"use client";

import Link from "next/link";
import StrokeBar from "./StrokeBar";
import { useProgress, listId } from "@/lib/progress";
import { KIND_MEANING, type List, type Shelf } from "@/lib/content";

export default function ListCard({ shelf, list }: { shelf: Shelf; list: List }) {
  const { count } = useProgress();
  const done = count(listId(shelf.slug, list.slug));
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
      <StrokeBar color={shelf.mark} pct={pct} />
      <span className="meta">
        <span>
          {done} / {list.rows.length} {list.verb}
        </span>
        <span>{pct}%</span>
      </span>
    </Link>
  );
}
