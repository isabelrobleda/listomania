"use client";

import { useCallback, useSyncExternalStore } from "react";

/**
 * Your own entries — the third per-person store, alongside done and want.
 *
 * The other two point *at* content: a mark is a list id and a row key, and the
 * row itself lives in the repo. An entry has nothing to point at. It is content
 * that only you have, which makes it the one thing on this site that can be
 * lost, and that shapes every decision in this file:
 *
 *  - The id is minted here, in the browser, not by the database. An entry has
 *    to exist before anyone signs in and keep the same identity afterwards,
 *    otherwise claiming a browser would create a second copy of everything.
 *  - Signed out it lives in localStorage, exactly like the marks, so the
 *    feature works with no account at all.
 *  - Writes to the server are per-entry, never a whole-list flush.
 *
 * Same store pattern as lib/progress.ts. It is duplicated rather than shared
 * because the shapes genuinely differ — a set of keys versus a list of records
 * — and a generic that fits both would be harder to read than either.
 */

export type Entry = {
  id: string;
  shelf: string;
  pri: string;   // the thing itself
  sec: string;   // author / artist / director / what it is
  note: string;  // why, in your own words
};

/** shelf slug -> entries, in the order they were added */
type Bag = Record<string, Entry[]>;
const EMPTY: Bag = {};
const KEY = "listomania:mine";

export function newId(): string {
  try {
    return crypto.randomUUID();
  } catch {
    // Older Safari, and any non-secure context. Collisions here would have to
    // happen inside one person's own browser to matter at all.
    return `e${Date.now().toString(36)}${Math.random().toString(36).slice(2, 10)}`;
  }
}

let local: Bag = {};
let remote: Bag | null = null;   // non-null exactly when signed in
let loaded = false;
const listeners = new Set<() => void>();

const state = () => remote ?? local;
const emit = () => listeners.forEach((l) => l());

function load() {
  if (loaded || typeof window === "undefined") return;
  try {
    const raw = JSON.parse(window.localStorage.getItem(KEY) || "{}");
    local = raw && typeof raw === "object" ? raw : {};
  } catch {
    local = {};
  }
  loaded = true;
}

function persist() {
  if (remote) return;   // signed in: the server is the record, not this browser
  try {
    window.localStorage.setItem(KEY, JSON.stringify(local));
  } catch {
    /* private window, quota, blocked storage: it won't survive a reload */
  }
}

function subscribe(listener: () => void) {
  load();
  listeners.add(listener);
  const onStorage = (e: StorageEvent) => {
    if (e.key !== KEY) return;
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

function write(next: Bag) {
  if (remote) remote = next;
  else {
    local = next;
    persist();
  }
  emit();
}

/** Add a new entry, or replace an existing one with the same id. */
function put(e: Entry) {
  const base = state();
  const list = base[e.shelf] || [];
  const at = list.findIndex((x) => x.id === e.id);
  const next: Bag = {
    ...base,
    [e.shelf]: at >= 0 ? list.map((x) => (x.id === e.id ? e : x)) : [...list, e],
  };
  write(next);

  if (remote) {
    // Optimistic, like the marks: the entry appears now and the network catches
    // up. A failed write leaves it in the UI until a reload, which is the right
    // way round — silently vanishing text someone typed is much worse.
    fetch("/api/entries", {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(e),
    }).catch(() => {});
  }
}

function remove(shelf: string, id: string) {
  const base = state();
  const next: Bag = { ...base, [shelf]: (base[shelf] || []).filter((x) => x.id !== id) };
  if (next[shelf].length === 0) delete next[shelf];
  write(next);

  if (remote) {
    fetch("/api/entries", {
      method: "DELETE",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ id }),
    }).catch(() => {});
  }
}

/** Points the store at the account, or back at this browser. Called by SyncProvider. */
export async function syncEntriesWithAccount(signedIn: boolean) {
  if (!signedIn) {
    remote = null;
    emit();
    return;
  }
  try {
    const res = await fetch("/api/entries");
    if (!res.ok) return;
    const data = await res.json();
    remote = data.entries || {};
    emit();
  } catch {
    /* offline: stay on the local copy rather than showing an empty account */
  }
}

/** Everything this browser holds that an account could claim. */
export function unclaimedEntries(): Entry[] {
  load();
  return Object.values(local).flat();
}

/** Hand this browser's entries to the signed-in account. Additive, never destructive. */
export async function claimLocalEntries() {
  const items = unclaimedEntries();
  if (items.length === 0) return 0;
  const res = await fetch("/api/entries", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ items }),
  });
  if (!res.ok) throw new Error("claim failed");
  await syncEntriesWithAccount(true);
  return items.length;
}

/** Forget what this browser is holding — only ever called after a claim. */
export function clearLocalEntries() {
  try {
    window.localStorage.removeItem(KEY);
  } catch {
    /* already in the account either way */
  }
}

export function useEntries() {
  const bag = useSyncExternalStore(subscribe, () => {
    load();
    return state();
  }, () => EMPTY);

  const forShelf = useCallback((shelf: string) => bag[shelf] || [], [bag]);
  const count = useCallback((shelf: string) => (bag[shelf] || []).length, [bag]);

  return { forShelf, count, put, remove };
}

/**
 * What the two text fields are called, per shelf.
 *
 * A generic "name / detail" pair would be less code and a worse form: nobody
 * thinks of a director as a detail. The labels are the shelf's own columns, so
 * an entry you add reads like the rows it sits beside.
 */
export const FIELDS: Record<string, { pri: string; sec: string; hint: string }> = {
  music:      { pri: "Song or album", sec: "Artist",       hint: "e.g. Lisztomania — Phoenix" },
  books:      { pri: "Title",         sec: "Author",       hint: "e.g. Stoner — John Williams" },
  film:       { pri: "Film",          sec: "Director",     hint: "e.g. Chungking Express — Wong Kar-wai" },
  television: { pri: "Series",        sec: "Creator",      hint: "e.g. Fleabag — Phoebe Waller-Bridge" },
  places:     { pri: "Place",         sec: "What it is",   hint: "e.g. Tulus Lotrek — Fine dining" },
  podcasts:   { pri: "Podcast",       sec: "Made by",      hint: "e.g. Heavyweight — Jonathan Goldstein" },
};

export const DEFAULT_FIELDS = { pri: "Name", sec: "Detail", hint: "" };
