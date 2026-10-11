#!/usr/bin/env python3
"""KEXP — "Listeners' Favorite Songs of the '90s" (2026), all 540.

A canon, not a tally: KEXP's listeners voted ahead of the station's 2026 Fall
Fundraising Drive and KEXP published the ranking in six pages (540–500,
499–400, 399–300, 299–200, 199–100, 99–1). This keeps KEXP's order, #1 to #540.

Transcribed from those six pages. Spelling is tidied where the page has an
obvious typo or a house-style variant (REM → R.E.M., Bjork → Björk, "Little
Fluffly Clouds", "Set Adrfit", "Alanis Morisette", "Bone Thugz"); the FIXES
table below lists every change, so nothing is silently rewritten.

One entry KEXP's page itself gets wrong: #94, The Presidents of the United
States of America, has its title printed as "x". It stays in the list at #94
with the title marked unknown, and is left out of the Spotify CSV rather than
guessed.

Also writes the Spotify import CSV (Year,Artist,Track,Album; Year and Album
blank). Run from the repo root:

    python3 tools/kexp90s.py [path/to/kexp-90s.csv]
"""
import csv
import json
import re
import sys

PATH = "content/shelves.json"
SLUG = "kexp-listeners-favorite-songs-of-the-90s"
BASE = "https://www.kexp.org/countdowns/90s/"
PAGES = ["540-500", "499-400", "399-300", "299-200", "199-100", "99-1"]

