"""r/movies — "What Are Everyone's Top 5 Favorite Movies?"

The loosest of the film tallies, and the most honest about it. No decade, no
"best" — favourites. People said so out loud: "my favourites not my idea of
the best", "infinitely rewatchable, not my Top 5 best Oscar worthy films".

Counting rules, all recorded in the note:
  * One ballot per redditor: their top five. Follow-up comments adding
    "ooh and also…", honourable-mention piles, and second lists posted a year
    later are not counted — one person, one vote per film.
  * Two commenters replied with a top ten instead of a five; those count as
    ballots, since they are still that person naming favourites.
  * One commenter posted a 37-film "short list" and another a 22-film pile of
    honourable mentions. Neither is a top five; both are left out entirely
    rather than counted at full weight.
  * The asker's own five are excluded, as in the other tallies.
  * Trilogies are counted as the person named them. "The Lord of the Rings
    trilogy" and "The Fellowship of the Ring" are different picks and stay
    separate rows.

Expect a long tail of single mentions. That is the finding, not a flaw: ask
strangers for all-time favourites with no constraint and you get 200 films,
almost all named once.
"""
import json
from collections import defaultdict

THREAD = {
 "q": "What Are Everyone's Top 5 Favorite Movies?",
 "site": "Reddit · r/movies", "year": 2023,
 "meta": "top-five lists",
 "url": "https://www.reddit.com/r/movies/comments/1666cfv/what_are_everyones_top_5_favorite_movies/",
}

LOTR = "The Lord of the Rings trilogy"

