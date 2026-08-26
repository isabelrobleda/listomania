"""r/movies — "What is your top 10 of the 2010s?"

Structurally different from the other tallies: nearly every commenter posted a
ranked list of ten, so a mention here means "made someone's top ten of the
decade" rather than "someone mentioned it". Counted by distinct redditor.

The asker's own ten is excluded from the count, as in the documentaries list —
otherwise the question rigs its own answer.
"""
import json
from collections import defaultdict

THREAD = {
 "q": "What is your top 10 of the 2010s?",
 "site": "Reddit · r/movies", "year": 2022,
 "meta": "ranked top-ten lists",
 "url": "https://www.reddit.com/r/movies/comments/yqknq9/what_is_your_top_10_of_the_2010s/",
}

BALLOTS = {
"NoDisintegrationz": ["If Beale Street Could Talk","Parasite","Hunt for the Wilderpeople",
  "We Need to Talk About Kevin","Prisoners","What We Do in the Shadows","Whiplash",
  "The Florida Project","Moonlight","BlacKkKlansman"],
"Kelvin_Inman": ["The Cabin in the Woods","Dredd","Fast Five","Interstellar","It Follows",
  "John Wick","Mad Max: Fury Road","Predators","Resident Evil: Afterlife","Train to Busan"],
"LEXX911": ["Arrival","Blade Runner 2049","Sicario","Interstellar","Inception","Mad Max: Fury Road",
  "Dawn of the Planet of the Apes","Ex Machina","Parasite","The Handmaiden","Annihilation","Logan",
  "Looper","The Martian","Edge of Tomorrow","X-Men: Days of Future Past"],
"oh_orpheus": ["Only Lovers Left Alive","Beyond the Hills","Meek's Cutoff","Like Someone in Love",
  "Our Little Sister","Inherent Vice","Roma","Elena","Black Mother","American Honey"],
"onetwothreewhore": ["Whiplash","Inherent Vice","Uncut Gems","Get Out","The Florida Project",
  "Annihilation","Inside Llewyn Davis","The Lighthouse","Arrival","Once Upon a Time in Hollywood"],
"McCabbe": ["Mad Max: Fury Road","Leviathan","Portrait of a Lady on Fire","The Grand Budapest Hotel",
  "Parasite","Manchester by the Sea","Raw","Monos","Birdman","The Witch"],
"Spidey_Almighty": ["The Lego Movie","Whiplash","The Avengers","The Wolf of Wall Street",
  "Django Unchained","Drive","La La Land","Life of Pi","Birdman","Room"],
"Twigling": ["Klaus","La La Land","Mission: Impossible – Ghost Protocol",
  "Mission: Impossible – Rogue Nation","Edge of Tomorrow","Paddington","Paddington 2","Deadpool",
  "Black Swan","Guardians of the Galaxy"],
"HalloweenSongScholar": ["The Red Turtle","Mad Max: Fury Road","Annihilation","Doctor Sleep",
  "Hereditary","The Hateful Eight","Arrival","I Saw the Devil","Inception","Evil Dead"],
"OldVariation7440": ["Once Upon a Time in Hollywood","The Social Network","Hereditary","The Master",
  "Certified Copy","Birdman","Inception","Moonrise Kingdom","The Comedy","Good Time"],
"HEHEHO2022": ["The Master","Arrival","Our Little Sister","Phantom Thread","Inherent Vice",
  "I'm Thinking of Ending Things","The Farewell","The Grand Budapest Hotel","Suspiria","Under the Skin"],
"mhowes666": ["Parasite","A Taxi Driver","Only Lovers Left Alive","The Handmaiden","Dirty Computer",
  "Blade Runner 2049","Super Deluxe","Blindspotting","The Farewell","Tomboy"],
"noodles240": ["Carnage","Contagion","Moneyball","The Grand Budapest Hotel","The Big Short",
  "Steve Jobs","Everybody Wants Some!!","Ingrid Goes West","Spider-Man: Into the Spider-Verse",
  "Little Women"],
"Old-Inevitable3069": ["Phantom Thread","The Lighthouse","The Grand Budapest Hotel","Good Time",
  "The Hateful Eight","Nightcrawler","Birdman","Whiplash","The Social Network","Inside Llewyn Davis"],
"Puzzleheaded-Mud7288": ["Good Time","The Place Beyond the Pines","Swiss Army Man","Nightcrawler",
  "Uncut Gems","Django Unchained","The Nice Guys","The Wolf of Wall Street","The Founder",
  "You Were Never Really Here"],
"loverofonion": ["Once Upon a Time in Hollywood","Blade Runner 2049","In Order of Disappearance",
  "The Handmaiden","Three Billboards Outside Ebbing, Missouri","The Girl with the Dragon Tattoo",
  "Hidden Figures","Identity Thief","Jumanji: Welcome to the Jungle","Doctor Sleep"],
"Foxtrot434": ["It's Such a Beautiful Day","A Separation","Manchester by the Sea","Boyhood",
  "Incendies","Laurence Anyways","Eighth Grade","The Hunt","The Grand Budapest Hotel",
  "The Tale of the Princess Kaguya"],
"ClassyMidget": ["The Social Network","Waves","The Master","Personal Shopper","Sicario",
  "The Favourite","Green Room","Mad Max: Fury Road","Dunkirk","Ex Machina"],
"Steelburgh": ["Arrival","Interstellar","Jojo Rabbit","Kubo and the Two Strings","Hereditary",
  "Inside Out","Gravity","Get Out","Swiss Army Man","Movie 43"],
"BlueSnaggleTooth359": ["Wonder Woman","The Tree of Life","Blade Runner 2049","La La Land",
  "Little Women","Black Swan","War for the Planet of the Apes","Knives Out","Interstellar",
  "The Witch","Once Upon a Time in Hollywood","First Man","Gravity","Hugo","Her","Ex Machina",
  "Arrival","The Artist","Christopher Robin","BlacKkKlansman","Edge of Tomorrow","True Grit",
  "Tolkien","Ophelia","The Aeronauts","Bumblebee","Hidden Figures","Guardians of the Galaxy",
  "Ant-Man"],
"Mrmoviesguy": ["Arrival","Mission: Impossible – Ghost Protocol","Inception","Edge of Tomorrow",
  "Megamind","Knives Out","Hidden Figures","Guardians of the Galaxy Vol. 2","Paddington",
  "Olympus Has Fallen"],
"Jerrymoviefan3": ["Parasite","Poetry","Ida","Room","Her","12 Years a Slave","Spotlight",
  "Ex Machina","Zero Dark Thirty","The Handmaiden"],
"Top_Industry_2641": ["The Way Way Back"],
"Far-Pomegranate-2139": ["Smurfs: The Lost Village","Train to Busan"],
}

