# Listomania

An encyclopedia of lists — canons, crowd tallies, and things to get through.

Live: _(add the Vercel URL once deployed)_

## What this is

Four shelves (Music, Books, Film, Places) holding ten lists and ~1,600 items.
Every list declares what **kind** of authority it has:

| Kind        | Meaning                                  |
| ----------- | ---------------------------------------- |
| **Canon**   | Someone decided this list                |
| **Tally**   | Strangers voted this into being          |
| **Seed**    | A start, not the finished list           |
| **Derived** | Computed from the other lists            |

That distinction is the point of the site. A canon and a crowd tally are
different claims about the world, and each list says which it is, where it came
from, and how it was counted.

## Architecture, and why

**The lists are content, not user data.** They live in `content/shelves.json`,
in the repo. That means every change to a list is a visible, reviewable diff in
a pull request — not an invisible database write. It also means the whole site
prerenders to static HTML: no database, no server, no query latency, nothing to
run out of connections.

**The only per-person state is which items you've marked off**, and in v1 that
lives in the browser (`localStorage`), managed by `lib/progress.ts`. There are no
accounts yet. When accounts arrive, that one file is the only place that has to
learn about a server.

This is a deliberate order of operations: ship the reading experience, add the
backend when there are people to log in.

```
app/
  layout.tsx                 top bar, rail, shell
  page.tsx                   home — shelves and their lists
  [shelf]/page.tsx           one shelf
  [shelf]/[list]/page.tsx    one list
components/
  Wordmark.tsx               the logo, drawn as vector letterforms
  ListTable.tsx              the table: search, filter, marking off
  StrokeBar.tsx              marker stroke — used as heading rule AND progress bar
  Rail.tsx  Stats.tsx  ShelfTheme.tsx  ShelfProgress.tsx  ListCard.tsx
lib/
  content.ts                 types + accessors over the JSON
  progress.ts                the marked-off store
content/
  shelves.json               all the lists
tools/                       scripts that generated the content and the logo
```

## Design notes

- **Colour belongs to the shelf, not the list.** `ShelfTheme` sets `--mark`,
  `--on-mark` and `--mark-soft` on `<main>`, and everything below reads them.
- **The marker stroke does double duty**: it underlines every heading and it *is*
  the progress bar, drawn to the percentage complete. One gesture, two jobs.
- **The wordmark is custom vector letterforms**, not a licensed typeface — each
  glyph is a skeleton of marker strokes with round caps, thickened until the
  counters nearly close. Regenerate with `python3 tools/letters.py`.
- **YouTube links are searches, not video IDs.** Trailers get taken down,
  re-uploaded and region-locked; a search never rots, and it lets you pick the
  right one when a title is ambiguous (*The Staircase* is a doc and a series).

## Running it

```bash
npm install
npm run dev      # http://localhost:3000
npm run build    # prerenders all 18 pages to static HTML
```

## Adding a list

Everything is data. Add an object to the right shelf's `lists` array in
`content/shelves.json`:

```jsonc
{
  "slug": "url-safe-name",
  "title": "Human Readable Name",
  "kind": "Tally",
  "verb": "read",              // "3 / 61 read"
  "desc": "One sentence on what this list is.",
  "cols": ["Said by", "Author", "Title", "Source"],
  "sources": [{ "url": "…", "label": "Reddit · r/books", "q": "the question asked", "meta": "2026 · 400 comments" }],
  "note": "How it was counted, and what it can't tell you.",
  "rows": [{ "key": "stable-id", "lead": "6×", "sec": "Author", "pri": "Title" }]
}
```

`key` is the item's stable identity — it's what progress is stored against, so
changing it resets people's ticks for that row.

Every tally should carry its `note`. Saying how a list was counted, and what it
skews toward, is what separates it from an anonymous internet ranking.

## Deploying

Pushes to `main` deploy automatically once the repo is connected to Vercel.
No environment variables are needed — there's nothing to configure.
