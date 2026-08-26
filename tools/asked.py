"""Build the 'Asked' list from two real Hacker News threads.

Extraction was done by reading each thread's comments via the public HN
(Algolia) API. Titles are counted by DISTINCT USERNAME, so one commenter
listing forty books contributes one mention each, not forty votes.
"""
import json, re
from collections import defaultdict

T1 = "17168136"   # Ask HN: What's one book that changed your life?  (2018)
T2 = "19087418"   # Ask HN: What books changed the way you think...?  (2019)

RAW = []
def add(tid, block):
    for line in block.strip().splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 2: continue
        user, title = parts[0], parts[1]
        author = parts[2] if len(parts) > 2 else ""
        if not title or title.startswith("("): continue
        RAW.append((tid, user, title, author))

add(T1, """
rmason | New Rules for the New Economy | Kevin Kelly
Finnucane | Do Androids Dream of Electric Sheep? | Philip K. Dick
Finnucane | Little, Big | John Crowley
Finnucane | The Shadow of the Torturer | Gene Wolfe
brogrammernot | The Inner Game of Tennis | W. Timothy Gallwey
bjoli | The Inner Game of Tennis | W. Timothy Gallwey
z66is | Writing on Water | Mooji
kaycebasques | The Six Pillars of Self-Esteem | Nathaniel Branden
porter | Critique of Pure Reason | Immanuel Kant
kirubakaran | The Hitchhiker's Guide to the Galaxy | Douglas Adams
AlphaGeekZulu | 1984 | George Orwell
AlphaGeekZulu | Gödel, Escher, Bach | Douglas Hofstadter
scirocco | Mindset | Carol Dweck
kp1 | How to Win Friends and Influence People | Dale Carnegie
Overtonwindow | Blink | Malcolm Gladwell
ex3ndr | Introduction to Algorithms | Cormen, Leiserson, Rivest, Stein
ziotom78 | The Brothers Karamazov | Fyodor Dostoevsky
mlthoughts2018 | Moral Mazes | Robert Jackall
lordnacho | The Poker Face of Wall Street | Aaron Brown
aphextron | Zen Mind, Beginner's Mind | Shunryu Suzuki
baxtr | Siddhartha | Hermann Hesse
clay_the_ripper | The War of Art | Steven Pressfield
mck- | The Art of Worldly Wisdom | Baltasar Gracián
akerbeltz | Gates of Fire | Steven Pressfield
Keloo | Zen and the Art of Motorcycle Maintenance | Robert M. Pirsig
filleokus | Economics in One Lesson | Henry Hazlitt
viburnum | Middlemarch | George Eliot
eddd | Crime and Punishment | Fyodor Dostoevsky
stephenson | Getting Real | 37signals
myst | Dandelion Wine | Ray Bradbury
Method5440 | The Story of B | Daniel Quinn
ariosto | The Catcher in the Rye | J.D. Salinger
alienjr | 12 Rules for Life | Jordan Peterson
alienjr | Meditations | Marcus Aurelius
alienjr | Thinking, Fast and Slow | Daniel Kahneman
alienjr | Walden | Henry David Thoreau
alienjr | On Liberty | John Stuart Mill
alienjr | The Master and Margarita | Mikhail Bulgakov
alienjr | One Day in the Life of Ivan Denisovich | Aleksandr Solzhenitsyn
alienjr | The Captive Mind | Czesław Miłosz
immigrantsheep | Count Zero | William Gibson
lpolovets | A Guide to the Good Life | William B. Irvine
9024037290 | A Confederacy of Dunces | John Kennedy Toole
qop | How to Win Friends and Influence People | Dale Carnegie
qop | Atlas Shrugged | Ayn Rand
lurena | The Space Merchants | Pohl & Kornbluth
madhouse | Flowers for Algernon | Daniel Keyes
rsheehan | The Art of Loving | Erich Fromm
uvesten | Finite and Infinite Games | James P. Carse
biswaroop | Kim | Rudyard Kipling
Buttons840 | Boyd: The Fighter Pilot Who Changed the Art of War | Robert Coram
ekblom | Quiet | Susan Cain
amrrs | Outliers | Malcolm Gladwell
spicyusername | The Sirens of Titan | Kurt Vonnegut
Isinlor | Into the Wild | Jon Krakauer
Isinlor | Born to Run | Christopher McDougall
HaoZeke | To Kill a Mockingbird | Harper Lee
_8usx | Ghost in the Wires | Kevin Mitnick
z66is | The Glass Bead Game | Hermann Hesse
bjoli | Practical Ethics | Peter Singer
wrycoder | The Order of Time | Carlo Rovelli
wrycoder | Absalom, Absalom! | William Faulkner
bbody | Thinking, Fast and Slow | Daniel Kahneman
oliwarner | The Easy Way to Stop Smoking | Allen Carr
rwieruch | Flow | Mihaly Csikszentmihalyi
gisborne | Dune | Frank Herbert
senatorobama | 12 Rules for Life | Jordan Peterson
MichaelMoser123 | The Tao of Pooh | Benjamin Hoff
MichaelMoser123 | Slaughterhouse-Five | Kurt Vonnegut
MichaelMoser123 | Darkness at Noon | Arthur Koestler
MichaelMoser123 | The Little Prince | Antoine de Saint-Exupéry
MichaelMoser123 | War and Peace | Leo Tolstoy
coreyyanofsky | Probability Theory: The Logic of Science | E.T. Jaynes
paridiso | Infinite Jest | David Foster Wallace
oluckyman | Why I Am Not a Christian | Bertrand Russell
fcolombo56 | Atlas Shrugged | Ayn Rand
Glench | Nonviolent Communication | Marshall Rosenberg
ydnaclementine | The Three-Body Problem | Liu Cixin
Arete31415 | A Tree Grows in Brooklyn | Betty Smith
joddystreet | Sapiens | Yuval Noah Harari
Fuzzwah | Operating Manual for Spaceship Earth | Buckminster Fuller
Fuzzwah | Small Gods | Terry Pratchett
drummyfish | Free Culture | Lawrence Lessig
Simulacra | Atlas Shrugged | Ayn Rand
blikdak | What Do You Say After You Say Hello? | Eric Berne
brensmith | A Pattern Language | Christopher Alexander
AnIdiotOnTheNet | Hogfather | Terry Pratchett
TheAlchemist | The Alchemist | Paulo Coelho
""")

