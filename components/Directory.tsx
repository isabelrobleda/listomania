"use client";

import Link from "next/link";
import { useProgress, listId } from "@/lib/progress";
import { KIND_MEANING, type List, type Shelf } from "@/lib/content";

/**
 * One line of the front-page directory. It carries the two numbers that matter
 * — how big the list is, and how far you are into it — and nothing else. The
 * kind badge stays, because "who says so" is the whole premise of the site.
 */
export function ListLine({ shelf, list }: { shelf: Shelf; list: List }) {
  const { count } = useProgress();
  const done = count(listId(shelf.slug, list.slug));

  return (
    <li>
      <Link href={`/${shelf.slug}/${list.slug}`}>
        <span className="t">{list.title}</span>
        <span className="k" title={KIND_MEANING[list.kind]}>
          {list.kind.toLowerCase()}
        </span>
        <span className="n">
          {done > 0 && !list.noTick ? `${done}/` : ""}
          {list.rows.length.toLocaleString()}
        </span>
      </Link>
    </li>
  );
}
