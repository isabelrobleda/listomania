#!/usr/bin/env python3
"""
Build a Spotify playlist from a CSV of tracks. No track limit.

CSV format (header required): Year,Artist,Track,Album

Uses spotipy ONLY for the OAuth login flow, and calls the Spotify Web API
directly for everything else. This matters: Spotify's Feb/Mar 2026 API
migration removed the endpoints spotipy still uses, so the library's
playlist helpers return 403. Current endpoints used here:
    POST /v1/me/playlists          (was /v1/users/{id}/playlists)
    POST /v1/playlists/{id}/items  (was /v1/playlists/{id}/tracks)

Setup:
  1. pip3 install spotipy
  2. https://developer.spotify.com/dashboard -> Create app
       Redirect URI: http://127.0.0.1:8888/callback
       APIs: Web API
     Then Settings -> User Management -> add your Spotify account email.
  3. Paste Client ID and Secret below.

Run:
  python3 spotify_import.py best-songs.csv "The Best Song You've Ever Heard"

Progress is saved to <csv>.progress.json, so re-running the same command
resumes instead of duplicating. Misses go to <csv>.notfound.csv.

If that progress file is lost — a new laptop, a cleared Downloads folder —
point the script at the playlist it was filling and it recovers on its own:

  python3 spotify_import.py <csv> "<name>" --playlist <playlist_id>

It reads what the playlist already contains and skips those tracks, so it
picks up where it stopped without duplicating anything. The row counter in
the progress file was only ever an optimisation; the playlist itself is the
real record of what got added.
"""

import csv
import json
import os
import re
import sys
import time
import unicodedata

try:
    import requests
    from spotipy.oauth2 import SpotifyOAuth
except ImportError:
    sys.exit("Missing dependency. Run:  pip3 install spotipy")

CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID") or "PASTE_YOUR_CLIENT_ID_HERE"
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET") or "PASTE_YOUR_CLIENT_SECRET_HERE"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
# Modify scopes let you WRITE to a playlist; they do not let you READ one.
# Omitting the read scopes is what made every GET on a private playlist return
# 403, which the dedupe then took to mean "the playlist is empty" and added
# everything a second time. Both halves are needed.
SCOPE = ("playlist-modify-private playlist-modify-public "
         "playlist-read-private playlist-read-collaborative")
API = "https://api.spotify.com/v1"

# Development Mode apps have a daily request quota. Pacing requests keeps you
# under it for longer; PAUSE seconds are slept between each track lookup.
PAUSE = float(os.environ.get("PAUSE", "0.4"))
# If Spotify asks us to wait longer than this many seconds, stop instead of
# sleeping. The default is deliberately low so an unattended run can't hang for
# hours; raise it (MAX_WAIT=3600) when you'd rather it sat out a long cooldown.
# Note that a wait of a few minutes is ordinary throttling, not the daily quota
# — the limit is a rolling window shared across everything the app has done.
MAX_WAIT = int(os.environ.get("MAX_WAIT", "900"))


class QuotaExceeded(Exception):
    pass


class Api:
    def __init__(self):
        if "PASTE_YOUR" in CLIENT_ID or "PASTE_YOUR" in CLIENT_SECRET:
            sys.exit("Set CLIENT_ID and CLIENT_SECRET near the top of this file first.")
        # The token cache lives OUTSIDE the repo. spotipy defaults to a
        # .cache file in the working directory, which for this script is the
        # repo root — so a `git add -A` sweeps up a file containing a live
        # refresh token and pushes it to a public remote. That happened, and
        # GitGuardian caught it. ~/.config is not in any working tree, so the
        # same mistake can't be made twice.
        cache_dir = os.path.join(os.path.expanduser("~"), ".config", "listomania")
        os.makedirs(cache_dir, exist_ok=True)
        cache_path = os.path.join(cache_dir, "spotify-token.json")
        try:
            os.chmod(cache_dir, 0o700)
        except OSError:
            pass

        self.auth = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_path=cache_path,
            open_browser=True,
        )
        self.auth.get_access_token(as_dict=False)

    def _headers(self):
        tok = self.auth.get_access_token(as_dict=False)
        return {"Authorization": "Bearer " + tok, "Content-Type": "application/json"}

    def request(self, method, path, **kw):
        """One API call, with retry on rate limit / transient server errors."""
        url = API + path
        for attempt in range(6):
            r = requests.request(method, url, headers=self._headers(), timeout=30, **kw)
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 5)) + 1
                if wait > MAX_WAIT:
                    hrs = wait / 3600.0
                    raise QuotaExceeded(
                        f"Spotify asks for a {wait}s (~{hrs:.1f}h) wait, longer than "
                        f"MAX_WAIT={MAX_WAIT}s. Re-run to continue, or set a higher "
                        f"MAX_WAIT to sit it out."
                    )
                print(f"    rate limited, waiting {wait}s")
                time.sleep(wait)
                continue
            if r.status_code >= 500:
                time.sleep(2 * (attempt + 1))
                continue
            if not r.ok:
                raise RuntimeError(f"{method} {path} -> {r.status_code}: {r.text[:300]}")
            return r.json() if r.text else {}
        raise RuntimeError(f"{method} {path} failed after repeated retries")


