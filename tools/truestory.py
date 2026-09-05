#!/usr/bin/env python3
"""
"What is your favorite movie that is 'based on a true story?'" — r/movies, 6,047
comments. Five sorts of the thread (top, best, new, old, controversial) were
captured at ?depth=1, which strips replies and leaves one clean top-level answer
per person, then merged and de-duplicated by (author, answer).

Ranked by DISTINCT REDDITORS naming the film, the site's default method. Upvotes
are carried along as the tie-break, because on a three-year-old thread the top of
the page has thousands of votes and the bottom has one, and sorting by score
alone would just re-print the first screen.

One editorial rule, and it is the only one: joke answers are dropped. A large
minority of this thread answers "Star Wars", "Idiocracy", "The Matrix", "Shrek 2"
— the running gag being that these too are documentaries. They are funny and they
are not an answer to the question, so they are not in the list. Fargo stays: it
opens with a title card claiming to be a true story and does not mean it, which
makes it the one joke that is actually about the question being asked.
"""

import json, re, collections

FILMS = [
 ("Fargo", "Joel & Ethan Coen, 1996", r"\bfargo\b"),
 ("Cocaine Bear", "Elizabeth Banks, 2023", r"cocaine ?bear|cocain bear|cocaine grizzly"),
 ("Goodfellas", "Martin Scorsese, 1990", r"good ?fellas"),
 ("Catch Me If You Can", "Steven Spielberg, 2002", r"catch me if you can"),
 ("Apollo 13", "Ron Howard, 1995", r"apollo 13"),
 ("Hacksaw Ridge", "Mel Gibson, 2016", r"hacksaw ridge"),
 ("Into the Wild", "Sean Penn, 2007", r"into the wild"),
 ("Zodiac", "David Fincher, 2007", r"\bzodiac\b"),
 ("The Big Short", "Adam McKay, 2015", r"big short"),
 ("The Wolf of Wall Street", "Martin Scorsese, 2013", r"wolf (of|on) wall ?street"),
 ("Remember the Titans", "Boaz Yakin, 2000", r"remember the titans"),
 ("Bloodsport", "Newt Arnold, 1988", r"bloodsport"),
 ("October Sky", "Joe Johnston, 1999", r"october sky"),
 ("Cool Runnings", "Jon Turteltaub, 1993", r"cool runnings"),
 ("Fear and Loathing in Las Vegas", "Terry Gilliam, 1998", r"fear and loathing"),
 ("Rudy", "David Anspaugh, 1993", r"\brudy\b"),
 ("Tombstone", "George P. Cosmatos, 1993", r"tombstone"),
 ("Hidden Figures", "Theodore Melfi, 2016", r"hidden figures"),
 ("Spotlight", "Tom McCarthy, 2015", r"\bspotlight\b"),
 ("The Social Network", "David Fincher, 2010", r"social network"),
 ("The Imitation Game", "Morten Tyldum, 2014", r"imitation game"),
 ("BlacKkKlansman", "Spike Lee, 2018", r"blackk?k?lansman"),
 ("Fire in the Sky", "Robert Lieberman, 1993", r"fire (in|on) the sky"),
 ("Lawrence of Arabia", "David Lean, 1962", r"lawrence( of arabia)?\b"),
 ("The Men Who Stare at Goats", "Grant Heslov, 2009", r"stare at goats"),
 ("Argo", "Ben Affleck, 2012", r"\bargo\b"),
 ("The Impossible", "J. A. Bayona, 2012", r"the impossible"),
 ("Ed Wood", "Tim Burton, 1994", r"\bed wood\b"),
 ("Miracle", "Gavin O'Connor, 2004", r"\bmiracle\b"),
 ("Walk the Line", "James Mangold, 2005", r"walk the line"),
 ("Schindler's List", "Steven Spielberg, 1993", r"schindler"),
 ("Moneyball", "Bennett Miller, 2011", r"moneyball"),
 ("City of God", "Fernando Meirelles, 2002", r"city of god"),
 ("The Ghost and the Darkness", "Stephen Hopkins, 1996", r"ghost and the darkness"),
 ("Dog Day Afternoon", "Sidney Lumet, 1975", r"dog day afternoon"),
 ("Black Hawk Down", "Ridley Scott, 2001", r"black ?hawk down"),
 ("Heavenly Creatures", "Peter Jackson, 1994", r"heavenly creatures"),
 ("Captain Phillips", "Paul Greengrass, 2013", r"captain phillips"),
 ("127 Hours", "Danny Boyle, 2010", r"127 hours"),
 ("The King's Speech", "Tom Hooper, 2010", r"king.?s speech"),
 ("I, Tonya", "Craig Gillespie, 2017", r"\bi,? tonya"),
 ("Band of Brothers", "Spielberg & Hanks, 2001", r"band of brothers"),
 ("The Right Stuff", "Philip Kaufman, 1983", r"right stuff"),
 ("Touching the Void", "Kevin Macdonald, 2003", r"touching the void"),
 ("All the President's Men", "Alan J. Pakula, 1976", r"president.?s men"),
 ("Bernie", "Richard Linklater, 2011", r"\bbernie\b(?!.?s)"),
 ("Amadeus", "Miloš Forman, 1984", r"amadeus"),
 ("The Great Escape", "John Sturges, 1963", r"great escape"),
 ("Dunkirk", "Christopher Nolan, 2017", r"dunkirk"),
 ("The Intouchables", "Nakache & Toledano, 2011", r"intouchables"),
 ("Weird: The Al Yankovic Story", "Eric Appel, 2022", r"weird al|al yankovic|wierd al"),
 ("The Last Emperor", "Bernardo Bertolucci, 1987", r"last emperor"),
 ("Lords of Dogtown", "Catherine Hardwicke, 2005", r"lords of dogtown"),
 ("Monster", "Patty Jenkins, 2003", r"^monster$"),
 ("Confessions of a Dangerous Mind", "George Clooney, 2002", r"confessions? of a dangerous mind"),
 ("Life of Brian", "Terry Jones, 1979", r"life of brian"),
 ("Rush", "Ron Howard, 2013", r"\brush\b"),
 ("The Killing Fields", "Roland Joffé, 1984", r"killing fields"),
 ("Casino", "Martin Scorsese, 1995", r"\bcasino\b"),
 ("Ray", "Taylor Hackford, 2004", r"^ray\b"),
 ("The Pursuit of Happyness", "Gabriele Muccino, 2006", r"pursuit of happ"),
 ("Chernobyl", "Craig Mazin, 2019", r"chernobyl"),
 ("We Were Soldiers", "Randall Wallace, 2002", r"we were soldiers"),
 ("Once Upon a Time in Hollywood", "Quentin Tarantino, 2019", r"once upon a time in hollywood"),
 ("Green Book", "Peter Farrelly, 2018", r"green book"),
 ("The Blind Side", "John Lee Hancock, 2009", r"blind side"),
 ("A Beautiful Mind", "Ron Howard, 2001", r"beautiful mind"),
 ("Erin Brockovich", "Steven Soderbergh, 2000", r"erin brock|erin brok|erin go brock"),
 ("Ford v Ferrari", "James Mangold, 2019", r"ford v"),
 ("The Pianist", "Roman Polanski, 2002", r"the pianist"),
 ("Coal Miner's Daughter", "Michael Apted, 1980", r"coal miner"),
 ("Tick, Tick… Boom!", "Lin-Manuel Miranda, 2021", r"tick,? ?tick"),
 ("Hoosiers", "David Anspaugh, 1986", r"hoosiers"),
 ("Blow", "Ted Demme, 2001", r"\bblow\b"),
 ("The Mothman Prophecies", "Mark Pellington, 2002", r"mothman"),
 ("Molly's Game", "Aaron Sorkin, 2017", r"molly.?s game"),
 ("Secretariat", "Randall Wallace, 2010", r"secretariat"),
 ("Saving Private Ryan", "Steven Spielberg, 1998", r"saving private ryan"),
 ("Almost Famous", "Cameron Crowe, 2000", r"almost famous"),
 ("The Texas Chain Saw Massacre", "Tobe Hooper, 1974", r"texas chain ?saw"),
 ("Unbroken", "Angelina Jolie, 2014", r"unbroken"),
 ("Malcolm X", "Spike Lee, 1992", r"malcolm x"),
 ("The World's Fastest Indian", "Roger Donaldson, 2005", r"fastest indian"),
 ("American Sniper", "Clint Eastwood, 2014", r"american sniper"),
 ("Hachi: A Dog's Tale", "Lasse Hallström, 2009", r"hachi"),
 ("Pain & Gain", "Michael Bay, 2013", r"pain (and|&|) ?gain"),
 ("A League of Their Own", "Penny Marshall, 1992", r"league of their own"),
 ("Glory", "Edward Zwick, 1989", r"\bglory\b"),
 ("Donnie Brasco", "Mike Newell, 1997", r"donnie brasco"),
 ("The Departed", "Martin Scorsese, 2006", r"departed"),
 ("Braveheart", "Mel Gibson, 1995", r"brave ?heart"),
 ("In Cold Blood", "Richard Brooks, 1967", r"in cold blood"),
 ("Alive", "Frank Marshall, 1993", r"^alive$"),
 ("The Sound of Music", "Robert Wise, 1965", r"sound of music"),
 ("The Exorcist", "William Friedkin, 1973", r"the exorcist"),
 ("The Disaster Artist", "James Franco, 2017", r"disaster artist"),
 ("Gallipoli", "Peter Weir, 1981", r"gallipoli"),
 ("13 Hours", "Michael Bay, 2016", r"13 h(ou)?rs|benga"),
 ("Dallas Buyers Club", "Jean-Marc Vallée, 2013", r"dallas buyers"),
 ("Papillon", "Franklin J. Schaffner, 1973", r"papillon"),
 ("Freedom Writers", "Richard LaGravenese, 2007", r"freedom writers"),
 ("Coach Carter", "Thomas Carter, 2005", r"coach carter"),
 ("Lion", "Garth Davis, 2016", r"\blion\b(?! king)"),
 ("Zero Dark Thirty", "Kathryn Bigelow, 2012", r"0 dark thirty|zero dark thirty"),
 ("JFK", "Oliver Stone, 1991", r"\bjfk\b"),
 ("Lord of War", "Andrew Niccol, 2005", r"lord of war"),
 ("Bridge of Spies", "Steven Spielberg, 2015", r"bridge of spies"),
 ("American Hustle", "David O. Russell, 2013", r"american hustle"),
 ("Cinderella Man", "Ron Howard, 2005", r"cinderella man"),
 ("Memories of Murder", "Bong Joon-ho, 2003", r"memories of murder"),
 ("Quiz Show", "Robert Redford, 1994", r"quiz show"),
 ("The Straight Story", "David Lynch, 1999", r"straight story"),
 ("Eddie the Eagle", "Dexter Fletcher, 2016", r"eddie the eagle"),
 ("Operation Mincemeat", "John Madden, 2021", r"mincemeat"),
 ("First Man", "Damien Chazelle, 2018", r"first man"),
 ("Hotel Rwanda", "Terry George, 2004", r"hotel raw?anda|hotel rwanda"),
 ("Man on Fire", "Tony Scott, 2004", r"man on fire"),
 ("Temple Grandin", "Mick Jackson, 2010", r"temple grandin"),
 ("The Terminal", "Steven Spielberg, 2004", r"the terminal"),
 ("Spencer", "Pablo Larraín, 2021", r"^spencer"),
 ("Bronson", "Nicolas Winding Refn, 2008", r"^bronson"),
 ("The Theory of Everything", "James Marsh, 2014", r"theory of everything"),
 ("Blood Diamond", "Edward Zwick, 2006", r"blood diamond"),
 ("Midnight Express", "Alan Parker, 1978", r"midnight express"),
 ("Thirteen Days", "Roger Donaldson, 2000", r"thirteen days"),
 ("Charlie Wilson's War", "Mike Nichols, 2007", r"charlie wilson"),
 ("Lone Survivor", "Peter Berg, 2013", r"lone survivor"),
 ("The Post", "Steven Spielberg, 2017", r"^the post"),
 ("Saving Mr. Banks", "John Lee Hancock, 2013", r"saving mr banks|saving mr\. banks"),
 ("Sergeant York", "Howard Hawks, 1941", r"sergeant york"),
 ("Hidalgo", "Joe Johnston, 2004", r"hidalgo"),
 ("Star 80", "Bob Fosse, 1983", r"star 80"),
 ("Dark Water", "Hideo Nakata, 2002", r"dark water"),
 ("Wonderland", "James Cox, 2003", r"^wonderland"),
 ("The Exorcism of Emily Rose", "Scott Derrickson, 2005", r"emily rose"),
 ("Jackass: The Movie", "Jeff Tremaine, 2002", r"jackass"),
 ("30 Minutes or Less", "Ruben Fleischer, 2011", r"30 minutes or less"),
 ("Only the Brave", "Joseph Kosinski, 2017", r"only the brave"),
 ("Midway", "Roland Emmerich, 2019", r"midway"),
 ("Lincoln", "Steven Spielberg, 2012", r"^lincoln"),
 ("Apocalypse Now", "Francis Ford Coppola, 1979", r"apocalypse now"),
 ("The Hunt", "Thomas Vinterberg, 2012", r"the hunt by"),
 ("Chariots of Fire", "Hugh Hudson, 1981", r"chariots of fire"),
 ("The Diving Bell and the Butterfly", "Julian Schnabel, 2007", r"diving bell"),
 ("Boys Don't Cry", "Kimberly Peirce, 1999", r"boys don.?t cry"),
 ("Adaptation", "Spike Jonze, 2002", r"^adaptation"),
 ("Come and See", "Elem Klimov, 1985", r"come and see"),
 ("Tora! Tora! Tora!", "Fleischer, Masuda & Fukasaku, 1970", r"tora tora"),
 ("A Night to Remember", "Roy Ward Baker, 1958", r"night to remember"),
 ("Gettysburg", "Ronald F. Maxwell, 1993", r"gettysburg"),
 ("Dead Man Walking", "Tim Robbins, 1995", r"dead man walking"),
 ("Little Big Man", "Arthur Penn, 1970", r"little big man"),
 ("Open Water", "Chris Kentis, 2003", r"open water"),
 ("Das Boot", "Wolfgang Petersen, 1981", r"das boo?t"),
 ("Room", "Lenny Abrahamson, 2015", r"^room$"),
 ("The Elephant Man", "David Lynch, 1980", r"elephant man"),
 ("Mask", "Peter Bogdanovich, 1985", r"^mask$"),
 ("Patch Adams", "Tom Shadyac, 1998", r"patch adams"),
 ("Breaker Morant", "Bruce Beresford, 1980", r"breaker morant"),
 ("In the Name of the Father", "Jim Sheridan, 1993", r"name of the father"),
 ("The Woman King", "Gina Prince-Bythewood, 2022", r"woman king"),
 ("Three Billboards Outside Ebbing, Missouri", "Martin McDonagh, 2017", r"three billboards"),
 ("Searching for Sugar Man", "Malik Bendjelloul, 2012", r"sugar ?man"),
 ("Margin Call", "J. C. Chandor, 2011", r"margin call"),
 ("Sully", "Clint Eastwood, 2016", r"\bsully\b"),
 ("The Founder", "John Lee Hancock, 2016", r"the founder"),
 ("American Made", "Doug Liman, 2017", r"american made"),
 ("Amityville Horror", "Stuart Rosenberg, 1979", r"amityville"),
 ("Togo", "Ericson Core, 2019", r"^togo"),
 ("Thirteen Lives", "Ron Howard, 2022", r"thirteen lives"),
 ("War Dogs", "Todd Phillips, 2016", r"war dogs"),
 ("Mesrine", "Jean-François Richet, 2008", r"mesrine"),
 ("Stand and Deliver", "Ramón Menéndez, 1988", r"stand and deliver"),
 ("We Are Marshall", "McG, 2006", r"we are marshall?"),
 ("Fly Away Home", "Carroll Ballard, 1996", r"fly away home"),
 ("The Polka King", "Maya Forbes, 2017", r"polka king"),
 ("Brian's Song", "Buzz Kulik, 1971", r"brian.?s song"),
 ("Love & Mercy", "Bill Pohlad, 2014", r"love (and|&) mercy"),
 ("Jackie", "Pablo Larraín, 2016", r"^jackie"),
 ("Awakenings", "Penny Marshall, 1990", r"awakening"),
 ("Reds", "Warren Beatty, 1981", r"\breds\b"),
 ("The Trial of the Chicago 7", "Aaron Sorkin, 2020", r"chicago (seven|7)"),
 ("Titanic", "James Cameron, 1997", r"\btitanic\b"),
 ("Gandhi", "Richard Attenborough, 1982", r"gh?andi\b"),
 ("1917", "Sam Mendes, 2019", r"\b1917\b"),
 ("Downfall", "Oliver Hirschbiegel, 2004", r"downfall"),
 ("The Irishman", "Martin Scorsese, 2019", r"irishman"),
 ("Valkyrie", "Bryan Singer, 2008", r"valkyrie"),
 ("Man on the Moon", "Miloš Forman, 1999", r"man on the moon"),
 ("Good Night, and Good Luck", "George Clooney, 2005", r"good night,? and good luck"),
 ("The Infiltrator", "Brad Furman, 2016", r"infiltrator"),
]

def main():
    rows = [l.rstrip("\n").split(" :: ", 2)
            for l in open("/home/claude/truestory.txt") if l.count(" :: ") >= 2]
    people = collections.defaultdict(set)
    score = collections.Counter()
    pats = [(t, d, re.compile(p)) for t, d, p in FILMS]
    for u, p, b in rows:
        k = re.sub(r"[^a-z0-9 &,'.!]", " ", b.lower())
        k = re.sub(r"\s+", " ", k).strip()
        for t, d, rx in pats:
            if rx.search(k):
                people[t].add(u)
                score[t] += int(p)
    meta = {t: d for t, d, _ in FILMS}
    out = sorted(people, key=lambda t: (-len(people[t]), -score[t], t))
    return [{"title": t, "by": meta[t], "n": len(people[t]), "pts": score[t]} for t in out]

if __name__ == "__main__":
    res = main()
    print(len(res))
    for r in res[:30]:
        print(r["n"], r["pts"], r["title"])
