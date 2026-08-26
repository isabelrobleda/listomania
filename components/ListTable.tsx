"use client";

import { useMemo, useState } from "react";
import StrokeBar, { Underline } from "./StrokeBar";
import { useProgress, listId } from "@/lib/progress";
import { youtube, type List, type Row, type Shelf } from "@/lib/content";

/**
 * The last column carries whatever a given list has for a row — a watch link, an
 * author, one source, several. Build the pieces first and join them, so two of
 * them never end up jammed together with no separator.
 */
function LastCell({ row }: { row: Row }) {
  const parts: React.ReactNode[] = [];

  if (row.yt) {
    parts.push(
      <a
        key="yt"
        className="tr"
        href={youtube(`${row.yt} ${row.ytWord || "trailer"}`)}
        target="_blank"
        rel="noopener noreferrer"
      >
        ▶ {row.ytWord || "Trailer"}
      </a>
    );
  }
  if (row.extra) parts.push(<span key="extra">{row.extra}</span>);
  if (row.src) {
    parts.push(
      <a key="src" href={row.src.url} target="_blank" rel="noopener noreferrer">
        {row.src.label}
      </a>
    );
  }
  row.links?.forEach((l) =>
    parts.push(
      <a key={l.url} href={l.url} target="_blank" rel="noopener noreferrer">
        {l.label}
      </a>
    )
  );

  return (
    <>
      {parts.map((p, i) => (
        <span key={i}>
          {i > 0 && <span className="sep"> · </span>}
          {p}
        </span>
      ))}
    </>
  );
}

const Check = () => (
  <svg viewBox="0 0 12 12" fill="none" aria-hidden="true">
    <path d="M2 6.2 4.6 8.8 10 3.4" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export default function ListTable({ shelf, list }: { shelf: Shelf; list: List }) {
  const id = listId(shelf.slug, list.slug);
  const { marked, toggle, count } = useProgress();
  const [q, setQ] = useState("");
  const [onlyMarked, setOnlyMarked] = useState(false);

  const done = count(id);
  const pct = Math.round((done / list.rows.length) * 100);

  const rows = useMemo(() => {
    const needle = q.trim().toLowerCase();
    return list.rows
      .map((r, i) => ({ ...r, i }))
      .filter((r) => {
        if (onlyMarked && !marked(id, r.key)) return false;
        if (!needle) return true;
        return `${r.pri} ${r.sec} ${r.lead} ${r.extra || ""}`.toLowerCase().includes(needle);
      });
  }, [list.rows, q, onlyMarked, marked, id]);

  return (
    <>
      <div className="lhead">
        <div>
          <h1>
            <span className="mk">
              <Underline color={shelf.mark} />
              <span className="w">{list.title}</span>
            </span>
          </h1>
          <p>{list.desc}</p>
        </div>
        <div className="prog">
          <div className="row">
            <span className="big">
              {done} / {list.rows.length}
            </span>
            <span className="pct">{pct}%</span>
          </div>
          <StrokeBar color={shelf.mark} pct={pct} height={17} />
        </div>
      </div>

      {list.sources && list.sources.length > 0 && (
        <div className="srcbox">
          <span className="srclab">Asked in</span>
          {list.sources.map((s) => (
            <a className="srclink" key={s.url} href={s.url} target="_blank" rel="noopener noreferrer">
              <span className="sq">&ldquo;{s.q}&rdquo;</span>
              <span className="sm">
                {s.label} · {s.meta} ↗
              </span>
            </a>
          ))}
        </div>
      )}

      <div className="tools">
        <input
          className="search"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder={`Search ${list.rows.length.toLocaleString()} entries…`}
          aria-label={`Search ${list.title}`}
        />
        <button className="chip" aria-pressed={onlyMarked} onClick={() => setOnlyMarked((v) => !v)}>
          Only marked
        </button>
        {list.action && (
          <a className="plbtn" href={list.action.url} target="_blank" rel="noopener noreferrer">
            {list.action.label}
          </a>
        )}
      </div>

      <div className="tbl">
        <div className="scroll">
          <table>
            <thead>
              <tr>
                <th>
                  <span className="sr">Marked</span>
                </th>
                <th>#</th>
                {list.cols.map((c, i) => (
                  <th key={i}>{c}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.length === 0 && (
                <tr>
                  <td className="empty" colSpan={6}>
                    Nothing matches &ldquo;{q}&rdquo;.
                  </td>
                </tr>
              )}
              {rows.map((r) => {
                const on = marked(id, r.key);
                return (
                  <tr key={r.key} className={on ? "on" : undefined}>
                    <td className="tk">
                      <button
                        className="tick"
                        aria-pressed={on}
                        aria-label={`Mark ${r.pri} as ${list.verb}`}
                        onClick={() => toggle(id, r.key)}
                      >
                        <Check />
                      </button>
                    </td>
                    <td className="ix">{String(r.i + 1).padStart(3, "0")}</td>
                    <td className="yr">{r.lead}</td>
                    <td className="sec">{r.sec}</td>
                    <td className="pri">{r.pri}</td>
                    <td className="trk">
                      <LastCell row={r} />
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {list.note && (
        <p className="note">
          <b>How this was counted.</b>{" "}
          <span dangerouslySetInnerHTML={{ __html: list.note }} />
        </p>
      )}
      {list.kind === "Seed" && (
        <p className="note">
          <b>Seed list.</b> These {list.rows.length} entries are a starting point, not the finished
          canon — enough to show how the list reads and behaves.
        </p>
      )}
    </>
  );
}
