#!/usr/bin/env python3
"""r/nonfictionbooks — "What is your top 3 non fiction books of all time?"

The whole thread, replies included: 141 comments captured of 144, nothing left
behind "load more".

Ranked by DISTINCT REDDITORS naming the book as one they rate. Where a comment
lists several books, each one counts — honourable mentions and "shout-outs"
too, since those were offered as favourites. A reply counts when it names the
book with an opinion of its own ("Into Thin Air is so good!", "The Swerve is
pretty great"); nameless agreement ("YES. YES. YES.", "That first one is the
best") adds nothing. Upvotes on the naming comments break ties.

Left out:
  - the asker's own pick (The Spy and the Traitor, in a reply), as on every
    other book tally;
  - suggestions with no opinion attached ("Take a look at Into the Raging
    Sea"), and books someone has only just requested or plans to read;
  - authors or bodies of work with no title ("Love Barbara Tuchman", "Andrew
    Ross Sorkin's books", "I bow down to bell hooks");
  - things that are not non-fiction: The Killer Angels (a novel), Shakespeare's
    Sonnets;
  - a commenter plugging his own two books.

Run from the repo root:  python3 tools/nonfiction.py && python3 tools/agreed.py
"""
import json

PATH = "content/shelves.json"
SLUG = "top-three-non-fiction"
URL = "https://www.reddit.com/r/nonfictionbooks/comments/1wngzve/what_is_your_top_3_non_fiction_books_of_all_time/"

