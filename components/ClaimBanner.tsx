"use client";

import { useEffect, useState } from "react";
import { useSession } from "next-auth/react";
import { unclaimedMarks, claimLocalMarks, clearLocalMarks } from "@/lib/progress";

/**
 * Shown once, to a signed-in person whose browser is still holding marks from
 * before they had an account.
 *
 * It asks rather than merging silently, and that is the whole point: on a
 * shared laptop, an automatic merge hands one person's reading history to
 * whoever signs in next. "Keep them separate" is a real answer, and dismissing
 * is remembered so nobody gets nagged.
 */
const DISMISS = "listomania:claim-dismissed";

export default function ClaimBanner() {
  const { status } = useSession();
  const [n, setN] = useState(0);
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(0);

  useEffect(() => {
    if (status !== "authenticated") return;
    try {
      if (window.localStorage.getItem(DISMISS)) return;
    } catch {
      /* storage blocked: showing the offer once is harmless */
    }
    setN(unclaimedMarks().length);
  }, [status]);

  if (status !== "authenticated" || (n === 0 && done === 0)) return null;

  if (done > 0) {
    return (
      <p className="claim ok">
        <b>Added {done} {done === 1 ? "item" : "items"} to your account.</b> They&rsquo;ll follow you
        to any browser you sign in to.
      </p>
    );
  }

  const dismiss = () => {
    try {
      window.localStorage.setItem(DISMISS, "1");
    } catch {
      /* nothing to remember it with; the banner just reappears */
    }
    setN(0);
  };

  return (
    <div className="claim">
      <p>
        <b>This browser is holding {n} {n === 1 ? "item" : "items"}</b> you marked before signing in.
        Add them to your account?
      </p>
      <div className="row">
        <button
          className="chip"
          disabled={busy}
          onClick={async () => {
            setBusy(true);
            try {
              const added = await claimLocalMarks();
              clearLocalMarks();
              setDone(added);
              setN(0);
            } catch {
              setBusy(false);
            }
          }}
        >
          {busy ? "Adding…" : "Add them"}
        </button>
        <button className="chip" onClick={dismiss}>
          Keep them separate
        </button>
      </div>
    </div>
  );
}
