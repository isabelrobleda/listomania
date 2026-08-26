"""r/suggestmeabook — "What is your number 1 MUST-READ fiction book of the last 10-15 years?"
Counted by distinct redditor: naming a book, or endorsing it in a reply, counts once.
"""
import json

THREAD = {
 "q": "What is your number 1 MUST-READ fiction book of the last 10-15 years?",
 "site": "Reddit · r/suggestmeabook", "year": 2025,
 "meta": "647 points · 1K comments",
 "url": "https://www.reddit.com/r/suggestmeabook/comments/1hw0pty/what_is_your_number_1_must_read_fiction_book_of/",
}

D = [
 ("Demon Copperhead","Barbara Kingsolver",2022,5),
 ("Small Things Like These","Claire Keegan",2021,4),
 ("11/22/63","Stephen King",2011,3),
 ("Station Eleven","Emily St. John Mandel",2014,3),
 ("The Library at Mount Char","Scott Hawkins",2015,3),
 ("The Poisonwood Bible","Barbara Kingsolver",1998,3),
 ("The Heart's Invisible Furies","John Boyne",2017,2),
 ("Drive Your Plow Over the Bones of the Dead","Olga Tokarczuk",2009,2),
 ("The Neapolitan Novels","Elena Ferrante",2012,2),
 ("Pachinko","Min Jin Lee",2017,2),
 ("The Overstory","Richard Powers",2018,2),
 ("The Amazing Adventures of Kavalier & Clay","Michael Chabon",2000,2),
 ("A Gentleman in Moscow","Amor Towles",2016,2),
 ("Cloud Cuckoo Land","Anthony Doerr",2021,2),
 ("Project Hail Mary","Andy Weir",2021,2),
 ("Lincoln in the Bardo","George Saunders",2017,2),
 ("All the Light We Cannot See","Anthony Doerr",2014,2),
 ("Wool","Hugh Howey",2011,2),
 ("Homegoing","Yaa Gyasi",2016,1),
 ("Flights","Olga Tokarczuk",2007,1),
 ("The Fifth Season","N.K. Jemisin",2015,1),
 ("Severance","Ling Ma",2018,1),
 ("A Fine Balance","Rohinton Mistry",1995,1),
 ("Playground","Richard Powers",2024,1),
 ("Greenwood","Michael Christie",2019,1),
 ("Shantaram","Gregory David Roberts",2003,1),
 ("Shuggie Bain","Douglas Stuart",2020,1),
 ("The Nickel Boys","Colson Whitehead",2019,1),
 ("The Goldfinch","Donna Tartt",2013,1),
 ("Commonwealth","Ann Patchett",2016,1),
 ("Sea of Tranquility","Emily St. John Mandel",2022,1),
 ("The Dog Stars","Peter Heller",2012,1),
 ("Circe","Madeline Miller",2018,1),
 ("Remarkably Bright Creatures","Shelby Van Pelt",2022,1),
 ("The Power","Naomi Alderman",2016,1),
 ("Piranesi","Susanna Clarke",2020,1),
 ("The Song of Achilles","Madeline Miller",2011,1),
 ("The Terror","Dan Simmons",2007,1),
 ("Anathem","Neal Stephenson",2008,1),
 ("The Will of the Many","James Islington",2023,1),
 ("Still Life","Sarah Winman",2021,1),
 ("Eleanor Oliphant Is Completely Fine","Gail Honeyman",2017,1),
 ("The Power of the Dog","Don Winslow",2005,1),
 ("Being Mortal","Atul Gawande",2014,1),
 ("Nuclear War: A Scenario","Annie Jacobsen",2024,1),
 ("The Bear and the Nightingale","Katherine Arden",2017,1),
 ("The God of the Woods","Liz Moore",2024,1),
 ("There There","Tommy Orange",2018,1),
 ("The Martian","Andy Weir",2011,1),
 ("Atonement","Ian McEwan",2001,1),
 ("Parable of the Sower","Octavia E. Butler",1993,1),
 ("We, the Drowned","Carsten Jensen",2006,1),
 ("Klara and the Sun","Kazuo Ishiguro",2021,1),
 ("The House of Special Purpose","John Boyne",2009,1),
]

rows = sorted(({"title": t, "author": a, "year": y, "mentions": m} for t, a, y, m in D),
              key=lambda r: (-r["mentions"], r["title"].lower()))
json.dump({"thread": THREAD, "rows": rows}, open("mustread.json", "w"),
          ensure_ascii=False, separators=(",", ":"))
print(len(rows), "books;", sum(r["mentions"] for r in rows), "mentions")
for r in rows[:8]:
    print(f'  {r["mentions"]}x  {r["title"]} — {r["author"]} ({r["year"]})')
