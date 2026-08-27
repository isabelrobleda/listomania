export const runtime = "nodejs";

import { NextResponse } from "next/server";
import { pool, hasDb } from "@/lib/db";
import {
  checkUsername,
  findByUsername,
  hashSecret,
  newRecoveryCode,
  passwordProblem,
  verifySecret,
} from "@/lib/accounts";

/**
 * Set a new password using the recovery code. This is the whole reset story —
 * there's no email to send a link to, which is the deal a site that doesn't ask
 * for your email has to make.
 *
 * The code is single-use: a fresh one is issued and returned, because a code
 * that keeps working after it's been written on a Post-it is a password with
 * extra steps.
 */
export async function POST(req: Request) {
  if (!hasDb) return NextResponse.json({ error: "Accounts aren't switched on here." }, { status: 501 });

  const body = await req.json().catch(() => null);
  const username = checkUsername(body?.username);
  const code = typeof body?.code === "string" ? body.code.trim().toUpperCase() : "";
  const bad = passwordProblem(body?.password);
  if (bad) return NextResponse.json({ error: bad }, { status: 400 });

  const user = username ? await findByUsername(username) : null;
  // Same answer whether the username is wrong or the code is.
  if (!user || !(await verifySecret(user.recovery_hash, code))) {
    return NextResponse.json({ error: "That username and recovery code don't match." }, { status: 401 });
  }

  const recovery = newRecoveryCode();
  const [password_hash, recovery_hash] = await Promise.all([
    hashSecret(body.password),
    hashSecret(recovery),
  ]);
  await pool.query(
    `UPDATE users SET password_hash = $2, recovery_hash = $3,
            failed_logins = 0, locked_until = NULL
      WHERE id = $1`,
    [user.id, password_hash, recovery_hash]
  );

  return NextResponse.json({ ok: true, recovery });
}
