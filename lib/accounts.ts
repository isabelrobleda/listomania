import { hash, verify } from "@node-rs/argon2";
import { pool } from "@/lib/db";

/**
 * Password accounts, kept deliberately small: a username, a hash, and a
 * recovery code. No email — it is the obvious way to do password resets and
 * exactly the personal data this site has no other use for.
 */

export { MIN_PASSWORD, MAX_USERNAME, cleanUsername, usernameKey } from "@/lib/authRules";
import { MIN_PASSWORD, cleanUsername, usernameKey } from "@/lib/authRules";

/** The handful that a rule about length can't catch. */
const OBVIOUS = new Set([
  "password12", "1234567890", "qwertyuiop", "letmeinnow", "iloveyou12",
  "listomania", "passwordpassword", "adminadmin",
]);

/** The display form, or null if it isn't a name at all. */
export const checkUsername = cleanUsername;

export function passwordProblem(p: unknown): string | null {
  if (typeof p !== "string" || p.length < MIN_PASSWORD) {
    return `Password needs to be at least ${MIN_PASSWORD} characters.`;
  }
  if (p.length > 200) return "That password is longer than anything needs to be.";
  if (OBVIOUS.has(p.toLowerCase())) return "That's one of the first passwords anyone would guess.";
  return null;
}

/**
 * A recovery code, in the only format people actually manage to write down.
 * Four short groups, no ambiguous characters — no O/0, no I/l/1.
 */
const ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789";
export function newRecoveryCode() {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  const chars = Array.from(bytes, (b) => ALPHABET[b % ALPHABET.length]);
  return [0, 4, 8, 12].map((i) => chars.slice(i, i + 4).join("")).join("-");
}

const OPTS = { memoryCost: 19456, timeCost: 2, parallelism: 1 };

export const hashSecret = (s: string) => hash(s, OPTS);
export async function verifySecret(stored: string | null, given: string) {
  if (!stored) return false;
  try {
    return await verify(stored, given, OPTS);
  } catch {
    return false;
  }
}

const LOCK_AFTER = 8;
const LOCK_MINUTES = 15;

type Row = {
  id: number;
  username: string;
  password_hash: string | null;
  recovery_hash: string | null;
  failed_logins: number;
  locked_until: Date | null;
};

export async function findByUsername(name: string) {
  const { rows } = await pool.query<Row>(
    `SELECT id, username, password_hash, recovery_hash, failed_logins, locked_until
       FROM users WHERE lower(username) = $1`,
    [usernameKey(name)]
  );
  return rows[0] || null;
}

export const isLocked = (u: Row) => Boolean(u.locked_until && u.locked_until > new Date());

/** Wrong password: count it, and lock the account for a while once it's clearly
 *  being guessed at. Per-account rather than per-IP — it can't be evaded by
 *  changing address, and it can't be used to lock a stranger out of much. */
export async function noteFailure(id: number) {
  await pool.query(
    `UPDATE users
        SET failed_logins = failed_logins + 1,
            locked_until = CASE WHEN failed_logins + 1 >= $2
                                THEN now() + ($3 || ' minutes')::interval
                                ELSE locked_until END
      WHERE id = $1`,
    [id, LOCK_AFTER, LOCK_MINUTES]
  );
}

export async function noteSuccess(id: number) {
  await pool.query(
    "UPDATE users SET failed_logins = 0, locked_until = NULL WHERE id = $1",
    [id]
  );
}
