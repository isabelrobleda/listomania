"""r/booksuggestions — "What's 1 book you will never stop recommending?"

Counted by DISTINCT REDDITOR. A person counts once per book, whether they
named it in a top-level comment or endorsed it in a reply ("can't recommend
this enough", "I second this"). Replies that only react ("you sold me") are
not counted, and neither are books mentioned to disagree with them.
"""
import json
from collections import defaultdict

THREAD = {
    "q": "What's 1 book you will never stop recommending?",
    "site": "Reddit · r/booksuggestions",
    "year": 2026,
    "url": "https://www.reddit.com/r/booksuggestions/comments/1rcgu40/whats_1_book_you_will_never_stop_recommending/",
}

# title, author, [usernames who recommended or endorsed it]
DATA = [
 ("Jurassic Park","Michael Crichton",["(top comment)","mikeybhoy_1985","Standard_Chance_7424","Tobias-Rasmussen","WanderlustDiveJunkie","Wireman332"]),
 ("Lonesome Dove","Larry McMurtry",["HouseOfSnax","princessdragon0","AbeFromanSassageKing","chunkychickmunk","fluffy_corgi_","girthytacos"]),
 ("Project Hail Mary","Andy Weir",["zachariah22791","Okay_Response","Mexikim","EvenTallerTree","Rachel1107"]),
 ("East of Eden","John Steinbeck",["Jules_Chaplin","gaust5","secretsafewiththis","girthytacos"]),
 ("The Count of Monte Cristo","Alexandre Dumas",["Majestic_Day_5559","GloomyRambouillet","FlobiusHole","Crown_the_Cat"]),
 ("The Pillars of the Earth","Ken Follett",["al778","elementalmw","Jae_Rides_Apes","23odyssey"]),
 ("11/22/63","Stephen King",["laurie911","mulvda","Banana_Stanley","autofry"]),
 ("Nineteen Eighty-Four","George Orwell",["Fruney21","ShirtDizzy","failure_mcgee"]),
 ("Shogun","James Clavell",["RegattaJoe","Beernuts1091","jfstompers"]),
 ("The Remains of the Day","Kazuo Ishiguro",["norfolkipine","gaust5","jfstompers"]),
 ("A Thousand Splendid Suns","Khaled Hosseini",["Elessaria","gryffindorr7","LukasLeonard"]),
 ("Dungeon Crawler Carl","Matt Dinniman",["Dry_Event_7695","ninade1022","GhettoBookWorm"]),
 ("Watership Down","Richard Adams",["mom_with_an_attitude","iDetestCambridge"]),
 ("The Giver","Lois Lowry",["sunnysideski1073","TanaFey"]),
 ("Pachinko","Min Jin Lee",["Wrong-One7376","skinnyontheloose"]),
 ("The Hitchhiker's Guide to the Galaxy","Douglas Adams",["Admirable_Tear_1438","Fruney21"]),
 ("A Prayer for Owen Meany","John Irving",["(deleted user)","UnicornOnTheJayneCob"]),
 ("Catch-22","Joseph Heller",["The-zKR0N0S","UnicornOnTheJayneCob"]),
 ("The Art of Racing in the Rain","Garth Stein",["Claud6568","Doingbit"]),
 ("Station Eleven","Emily St. John Mandel",["fabfour66","jfstompers"]),
 ("Lamb","Christopher Moore",["RoosterClan2","bolivar-shagnasty"]),
 ("Perfume: The Story of a Murderer","Patrick Süskind",["mikenotduncan"]),
 ("The Book Thief","Markus Zusak",["Fencejumper89"]),
 ("Educated","Tara Westover",["laurie911"]),
 ("A Wizard of Earthsea","Ursula K. Le Guin",["comandante_soft_wolf"]),
 ("600 Hours of Edward","Craig Lancaster",["al778"]),
 ("The Secret History","Donna Tartt",["_Sanxession_"]),
 ("The Goldfinch","Donna Tartt",["tanzimat14"]),
 ("The House in the Cerulean Sea","TJ Klune",["thedoc617"]),
 ("The Lord of the Rings","J.R.R. Tolkien",["SlappinPickle"]),
 ("One Hundred Years of Solitude","Gabriel García Márquez",["wretch3d-user"]),
 ("We Have Always Lived in the Castle","Shirley Jackson",["BatmanDoesntDoShips_"]),
 ("Demon Copperhead","Barbara Kingsolver",["Eudaimonita803"]),
 ("Man's Search for Meaning","Viktor E. Frankl",["yellowmonkeyzx93"]),
 ("Five Little Pigs","Agatha Christie",["MikaelAdolfsson"]),
 ("The Pearl","John Steinbeck",["Smooth_Review1046"]),
 ("The Autobiography of Malcolm X","Alex Haley",["om_hi"]),
 ("Flowers for Algernon","Daniel Keyes",["kelpkelso"]),
 ("Eleanor Oliphant Is Completely Fine","Gail Honeyman",["marvelous88"]),
 ("A Man Called Ove","Fredrik Backman",["Snus_Goes_Brrrr"]),
 ("The Kite Runner","Khaled Hosseini",["Lifestyle_Journal07"]),
 ("World War Z","Max Brooks",["jackalee219"]),
 ("Braiding Sweetgrass","Robin Wall Kimmerer",["inthedeadlights"]),
 ("The Screwtape Letters","C.S. Lewis",["seejoshrun"]),
 ("The Shadow of the Wind","Carlos Ruiz Zafón",["RoosterClan2"]),
 ("A Confederacy of Dunces","John Kennedy Toole",["SunshineDaedream"]),
 ("Jonathan Strange & Mr Norrell","Susanna Clarke",["_SiddharthaGautama_"]),
 ("A Short Stay in Hell","Steven L. Peck",["failure_mcgee"]),
 ("House of Leaves","Mark Z. Danielewski",["failure_mcgee"]),
 ("The Poisonwood Bible","Barbara Kingsolver",["sharpbehind2"]),
 ("John Dies at the End","David Wong",["Japjer"]),
 ("The Moon Is a Harsh Mistress","Robert A. Heinlein",["jfstompers"]),
 ("Furiously Happy","Jenny Lawson",["Any_Oil_4539"]),
 ("The Midnight Library","Matt Haig",["Changan96"]),
 ("A Tale of Two Cities","Charles Dickens",["Automatic-Bed-7845"]),
 ("The Blind Assassin","Margaret Atwood",["yesitsmenotyou"]),
 ("White Oleander","Janet Fitch",["ASadPanda208"]),
 ("She's Come Undone","Wally Lamb",["ASadPanda208"]),
 ("Sphere","Michael Crichton",["mikeybhoy_1985"]),
 ("The Andromeda Strain","Michael Crichton",["mikeybhoy_1985"]),
 ("Prey","Michael Crichton",["danielcube"]),
]

rows = sorted(
    ({"title": t, "author": a, "mentions": len(set(u))} for t, a, u in DATA),
    key=lambda r: (-r["mentions"], r["title"].lower()),
)
json.dump({"thread": THREAD, "rows": rows}, open("recs.json", "w"),
          ensure_ascii=False, separators=(",", ":"))
print(len(rows), "books;", sum(r["mentions"] for r in rows), "recommendations")
for r in rows[:12]:
    print(f'  {r["mentions"]}x  {r["title"]} — {r["author"]}')
