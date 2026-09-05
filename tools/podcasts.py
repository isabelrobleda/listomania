# -*- coding: utf-8 -*-
import re, json, collections

EXTRA = [
 ("Someone Knows Something","David Ridgen"),("Stuff They Don't Want You to Know","iHeart"),
 ("Pretend","Javier Leiva"),("Something You Should Know","Mike Carruthers"),
 ("Dear Hank & John","Hank & John Green"),("The Rich Roll Podcast","Rich Roll"),
 ("On Brand","Jon & Marisa"),("Kill List","Carl Miller"),("The Louis Theroux Podcast","Louis Theroux"),
 ("Full Disclosure","James O'Brien"),("To Live and Die in LA","Neil Strauss"),
 ("A Mediocre Time with Tom and Dan","Tom & Dan"),("Attitudes!","Bryan Safi & Erin Gibson"),
 ("The Polybius Conspiracy",""),("The Infinite Monkey Cage","Brian Cox & Robin Ince"),
 ("What Now?","Trevor Noah"),("Strangers on a Bench","Tom Rosenthal"),
 ("Why'd You Push That Button?","The Verge"),("Humble and Fred",""),
 ("Conversations","ABC"),("Parenting Hell","Rob Beckett & Josh Widdicombe"),
 ("The Dr. John Delony Show","John Delony"),("We're Alive","Kc Wayland"),
 ("Pablo Torre Finds Out","Pablo Torre"),("Sherlock & Co.",""),
 ("I Hate It But I Love It",""),("Puttin' On Airs","Trae Crowder & Corey Ryan Forrester"),
 ("Midnight Facts for Insomniacs",""),("How to Destroy Everything","Ian Bagg"),
 ("Well There's Your Problem",""),("Vibe Check",""),("Guys: A Podcast About Guys",""),
 ("Persona: The French Deception",""),("Regulate & Rewire","Amanda Armstrong"),
 ("After Dark","History Hit"),("CounterSpin","FAIR"),("Distractible","Markiplier"),
 ("Cover to Cover","Chris Franjola"),("All-In Podcast",""),("Search Engine","PJ Vogt"),
 ("Hyperfixed","Alex Goldman"),("Your Stupid Opinions",""),("Never Seen It","Kyle Ayers"),
 ("Two Girls One Ghost",""),("Otherworld","Jack Wagner"),
 ("The Ongoing History of New Music","Alan Cross"),("Garbage in My Heart",""),
 ("R U Talkin' R.E.M. Re: Me?","Adam Scott & Scott Aukerman"),("BeerBiceps","Ranveer Allahbadia"),
 ("Girls Gotta Eat",""),("The Virtual Memories Show","Gil Roth"),("Thumb Cramps",""),
 ("Mostly Murder",""),("Dakota Spotlight","James Wolner"),("Permanent Record","Edward Snowden"),
 ("It Means What It Means",""),("Knifepoint Horror","Soren Narnia"),("The Spy Who","Wondery"),
 ("Invisible Choir",""),("Murder in America",""),("The Minds of Madness",""),
 ("Jim Harold's Campfire","Jim Harold"),("The Prof G Pod","Scott Galloway"),
 ("Ephemeral",""),("Literature and History","Doug Metzger"),("Talking@theMovies",""),
 ("Authentically Imperfect",""),("Why America","Leigh Miller"),("Wiki Featured",""),
 ("Revolutionary Left Radio",""),("The Opportunist",""),("Revisionist History","Malcolm Gladwell"),
 ("Smart Mouth",""),("Sold a Story","Emily Hanford"),("The Dream",""),
 ("Case 63",""),("SportSense",""),("The Girl God Experience",""),
 ("Crime in Sport",""),("Uhh Yeah Dude",""),("Fartcast",""),("Threedom",""),
 ("The Telepathy Tapes","Ky Dickens"),("Comedy Bang Bang","Scott Aukerman"),
 ("Bear Brook",""),("Limetown",""),("Wooden Overcoats",""),("Normal Gossip",""),
 ("Hunting Warhead",""),("Science Vs","Wendy Zukerman"),("How Did This Get Made",""),
 ("Up and Vanished","Payne Lindsey"),("The Vanished",""),("Swindled",""),
 ("Darknet Diaries","Jack Rhysider"),("Mission to Zyxx",""),("Flightless Bird","David Farrier"),
 ("Citation Needed",""),("Hard Fork","The New York Times"),("Rotten Mango","Stephanie Soo"),
 ("The Basement Yard",""),("Gangster Capitalism",""),("This Is Actually Happening","Whit Missildine"),
 ("Where Should We Begin","Esther Perel"),("Pivot","Kara Swisher & Scott Galloway"),
]

