"use client";

import { useCallback, useSyncExternalStore } from "react";

/**
 * Two things a person can do to a row, kept in two separate stores:
 *
 *   done  — "I've read / seen / eaten at this". A fact about the past.
 *   want  — "put this on my list". An intention about the future.
 *
 * They are deliberately not one tri-state toggle. You can want something you
 * have already read, and un-ticking a row shouldn't quietly wipe the reason you
 * saved it in the first place.
 *
 * Signed out, both live in this browser's localStorage. Signed in, they live in
 * the database and this file mirrors every toggle to it. The two are kept
 * *side by side* rather than merged: what a browser was holding before anyone
 * signed in stays exactly where it was, and only moves into an account when
 * someone chooses to claim it (see ClaimBanner). That is what stops a shared
 * laptop from handing one person's list to whoever logs in next.
 *
 * When accounts arrived, this was the only file that had to learn about a
 * server — which was the point of writing it this way in the first place.
 */

type Marks = Record<string, Record<string, 1>>;
const EMPTY: Marks = {};

type Kind = "done" | "want";

function createStore(kind: Kind, storageKey: string) {
  let local: Marks = {};
  let remote: Marks | null = null;   // non-null exactly when signed in
  let loaded = false;
  const listeners = new Set<() => void>();

  const state = () => remote ?? local;

  function load() {
    if (loaded || typeof window === "undefined") return;
    try {
      local = JSON.parse(window.localStorage.getItem(storageKey) || "{}");
    } catch {
      local = {};
    }
    loaded = true;
  }

  function persist() {
    if (remote) return;   // signed in: the server is the record, not this browser
    try {
      window.localStorage.setItem(storageKey, JSON.stringify(local));
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
    kind,
    subscribe,
    snapshot: () => {
      load();
      return state();
    },
    serverSnapshot: () => EMPTY,
    /** What this browser is holding, whether or not anyone is signed in. */
    localMarks: () => {
      load();
      return local;
    },
    signedIn: () => remote !== null,
    /** Swap the store over to (or back from) the signed-in copy. */
    setRemote(next: Marks | null) {
      remote = next;
      emit();
    },
    toggle(list: string, key: string) {
      const base = state();
      const on = !base[list]?.[key];
      const next: Marks = { ...base, [list]: { ...(base[list] || {}) } };
      if (on) next[list][key] = 1;
      else delete next[list][key];

      if (remote) {
        remote = next;
        // Optimistic: the click lands now, the network catches up. A failed
        // write is worth a log, not a UI that jumps backwards under someone.
        fetch("/api/marks", {
          method: "PATCH",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ kind, list, key, on }),
        }).catch(() => {});
      } else {
        local = next;
        persist();
      }
      emit();
    },
  };
}

const doneStore = createStore("done", "listomania");        // unchanged key: existing ticks survive
const wantStore = createStore("want", "listomania:want");

/**
 * Called once, by SyncProvider, when the session is known. Signed in, it pulls
 * the account's marks and points both stores at them; signed out, it points
 * them back at this browser.
 */
export async function syncWithAccount(signedIn: boolean) {
  if (!signedIn) {
    doneStore.setRemote(null);
    wantStore.setRemote(null);
    return;
  }
  try {
    const res = await fetch("/api/marks");
    if (!res.ok) return;
    const data = await res.json();
    doneStore.setRemote(data.done || {});
    wantStore.setRemote(data.want || {});
  } catch {
    /* offline: stay on the local copy rather than showing an empty account */
  }
}

/** Everything this browser holds that an account could claim. */
export function unclaimedMarks() {
  const items: { kind: Kind; list: string; key: string }[] = [];
  for (const store of [doneStore, wantStore]) {
    const marks = store.localMarks();
    for (const list of Object.keys(marks)) {
      for (const key of Object.keys(marks[list])) {
        items.push({ kind: store.kind, list, key });
      }
    }
  }
  return items;
}

/** Hand this browser's marks to the signed-in account. Additive, never destructive. */
export async function claimLocalMarks() {
  const items = unclaimedMarks();
  if (items.length === 0) return 0;
  const res = await fetch("/api/marks", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ items }),
  });
  if (!res.ok) throw new Error("claim failed");
  await syncWithAccount(true);
  return items.length;
}

/** Forget what this browser is holding — only ever called after a claim. */
export function clearLocalMarks() {
  try {
    window.localStorage.removeItem("listomania");
    window.localStorage.removeItem("listomania:want");
  } catch {
    /* nothing to do: the marks are already in the account either way */
  }
}

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
