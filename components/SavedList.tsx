"use client";

import Link from "next/link";
import { Underline } from "./StrokeBar";
import { useSaved, useProgress, listId } from "@/lib/progress";
import { goodreads, youtube, type Row, type List, type Shelf } from "@/lib/content";

/**
 * A person's own list for one shelf: every row they've saved, grouped by the
 * list it came from. Nothing here is stored separately — it's the same saved
 * keys the tables write, resolved back against the content. That means a saved
 * row can never drift out of sync with the list it came from, and a row that
 * gets removed from a list simply stops appearing here.
 */
export default function SavedList({ shelf }: { shelf: Shelf }) {
  const { keys, toggle } = useSaved();
  const { marked } = useProgress();

  const groups = shelf.lists
    .map((list: List) => {
      const id = listId(shelf.slug, list.slug);
      const chosen = new Set(keys(id));
      return { list, id, rows: list.rows.filter((r) => chosen.has(r.key)) };
    })
    .filter((g) => g.rows.length > 0);

  const total = groups.reduce((n, g) => n + g.rows.length, 0);

  function copy() {
    const text = groups
      .map((g) => `${g.list.title}\n` + g.rows.map((r) => `- ${r.pri}${r.sec ? ` — ${r.sec}` : ""}`).join("\n"))
      .join("\n\n");
    navigator.clipboard?.writeText(text);
  }

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
            Everything you&rsquo;ve saved from the {shelf.name.toLowerCase()} shelf, kept in this
            browser.
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

          {groups.map((g) => (
            <section key={g.list.slug} className="savedsec">
              <h2>
                <Link href={`/${shelf.slug}/${g.list.slug}`}>{g.list.title}</Link>
                <span className="ct">{g.rows.length}</span>
              </h2>
              <div className="tbl">
                <div className="scroll">
                  <table>
                    <tbody>
                      {g.rows.map((r: Row) => (
                        <tr key={r.key} className={marked(g.id, r.key) ? "on" : undefined}>
                          <td className="sec">{r.sec}</td>
                          <td className="pri">{r.pri}</td>
                          <td className="trk">
                            {g.list.gr && (
                              <a
                                className="tr"
                                href={goodreads(
                                  `${r.pri} ${(g.list.gr === "extra" ? r.extra : r.sec) || ""}`.trim()
                                )}
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                ★ Goodreads
                              </a>
                            )}
                            {r.yt && (
                              <a
                                className="tr"
                                href={youtube(`${r.yt} ${r.ytWord || "trailer"}`)}
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                ▶ {r.ytWord || "Trailer"}
                              </a>
                            )}
                            {r.links?.map((l) => (
                              <a key={l.url} href={l.url} target="_blank" rel="noopener noreferrer">
                                {l.label}
                              </a>
                            ))}
                          </td>
                          <td className="tk add">
                            <button
                              className="tick plus"
                              aria-pressed={true}
                              aria-label={`Remove ${r.pri} from my list`}
                              title="Remove from my list"
                              onClick={() => toggle(g.id, r.key)}
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
            </section>
          ))}

          <p className="note">
            <b>This list lives in your browser.</b> There are no accounts yet, so it isn&rsquo;t
            synced to another device and clearing your site data clears it. &ldquo;Copy as text&rdquo;
            is the way to take it somewhere safer.
          </p>
        </>
      )}
    </>
  );
}