BASE = json.load(open('/tmp/podcnt.json'))
CANON = {}
for n in BASE: CANON[n] = ""
AUTH = {}
for n, a in EXTRA: AUTH[n] = a
AUTHORS = {
 "Heavyweight":"Jonathan Goldstein","The History of English Podcast":"Kevin Stroud",
 "This American Life":"Ira Glass","S-Town":"Brian Reed","Conan O'Brien Needs a Friend":"Conan O'Brien",
 "The Skeptics' Guide to the Universe":"Steven Novella","Serial":"Sarah Koenig",
 "A History of Rock Music in 500 Songs":"Andrew Hickey","Hardcore History":"Dan Carlin",
 "Ologies":"Alie Ward","In the Dark":"Madeleine Baran","Reply All":"PJ Vogt & Alex Goldman",
 "My Dad Wrote a Porno":"Jamie Morton","Planet Money":"NPR","Sawbones":"Justin & Sydnee McElroy",
 "Ear Hustle":"Earlonne Woods & Nigel Poor","Stuff You Should Know":"Josh Clark & Chuck Bryant",
 "In Our Time":"Melvyn Bragg","99% Invisible":"Roman Mars","The Memory Palace":"Nate DiMeo",
 "Criminal":"Phoebe Judge","Everything Is Alive":"Ian Chillag","The Anthropocene Reviewed":"John Green",
 "Revolutions":"Mike Duncan","The History of Rome":"Mike Duncan","Behind the Bastards":"Robert Evans",
 "The Dollop":"Dave Anthony & Gareth Reynolds","Fall of Civilizations":"Paul Cooper",
 "Kill Tony":"Tony Hinchcliffe","Smartless":"Bateman, Arnett & Hayes",
 "My Favorite Murder":"Kilgariff & Hardstark","Crime Junkie":"Ashley Flowers",
 "Mr. Ballen":"John Allen","Levar Burton Reads":"LeVar Burton","Philosophize This!":"Stephen West",
 "American Scandal":"Lindsay Graham","Tooth & Claw":"Wes Larson","Valley Heat":"Doug Duguay",
 "The Rest Is History":"Holland & Sandbrook","Snap Judgment":"Glynn Washington",
 "Heaven's Gate":"Glynn Washington","Mystery Show":"Starlee Kine","Blowback":"James & Kulwin",
 "Beautiful Anonymous":"Chris Gethard","You're Wrong About":"Sarah Marshall","The Daily":"The New York Times",
 "No Such Thing as a Fish":"QI Elves","Your Own Backyard":"Chris Lambert",
 "Small Town Murder":"Whisman & Pietragallo","Knowledge Fight":"Dan & Jordan",
 "Dead Eyes":"Connor Ratliff","Twenty Thousand Hertz":"Dallas Taylor","Sword and Scale":"Mike Boudet",
 "Scam Goddess":"Laci Mosley","My Brother, My Brother and Me":"The McElroys",
 "Something Was Wrong":"Tiffany Reese","Somebody Knows Something":"David Ridgen",
 "The Magnus Archives":"Jonathan Sims","Cold":"Dave Cawley","Cautionary Tales":"Tim Harford",
 "The Constant":"Mark Chrisler","You Must Remember This":"Karina Longworth","Life Kit":"NPR",
 "The Omnibus":"Ken Jennings & John Roderick","We Can Do Hard Things":"Glennon Doyle",
 "Missing and Murdered":"Connie Walker","The Wonder of Stevie":"Wesley Morris",
 "Huberman Lab":"Andrew Huberman","The Diary of a CEO":"Steven Bartlett",
 "Bill Burr's Monday Morning Podcast":"Bill Burr","Nothing Much Happens":"Kathryn Nicolai",
 "The Joe Rogan Experience":"Joe Rogan","Making Sense":"Sam Harris","On the Media":"WNYC",
 "The Great Simplification":"Nate Hagens","Betwixt the Sheets":"Kate Lister","Risk!":"Kevin Allison",
 "Short History Of...":"","The Moth":"","The Silt Verses":"","Doughboys":"",
 "Three Bean Salad":"","The History Chicks":"","What Went Wrong":"","Root of Evil":"",
 "Cumtown":"","Pod Save America":"","SRSLY Wrong":"","We Hate Movies":"","Toni and Ryan":"",
 "It Could Happen Here":"","Sherlock & Co.":"",
}
AUTHORS.update(AUTH)

