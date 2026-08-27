export const runtime = "nodejs";

import { NextResponse } from "next/server";
import { pool, hasDb } from "@/lib/db";
import {
  MAX_USERNAME,
  checkUsername,
  hashSecret,
  newRecoveryCode,
  passwordProblem,
} from "@/lib/accounts";

/**
 * Create an account. Returns the recovery code exactly once — it is hashed
 * before it's stored, so this response is the only time it can ever be read.
 */
export async function POST(req: Request) {
  if (!hasDb) return NextResponse.json({ error: "Accounts aren't switched on here." }, { status: 501 });

  const body = await req.json().catch(() => null);
  const username = checkUsername(body?.username);
  if (!username) {
    return NextResponse.json(
      { error: `Pick a name: anything up to ${MAX_USERNAME} characters.` },
      { status: 400 }
    );
  }
  const bad = passwordProblem(body?.password);
  if (bad) return NextResponse.json({ error: bad }, { status: 400 });

  const recovery = newRecoveryCode();
  const [password_hash, recovery_hash] = await Promise.all([
    hashSecret(body.password),
    hashSecret(recovery),
  ]);

  try {
    await pool.query(
      // name and username are passed separately rather than reusing $1: they
      // are varchar and text, and Postgres refuses to infer one parameter as
      // both ("character varying versus text").
      `INSERT INTO users (name, username, password_hash, recovery_hash)
       VALUES ($1, $2, $3, $4)`,
      [username, username, password_hash, recovery_hash]
    );
  } catch (e) {
    // 23505 is the unique index on lower(username).
    if ((e as { code?: string }).code === "23505") {
      return NextResponse.json({ error: "That username is taken." }, { status: 409 });
    }
    throw e;
  }

  return NextResponse.json({ ok: true, recovery });
}
