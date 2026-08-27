"use client";

import { useEffect, useRef, useState } from "react";

/**
 * The theme song.
 *
 * The site is named after a Phoenix record, so there is a button in the top bar
 * that plays the hook and nothing else. It is a joke that only works if it's
 * *fast* — press, twenty seconds of chorus, done — so it starts at the hook
 * rather than at 0:00 and stops on its own at the end of it.
 *
 * Three rules it follows, none of them optional:
 *
 *   - It never plays on load. Sound that starts without being asked for is the
 *     single most hostile thing a website can do.
 *   - The player is visible, not a hidden iframe. Embedding YouTube's player
 *     where the viewer can see it is the arrangement YouTube actually offers;
 *     a 0×0 iframe playing audio is a stunt that eventually gets blocked, and
 *     it would also hide the one control someone reaching for silence wants.
 *   - The iframe is only created *after* the first press. Nothing is fetched
 *     from youtube.com, and no cookie of theirs is set, for a reader who never
 *     touches the button.
 *
 * If the video ever goes away, the panel still holds a plain search link, which
 * is the same reason every other link on this site is a search.
 */

/** The official upload, and the seconds the hook runs between.
 *  These three numbers are the whole configuration — nudge START/END by a
 *  second or two if the entry ever feels early or late. */
const VIDEO = "4BJDNw7o6so";
const START = 51;
const END = 73;

export default function ThemeSong() {
  const [on, setOn] = useState(false);
  const panel = useRef<HTMLDivElement>(null);

  // Esc stops it. Anyone hunting for silence tries that key first.
  useEffect(() => {
    if (!on) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOn(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [on]);

  const src =
    `https://www.youtube-nocookie.com/embed/${VIDEO}` +
    `?autoplay=1&start=${START}&end=${END}&rel=0&modestbranding=1&playsinline=1`;

  return (
    <div className="tsong">
      <button
        type="button"
        className="tsbtn"
        aria-pressed={on}
        aria-expanded={on}
        title={on ? "Stop Lisztomania" : "Play Lisztomania — the chorus, 20 seconds"}
        onClick={() => setOn((v) => !v)}
      >
        {on ? (
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <rect x="6.5" y="6" width="4" height="12" rx="1" />
            <rect x="13.5" y="6" width="4" height="12" rx="1" />
          </svg>
        ) : (
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M8.5 5.6 18 12l-9.5 6.4Z" />
          </svg>
        )}
        <span>Lisztomania</span>
      </button>

      {on && (
        <div className="tspanel" ref={panel}>
          <iframe
            src={src}
            title="Phoenix — Lisztomania"
            allow="autoplay; encrypted-media"
            referrerPolicy="strict-origin-when-cross-origin"
            loading="lazy"
          />
          <p>
            <b>Phoenix &mdash; Lisztomania.</b> The chorus, then it stops.{" "}
            <a
              href={`https://www.youtube.com/watch?v=${VIDEO}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              Whole song
            </a>
          </p>
        </div>
      )}
    </div>
  );
}