BALLOTS = {
"Anarchy_Chess_Member": ["Inception","The Prestige","Avengers: Endgame","Se7en",
  "No Country for Old Men"],
"KeenDeadPool": ["12 Angry Men","No Country for Old Men","Pulp Fiction","Taxi Driver","Green Book"],
"KelMHill": ["Fanny and Alexander","Cinema Paradiso","The Shining","Reds","JFK"],
"The_GILF_Next_Door": ["American Beauty","Good Will Hunting","No Country for Old Men",
  "Eternal Sunshine of the Spotless Mind","Catch Me If You Can"],
"Movies_Music_Lover": ["The Father","Inception","The Revenant","Prisoners","Triangle of Sadness"],
"krill482": ["Good Will Hunting","Apocalypse Now","Avengers: Endgame","Catch Me If You Can",
  "The Matrix"],
"Similar_Catch7199": ["Inception","Requiem for a Dream","Airplane!","Scott Pilgrim vs. the World",
  "A Nightmare on Elm Street"],
"Lazy-Photograph-317": ["Cloud Atlas","Doctor Zhivago","Parasite",
  "The Lord of the Rings: The Return of the King","Lawrence of Arabia"],
"faithful_larry": ["Saving Private Ryan","Avengers: Infinity War","Puss in Boots: The Last Wish",
  "Everything Everywhere All at Once","Star Wars original trilogy"],
"jyhzb4s": ["Inception","Spirited Away","Se7en","Goodfellas","Your Name."],
"Zookeeper945": ["Forrest Gump","Green Book","Back to the Future","Inception","Predestination"],
"Muffin_Most": ["The Terminator","Napoleon Dynamite","The Big Lebowski","The Cable Guy",
  "American Psycho"],
"WarcraftFarscape": ["The Lord of the Rings: The Fellowship of the Ring","Back to the Future",
  "Avengers: Infinity War","Wet Hot American Summer","Jurassic Park"],
"kactus": ["Interstellar","Avengers: Endgame","The Revenant","Toy Story 3","Apollo 13"],
"ockybop": ["Tombstone","The Last of the Mohicans","Interstellar","Apocalypse Now",
  "The Muppet Christmas Carol"],
"Particular-Echo347": ["Labyrinth","The Texas Chain Saw Massacre","The Cabin in the Woods",
  "Step Brothers","Interstellar"],
"Anticitizen1_": ["The Nice Guys","Wind River","Interstellar","The Big Lebowski","Roman Holiday"],
"D-Rich-88": ["Top Gun","Avengers: Infinity War","The Departed","Wrath of Man","Goodfellas"],
"jykf58b": ["Chinatown","Casablanca","Margin Call","The Exorcist","Heat"],
"Disconaut90": ["Unforgiven","Raging Bull","The Thing","Farewell My Concubine","Zodiac"],
"Dontnerf": ["Fight Club","Kick-Ass","John Wick","Brawl in Cell Block 99","Anchorman"],
"Sufficient_Bunch5679": ["Training Day","The Dark Knight","The Shining","No Country for Old Men",
  "The Lion King"],
"tebla": ["The Shawshank Redemption","Pulp Fiction","Memento","Moneyball","True Romance"],
"Desperate-Ad-273": ["It's a Wonderful Life","12 Angry Men","Searching for Bobby Fischer",
  "Back to the Future","Groundhog Day"],
# Replied with a ten rather than a five. Still that person naming favourites.
"l5msmwr": ["The Lord of the Rings: The Fellowship of the Ring","The Matrix","Starship Troopers",
  "The Verdict","Forgetting Sarah Marshall","The Godfather Part II","Mad Max: Fury Road",
  "Big Trouble in Little China","12 Angry Men","Lawrence of Arabia"],
"jfstompers": ["Lost in Translation","Jaws","Moulin Rouge!","Jackie Brown","The Big Short"],
"Forsaken_BiscuitGoat": ["Annie Hall","The Godfather","Arizona Dream","Melancholia","Mood Indigo",
  "Stalker"],
"disco-on-acid": ["Alien","Trainspotting","The Thing","Terminator 2: Judgment Day","Pulp Fiction"],
"jyi6ufl": ["Star Wars: The Rise of Skywalker","The Godfather Part III","Ghostbusters (2016)",
  "The Boondock Saints","My Big Fat Greek Wedding"],
"TioRalph": [LOTR,"The Terminator","Scarface","Platoon","The Mummy"],
"BigRedJon": ["There Will Be Blood","Oldboy","The Lighthouse","Rushmore","I ♥ Huckabees"],
"AJray15": ["The Dark Knight trilogy","Star Wars original trilogy","Inception",
  "Indiana Jones original trilogy","The Avengers"],
"belatarrr": ["La La Land","Amélie","12 Angry Men","The Grand Budapest Hotel","WALL·E"],
"Rabbitscooter": ["In the Heat of the Night","Robinson Crusoe on Mars","The Third Man",
  "The War of the Worlds","Star Wars","Red River"],
"Ok-Investigator-5595": ["Children of Men","The Godfather","Downfall","The Thing","Whiplash"],
"FrenchAccented": ["Click","Megamind","Mr. & Mrs. Smith","Spider-Man 3","Superbad"],
"m0ggcg9": ["Snow White and the Seven Dwarfs","Carnival of Souls","Muriel's Wedding","Poltergeist",
  "Home Alone"],
"Pumpkinbinx": ["Eternal Sunshine of the Spotless Mind","Scott Pilgrim vs. the World",
  "The Royal Tenenbaums","The Truman Show","The Butterfly Effect"],
"Sufficient_Trade_58": ["Ferris Bueller's Day Off","Bugsy Malone","Fantastic Mr. Fox",
  "Inglourious Basterds","Good Will Hunting"],
"Key_Discipline890": ["1408","Parasite","Puss in Boots: The Last Wish","Donnie Darko",
  "Falling Down"],
"AdFragrant3331": ["Donnie Darko","The Prestige","The Man from Earth","A Clockwork Orange",
  "The Truman Show"],
"Wooper1302": ["The Dark Knight","Avengers: Endgame","Spider-Man: Across the Spider-Verse",
  "The Wild Robot","Interstellar"],
"Commercial_Usual7023": ["Top Gun: Maverick","The Silence of the Lambs","The Wailing","Constantine"],
"Aggravating-Lead29": ["Indiana Jones original trilogy",LOTR,"Kung Fu Panda trilogy","Godzilla",
  "Pirates of the Caribbean trilogy"],
"TrueLegateDamar": ["RoboCop","The Blues Brothers","V for Vendetta","Aliens","The Truman Show"],
"jyi2pto": ["Lawrence of Arabia","War and Peace","The Revenant",LOTR,
  "Indiana Jones original trilogy"],
"R4kshim": ["The Shining","Jurassic Park","Interstellar","The Dark Knight Rises","The Departed"],
"Scottie2K3": ["Blade Runner","The Addiction","The Passion of Joan of Arc","A Tale of Two Sisters",
  "The Haunting"],
"kwyf4ki": ["Schindler's List",LOTR,"Jurassic Park","The Shawshank Redemption","Oppenheimer"],
"_TLDR_Swinton": ["The Matrix","Jaws","The Thing","The Terminator","Aliens"],
}