RAW = """
540|Spiritualized|Ladies and Gentlemen We Are Floating in Space
539|Pearl Jam|Porch
538|R.E.M.|Crush With Eyeliner
537|Modest Mouse|Polar Opposites
536|Oasis|Morning Glory
535|Pavement|Grounded
534|Garbage|#1 Crush
533|Pixies|U-Mass
532|Depeche Mode|I Feel You
531|U2|The Fly
530|R.E.M.|Try Not to Breathe
529|A Tribe Called Quest|Excursions
528|The Chemical Brothers|Setting Sun
527|Soundgarden|Superunknown
526|Pearl Jam|Breath
525|Alice in Chains|Don't Follow
524|PJ Harvey|Dress
523|Hammerbox|When 3 Is 2
522|Tom Petty and the Heartbreakers|Learning to Fly
521|Paul Westerberg|Dyslexic Heart
520|Lenny Kravitz|Are You Gonna Go My Way
519|Lush|Ladykillers
518|Eminem|My Name Is
517|Whale|Hobo Humpin Slobo Babe
516|Pixies|Alec Eiffel
515|The Sugarcubes|Hit
514|R.E.M.|Shiny Happy People
513|The Sundays|Wild Horses
512|American Football|Never Meant
511|Weezer|In the Garage
510|The Roots|You Got Me (feat. Erykah Badu)
509|The Offspring|Come Out and Play
508|Boyz II Men|End of the Road
507|Blues Traveler|Hook
506|The Gits|Second Skin
505|Montell Jordan|This Is How We Do It
504|Blind Melon|Change
503|Collective Soul|Shine
502|Soul Coughing|Screenwriter's Blues
501|Elliott Smith|Needle in the Hay
500|Bad Religion|American Jesus
499|Bjork|Bachelorette
498|The Chemical Brothers|Let Forever Be
497|The Stone Roses|Love Spreads
496|Fatboy Slim|Right Here, Right Now
495|Son Volt|Windfall
494|My Bloody Valentine|When You Sleep
493|Cibo Matto|Sugar Water
492|Cracker|Teen Angst (What the World Needs Now)
491|Teenage Fanclub|The Concept
490|Fiona Apple|Paper Bag
489|The Magnetic Fields|Papa Was a Rodeo
488|The Flaming Lips|Race for the Prize
487|Dr. Dre|Still DRE
486|Sade|Kiss of Life
485|CAKE|I Will Survive
484|The Jayhawks|Blue
483|Us3|Cantaloop (Flip Fantasia)
482|Jane's Addiction|Classic Girl
481|Bran Van 3000|Drinking in L.A.
480|R.E.M.|Drive
479|Guided By Voices|Game of Pricks
478|Saint Etienne|Only Love Can Break Your Heart
477|The Notorious B.I.G.|Big Poppa
476|Belle and Sebastian|Get Me Away From Here, I'm Dying
475|Tori Amos|God
474|Depeche Mode|Halo
473|Prince|Gett Off
472|Annie Lennox|Why
471|Ministry|N.W.O.
470|Skee-Lo|I Wish
469|A Tribe Called Quest|Jazz (We've Got)
468|The Pharcyde|Runnin'
467|The Tragically Hip|Ahead by a Century
466|AIR|Sexy Boy
465|Queen Latifah|U.N.I.T.Y.
464|Silver Jews|Random Rules
463|The Smashing Pumpkins|Zero
462|Chapterhouse|Pearl
461|Green Day|Welcome to Paradise
460|Aphex Twin|Windowlicker
459|The Black Crowes|Remedy
458|Rancid|Ruby Soho
457|James|Sit Down
456|Paul Simon|The Obvious Child
455|Cocteau Twins|Iceblink Luck
454|King Missile|Detachable Penis
453|The Afghan Whigs|Gentlemen
452|Filter|Hey Man Nice Shot
451|Iggy Pop|Candy (feat. Kate Pierson)
450|Lush|De-Luxe
449|U2|Ultra Violet (Light My Way)
448|Depeche Mode|Walking in My Shoes
447|Big Audio Dynamite II|The Globe
446|Tom Petty|You Don't Know how it feels
445|Primus|Jerry Was a Race Car Driver
444|Tori Amos|Little Earthquakes
443|Nirvana|Lounge Act
442|A Tribe Called Quest|I Left My Wallet in El Segundo
441|Daft Punk|Da Funk
440|Prince & The New Power Generation|Cream
439|Buena Vista Social Club|Chan Chan
438|Sugar|A Good Idea
437|Midnight Oil|Blue Sky Mine
436|Faith No More|Midlife Crisis
435|The Cardigans|My Favourite Game
434|Nas|The World Is Yours
433|Built to Spill|Else
432|Mazzy Star|Into Dust
431|Hooverphonic|2Wicky
430|En Vogue|Free Your Mind
429|Fugees|Fu-Gee-La
428|Nirvana|Territorial Pissings
427|Cypress Hill|Insane in the Brain
426|Pavement|Range Life
425|Belle and Sebastian|The State I Am In
424|Built to Spill|Randy Described Eternity
423|Concrete Blonde|Bloodletting (The Vampire Song)
422|PJ Harvey|To Bring You My Love
421|Dinosaur Jr.|Start Choppin
420|Blur|Coffee & TV
419|PJ Harvey|Sheela-Na-Gig
418|Sinéad O'Connor|Black Boys on Mopeds
417|Nirvana|Where Did You Sleep Last Night?
416|Mazzy Star|Halah
415|Happy Mondays|Step On
414|Radiohead|Airbag
413|Hole|Celebrity Skin
412|Digital Underground|The Humpty Dance
411|Spin Doctors|Two Princes
410|Fugazi|Repeater
409|Radiohead|The Bends
408|Sonic Youth|Sugar Kane
407|Sheryl Crow|If It Makes You Happy
406|Rage Against the Machine|Bombtrack
405|Ben Folds Five|Brick
404|Prince|7
403|Bone Thugz-N-Harmony|Crossroads
402|Toad the Wet Sprocket|All I Want
401|Dinosaur Jr.|Out There
400|The Folk Implosion|Natural One
399|Alice in Chains|No Excuses
398|Nine Inch Nails|Wish
397|Enigma|Return to Innocence
396|Sleater-Kinney|One More Hour
395|Primal Scream|Loaded
394|The Verve|Lucky Man
393|Morphine|Thursday
392|Rancid|Time Bomb
391|Neutral Milk Hotel|Two-Headed Boy
390|The Smashing Pumpkins|Siva
389|Soul Coughing|Super Bon Bon
388|Lush|Sweetness and Light
387|Pearl Jam|Release
386|Beck|Debra
385|Dave Matthews Band|Crash Into Me
384|Nirvana|Aneurysm
383|Deftones|Be Quiet and Drive (Far Away)
382|Indigo Girls|Galileo
381|The Cure|High
380|Nick Cave and the Bad Seeds|Into My Arms
379|Neutral Milk Hotel|King Of Carrot Flowers Part 1
378|Placebo|Pure Morning
377|Seal|Crazy
376|Lucinda Williams|Car Wheels on a Gravel Road
375|The Jon Spencer Blues Explosion|Bellbottoms
374|Alice in Chains|Down in a Hole
373|The Offspring|Self Esteem
372|Ned's Atomic Dustbin|Kill Your Television
371|Sixpence None the Richer|Kiss Me
370|Ride|Leave Them All Behind
369|Tool|Sober
368|Björk|Hunter
367|Dinosaur Jr.|The Wagon
366|Blur|Tender
365|Ani DiFranco|32 Flavors
364|Soundgarden|Slaves & Bulldozers
363|Nirvana|Something in the Way
362|The Jesus and Mary Chain|Sometimes Always
361|Beck|The New Pollution
360|LIVE|Lightning Crashes
359|Hole|Miss World
358|En Vogue|My Lovin' (You're Never Gonna Get It)
357|Guns N' Roses|November Rain
356|Wu-Tang Clan|Protect Ya Neck
355|Red Hot Chili Peppers|Give It Away
354|Edwyn Collins|A Girl Like You
353|Sinéad O'Connor|The Last Day of Our Acquaintance
352|Pearl Jam|Given to Fly
351|Wilco|A Shot In The Arm
350|Meat Puppets|Backwater
349|DJ Shadow|Building Steam With A Grain of Salt
348|Duran Duran|Come Undone
347|The Smashing Pumpkins|Rhinoceros
346|Chris Cornell|Seasons
345|Radiohead|Subterranean Homesick Alien
344|Fatboy Slim|The Rockafeller Skank
343|Catherine Wheel|Crank
342|Pearl Jam|Daughter
341|Hole|Malibu
340|Nas|N.Y. State of Mind
339|Beastie Boys|Root Down
338|Morphine|Buena
337|Sonic Youth|100%
336|AIR|La Femme d'argent
335|Soundgarden|Blow Up the Outside World
334|House of Pain|Jump Around
333|Liz Phair|Never Said
332|Counting Crows|Round Here
331|Mobb Deep|Shook Ones, Part II
330|Alice in Chains|Them Bones
329|Built to Spill|The Plan
328|Pulp|Disco 2000
327|Pavement|Stereo
326|U2|Until the End of the World
325|Depeche Mode|World in My Eyes
324|Duran Duran|Ordinary World
323|Porno For Pyros|Pets
322|Björk|It's Oh So Quiet
321|EELS|Novocaine for the Soul
320|The Breeders|Divine Hammer
319|The Smashing Pumpkins|I Am One
318|Nada Surf|Popular
317|Len|Steal My Sunshine
316|The Afghan Whigs|Debonair
315|Weezer|Only in Dreams
314|Archers of Loaf|Web in Front
313|Nirvana|Breed
312|Beastie Boys|Get It Together
311|De La Soul|A Rollerskating Jam Named "Saturdays"
310|Nirvana|Drain You
309|PJ Harvey|50ft Queenie
308|Sublime|What I Got
307|The Cure|Burn
306|Björk|Jóga
305|Lauryn Hill|Everything Is Everything
304|Stereo MC's|Connected
303|TLC|Creep
302|Elastica|Stutter
301|Buffalo Tom|Taillights Fade
300|Screaming Trees|Dollar Bill
299|Pearl Jam|Rearviewmirror
298|Blur|There's No Other Way
297|Ace of Base|The Sign
296|OutKast|SpottieOttieDopaliscious
295|Janet Jackson|That's the Way Love Goes
294|Sade|No Ordinary Love
293|Everclear|Santa Monica
292|Jane's Addiction|Stop
291|Radiohead|Street Spirit (Fade Out)
290|Modest Mouse|Trailer Trash
289|Tori Amos|Silent All These Years
288|Tracy Chapman|Give Me One Reason
287|The Smashing Pumpkins|Hummer
286|Blur|Parklife
285|Beastie Boys|Pass the Mic
284|Jesus Jones|Right Here, Right Now
283|Green Day|Longview
282|Cornershop|Brimful of Asha
281|Weezer|My Name Is Jonas
280|Salt-N-Pepa|Shoop
279|The Wallflowers|One Headlight
278|Wilco|Via Chicago
277|Throwing Muses|Not Too Soon
276|Temple of the Dog|Say Hello 2 Heaven
275|Soundgarden|The Day I Tried to Live
274|Elliott Smith|Angeles
273|Pearl Jam|Better Man
272|Built to Spill|Car
271|Lauryn Hill|Ex-Factor
270|Seal|Kiss From a Rose
269|Depeche Mode|Policy of Truth
268|The Smashing Pumpkins|Bullet with Butterfly Wings
267|Soundgarden|Burden in My Hand
266|Liz Phair|Divorce Song
265|Whitney Houston|I Will Always Love You
264|Radiohead|Just
263|Stone Temple Pilots|Plush
262|The Flaming Lips|She Don't Use Jelly
261|Fiona Apple|Sleep to Dream
260|Sinéad O'Connor|The Emperor's New Clothes
259|Erykah Badu|On & On
258|Bush|Glycerine
257|Belle and Sebastian|The Boy With the Arab Strap
256|Slint|Good Morning, Captain
255|Jeff Buckley|Grace
254|Concrete Blonde|Joey
253|The Charlatans UK|The Only One I Know
252|Primitive Radio Gods|Standing Outside a Broken Phone Booth with Money in My Hand
251|Le Tigre|Deceptacon
250|The Notorious B.I.G.|Hypnotize
249|Snoop Doggy Dogg feat. Dat N***a Daz|Gin and Juice
248|Moby|Porcelain
247|Oasis|Supersonic
246|Mad Season|River of Deceit
245|Tom Petty|Wildflowers
244|Nirvana|The Man Who Sold the World
243|Green Day|When I Come Around
242|Nick Cave and the Bad Seeds|Red Right Hand
241|Britney Spears|...Baby One More Time
240|Slowdive|When the Sun Hits
239|Guided By Voices|I Am a Scientist
238|Mariah Carey|Fantasy
237|The Prodigy|Breathe
236|Fiona Apple|Shadowboxer
235|The Cure|A Letter to Elise
234|Fatboy Slim|Praise You
233|Morphine|Cure for Pain
232|Pearl Jam|Elderly Woman Behind the Counter in a Small Town
231|Depeche Mode|Personal Jesus
230|Cracker|Low
229|The Lemonheads|It's a Shame About Ray
228|Blackstreet|No Diggity
227|A Tribe Called Quest|Check the Rhime
226|David Bowie|I'm Afraid of Americans
225|Liz Phair|6'1
224|Beck|Devil's Haircut
223|Sugar|If I Can't Change Your Mind
222|The Prodigy|Firestarter
221|Sarah McLachlan|Possession
220|Helmet|Unsung
219|Portishead|Roads
218|A Tribe Called Quest|Electric Relaxation
217|The Smashing Pumpkins|Drown
216|The Cure|From the Edge of the Deep Green Sea
215|Sugar|Hoover Damn
214|James|Sometimes
213|Siouxsie and the Banshees|Kiss Them For Me
212|Soundgarden|Spoonman
211|REM|Everybody Hurts
210|Ministry|Jesus Built My Hotrod
209|The La's|There She Goes
208|Pixies|Dig For Fire
207|Yo La Tengo|Autumn Sweater
206|Radiohead|No Surprises
205|Alanis Morisette|Hand in My Pocket
204|Radiohead|Exit Music (for a Film)
203|The Orb|Little Fluffly Clouds
202|Pavement|Cut Your Hair
201|Elliott Smith|Between the Bars
200|The Smashing Pumpkins|Disarm
199|The Chemical Brothers|Block Rockin' Beats
198|Neutral Milk Hotel|Holland, 1945
197|The Pharcyde|Passin' Me By
196|DJ Shadow|Midnight in a Perfect World
195|Soundgarden|Fell on Black Days
194|Pearl Jam|Corduroy
193|Oasis|Live Forever
192|The Smashing Pumpkins|Tonight, Tonight
191|A Tribe Called Quest|Award Tour
190|R.E.M.|What's the Frequency, Kenneth?
189|Jeff Buckley|Lover, You Should've Come Over
188|Lisa Loeb & Nine Stories|Stay (I Missed You)
187|Outkast|Rosa Parks
186|Neil Young|Harvest Moon
185|The Notorious B.I.G.|Juicy
184|Cocteau Twins|Cherry-Coloured Funk
183|Bjork|Big Time Sensuality
182|No Doubt|Don't Speak
181|Sleater-Kinney|Dig Me Out
180|Matthew Sweet|Girlfriend
179|Gin Blossoms|Hey Jealousy
178|Radiohead|High and Dry
177|Pearl Jam|State of Love and Trust
176|Souls of Mischief|93 'til Infinity
175|Alice in Chains|Man in the Box
174|TLC|No Scrubs
173|Pixies|Velouria
172|Chumbawamba|Tubthumping
171|Mark Morrison|Return of the Mack
170|Nine Inch Nails|March of the Pigs
169|10,000 Maniacs|These Are the Days
168|REM|Man on the Moon
167|Liz Phair|Fuck and Run
166|Hole|Doll Parts
165|Massive Attack|Protection
164|Arrested Development|Tennessee
163|Warren G|Regulate
162|Everything But the Girl|Missing (Todd Terry Club Mix)
161|Liz Phair|Supernova
160|Alice in Chains|Rooster
159|Blur|Girls & Boys
158|Jeff Buckley|Hallelujah
157|Spice Girls|Wannabe
156|Fugees|Ready or Not
155|Weezer|Buddy Holly
154|Tom Waits|I Don't Want To Grow Up
153|My Bloody Valentine|Soon
152|Sublime|Santeria
151|Spacehog|In the Meantime
150|Pearl Jam|Yellow Ledbetter
149|Tori Amos|Crucify
148|U2|Mysterious Ways
147|L7|Pretend We're Dead
146|Veruca Salt|Seether
145|Soundgarden|Outshined
144|LL Cool J|Mama Said Knock You Out
143|Jamiroquai|Virtual Insanity
142|Sir Mix-A-Lot|Baby Got Back
141|The Beta Band|Dry the Rain
140|Orbital|Halcyon + On + On
139|Massive Attack|Unfinished Sympathy
138|Coolio|Gangsta's Paradise
137|Garbage|Stupid Girl
136|Missy Elliott|The Rain (Supa Dupa Fly)
135|Tricky|Black Steel
134|P.M. Dawn|Set Adrfit on Memory Bliss
133|No Doubt|Just a Girl
132|Madonna|Vogue
131|Counting Crows|Mr. Jones
130|Alice in Chains|Nutshell
129|2Pac Feat. Dr Dre|California Love
128|Butthole Surfers|Pepper
127|Stone Temple Pilots|Interstate Love Song
126|Ned's Atomic Dustbin|Grey Cell Green
125|Dr. Dre|Nuthin' But a "G" Thang
124|Elastica|Connection
123|Dinosaur Jr.|Feel the Pain
122|Alanis Morissette|Ironic
121|Billy Bragg & Wilco|California Stars
120|New Order|Regret
119|Third Eye Blind|Semi-Charmed Life
118|Pavement|Gold Soundz
117|Luscious Jackson|Naked Eye
116|PJ Harvey|Rid of Me
115|Oasis|Champagne Supernova
114|Pearl Jam|Jeremy
113|4 Non Blondes|What's Up
112|Metallica|Enter Sandman
111|Neutral Milk Hotel|In the Aeroplane Over the Sea
110|Portishead|Wandering Star
109|Red Hot Chili Peppers|Under the Bridge
108|Ride|Vapour Trail
107|Nirvana|In Bloom
106|Nine Inch Nails|Hurt
105|Madonna|Ray of Light
104|Belly|Feed the Tree
103|Massive Attack|Angel
102|Cocteau Twins|Heaven or Las Vegas
101|Ice Cube|It Was a Good Day
100|Rage Against the Machine|Bulls On Parade
99|Jeff Buckley|Last Goodbye
98|Jane's Addiction|Been Caught Stealing
97|Sonic Youth|Kool Thing
96|Sunny Day Real Estate|In Circles
95|Cake|The Distance
94|Presidents of the United States of America|x
93|Nirvana|All Apologies
92|Modest Mouse|Dramamine
91|Soundgarden|Jesus Christ Pose
90|Beastie Boys|Sure Shot
89|Pavement|Summer Babe (Winter Version)
88|Beastie Boys|Intergalactic
87|Green Day|Basket Case
86|Beck|Where It's At
85|Public Enemy|Fight the Power
84|Elliott Smith|Waltz #2 (XO)
83|A Tribe Called Quest|Scenario
82|Soundgarden|Rusty Cage
81|Pearl Jam|Even Flow
80|Fugees|Killing Me Softly
79|They Might Be Giants|Birdhouse in Your Soul
78|Weezer|Undone (The Sweater Song)
77|The Cardigans|Lovefool
76|TLC|Waterfalls
75|Toadies|Possum Kingdom
74|Daft Punk|Around the World
73|Digable Planets|Rebirth of Slick (Cool Like Dat)
72|Blur|Song 2
71|Catherine Wheel|Black Metallic
70|The Smashing Pumpkins|Cherub Rock
69|Oasis|Don't Look Back In Anger
68|Wu-Tang Clan|C.R.E.A.M.
67|Bjork|Human Behaviour
66|The Smashing Pumpkins|Today
65|Weezer|Say it Ain't So
64|Jane's Addiction|Three Days
63|Nirvana|Heart-Shaped Box
62|Garbage|Only Happy When it Rains
61|Sneaker Pimps|6 Underground
60|New Radicals|You Get What You Give
59|Tori Amos|Cornflake Girl
58|Built to Spill|Carry the Zero
57|Temple of the Dog|Hunger Strike
56|Nirvana|Come as You Are
55|The Sundays|Here's Where the Story Ends
54|Harvey Danger|Flagpole Sitta
53|My Bloody Valentine|Only Shallow
52|Nirvana|Lithium
51|A Tribe Called Quest|Can I Kick It?
50|The Smashing Pumpkins|Mayonaise
49|George Michael|Freedom 90
48|PJ Harvey|Down by the Water
47|Screaming Trees|Nearly Lost You
46|Lauryn Hill|Doo Wop (That Thing)
45|Bjork|Hyperballad
44|James|Laid
43|Beastie Boys|So What'cha Want
42|Underworld|Born Slippy (Nuxx)
41|U2|One
40|Foo Fighters|Everlong
39|Portishead|Sour Times
38|Hum|Stars
37|The Cure|Friday I'm In Love
36|Hole|Violet
35|Radiohead|Karma Police
34|Radiohead|Let Down
33|Bjork|Army of Me
32|Alice in Chains|Would?
31|Radiohead|Fake Plastic Trees
30|The Cranberries|Linger
29|Bikini Kill|Rebel Girl
28|Sinead O Connor|Nothing Compares 2 U
27|Blind Melon|No Rain
26|Fiona Apple|Criminal
25|The Cranberries|Dreams
24|REM|Nightswimming
23|Pearl Jam|Alive
22|Oasis|Wonderwall
21|Pulp|Common People
20|The Smashing Pumpkins|1979
19|Rage Against the Machine|Killing in the Name Of
18|The Cranberries|Zombie
17|Alanis Morissette|You Oughta Know
16|Portishead|Glory Box
15|REM|Losing My Religion
14|Pearl Jam|Black
13|The Verve|Bitter Sweet Symphony
12|Nine Inch Nails|Closer
11|Depeche Mode|Enjoy the Silence
10|Beck|Loser
9|Soundgarden|Black Hole Sun
8|Radiohead|Creep
7|Deee-Lite|Groove is in the Heart
6|Massive Attack|Teardrop
5|Radiohead|Paranoid Android
4|The Breeders|Cannonball
3|Beastie Boys|Sabotage
2|Mazzy Star|Fade Into You
1|Nirvana|Smells Like Teen Spirit
"""

