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

    const dark = () =>
      window.matchMedia("(prefers-color-scheme: dark)").matches;

    const apply = () => {
      main.style.setProperty("--mark", shelf.mark);
      main.style.setProperty("--on-mark", shelf.on);
      main.style.setProperty("--mark-soft", dark() ? shelf.softDark : shelf.soft);
    };
    apply();

    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    mq.addEventListener("change", apply);
    return () => {
      mq.removeEventListener("change", apply);
      ["--mark", "--on-mark", "--mark-soft"].forEach((p) => main.style.removeProperty(p));
    };
  }, [shelf]);

  return null;
}
