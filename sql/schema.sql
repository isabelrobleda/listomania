-- Listomania's entire server-side state.
--
-- Two things live here and nothing else: who you are (so the marks have an
-- owner), and what you ticked or bookmarked. The lists themselves stay in the
-- repository as JSON — a list is content, not user data, and putting it in a
-- database would make every edit an invisible write instead of a reviewable
-- diff.

-- ---------------------------------------------------------------- Auth.js ---
-- Verbatim from the Auth.js Postgres adapter. Don't hand-edit these.
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255),
  "emailVerified" TIMESTAMPTZ,
  image TEXT
);

CREATE TABLE IF NOT EXISTS accounts (
  id SERIAL PRIMARY KEY,
  "userId" INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type VARCHAR(255) NOT NULL,
  provider VARCHAR(255) NOT NULL,
  "providerAccountId" VARCHAR(255) NOT NULL,
  refresh_token TEXT,
  access_token TEXT,
  expires_at BIGINT,
  id_token TEXT,
  scope TEXT,
  session_state TEXT,
  token_type TEXT
);

CREATE TABLE IF NOT EXISTS sessions (
  id SERIAL PRIMARY KEY,
  "userId" INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  expires TIMESTAMPTZ NOT NULL,
  "sessionToken" VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS verification_token (
  identifier TEXT,
  expires TIMESTAMPTZ NOT NULL,
  token TEXT,
  PRIMARY KEY (identifier, token)
);

-- ------------------------------------------------------------------ Marks ---
-- One row per (person, kind, list, item). The primary key is the whole tuple,
-- so a double-click or a replayed request can't create a duplicate — ticking
-- something twice is the same as ticking it once, which is what a person would
-- expect and what makes the sync safe to retry.
--
-- kind: 'done'  — I've read / seen / eaten at this
--       'want'  — it's on my list
-- They are separate rows on purpose: wanting to reread a book you've read is a
-- normal thing to want.
CREATE TABLE IF NOT EXISTS marks (
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  kind    TEXT NOT NULL CHECK (kind IN ('done', 'want')),
  list_id TEXT NOT NULL,
  item_key TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, kind, list_id, item_key)
);

CREATE INDEX IF NOT EXISTS marks_user_idx ON marks (user_id);

-- --------------------------------------------------------------- Usernames ---
-- Password accounts. Nullable because a GitHub account has none of this, and a
-- username account has no email — the two paths meet at users.id and nowhere
-- else.
--
-- There is deliberately no email column for password accounts. It would be the
-- obvious way to offer password resets, and it is exactly the piece of personal
-- data this site has no other use for. The recovery code is the trade: one
-- string, shown once at signup, hashed here the same way the password is.
ALTER TABLE users ADD COLUMN IF NOT EXISTS username TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS recovery_hash TEXT;

-- Case-insensitive uniqueness: "Isabel" and "isabel" must not be two people.
CREATE UNIQUE INDEX IF NOT EXISTS users_username_key ON users (lower(username));

-- Per-account throttling. Guessing a password should get slower for the account
-- being guessed at, without telling the guesser whether it exists.
ALTER TABLE users ADD COLUMN IF NOT EXISTS failed_logins INTEGER NOT NULL DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS locked_until TIMESTAMPTZ;
