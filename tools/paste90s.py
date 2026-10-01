#!/usr/bin/env python3
"""Paste Magazine — "The 100 Greatest Songs of the 1990s" (Paste Staff, 2026).

A canon, not a tally: Paste's staff ranked these, and the list keeps Paste's
order, #1 to #100. Transcribed from the article's three pages; artist credits
as Paste printed them, titles in their released spelling ("Check the Rhime").

Also writes the Spotify import CSV (Year,Artist,Track,Album) next to it, with
the "feat." credits trimmed so the search matches the lead artist.

Run from the repo root:  python3 tools/paste90s.py
"""
import csv
import json
import re
import sys

PATH = "content/shelves.json"
SLUG = "paste-greatest-songs-of-the-90s"
URL = "https://www.pastemagazine.com/music/1990s/the-100-greatest-songs-of-the-1990s"

# rank, artist, title, year
S = [
(1, "Wu-Tang Clan", "C.R.E.A.M.", 1993),
(2, "Tori Amos", "Caught a Lite Sneeze", 1996),
(3, "Silver Jews", "Random Rules", 1998),
(4, "Björk", "Hyperballad", 1997),
(5, "Moodymann", "The Thief That Stole My Sad Days… Ya Blessin' Me", 1999),
(6, "Mariah Carey", "Can't Let Go", 1991),
(7, "Juvenile feat. Mannie Fresh & Lil Wayne", "Back That Azz Up", 1999),
(8, "Hole", "Violet", 1994),
(9, "New Radicals", "You Get What You Give", 1998),
(10, "Aphex Twin", "Fingerbib", 1996),
(11, "Lucinda Williams", "Car Wheels on a Gravel Road", 1998),
(12, "The Notorious B.I.G.", "Everyday Struggle", 1994),
(13, "The KLF feat. Tammy Wynette", "Justified & Ancient", 1991),
(14, "Bonnie \"Prince\" Billy", "I See a Darkness", 1998),
(15, "PJ Harvey", "Man-Size", 1993),
(16, "D'Angelo", "Brown Sugar", 1995),
(17, "Janet Jackson", "If", 1993),
(18, "Nirvana", "Aneurysm", 1992),
(19, "Sade", "No Ordinary Love", 1992),
(20, "Bruce Springsteen", "Streets of Philadelphia", 1993),
(21, "OutKast", "Da Art of Storytellin', Pt. 1", 1998),
(22, "Theo Parrish", "Sweet Sticky", 1998),
(23, "George Michael", "Freedom! '90", 1990),
(24, "Missy Elliott", "The Rain (Supa Dupa Fly)", 1997),
(25, "Wilco", "A Shot in the Arm", 1999),
(26, "Liz Phair", "Fuck and Run", 1993),
(27, "A Tribe Called Quest", "Check the Rhime", 1991),
(28, "Fiona Apple", "Fast As You Can", 1999),
(29, "Pete Rock & C.L. Smooth", "They Reminisce Over You (T.R.O.Y.)", 1992),
(30, "Britney Spears", "…Baby One More Time", 1998),
(31, "The Breeders", "Cannonball", 1993),
(32, "Daft Punk", "Around the World", 1997),
(33, "Bikini Kill", "Rebel Girl", 1992),
(34, "Bone Thugs-N-Harmony", "Tha Crossroads", 1996),
(35, "Erykah Badu", "Other Side of the Game", 1997),
(36, "Pavement", "Range Life", 1994),
(37, "Lauryn Hill", "Ex-Factor", 1998),
(38, "Third Eye Blind", "Semi-Charmed Life", 1997),
(39, "Portishead", "Sour Times", 1994),
(40, "Nas", "Life's a Bitch", 1994),
(41, "Madonna", "Ray of Light", 1998),
(42, "Geto Boys", "Mind Playing Tricks on Me", 1991),
(43, "Radiohead", "Planet Telex", 1995),
(44, "Brandy & Monica", "The Boy Is Mine", 1998),
(45, "Massive Attack", "Teardrop", 1998),
(46, "Mobb Deep", "Shook Ones, Pt. II", 1995),
(47, "Celine Dion", "It's All Coming Back to Me Now", 1996),
(48, "Guided by Voices", "Game of Pricks", 1995),
(49, "DMX", "Ruff Ryders' Anthem", 1998),
(50, "Gillian Welch", "Orphan Girl", 1996),
(51, "TLC", "No Scrubs", 1999),
(52, "DJ Shadow", "Midnight in a Perfect World", 1996),
(53, "Elliott Smith", "Christian Brothers", 1995),
(54, "The Roots feat. Erykah Badu & Eve", "You Got Me", 1999),
(55, "Public Enemy", "Welcome to the Terrordome", 1990),
(56, "Jamiroquai", "Canned Heat", 1999),
(57, "Tom Waits", "Come On Up to the House", 1999),
(58, "Richard Jacques", "Can You Feel the Sunshine?", 1998),
(59, "Yo La Tengo", "Autumn Sweater", 1997),
(60, "Aaliyah", "Are You That Somebody?", 1998),
(61, "Weezer", "Only in Dreams", 1994),
(62, "JAY-Z", "Dead Presidents II", 1996),
(63, "Mazzy Star", "Fade Into You", 1993),
(64, "Jeff Buckley", "Lover, You Should've Come Over", 1994),
(65, "Built to Spill", "Carry the Zero", 1999),
(66, "De La Soul", "Stakes Is High", 1996),
(67, "Kristin Hersh", "Your Ghost", 1994),
(68, "Prince", "Gold", 1995),
(69, "Pulp", "Common People", 1995),
(70, "Digable Planets", "Rebirth of Slick (Cool Like Dat)", 1992),
(71, "Cat Power", "Metal Heart", 1998),
(72, "MF DOOM feat. Pebbles the Invisible Girl", "Doomsday", 1999),
(73, "The Sundays", "Here's Where the Story Ends", 1990),
(74, "Destiny's Child", "Say My Name", 1999),
(75, "Sinéad O'Connor", "Nothing Compares 2 U", 1990),
(76, "Belle and Sebastian", "Get Me Away from Here, I'm Dying", 1996),
(77, "The Pharcyde", "Otha Fish", 1992),
(78, "Daniel Johnston", "Some Things Last a Long Time", 1990),
(79, "Shania Twain", "Man! I Feel Like a Woman!", 1997),
(80, "Ice Cube", "It Was a Good Day", 1992),
(81, "Beck", "Lord Only Knows", 1996),
(82, "Ini Kamoze", "Here Comes the Hotstepper", 1994),
(83, "Natalie Imbruglia", "Torn", 1997),
(84, "Gang Starr", "Mass Appeal", 1993),
(85, "R.E.M.", "Nightswimming", 1992),
(86, "Camp Lo", "Luchini AKA This Is It", 1997),
(87, "Neutral Milk Hotel", "Gardenhead / Leave Me Alone", 1996),
(88, "Three 6 Mafia", "Tear Da Club Up '97", 1997),
(89, "Le Tigre", "Deceptacon", 1999),
(90, "Cocteau Twins", "Heaven or Las Vegas", 1990),
(91, "The Smashing Pumpkins", "1979", 1995),
(92, "UGK feat. Mr. 3-2 & Ronnie Spencer", "One Day", 1996),
(93, "The Chicks", "Wide Open Spaces", 1998),
(94, "Stereolab", "The Flower Called Nowhere", 1997),
(95, "Warren G feat. Nate Dogg", "Regulate", 1994),
(96, "The Cranberries", "Linger", 1993),
(97, "Depeche Mode", "Enjoy the Silence", 1990),
(98, "Mary J. Blige", "Real Love", 1992),
(99, "Modest Mouse", "Cowboy Dan", 1997),
(100, "Raekwon", "Incarcerated Scarfaces", 1995),
]
assert [r for r, *_ in S] == list(range(1, 101))


