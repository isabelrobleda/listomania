# tools

Scripts that produced the content and the logo. They are not part of the build —
they run by hand and their output is committed.

- `letters.py` — draws the wordmark. `W_OUT`, `W_IN` and `SP` control the outline
  weight, inner weight and letterspacing. Writes `wordmark.svg`.
- `songs.py`, `docs.py`, `recs.py`, `unput.py`, `asked.py` — the tallies. Each holds
  the counted data from one thread and writes a JSON file. Counting is by distinct
  commenter, and each script's docstring records the rule it used.
- `spotify_import.py` — builds a Spotify playlist from a CSV of tracks. Needs your
  own Spotify app credentials; see the comments at the top.