TITLES = sorted(set(list(BASE.keys()) + [n for n, _ in EXTRA]), key=len, reverse=True)

def pat(n):
    return re.escape(n).replace("\\ ", r"[\s]+").replace("'", "['’]?").replace("\\.\\.\\.", "")

RX = [(n, re.compile(pat(n), re.I)) for n in TITLES]

def find(b):
    for n, r in RX:
        if r.search(b):
            return n
    return None

rows = [l.rstrip("\n").split("\t", 2) for l in open('/tmp/pods.tsv') if l.count("\t") >= 2]

# Walk in thread order. A comment that names a show is an answer. A comment that
# names nothing is read as an endorsement of the answer above it — which is what
# it is, in a thread where the replies are all "came here to say this".
# An endorsement has to *refer* to something — "this", "it", "same", "agree".
# Requiring that is what stops a run of unmatched one-line answers at the tail of
# the thread being swept up as votes for whichever show happened to come before
# them, which is exactly what the first version of this did.
ENDORSE = re.compile(r"\b(this|that|it['’]?s|it |same|agree|second(ing)?|came here|"
                     r"love it|so good|yes+|ditto|too\b|his |her |their |the host|"
                     r"episode|listen(ed|ing)? to (it|this)|👍|💯)", re.I)
DROP = re.compile(r"^(what|why|how|is |are |does |did |who |where |when |\?)|"
                  r"downvot|racist|don't get|didn.t|couldn.t get|not for me|gave up|"
                  r"overrated|problematic|misleading|hate |worst", re.I)

votes = collections.defaultdict(set)
cur, since = None, 0
# Endorsements only count close to their answer. Reddit's flat text loses the
# indentation, so distance is the only handle left on "is this a reply or just
# the next answer down" — and past about ten lines it is always the latter.
for u, p, b in rows:
    since += 1
    n = find(b)
    if n:
        # Only an answer that actually drew a crowd can collect endorsements.
        # A one-point answer at the bottom of the thread has no reply chain, so
        # anything following it is somebody else's reply, not agreement with it.
        cur, since = (n if int(p) >= 5 else None), 0
        votes[n].add(u)
    elif cur and since <= 10 and ENDORSE.search(b) and not DROP.search(b) and len(b) < 300:
        votes[cur].add(u)

D = [(n, AUTHORS.get(n, ""), len(v)) for n, v in votes.items() if v]
D.sort(key=lambda r: (-r[2], r[0].lower()))
print(len(D), "podcasts;", sum(x[2] for x in D), "endorsements")
for n, a, c in D[:25]:
    print(f"{c:4} {n}")
json.dump(D, open('/tmp/podrows.json', 'w'), ensure_ascii=False)
