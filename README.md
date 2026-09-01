# Listomania

An encyclopedia of lists — canons, crowd tallies, and things to get through.

**Live: https://listomania-nine.vercel.app**

## What this is

Five shelves (Music, Books, Film, Places, Television) holding 24 lists and 5,539
items.
Every list says where it came from and how it was counted, in a sentence, on
the list itself. That sentence is the point of the site: a canon and a crowd
tally are different claims about the world, and the difference is only worth
anything when it's spelled out.

There used to be a `canon` / `tally` / `seed` / `derived` badge beside every
title as well. It's gone. A four-word taxonomy meant something to whoever wrote
it and nothing to anyone reading — you cannot tell from the word "tally" whether
strangers voted once or three hundred times — and it cost a column in an index
whose whole virtue is density. The `kind` field stays in `shelves.json` because
`tools/agreed.py` uses it to decide which Books lists to compute the derived
list from; it just isn't shown to anyone.

## Architecture, and why

**The lists are content, not user data.** They live in `content/shelves.json`,
in the repo. That means every change to a list is a visible, reviewable diff in
a pull request — not an invisible database write. It also means the whole site
prerenders to static HTML: no database, no server, no query latency, nothing to
run out of connections.

**Accounts are optional, and the site works without one.** Signed out, your
marks live in this browser. Signed in, they live in Postgres and follow you
between devices. With no `DATABASE_URL` set the whole auth layer switches off
and the site still builds and runs — a fork or a local checkout needs no
secrets.

**Per-person state is two things, kept apart on purpose**, and in v1 both live
in the browser (`localStorage`), managed by `lib/progress.ts`:

| | | |
| --- | --- | --- |
| **done** | the tick at the left of a row | a fact about the past — "I've read this" |
| **want** | the bookmark at the right | an intention about the future — "put it on my list" |
| **fav** | the star, inside the row | a judgement — "this one is mine" |

They are not one tri-state control, or one control cycling through three. You can want to reread something you've
already read, and un-ticking a row shouldn't quietly throw away the reason you
saved it. Saved rows collect on `/{shelf}/my-list`, which stores nothing of its
own — it resolves the saved keys back against the content, so a personal list
can never drift out of sync with the list it came from.

The star is the only one that implies another: starring marks a row done as
well, because calling a film a favourite you haven't seen isn't a thing anyone
means. Un-starring never un-ticks — forgetting you watched it isn't implied by
changing your mind about it. The star sits *inside* the row rather than beside
the bookmark at the edge: the bookmark is housekeeping and the star is an
opinion, and two identical pills side by side invite pressing the wrong one.

Some lists set `"noTick": true` (all six music lists do). You don't *finish* a
song the way you finish a book, so those drop the tick entirely and keep only
the saving — and their shelf reports "N saved" rather than a percentage.

When accounts arrived, `lib/progress.ts` was the only file that had to learn
about a server — which was the point of writing it that way. The two copies sit
*side by side* rather than merged: what a browser held before anyone signed in
stays put until someone claims it, which is what stops a shared laptop handing
one person's reading history to whoever logs in next.

**A personal list holds one copy of a thing.** The same book is a different row
in every tally it appears in — right for the lists, where each row is that
crowd's answer, wrong for your list. `sameThing()` in `lib/content.ts` decides
what counts as the same: title plus the author where a list has one, plus the
year where it doesn't (so two films called *The Thing* stay two films), with
accents and punctuation folded. Every count on the site uses it via
`countSaved()`, because a shelf that says 6 leading to a page that shows 3 is
worse than either number alone. Removing a merged row removes it from every list
it was saved from — otherwise one click leaves a copy behind that reappears
tomorrow as a duplicate.

What it can't fix: two lists spelling an author differently ("Dostoevsky" and
"Dostoyevsky") are still two things.

Sync is **per-item toggles, not a state blob**. A "save everything" endpoint is
how someone loses a phone's worth of bookmarks because a stale laptop tab
flushed an old copy; a toggle can't do that, and the primary key on
`(user, kind, list, item)` makes every write idempotent and safe to retry.

```
app/
  layout.tsx                 top bar, rail, shell
  page.tsx                   home — the directory of every list
  [shelf]/page.tsx           one shelf
  [shelf]/[list]/page.tsx    one list
components/
  Wordmark.tsx               the logo, drawn as vector letterforms
  ListTable.tsx              the table: search, filter, marking off
  StrokeBar.tsx              marker stroke — used as heading rule AND progress bar
  Directory.tsx              the front-page index lines
  SavedList.tsx              one shelf's saved rows
  ThemeToggle.tsx            light / dark / system
  ThemeSong.tsx              the Phoenix chorus, on demand
  NavToggle.tsx              the shelf drawer, on phones
  Rail.tsx  Stats.tsx  ShelfTheme.tsx  ShelfProgress.tsx  ListCard.tsx
lib/
  content.ts                 types + accessors over the JSON
  progress.ts                the two per-person stores: done, and saved
  entries.ts                 the third: things you added yourself
content/
  shelves.json               all the lists
tools/                       scripts that generated the content and the logo
```

