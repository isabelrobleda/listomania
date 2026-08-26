"use client";

import { useCallback, useSyncExternalStore } from "react";

/**
 * Progress lives in the browser — there are no accounts in v1, so there's
 * nothing to sync and no database to keep.
 *
 * It's a single module-level store rather than per-component state: the sidebar,
 * the home page counters and the table all read the same numbers, so ticking a
 * row has to update every one of them. `useSyncExternalStore` also gives us a
 * correct server snapshot, so the markup React renders on the server matches
 * what it renders on the client during hydration.
 *
 * When accounts arrive, this file is the only place that has to learn about the
 * server.
 */

const STORAGE_KEY = "listomania";

type Progress = Record<string, Record<string, 1>>;

let state: Progress = {};
let loaded = false;
const listeners = new Set<() => void>();

const EMPTY: Progress = {};

function load() {
  if (loaded || typeof window === "undefined") return;
  try {
    state = JSON.parse(window.localStorage.getItem(STORAGE_KEY) || "{}");
  } catch {
    state = {};
  }
  loaded = true;
}

function persist() {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    /* private window, quota, blocked storage: progress just won't survive a reload */
  }
}

function emit() {
  listeners.forEach((l) => l());
}

function subscribe(listener: () => void) {
  load();
  listeners.add(listener);

  // Another tab ticking something should update this one too.
  const onStorage = (e: StorageEvent) => {
    if (e.key !== STORAGE_KEY) return;
    loaded = false;
    load();
    emit();
  };
  window.addEventListener("storage", onStorage);

  return () => {
    listeners.delete(listener);
    window.removeEventListener("storage", onStorage);
  };
}

function getSnapshot(): Progress {
  load();
  return state;
}

/** The server has no localStorage, so everything starts at zero there. */
function getServerSnapshot(): Progress {
  return EMPTY;
}

export function useProgress() {
  const progress = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);

  const toggle = useCallback((list: string, key: string) => {
    const next: Progress = { ...state, [list]: { ...(state[list] || {}) } };
    if (next[list][key]) delete next[list][key];
    else next[list][key] = 1;
    state = next;
    persist();
    emit();
  }, []);

  const marked = useCallback(
    (list: string, key: string) => Boolean(progress[list]?.[key]),
    [progress]
  );

  const count = useCallback(
    (list: string) => Object.keys(progress[list] || {}).length,
    [progress]
  );

  return { toggle, marked, count };
}

export function listId(shelfSlug: string, listSlug: string) {
  return `${shelfSlug}/${listSlug}`;
}
