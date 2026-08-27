import { Pool } from "pg";

/**
 * One pool for the whole server. Vercel injects POSTGRES_URL when you attach a
 * database; DATABASE_URL is the name everything else in the world uses, so
 * accept either rather than making the deploy depend on which one you set.
 *
 * The pool is deliberately small: serverless functions each get their own, and
 * a generous per-function pool is how a free-tier Postgres runs out of
 * connections at exactly the moment the site gets popular.
 */
declare global {
  // eslint-disable-next-line no-var
  var _pool: Pool | undefined;
}

const connectionString = process.env.POSTGRES_URL || process.env.DATABASE_URL;

export const pool =
  global._pool ||
  new Pool({
    connectionString,
    max: 3,
    ssl: connectionString?.includes("localhost") ? false : { rejectUnauthorized: false },
  });

if (process.env.NODE_ENV !== "production") global._pool = pool;

/** True when a database is configured at all — lets the site run without one. */
export const hasDb = Boolean(connectionString);
