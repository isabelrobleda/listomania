"""r/suggestmeabook — "What is that ONE book that slapped you across the face?"

Different from the other book tallies in one important way: the asker explicitly
ruled out the school-canon answers ("Orwell, Salinger, Harper Lee… no shade")
and asked for the ones you'd never have found on your own. So this list skews
obscure by construction, and that is the point of keeping it separate from
Never Stop Recommending and Books That Changed People.

Counting: by distinct redditor. A reply that seconds a book ("another vote for
Evicted", "THIS, I've re-read it so many times") counts as a mention, the same
as naming it first — agreement is the signal a tally is made of. A reply that
merely links the text or quotes a line does not. The asker's own books are
excluded, as everywhere else.

Four of these are not books: This Is Water and Consider the Lobster are essays,
Harrison Bergeron a short story, Letters to a Young Poet a set of letters. They
stay, because each was somebody's answer to the question.
"""
import json
from collections import defaultdict

THREAD = {
 "q": "What is that ONE book that slapped you across the face?",
 "site": "Reddit · r/suggestmeabook", "year": 2020,
 "meta": "2.3K points · 1.4K comments",
 "url": "https://www.reddit.com/r/suggestmeabook/comments/lludyk/what_is_that_one_book_that_slapped_you_across_the/",
}

# redditor -> the books they named
B = {
"Pumpernickel7": ["The House of the Spirits"],
"royalinsomniac": ["The House of the Spirits", "Daughter of Fortune", "Portrait in Sepia"],
"alwayssleepy99": ["The House of the Spirits"],
"garbanzoismyname": ["The House of the Spirits"],
"booktrovert": ["This Is Water"],
"Patriaboricua": ["This Is Water"],
"VivereIntrepidus": ["This Is Water"],
"vitasevern": ["This Is Water"],
"mila_sonder": ["This Is Water"],
"trissle_hippie": ["Crime and Punishment"],
"-n_h101-": ["A River Runs Through It"],
"Spock_Drop-n-Roll": ["Siddhartha"],
"carilee22": ["Saga"],
"calmtitties": ["Saga"],
"AntipatheticDating": ["Saga"],
"HoaryPuffleg": ["Saga", "Y: The Last Man"],
"gnrqtfa": ["How Children Fail"],
"gnswhwc": ["How Children Fail", "How Children Learn"],
"gnrx2ww": ["How Children Fail"],
"gnrnbqq": ["Speaker for the Dead"],
"pm_ur_DnD_backstory": ["Speaker for the Dead"],
"ilike41turtles": ["Speaker for the Dead"],
"gnrwuwi_nlmg": ["Never Let Me Go"],
"Dutten83": ["Never Let Me Go"],
"8heist": ["Never Let Me Go"],
"gns0i6a": ["Fahrenheit 451", "The Pillars of the Earth"],
"Flowers_4_Ophelia": ["White Oleander"],
"gns28zy": ["White Oleander"],
"whiskeyknitting": ["Night", "Donbas"],
"hockeygolfer": ["The Hitchhiker's Guide to the Galaxy"],
"ice1000": ["The Little Prince"],
"thematicwater": ["Frankenstein"],
"freshnutmeg33": ["Nickel and Dimed", "Evicted"],
"Nervous-Shark": ["Evicted"],
"gnrgw1a": ["Smoke and Mirrors"],
"gnrmofy": ["Chasing the Scream"],
"jashhond": ["The Wind-Up Bird Chronicle"],
"sandyshelley_": ["Only Ever Yours"],
"saevuswinds": ["Pachinko"],
"AtheneSchmidt": ["Harrison Bergeron"],
"Living_Employee_7735": ["In Cold Blood"],
"dinner-for-breakfast": ["The Unwinding", "The Heartbeat of Wounded Knee",
  "Stamped from the Beginning", "The New Jim Crow", "Caste", "Dreamland",
  "Winners Take All", "Sapiens"],
"Sentence_Electrical": ["East of Eden"],
"sunny2025": ["East of Eden"],
"n0thingt0seehere007": ["East of Eden"],
"blh497": ["Flowers for Algernon"],
"noelle2371": ["Flowers for Algernon"],
"Fear_Elise": ["Killers of the Flower Moon"],
"i_like_bread1": ["Beartown"],
"gnruuc7": ["Tortilla Flat"],
"5piders": ["If This Is a Man (Survival in Auschwitz)"],
"nubian_butter": ["I Know This Much Is True", "The Hour I First Believed"],
"erinmiyu": ["She's Come Undone"],
"authorpics": ["The Power of Now"],
"jharleyk": ["A Tale for the Time Being"],
"Cotford": ["Dune"],
"lettuce_embargo": ["The Red Tent"],
"coy__fish": ["The Gray House"],
"gnsrdah": ["Gone with the Wind"],
"kottabaz": ["Bullshit Jobs"],
"FittedSheets88": ["The Demon-Haunted World"],
"gnrsc7o": ["The Good Earth"],
"gnrz5ib": ["The Good Earth"],
"PlaceboRoshambo": ["Talking to Strangers"],
"jholla_albologne": ["Slaughterhouse-Five"],
"Cosy_Majesty": ["Thinking, Fast and Slow"],
"rita1431": ["The Outsiders"],
"bgkh20": ["Tess of the d'Urbervilles"],
"Scepta101": ["Percy Jackson and the Olympians"],
"gnrgbi2": ["Between the World and Me"],
"noveltoes": ["Letters to a Young Poet", "The Four Agreements"],
"LookItsOnlyHarry": ["Of Mice and Men", "To Kill a Mockingbird"],
"bonky4": ["Consider the Lobster"],
"brith89": ["The Art of Asking"],
"Oleah2014": ["Call the Midwife"],
"woahdudeyeeeeet": ["The Poisonwood Bible"],
"jd208bh": ["The Book Thief"],
"imgayandilikethings": ["The Book Thief"],
"teaheadcase": ["We Were the Mulvaneys", "Horns", "Junky"],
"AfterSomewhere": ["I Know Why the Caged Bird Sings"],
}

