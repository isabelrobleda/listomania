#!/usr/bin/env python3
"""Most beautiful city you've ever visited — r/AskReddit, 1wyx5a0.

Same rule as cities.py (r/BeautifulTravelPlaces): counted by distinct redditor
who *names* a city as beautiful, top-level or in a reply. "Agreed", "Came
here to say this", "It's a winter wonderland" without a name add nothing, and a
city named only to knock it ("I would 100% NOT consider [Cologne] beautiful",
"You've clearly never been to Hamilton or Palmy") is not a vote. Upvotes on
the naming comments break ties.

Left out because they aren't a city: the Cotswolds, the Isle of Skye, Lake
Bled, and Elfin Cove (its own commenter says "not a city"). Villages and towns
that people gave as their answer stay — Lauterbrunnen, Gimmelwald, Hallstatt,
Valldemossa — as they did in cities.py. Joke answers stay too (Gary, Indiana;
Scranton; Reno): a tally records what was said.

The whole thread: 174 of 178 comments, nothing behind "load more".
Data transcribed by hand from the thread's old.reddit .json, attached.

Run from the repo root:  python3 tools/cities_askreddit.py
"""
import json
from urllib.parse import quote

PATH = "content/shelves.json"
SLUG = "most-beautiful-city-visited"
URL = "https://www.reddit.com/r/AskReddit/comments/1wyx5a0/what_was_the_most_beautiful_city_youve_ever/"

