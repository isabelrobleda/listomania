"use client";

import Link from "next/link";
import { shelves } from "@/lib/content";
import { useSaved, useFavourites, listId } from "@/lib/progress";
import { useEntries } from "@/lib/entries";
import { countSaved } from "@/lib/saved";

/**
 * Sits first in the directory, because the thing you came back for is your own
 * list, not the twelfth crowd tally. Shelves you haven't touched stay out of it
 * — an index of empty pages is worse than no index.
 *
 * Two kinds of line, kept apart: what you *saved* from other people's lists,
 * and what you *added* yourself. Merging the counts would be tidier and would
 * quietly claim that bookmarking a stranger's recommendation and writing down
 * your own favourite are the same act. They aren't, and this whole site is an
 * argument that the difference is worth stating.
 */
export default function MyLists() {
  const { keys } = useSaved();
  const { count: mineCount } = useEntries();
  const { keys: starKeys } = useFavourites();

  const rows = shelves
    .map((s) => ({
      shelf: s,
      // Things, not saves: the same book from three tallies is one line here.
      saved: countSaved(s, (slug) => keys(listId(s.slug, slug))),
      own: mineCount(s.slug) + countSaved(s, (slug) => starKeys(listId(s.slug, slug))),
    }))
    .filter((m) => m.saved > 0 || m.own > 0);

  const total = rows.reduce((t, m) => t + m.saved + m.own, 0);

  return (
    <section className="clsec mylists">
      <h2>
        <span className="dot" />
        My lists
        {total > 0 && <span className="tot">{total}</span>}
      </h2>

      {rows.length === 0 ? (
        <p className="clblurb">
          Bookmark a row to come back to it, star one you loved, or write in something the lists
          missed. It all lands here, one page per shelf.
        </p>
      ) : (
        <ul>
          {rows.map(({ shelf, saved, own }) => (
            <li key={shelf.slug}>
              {saved > 0 && (
                <Link href={`/${shelf.slug}/my-list`}>
                  <span className="sq" style={{ background: shelf.mark }} />
                  <span className="t">My {shelf.name.toLowerCase()} list</span>
                  <span className="n">{saved}</span>
                </Link>
              )}
              {own > 0 && (
                <Link href={`/${shelf.slug}/my-favourites`}>
                  <span className="sq" style={{ background: shelf.mark }} />
                  <span className="t">My {shelf.name.toLowerCase()} favourites</span>
                  <span className="n">{own}</span>
                </Link>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
