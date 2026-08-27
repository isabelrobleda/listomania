import { sameThing, type Shelf } from "@/lib/content";

/**
 * How many *things* are on a shelf's personal list, as opposed to how many
 * saves. One book saved from three tallies is one thing, and every count on the
 * site has to agree about that or the numbers contradict each other on the way
 * to the page that shows them.
 */
export function countSaved(shelf: Shelf, keysFor: (listSlug: string) => string[]) {
  const seen = new Set<string>();
  for (const list of shelf.lists) {
    const chosen = new Set(keysFor(list.slug));
    for (const row of list.rows) {
      if (chosen.has(row.key)) seen.add(sameThing(list, row));
    }
  }
  return seen.size;
}
