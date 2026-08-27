export const runtime = "nodejs";

import { NextResponse } from "next/server";
import { auth } from "@/auth";
import { pool, hasDb } from "@/lib/db";

/**
 * The whole sync API: read everything you've marked, toggle one thing, or hand
 * over what a browser was holding before you signed in.
 *
 * It is deliberately not a "save my whole state" endpoint. A last-write-wins
 * blob is how someone loses a phone's worth of bookmarks because a stale laptop
 * tab flushed an old copy; per-item toggles can't do that.
 */

type Kind = "done" | "want";
const KINDS: Kind[] = ["done", "want"];
const isKind = (v: unknown): v is Kind => KINDS.includes(v as Kind);

/** Payload sizes are capped so a malformed client can't post a novel. */
const MAX_BULK = 5000;
const MAX_LEN = 400;
const ok = (s: unknown) => typeof s === "string" && s.length > 0 && s.length <= MAX_LEN;

async function userId() {
  if (!hasDb) return null;
  const session = await auth();
  return session?.user?.id ? Number(session.user.id) : null;
}

/** Everything this person has marked, shaped the way the client store holds it. */
export async function GET() {
  const uid = await userId();
  if (!uid) return NextResponse.json({ signedIn: false, done: {}, want: {} });

  const { rows } = await pool.query<{ kind: Kind; list_id: string; item_key: string }>(
    "SELECT kind, list_id, item_key FROM marks WHERE user_id = $1",
    [uid]
  );

  const out: Record<Kind, Record<string, Record<string, 1>>> = { done: {}, want: {} };
  for (const r of rows) {
    (out[r.kind][r.list_id] ||= {})[r.item_key] = 1;
  }
  return NextResponse.json({ signedIn: true, ...out });
}

/** Toggle one item. Idempotent in both directions. */
export async function PATCH(req: Request) {
  const uid = await userId();
  if (!uid) return NextResponse.json({ error: "not signed in" }, { status: 401 });

  const body = await req.json().catch(() => null);
  if (!body || !isKind(body.kind) || !ok(body.list) || !ok(body.key)) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

  if (body.on) {
    await pool.query(
      `INSERT INTO marks (user_id, kind, list_id, item_key) VALUES ($1,$2,$3,$4)
       ON CONFLICT DO NOTHING`,
      [uid, body.kind, body.list, body.key]
    );
  } else {
    await pool.query(
      "DELETE FROM marks WHERE user_id=$1 AND kind=$2 AND list_id=$3 AND item_key=$4",
      [uid, body.kind, body.list, body.key]
    );
  }
  return NextResponse.json({ ok: true });
}

/**
 * Claim what a browser was holding. Additive only — it can add rows to your
 * account and can never remove one, so claiming a browser you'd forgotten about
 * is not a way to lose anything.
 */
export async function POST(req: Request) {
  const uid = await userId();
  if (!uid) return NextResponse.json({ error: "not signed in" }, { status: 401 });

  const body = await req.json().catch(() => null);
  const items: unknown = body?.items;
  if (!Array.isArray(items)) return NextResponse.json({ error: "bad request" }, { status: 400 });
  if (items.length > MAX_BULK) {
    return NextResponse.json({ error: "too many items" }, { status: 413 });
  }

  const rows = items.filter(
    (i): i is { kind: Kind; list: string; key: string } =>
      Boolean(i) && isKind((i as never)["kind"]) && ok((i as never)["list"]) && ok((i as never)["key"])
  );
  if (rows.length === 0) return NextResponse.json({ ok: true, added: 0 });

  // One statement rather than a loop: a claim of a few thousand rows shouldn't
  // be a few thousand round trips to a database on the other side of the sea.
  const values = rows
    .map((_, i) => `($1, $${i * 3 + 2}, $${i * 3 + 3}, $${i * 3 + 4})`)
    .join(",");
  const params: unknown[] = [uid];
  for (const r of rows) params.push(r.kind, r.list, r.key);

  const res = await pool.query(
    `INSERT INTO marks (user_id, kind, list_id, item_key) VALUES ${values}
     ON CONFLICT DO NOTHING`,
    params
  );
  return NextResponse.json({ ok: true, added: res.rowCount ?? 0 });
}
