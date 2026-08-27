"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";

/**
 * The shelf navigation, as a drawer, on phones.
 *
 * The rail is a real sidebar on a desktop. On a phone it used to collapse into
 * a block stacked *above* the page, which meant every visit began with a
 * screenful of navigation and you had to scroll past the furniture to reach
 * the thing you came for. It is the same list of shelves either way, so it
 * should behave the same way: off to the side, out of the way until asked for.
 *
 * The open state lives on <html> as data-nav, so the rail and the scrim can be
 * styled from CSS without either of them needing to be a child of this
 * component or to know it exists.
 *
 * Four ways out, because a drawer you can't dismiss is a trap: the button, the
 * scrim, Escape, and following any link inside it — that last one matters most,
 * since a menu that stays open over the page you just chose is the single most
 * common way this pattern is got wrong.
 */
export default function NavToggle() {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  // Navigating closes it. Keyed on pathname so it also fires for a link tapped
  // inside the drawer, which is the whole point of opening it.
  useEffect(() => setOpen(false), [pathname]);

  useEffect(() => {
    const root = document.documentElement;
    if (open) root.setAttribute("data-nav", "open");
    else root.removeAttribute("data-nav");

    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false);
    window.addEventListener("keydown", onKey);
    // Stops the page behind the drawer scrolling under your thumb.
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", onKey);
      document.body.style.overflow = prev;
    };
  }, [open]);

  return (
    <>
      <button
        type="button"
        className="navbtn"
        aria-expanded={open}
        aria-controls="rail"
        aria-label={open ? "Close shelves" : "Shelves"}
        onClick={() => setOpen((v) => !v)}
      >
        <svg viewBox="0 0 24 24" aria-hidden="true">
          {open ? (
            <path d="M5.5 5.5l13 13M18.5 5.5l-13 13" />
          ) : (
            <path d="M3.5 6.5h17M3.5 12h17M3.5 17.5h17" />
          )}
        </svg>
      </button>
      {/* Inert and invisible until the drawer is open; CSS does that part. */}
      <button
        type="button"
        className="scrim"
        tabIndex={-1}
        aria-hidden="true"
        onClick={() => setOpen(false)}
      />
    </>
  );
}
