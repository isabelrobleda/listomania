"use client";

import Link from "next/link";
import { useSession } from "next-auth/react";

export default function AccountButton() {
  const { data, status } = useSession();

  // Deliberately renders nothing while the session resolves rather than
  // flashing "Sign in" at someone who is already signed in.
  if (status === "loading") return <span className="acct ghost" aria-hidden="true" />;

  return (
    <Link className="acct" href="/account">
      {status === "authenticated"
        ? data?.user?.name || data?.user?.email || "Account"
        : "Sign in"}
    </Link>
  );
}
