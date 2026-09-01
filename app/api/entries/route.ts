export const runtime = "nodejs";

import { NextResponse } from "next/server";
import { auth } from "@/auth";
import { pool, hasDb } from "@/lib/db";

/**
 * Your own entries: the things you added yourself, per shelf.
 *
 * Deliberately shaped like /api/marks — read everything, write one, delete one,
 * hand over what a browser was holding — for the same reason. A "save my whole
 * list" endpoint is how a stale tab in another window silently overwrites what
 * you typed on your phone this morning.
 *
 * The one difference from marks: an entry can be *edited*, so PUT upserts by id
 * rather than only inserting. The id comes from the client, so an entry written
 * signed-out keeps its identity when the browser is later claimed — which is
 * what stops a claim creating a second copy of everything.
 */

const MAX_BULK = 500;
const LIMITS = { pri: 200, sec: 200, note: 600, shelf: 60, id: 64 };

type Entry = { id: string; shelf: string; pri: string; sec: string; note: string };

/** Trim, cap, and refuse anything that isn't a usable string. */
function clean(v: unknown, max: number): string {
  return typeof v === "string" ? v.trim().slice(0, max) : "";
}

function parse(v: unknown): Entry | null {
  if (!v || typeof v !== "object") return null;
  const o = v as Record<string, unknown>;
  const e = {
    id: clean(o.id, LIMITS.id),
    shelf: clean(o.shelf, LIMITS.shelf),
    pri: clean(o.pri, LIMITS.pri),
    sec: clean(o.sec, LIMITS.sec),
    note: clean(o.note, LIMITS.note),
  };
  // An entry with no name is not an entry. Everything else may be empty.
  return e.id && e.shelf && e.pri ? e : null;
}

async function userId() {
  if (!hasDb) return null;
  const session = await auth();
  return session?.user?.id ? Number(session.user.id) : null;
}

/** Everything you've added, grouped by shelf, the way the client store holds it. */
export async function GET() {
  const uid = await userId();
  if (!uid) return NextResponse.json({ signedIn: false, entries: {} });

  const { rows } = await pool.query<Entry & { created_at: string }>(
    `SELECT id, shelf, pri, sec, note, created_at FROM entries
     WHERE user_id = $1 ORDER BY created_at`,
    [uid]
  );

  const out: Record<string, Entry[]> = {};
  for (const r of rows) {
    (out[r.shelf] ||= []).push({ id: r.id, shelf: r.shelf, pri: r.pri, sec: r.sec, note: r.note });
  }
  return NextResponse.json({ signedIn: true, entries: out });
}

/** Add or edit one entry. Upsert by id, so a retried write can't duplicate. */
export async function PUT(req: Request) {
  const uid = await userId();
  if (!uid) return NextResponse.json({ error: "not signed in" }, { status: 401 });

  const e = parse(await req.json().catch(() => null));
  if (!e) return NextResponse.json({ error: "bad request" }, { status: 400 });

  await pool.query(
    `INSERT INTO entries (user_id, id, shelf, pri, sec, note) VALUES ($1,$2,$3,$4,$5,$6)
     ON CONFLICT (user_id, id) DO UPDATE SET pri = $4, sec = $5, note = $6`,
    [uid, e.id, e.shelf, e.pri, e.sec, e.note]
  );
  return NextResponse.json({ ok: true });
}

/** Remove one entry. Unlike a mark, this destroys text nobody else has a copy
 *  of, so the confirm lives in the UI — but the endpoint stays idempotent. */
export async function DELETE(req: Request) {
  const uid = await userId();
  if (!uid) return NextResponse.json({ error: "not signed in" }, { status: 401 });

  const body = await req.json().catch(() => null);
  const id = clean(body?.id, LIMITS.id);
  if (!id) return NextResponse.json({ error: "bad request" }, { status: 400 });

  await pool.query("DELETE FROM entries WHERE user_id=$1 AND id=$2", [uid, id]);
  return NextResponse.json({ ok: true });
}

/** Claim what a browser was holding. Additive: an id already in the account
 *  keeps the account's copy, so claiming can never overwrite what you typed
 *  somewhere else. */
export async function POST(req: Request) {
  const uid = await userId();
  if (!uid) return NextResponse.json({ error: "not signed in" }, { status: 401 });

  const body = await req.json().catch(() => null);
  if (!Array.isArray(body?.items)) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }
  if (body.items.length > MAX_BULK) {
    return NextResponse.json({ error: "too many items" }, { status: 413 });
  }

  const rows = body.items.map(parse).filter((e: Entry | null): e is Entry => e !== null);
  if (rows.length === 0) return NextResponse.json({ ok: true, added: 0 });

  const values = rows
    .map((_: Entry, i: number) => `($1,$${i * 5 + 2},$${i * 5 + 3},$${i * 5 + 4},$${i * 5 + 5},$${i * 5 + 6})`)
    .join(",");
  const params: unknown[] = [uid];
  for (const r of rows) params.push(r.id, r.shelf, r.pri, r.sec, r.note);

  const res = await pool.query(
    `INSERT INTO entries (user_id, id, shelf, pri, sec, note) VALUES ${values}
     ON CONFLICT DO NOTHING`,
    params
  );
  return NextResponse.json({ ok: true, added: res.rowCount ?? 0 });
}