# Every change from KEXP's printed text, and why.
ARTIST_FIX = {
    "REM": "R.E.M.",                                   # house style varies across pages
    "Bjork": "Björk",
    "Sinead O Connor": "Sinéad O'Connor",
    "Alanis Morisette": "Alanis Morissette",
    "Bone Thugz-N-Harmony": "Bone Thugs-N-Harmony",
    "Outkast": "OutKast",
    "CAKE": "Cake",
    "Guided By Voices": "Guided by Voices",
    "Presidents of the United States of America": "The Presidents of the United States of America",
    "Snoop Doggy Dogg feat. Dat N***a Daz": "Snoop Doggy Dogg",   # censored guest credit dropped
    "2Pac Feat. Dr Dre": "2Pac feat. Dr. Dre",
}
TITLE_FIX = {
    "Little Fluffly Clouds": "Little Fluffy Clouds",
    "Set Adrfit on Memory Bliss": "Set Adrift on Memory Bliss",
    "Hoover Damn": "Hoover Dam",
    "Crossroads": "Tha Crossroads",
    "These Are the Days": "These Are Days",
    "Freedom 90": "Freedom! '90",
    "6'1": "6'1\"",
    "You Don't Know how it feels": "You Don't Know How It Feels",
    "Say it Ain't So": "Say It Ain't So",
    "Only Happy When it Rains": "Only Happy When It Rains",
    "Groove is in the Heart": "Groove Is in the Heart",
    "Friday I'm In Love": "Friday I'm in Love",
    "x": "",                                           # KEXP's page prints "x" for #94
}