## Your own entries

`/{shelf}/my-favourites` holds two things that arrive by different doors: rows
you **starred** on someone else's list, and entries you **typed** because no
list here had them. They're shown in two sections rather than merged. Merging
would be tidier and would lose exactly the distinction this site exists to make
— one of them is you agreeing with a crowd, the other is you on your own.

The typed half is the shelf's blank page: the things you'd have said if you'd
been in the thread.

It is deliberately **not** a row you add to an existing tally. A count of one
person is not the same kind of claim as a count of three hundred, and the whole
site is an argument that the difference is worth stating out loud. So your
entries live on their own page, beside the tallies, and never inside one.

This is the third per-person store, and the only one that holds something
irreplaceable:

| | points at | worst case if lost |
| --- | --- | --- |
| **done** / **want** | a row in `shelves.json` | you re-tick it |
| **entries** | nothing — it *is* the content | the text is gone |

That difference drives every decision in `lib/entries.ts`:

- **The id is minted in the browser** (`crypto.randomUUID`), not by the
  database. An entry has to exist before anyone signs in and keep the same
  identity afterwards — a serial assigned at claim time would make claiming a
  browser create a second copy of everything you'd written.
- **Writes are per-entry.** `PUT` upserts by id, so a retried write can't
  duplicate, and no request ever carries your whole list — same reason the marks
  API isn't a state blob.
- **Claiming is additive.** An id already in the account keeps the account's
  copy, so claiming an old browser can never overwrite what you typed on your
  phone this morning.
- **Deleting is two-step**, which nothing else on the site is. Un-ticking a row
  loses a boolean; deleting an entry destroys a paragraph only you have.

The two text fields are named per shelf in `FIELDS` — Title/Author for books,
Film/Director for film, Place/What it is for places — rather than a generic
name/detail pair, so an entry reads like the rows it sits beside and gets the
same Goodreads, YouTube or Maps link.

The third field, the note, is the point of the feature. A tally can tell you a
book was named 31 times and can never tell you why, because counting is exactly
the operation that throws the why away. Here it's the only thing there's room
for.

## Design notes

- **The front page is a directory, not a showcase.** Cards looked good and
  scaled badly — five shelves of them already pushed the newest lists below the
  fold, and every list added made it worse. Columns of plain links (the
  craigslist move) get *denser* as the site grows instead of longer, and the
  counts carry the information the cards were decorating. Counts are
  fixed-width so they form straight columns; a ragged right edge is what makes a
  dense index unscannable.
- **Colour belongs to the shelf, not the list.** `ShelfTheme` sets `--mark`,
  `--on-mark` and `--mark-soft` on `<main>`, and everything below reads them.
- **The marker stroke does double duty**: it underlines every heading and it *is*
  the progress bar, drawn to the percentage complete. One gesture, two jobs.
- **The wordmark is Archivo Black, converted to outlines** by
  `tools/wordmark.py`, with a highlighter swipe behind it. Outlines rather than
  live text: a logo that depends on a webfont loading is briefly the *wrong*
  logo on every cold visit, and the swipe is drawn to these exact letterforms,
  so a fallback face would leave the band hanging off the end of the word. The
  letters are hard-coded dark rather than `var(--ink)` — they sit on lime in
  both themes, and cream on lime is unreadable. (`tools/letters.py` still holds
  the earlier hand-drawn alphabet, kept for reference.)
- **The theme switch has three states, not two.** Light, dark, and *follow my
  system* — the last is a real preference, not the absence of one, and a two-way
  switch would silently pin someone to whichever they last tapped. A tiny inline
  script in `layout.tsx` applies the stored choice before the first paint;
  without it, a reader who chose dark gets a flash of the light page on every
  navigation, which is worse than not offering the choice at all.
- **The top bar is paper, not pink.** Once the lime belongs to the logo, pink is
  free to mean one thing only: the Books shelf.
- **Every book row links out to Goodreads**, and every film and song row to
  YouTube — both as *searches*. A list is worth more when you can act on a row
  without leaving to go look it up. Set `"gr": "sec"` on a books list, or
  `"gr": "extra"` where the author sits in the extra column instead.
- **The top bar is one line on a phone, whatever the username.** It has to hold
  five controls, and the only one that can be shortened without losing anything
  is the name — you know who you're signed in as. So it collapses to its first
  character, taken with `Intl.Segmenter` rather than `name[0]`, which cuts an
  emoji in half; an emoji initial gets a pale disc instead of the black one,
  since half of them vanish on black. Signed out becomes a door glyph. The
  wordmark is the only flexible item in the bar, so whatever width is still
  missing comes out of the logo rather than out of the single line.
- **The rail is a drawer on a phone, not a block above the page.** Stacked, it
  meant every visit opened on a screenful of navigation you had to scroll past
  to reach what you came for. Off-canvas it behaves the way it already does on
  a desktop: there when asked for, gone otherwise. Closed, it's
  `visibility: hidden` as well as translated away — off-canvas is not the same
  as absent, and without it a keyboard tabs into a menu nobody opened. Four
  ways out (button, scrim, Escape, following a link), and the link one matters
  most: a menu that stays open over the page you just chose is how this pattern
  is usually got wrong.
