"use client";

import Link from "next/link";
import { shelves } from "@/lib/content";
import { useSaved, listId } from "@/lib/progress";
import { countSaved } from "@/lib/saved";

/**
 * Sits first in the directory, because the thing you came back for is your own
 * list, not the twelfth crowd tally. Shelves you haven't saved anything on stay
 * out of it — an index of empty pages is worse than no index.
 */
export default function MyLists() {
  const { keys } = useSaved();

  const mine = shelves
    .map((s) => ({
      shelf: s,
      // Things, not saves: the same book from three tallies is one line here.
      n: countSaved(s, (slug) => keys(listId(s.slug, slug))),
    }))
    .filter((m) => m.n > 0);

  const total = mine.reduce((t, m) => t + m.n, 0);

  return (
    <section className="clsec mylists">
      <h2>
        <span className="dot" />
        My lists
        {total > 0 && <span className="tot">{total}</span>}
      </h2>

      {mine.length === 0 ? (
        <p className="clblurb">
          Bookmark a row on any list and it lands here, one list per shelf.
        </p>
      ) : (
        <ul>
          {mine.map(({ shelf, n }) => (
            <li key={shelf.slug}>
              <Link href={`/${shelf.slug}/my-list`}>
                <span className="sq" style={{ background: shelf.mark }} />
                <span className="t">My {shelf.name.toLowerCase()} list</span>
                <span className="n">{n}</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
