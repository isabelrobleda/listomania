"use client";

import { useState } from "react";
import Link from "next/link";
import { Underline } from "./StrokeBar";
import { useEntries, newId, FIELDS, DEFAULT_FIELDS, type Entry } from "@/lib/entries";
import { goodreads, youtube, sameThing, type Row, type List, type Shelf } from "@/lib/content";
import { useFavourites, listId } from "@/lib/progress";

/**
 * The one list on this site nobody voted on.
 *
 * Every other list here is an argument someone else had — a crowd tally, a
 * canon, a saved list from a stranger. This is the shelf's blank page: things
 * you'd have said if you'd been in the thread. It sits beside the tallies
 * rather than inside them on purpose, because a count of one person is not the
 * same kind of claim as a count of three hundred, and the whole site is built
 * on not blurring that line.
 *
 * The `note` field is the reason this is worth having at all. A tally can tell
 * you a book was named 31 times; it can't tell you *why*, because a count
 * throws that away. Here the why is the only thing there's room for.
 *
 * Two things land on this page, and they are kept visibly apart. Rows you
 * **starred** on somebody else's list came from a crowd and are shown with the
 * list they came from; entries you **typed** came from nowhere but you. Merging
 * them into one undifferentiated list would be tidier and would lose the only
 * distinction this whole site exists to make.
 */
type Starred = { id: string; row: Row; list: List; froms: List[] };

