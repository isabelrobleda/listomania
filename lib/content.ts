import shelvesData from "@/content/shelves.json";

/**
 * The lists are content, not user data: they live in the repo as JSON, so they're
 * versioned, diffable and reviewable in a pull request. Nothing here needs a database.
 * The only thing that varies per person is which items you've marked off, and that
 * lives in the browser.
 */

export type Link = { url: string; label: string };

export type Row = {
  key: string;          // stable identity for an item, used for progress
  lead: string;         // leftmost data column (a year, or a mention count)
  sec: string;          // secondary (artist, author, director, city)
  pri: string;          // the thing itself (album, book, film, museum)
  extra?: string;       // free text in the last column
  yt?: string;          // YouTube search query, if the row is watchable/listenable
  ytWord?: string;      // "Trailer" | "Listen"
  src?: Link;           // where this row came from
  links?: Link[];       // several sources
};

export type Source = { url: string; label: string; q: string; meta: string };

export type List = {
  slug: string;
  title: string;
  kind: "Canon" | "Tally" | "Seed" | "Derived";
  verb: string;
  desc: string;
  cols: string[];
  rows: Row[];
  sources?: Source[];
  note?: string;
  action?: { url: string; label: string };
  /** Books lists get a Goodreads lookup per row. The value names which column
   *  holds the author, because it isn't the same one in every list. */
  gr?: "sec" | "extra";
  /** "Asked in" is right for a thread and wrong for a saved list. */
  srcLabel?: string;
};

export type Shelf = {
  slug: string;
  name: string;
  mark: string;      // the shelf's marker colour
  on: string;        // text that sits on top of the marker colour
  soft: string;      // tinted row background, light theme
  softDark: string;  // and dark
  blurb: string;
  lists: List[];
};

export const shelves = shelvesData as Shelf[];

export const KIND_MEANING: Record<List["kind"], string> = {
  Canon: "Someone decided this list",
  Tally: "Strangers voted this into being",
  Seed: "A start, not the finished list",
  Derived: "Computed from the other lists",
};

export function getShelf(slug: string): Shelf | undefined {
  return shelves.find((s) => s.slug === slug);
}

export function getList(shelfSlug: string, listSlug: string) {
  const shelf = getShelf(shelfSlug);
  const list = shelf?.lists.find((l) => l.slug === listSlug);
  return shelf && list ? { shelf, list } : undefined;
}

export function totals() {
  const lists = shelves.reduce((n, s) => n + s.lists.length, 0);
  const items = shelves.reduce(
    (n, s) => n + s.lists.reduce((m, l) => m + l.rows.length, 0),
    0
  );
  return { shelves: shelves.length, lists, items };
}

/** A YouTube search, not a video id: trailers get taken down, re-uploaded and
 *  region-locked, and a search never rots. */
/** Like the YouTube links, a search rather than a book id: editions get merged,
 *  split and re-numbered on Goodreads, and a search survives all of that. */
export function goodreads(query: string) {
  return "https://www.goodreads.com/search?q=" + encodeURIComponent(query);
}

export function youtube(query: string) {
  return "https://www.youtube.com/results?search_query=" + encodeURIComponent(query);
}