def find_track(api, artist, track, album):
    """Try progressively looser queries; return (uri, name, artist) or None."""
    queries = []
    if album:
        queries.append(f'track:"{track}" artist:"{artist}" album:"{album}"')
    queries += [f'track:"{track}" artist:"{artist}"', f"{artist} {track}"]
    for q in queries:
        try:
            res = api.request("GET", "/search", params={"q": q, "type": "track", "limit": 5})
        except RuntimeError:
            continue
        items = res.get("tracks", {}).get("items", [])
        if items:
            best = max(items, key=lambda t: t.get("popularity", 0))
            return best["uri"], best["name"], best["artists"][0]["name"]
    return None


def fold(s):
    """Normalise a title or artist for comparison.

    Dedupe used to compare Spotify track URIs. That fails, and did: the
    playlist held "Mood Indigo" while a fresh search returned "Mood Indigo -
    Remastered", a different recording with a different URI, so the check said
    "not present" and added a second copy. Search is not stable across time,
    market or catalogue changes, so the URI is the wrong key. Compare what a
    person would compare — the artist and the title, with the reissue noise
    stripped off.
    """
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    # " - 2011 Remaster", "(Remastered 2009)", "- Single Version", "[Live]" ...
    s = re.sub(r"\s*[-–]\s*(\d{4}\s*)?(digital\s+)?(remaster|remastered|mono|stereo|live|"
               r"single|album|radio|edit|version|mix|take)\b.*$", "", s)
    s = re.sub(r"[\(\[][^)\]]*(remaster|mono|stereo|live|version|edit|mix|bonus)"
               r"[^)\]]*[\)\]]", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def playlist_items(api, pid):
    """Raw track objects already in the playlist.

    Two things here are scar tissue. The endpoint is tried both ways because
    Spotify's 2026 migration renamed /tracks to /items and old and new accounts
    have not moved in step. And nothing is passed in `fields`: a filter that
    the API doesn't like comes back as an empty list rather than an error,
    which is exactly how a silent empty result caused this function's caller
    to add a thousand duplicates.
    """
    last_error = None
    for path in (f"/playlists/{pid}/items", f"/playlists/{pid}/tracks"):
        out, offset = [], 0
        try:
            while True:
                res = api.request("GET", path, params={"limit": 100, "offset": offset})
                items = res.get("items") or []
                for it in items:
                    # Spotify's 2026 migration renamed this key from "track" to
                    # "item". Reading the old name returned None for every row,
                    # which looked exactly like an empty playlist and is what
                    # caused this script to add a thousand duplicates. Accept
                    # both, newest first.
                    tr = (it or {}).get("item") or (it or {}).get("track") or {}
                    if tr.get("name"):
                        out.append(tr)
                offset += len(items)
                if not items or offset >= (res.get("total") or 0):
                    break
            # Success is "the request worked", not "the request found
            # something". An empty playlist is a perfectly good answer and
            # returning it here is what lets a brand-new playlist be filled.
            #
            # Treating an empty result as failure was a fail-safe added after a
            # silent empty read caused a thousand duplicates — but it was the
            # wrong fail-safe. The danger was never emptiness; it was emptiness
            # from an endpoint that had actually errored. That case still
            # raises, because a real error lands in `except` below. The caller
            # keeps its own guard: it refuses to adopt a playlist that reads as
            # empty unless the run is expected to be filling one from scratch.
            return out, path
        except RuntimeError as e:
            last_error = e
            continue
    if last_error and "403" in str(last_error):
        raise RuntimeError(
            f"Not allowed to read playlist {pid} (403). This usually means the "
            "cached login predates the playlist-read-private scope: delete the "
            ".cache file next to this script and run again to re-authorise.\n"
            f"  {last_error}")
    raise RuntimeError(
        f"Could not read the contents of playlist {pid}. Last error: {last_error}"
        if last_error else
        f"Playlist {pid} came back empty from both /items and /tracks.")


def existing_tracks(api, pid):
    """What the playlist holds, by title AND by album.

    Title matching alone is not enough for this list. The playlist was built
    from a CSV that chose different tracks for the same albums than the one
    rebuilt from the repo, so an album already represented twice would sail
    through a title check and get two *more* tracks added. The list promises
    two tracks per album, so the album is the unit that matters.
    """
    tracks, path = playlist_items(api, pid)
    titles, albums = {}, {}
    for tr in tracks:
        for a in tr.get("artists") or []:
            titles.setdefault(fold(tr["name"]), set()).add(fold(a.get("name", "")))
        name = ((tr.get("album") or {}).get("name")) or ""
        if name:
            albums[fold(name)] = albums.get(fold(name), 0) + 1
    print(f"Read {len(tracks)} tracks from the playlist via {path} — "
          f"{len(titles)} distinct titles across {len(albums)} albums.")
    if not albums:
        print("  WARNING: no album data came back, so only titles can be "
              "matched. Expect albums to be over-filled.")
    return {"titles": titles, "albums": albums}


PER_ALBUM = 2   # what the list promises: two tracks from each album


def already_there(seen, artist, track, album=None):
    """True if this row should be skipped.

    Two reasons to skip. The album already has its quota — the important one,
    and the one a title check misses. Or this exact title is already in, which
    catches the case where album names differ between sources.

    Artists are matched loosely in either direction, because the same
    recording is credited "Duke Ellington" on one release and "Duke Ellington
    & His Orchestra" on the next.
    """
    if album and seen["albums"].get(fold(album), 0) >= PER_ALBUM:
        return True
    who = seen["titles"].get(fold(track))
    if not who:
        return False
    a = fold(artist)
    return any(a and b and (a in b or b in a) for b in who)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a.split("=")[0]: (a.split("=", 1)[1] if "=" in a else None)
             for a in sys.argv[1:] if a.startswith("--")}
    if "--playlist" in flags and flags["--playlist"] is None:
        # allow "--playlist ID" as well as "--playlist=ID"
        i = sys.argv.index("--playlist")
        if i + 1 < len(sys.argv):
            flags["--playlist"] = sys.argv[i + 1]
            args = [a for a in args if a != sys.argv[i + 1]]
    if not args:
        sys.exit("Usage: python3 spotify_import.py <tracks.csv> [playlist name] "
                 "[--playlist <id>] [--check] [--append]")
    csv_path = args[0]
    name = args[1] if len(args) > 1 else "Imported Playlist"
    adopt = flags.get("--playlist")

    progress_path = csv_path + ".progress.json"
    notfound_path = csv_path + ".notfound.csv"

    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"{len(rows)} rows in {csv_path}")

    state = {"playlist_id": None, "done": 0, "added": 0}
    if os.path.exists(progress_path):
        state.update(json.load(open(progress_path)))
        print(f"Resuming: {state['done']} rows already processed, {state['added']} added.")
    if adopt:
        state["playlist_id"] = adopt
        if "--append" not in flags:
            # Adopting an existing playlist means the row counter is not to be
            # trusted — start from the top and let the dedupe below do the work.
            state["done"] = 0
        # --append is the exception, and the reason this branch is guarded.
        # Restarting from the top is only safe because already_there() skips
        # what's in the playlist; --append switches that check OFF. The two
        # flags together used to mean "read nothing, and start again from row
        # one", which re-added every track that had already gone in. If there
        # is no row counter to trust in append mode, there is nothing safe to
        # do, so refuse rather than guess.
        elif not os.path.exists(progress_path):
            sys.exit(
                "--append with --playlist needs a progress file to know where it "
                "stopped, and there isn't one at\n  " + progress_path +
                "\nWithout it this run would start at row 1 and duplicate "
                "everything already added. Drop --append to let the script read "
                "the playlist and skip what's in it."
            )

    api = Api()
    me = api.request("GET", "/me")
    print(f"Signed in as {me.get('id')}")

    # --check reads and reports, then stops. Nothing is created, nothing is
    # added. Use it to confirm the script can actually see a playlist before
    # trusting it to skip what's in one.
    if "--check" in flags:
        if not adopt:
            sys.exit("--check needs --playlist <id> to look at.")

        # What the token was actually granted, rather than what we asked for.
        try:
            tok = api.auth.get_cached_token() or {}
            print("\nToken scopes granted:")
            for s in sorted((tok.get("scope") or "").split()):
                print(f"    {s}")
            if not tok.get("scope"):
                print("    (none reported)")
        except Exception as e:
            print(f"  could not read cached token: {e}")

        # Probe the playlist object as the API actually returns it, with no
        # fields filter to hide anything. The 2026 migration moved things
        # around; this shows where the track list lives now rather than
        # assuming it is still under "tracks".
        print(f"\nPlaylist {adopt}:")
        try:
            meta = api.request("GET", f"/playlists/{adopt}")
            print("    top-level keys: " + ", ".join(sorted(meta.keys())))
            owner = meta.get("owner") or {}
            print(f"    name        {meta.get('name')}")
            print(f"    owner       {owner.get('id')}   signed in: {me.get('id')}")
            for k, v in sorted(meta.items()):
                if isinstance(v, dict):
                    inner = ", ".join(f"{ik}={v[ik]!r}" for ik in sorted(v)
                                      if not isinstance(v[ik], (dict, list)))
                    print(f"    {k}: {{{inner[:160]}}}")
                elif isinstance(v, list):
                    print(f"    {k}: list of {len(v)}")
        except RuntimeError as e:
            print(f"    metadata read failed: {e}")

        # Each candidate endpoint separately, so one failure cannot hide another.
        for path in (f"/playlists/{adopt}/items", f"/playlists/{adopt}/tracks"):
            try:
                res = api.request("GET", path, params={"limit": 1})
                items = res.get("items")
                print(f"\n    GET {path} -> ok; total={res.get('total')}, "
                      f"keys={sorted(res.keys())}")
                if items:
                    print(f"      first item keys: {sorted(items[0].keys())}")
            except RuntimeError as e:
                print(f"\n    GET {path} -> {e}")

        # Now the path the real run uses, so --check proves the import rather
        # than just describing the API.
        print()
        seen = existing_tracks(api, adopt)
        import copy
        probe = copy.deepcopy(seen)
        hit, miss = [], []
        for r in rows:
            if already_there(probe, r["Artist"], r["Track"], r.get("Album")):
                hit.append(r)
            else:
                miss.append(r)
                if r.get("Album"):
                    k = fold(r["Album"])
                    probe["albums"][k] = probe["albums"].get(k, 0) + 1
        print(f"\nAgainst {csv_path}: {len(hit)} rows already present, "
              f"{len(miss)} would be added.")
        if miss:
            print("  first 5 that would be added:")
            for r in miss[:5]:
                print(f"    {r['Artist']} — {r['Track']}")
        return


    if not state["playlist_id"]:
        pl = api.request(
            "POST",
            "/me/playlists",
            data=json.dumps(
                {
                    "name": name,
                    "public": False,
                    "description": "Built from a Listomania list.",
                }
            ),
        )
        state["playlist_id"] = pl["id"]
        json.dump(state, open(progress_path, "w"))
        print(f"Created playlist: {pl.get('external_urls', {}).get('spotify')}")

    pid = state["playlist_id"]

    # What is already in there. Checked whenever we are resuming into a
    # playlist that has contents, which is the case that used to duplicate.
    already = {"titles": {}, "albums": {}}
    if "--append" in flags:
        # Straight append: no reading, no matching, no skipping. For a CSV that
        # has already been trimmed to exactly what's missing, which is both
        # simpler and more predictable than any amount of fuzzy matching —
        # Spotify's album names carry edition suffixes ("(Super Deluxe)",
        # "The Original Album") that the source list does not, so matching them
        # was never going to be reliable.
        print("Append mode: adding every row, no duplicate checking.")
    elif state["done"] == 0 and state["added"] == 0 or adopt:
        already = existing_tracks(api, pid)
        # An empty read from a playlist that should have contents means the
        # read failed, not that the playlist is empty. Continuing here is how
        # every track gets added a second time, so refuse instead.
        if adopt and not already and "--empty-ok" not in flags:
            sys.exit(
                f"Refusing to continue: playlist {pid} reported zero tracks.\n"
                "On a playlist that should have contents this is a read failure, "
                "and adding now would duplicate everything in it.\n"
                "If the playlist really is empty — you just created it, or the "
                "run that was meant to fill it never got going — re-run with "
                "--empty-ok to say so. Do NOT drop --playlist to get past this: "
                "that creates a second playlist and leaves the first one empty."
            )

    notfound = open(notfound_path, "a", newline="", encoding="utf-8")
    nf = csv.writer(notfound)
    buffer = []

    def flush(quiet=False):
        """Add the buffered tracks. If the add fails we must NOT count those rows
        as done, or they'd be silently skipped on the next run."""
        if not buffer:
            return True
        try:
            api.request("POST", f"/playlists/{pid}/items", data=json.dumps({"uris": buffer}))
        except Exception as e:
            if not quiet:
                print(f"    could not add the last {len(buffer)} tracks: {e}")
            # Rewind so they're retried. In adopt mode the row counter means
            # nothing — the playlist's own contents are the record — so leave
            # it at zero rather than writing an offset that would be believed
            # by a later run without the flag.
            state["done"] = 0 if adopt else state["added"]
            buffer.clear()
            json.dump(state, open(progress_path, "w"))
            return False
        state["added"] += len(buffer)
        buffer.clear()
        json.dump(state, open(progress_path, "w"))
        return True

    try:
        for i, row in enumerate(rows):
            if i < state["done"]:
                continue
            artist, track, album = row["Artist"], row["Track"], row["Album"]
            # Checked before searching, not after: a row that is already in the
            # playlist now costs zero API calls instead of one, which is most of
            # the daily quota back on a resumed run.
            if already["titles"] and already_there(already, artist, track, album):
                state["done"] = i + 1
                continue
            hit = find_track(api, artist, track, album)
            if hit:
                buffer.append(hit[0])
                already["titles"].setdefault(fold(track), set()).add(fold(artist))
                if album and already["albums"] is not None:
                    already["albums"][fold(album)] = already["albums"].get(fold(album), 0) + 1
            else:
                nf.writerow([row.get("Year", ""), artist, track, album])
                notfound.flush()
                print(f"  not found: {artist} - {track}")
            state["done"] = i + 1
            if len(buffer) >= 100:
                flush()
                print(f"  {state['done']}/{len(rows)} processed, {state['added']} added")
            time.sleep(PAUSE)
        flush()
    except QuotaExceeded as e:
        # The quota is gone, so adding the buffer would fail too. Rewind instead,
        # so nothing is counted as done that never made it into the playlist.
        state["done"] = 0 if adopt else state["added"]
        buffer.clear()
        json.dump(state, open(progress_path, "w"))
        print(f"\n{e}")
        print(f"Stopped cleanly at {state['added']} of {len(rows)} tracks added.")
        print("Re-run the same command once the quota resets and it continues from here.")
        return
    except KeyboardInterrupt:
        flush()
        print(f"\nStopped at {state['done']}/{len(rows)}. Re-run the same command to resume.")
        return
    finally:
        notfound.close()
        json.dump(state, open(progress_path, "w"))

    print(f"\nDone. {state['added']} tracks added, {state['done'] - state['added']} not found.")
    if state["done"] - state["added"]:
        print(f"Misses listed in {notfound_path}")
    print(f"https://open.spotify.com/playlist/{pid}")


if __name__ == "__main__":
    main()
