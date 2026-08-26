"""r/movies — "Documentaries that make you go 'what the fuck?!?'" (2024)
Counted by distinct redditor: naming a doc, or endorsing one in a reply, counts once.
The asker's own examples (Dear Zachary, The Jinx, Cropsey, Three Identical Strangers)
are excluded from the count where they came from the question rather than an answer.
"""
import json

THREAD = {
 "q": "Documentaries that make you go “what the fuck?!?”",
 "site": "Reddit · r/movies", "year": 2024,
 "meta": "3.6K points · 2.7K comments",
 "url": "https://www.reddit.com/r/movies/comments/1ajrrc1/documentaries_that_make_you_go_what_the_fuck/",
}

D = [
 ("Abducted in Plain Sight", 2017, 8),
 ("Love Has Won: The Cult of Mother God", 2023, 8),
 ("Tickled", 2016, 6),
 ("The Act of Killing", 2012, 5),
 ("Grizzly Man", 2005, 4),
 ("American Nightmare", 2024, 4),
 ("Wild Wild Country", 2018, 3),
 ("The Wild and Wonderful Whites of West Virginia", 2009, 3),
 ("Weiner", 2016, 3),
 ("Free Solo", 2018, 3),
 ("The Mad Genius Behind Sea Monkeys", 2016, 2),
 ("The Imposter", 2012, 2),
 ("Evil Genius", 2018, 2),
 ("Icarus", 2017, 2),
 ("Going Clear", 2015, 2),
 ("Long Shot", 2017, 2),
 ("Tell Me Who I Am", 2019, 2),
 ("Hot Coffee", 2011, 2),
 ("The Staircase", 2004, 2),
 ("Capturing the Friedmans", 2003, 2),
 ("Kumaré", 2011, 1),
 ("Project Grizzly", 1996, 1),
 ("No Man Shall Protect Us", 2018, 1),
 ("Mister Organ", 2022, 1),
 ("Dark Days", 2000, 1),
 ("Keep Sweet: Pray and Obey", 2022, 1),
 ("The King of Kong", 2007, 1),
 ("Russia 1985–1999: TraumaZone", 2022, 1),
 ("Bitter Lake", 2015, 1),
 ("9/11", 2002, 1),
 ("Jesus Camp", 2006, 1),
 ("Into the Deep", 2020, 1),
 ("Murdaugh Murders: A Southern Scandal", 2023, 1),
 ("Exit Through the Gift Shop", 2010, 1),
 ("Stolen Youth: Inside the Cult at Sarah Lawrence", 2023, 1),
 ("The Keepers", 2017, 1),
 ("Class Action Park", 2020, 1),
 ("The Dawn Wall", 2017, 1),
 ("Meru", 2015, 1),
 ("Dark Side of the Ring", 2019, 1),
 ("Man on Wire", 2008, 1),
 ("Desperately Seeking Soulmate: Escaping Twin Flames Universe", 2023, 1),
 ("Fyre", 2019, 1),
 ("Catfish", 2010, 1),
]

rows = sorted(({"title": t, "year": y, "mentions": m} for t, y, m in D),
              key=lambda r: (-r["mentions"], r["title"].lower()))
json.dump({"thread": THREAD, "rows": rows}, open("docs.json", "w"),
          ensure_ascii=False, separators=(",", ":"))
print(len(rows), "documentaries;", sum(r["mentions"] for r in rows), "mentions")
for r in rows[:8]:
    print(f'  {r["mentions"]}x  {r["title"]} ({r["year"]})')