YEARS = {
"12 Years a Slave":2013,"A Separation":2011,"A Taxi Driver":2017,"American Honey":2016,
"Annihilation":2018,"Ant-Man":2015,"Arrival":2016,"Beyond the Hills":2012,"Birdman":2014,
"BlacKkKlansman":2018,"Black Mother":2018,"Black Swan":2010,"Blade Runner 2049":2017,
"Blindspotting":2018,"Boyhood":2014,"Bumblebee":2018,"Carnage":2011,"Certified Copy":2010,
"Christopher Robin":2018,"Contagion":2011,"Dawn of the Planet of the Apes":2014,"Deadpool":2016,
"Dirty Computer":2018,"Django Unchained":2012,"Doctor Sleep":2019,"Dredd":2012,"Drive":2011,
"Dunkirk":2017,"Edge of Tomorrow":2014,"Eighth Grade":2018,"Elena":2011,"Everybody Wants Some!!":2016,
"Evil Dead":2013,"Ex Machina":2014,"Fast Five":2011,"First Man":2018,"Get Out":2017,"Good Time":2017,
"Gravity":2013,"Green Room":2015,"Guardians of the Galaxy":2014,"Guardians of the Galaxy Vol. 2":2017,
"Her":2013,"Hereditary":2018,"Hidden Figures":2016,"Hugo":2011,"Hunt for the Wilderpeople":2016,
"I Saw the Devil":2010,"I'm Thinking of Ending Things":2020,"Ida":2013,"Identity Thief":2013,
"If Beale Street Could Talk":2018,"In Order of Disappearance":2014,"Incendies":2010,"Inception":2010,
"Ingrid Goes West":2017,"Inherent Vice":2014,"Inside Llewyn Davis":2013,"Inside Out":2015,
"Interstellar":2014,"It Follows":2014,"It's Such a Beautiful Day":2012,"Jojo Rabbit":2019,
"John Wick":2014,"Jumanji: Welcome to the Jungle":2017,"Klaus":2019,"Knives Out":2019,
"Kubo and the Two Strings":2016,"La La Land":2016,"Laurence Anyways":2012,"Leviathan":2014,
"Life of Pi":2012,"Like Someone in Love":2012,"Little Women":2019,"Logan":2017,"Looper":2012,
"Mad Max: Fury Road":2015,"Manchester by the Sea":2016,"Meek's Cutoff":2010,"Megamind":2010,
"Mission: Impossible – Ghost Protocol":2011,"Mission: Impossible – Rogue Nation":2015,"Monos":2019,
"Moonlight":2016,"Moonrise Kingdom":2012,"Moneyball":2011,"Movie 43":2013,"Nightcrawler":2014,
"Olympus Has Fallen":2013,"Once Upon a Time in Hollywood":2019,"Only Lovers Left Alive":2013,
"Ophelia":2018,"Our Little Sister":2015,"Paddington":2014,"Paddington 2":2017,"Parasite":2019,
"Personal Shopper":2016,"Phantom Thread":2017,"Poetry":2010,"Portrait of a Lady on Fire":2019,
"Predators":2010,"Prisoners":2013,"Raw":2016,"Resident Evil: Afterlife":2010,"Roma":2018,
"Room":2015,"Sicario":2015,"Smurfs: The Lost Village":2017,"Spider-Man: Into the Spider-Verse":2018,
"Spotlight":2015,"Steve Jobs":2015,"Super Deluxe":2019,"Suspiria":2018,"Swiss Army Man":2016,
"The Aeronauts":2019,"The Artist":2011,"The Avengers":2012,"The Big Short":2015,
"The Cabin in the Woods":2011,"The Comedy":2012,"The Farewell":2019,"The Favourite":2018,
"The Florida Project":2017,"The Founder":2016,"The Girl with the Dragon Tattoo":2011,
"The Grand Budapest Hotel":2014,"The Handmaiden":2016,"The Hateful Eight":2015,"The Hunt":2012,
"The Lego Movie":2014,"The Lighthouse":2019,"The Martian":2015,"The Master":2012,
"The Nice Guys":2016,"The Place Beyond the Pines":2012,"The Red Turtle":2016,
"The Social Network":2010,"The Tale of the Princess Kaguya":2013,"The Tree of Life":2011,
"The Way Way Back":2013,"The Witch":2015,"The Wolf of Wall Street":2013,
"Three Billboards Outside Ebbing, Missouri":2017,"Tolkien":2019,"Tomboy":2011,
"Train to Busan":2016,"True Grit":2010,"Uncut Gems":2019,"Under the Skin":2013,
"War for the Planet of the Apes":2017,"Waves":2019,"We Need to Talk About Kevin":2011,
"What We Do in the Shadows":2014,"Whiplash":2014,"Wonder Woman":2017,
"X-Men: Days of Future Past":2014,"You Were Never Really Here":2017,"Zero Dark Thirty":2012,
}

counts = defaultdict(set)
for user, films in BALLOTS.items():
    for f in films:
        counts[f].add(user)

rows = sorted(
    ({"title": f, "year": YEARS.get(f, ""), "mentions": len(u)} for f, u in counts.items()),
    key=lambda r: (-r["mentions"], r["title"].lower()))

json.dump({"thread": THREAD, "rows": rows}, open("films2010s.json", "w"),
          ensure_ascii=False, separators=(",", ":"))
missing = [r["title"] for r in rows if not r["year"]]
print(len(rows), "films from", len(BALLOTS), "ballots;",
      sum(r["mentions"] for r in rows), "placements")
print("missing years:", missing or "none")
for r in rows[:14]:
    print(f'  {r["mentions"]}x  {r["title"]} ({r["year"]})')
