"use client";

import { useState } from "react";
import { useEntries, newId, FIELDS, DEFAULT_FIELDS, type Entry } from "@/lib/entries";
import { goodreads, youtube, type Shelf } from "@/lib/content";

/**
 * The write-it-in-yourself half of a shelf's two personal pages, shared by both.
 *
 * `want: false` is My favourites — things you've already had. `want: true` is
 * My list — things you haven't got to yet. Same fields, same store, one flag
 * apart, because the difference between them is tense and nothing else.
 *
 * The two differ only in wording and in one control: a want can be marked done,
 * which flips the flag and moves it to the other page. That is the whole point
 * of making this one record with a flag rather than two separate stores — the
 * day you finally read the book, you press a button instead of retyping it.
 *
 * `children` renders between the form and the typed table, which is where each
 * page puts the rows that came from somewhere else (starred rows, saved rows).
 * The form has to sit at the top on both, and the editing state belongs to
 * whichever component owns the form, so the slot is the simplest way to keep
 * one copy of this code.
 */
export default function OwnEntries({
  shelf,
  want,
  children,
}: {
  shelf: Shelf;
  want: boolean;
  children?: React.ReactNode;
}) {
  const { forShelf, put, remove } = useEntries();
  const entries = forShelf(shelf.slug, want);
  const f = FIELDS[shelf.slug] || DEFAULT_FIELDS;

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
      want,
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

  /** Had it after all: same entry, other page. Nothing is retyped and the note
   *  you wrote when you added it survives, which is the part worth keeping. */
  const had = (en: Entry) => put({ ...en, want: false });

  const isBooks = shelf.slug === "books";
  const isWatchable = shelf.slug === "film" || shelf.slug === "television";
  const isMusic = shelf.slug === "music";
  const isPod = shelf.slug === "podcasts";

  // The shelf's own word for having had the thing — "read", "seen", "been" —
  // taken from its lists rather than invented here, so the button says what
  // every other control on the shelf says.
  const verb = shelf.lists.find((l) => l.verb)?.verb || "done";

  return (
    <>
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
            {want ? "Where you heard about it" : "Why"} <i>optional</i>
          </span>
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            maxLength={600}
            rows={2}
            placeholder={
              want
                ? "Who told you, or what made you write it down. You will not remember in six months."
                : "What it did to you. Nobody else is going to write this down."
            }
          />
        </label>
        <div className="ownbtns">
          <button className="chip go" type="submit">
            {editing ? "Save changes" : want ? "Add to my list" : "Add to my favourites"}
          </button>
          {editing && (
            <button className="chip" type="button" onClick={clear}>
              Cancel
            </button>
          )}
        </div>
      </form>

      {children}

      {entries.length > 0 && (
        <>
          <h2 className="ownh">Added by you</h2>
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
                        {want && (
                          <button className="tr as" onClick={() => had(en)}>
                            {`Mark ${verb} →`}
                          </button>
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
        </>
      )}
    </>
  );
}