S = []
for line in RAW.strip().splitlines():
    r, a, t = line.split("|")
    S.append((int(r), ARTIST_FIX.get(a, a), TITLE_FIX.get(t, t)))
S.sort()
assert [r for r, *_ in S] == list(range(1, 541)), "ranks must run 1..540 with no gaps"


def page_for(rank):
    for p in PAGES:
        hi, lo = map(int, p.split("-"))
        if lo <= rank <= hi:
            return BASE + p + "/"


def lead_artist(a):
    return re.split(r"\s+feat\.\s+", a, flags=re.I)[0]


def search_title(t):
    return re.sub(r"\s*\((feat\.|Todd Terry)[^)]*\)", "", t).strip()


rows = []
for r, a, t in S:
    row = {
        "key": f"kexp90|{r}",
        "lead": f"#{r}",
        "sec": a,
        "pri": t or "(title missing on KEXP's page)",
        "src": {"label": "KEXP", "url": page_for(r)},
    }
    if t:
        row["yt"] = f"{search_title(t)} {lead_artist(a)}"
        row["ytWord"] = "Listen"
    rows.append(row)

LIST = {
    "slug": SLUG,
    "title": "KEXP Listeners' Favorite Songs of the '90s",
    "kind": "Canon",
    "verb": "heard",
    "noTick": True,
    "desc": ("Seattle&rsquo;s KEXP asked its listeners, and 540 songs came back. Nirvana at #1, of course; "
             "Mazzy Star at #2, which is the more KEXP answer."),
    "cols": ["Rank", "Artist", "Song", "Listen · source"],
    "srcLabel": "Voted in",
    "sources": [{"url": BASE + "99-1/", "label": "KEXP",
                 "q": "Listeners' Favorite Songs of the '90s",
                 "meta": "2026 · listener vote · 540 songs"}],
    "note": ("A canon, not a tally: KEXP&rsquo;s listeners voted ahead of the station&rsquo;s 2026 fall "
             "fund drive, and the list keeps KEXP&rsquo;s order, #1 to #540. Each row&rsquo;s source link "
             "goes to the KEXP page that holds it. Spellings are tidied where the page has a typo or switches "
             "style between pages (REM and R.E.M., Bjork and Björk); every change is listed in the script. "
             "One entry KEXP&rsquo;s own page gets wrong: #94, The Presidents of the United States of America, "
             "has its title printed as &ldquo;x&rdquo;, so it&rsquo;s marked missing here rather than guessed. "
             "Read it next to <em>Paste&rsquo;s</em> critics&rsquo; 100 for the same decade: 45 songs make both "
             "lists, but rarely in the same place. Paste&rsquo;s #1, <em>C.R.E.A.M.</em>, is #68 here; its #3, "
             "Silver Jews&rsquo; <em>Random Rules</em>, is #464. Going the other way, a Seattle station&rsquo;s "
             "listeners put Pearl Jam in the top 200 seven times, and Soundgarden five."),
    "rows": rows,
}

if __name__ == "__main__":
    shelves = json.load(open(PATH))
    music = [s for s in shelves if s["slug"] == "music"][0]
    old = [l for l in music["lists"] if l["slug"] == SLUG]
    if old and "action" in old[0]:
        LIST["action"] = old[0]["action"]          # keep the playlist link on re-runs
    music["lists"] = [l for l in music["lists"] if l["slug"] != SLUG] + [LIST]
    open(PATH, "w").write(json.dumps(shelves, ensure_ascii=False, indent=1))

    out = sys.argv[1] if len(sys.argv) > 1 else "kexp-90s.csv"
    n = 0
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["Year", "Artist", "Track", "Album"])
        for r, a, t in S:
            if t:
                w.writerow(["", lead_artist(a), search_title(t), ""])
                n += 1
    print(len(rows), "songs →", PATH, ";", n, "tracks →", out)