A = {
"A River Runs Through It": "Norman Maclean",
"A Tale for the Time Being": "Ruth Ozeki",
"Beartown": "Fredrik Backman",
"Between the World and Me": "Ta-Nehisi Coates",
"Bullshit Jobs": "David Graeber",
"Call the Midwife": "Jennifer Worth",
"Caste": "Isabel Wilkerson",
"Chasing the Scream": "Johann Hari",
"Consider the Lobster": "David Foster Wallace",
"Crime and Punishment": "Fyodor Dostoevsky",
"Daughter of Fortune": "Isabel Allende",
"Donbas": "Jacques Sandulescu",
"Dreamland": "Sam Quinones",
"Dune": "Frank Herbert",
"East of Eden": "John Steinbeck",
"Evicted": "Matthew Desmond",
"Fahrenheit 451": "Ray Bradbury",
"Flowers for Algernon": "Daniel Keyes",
"Frankenstein": "Mary Shelley",
"Gone with the Wind": "Margaret Mitchell",
"Harrison Bergeron": "Kurt Vonnegut",
"Horns": "Joe Hill",
"How Children Fail": "John Holt",
"How Children Learn": "John Holt",
"I Know This Much Is True": "Wally Lamb",
"I Know Why the Caged Bird Sings": "Maya Angelou",
"If This Is a Man (Survival in Auschwitz)": "Primo Levi",
"In Cold Blood": "Truman Capote",
"Junky": "William S. Burroughs",
"Killers of the Flower Moon": "David Grann",
"Letters to a Young Poet": "Rainer Maria Rilke",
"Never Let Me Go": "Kazuo Ishiguro",
"Nickel and Dimed": "Barbara Ehrenreich",
"Night": "Elie Wiesel",
"Of Mice and Men": "John Steinbeck",
"Only Ever Yours": "Louise O'Neill",
"Pachinko": "Min Jin Lee",
"Percy Jackson and the Olympians": "Rick Riordan",
"Portrait in Sepia": "Isabel Allende",
"Saga": "Brian K. Vaughan & Fiona Staples",
"Sapiens": "Yuval Noah Harari",
"She's Come Undone": "Wally Lamb",
"Siddhartha": "Hermann Hesse",
"Slaughterhouse-Five": "Kurt Vonnegut",
"Smoke and Mirrors": "Dan Baum",
"Speaker for the Dead": "Orson Scott Card",
"Stamped from the Beginning": "Ibram X. Kendi",
"Talking to Strangers": "Malcolm Gladwell",
"Tess of the d'Urbervilles": "Thomas Hardy",
"The Art of Asking": "Amanda Palmer",
"The Book Thief": "Markus Zusak",
"The Demon-Haunted World": "Carl Sagan",
"The Four Agreements": "Don Miguel Ruiz",
"The Good Earth": "Pearl S. Buck",
"The Gray House": "Mariam Petrosyan",
"The Heartbeat of Wounded Knee": "David Treuer",
"The Hitchhiker's Guide to the Galaxy": "Douglas Adams",
"The Hour I First Believed": "Wally Lamb",
"The House of the Spirits": "Isabel Allende",
"The Little Prince": "Antoine de Saint-Exupéry",
"The New Jim Crow": "Michelle Alexander",
"The Outsiders": "S. E. Hinton",
"The Pillars of the Earth": "Ken Follett",
"The Poisonwood Bible": "Barbara Kingsolver",
"The Power of Now": "Eckhart Tolle",
"The Red Tent": "Anita Diamant",
"The Unwinding": "George Packer",
"The Wind-Up Bird Chronicle": "Haruki Murakami",
"Thinking, Fast and Slow": "Daniel Kahneman",
"This Is Water": "David Foster Wallace",
"To Kill a Mockingbird": "Harper Lee",
"Tortilla Flat": "John Steinbeck",
"We Were the Mulvaneys": "Joyce Carol Oates",
"White Oleander": "Janet Fitch",
"Winners Take All": "Anand Giridharadas",
"Y: The Last Man": "Brian K. Vaughan",
}

counts = defaultdict(set)
for user, books in B.items():
    for b in books:
        counts[b].add(user)

rows = sorted(({"title": t, "author": A.get(t, ""), "mentions": len(u)} for t, u in counts.items()),
              key=lambda r: (-r["mentions"], r["title"].lower()))

json.dump({"thread": THREAD, "rows": rows}, open("slapped.json", "w"),
          ensure_ascii=False, separators=(",", ":"))
print(len(rows), "books from", len(B), "redditors;", sum(r["mentions"] for r in rows), "mentions")
print("missing authors:", [r["title"] for r in rows if not r["author"]] or "none")
for r in rows[:10]:
    print(f'  {r["mentions"]}x  {r["title"]} — {r["author"]}')