# redditor -> (score of the naming comment, cities)
V = {
"Kattenaars": (39, ["Bergen"]),
"Curlydeadhead": (152, ["Quebec City"]),
"senseigorilla": (23, ["Vancouver", "Quebec City", "Victoria", "Doha"]),
"Foreign-Dependent-12": (3, ["Kotor", "Quebec City", "Vancouver"]),
"the-mongoose-": (292, ["Vancouver"]),
"BritishShark": (10, ["Vancouver", "London"]),
"yoloswagger42069": (5, ["Vancouver"]),
"FC3MugenSi": (43, ["Amsterdam"]),
"djorion87": (144, ["San Francisco"]),
"nombresespeciales": (30, ["San Francisco"]),
"MrOtero": (104, ["Seville"]),
"MisterKM": (72, ["Florence"]),
"mojomarc": (24, ["Florence", "Rome", "Istanbul"]),
"scuzzmonster1": (19, ["Cádiz"]),
"augenwiehimmel": (103, ["Vienna"]),
"cozy_goblin46": (117, ["Kyoto"]),
"Thebigpicture42": (45, ["Salzburg"]),
"TheDamned1333": (43, ["Venice"]),
"absolutevalue-worth": (15, ["Mexico City"]),
"velvetlane1": (37, ["Prague"]),
"GeographyGeek01": (45, ["Vienna", "Edinburgh"]),
"Chris149ny": (2, ["Edinburgh"]),
"Mentalfloss1": (112, ["Victoria"]),
"GaIaxian": (26, ["Annecy"]),
"Ok-Wonder-9788": (24, ["Prague", "Vancouver"]),
"ApartInfluence4429": (61, ["Ljubljana", "Budapest"]),
"infernalmachine000": (50, ["Amsterdam", "Vancouver"]),
"yellowsubmarinr": (57, ["Bruges", "Ghent"]),
"Due-Presentation4344": (2, ["Ghent"]),
"throw223344555": (10, ["Rio de Janeiro"]),
"Marieh_": (9, ["Lauterbrunnen"]),
"Shodoma": (63, ["Rome"]),
"iliketinafey": (8, ["Carmel-by-the-Sea"]),
"karankk11": (9, ["Budapest"]),
"Puzzleheaded-Twist14": (12, ["San Sebastián"]),
"Artistic_Nothing2382": (20, ["Vienna", "Rome"]),
"sunbearimon": (26, ["Tallinn"]),
"Opposite2": (14, ["Porto"]),
"No-Data-3048": (1, ["Porto"]),
"Owl_Nice": (6, ["Ålesund"]),
"hyp_thetical": (5, ["Amsterdam"]),
"QrtJester": (13, ["Paris"]),
"Sfswine": (9, ["Davos"]),
"foofarraw": (33, ["Gary"]),
"hoggytime613": (7, ["Scranton"]),
"fqh": (1, ["Reno"]),
"leebonnie2000": (12, ["Prague"]),
"smoothbrainkoala": (4, ["Prague", "Kraków"]),
"Unfair-Community-321": (4, ["London"]),
"FancyLittleTurnip": (10, ["Venice"]),
"Dr_Who314": (6, ["Rome", "Vienna"]),
"mp6521": (6, ["Copenhagen"]),
"_DecoyOctopus_": (7, ["Queenstown"]),
"dafsuhammer": (3, ["Te Anau"]),
"Winter-Reason-5257": (3, ["Taos"]),
"slow__punch": (3, ["Cape Town"]),
"allieballie1122": (8, ["Barcelona"]),
"wutangassociates": (4, ["Chicago"]),
"Devotee97": (5, ["Southampton"]),
"NateFisher22": (3, ["Heidelberg"]),
"digbug0": (3, ["Amsterdam"]),
"Key-Goal-2907": (3, ["Istanbul"]),
"GoRangers5": (5, ["London"]),
"Careless_Aroma_227": (2, ["L'Étang-la-Ville"]),
"couchpotato287": (2, ["Ghent", "Stellenbosch"]),
"EdTeeZ": (2, ["Bonifacio", "Piran"]),
"BusinessHammocks": (2, ["Ponta Delgada"]),
"deguzman6": (2, ["Nice"]),
"andrew2018022": (2, ["Lugano"]),
"coeu5": (2, ["Bern"]),
"lospiesdejavi": (2, ["Annemasse"]),
"SlothyYapper": (2, ["Lucerne"]),
"westcoastwomann": (2, ["Ubud"]),
"Citizen_of_H": (2, ["Bamberg"]),
"Real-Car1184": (2, ["Ghent", "Cape Town"]),
"Motorsensational1000": (2, ["Rome", "Edinburgh"]),
"Early-Ad1123": (3, ["Lauterbrunnen"]),
"Ok-Vermicelli1117": (4, ["Vienna"]),
"savage_italiano": (3, ["Málaga"]),
"gavja87": (4, ["Sydney", "Prague"]),
"FredMcGriff493": (2, ["Fresno"]),
"WaZeedeGij": (2, ["Florence"]),
"BashfulSnail": (2, ["Gimmelwald"]),
"AIG_the_lion": (2, ["Taipei"]),
"Bruker6": (3, ["Tokyo"]),
"Omelaros": (1, ["Salalah", "Grindelwald"]),
"ProffesorBongsworth": (1, ["Valldemossa"]),
"mistermuk": (1, ["Barcelona", "Edinburgh"]),
"Interesting-Ad-1291": (1, ["Bruges"]),
"Seefutjay": (1, ["Prague", "Vienna"]),
"Next-Clothes-3451": (1, ["Bergen"]),
"BloodyMuggle": (1, ["Vienna"]),
"sadscience": (1, ["Florence"]),
"sfm7019": (1, ["Kaohsiung"]),
"itsfairadvantage": (1, ["Ghent"]),
"Ninja-Panda70": (1, ["Vienna", "Edinburgh", "Salzburg"]),
"Purple_Band_8681": (1, ["Grindelwald", "Rio de Janeiro"]),
"Paris-hotguy": (1, ["Istanbul"]),
"ElectronicArea7693": (1, ["Budapest"]),
"Glaucoma_suspect": (1, ["Edinburgh"]),
"blondedAZ": (1, ["Kyoto", "Oslo", "Istanbul"]),
"Typical_Fruit_331": (1, ["Avignon"]),
"PandasOnGiraffes": (1, ["Vancouver", "Madrid", "Rome", "Venice", "Palma", "London", "Quebec City", "Edinburgh"]),
"BetaRhoVelo": (1, ["Boulder"]),
"Rayne_K": (1, ["Prague", "Quebec City"]),
"ufknfet": (1, ["Copenhagen"]),
"Sweaty-Helicopter-75": (1, ["Melbourne"]),
"MishaIvanova": (1, ["Paris"]),
"No_Judgment3450": (1, ["San Sebastián"]),
"ennzedd": (1, ["Queenstown"]),
"Ornery-Fishing-5483": (1, ["Mérida"]),
"hilarybe": (1, ["Queenstown"]),
"hotdog_dachshund": (1, ["Cape Town"]),
"_etcetera_etcetera": (1, ["Sopron"]),
"verilyI": (1, ["Venice"]),
"MealAsleep": (1, ["Prague"]),
"standing_staring": (1, ["Florence"]),
"BeamoBeamer77": (0, ["Bangalore"]),
"Late_Quail7194": (0, ["Hallstatt"]),
"Forsaken_Plant_4042": (0, ["Los Angeles"]),
"_Raro": (-1, ["Cologne"]),
"wipeitonthedog": (0, ["Tbilisi"]),
"Naeem759": (-5, ["Doha"]),
"FancyFriendship1191": (-18, ["Dubai"]),
"algggag": (-6, ["Houston"]),
}

