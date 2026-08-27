"use client";

import Link from "next/link";
import { Underline } from "./StrokeBar";
import { useSaved, useProgress, listId } from "@/lib/progress";
import { goodreads, sameThing, youtube, type Row, type List, type Shelf } from "@/lib/content";

/**
 * A person's own list for one shelf.
 *
 * Nothing here is stored separately — it's the same saved keys the tables
 * write, resolved back against the content. That means a saved row can never
 * drift out of sync with the list it came from, and a row that gets removed
 * from a list simply stops appearing here.
 *
 * The one thing this page does that the tables don't is **collapse
 * duplicates**. The same book is a different row in every tally it appears in,
 * which is right for the lists — each row is that crowd's answer — and wrong
 * here: your list should hold one copy of East of Eden however many crowds
 * recommended it. Grouping is by title-and-author rather than by list, and the
 * lists it came from become a footnote on the row, which is more interesting
 * than a repeat anyway.
 */
type Item = {
  id: string;
  row: Row;
  list: List;
  froms: { list: List; listKey: string; rowKey: string }[];
  done: boolean;
};

export default function SavedList({ shelf }: { shelf: Shelf }) {
  const { keys, toggle } = useSaved();
  const { marked } = useProgress();

  const byThing = new Map<string, Item>();
  for (const list of shelf.lists) {
    const lid = listId(shelf.slug, list.slug);
    const chosen = new Set(keys(lid));
    for (const row of list.rows) {
      if (!chosen.has(row.key)) continue;
      const id = sameThing(list, row);
      const existing = byThing.get(id);
      if (existing) {
        existing.froms.push({ list, listKey: lid, rowKey: row.key });
        existing.done ||= marked(lid, row.key);
      } else {
        byThing.set(id, {
          id,
          row,
          list,
          froms: [{ list, listKey: lid, rowKey: row.key }],
          done: marked(lid, row.key),
        });
      }
    }
  }

  const items = [...byThing.values()].sort((a, b) => a.row.pri.localeCompare(b.row.pri));
  const total = items.length;
  const dupes = items.filter((i) => i.froms.length > 1).length;

  function copy() {
    const text = items
      .map((i) => `- ${i.row.pri}${i.row.sec ? ` — ${i.row.sec}` : ""}`)
      .join("\n");
    navigator.clipboard?.writeText(text);
  }

  /** Removing an item removes it from every list it was saved from — otherwise
   *  one click would leave a copy behind that reappears as a duplicate. */
  const remove = (item: Item) => item.froms.forEach((f) => toggle(f.listKey, f.rowKey));

  return (
    <>
      <nav className="crumbs" aria-label="Breadcrumb">
        <Link href="/">Everything</Link>
        <span aria-hidden="true">/</span>
        <Link href={`/${shelf.slug}`}>{shelf.name}</Link>
        <span aria-hidden="true">/</span>
        <b>My list</b>
      </nav>

      <div className="lhead">
        <div>
          <h1>
            <span className="mk">
              <Underline color={shelf.mark} />
              <span className="w">My {shelf.name.toLowerCase()} list</span>
            </span>
          </h1>
          <p>
            Everything you&rsquo;ve saved from the {shelf.name.toLowerCase()} shelf, one copy each.
          </p>
        </div>
        <div className="prog">
          <div className="row">
            <span className="big">{total}</span>
            <span className="pct">saved</span>
          </div>
        </div>
      </div>

      {total === 0 ? (
        <p className="note" style={{ marginTop: 22 }}>
          <b>Nothing saved yet.</b> Open any list on this shelf and press the{" "}
          <span className="inlineplus">+</span> at the end of a row. This page is where they land.
        </p>
      ) : (
        <>
          <div className="tools">
            <button className="chip" onClick={copy}>
              Copy as text
            </button>
          </div>

          <div className="tbl" style={{ marginTop: 6 }}>
            <div className="scroll">
              <table>
                <tbody>
                  {items.map((item) => (
                    <tr key={item.id} className={item.done ? "on" : undefined}>
                      <td className="sec">{item.row.sec}</td>
                      <td className="pri">
                        {item.row.pri}
                        <span className="froms">
                          {item.froms.map((f) => (
                            <Link key={f.list.slug} href={`/${shelf.slug}/${f.list.slug}`}>
                              {f.list.title}
                            </Link>
                          ))}
                        </span>
                      </td>
                      <td className="trk">
                        {item.list.gr && (
                          <a
                            className="tr"
                            href={goodreads(
                              `${item.row.pri} ${
                                (item.list.gr === "extra" ? item.row.extra : item.row.sec) || ""
                              }`.trim()
                            )}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            ★ Goodreads
                          </a>
                        )}
                        {item.row.yt && (
                          <a
                            className="tr"
                            href={youtube(`${item.row.yt} ${item.row.ytWord || "trailer"}`)}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            ▶ {item.row.ytWord || "Trailer"}
                          </a>
                        )}
                        {item.row.links?.map((l) => (
                          <a key={l.url} href={l.url} target="_blank" rel="noopener noreferrer">
                            {l.label}
                          </a>
                        ))}
                      </td>
                      <td className="tk add">
                        <button
                          className="tick plus"
                          aria-pressed={true}
                          aria-label={`Remove ${item.row.pri} from my list`}
                          title={
                            item.froms.length > 1
                              ? `Remove from my list (saved from ${item.froms.length} lists)`
                              : "Remove from my list"
                          }
                          onClick={() => remove(item)}
                        >
                          <svg viewBox="0 0 12 12" fill="none" aria-hidden="true">
                            <path
                              d="M3.2 1.6h5.6v8.8L6 8.2l-2.8 2.2Z"
                              strokeWidth="1.6"
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

          {dupes > 0 && (
            <p className="note">
              <b>
                {dupes} {dupes === 1 ? "item was" : "items were"} recommended by more than one list.
              </b>{" "}
              They appear once here, with every list that put them there — which is a better reason
              to read something than any single list is.
            </p>
          )}

          <p className="note">
            <b>Where this lives.</b> Signed in, on your account, following you between browsers.
            Signed out, in this browser only &mdash; clearing your site data clears it, and
            &ldquo;copy as text&rdquo; is the way to take it somewhere safer.
          </p>
        </>
      )}
    </>
  );
}