- **A list can be in its own language.** `"lang": "es"` on a list puts the
  handful of interface strings that sit *inside* the table — search box, the
  two filter chips, the empty state — into that language. Everything outside
  the list stays in English, because that's the language of the site, not of
  the list. It is six strings in a `STRINGS` object rather than an i18n
  framework: a framework for six strings is a framework you maintain forever
  for nothing.
- **The top bar plays the theme song.** The site is named after a Phoenix
  record, so there's a button that plays the hook — twenty seconds, then it
  stops on its own. Three rules, in `ThemeSong.tsx`: it never plays on load;
  the player is visible rather than a hidden 0×0 iframe, because that's the
  arrangement YouTube actually offers and because it puts the stop button where
  someone reaching for silence will look; and the iframe isn't created until the
  first press, so nothing is fetched from youtube.com and no cookie of theirs is
  set for a reader who never touches it. This is the one place on the site with
  a hard-coded video ID — a search can't start at 0:51 — so it degrades to a
  plain search link if the upload ever goes away.
- **YouTube links are searches, not video IDs.** Trailers get taken down,
  re-uploaded and region-locked; a search never rots, and it lets you pick the
  right one when a title is ambiguous (*The Staircase* is a doc and a series).

## Running it

```bash
npm install
npm run dev      # http://localhost:3000
npm run build    # prerenders every page to static HTML
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

**Adding a book tally means recomputing the derived list.** Run
`python3 tools/agreed.py` from the repo root — it rebuilds *Agreed Across
Crowds* from every Tally on the Books shelf, matching titles across lists that
punctuate and accent them differently. Skip it and that list quietly claims to
cover a tally it has never seen.

Every tally should carry its `note`. Saying how a list was counted, and what it
skews toward, is what separates it from an anonymous internet ranking.

### Sign-in

A **username and password** is the main path. GitHub is a one-click alternative
for people who have one; asking a reader of book lists for a GitHub account is a
strange demand.

**No email address is stored, on either path.** GitHub hands one over whether we
want it or not, and it's discarded on sign-in rather than saved, so both paths
store the same minimal thing: a username, a password hash, and your marks. The
price is stated plainly on the account page — with no address on file there is
no reset link for anyone, so signup issues a **one-time recovery code** instead.
Recovery codes are hashed like passwords and rotated on use.

Encrypting an email rather than dropping it was considered and rejected: the app
would need the key to send anything, so the key lives beside the data and buys
protection only against a database dump that somehow leaves the environment
behind. Not holding the address is the version that's actually true.

**Usernames can be almost anything** — accents, Cyrillic, Japanese, emoji,
spaces in the middle, up to 30 characters. The exceptions are the characters
that would make two different names look *identical*, which is the one property
a username has to have: zero-width and bidi-control characters are stripped
(`isa\u200bbel` and `isabel` must not be two accounts), NFKC folds the
compatibility forms so `ﬁnn` collides with `finn`, and surrounding or doubled
spaces are trimmed rather than rejected because `" isabel"` is a typo, not a
person. Matching is case- and space-insensitive; the stored spelling is what
gets displayed, so signing in as `"  ISABEL "` still shows *Isabel*.

Not solved: visual confusables across scripts — Latin `a` and Cyrillic `а` are
still different names. That only matters when usernames are shown to *other*
people, which they currently never are. If lists ever become public, revisit it.

Passwords are argon2id. Sign-in failures are counted per account and lock it for
15 minutes after 8 — per account rather than per IP, because an IP is a
suggestion. Every failure returns the same sentence: "no such user" is a way to
enumerate which usernames exist.

## Turning accounts on

1. **Database.** Vercel → your project → Storage → attach Postgres (Neon). It
   injects `POSTGRES_URL` itself. Then run `sql/schema.sql` once against it.
   Neon's free tier scales to zero when idle and wakes on the next query;
   Supabase's free tier *pauses* after a week of no traffic and needs a human to
   restore it, which is why this doesn't use Supabase.
2. **GitHub OAuth app** (optional — omit it and the button doesn't render). github.com → Settings → Developer settings → OAuth
   Apps → New. Callback URL `https://YOUR-SITE/api/auth/callback/github`.
   Put the id and secret in `AUTH_GITHUB_ID` / `AUTH_GITHUB_SECRET`.
3. **`AUTH_SECRET`** — `openssl rand -base64 32`.

See `.env.example`. Adding Google or magic links later is one provider entry;
neither the adapter nor the `marks` table cares which one someone used.

## Deploying

Pushes to `main` deploy automatically via Vercel. No environment variables are
needed — there's nothing to configure.

One gotcha worth recording: Vercel **blocks deployments of Next.js versions with
known security advisories**. The build succeeds and the deployment is rejected
afterwards, so the build log ends with a normal route table and no error line.
If a deploy fails for no visible reason, check the `npm warn deprecated next@…`
line near the top of the log. Versions here are pinned exactly rather than with
carets so a deploy can't drift onto an unpatched build.