# city -> (country, map query)
C = {
"Bergen": "Norway", "Quebec City": "Canada", "Vancouver": "Canada", "Victoria": "Canada",
"Doha": "Qatar", "Kotor": "Montenegro", "London": "United Kingdom", "Amsterdam": "Netherlands",
"San Francisco": "United States", "Seville": "Spain", "Florence": "Italy", "Rome": "Italy",
"Istanbul": "Türkiye", "Cádiz": "Spain", "Vienna": "Austria", "Kyoto": "Japan", "Salzburg": "Austria",
"Venice": "Italy", "Mexico City": "Mexico", "Prague": "Czechia", "Edinburgh": "United Kingdom",
"Annecy": "France", "Ljubljana": "Slovenia", "Budapest": "Hungary", "Bruges": "Belgium",
"Ghent": "Belgium", "Rio de Janeiro": "Brazil", "Lauterbrunnen": "Switzerland",
"Carmel-by-the-Sea": "United States", "San Sebastián": "Spain", "Tallinn": "Estonia",
"Porto": "Portugal", "Ålesund": "Norway", "Paris": "France", "Davos": "Switzerland",
"Gary": "United States", "Scranton": "United States", "Reno": "United States",
"Kraków": "Poland", "Copenhagen": "Denmark", "Queenstown": "New Zealand", "Te Anau": "New Zealand",
"Taos": "United States", "Cape Town": "South Africa", "Barcelona": "Spain", "Chicago": "United States",
"Southampton": "United Kingdom", "Heidelberg": "Germany", "L'Étang-la-Ville": "France",
"Stellenbosch": "South Africa", "Bonifacio": "France", "Piran": "Slovenia",
"Ponta Delgada": "Portugal", "Nice": "France", "Lugano": "Switzerland", "Bern": "Switzerland",
"Annemasse": "France", "Lucerne": "Switzerland", "Ubud": "Indonesia", "Bamberg": "Germany",
"Málaga": "Spain", "Sydney": "Australia", "Fresno": "United States", "Gimmelwald": "Switzerland",
"Taipei": "Taiwan", "Tokyo": "Japan", "Salalah": "Oman", "Grindelwald": "Switzerland",
"Valldemossa": "Spain", "Kaohsiung": "Taiwan", "Oslo": "Norway", "Avignon": "France",
"Madrid": "Spain", "Palma": "Spain", "Boulder": "United States", "Melbourne": "Australia",
"Mérida": "Mexico", "Sopron": "Hungary", "Bangalore": "India", "Hallstatt": "Austria",
"Los Angeles": "United States", "Cologne": "Germany", "Tbilisi": "Georgia", "Dubai": "United Arab Emirates",
"Houston": "United States",
}
STATE = {"Gary": "Gary, Indiana", "Scranton": "Scranton, Pennsylvania", "Reno": "Reno, Nevada",
         "Taos": "Taos, New Mexico", "Boulder": "Boulder, Colorado", "Fresno": "Fresno, California",
         "Victoria": "Victoria, British Columbia"}