def lead(artist):
    """Search artist for Spotify: drop the featured credits."""
    return re.split(r"\s+feat\.\s+", artist)[0]


src = {"label": "Paste", "url": URL}
rows = [{
    "key": f"paste90|{r}",
    "lead": f"#{r}",
    "sec": a,
    "pri": t,
    "extra": str(y),
    "yt": f"{t} {lead(a)}",
    "ytWord": "Listen",
    "src": src,
} for r, a, t, y in S]

LIST = {
    "slug": SLUG,
    "title": "The 100 Greatest Songs of the 1990s",
    "kind": "Canon",
    "verb": "heard",
    "noTick": True,
    "desc": ("Paste Magazine&rsquo;s staff ranking, in Paste&rsquo;s order. Wu-Tang at #1, Tori Amos at #2, "
             "and a decade that put Britney, Aphex Twin and Shania Twain on the same list."),
    "cols": ["Rank", "Artist", "Song", "Listen · year · source"],
    "srcLabel": "Ranked in",
    "sources": [{"url": URL, "label": "Paste Magazine",
                 "q": "The 100 Greatest Songs of the 1990s",
                 "meta": "2026 · Paste Staff · 100 songs"}],
    "note": ("A canon, not a tally: Paste&rsquo;s writers made this ranking, and it stays in their order "
             "rather than being re-sorted by anything here. Artist credits follow Paste, featured guests "
             "included, and the year is the one Paste gives for each song. The write-ups "
             "that go with each entry are Paste&rsquo;s and live on their pages &mdash; the source link "
             "goes there. What makes it worth reading is the spread: Wu-Tang&rsquo;s <em>C.R.E.A.M.</em> on "
             "top, Detroit house from Moodymann and Theo Parrish in the top 25, a <em>Sonic R</em> soundtrack "
             "cut at #58, and the decade&rsquo;s biggest pop &mdash; Celine Dion, Britney, Third Eye Blind "
             "&mdash; ranked without apology among the indie canon."),
    "rows": rows,
}

if __name__ == "__main__":
    shelves = json.load(open(PATH))
    music = [s for s in shelves if s["slug"] == "music"][0]
    old = [l for l in music["lists"] if l["slug"] == SLUG]
    if old and "action" in old[0]:
        LIST["action"] = old[0]["action"]          # keep the playlist link on re-runs
    music["lists"] = [l for l in music["lists"] if l["slug"] != SLUG] + [LIST]
    open(PATH, "w").write(json.dumps(shelves, ensure_ascii=False, indent=1))

    out = sys.argv[1] if len(sys.argv) > 1 else "paste-90s.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["Year", "Artist", "Track", "Album"])
        for r, a, t, y in S:
            w.writerow([y, lead(a).replace("Pete Rock & C.L. Smooth", "Pete Rock"), t, ""])
    print(len(rows), "songs →", PATH, "and", out)
