/**
 * The rules both sides need to agree on, in a file with no server imports —
 * the sign-in form is a client component, and importing them from the module
 * that hashes passwords would drag argon2 and the Postgres driver into the
 * browser bundle.
 */
export const USERNAME_RE = /^[a-z0-9_-]{3,24}$/;

/** Length is the only rule that reliably helps; character-class rules mostly
 *  produce "Password1!". */
export const MIN_PASSWORD = 10;