people, pts = {}, {}
for who, (score, cities) in V.items():
    for c in dict.fromkeys(cities):
        assert c in C, c
        people.setdefault(c, set()).add(who)
        pts[c] = pts.get(c, 0) + score

order = sorted(people, key=lambda c: (-len(people[c]), -pts[c], c))
src = {"label": "r/AskReddit", "url": URL}
rows = []
for c in order:
    q = STATE.get(c, f"{c} {C[c]}")
    rows.append({
        "key": f"cityv|{c}",
        "lead": f"{len(people[c])}×",
        "sec": C[c],
        "pri": STATE.get(c, c),
        "links": [{"url": "https://www.google.com/maps/search/?api=1&query=" + quote(q), "label": "Map ↗"}],
        "src": src,
    })

n_red = len(V)
LIST = {
    "slug": SLUG,
    "title": "Most Beautiful City You've Ever Visited",
    "kind": "Tally",
    "verb": "been to",
    "desc": (f"{len(rows)} cities from {n_red} people on r/AskReddit. Vancouver, Vienna and Prague tie on eight; "
             "Vancouver takes it on upvotes. Rio, top of the travel subreddit&rsquo;s version, gets two."),
    "cols": ["Said by", "Country", "City"],
    "sources": [{"url": URL, "label": "Reddit · r/AskReddit",
                 "q": "What was the most beautiful city you've ever visited?",
                 "meta": "2026 · 86 points · 178 comments"}],
    "note": ("Counted the same way as <em>Most Beautiful City in the World</em>: by distinct redditor who "
             "<em>names</em> a city, top-level or in a reply, with upvotes on the naming comments breaking ties. "
             "Agreement without a name (&ldquo;Came here to say this&rdquo;) adds nothing, and a city named only "
             "to knock it &mdash; &ldquo;I would 100% NOT consider it beautiful&rdquo; of Cologne, &ldquo;you&rsquo;ve "
             "clearly never been to Hamilton&rdquo; &mdash; isn&rsquo;t a vote. Answers that aren&rsquo;t a city "
             "(the Cotswolds, the Isle of Skye, Lake Bled) are left out; villages people gave as their answer stay, "
             "and so do the jokes: Gary, Indiana, followed in the replies by Scranton and Reno. The whole thread, "
             "174 of 178 comments. <b>Set it next to the other list.</b> Asked for the most "
             "beautiful city <em>in the world</em>, a travel subreddit put Rio and Venice first and Paris third. "
             "Asked for the most beautiful one <em>you&rsquo;ve visited</em>, AskReddit named Rio and Paris twice "
             "each and went instead for Vancouver, Vienna, Prague and Edinburgh &mdash; the four cities that sit "
             "near the top of both. Ghent is the surprise: five votes here, three there."),
    "srcLabel": "Named in",
    "rows": rows,
}

if __name__ == "__main__":
    shelves = json.load(open(PATH))
    places = [s for s in shelves if s["slug"] == "places"][0]
    places["lists"] = [l for l in places["lists"] if l["slug"] != SLUG] + [LIST]
    open(PATH, "w").write(json.dumps(shelves, ensure_ascii=False, indent=1))
    print(len(rows), "cities from", n_red, "redditors,", sum(len(p) for p in people.values()), "votes")
    for c in order[:20]:
        print(f"  {len(people[c]):>2}×  {c} ({pts[c]})")
