"use client";

import Link from "next/link";
import { useProgress, listId } from "@/lib/progress";
import { type List, type Shelf } from "@/lib/content";

/**
 * One line of the front-page directory. It carries the two numbers that matter
 * — how big the list is, and how far you are into it — and nothing else.
 *
 * There used to be a canon/tally/seed badge here too. It was a taxonomy that
 * meant something to whoever wrote it and nothing to anyone reading, and it
 * cost a column in a dense index. Where a list came from and how it was
 * counted is still on the list itself, in a sentence, which is where it was
 * always doing the real work.
 */
export function ListLine({ shelf, list }: { shelf: Shelf; list: List }) {
  const { count } = useProgress();
  const done = count(listId(shelf.slug, list.slug));

  return (
    <li>
      <Link href={`/${shelf.slug}/${list.slug}`}>
        <span className="t">{list.title}</span>
        <span className="n">
          {done > 0 && !list.noTick ? `${done}/` : ""}
          {list.rows.length.toLocaleString()}
        </span>
      </Link>
    </li>
  );
}
