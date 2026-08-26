"""r/AskReddit — "What's a TV series you'll never get tired of recommending?"

First list on a new shelf. Counted by distinct redditor, same rule as the book
and film tallies: naming a show counts, and a reply agreeing with it counts.

One bias worth stating out loud, because it visibly bends this particular
list: replies that are pure catchphrase — "Omar comin'", "Noice", "EAT
GLASS!!!", "Shiiiiiit" — are *not* counted, since a quote isn't a
recommendation. But a show being quotable is itself a kind of devotion, so the
shows whose fans answer in catchphrases (Schitt's Creek, Brooklyn Nine-Nine,
The Wire) come out lower here than the thread actually feels. The alternative —
counting every affectionate joke — would have made the tally meaningless in the
other direction.
"""
import json
from collections import defaultdict

THREAD = {
 "q": "What's a TV series you'll never get tired of recommending to someone?",
 "site": "Reddit · r/AskReddit", "year": 2026,
 "meta": "1.2K points",
 "url": "https://www.reddit.com/r/AskReddit/comments/1s3t8p9/whats_a_tv_series_youll_never_get_tired_of/",
}

B = {
"avocadogs09": ["Dark"], "existentialdetective": ["Dark"], "Revenant_40": ["Dark"],
"Green__Meanie": ["Dark"],
"SpicyTiconderoga": ["Arrested Development"], "FiftyShadesOfGregg": ["Arrested Development"],
"theinspectorst": ["Arrested Development"],
"foolishdrunk211": ["The Wire"], "ifnotnowtisyettocome": ["The Wire"],
"androidmanwren": ["The Wire"],
"tnetennba8587": ["Psych"], "lundbergintexas": ["Psych"], "hurtsdonut_": ["Psych"],
"Howling_Mad_Man": ["The Expanse"], "mabrasm": ["The Expanse"],
"Magerimoje": ["For All Mankind"],
"wattsjmichael": ["What We Do in the Shadows"],
"Think-Firefighter106": ["What We Do in the Shadows"],
"Collect_Underpants": ["What We Do in the Shadows"],
"mamapello": ["Derry Girls"], "interstatebus": ["Derry Girls"],
"BrewSkiNora": ["The Good Place"], "lying_flerkin": ["The Good Place"],
"zokka_son_of_zokka": ["The Good Place"],
"DONETTES1992": ["The Pitt"], "Ok-Storm-5704": ["The Pitt"], "sheriffofnothingtown": ["The Pitt"],
"SpungyDanglin69": ["The Golden Girls"],
"KingKookus": ["Futurama"], "_bugmenot_": ["Futurama"],
"TollyVonTheDruth": ["The Fall of the House of Usher"],
"Big2ndToe": ["The Fall of the House of Usher", "The Haunting of Hill House",
              "The Haunting of Bly Manor"],
"poggers11": ["Midnight Mass"],
"QuicheSmash": ["Parks and Recreation"], "BaconRapper": ["Parks and Recreation"],
"Stand_Additional": ["Parks and Recreation"],
"vorgorgone": ["Fleabag"], "ketchuptheclown": ["Fleabag"],
"No-Present-3855": ["Deadwood"], "orangepeel6": ["Deadwood"], "Bosworth02": ["Deadwood"],
"oldguarddawg": ["Barney Miller"],
"downstairs591": ["True Detective (season 1)"],
"EurOblivion": ["Brooklyn Nine-Nine"], "dinkytoy80": ["Brooklyn Nine-Nine"],
"chiefoblock": ["Veep"],
"StoreHistorical9175": ["Andor"], "DarthTaz_99": ["Andor"],
"TripPsychological403": ["House"],
"fairyprincessdoll": ["Malcolm in the Middle"],
"MDJokerQueen": ["Malcolm in the Middle", "Twin Peaks"],
"stimj": ["Detectorists"],
"Annual-Success-5696": ["Shrinking"], "BucketsOnly29": ["Shrinking"],
"UnfairLynx": ["Ted Lasso"], "Pure_Tuft": ["Ted Lasso"], "idgahoot2": ["Ted Lasso"],
"ApprehensivePanic757": ["Firefly"], "crimson_binome": ["Firefly"],
"dmckidd": ["The Righteous Gemstones"], "Old_Veterinarian3659": ["The Righteous Gemstones"],
"marclove7": ["Mr Inbetween"],
"Kasia1235": ["Doctor Who"],
"kevinlc1971": ["Justified"],
"dsclamato": ["The Last Kingdom"],
"Darius2112": ["The IT Crowd"],
"FireEater101": ["The Sopranos", "Chernobyl"],
"conniewanders": ["Broad City"],
"SpecificStatic": ["Schitt's Creek"],
"RealPVS": ["The West Wing"],
"cparksrun": ["Slow Horses"],
"sharsh1": ["Party Down"],
"DrunkleSam47": ["Stargate SG-1", "Game Changer"],
"DogOk1726": ["Somebody Somewhere"],
}

YEARS = {
"Andor": "2022–25", "Arrested Development": "2003–19", "Barney Miller": "1975–82",
"Broad City": "2014–19", "Brooklyn Nine-Nine": "2013–21", "Chernobyl": "2019",
"Dark": "2017–20", "Deadwood": "2004–06", "Derry Girls": "2018–22",
"Detectorists": "2014–22", "Doctor Who": "1963–", "Firefly": "2002",
"Fleabag": "2016–19", "For All Mankind": "2019–", "Futurama": "1999–",
"Game Changer": "2019–", "House": "2004–12", "Justified": "2010–15",
"Malcolm in the Middle": "2000–06", "Midnight Mass": "2021", "Mr Inbetween": "2018–21",
"Parks and Recreation": "2009–15", "Party Down": "2009–23", "Psych": "2006–14",
"Schitt's Creek": "2015–20", "Shrinking": "2023–", "Slow Horses": "2022–",
"Somebody Somewhere": "2021–24", "Stargate SG-1": "1997–2007",
"Ted Lasso": "2020–", "The Expanse": "2015–22",
"The Fall of the House of Usher": "2023", "The Golden Girls": "1985–92",
"The Good Place": "2016–20", "The Haunting of Bly Manor": "2020",
"The Haunting of Hill House": "2018", "The IT Crowd": "2006–13",
"The Last Kingdom": "2015–22", "The Pitt": "2025–",
"The Righteous Gemstones": "2019–25", "The Sopranos": "1999–2007",
"The West Wing": "1999–2006", "The Wire": "2002–08",
"True Detective (season 1)": "2014", "Twin Peaks": "1990–91", "Veep": "2012–19",
"What We Do in the Shadows": "2019–24",
}

counts = defaultdict(set)
for user, shows in B.items():
    for s in shows:
        counts[s].add(user)

rows = sorted(({"title": t, "years": YEARS.get(t, ""), "mentions": len(u)} for t, u in counts.items()),
              key=lambda r: (-r["mentions"], r["title"].lower()))

json.dump({"thread": THREAD, "rows": rows}, open("tv.json", "w"),
          ensure_ascii=False, separators=(",", ":"))
print(len(rows), "series from", len(B), "redditors;", sum(r["mentions"] for r in rows), "mentions")
print("missing years:", [r["title"] for r in rows if not r["years"]] or "none")
for r in rows[:12]:
    print(f'  {r["mentions"]}x  {r["title"]} ({r["years"]})')
