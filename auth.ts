import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
import Credentials from "next-auth/providers/credentials";
import PostgresAdapter from "@auth/pg-adapter";
import { pool, hasDb } from "@/lib/db";
import {
  checkUsername,
  findByUsername,
  isLocked,
  noteFailure,
  noteSuccess,
  verifySecret,
} from "@/lib/accounts";

/**
 * Sign-in exists for one reason: so the things you've ticked and bookmarked
 * follow you off this browser. Nothing else about you is wanted here.
 *
 * A username and password is the main path, because asking a reader of book
 * lists for a GitHub account is a strange demand, and because a username is
 * less about them than an email address is. GitHub stays as a one-click
 * alternative for people who have one.
 *
 * Sessions are signed cookies rather than database rows: a credentials provider
 * can't use database sessions. The adapter still owns the user table, so both
 * paths meet at users.id and the marks don't care which was used.
 */
const forgetEmail = (id: string) =>
  pool.query("UPDATE users SET email = NULL, image = NULL WHERE id = $1", [id]);

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: hasDb ? PostgresAdapter(pool) : undefined,
  session: { strategy: "jwt" },
  providers: [
    GitHub,
    Credentials({
      name: "Username",
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(raw) {
        if (!hasDb) return null;
        const username = checkUsername(raw?.username);
        const password = typeof raw?.password === "string" ? raw.password : "";
        if (!username || !password) return null;

        const user = await findByUsername(username);
        // Every failure returns the same null, and the caller shows the same
        // sentence. Telling someone "no such user" hands them a list of which
        // usernames exist.
        if (!user || isLocked(user)) return null;

        if (!(await verifySecret(user.password_hash, password))) {
          await noteFailure(user.id);
          return null;
        }
        await noteSuccess(user.id);
        return { id: String(user.id), name: username };
      },
    }),
  ],
  pages: { signIn: "/account" },
  events: {
    /**
     * GitHub hands over an email address whether or not we want one, and the
     * adapter dutifully stores it. We don't want one: a username account has no
     * email, and the honest thing is for the GitHub path to store no more than
     * the username path does. So it's thrown away the moment the row exists,
     * and again on every sign-in in case the provider refreshes it.
     *
     * The trade-off, stated plainly on the account page: with no address on
     * file there is no "email me a reset link" for anyone, ever.
     */
    async createUser({ user }) {
      if (hasDb && user.id) await forgetEmail(user.id);
    },
    async signIn({ user }) {
      if (hasDb && user?.id) await forgetEmail(user.id);
    },
  },
  callbacks: {
    jwt({ token, user }) {
      if (user?.id) token.uid = user.id;
      return token;
    },
    session({ session, token }) {
      if (token.uid) session.user.id = String(token.uid);
      return session;
    },
  },
  trustHost: true,
});
