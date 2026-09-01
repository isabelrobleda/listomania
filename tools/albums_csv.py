# -*- coding: utf-8 -*-
"""Rebuild 1001-albums-2-tracks.csv from the list in content/shelves.json.

The CSV that fed the 1001 Albums playlist lived only in a Downloads folder and
went with the laptop. It turns out not to matter: the two tracks per album are
stored in the list itself, in the "Two most-played tracks" column, so the file
is derivable from the repo and always was. Anything a tool needs twice belongs
in the repo — that is the lesson, and this script is it.

Order matches the list, which is the order the original was written in, so the
row offsets in any surviving .progress.json still line up.

  python3 tools/albums_csv.py            # writes 1001-albums-2-tracks.csv
"""
import csv
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
data = json.loads((HERE.parent / "content" / "shelves.json").read_text())
music = next(s for s in data if s["slug"] == "music")
albums = next(l for l in music["lists"] if l["slug"] == "1001-albums")["rows"]

out = HERE.parent / "1001-albums-2-tracks.csv"
n = 0
with out.open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["Year", "Artist", "Track", "Album"])
    for row in albums:
        year, artist, album = row["lead"], row["sec"], row["pri"]
        for track in (row.get("extra") or "").split(" · "):
            track = track.strip()
            if track:
                w.writerow([year, artist, track, album])
                n += 1

print(f"{n} tracks from {len(albums)} albums -> {out.name}")
