#!/usr/bin/env python3
"""KEXP — "Top Songs of All Time" (2017), all 631.

A canon, not a tally — and not a vote either. KEXP's page says it counted
these down during its 2017 Fall Fundraising Drive "ranked by amount of
airplay": the songs the station itself played most. That makes it a portrait
of KEXP's DJs over the years rather than of its listeners (compare the '90s
countdown, which listeners voted on).

Transcribed from the single countdown page. Spelling is tidied where the page
has a typo or switches style ("Siouxsie and The Bashees", "TImebomb", AIR/Air,
Stereo MCs); every change is in the FIXES tables below.

Also writes the Spotify import CSV (Year,Artist,Track,Album; Year and Album
blank). Run from the repo root:

    python3 tools/kexp_alltime.py [path/to/kexp-all-time.csv]
"""
import csv
import json
import re
import sys

PATH = "content/shelves.json"
SLUG = "kexp-top-songs-of-all-time"
URL = "https://www.kexp.org/countdowns/kexp-top-songs-of-all-time-countdown/"

RAW = """
631|The Waterboys|This Is the Sea
630|Violent Femmes|Blister In The Sun
629|Urban Dance Squad|Deeper Shade of Soul
628|The New Pornographers|The Laws Have Changed
627|The House of Love|I Don't Know Why I Love You
626|Elastica|Connection
625|Modest Mouse|Polar Opposites
624|The Heavy|How You Like Me Now?
623|The Clash|The Guns of Brixton
622|Sufjan Stevens|Chicago
621|Radiohead|Weird Fishes/Arpeggi
620|Morphine|Buena
619|Ladytron|Ghosts
618|Jurassic 5|A Day at the Races
617|Frank Black|Los Angeles
616|Fleet Foxes|Mykonos
615|Elbow|Station Approach
614|Django Django|Hail Bop
613|Cat Power|Cross Bones Style
612|Yeah Yeah Yeahs|Hysteric
611|X|I Must Not Think Bad Thoughts
610|Washed Out|Feel It All Around
609|Pixies|La La Love You
608|Maps|So Low, So High
607|Lou Reed|Vicious
606|Sleater-Kinney|Oh!
605|Kinski|Newport
604|Foals|Inhaler
603|DOM|Living In America
602|Digable Planets|Where I'm From
601|The Wedding Present|Interstate 5 (extended version)
600|The Sleepy Jackson|Good Dancers
599|Beck|Dreams
598|The Lemonheads|It's A Shame About Ray
597|Spoon|Everything Hits at Once
596|The Dismemberment Plan|You Are Invited
595|Sparklehorse|Piano Fire
594|Soundgarden|Hands All Over
593|Okkervil River|Black
592|Local Natives|Sun Hands
591|Junius Meyvant|Color Decay
590|Cat Power|Cherokee
589|The Jayhawks|Waiting For The Sun
588|Hoodoo Gurus|I Want You Back
587|Guided By Voices|Glad Girls
586|Goldfrapp|Strict Machine
585|Catherine Wheel|I Want to Touch You
584|Built to Spill|Big Dipper
583|Austra|Beat and The Pulse
582|Portishead|Machine Gun
581|Archie Bronson Outfit|Cherry Lips
580|Siouxsie and The Bashees|Kiss Them For Me
579|Ice Cube|It Was A Good Day
578|The Cure|In Between Days
577|The Posies|Dream All Day
576|MC Solaar|Nouveau Western
575|Jónsi|Go Do
574|The Smiths|There is a Light That Never Goes Out
573|The Raveonettes|Aly, Walk With Me
572|Björk|Army of Me
571|TV on the Radio|New Health Rock
570|Grandaddy|Now It's On
569|Passion Pit|The Reeling
568|Modest Mouse|Dashboard
567|Her Space Holiday|Sleepy California
566|The Cure|A Forest
565|Gorillaz|Clint Eastwood
564|Ghostland Observatory|Piano Man
563|Cat Power|Nude as the News
562|Jeff Buckley|Grace
561|Wolf Parade|Language City
560|They Might Be Giants|Ana Ng
559|Sonic Youth|Incinerate
558|PJ Harvey|We Float
557|Warpaint|Undertow
556|Pickwick|The Round
555|Out Hud|It's for You
554|Jeff Buckley|So Real
553|Deep Sea Diver|Secrets
552|The Cure|Pictures of You
551|David Bowie|Queen Bitch
550|Arcade Fire|Ready to Start
549|The Smiths|Ask
548|Sons and Daughters|Dance Me In
547|The Orwells|The Righteous One
546|Nada Surf|When I Was Young
545|The Magnetic Fields|Papa Was A Rodeo
544|Talking Heads|Born Under Punches (The Heat Goes On)
543|Gorillaz|DARE
542|Gnarls Barkley|Crazy
541|Crooked Fingers|Call To Love
540|Television|Marquee Moon
539|Common Market|Connect For
538|Blur|There's No Other Way
537|Matt & Kim|Daylight
536|Beirut|Santa Fe
535|New Order|Your Silent Face
534|Arcade Fire|The Suburbs
533|Washed Out|It All Feels Right
532|The Smiths|This Charming Man
531|Neko Case|Star Witness
530|Gang of Four|What We All Want
529|Death Cab for Cutie|The New Year
528|Unknown Mortal Orchestra|Multi-Love
527|The Dutchess & the Duke|Reservoir Park
526|Radiohead|Pyramid Song
525|The Halo Benders|Virginia Reel Around the Fountain
524|Shawn Smith|Wrapped In My Memory
523|Massive Attack|Paradise Circus
522|TV On The Radio|Trouble
521|Washed Out|Amor Fati
520|UNKLE|In A State
519|A Tribe Called Quest|Check the Rhime
518|Looper|Mondo '77
517|Sky Cries Mary|Moonbathing
516|The Shins|Know Your Onion!
515|The Magnetic Fields|I Think I Need A New Heart
514|Rogue Wave|Bird on a Wire
513|Nirvana|School
512|Art Brut|Good Weekend
511|Voom Blooms|Thoughts of Rena
510|Throwing Muses|Bright Yellow Gun
509|Blur|Coffee & TV
508|Shuggie Otis|Inspiration Information
507|M83|Graveyard Girl
506|The Shins|Turn on Me
505|My Morning Jacket|Lay Low
504|Cold War Kids|Tell Me in the Morning
503|Tame Impala|Feels Like We Only Go Backwards
502|Parquet Courts|Stoned And Starving
501|The Smiths|Bigmouth Strikes Again
500|The Cure|Boys Don't Cry
499|Joseph Arthur|Even Tho
498|Pulp|Common People
497|alt-J|Hunger of the Pine
496|Vampire Weekend|The Kids Don't Stand a Chance
495|Liz Phair|Never Said
494|Metric|Help I'm Alive
493|Cloud Cult|Living on the Outside of Your Skin
492|The Modern Lovers|Roadrunner
491|Clap Your Hands Say Yeah|Upon This Tidal Wave of Young Blood
490|The Velvet Underground|I'm Waiting for the Man
489|Tones on Tail|Go!
488|Grizzly Bear|Two Weeks
487|Blitzen Trapper|Furr
486|The Shins|Australia
485|AIR|Run
484|Phoenix|1901
483|Fitz and The Tantrums|Breakin' The Chains of Love
482|Rocky Votolato|White Daisy Passing
481|Seachange|Glitterball
480|Ratatat|Wildcat
479|Yo La Tengo|Autumn Sweater
478|The Strokes|Someday
477|The La's|There She Goes
476|The Clash|Should I Stay or Should I Go
475|The Buzzcocks|What Do I Get?
474|Morrissey|Everyday Is Like Sunday
473|Interpol|Slow Hands
472|Black Rebel Motorcycle Club|Stop
471|Yeah Yeah Yeahs|Date With the Night
470|Woods|Moving to the Left
469|The Long Winters|Stupid
468|Ted Leo and the Pharmacists|Me and Mia
467|Sharon Jones and the Dap-Kings|100 Days, 100 Nights
466|PJ Harvey|Good Fortune
465|Peter Bjorn and John|Up Against the Wall
464|MGMT|Time to Pretend
463|Elliott Smith|Waltz #1
462|Japandroids|Young Hearts Spark Fire
461|Django Django|Default
460|Arcade Fire|Keep the Car Running
459|The White Stripes|Blue Orchid
458|The Smiths|What Difference Does It Make?
457|The Damnwells|sleepsinging
456|Sunny Day Real Estate|Seven
455|Interpol|NYC
454|Harvey Danger|Little Round Mirrors
453|Brian Eno|Baby's On Fire
452|Deerhunter|Snakeskin
451|Aesop Rock|None Shall Pass
450|XTC|Senses Working Overtime
449|The Helio Sequence|Harmonica Song
448|The Black Angels|Manipulation
447|The Flaming Lips|Turn It On
446|Snow Patrol|Chocolate
445|XTC|Making Plans For Nigel
444|M. Ward|Helicopter
443|Joseph Arthur|Can't Exist
442|Elbow|Forget Myself
441|Broadcast|America's Boy
440|Beach House|Norway
439|Alabama Shakes|Hold On
438|The Thermals|A Pillar of Salt
437|The Temper Trap|Sweet Disposition
436|The Go! Team|Ladyflash
435|Pixies|Gouge Away
434|Haerts|Wings
433|Dirty Projectors|Stillness Is the Move
432|The Strokes|You Only Live Once
431|Death Cab for Cutie|A Movie Script Ending
430|The Cave Singers|Seeds of Night
429|Aloe Blacc|I Need a Dollar
428|The Little Ones|Lovers Who Uncover
427|The Afghan Whigs|Debonair
426|Ramones|I Wanna Be Sedated
425|Cat Power|The Greatest
424|Broken Social Scene|World Sick
423|Band of Horses|Weed Party
422|Seapony|Dreaming
421|Ride|Leave Them All Behind
420|Elbow|Grounds for Divorce
419|Snow Patrol|Wow
418|Portishead|Sour Times
417|Sharon Jones and the Dap-Kings|This Land Is Your Land
416|Porno for Pyros|Pets
415|Mission of Burma|That's When I Reach For My Revolver
414|Love and Rockets|No New Tale to Tell
413|Kitchens of Distinction|Drive That Fast
412|Doves|Rise
411|Bauhaus|Dark Entries
410|Radiohead|Paranoid Android
409|Cults|Go Outside
408|Broken Social Scene|Stars and Sons
407|The Sonics|Have Love Will Travel
406|Iron & Wine|Boy With a Coin
405|Wilco|Impossible Germany
404|The Head and The Heart|Lost In My Mind
403|Sebadoh|On Fire
402|Beirut|Elephant Gun
401|Portishead|Wandering Star
400|Mirah|Cold Cold Water
399|Arcade Fire|Sprawl II (Mountains Beyond Mountains)
398|Neutral Milk Hotel|In the Aeroplane Over the Sea
397|Muscles|Ice Cream
396|Fujiya & Miyagi|Collarbone
395|Lily Allen|Friday Night
394|Friendly Fires|Jump in the Pool
393|Pixies|Wave of Mutilation
392|Maps|To the Sky
391|Rodriguez|Sugar Man
390|Talking Heads|Psycho Killer
389|Luna|California (All the Way)
388|Built to Spill|In the Morning
387|Primal Scream|Movin' on Up
386|The Raveonettes|Love in a Trashcan
385|Dead Kennedys|Holiday in Cambodia
384|José González|Heartbeats
383|Fleet Foxes|Ragged Wood
382|Band of Horses|Ode to LRC
381|The Lightning Seeds|Pure
380|Passion Pit|Sleepyhead
379|Hercules and Love Affair|Blind
378|Yo La Tengo|Ohm
377|Broken Bells|The High Road
376|Jagwar Ma|Come Save Me
375|Broadcast|Black Cat
374|The Stills|Lola stars and stripes
373|The Jam|In the City
372|South|Paint the Silence
371|New Order|Love Vigilantes
370|Miike Snow|Animal
369|Franz Ferdinand|Take Me Out
368|Death in Vegas|Girls
367|Caribou|Can't Do Without You
366|Blonde Redhead|Spring and by Summer Fall
365|Washed Out|Eyes Be Closed
364|Death Cab for Cutie|Transatlanticism
363|The The|Love Is Stronger Than Death
362|The Black Angels|The Sniper at the Gates of Heaven
361|The Postal Service|Sleeping In
360|Luna|23 Minutes in Brussels
359|Delays|Nearer Than Heaven
358|The Clash|This Is Radio Clash
357|Caribou|Sun
356|Broken Social Scene|Anthems for a Seventeen Year-Old Girl
355|Alexi Murdoch|Orange Sky
354|AIR|Cherry Blossom Girl
353|Elliott Smith|Needle in the Hay
352|Rogue Wave|Publish My Love
351|Loretta Lynn|Portland, Oregon (feat. Jack White)
350|Yeah Yeah Yeahs|Phenomena
349|Cut Copy|Need You Now
348|David Byrne and Brian Eno|Strange Overtones
347|Archers of Loaf|Web in Front
346|Wilco|Handshake Drugs
345|The Hold Steady|Stay Positive
344|The Clash|Straight to Hell
343|Snow Patrol|Run
342|Mylo|In My Arms
341|Maxïmo Park|Apply Some Pressure
340|Interpol|Untitled
339|DeVotchKa|The Enemy Guns
338|Depeche Mode|Enjoy the Silence
337|Baby Dayliner|You Push I'll go
336|Wilco|I Am Trying to Break Your Heart
335|Tame Impala|Apocalypse Dreams
334|T. Rex|Jeepster
333|Stereo MCs|Connected
332|Sea Ray|Revelry
331|Yeasayer|Ambling Alp
330|Travis|Sing
329|Pickwick|Hacienda Motel
328|Perfume Genius|Queen
327|New Order|Regret
326|Joseph Arthur|Honey and the Moon
325|Iggy & The Stooges|Search and Destroy
324|Foals|Black Gold
323|Cut Copy|Where I'm Going
322|Beirut|Nantes
321|16 Horsepower|Black Soul Choir
320|Brazilian Girls|Don't Stop
319|Sleater-Kinney|Jumpers
318|The Shins|Phantom Limb
317|Tame Impala|Let It Happen
316|Johnny Cash|Hurt
315|DJ Shadow|Midnight in a Perfect World
314|Fleet Foxes|Your Protector
313|Radiohead|Optimistic
312|Massive Attack|Angel
311|Badly Drawn Boy|Once Around the Block
310|Pixies|Bone Machine
309|Tapes 'n Tapes|Cowbell
308|The Godfathers|Birth, School, Work, Death
307|Husky Rescue|Summertime Cowboy
306|Arcade Fire|Neighborhood #3
305|Vampire Weekend|A-Punk
304|The White Stripes|Fell in Love With a Girl
303|Spoon|The Way We Get By
302|Foals|My Number
301|Spoon|Stay Don't Go
300|Simian Mobile Disco|Hustler
299|The Verve|Bitter Sweet Symphony
298|Grizzly Bear|Knife
297|Blonde Redhead|23
296|Public Enemy|Fight The Power
295|Public Image Ltd.|Public Image
294|Beck|Beercan
293|Lou Reed|Walk on the Wild Side
292|My Morning Jacket|Off the Record
291|The Dandy Warhols|Godless
290|Depeche Mode|Never Let Me Down Again
289|Band of Horses|Is There a Ghost
288|Band of Horses|Wicked Gil
287|Mission of Burma|Academy Fight Song
286|Yeah Yeah Yeahs|Zero
285|Visqueen|Vaxxine
284|Joy Division|Disorder
283|EELS|Fresh Feeling
282|Imperial Teen|Ivanka
281|Old 97's|TImebomb
280|Built to Spill|Strange
279|alt-J|Dissolve Me
278|The Ruby Doe|Red Letters
277|The National|Bloodbuzz Ohio
276|The Joy Formidable|Austere
275|Pixies|Here Comes Your Man
274|MGMT|Electric Feel
273|DJ Shadow|Building Steam With A Grain of Salt
272|Johnny Cash|Ring of Fire
271|Built to Spill|Kicked It in the Sun
270|Yeah Yeah Yeahs|Gold Lion
269|Rose Windows|Native Dreams
268|The Stranglers|Golden Brown
267|The National|Fake Empire
266|Longwave|Wake Me When It's Over
265|Gorillaz|Rock the House
264|Yeasayer|Sunrise
263|The Clash|Train in Vain
262|We Were Promised Jetpacks|Quiet Little Voices
261|The Helio Sequence|Can't Say No
260|Peter Bjorn and John|The Chills
259|Longwave|Everywhere You Turn
258|Joy Division|She's Lost Control
257|The Replacements|Alex Chilton
256|TV on the Radio|I Was a Lover
255|The Postal Service|We Will Become Silhouettes
254|The Jam|Town Called Malice
253|The Futureheads|Hounds of Love
252|The Breeders|Divine Hammer
251|Radio Nationals|Golden
250|Lyrics Born|Callin' Out
249|!!!|AM/FM
248|M83|Don't Save Us From the Flames
247|Kate Bush|Running Up That Hill (A Deal With God)
246|The Wrens|Everyone Chooses Sides
245|David Bowie|Sound and Vision
244|The Replacements|Bastards of Young
243|The Stills|Still In Love Song
242|The Joy Formidable|Whirring
241|Spoon|Sister Jack
240|PJ Harvey|Down By The Water
239|Hum|Stars
238|Catherine Wheel|Crank
237|Cat Power|Free
236|AIR|Surfing on a Rocket
235|The New Pornographers|Letter From an Occupant
234|The Jesus and Mary Chain|Happy when it rains
233|Sugar|Hoover Dam
232|New Order|Temptation
231|Dinosaur Jr.|Start Choppin
230|The Mountain Goats|No Children
229|The Flaming Lips|Fight Test
228|The Chemical Brothers|Swoon
227|Slint|Good Morning, Captain
226|Pixies|Monkey Gone To Heaven
225|Jeff Buckley|Last Goodbye
224|Modest Mouse|Gravity Rides Everything
223|Echo & The Bunnymen|Lips Like Sugar
222|M83|Kim & Jessie
221|LCD Soundsystem|North American Scum
220|Bloc Party|Like Eating Glass
219|Arcade Fire|Reflektor
218|The Flaming Lips|Yoshimi Battles The Pink Robots pt. 1
217|The Clash|London Calling
216|MGMT|Kids
215|Basement Jaxx|Raindrops
214|The White Stripes|Jolene
213|Radiohead|I Might Be Wrong
212|Radiohead|Let Down
211|Gil Scott-Heron|Me And The Devil
210|Tom Waits|Hoist That Rag
209|Kasabian|Club Foot
208|Beck|Hell Yes
207|Beach House|Walk in the Park
206|Father John Misty|Hollywood Forever Cemetery Sings
205|Devo|Freedom of Choice
204|Sonic Youth|100%
203|The Notwist|One With the Freaks
202|Rilo Kiley|Portions for Foxes
201|Neutral Milk Hotel|Two-Headed Boy
200|Kings of Leon|King of the Rodeo
199|alt-J|Fitzpleasure
198|The Dead Milkmen|Punk Rock Girl
197|Pavement|Stereo
196|New Order|Ceremony
195|A Tribe Called Quest|Can I Kick It?
194|My Morning Jacket|Wordless Chorus
193|Aqualung|Brighter Than Sunshine
192|The War on Drugs|Red Eyes
191|The Postal Service|The District Sleeps Alone Tonight
190|Clap Your Hands Say Yeah|The Skin of My Yellow Country Teeth
189|Bon Iver|Skinny Love
188|The Wrens|Happy
187|Silversun Pickups|Lazy Eye
186|Arcade Fire|Rebellion (Lies)
185|LCD Soundsystem|I Can Change
184|Phantogram|When I'm Small
183|Editors|Smokers Outside the Hospital Doors
182|Phantogram|Black Out Days
181|Of Monsters and Men|Little Talks
180|Yeah Yeah Yeahs|Y Control
179|The Black Angels|Black Grease
178|Pela|Lost To The Lonesome
177|Iggy Pop|Lust for Life
176|THEESatisfaction|Queens
175|Sonic Youth|Teen Age Riot
174|LCD Soundsystem|Losing My Edge
173|Interpol|Evil
172|The Helio Sequence|Hallelujah
171|Shuggie Otis|Strawberry Letter 23
170|Beat Connection|In the Water
169|Pavement|Cut Your Hair
168|Patti Smith|Gloria
167|Hot Chip|And I Was a Boy From School
166|Bloc Party|This Modern Love
165|The Sugarcubes|Birthday
164|Talking Heads|Once in a Lifetime
163|Sleigh Bells|Rill Rill
162|Sia|Breathe Me
161|Sonic Youth|Sugar Kane
160|Ned's Atomic Dustbin|Grey Cell Green
159|Deltron 3030|3030
158|Ryan Adams|To Be Young (Is to Be Sad, Is to Be High)
157|The Long Winters|Cinnamon
156|Massive Attack|Protection
155|Empire of the Sun|Alive
154|LCD Soundsystem|Get Innocuous!
153|Built to Spill|Car
152|Nada Surf|Always Love
151|The Black Keys|10 A.M. Automatic
150|Spoon|I Turn My Camera On
149|Nick Drake|Pink Moon
148|Pavement|Summer Babe (Winter Version)
147|The Breeders|Cannonball
146|Gossip|Standing In The Way Of Control
145|Little Dragon|Ritual Union
144|Beach House|Myth
143|Animal Collective|What Would I Want? Sky
142|Broken Social Scene|7/4 (Shoreline)
141|LCD Soundsystem|Dance Yrself Clean
140|Citizen Cope|Bullet And A Target
139|The Wrens|This Boy Is Exhausted
138|The Shins|So Says I
137|PJ Harvey|You Said Something
136|Peter Bjorn and John|Young Folks
135|Tapes 'n Tapes|Insistor
134|Papas Fritas|Way You Walk
133|The Replacements|Can't Hardly Wait
132|Flight of the Conchords|Business Time
131|Wilco|I'm the Man Who Loves You
130|The Twilight Sad|That Summer, At Home I Had Become the Invisible Boy
129|The Shins|Kissing the Lipless
128|Deerhunter|Helicopter
127|Ride|Taste
126|The Stone Roses|Waterfall
125|Nick Cave & The Bad Seeds|Red Right Hand
124|The Beatles|Tomorrow Never Knows
123|Fruit Bats|When U Love Somebody
122|Stars|Elevator Love Letter
121|Animal Collective|Summertime Clothes
120|The Cave Singers|Dancing on Our Graves
119|Foals|Spanish Sahara
118|Yeasayer|O.N.E.
117|Phosphorescent|Song For Zula
116|De La Soul|Eye Know
115|Röyksopp|What Else Is There?
114|LCD Soundsystem|All My Friends
113|Jeff Buckley|Hallelujah
112|Mazzy Star|Fade Into You
111|Arcade Fire|Neighborhood #1
110|The Saturday Knights|45
109|Silversun Pickups|Kissing Families
108|Modest Mouse|Dramamine
107|The Cure|Just Like Heaven
106|The Replacements|Left of the Dial
105|Band of Horses|The Great Salt Lake
104|Aretha Franklin|Rock Steady
103|Japandroids|The House That Heaven Built
102|The National|Abel
101|Nirvana|Love Buzz
100|Television|See No Evil
99|Built to Spill|Carry the Zero
98|The Rapture|House of Jealous Lovers
97|The Stooges|I Wanna Be Your Dog
96|Throwing Muses|Not Too Soon
95|Billy Bragg & Wilco|California Stars
94|Radiohead|The National Anthem
93|Gang of Four|Damaged Goods
92|The Flaming Lips|Do You Realize??
91|Neko Case|Hold On, Hold On
90|Grimes|Genesis
89|LCD Soundsystem|Too Much Love
88|The National|Mistaken for Strangers
87|Talib Kweli|Get By
86|Modest Mouse|Float On
85|Camper Van Beethoven|Take The Skinheads Bowling
84|Arcade Fire|Intervention
83|Doves|Words
82|Yeah Yeah Yeahs|Maps
81|The National|Lit Up
80|The Church|Under the Milky Way
79|Gui Boratto|No Turning Back
78|Tricky|Black Steel
77|The Dandy Warhols|We Used To Be Friends
76|Bikini Kill|Rebel Girl
75|Nada Surf|Happy Kid
74|Radiohead|Idioteque
73|Catherine Wheel|Black Metallic
72|M.I.A.|Paper Planes
71|The Roots|The Seed (2.0)
70|Built to Spill|Goin' Against Your Mind
69|Air|Sexy Boy
68|The Reindeer Section|You Are My Joy
67|Ghostland Observatory|Sad Sad City
66|My Bloody Valentine|Soon
65|Cut Copy|Lights and Music
64|Sonic Youth|Kool Thing
63|Phantogram|Mouthful of Diamonds
62|Doves|There Goes The Fear
61|New Order|Age of Consent
60|Caribou|Odessa
59|LCD Soundsystem|Daft Punk Is Playing At My House
58|mclusky|To Hell With Good Intentions
57|Wolf Parade|Shine a Light
56|DeVotchKa|How It Ends
55|Sugar|A Good Idea
54|The Avalanches|Frontier Psychiatrist
53|Pixies|Debaser
52|Doves|Pounding
51|Arcade Fire|Neighborhood #2
50|Junior Boys|In the Morning
49|The The|This Is The Day
48|The Clash|Police On My Back
47|Okkervil River|For Real
46|Midlake|Roscoe
45|Pixies|Gigantic
44|Massive Attack|Teardrop
43|The Shins|Caring Is Creepy
42|Neutral Milk Hotel|Holland, 1945
41|The Smiths|How Soon Is Now?
40|School of Seven Bells|Half Asleep
39|The Helio Sequence|Keep Your Eyes Ahead
38|The Go! Team|The Power Is On
37|Radiohead|Everything in Its Right Place
36|TV on the Radio|Staring At the Sun
35|The Undertones|Teenage Kicks
34|Neko Case|Deep Red Bells
33|Yeasayer|2080
32|Interpol|Obstacle 1
31|Echo & The Bunnymen|The Killing Moon
30|The Postal Service|Such Great Heights
29|Sunny Day Real Estate|In Circles
28|The Strokes|The Modern Age
27|Deerhunter|Desire Lines
26|The Jesus and Mary Chain|Just Like Honey
25|Talking Heads|This Must Be the Place (Naive Melody)
24|The Shins|New Slang
23|The Knife|Heartbeats
22|The Stone Roses|I Wanna Be Adored
21|Animal Collective|My Girls
20|Band of Horses|The Funeral
19|M83|Midnight City
18|Interpol|PDA
17|Ladytron|Destroy Everything You Touch
16|Ride|Vapour Trail
15|Iggy Pop|The Passenger
14|The Walkmen|The Rat
13|The Replacements|I Will Dare
12|Nada Surf|Blonde on Blonde
11|TV on the Radio|Wolf Like Me
10|Arcade Fire|No Cars Go
9|Fugazi|Waiting Room
8|Joy Division|Transmission
7|Arcade Fire|Wake Up
6|The Beta Band|Dry the Rain
5|Joy Division|Love Will Tear Us Apart
4|My Bloody Valentine|Only Shallow
3|Pixies|Where Is My Mind?
2|The Mountain Goats|This Year
1|LCD Soundsystem|Someone Great
"""