# (redditor, score of the naming comment, books)
C = [
("Repulsive-Dot553", 39, ["Master of the Senate", "Shadow Divers", "Team of Rivals", "This House of Grief", "The Season"]),
("sethj1972", 6, ["Shadow Divers"]),
("ms_merry", 4, ["The New Jim Crow", "Master of the Senate", "The Devil's Highway", "Shadow Divers",
                 "Pirate Hunters", "The Power Broker", "Boom Town", "Rising Tide", "Killings", "War",
                 "Fatherland"]),
("BooBoo_Cat", 18, ["The Mother Tongue", "The World in a Grain", "Entangled Life"]),
("nothanks211", 11, ["Entangled Life", "I Know Why the Caged Bird Sings", "Ain't I a Woman"]),
("Timely_Bluebird_3177", 30, ["The Autobiography of Malcolm X", "In Cold Blood", "Into Thin Air"]),
("AaronJudge2", 1, ["Into Thin Air"]),
("Constant_Wonder_617", 3, ["In Cold Blood", "The Spy and the Traitor", "Empire of Pain", "A Woman of No Importance",
                            "The Indifferent Stars Above", "The Wager", "Say Nothing"]),
("rp_editing", 13, ["The Swerve", "The Spirit Catches You and You Fall Down", "The Serpent and the Rainbow"]),
("prairiepog", 4, ["The Spirit Catches You and You Fall Down"]),
("CleverMeatRobot", 2, ["The Swerve"]),
("Kind-Patience6169", 12, ["The Wager", "In the Heart of the Sea", "The Indifferent Stars Above", "The Best Land Under Heaven"]),
("Grand-Agent-4189", 21, ["The Warmth of Other Suns"]),
("UnripeBanana_Hammock", 4, ["Caste"]),
("Disastrous_Sorbet350", 8, ["Endurance", "Into Thin Air", "Are Prisons Obsolete?", "Overground Railroad",
                             "Woody Guthrie: A Life", "Blitzed"]),
("Realistic-Owl-9904", 3, ["Blitzed", "An Immense World", "Team of Rivals", "All the President's Men",
                           "The Power Broker", "The Boys in the Boat"]),
("Remote-Possible5666", 13, ["A Billion Years", "Everything Is Tuberculosis", "The Emperor of All Maladies"]),
("TrekingTrogdor", 5, ["The Lumumba Plot", "Homefront", "Patriotic Treason"]),
("ataltalt", 15, ["Say Nothing", "The Only Plane in the Sky", "Boom Town"]),
("tarmaroc", 2, ["Say Nothing"]),
("RansomRd", 2, ["The Only Plane in the Sky", "The Tender Bar", "What Should I Do with My Life?",
                 "The Man in the Rockefeller Suit"]),
("Few_Freedom_2283", 1, ["The Only Plane in the Sky"]),
("Ok_Yesterday_9181", 2, ["The Beast", "The Lost City of Z", "Into Thin Air", "Krakatoa"]),
("SoilNerdForAMF", 2, ["The 1619 Project"]),
("No-Hurry3034", 4, ["Einstein", "Team of Rivals", "Blood and Thunder", "The Westerners"]),
("c77123", 3, ["Say Nothing", "Moneyball", "The Looming Tower"]),
("asteriskelipses", 3, ["Subculture: The Meaning of Style", "Folk Devils and Moral Panics", "Fearing the Black Body"]),
("bpottrb", 4, ["The Guns of August", "The Spirit Catches You and You Fall Down", "Being Mortal",
                "Cadillac Desert", "Under the Banner of Heaven"]),
("xbookxbookxbook", 4, ["Rising Tide", "A Civil Action", "Killings", "Valley So Low"]),
("Betty_Pitch_", 7, ["People Who Eat Darkness", "Under the Banner of Heaven", "Hidden Valley Road"]),
("SmartPolicy6430", 6, ["Islands of Abandonment", "The Old Ways", "Stalin: The Court of the Red Tsar"]),
("michaelmoby", 3, ["Carrying the Fire", "John Adams", "Royal Panoply"]),
("I_see_zebras", 2, ["John Adams"]),
("TedBroke", 3, ["The Demon-Haunted World", "The Looming Tower", "The Devil's Chessboard"]),
("hollywobble", 3, ["Radium Girls", "The Five", "This One Wild and Precious Life"]),
("FrenchToastMMM", 4, ["The Power Broker", "One Day", "Deep Survival"]),
("GolfAlternative8572", 4, ["Master of the Senate", "The Power Broker", "Storm of Steel"]),
("cjersin1021", 2, ["Why Fish Don't Exist", "A Short History of Nearly Everything", "Reaganland"]),
("Minute-Sun8047", 2, ["Empire of Pain", "Rising Out of Hatred", "The Psychopath Test", "After Steve",
                       "Apple in China", "Dark Towers"]),
("ontheshelves", 2, ["Down by the Riverside", "Living in the Shadow of Death", "Everyday Life in Early America"]),
("Mscharlita", 2, ["Seven Years in Tibet", "Empty Mansions", "Actress of a Certain Age"]),
("christinemillerdvm", 2, ["Race Against Time", "The Hot Zone", "The Rise and Fall of the Third Reich"]),
("PTechNM", 2, ["The New Jim Crow", "The Dawn of Everything", "Open Veins of Latin America"]),
("Vegan_Zukunft", 2, ["The Color of Law"]),
("caffinatedswan", 2, ["Angela's Ashes", "Salt: A World History", "My Life in France"]),
("FormerIndependence68", 2, ["Agent Zo", "The Bounty", "Eisenhower in War and Peace", "How Ike Led",
                             "Batavia", "Ned Kelly"]),
("Basic-Style-8512", 2, ["Ecclesiastes", "On the Origin of Species"]),
("pandantea", 2, ["Good Morning, Monster", "Spark", "Why We Sleep"]),
("Deep-Dimension-1088", 2, ["Where the Wild Things Were", "The Gene", "The Omnivore's Dilemma"]),
("The_BobSacamano", 2, ["Man's Search for Meaning"]),
("Alternative-Card-261", 3, ["The Warmth of Other Suns"]),
("sjplep", 2, ["Tao Te Ching", "The Communist Manifesto", "Meditations"]),
("Slackermom66", 1, ["Gertrude Bell: Queen of the Desert", "Last Call", "Team of Rivals"]),
("SoftCheeseHero", 1, ["One of Us", "How the Word Is Passed", "Into the Wild"]),
("New_Seaweed_6554", 1, ["The Power Broker", "The Age of Faith", "Common Ground"]),
("pontiuspilate01", 1, ["Savage Continent", "Caste", "The Origins of Totalitarianism"]),
("Maximum_Jello_9460", 1, ["The Master and His Emissary", "Buckley", "Food of the Gods"]),
("IcedCoffeeBlack1", 1, ["In Cold Blood", "Into Thin Air", "Kitchen Confidential"]),
("tweedlebettlebattle", 1, ["Piece of Cake", "Ravensbrück", "An Interrupted Life"]),
("Background_Pepper225", 1, ["And the Band Played On", "Spillover", "The Emperor of All Maladies"]),
("CannotSt0p", 1, ["The Lost"]),
("Jorelthethird", 1, ["The Autobiography of Benjamin Franklin", "Against the Gods", "A World Lit Only by Fire"]),
("LeninsState", 1, ["Washington Bullets", "Secrets", "Say Nothing"]),
("Worth-Secretary-3383", 1, ["Master of the Senate", "What It Takes", "Go East, Young Man"]),
("briantomoc", 1, ["Into Thin Air", "Emptiness Dancing", "Everything Was Possible"]),
("Outdoorfan73", 1, ["The Emperor of All Maladies", "Being Mortal", "The Color of Law"]),
("kaki3261", 1, ["Marching Powder", "London Falling", "How to Fail"]),
("Imperial_Haberdasher", 1, ["The Death and Life of Great American Cities", "In the Slick of the Cricket",
                             "Motoring with Mohammed"]),
("SunKissedHibiscus", 1, ["People Love Dead Jews", "Ordinary Men", "The Lady and Her Monsters"]),
("Flimsy-Extreme5007", 1, ["The Man from the Train"]),
("sibling_revelry", 1, ["Colour: Travels Through the Paintbox", "Ghosts of the Tsunami", "Krakatoa"]),
("niceonebruv432", 1, ["Thus Spoke Zarathustra", "Down and Out in Paris and London", "The Secret"]),
("Perfect-Leg-3348", 1, ["The Influence of Sea Power Upon History", "Personal Memoirs of U. S. Grant",
                         "Disturbing the Universe"]),
("stimmtnicht", 1, ["Into Thin Air", "Say Nothing", "Just Mercy"]),
("masson34", 1, ["Man's Search for Meaning", "Under the Banner of Heaven", "Tuesdays with Morrie"]),
("zigzagdingbat", 1, ["The Path to Power", "Che Guevara: A Revolutionary Life", "Heroes: Mass Murder and Suicide"]),
]

