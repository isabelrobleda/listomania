"use client";

import { useEffect } from "react";
import type { Shelf } from "@/lib/content";

/**
 * Each shelf owns a colour, and it drives the ticks, the tinted rows and the
 * marker strokes. Setting it as CSS variables on <main> means the components
 * below don't each have to know which shelf they're in.
 */
export default function ShelfTheme({ shelf }: { shelf: Shelf }) {
  useEffect(() => {
    const main = document.getElementById("main");
    if (!main) return;

    /* "Is it dark right now" has two inputs since the theme switch exists: an
       explicit choice on <html data-theme>, and the OS preference when there
       isn't one. Reading only the media query left the tinted rows in their
       light-mode colour whenever someone forced dark by hand. */
    const dark = () => {
      const forced = document.documentElement.getAttribute("data-theme");
      if (forced === "dark") return true;
      if (forced === "light") return false;
      return window.matchMedia("(prefers-color-scheme: dark)").matches;
    };

    const apply = () => {
      main.style.setProperty("--mark", shelf.mark);
      main.style.setProperty("--on-mark", shelf.on);
      main.style.setProperty("--mark-soft", dark() ? shelf.softDark : shelf.soft);
    };
    apply();

    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    mq.addEventListener("change", apply);

    // …and re-apply when the switch flips the attribute.
    const obs = new MutationObserver(apply);
    obs.observe(document.documentElement, { attributeFilter: ["data-theme"] });

    return () => {
      mq.removeEventListener("change", apply);
      obs.disconnect();
      ["--mark", "--on-mark", "--mark-soft"].forEach((p) => main.style.removeProperty(p));
    };
  }, [shelf]);

  return null;
}
