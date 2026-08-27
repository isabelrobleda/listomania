"use client";

import { useCallback, useSyncExternalStore } from "react";

/**
 * Three states, not two: light, dark, and "follow my system".
 *
 * System is the default and a real choice, not the absence of one — someone
 * whose laptop flips to dark at sunset wants this page to flip with it. A
 * two-way switch would silently pin them to whichever one they last tapped.
 *
 * The value is applied to <html data-theme> by the blocking script in
 * layout.tsx, so the page is already the right colour before it paints. This
 * component only has to keep the attribute and localStorage in step after that.
 */

const KEY = "listomania:theme";
type Theme = "light" | "dark" | "system";

const listeners = new Set<() => void>();
let value: Theme | null = null;

function read(): Theme {
  if (value) return value;
  if (typeof window === "undefined") return "system";
  const v = window.localStorage.getItem(KEY);
  value = v === "light" || v === "dark" ? v : "system";
  return value;
}

function subscribe(fn: () => void) {
  listeners.add(fn);
  const onStorage = (e: StorageEvent) => {
    if (e.key !== KEY) return;
    value = null;
    listeners.forEach((l) => l());
  };
  window.addEventListener("storage", onStorage);
  return () => {
    listeners.delete(fn);
    window.removeEventListener("storage", onStorage);
  };
}

/** The server can't know the system preference, so it renders as "system". */
const serverSnapshot = (): Theme => "system";

const Sun = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <circle cx="12" cy="12" r="4.2" />
    <path d="M12 2v2.6M12 19.4V22M2 12h2.6M19.4 12H22M4.9 4.9l1.9 1.9M17.2 17.2l1.9 1.9M19.1 4.9l-1.9 1.9M6.8 17.2l-1.9 1.9" />
  </svg>
);
const Moon = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <path d="M20 14.2A8.3 8.3 0 1 1 9.8 4a6.6 6.6 0 0 0 10.2 10.2Z" />
  </svg>
);
const Auto = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <rect x="2.8" y="4.5" width="18.4" height="12.5" rx="2" />
    <path d="M8.5 20.5h7" />
  </svg>
);

export default function ThemeToggle() {
  const theme = useSyncExternalStore(subscribe, read, serverSnapshot);

  const set = useCallback((next: Theme) => {
    value = next;
    try {
      if (next === "system") window.localStorage.removeItem(KEY);
      else window.localStorage.setItem(KEY, next);
    } catch {
      /* private window: the choice just won't survive a reload */
    }
    const root = document.documentElement;
    if (next === "system") root.removeAttribute("data-theme");
    else root.setAttribute("data-theme", next);
    listeners.forEach((l) => l());
  }, []);

  const opts: [Theme, string, () => React.ReactElement][] = [
    ["light", "Light", Sun],
    ["system", "Match my system", Auto],
    ["dark", "Dark", Moon],
  ];

  return (
    <div className="theme" role="group" aria-label="Colour theme">
      {opts.map(([v, label, Icon]) => (
        <button
          key={v}
          type="button"
          aria-pressed={theme === v}
          aria-label={label}
          title={label}
          onClick={() => set(v)}
        >
          <Icon />
        </button>
      ))}
    </div>
  );
}
