"use client";

import { useEffect } from "react";
import { useSession } from "next-auth/react";
import { syncWithAccount } from "@/lib/progress";

/** Points the mark stores at the account (or back at this browser) when the
 *  session resolves. Renders nothing; it exists to keep that wiring in one
 *  place instead of inside a component that also draws something. */
export default function SyncProvider() {
  const { status } = useSession();

  useEffect(() => {
    if (status === "loading") return;
    syncWithAccount(status === "authenticated");
  }, [status]);

  return null;
}