# Every change from KEXP's printed text.
ARTIST_FIX = {
    "Siouxsie and The Bashees": "Siouxsie and the Banshees",
    "TV On The Radio": "TV on the Radio",
    "AIR": "Air",
    "Stereo MCs": "Stereo MC's",
    "Guided By Voices": "Guided by Voices",
    "DOM": "Dom",
    "EELS": "Eels",
    "The Buzzcocks": "Buzzcocks",
}
TITLE_FIX = {
    "TImebomb": "Timebomb",
    "sleepsinging": "Sleepsinging",
    "Lola stars and stripes": "Lola Stars and Stripes",
    "Happy when it rains": "Happy When It Rains",
    "You Push I'll go": "You Push, I'll Go",
    "There is a Light That Never Goes Out": "There Is a Light That Never Goes Out",
}

S = []
for line in RAW.strip().splitlines():
    r, a, t = line.split("|")
    S.append((int(r), ARTIST_FIX.get(a, a), TITLE_FIX.get(t, t)))
S.sort()
assert [r for r, *_ in S] == list(range(1, 632)), "ranks must run 1..631 with no gaps"


def search_title(t):
    return re.sub(r"\s*\((feat\.|extended version)[^)]*\)", "", t).strip()


src = {"label": "KEXP", "url": URL}
rows = [{
    "key": f"kexpall|{r}",
    "lead": f"#{r}",
    "sec": a,
    "pri": t,
    "yt": f"{search_title(t)} {a}",
    "ytWord": "Listen",
    "src": src,
} for r, a, t in S]

