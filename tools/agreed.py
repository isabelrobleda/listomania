"""Recompute the "Agreed Across Crowds" list from the book tallies.

This one is Derived: it isn't a crowd's answer to anything, it's what happens
when you lay the crowds on top of each other. Which means it has to be rebuilt
whenever a book tally is added — otherwise it silently claims to cover lists it
has never seen. Run from the repo root:

    python3 tools/agreed.py

It rewrites the derived list in content/shelves.json in place.
"""
import json
import re
import unicodedata

DERIVED = "agreed-across-crowds"
PATH = "content/shelves.json"


def norm(title):
    """Match titles across lists written by different people on different days:
    fold accents and case, drop a leading article, drop punctuation."""
    t = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"\(.*?\)", " ", t)          # "If This Is a Man (Survival in…)"
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    t = re.sub(r"^(the|a|an)\s+", "", t.strip())
    return re.sub(r"\s+", " ", t).strip()


def author_of(row, lst):
    """The author isn't in the same column in every list."""
    return (row.get("extra") if lst.get("gr") == "extra" else row.get("sec")) or ""


shelves = json.load(open(PATH))
books = [s for s in shelves if s["slug"] == "books"][0]
sources = [l for l in books["lists"] if l["slug"] != DERIVED and l["kind"] == "Tally"]

seen = {}
for lst in sources:
    for row in lst["rows"]:
        k = norm(row["pri"])
        e = seen.setdefault(k, {"title": row["pri"], "author": "", "lists": []})
        if not e["author"]:
            e["author"] = author_of(row, lst)
        if lst["title"] not in e["lists"]:
            e["lists"].append(lst["title"])

overlap = [e for e in seen.values() if len(e["lists"]) > 1]
overlap.sort(key=lambda e: (-len(e["lists"]), e["title"].lower()))

rows = [{
    "key": f"agreed|{e['title']}",
    "lead": f"{len(e['lists'])} lists",
    "sec": e["author"],
    "pri": e["title"],
    "extra": " · ".join(e["lists"]),
} for e in overlap]

derived = [l for l in books["lists"] if l["slug"] == DERIVED][0]
derived["rows"] = rows
derived["desc"] = (
    f"Books that turned up in more than one of the {len(sources)} book tallies. "
    "Different crowds, different questions, same book — the closest thing here to a consensus."
)
json.dump(shelves, open(PATH, "w"), ensure_ascii=False, indent=1)

print(len(rows), "books agreed across", len(sources), "tallies")
for e in overlap[:8]:
    print(f"  {len(e['lists'])}  {e['title']} — {', '.join(e['lists'])}")
