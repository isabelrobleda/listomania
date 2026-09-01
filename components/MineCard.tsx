"use client";

import Link from "next/link";
import StrokeBar from "./StrokeBar";
import { useEntries, FIELDS, DEFAULT_FIELDS } from "@/lib/entries";
import { type Shelf } from "@/lib/content";

/**
 * Your own favourites, as a card in the shelf's grid.
 *
 * It sits *last*, after the crowd lists, and it says so on its face. A chip in
 * the toolbar was the first attempt and it read as a control rather than a
 * destination — you don't find a list by looking at a row of filters. But
 * putting it first would have been the other error: this shelf is mostly other
 * people's arguments, and the page should still open with them.
 *
 * The one thing it deliberately does not do is fake a progress bar. Every other
 * card shows how far through a list you are; there is no "through" here, so the
 * stroke stays empty and the meta line counts entries instead.
 */
export default function MineCard({ shelf }: { shelf: Shelf }) {
  const { count } = useEntries();
  const n = count(shelf.slug);
  const f = FIELDS[shelf.slug] || DEFAULT_FIELDS;

  return (
    <Link className="card mine" href={`/${shelf.slug}/my-favourites`}>
      <span className="kicker">Yours</span>
      <h3>My {shelf.name.toLowerCase()} favourites</h3>
      <span className="desc">
        {n === 0
          ? `The blank one. Add anything these lists missed — a ${f.pri.toLowerCase()}, and why it mattered.`
          : `Your own answers, not a crowd’s — with the reason, which is the part a tally can never keep.`}
      </span>
      <StrokeBar color={shelf.mark} pct={0} />
      <span className="meta">
        <span>{n === 0 ? "nothing here yet" : `${n} added`}</span>
        <span>{n === 0 ? "add one" : "add another"}</span>
      </span>
    </Link>
  );
}