AUTHORS = {
"Master of the Senate": "Robert Caro", "The Power Broker": "Robert Caro", "The Path to Power": "Robert Caro",
"Shadow Divers": "Robert Kurson", "Pirate Hunters": "Robert Kurson",
"Team of Rivals": "Doris Kearns Goodwin",
"This House of Grief": "Helen Garner", "The Season": "Helen Garner",
"The New Jim Crow": "Michelle Alexander", "The Devil's Highway": "Luis Alberto Urrea",
"Boom Town": "Sam Anderson", "Rising Tide": "John M. Barry", "Killings": "Calvin Trillin",
"War": "Sebastian Junger", "Fatherland": "Burkhard Bilger",
"The Mother Tongue": "Bill Bryson", "A Short History of Nearly Everything": "Bill Bryson",
"The World in a Grain": "Vince Beiser", "Entangled Life": "Merlin Sheldrake",
"I Know Why the Caged Bird Sings": "Maya Angelou", "Ain't I a Woman": "bell hooks",
"The Autobiography of Malcolm X": "Malcolm X & Alex Haley", "In Cold Blood": "Truman Capote",
"Into Thin Air": "Jon Krakauer", "Into the Wild": "Jon Krakauer", "Under the Banner of Heaven": "Jon Krakauer",
"The Spy and the Traitor": "Ben Macintyre", "Empire of Pain": "Patrick Radden Keefe", "Say Nothing": "Patrick Radden Keefe",
"A Woman of No Importance": "Sonia Purnell", "The Indifferent Stars Above": "Daniel James Brown",
"The Boys in the Boat": "Daniel James Brown", "The Wager": "David Grann", "The Lost City of Z": "David Grann",
"The Swerve": "Stephen Greenblatt", "The Spirit Catches You and You Fall Down": "Anne Fadiman",
"The Serpent and the Rainbow": "Wade Davis", "In the Heart of the Sea": "Nathaniel Philbrick",
"The Best Land Under Heaven": "Michael Wallis", "The Warmth of Other Suns": "Isabel Wilkerson",
"Caste": "Isabel Wilkerson", "Endurance": "Alfred Lansing", "Are Prisons Obsolete?": "Angela Y. Davis",
"Overground Railroad": "Candacy Taylor", "Woody Guthrie: A Life": "Joe Klein", "Blitzed": "Norman Ohler",
"An Immense World": "Ed Yong", "All the President's Men": "Carl Bernstein & Bob Woodward",
"A Billion Years": "Mike Rinder", "Everything Is Tuberculosis": "John Green",
"The Emperor of All Maladies": "Siddhartha Mukherjee", "The Gene": "Siddhartha Mukherjee",
"The Lumumba Plot": "Stuart A. Reid", "Homefront": "Catherine Lutz", "Patriotic Treason": "Evan Carton",
"The Only Plane in the Sky": "Garrett M. Graff", "The Tender Bar": "J. R. Moehringer",
"What Should I Do with My Life?": "Po Bronson", "The Man in the Rockefeller Suit": "Mark Seal",
"The Beast": "Óscar Martínez", "Krakatoa": "Simon Winchester", "The 1619 Project": "Nikole Hannah-Jones (ed.)",
"Einstein": "Walter Isaacson", "Blood and Thunder": "Hampton Sides", "The Westerners": "Megan Kate Nelson",
"Moneyball": "Michael Lewis", "The Looming Tower": "Lawrence Wright",
"Subculture: The Meaning of Style": "Dick Hebdige", "Folk Devils and Moral Panics": "Stanley Cohen",
"Fearing the Black Body": "Sabrina Strings", "The Guns of August": "Barbara W. Tuchman",
"Being Mortal": "Atul Gawande", "Cadillac Desert": "Marc Reisner", "A Civil Action": "Jonathan Harr",
"Valley So Low": "Jared Sullivan", "People Who Eat Darkness": "Richard Lloyd Parry",
"Ghosts of the Tsunami": "Richard Lloyd Parry", "Hidden Valley Road": "Robert Kolker",
"Islands of Abandonment": "Cal Flyn", "The Old Ways": "Robert Macfarlane",
"Stalin: The Court of the Red Tsar": "Simon Sebag Montefiore", "Carrying the Fire": "Michael Collins",
"John Adams": "David McCullough", "Royal Panoply": "Carolly Erickson",
"The Demon-Haunted World": "Carl Sagan", "The Devil's Chessboard": "David Talbot",
"Radium Girls": "Kate Moore", "The Five": "Hallie Rubenhold", "This One Wild and Precious Life": "Sarah Wilson",
"One Day": "Gene Weingarten", "Deep Survival": "Laurence Gonzales", "Storm of Steel": "Ernst Jünger",
"Why Fish Don't Exist": "Lulu Miller", "Reaganland": "Rick Perlstein",
"Rising Out of Hatred": "Eli Saslow", "The Psychopath Test": "Jon Ronson", "After Steve": "Tripp Mickle",
"Apple in China": "Patrick McGee", "Dark Towers": "David Enrich",
"Down by the Riverside": "Charles Joyner", "Living in the Shadow of Death": "Sheila M. Rothman",
"Everyday Life in Early America": "David Freeman Hawke",
"Seven Years in Tibet": "Heinrich Harrer", "Empty Mansions": "Bill Dedman & Paul Clark Newell Jr.",
"Actress of a Certain Age": "—",
"Race Against Time": "Jerry Mitchell", "The Hot Zone": "Richard Preston",
"The Rise and Fall of the Third Reich": "William L. Shirer", "The Dawn of Everything": "David Graeber & David Wengrow",
"Open Veins of Latin America": "Eduardo Galeano", "The Color of Law": "Richard Rothstein",
"Angela's Ashes": "Frank McCourt", "Salt: A World History": "Mark Kurlansky", "My Life in France": "Julia Child",
"Agent Zo": "Clare Mulley", "The Bounty": "Caroline Alexander", "Eisenhower in War and Peace": "Jean Edward Smith",
"How Ike Led": "Susan Eisenhower", "Batavia": "Peter FitzSimons", "Ned Kelly": "Ian Jones",
"Ecclesiastes": "The Bible", "On the Origin of Species": "Charles Darwin",
"Good Morning, Monster": "Catherine Gildiner", "Spark": "John J. Ratey", "Why We Sleep": "Matthew Walker",
"Where the Wild Things Were": "William Stolzenburg", "The Omnivore's Dilemma": "Michael Pollan",
"Man's Search for Meaning": "Viktor E. Frankl", "Tao Te Ching": "Laozi", "The Communist Manifesto": "Karl Marx & Friedrich Engels",
"Meditations": "Marcus Aurelius", "Gertrude Bell: Queen of the Desert": "Georgina Howell",
"Last Call": "Daniel Okrent", "One of Us": "Åsne Seierstad", "How the Word Is Passed": "Clint Smith",
"The Age of Faith": "Will Durant", "Common Ground": "J. Anthony Lukas", "Savage Continent": "Keith Lowe",
"The Origins of Totalitarianism": "Hannah Arendt", "The Master and His Emissary": "Iain McGilchrist",
"Buckley": "Sam Tanenhaus", "Food of the Gods": "Terence McKenna", "Kitchen Confidential": "Anthony Bourdain",
"Piece of Cake": "—", "Ravensbrück": "Sarah Helm", "An Interrupted Life": "Etty Hillesum",
"And the Band Played On": "Randy Shilts", "Spillover": "David Quammen", "The Lost": "Daniel Mendelsohn",
"The Autobiography of Benjamin Franklin": "Benjamin Franklin", "Against the Gods": "Peter L. Bernstein",
"A World Lit Only by Fire": "William Manchester", "Washington Bullets": "Vijay Prashad", "Secrets": "Daniel Ellsberg",
"What It Takes": "Richard Ben Cramer", "Go East, Young Man": "William O. Douglas",
"Emptiness Dancing": "Adyashanti", "Everything Was Possible": "Ted Chapin",
"Marching Powder": "Rusty Young", "London Falling": "—", "How to Fail": "Elizabeth Day",
"The Death and Life of Great American Cities": "Jane Jacobs", "In the Slick of the Cricket": "Russell Drumm",
"Motoring with Mohammed": "Eric Hansen", "People Love Dead Jews": "Dara Horn", "Ordinary Men": "Christopher R. Browning",
"The Lady and Her Monsters": "Roseanne Montillo", "The Man from the Train": "Bill James & Rachel McCarthy James",
"Colour: Travels Through the Paintbox": "Victoria Finlay", "Thus Spoke Zarathustra": "Friedrich Nietzsche",
"Down and Out in Paris and London": "George Orwell", "The Secret": "Rhonda Byrne",
"The Influence of Sea Power Upon History": "Alfred Thayer Mahan", "Personal Memoirs of U. S. Grant": "Ulysses S. Grant",
"Disturbing the Universe": "Freeman Dyson", "Just Mercy": "Bryan Stevenson", "Tuesdays with Morrie": "Mitch Albom",
"Che Guevara: A Revolutionary Life": "Jon Lee Anderson", "Heroes: Mass Murder and Suicide": "Franco \"Bifo\" Berardi",
}

