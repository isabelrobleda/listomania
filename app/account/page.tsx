import { auth, signOut } from "@/auth";
import { hasDb } from "@/lib/db";
import DeleteAccount from "@/components/DeleteAccount";
import SignInForms from "@/components/SignInForms";

export const metadata = {
  title: "Account — Listomania",
  robots: { index: false, follow: true },
};

/**
 * Everything an account can do, on one page: sign in, sign out, and leave.
 *
 * The delete button is here from the first day accounts exist rather than
 * "later". A service that can take your data and can't give it back is a
 * service you should not have signed into.
 */
export default async function AccountPage() {
  const session = await auth();

  if (!hasDb) {
    return (
      <>
        <h1>Account</h1>
        <p className="note" style={{ marginTop: 18 }}>
          <b>Accounts aren&rsquo;t switched on here.</b> This copy of the site is running without a
          database, so everything you tick and bookmark stays in this browser.
        </p>
      </>
    );
  }

  if (!session?.user) {
    return (
      <>
        <h1>Sign in</h1>
        <p style={{ maxWidth: "58ch", color: "var(--ink-2)" }}>
          Only so your ticks and bookmarks follow you off this browser. Nothing you mark is ever
          shown to anyone else.
        </p>

        <SignInForms github={Boolean(process.env.AUTH_GITHUB_ID)} />

        <p className="note" style={{ marginTop: 26, maxWidth: "60ch" }}>
          <b>What gets stored.</b> A username, a hash of your password, and the list rows
          you&rsquo;ve marked. That is the whole table. No email address &mdash; not even if you
          sign in with GitHub, which offers one; it&rsquo;s discarded rather than saved. The trade
          is that there is no reset link for anyone: the recovery code you get at signup is the way
          back in. You can delete all of it from this page at any time.
        </p>
      </>
    );
  }

  return (
    <>
      <h1>Account</h1>
      <p style={{ color: "var(--ink-2)" }}>
        Signed in as <b>{session.user.name || session.user.email}</b>. Your ticks and bookmarks now
        follow you to any browser you sign in to.
      </p>

      <div className="tools" style={{ marginTop: 18 }}>
        <form
          action={async () => {
            "use server";
            await signOut({ redirectTo: "/" });
          }}
        >
          <button className="chip" type="submit">
            Sign out
          </button>
        </form>
      </div>

      <DeleteAccount />
    </>
  );
}
