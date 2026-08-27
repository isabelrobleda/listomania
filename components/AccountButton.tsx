"use client";

import Link from "next/link";
import { useSession } from "next-auth/react";

/**
 * The first *character* of a name, where "character" means what a person would
 * point at — not the first code unit.
 *
 * Usernames here can be anything: accents, Cyrillic, Japanese, emoji. Slicing
 * a string at [0] cuts an emoji in half and renders a replacement box, and
 * even [...name][0] splits a family emoji or a flag into its pieces. Intl's
 * grapheme segmenter is the only thing that gets 🍕bel right.
 */
function initial(name: string): string {
  try {
    const seg = new Intl.Segmenter(undefined, { granularity: "grapheme" });
    const first = seg.segment(name)[Symbol.iterator]().next();
    if (!first.done) return first.value.segment.toLocaleUpperCase();
  } catch {
    /* very old browser: the code-point fallback is wrong for flags and
       family emoji and right for everything else, which is the better half */
  }
  return ([...name][0] || "?").toLocaleUpperCase();
}

export default function AccountButton() {
  const { data, status } = useSession();

  // Deliberately renders nothing while the session resolves rather than
  // flashing "Sign in" at someone who is already signed in.
  if (status === "loading") return <span className="acct ghost" aria-hidden="true" />;

  if (status !== "authenticated") {
    // Same two-renderings trick as below: the words on a desktop, a door glyph
    // on a phone, where they were the widest thing in a bar that has to hold
    // five controls on one line.
    return (
      <Link className="acct named" href="/account" aria-label="Sign in">
        <span className="full">Sign in</span>
        <span className="mini out" aria-hidden="true">
          <svg viewBox="0 0 24 24">
            <path d="M14 4.5h4.2a1.3 1.3 0 0 1 1.3 1.3v12.4a1.3 1.3 0 0 1-1.3 1.3H14" />
            <path d="M10 8.4 13.6 12 10 15.6M13.2 12H4.5" />
          </svg>
        </span>
      </Link>
    );
  }

  const name = data?.user?.name || "Account";
  const ch = initial(name);
  // An emoji carries its own colour and vanishes on a black disc.
  const isEmoji = /\p{Extended_Pictographic}/u.test(ch);

  /* Two renderings of the same link, one visible at a time. On a phone the bar
     has to hold a wordmark, an account, a play button and a theme switch, and
     a 30-character username is the one thing there that can be shortened
     without losing anything — you know who you are signed in as. */
  return (
    <Link className="acct named" href="/account" title={name} aria-label={`Account — ${name}`}>
      <span className="full">{name}</span>
      <span className={isEmoji ? "mini emoji" : "mini"} aria-hidden="true">
        {ch}
      </span>
    </Link>
  );
}
