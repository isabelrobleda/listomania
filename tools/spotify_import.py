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
  python3 spotify_import.py 1001-albums-2-tracks.csv "1001 Albums"

Progress is saved to <csv>.progress.json, so re-running the same command
resumes instead of duplicating. Misses go to <csv>.notfound.csv.
"""

import csv
import json
import os
import sys
import time

try:
    import requests
    from spotipy.oauth2 import SpotifyOAuth
except ImportError:
    sys.exit("Missing dependency. Run:  pip3 install spotipy")

CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID") or "PASTE_YOUR_CLIENT_ID_HERE"
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET") or "PASTE_YOUR_CLIENT_SECRET_HERE"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-modify-private playlist-modify-public"
API = "https://api.spotify.com/v1"

# Development Mode apps have a daily request quota. Pacing requests keeps you
# under it for longer; PAUSE seconds are slept between each track lookup.
PAUSE = float(os.environ.get("PAUSE", "0.4"))
# If Spotify asks us to wait longer than this many seconds, stop instead of
# sleeping (a daily-quota 429 asks for ~24h).
MAX_WAIT = 900


class QuotaExceeded(Exception):
    pass


class Api:
    def __init__(self):
        if "PASTE_YOUR" in CLIENT_ID or "PASTE_YOUR" in CLIENT_SECRET:
            sys.exit("Set CLIENT_ID and CLIENT_SECRET near the top of this file first.")
        self.auth = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
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
                        f"Spotify says wait {wait}s (~{hrs:.1f}h) - daily quota reached."
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


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 spotify_import.py <tracks.csv> [playlist name]")
    csv_path = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else "Imported Playlist"

    progress_path = csv_path + ".progress.json"
    notfound_path = csv_path + ".notfound.csv"

    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"{len(rows)} rows in {csv_path}")

    state = {"playlist_id": None, "done": 0, "added": 0}
    if os.path.exists(progress_path):
        state.update(json.load(open(progress_path)))
        print(f"Resuming: {state['done']} rows already processed, {state['added']} added.")

    api = Api()
    me = api.request("GET", "/me")
    print(f"Signed in as {me.get('id')}")

    if not state["playlist_id"]:
        pl = api.request(
            "POST",
            "/me/playlists",
            data=json.dumps(
                {
                    "name": name,
                    "public": False,
                    "description": "Two tracks from each album in the 1001 Albums list.",
                }
            ),
        )
        state["playlist_id"] = pl["id"]
        json.dump(state, open(progress_path, "w"))
        print(f"Created playlist: {pl.get('external_urls', {}).get('spotify')}")

    pid = state["playlist_id"]
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
            state["done"] = state["added"]      # rewind so they're retried
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
            hit = find_track(api, artist, track, album)
            if hit:
                buffer.append(hit[0])
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
        state["done"] = state["added"]
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
