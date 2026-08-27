"use client";

import { useState } from "react";
import { signOut } from "next-auth/react";

/** Two clicks, no dark pattern: the second one says exactly what it does. */
export default function DeleteAccount() {
  const [armed, setArmed] = useState(false);
  const [busy, setBusy] = useState(false);

  return (
    <div style={{ marginTop: 30 }}>
      {!armed ? (
        <button className="chip" onClick={() => setArmed(true)}>
          Delete my account
        </button>
      ) : (
        <div className="claim">
          <p>
            <b>This deletes everything.</b> Your account, and every tick and bookmark attached to
            it. It cannot be undone, and there&rsquo;s no copy kept.
          </p>
          <div className="row">
            <button
              className="chip danger"
              disabled={busy}
              onClick={async () => {
                setBusy(true);
                const res = await fetch("/api/account", { method: "DELETE" });
                if (res.ok) await signOut({ callbackUrl: "/" });
                else setBusy(false);
              }}
            >
              {busy ? "Deleting…" : "Yes, delete it all"}
            </button>
            <button className="chip" onClick={() => setArmed(false)}>
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