LIST = {
    "slug": SLUG,
    "title": "KEXP's Top Songs of All Time",
    "kind": "Canon",
    "verb": "heard",
    "noTick": True,
    "desc": ("The 631 songs Seattle&rsquo;s KEXP had played most, counted down in 2017. LCD Soundsystem at "
             "#1, The Mountain Goats at #2 &mdash; a station&rsquo;s own heavy rotation, not a poll."),
    "cols": ["Rank", "Artist", "Song", "Listen · source"],
    "srcLabel": "Counted down by",
    "sources": [{"url": URL, "label": "KEXP",
                 "q": "Top Songs of All Time",
                 "meta": "2017 · ranked by airplay · 631 songs"}],
    "note": ("A canon, and an unusual one: nobody voted. KEXP ranked these by how much the station had "
             "played them, and counted them down during its 2017 fall fund drive &mdash; so this is the sound "
             "of the DJs&rsquo; heavy rotation, not of a poll. The list keeps KEXP&rsquo;s order, #1 to #631. "
             "Spelling is tidied where the page has a typo or switches style (&ldquo;Siouxsie and The "
             "Bashees&rdquo;, AIR and Air); every change is listed in the script. Set it beside the station&rsquo;s "
             "own <em>Listeners&rsquo; Favorite Songs of the &rsquo;90s</em> and you can hear the difference "
             "between what a station plays and what its audience remembers: the airplay list belongs to the "
             "2000s &mdash; Arcade Fire twelve times, LCD Soundsystem nine, The Shins eight "
             "&mdash; and Nirvana&rsquo;s highest entry is <em>Love Buzz</em>, at #101."),
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

    out = sys.argv[1] if len(sys.argv) > 1 else "kexp-all-time.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["Year", "Artist", "Track", "Album"])
        for r, a, t in S:
            w.writerow(["", a, search_title(t), ""])
    print(len(rows), "songs →", PATH, "and", out)
