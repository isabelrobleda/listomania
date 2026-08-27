"use client";

import { useState } from "react";
import { signIn } from "next-auth/react";
import { MIN_PASSWORD, MAX_USERNAME, cleanUsername } from "@/lib/authRules";

/**
 * Sign in, create an account, or recover one — three modes of one small form.
 *
 * The sign-in failure message is the same sentence whatever went wrong, on
 * purpose: "no such user" is a way to find out which usernames exist.
 */
type Mode = "in" | "new" | "lost";

export default function SignInForms({ github }: { github: boolean }) {
  const [mode, setMode] = useState<Mode>("in");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [recovery, setRecovery] = useState("");

  // Shown after signing up or recovering: the only time this code is readable.
  if (recovery) {
    return (
      <div className="claim" style={{ maxWidth: "56ch" }}>
        <p>
          <b>Write this down before you close the page.</b> It&rsquo;s the only way back into your
          account if you forget your password — this site has no email address to send a reset link
          to, which is rather the point.
        </p>
        <p className="reccode">{recovery}</p>
        <div className="row">
          <button className="chip" onClick={() => (window.location.href = "/account")}>
            I&rsquo;ve written it down
          </button>
        </div>
      </div>
    );
  }

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setBusy(true);
    setError("");
    const f = new FormData(e.currentTarget);
    // Cleaned the same way the server will clean it, so what someone types and
    // what gets looked up can't disagree.
    const username = cleanUsername(f.get("username")) || "";
    const password = String(f.get("password") || "");

    try {
      if (mode === "in") {
        const res = await signIn("credentials", { username, password, redirect: false });
        if (res?.error) setError("That username and password don't match. Try again.");
        else window.location.href = "/account";
        return;
      }

      const url = mode === "new" ? "/api/signup" : "/api/recover";
      const payload =
        mode === "new"
          ? { username, password }
          : { username, password, code: String(f.get("code") || "") };

      const res = await fetch(url, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Something went wrong.");
        return;
      }
      // Sign them straight in, then show the code they must keep.
      await signIn("credentials", { username, password, redirect: false });
      setRecovery(data.recovery);
    } finally {
      setBusy(false);
    }
  }

  const tabs: [Mode, string][] = [
    ["in", "Sign in"],
    ["new", "Create account"],
    ["lost", "Forgot password"],
  ];

  return (
    <div style={{ maxWidth: "42ch" }}>
      <div className="tools" style={{ marginBottom: 16 }}>
        {tabs.map(([m, label]) => (
          <button
            key={m}
            className="chip"
            aria-pressed={mode === m}
            onClick={() => {
              setMode(m);
              setError("");
            }}
          >
            {label}
          </button>
        ))}
      </div>

      <form className="authform" onSubmit={submit}>
        <label>
          Username
          <input
            name="username"
            autoComplete="username"
            required
            maxLength={MAX_USERNAME * 2}
            placeholder={`anything, up to ${MAX_USERNAME} characters`}
          />
        </label>

        {mode === "lost" && (
          <label>
            Recovery code
            <input name="code" required placeholder="XXXX-XXXX-XXXX-XXXX" autoComplete="off" />
          </label>
        )}

        <label>
          {mode === "in" ? "Password" : "New password"}
          <input
            name="password"
            type="password"
            required
            minLength={mode === "in" ? undefined : MIN_PASSWORD}
            autoComplete={mode === "in" ? "current-password" : "new-password"}
            placeholder={mode === "in" ? "" : `at least ${MIN_PASSWORD} characters`}
          />
        </label>

        {error && <p className="autherr">{error}</p>}

        <button className="plbtn" type="submit" disabled={busy}>
          {busy
            ? "…"
            : mode === "in"
              ? "Sign in"
              : mode === "new"
                ? "Create account"
                : "Set new password"}
        </button>
      </form>

      {github && (
        <>
          <p className="oralso">or</p>
          <button className="chip" onClick={() => signIn("github", { callbackUrl: "/account" })}>
            Continue with GitHub
          </button>
        </>
      )}
    </div>
  );
}