add(T2, """
anthony_franco | How to Lie with Statistics | Darrell Huff
anthony_franco | 1984 | George Orwell
anthony_franco | How to Win Friends and Influence People | Dale Carnegie
elpakal | Guns, Germs and Steel | Jared Diamond
btkramer9 | Guns, Germs and Steel | Jared Diamond
elpakal | Europe and the People Without History | Eric Wolf
wooly_bully | Why the West Rules - For Now | Ian Morris
nikivi | Principles | Ray Dalio
MichaelEstes | Measure What Matters | John Doerr
RandomNick | The Ethics of Liberty | Murray Rothbard
nikivi | The Master and Margarita | Mikhail Bulgakov
Liquix | The Joyous Cosmology | Alan Watts
pretendscholar | The Master and Margarita | Mikhail Bulgakov
hangonhn | The Master and Margarita | Mikhail Bulgakov
yholio | The Undercover Economist | Tim Harford
yholio | The Long Tail | Chris Anderson
gglitch | A Thousand Plateaus | Deleuze & Guattari
gglitch | Finite and Infinite Games | James P. Carse
kvee | Harry Potter and the Methods of Rationality | Eliezer Yudkowsky
kvee | As a Man Thinketh | James Allen
ar1n | Brief Answers to the Big Questions | Stephen Hawking
pmoriarty | The Illuminatus! Trilogy | Shea & Wilson
jamesakirk | Cosmic Trigger | Robert Anton Wilson
jamesakirk | Prometheus Rising | Robert Anton Wilson
borski | The Design of Everyday Things | Don Norman
shadykiller | Why We Get Fat and What to Do About It | Gary Taubes
hackernews2 | Ender's Game | Orson Scott Card
erd0s | Thinking, Fast and Slow | Daniel Kahneman
Saturdays | The Design of Everyday Things | Don Norman
Saturdays | Educated | Tara Westover
Saturdays | The Glass Castle | Jeannette Walls
Saturdays | Why We Sleep | Matthew Walker
robotron | Zen and the Art of Motorcycle Maintenance | Robert M. Pirsig
afandian | Difficult Conversations | Stone, Patton & Heen
jaxbot | The Power Broker | Robert Caro
Simulacra | Atlas Shrugged | Ayn Rand
Simulacra | The Fountainhead | Ayn Rand
ndiscussion | The Selfish Gene | Richard Dawkins
fingerlocks | The Extended Phenotype | Richard Dawkins
""")

def key(t):
    t = t.lower().strip()
    t = re.sub(r"^(the|a|an)\s+", "", t)
    t = re.sub(r"[^a-z0-9 ]", "", t)
    return re.sub(r"\s+", " ", t)

agg = defaultdict(lambda: {"users": set(), "threads": set(), "title": "", "author": ""})
for tid, user, title, author in RAW:
    e = agg[key(title)]
    e["users"].add(user); e["threads"].add(tid)
    if len(title) > len(e["title"]): e["title"] = title
    if author and len(author) > len(e["author"]): e["author"] = author

rows = sorted(
    ({"title": v["title"], "author": v["author"],
      "mentions": len(v["users"]), "threads": sorted(v["threads"])} for v in agg.values()),
    key=lambda r: (-r["mentions"], r["title"].lower()),
)

out = {
 "threads": {
   T1: {"q":"What's one book that changed your life?","site":"Hacker News","year":2018,
        "points":214,"comments":176,"url":f"https://news.ycombinator.com/item?id={T1}"},
   T2: {"q":"What books changed the way you think about almost everything?","site":"Hacker News",
        "year":2019,"points":2009,"comments":1165,"url":f"https://news.ycombinator.com/item?id={T2}"},
 },
 "rows": rows,
}
json.dump(out, open("asked.json","w"), ensure_ascii=False, separators=(",",":"))
print(len(rows),"distinct books")
for r in rows[:12]:
    print(f'  {r["mentions"]}x  {r["title"]} — {r["author"]}')
