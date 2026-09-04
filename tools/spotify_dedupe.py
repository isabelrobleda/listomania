#!/usr/bin/env python3
"""
Remove duplicate tracks from a Spotify playlist, keeping the first copy of each.

This exists because `spotify_import.py --playlist <id> --append` used to reset
its row counter and re-add everything from the top. That bug is fixed; this
cleans up after it.

    python3 tools/spotify_dedupe.py <playlist_id>            # dry run, changes nothing
    python3 tools/spotify_dedupe.py <playlist_id> --apply    # actually remove

DRY RUN IS THE DEFAULT and that is not politeness. This is the only script here
that destroys anything, and a playlist has no undo — so it prints exactly what
it would remove and stops, and you have to come back and say --apply.

What counts as a duplicate: the same track URI appearing more than once. Not
"the same song by title", which would delete a live version, a remaster, or a
deliberate second appearance on a compilation. Only an exact repeat of the same
recording, which is the only thing the import bug could have produced.

The first occurrence of each URI is always kept, so the playlist's original
order survives.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spotify_import import Api, playlist_items, json  # noqa: E402


def all_uris(api, pid):
    """Every item in the playlist, in order, as (position, uri, label)."""
    out, offset = [], 0
    for path in (f"/playlists/{pid}/items", f"/playlists/{pid}/tracks"):
        out, offset = [], 0
        try:
            while True:
                res = api.request("GET", path, params={"limit": 100, "offset": offset})
                items = res.get("items") or []
                for n, it in enumerate(items):
                    tr = (it or {}).get("item") or (it or {}).get("track") or {}
                    uri = tr.get("uri")
                    if not uri:
                        continue
                    artists = ", ".join(a.get("name", "") for a in tr.get("artists") or [])
                    out.append((offset + n, uri, f"{artists} — {tr.get('name', '')}"))
                if len(items) < 100:
                    return out
                offset += 100
        except Exception as e:
            last = e
            continue
    if not out:
        raise SystemExit(f"Could not read the playlist: {last}")
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply_it = "--apply" in sys.argv
    if len(args) != 1:
        sys.exit(__doc__)
    pid = args[0].split("/")[-1].split("?")[0]

    api = Api()
    me = api.request("GET", "/me")
    print(f"Signed in as {me.get('id')}")

    items = all_uris(api, pid)
    print(f"{len(items)} tracks in the playlist")

    seen = set()
    dupes = []          # (position, uri, label) to remove
    for pos, uri, label in items:
        if uri in seen:
            dupes.append((pos, uri, label))
        else:
            seen.add(uri)

    print(f"{len(seen)} distinct tracks, {len(dupes)} duplicate copies")
    if not dupes:
        print("Nothing to do.")
        return

    for pos, _, label in dupes[:15]:
        print(f"  would remove position {pos}: {label}")
    if len(dupes) > 15:
        print(f"  … and {len(dupes) - 15} more")

    if not apply_it:
        print("\nDry run — nothing was changed.")
        print(f"Re-run with --apply to remove those {len(dupes)} copies.")
        return

    # Group positions by URI, because that is the shape the remove endpoint
    # wants. Positions are taken against the snapshot fetched above, and the
    # snapshot id is sent with the request, so Spotify removes exactly those
    # occurrences even though the list shifts as they go.
    snap = api.request("GET", f"/playlists/{pid}", params={"fields": "snapshot_id"})
    snapshot = snap.get("snapshot_id")

    by_uri = {}
    for pos, uri, _ in dupes:
        by_uri.setdefault(uri, []).append(pos)

    tracks = [{"uri": u, "positions": p} for u, p in by_uri.items()]
    removed = 0
    for i in range(0, len(tracks), 100):
        chunk = tracks[i:i + 100]
        body = {"tracks": chunk}
        if snapshot:
            body["snapshot_id"] = snapshot
        for path in (f"/playlists/{pid}/items", f"/playlists/{pid}/tracks"):
            try:
                res = api.request("DELETE", path, data=json.dumps(body))
                snapshot = res.get("snapshot_id", snapshot)
                removed += sum(len(t["positions"]) for t in chunk)
                break
            except Exception as e:
                last = e
        else:
            print(f"  could not remove a batch: {last}")
            break
        print(f"  removed {removed}/{len(dupes)}")

    print(f"\nDone. {removed} duplicate copies removed.")


if __name__ == "__main__":
    main()