export default function OwnList({ shelf }: { shelf: Shelf }) {
  const { forShelf, put, remove } = useEntries();
  const { keys: starKeys, toggle: unstar } = useFavourites();
  const entries = forShelf(shelf.slug);
  const f = FIELDS[shelf.slug] || DEFAULT_FIELDS;

  // Starred rows, resolved back against the content and collapsed the same way
  // the saved page does it: one copy of a thing, however many lists named it.
  const byThing = new Map<string, Starred>();
  for (const list of shelf.lists) {
    const lid = listId(shelf.slug, list.slug);
    const chosen = new Set(starKeys(lid));
    for (const row of list.rows) {
      if (!chosen.has(row.key)) continue;
      const id = sameThing(list, row);
      const seen = byThing.get(id);
      if (seen) seen.froms.push(list);
      else byThing.set(id, { id, row, list, froms: [list] });
    }
  }
  const starred = [...byThing.values()].sort((a, b) => a.row.pri.localeCompare(b.row.pri));

  /** Un-starring has to clear the star on every list the thing appears in,
   *  otherwise one click leaves a copy that reappears on the next render. */
  const removeStar = (it: Starred) =>
    it.froms.forEach((l) => unstar(listId(shelf.slug, l.slug), 
      l.rows.find((r) => sameThing(l, r) === it.id)!.key));

  const total = starred.length + entries.length;

  const [pri, setPri] = useState("");
  const [sec, setSec] = useState("");
  const [note, setNote] = useState("");
  const [editing, setEditing] = useState<string | null>(null);
  const [confirm, setConfirm] = useState<string | null>(null);

  const clear = () => {
    setPri("");
    setSec("");
    setNote("");
    setEditing(null);
  };

  function submit(e: React.FormEvent) {
    e.preventDefault();
    const name = pri.trim();
    if (!name) return;   // a nameless entry is not an entry
    put({
      id: editing || newId(),
      shelf: shelf.slug,
      pri: name,
      sec: sec.trim(),
      note: note.trim(),
    });
    clear();
  }

  function edit(en: Entry) {
    setEditing(en.id);
    setPri(en.pri);
    setSec(en.sec);
    setNote(en.note);
    setConfirm(null);
    // The form is above the table, and on a phone the row you tapped is often
    // below the fold — without this, "Edit" looks like it did nothing.
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function copy() {
    const lines = [
      ...starred.map((it) => `- ${it.row.pri}${it.row.sec ? ` — ${it.row.sec}` : ""}`),
      ...entries.map(
        (e) => `- ${e.pri}${e.sec ? ` — ${e.sec}` : ""}${e.note ? `\n    ${e.note}` : ""}`
      ),
    ];
    navigator.clipboard?.writeText(lines.join("\n"));
  }

  const isBooks = shelf.slug === "books";
  const isWatchable = shelf.slug === "film" || shelf.slug === "television";
  const isMusic = shelf.slug === "music";
  const isPod = shelf.slug === "podcasts";

  return (
    <>
      <nav className="crumbs" aria-label="Breadcrumb">
        <Link href="/">Everything</Link>
        <span aria-hidden="true">/</span>
        <Link href={`/${shelf.slug}`}>{shelf.name}</Link>
        <span aria-hidden="true">/</span>
        <b>My favourites</b>
      </nav>

      <div className="lhead">
        <div>
          <h1>
            <span className="mk">
              <Underline color={shelf.mark} />
              <span className="w">My {shelf.name.toLowerCase()} favourites</span>
            </span>
          </h1>
          <p>
            Star a row on any list on this shelf, or add something the lists missed &mdash; and
            say why, which is the part a tally can never keep.
          </p>
        </div>
        <div className="prog">
          <div className="row">
            <span className="big">{total}</span>
            <span className="pct">favourites</span>
          </div>
        </div>
      </div>

      <form className="ownform" onSubmit={submit}>
        <div className="fields">
          <label>
            <span>{f.pri}</span>
            <input
              value={pri}
              onChange={(e) => setPri(e.target.value)}
              maxLength={200}
              placeholder={f.hint}
              required
            />
          </label>
          <label>
            <span>
              {f.sec} <i>optional</i>
            </span>
            <input value={sec} onChange={(e) => setSec(e.target.value)} maxLength={200} />
          </label>
        </div>
        <label className="wide">
          <span>
            Why <i>optional</i>
          </span>
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            maxLength={600}
            rows={2}
            placeholder="What it did to you. Nobody else is going to write this down."
          />
        </label>
        <div className="ownbtns">
          <button className="chip go" type="submit">
            {editing ? "Save changes" : "Add to my favourites"}
          </button>
          {editing && (
            <button className="chip" type="button" onClick={clear}>
              Cancel
            </button>
          )}
        </div>
      </form>

      {total === 0 ? (
        <p className="note" style={{ marginTop: 22 }}>
          <b>Nothing here yet.</b> Press the ☆ at the end of any row on this shelf, or type
          something in above. This is the only list on the site that isn&rsquo;t someone
          else&rsquo;s opinion.
        </p>
      ) : (
        <>
          <div className="tools">
            <button className="chip" onClick={copy}>
              Copy as text
            </button>
          </div>

          {starred.length > 0 && (
            <>
              <h2 className="ownh">Starred from these lists</h2>
              <div className="tbl own" style={{ marginTop: 6 }}>
                <div className="scroll">
                  <table>
                    <tbody>
                      {starred.map((it) => (
                        <tr key={it.id}>
                          <td className="sec">{it.row.sec}</td>
                          <td className="pri">
                            {it.row.pri}
                            <span className="froms">
                              {it.froms.map((l) => (
                                <Link key={l.slug} href={`/${shelf.slug}/${l.slug}`}>
                                  {l.title}
                                </Link>
                              ))}
                            </span>
                          </td>
                          <td className="trk">
                            {it.list.gr && (
                              <a
                                className="tr"
                                href={goodreads(
                                  `${it.row.pri} ${
                                    (it.list.gr === "extra" ? it.row.extra : it.row.sec) || ""
                                  }`.trim()
                                )}
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                ★ Goodreads
                              </a>
                            )}
                            {it.row.yt && (
                              <a
                                className="tr"
                                href={youtube(`${it.row.yt} ${it.row.ytWord || "trailer"}`)}
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                ▶ {it.row.ytWord || "Trailer"}
                              </a>
                            )}
                            {it.row.links?.map((l) => (
                              <a key={l.url} href={l.url} target="_blank" rel="noopener noreferrer">
                                {l.label}
                              </a>
                            ))}
                          </td>
                          <td className="tk add">
                            <button
                              className="tick fav"
                              aria-pressed={true}
                              aria-label={`Remove ${it.row.pri} from my favourites`}
                              title="Remove from favourites"
                              onClick={() => removeStar(it)}
                            >
                              <svg viewBox="0 0 12 12" fill="currentColor" aria-hidden="true">
                                <path
                                  d="M6 1.4 7.45 4.4l3.3.48-2.39 2.32.57 3.28L6 8.93l-2.93 1.55.56-3.28L1.25 4.88l3.3-.48Z"
                                  strokeWidth="1.3"
                                  strokeLinejoin="round"
                                />
                              </svg>
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          )}

          {entries.length > 0 && starred.length > 0 && (
            <h2 className="ownh">Added by you</h2>
          )}

          {entries.length > 0 && (
          <div className="tbl own" style={{ marginTop: 6 }}>
            <div className="scroll">
              <table>
                <tbody>
                  {entries.map((en) => (
                    <tr key={en.id} className={editing === en.id ? "on" : undefined}>
                      <td className="sec">{en.sec}</td>
                      <td className="pri">
                        {en.pri}
                        {en.note && <span className="why">{en.note}</span>}
                      </td>
                      <td className="trk">
                        {isBooks && (
                          <a
                            className="tr"
                            href={goodreads(`${en.pri} ${en.sec}`.trim())}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            ★ Goodreads
                          </a>
                        )}
                        {(isWatchable || isMusic) && (
                          <a
                            className="tr"
                            href={youtube(
                              `${en.pri} ${en.sec} ${isMusic ? "" : "trailer"}`.trim()
                            )}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            ▶ {isMusic ? "Listen" : "Trailer"}
                          </a>
                        )}
                        {isPod && (
                          <a
                            className="tr"
                            href={
                              "https://open.spotify.com/search/" +
                              encodeURIComponent(`${en.pri} ${en.sec}`.trim()) +
                              "/podcasts"
                            }
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            ▶ Listen
                          </a>
                        )}
                        {shelf.slug === "places" && (
                          <a
                            href={
                              "https://www.google.com/maps/search/?api=1&query=" +
                              encodeURIComponent(en.pri)
                            }
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            Map ↗
                          </a>
                        )}
                        <button className="tr as" onClick={() => edit(en)}>
                          Edit
                        </button>
                      </td>
                      <td className="tk add">
                        {confirm === en.id ? (
                          <button
                            className="chip danger"
                            onClick={() => {
                              remove(shelf.slug, en.id);
                              setConfirm(null);
                            }}
                          >
                            Delete?
                          </button>
                        ) : (
                          <button
                            className="tick plus"
                            aria-label={`Remove ${en.pri}`}
                            title="Remove"
                            onClick={() => setConfirm(en.id)}
                          >
                            <svg viewBox="0 0 12 12" fill="none" aria-hidden="true">
                              <path d="M3 3l6 6M9 3l-6 6" strokeWidth="1.6" strokeLinecap="round" />
                            </svg>
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          )}

          {/* Deleting here destroys the only copy of something you wrote, which is
              not true anywhere else on the site — hence the two-step, and hence
              saying plainly where the text lives. */}
          <p className="note">
            <b>Where this lives.</b> Signed in, on your account, following you between browsers.
            Signed out, in this browser only &mdash; clearing your site data clears it. Unlike a
            bookmark, nobody else has a copy of what you typed here, so &ldquo;copy as text&rdquo;
            is worth doing before you clean out a browser.
          </p>
        </>
      )}
    </>
  );
}