YEARS = {
"12 Angry Men":1957,"1408":2007,"A Clockwork Orange":1971,"A Nightmare on Elm Street":1984,
"A Tale of Two Sisters":2003,"Airplane!":1980,"Alien":1979,"Aliens":1986,"American Beauty":1999,
"American Psycho":2000,"Amélie":2001,"Anchorman":2004,"Annie Hall":1977,"Apocalypse Now":1979,
"Apollo 13":1995,"Arizona Dream":1993,"Avengers: Endgame":2019,"Avengers: Infinity War":2018,
"Back to the Future":1985,"Big Trouble in Little China":1986,"Blade Runner":1982,
"Brawl in Cell Block 99":2017,"Bugsy Malone":1976,"Carnival of Souls":1962,"Casablanca":1942,
"Catch Me If You Can":2002,"Children of Men":2006,"Chinatown":1974,"Cinema Paradiso":1988,
"Click":2006,"Cloud Atlas":2012,"Constantine":2005,"Doctor Zhivago":1965,"Donnie Darko":2001,
"Downfall":2004,"Eternal Sunshine of the Spotless Mind":2004,
"Everything Everywhere All at Once":2022,"Falling Down":1993,"Fanny and Alexander":1982,
"Fantastic Mr. Fox":2009,"Farewell My Concubine":1993,"Ferris Bueller's Day Off":1986,
"Fight Club":1999,"Forgetting Sarah Marshall":2008,"Forrest Gump":1994,"Ghostbusters (2016)":2016,
"Godzilla":1954,"Good Will Hunting":1997,"Goodfellas":1990,"Green Book":2018,
"Groundhog Day":1993,"Heat":1995,"Home Alone":1990,"I ♥ Huckabees":2004,
"In the Heat of the Night":1967,"Inception":2010,"Indiana Jones original trilogy":"1981–89",
"Inglourious Basterds":2009,"Interstellar":2014,"It's a Wonderful Life":1946,"JFK":1991,
"Jackie Brown":1997,"Jaws":1975,"John Wick":2014,"Jurassic Park":1993,"Kick-Ass":2010,
"Kung Fu Panda trilogy":"2008–16","La La Land":2016,"Labyrinth":1986,"Lawrence of Arabia":1962,
"Lost in Translation":2003,"Mad Max: Fury Road":2015,"Margin Call":2011,"Megamind":2010,
"Melancholia":2011,"Memento":2000,"Moneyball":2011,"Mood Indigo":2013,"Moulin Rouge!":2001,
"Mr. & Mrs. Smith":2005,"Muriel's Wedding":1994,"My Big Fat Greek Wedding":2002,
"Napoleon Dynamite":2004,"No Country for Old Men":2007,"Oldboy":2003,"Oppenheimer":2023,
"Parasite":2019,"Pirates of the Caribbean trilogy":"2003–07","Platoon":1986,"Poltergeist":1982,
"Predestination":2014,"Prisoners":2013,"Pulp Fiction":1994,"Puss in Boots: The Last Wish":2022,
"Raging Bull":1980,"Red River":1948,"Reds":1981,"Requiem for a Dream":2000,
"Robinson Crusoe on Mars":1964,"RoboCop":1987,"Roman Holiday":1953,"Rushmore":1998,
"Saving Private Ryan":1998,"Scarface":1983,"Schindler's List":1993,
"Scott Pilgrim vs. the World":2010,"Se7en":1995,"Searching for Bobby Fischer":1993,
"Snow White and the Seven Dwarfs":1937,"Spider-Man 3":2007,
"Spider-Man: Across the Spider-Verse":2023,"Spirited Away":2001,"Stalker":1979,
"Star Wars":1977,"Star Wars original trilogy":"1977–83","Star Wars: The Rise of Skywalker":2019,
"Starship Troopers":1997,"Step Brothers":2008,"Superbad":2007,"Taxi Driver":1976,
"Terminator 2: Judgment Day":1991,"The Addiction":1995,"The Avengers":2012,
"The Big Lebowski":1998,"The Big Short":2015,"The Blues Brothers":1980,
"The Boondock Saints":1999,"The Butterfly Effect":2004,"The Cabin in the Woods":2011,
"The Cable Guy":1996,"The Dark Knight":2008,"The Dark Knight Rises":2012,
"The Dark Knight trilogy":"2005–12","The Departed":2006,"The Exorcist":1973,"The Father":2020,
"The Godfather":1972,"The Godfather Part II":1974,"The Godfather Part III":1990,
"The Grand Budapest Hotel":2014,"The Haunting":1963,"The Last of the Mohicans":1992,
"The Lighthouse":2019,"The Lion King":1994,
"The Lord of the Rings: The Fellowship of the Ring":2001,
"The Lord of the Rings: The Return of the King":2003,LOTR:"2001–03","The Man from Earth":2007,
"The Matrix":1999,"The Mummy":1999,"The Muppet Christmas Carol":1992,"The Nice Guys":2016,
"The Passion of Joan of Arc":1928,"The Prestige":2006,"The Revenant":2015,
"The Royal Tenenbaums":2001,"The Shawshank Redemption":1994,"The Shining":1980,
"The Silence of the Lambs":1991,"The Terminator":1984,
"The Texas Chain Saw Massacre":1974,"The Thing":1982,"The Third Man":1949,
"The Truman Show":1998,"The Verdict":1982,"The Wailing":2016,"The War of the Worlds":1953,
"The Wild Robot":2024,"There Will Be Blood":2007,"Tombstone":1993,"Top Gun":1986,
"Top Gun: Maverick":2022,"Toy Story 3":2010,"Trainspotting":1996,"Training Day":2001,
"Triangle of Sadness":2022,"True Romance":1993,"Unforgiven":1992,"V for Vendetta":2005,
"WALL·E":2008,"War and Peace":"1966–67","Wet Hot American Summer":2001,"Whiplash":2014,
"Wind River":2017,"Wrath of Man":2021,"Your Name.":2016,"Zodiac":2007,
}

counts = defaultdict(set)
for user, films in BALLOTS.items():
    for f in films:
        counts[f].add(user)

rows = sorted(
    ({"title": f, "year": YEARS.get(f, ""), "mentions": len(u)} for f, u in counts.items()),
    key=lambda r: (-r["mentions"], r["title"].lower()))

json.dump({"thread": THREAD, "rows": rows}, open("films_alltime.json", "w"),
          ensure_ascii=False, separators=(",", ":"))
missing = [r["title"] for r in rows if r["year"] == ""]
once = sum(1 for r in rows if r["mentions"] == 1)
print(len(rows), "films from", len(BALLOTS), "ballots;",
      sum(r["mentions"] for r in rows), "placements;", once, "named once")
print("missing years:", missing or "none")
for r in rows[:14]:
    print(f'  {r["mentions"]}x  {r["title"]} ({r["year"]})')