ASKER = "jmshdsth88"

people, votes = {}, {}
for who, score, books in C:
    assert who != ASKER
    for b in books:
        assert b in AUTHORS, b
        people.setdefault(b, set())
        if who not in people[b]:
            people[b].add(who)
            votes[b] = votes.get(b, 0) + score

order = sorted(people, key=lambda b: (-len(people[b]), -votes[b], b.lower()))
src = {"label": "r/nonfictionbooks", "url": URL}
rows = [{"key": f"nf3|{b}", "lead": f"{len(people[b])}×", "sec": AUTHORS[b], "pri": b, "src": src}
        for b in order]

top = order[0]
LIST = {
    "slug": SLUG,
    "title": "Top Three Non-Fiction",
    "kind": "Tally",
    "verb": "read",
    "desc": (f"r/nonfictionbooks, asked for their top three of all time: {len(rows)} books from "
             f"{len({w for w, _, _ in C})} readers. Krakauer on Everest on top, and two authors "
             "&mdash; Krakauer and Robert Caro &mdash; all over it."),
    "cols": ["Named by", "Author", "Title", "Look up · source"],
    "gr": "sec",
    "sources": [{"url": URL, "label": "Reddit · r/nonfictionbooks",
                 "q": "What is your top 3 non fiction books of all time?",
                 "meta": "2026 · 102 points · 144 comments"}],
    "note": ("Counted by distinct redditor; where a comment named several books, each one counts, honourable "
             "mentions included, and upvotes on the naming comments break ties. The whole thread, replies and "
             "all: 141 of 144 comments. A reply counts when it names the book with an opinion "
             "(&ldquo;<em>Into Thin Air</em> is so good!&rdquo;); nameless agreement doesn&rsquo;t. Left out: the "
             "asker&rsquo;s own pick, suggestions with no opinion attached, authors named without a title, a novel "
             "and a book of sonnets, and one commenter plugging his own jazz books. <b>A small thread, and it "
             "shows:</b> three books in four are named once, and the top count is seven, for <em>Into Thin "
             "Air</em>. The agreement is in authors rather than titles. Jon Krakauer is named eleven times "
             "across three books, Robert Caro ten across three &mdash; one reader leaves out &ldquo;the "
             "obligatory Caro, Krakauer, etc.&rdquo; precisely because everyone else will name them &mdash; and "
             "Patrick Radden Keefe eight, across two."),
    "rows": rows,
}

if __name__ == "__main__":
    shelves = json.load(open(PATH))
    books = [s for s in shelves if s["slug"] == "books"][0]
    books["lists"] = [l for l in books["lists"] if l["slug"] != SLUG] + [LIST]
    json.dump(shelves, open(PATH, "w"), ensure_ascii=False, indent=1)
    print(len(rows), "books from", len({w for w, _, _ in C}), "redditors,",
          sum(len(p) for p in people.values()), "mentions,", sum(1 for p in people.values() if len(p) == 1), "once")
    for b in order[:15]:
        print(f"  {len(people[b]):>2}×  {b} ({votes[b]} pts)")
