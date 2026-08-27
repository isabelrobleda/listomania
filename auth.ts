import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
import PostgresAdapter from "@auth/pg-adapter";
import { pool, hasDb } from "@/lib/db";

/**
 * Sign-in exists for one reason: so the things you've ticked and bookmarked
 * follow you off this browser. Nothing else about you is wanted here.
 *
 * GitHub only, for now. It's free, it's two minutes to register, and it needs
 * no email sender. Google and magic links are additive later — the adapter and
 * the marks table don't care which provider a person used.
 *
 * If no database is configured the site still builds and runs; it just has no
 * accounts. That keeps a fork or a local checkout working without secrets.
 */
export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: hasDb ? PostgresAdapter(pool) : undefined,
  providers: [GitHub],
  session: { strategy: hasDb ? "database" : "jwt" },
  pages: { signIn: "/account" },
  callbacks: {
    session({ session, user }) {
      if (user) session.user.id = String(user.id);
      return session;
    },
  },
  trustHost: true,
});
