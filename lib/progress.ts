"use client";

import { useCallback, useSyncExternalStore } from "react";

/**
 * Two things a person can do to a row, kept in two separate stores:
 *
 *   done  — "I've read / seen / eaten at this". A fact about the past.
 *   want  — "put this on my list". An intention about the future.
 *
 * They are deliberately not one tri-state toggle. You can want something you
 * have already read, and un-ticking something shouldn't quietly wipe the reason
 * you saved it in the first place.
 *
 * Both live in the browser — there are no accounts in v1, so there's nothing to
 * sync and no database to keep. Each is a single module-level store rather than
 * per-component state: the rail, the shelf cards, the table and the saved-list
 * page all read the same numbers, so one click has to update every one of them.
 * `useSyncExternalStore` also gives a correct server snapshot, so the markup
 * React renders on the server matches what it renders during hydration.
 *
 * When accounts arrive, this file is the only place that has to learn about a
 * server.
 */

type Marks = Record<string, Record<string, 1>>;
const EMPTY: Marks = {};

function createStore(storageKey: string) {
  let state: Marks = {};
  let loaded = false;
  const listeners = new Set<() => void>();

  function load() {
    if (loaded || typeof window === "undefined") return;
    try {
      state = JSON.parse(window.localStorage.getItem(storageKey) || "{}");
    } catch {
      state = {};
    }
    loaded = true;
  }

  function persist() {
    try {
      window.localStorage.setItem(storageKey, JSON.stringify(state));
    } catch {
      /* private window, quota, blocked storage: it just won't survive a reload */
    }
  }

  const emit = () => listeners.forEach((l) => l());

  function subscribe(listener: () => void) {
    load();
    listeners.add(listener);

    // Another tab ticking something should update this one too.
    const onStorage = (e: StorageEvent) => {
      if (e.key !== storageKey) return;
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

  return {
    subscribe,
    snapshot: () => {
      load();
      return state;
    },
    serverSnapshot: () => EMPTY,
    toggle(list: string, key: string) {
      const next: Marks = { ...state, [list]: { ...(state[list] || {}) } };
      if (next[list][key]) delete next[list][key];
      else next[list][key] = 1;
      state = next;
      persist();
      emit();
    },
  };
}

const doneStore = createStore("listomania");        // unchanged key: existing ticks survive
const wantStore = createStore("listomania:want");

function useStore(store: ReturnType<typeof createStore>) {
  const marks = useSyncExternalStore(store.subscribe, store.snapshot, store.serverSnapshot);

  const toggle = useCallback((list: string, key: string) => store.toggle(list, key), [store]);
  const marked = useCallback(
    (list: string, key: string) => Boolean(marks[list]?.[key]),
    [marks]
  );
  const count = useCallback((list: string) => Object.keys(marks[list] || {}).length, [marks]);
  const keys = useCallback((list: string) => Object.keys(marks[list] || {}), [marks]);

  return { toggle, marked, count, keys };
}

/** What you've already read / seen / eaten at. */
export function useProgress() {
  return useStore(doneStore);
}

/** What you've put on your own list. */
export function useSaved() {
  return useStore(wantStore);
}

export function listId(shelfSlug: string, listSlug: string) {
  return `${shelfSlug}/${listSlug}`;
}
