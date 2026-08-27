export const runtime = "nodejs";

import { NextResponse } from "next/server";
import { auth } from "@/auth";
import { pool, hasDb } from "@/lib/db";

/**
 * Delete the account and everything attached to it.
 *
 * One statement: the marks, sessions and provider rows all cascade from
 * users.id, so there is no way to half-delete someone and leave orphaned
 * reading history behind.
 */
export async function DELETE() {
  if (!hasDb) return NextResponse.json({ error: "no database" }, { status: 501 });
  const session = await auth();
  const uid = session?.user?.id ? Number(session.user.id) : null;
  if (!uid) return NextResponse.json({ error: "not signed in" }, { status: 401 });

  await pool.query("DELETE FROM users WHERE id = $1", [uid]);
  return NextResponse.json({ ok: true });
}
