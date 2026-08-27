# -*- coding: utf-8 -*-
"""r/Spanish — "Las mejores canciones en español?"

The first list on this site that isn't in English, and the first one that isn't
really a tally at all.

Every other crowd list here works because hundreds of strangers answer the same
question and the overlaps are the result. This thread has 46 comments, and the
asker opens by posting 36 songs of his own — so what accumulates isn't a
ranking, it's a playlist being built in public, one person at a time. Almost
nothing gets named twice. That is not a failure of the thread; it is what
happens when a question has no canon behind it, and it's the reason this list
is worth having next to the ones that do.

So the counting rule is the same as everywhere else — by distinct redditor,
naming counts, agreeing counts, an artist or an album without a song doesn't —
but with one deliberate change: the asker's own list is counted rather than
excluded. In every other thread here the asker's pick is a thumb on the scale.
Here he wrote "Empiezo:" and put down 36 songs, which is a contribution, not a
question.

What gets dropped: recommendations that name only an artist ("falta Pablo
Alborán", "cualquier cosa de Kevin Kaarl", "Buena Vista Social Club"), and one
album recommended whole. Songs given without an artist ("Quizás, quizás,
quizás, en infinidad de versiones") are kept and credited to Varios artistas,
because the point of naming them was that the song outlived any one recording.
"""
import csv
import json
from collections import defaultdict

THREAD = {
    "q": "Las mejores canciones en español?",
    "site": "Reddit · r/Spanish",
    "year": 2023,
    "meta": "38 puntos · 46 comentarios",
    "url": "https://www.reddit.com/r/Spanish/comments/17yiokm/las_mejores_canciones_en_espa%C3%B1ol/",
}

VARIOS = "Varios artistas"

# redditor -> [(canción, artista), ...]
B = {
# El que pregunta abre con 36 canciones. Aquí eso cuenta.
"zalogon119": [
  ("Lamento Boliviano", "Los Enanitos Verdes"), ("Falta de Querer", "Mon Laferte"),
  ("Juanito Alimaña", "Héctor Lavoe"), ("La Cita", "Galy Galiano"),
  ("Noches de Fantasía", "Joseph Fonseca"), ("Mujer Amante", "Rata Blanca"),
  ("Triste Canción", "El Tri"), ("Lo Dudo", "Frankie Ruiz"),
  ("La Nave del Olvido", "José José"),
  ("Vivir Así Es Morir de Amor", "Camilo Sesto"),
  ("Otro Ocupa Mi Lugar", "Miguel Gallardo"),
  ("Devórame Otra Vez", "Eddie Santiago"), ("Fanny", "Leo Dan"),
  ("Costumbre", "Sonora Skandalo"), ("Corazón Valiente", "Gilda"),
  ("Suavemente", "Elvis Crespo"), ("Por Una Cabeza", "Carlos Gardel"),
  ("Hoja en Blanco", "Monchy & Alexandra"),
  ("Para No Verte Más", "La Mosca Tse-Tse"), ("La Copa Rota", "José Feliciano"),
  ("Olvídala", "Binomio de Oro de América"), ("Noelia", "Nino Bravo"),
  ("Como la Flor", "Selena"), ("Valiente", "Pimpinela"),
  ("Si No Te Hubieras Ido", "Marco Antonio Solís"),
  ("Y Hubo Alguien", "Marc Anthony"), ("Volver a Amar", "Cristian Castro"),
  ("Tan Enamorados", "Ricardo Montaner"),
  ("Si Me Dejas No Vale", "La Línea"), ("Sin Sentimientos", "Grupo Niche"),
  ("La Quiero a Morir", "DLG"), ("Escríbeme una Carta", "Tierra Canela"),
  ("Mientes", "Ke Personajes"), ("Quimbara", "Celia Cruz"),
  ("Cómo Olvidarla", "Rodrigo Bueno"),
  ("Por Lo Que Yo Te Quiero", "Walter Olmos"), ("Bulería", "David Bisbal")],
"slepyhed": [("La Flaca", "Jarabe de Palo"), ("A Dios le Pido", "Juanes"),
  ("Para No Verte Más", "La Mosca Tse-Tse"), ("La Llorona", VARIOS)],
"el_ria_ton": [("Hasta la Raíz", "Natalia Lafourcade"),
  ("Amor Completo", "Mon Laferte"), ("Pa' Dónde Se Fue", "Mon Laferte"),
  ("Si Tú Me Quisieras", "Mon Laferte"), ("Primaveral", "Mon Laferte"),
  ("Amárrame", "Mon Laferte"), ("Tormento", "Mon Laferte"),
  ("Quédate Esta Noche", "Mon Laferte"), ("La Camisa Negra", "Juanes"),
  ("A Dios le Pido", "Juanes"), ("Me Enamora", "Juanes"),
  ("Nunca Es Suficiente", "Natalia Lafourcade"),
  ("Lo Que Construimos", "Natalia Lafourcade"), ("No", "Shakira"),
  ("Que Me Quedes Tú", "Shakira"), ("Antología", "Shakira"),
  ("Gitana", "Shakira"), ("La Tortura", "Shakira"),
  ("Día de Enero", "Shakira"), ("Gimme Tha Power", "Molotov"),
  ("Diseño Rolas", "Molotov"), ("Voto Latino", "Molotov"),
  ("Frijolero", "Molotov"), ("Reggaetón Champagne", "Bellakath & Dani Flow")],
"KarlIAM": [("Fabricando Fantasías", "Tito Nieves"),
  ("No Voy a Llorar", "Los Diablitos"), ("Así Fue", "Juan Gabriel"),
  ("Afuera", "Caifanes"), ("Rosas", "La Oreja de Van Gogh"),
  ("Europa VII", "La Oreja de Van Gogh"), ("Verano", "La Oreja de Van Gogh"),
  ("El Secreto de las Tortugas", "Maldita Nerea"),
  ("Bailarina", "Maldita Nerea"), ("¿No Podíamos Ser Agua?", "Maldita Nerea"),
  ("7 de Septiembre", "Mecano"), ("Me Cuesta Tanto Olvidarte", "Mecano"),
  ("Cruz de Navajas", "Mecano")],
"netinpanetin": [("Tonto el Que No Entienda", "Mecano"),
  ("Hijo de la Luna", "Mecano")],
"PolygonicResident": [("Alfonsina y el Mar", "Mercedes Sosa")],
"RICHUNCLEPENNYBAGS": [("Noche de Sexo", "Wisin & Yandel ft. Romeo Santos")],
"Flufsz": [("Hasta la Raíz", "Natalia Lafourcade"),
  ("Si Por Mí Fuera", "Beret"), ("Celoso", "Lele Pons")],
"Ventallot": [("Salir", "Extremoduro"), ("Golfa", "Extremoduro"),
  ("Stand By", "Extremoduro"),
  ("La Vereda de la Puerta de Atrás", "Extremoduro"),
  ("1932", "La M.O.D.A."), ("PRMVR", "La M.O.D.A."),
  ("Una Canción Para No Decir Te Quiero", "La M.O.D.A."),
  ("Los Héroes del Sábado", "La M.O.D.A."),
  ("Entre Dos Tierras", "Héroes del Silencio"),
  ("Iberia Sumergida", "Héroes del Silencio"),
  ("Maldito Duende", "Héroes del Silencio"),
  ("El Sol No Regresa", "La Quinta Estación"), ("Daría", "La Quinta Estación"),
  ("Algo Más", "La Quinta Estación"), ("Magia", "Saurom"),
  ("Noche de Halloween", "Saurom"), ("Música", "Saurom"),
  ("La Hija de las Estrellas", "Saurom")],
"Shmoneyy_Dance": [("Corazón Culpable", "Antony Santos"),
  ("Voy Pa'llá", "Antony Santos"), ("Dónde Estará", "Antony Santos"),
  ("Vete y Aléjate de Mí", "Antony Santos"),
  ("Linda y Difícil", "Antony Santos"), ("Por Mi Timidez", "Antony Santos"),
  ("Medicina de Amor", "Raulín Rodríguez"), ("Que Vuelva", "Raulín Rodríguez"),
  ("Morena Yo Soy Tu Marido", "Raulín Rodríguez"),
  ("Nereyda", "Raulín Rodríguez"), ("Esta Noche", "Raulín Rodríguez")],
"erriuga_leon27": [("Cómo Te Extraño Mi Amor", "Leo Dan"), ("Don", "Miranda!"),
  ("Hasta Que Te Conocí", "Juan Gabriel"),
  ("Puntos Cardinales", "Café Tacvba"), ("Luna", "Zoé"),
  ("Manía Cardiaca", "Enjambre"), ("Película Muda", "Pat3 de Fua"),
  ("La Carencia", "Panteón Rococó"), ("Círculo de Amor", "El Gran Silencio"),
  ("La Camisa Negra", "Juanes"), ("Yo Quisiera", "Reik")],
"continuousBaBa": [("Amores Lejanos", "Los Enanitos Verdes")],
"sergioaffs": [("No Soy de Aquí", "Facundo Cabral"),
  ("Y Nos Dieron las Diez", "Joaquín Sabina"),
  ("El Regalo Más Grande", "Tiziano Ferro"),
  ("De Música Ligera", "Soda Stereo"),
  ("Corazón Espinado", "Maná & Carlos Santana"),
  ("Suin Romanticón", "Monsieur Periné"), ("El Camino de la Vida", VARIOS),
  ("Corazón Partío", "Alejandro Sanz"),
  ("Como Yo Nadie Te Ha Amado", "Bon Jovi"), ("Rebelión", "Joe Arroyo"),
  ("Quizás, Quizás, Quizás", VARIOS), ("El Guitarro", "Andrés Cepeda"),
  ("Veneno en la Piel", "Andrés Calamaro"), ("Auto Rojo", "Vilma Palma e Vampiros"),
  ("La Tierra del Olvido", "Carlos Vives"), ("Chiquitita", "ABBA")],
"DanTarkan": [("Perdona Si Te Llamo Amor", "Maldita Nerea"),
  ("Lo Poco Que Tengo", "Ricardo Arjona"),
  ("Destino o Casualidad", "Melendi & Ha*Ash"),
  ("Tengo Ganas de Sonreír", "Zarcort & Town"),
  ("Veo en Ti la Luz", "Danna Paola & Chayanne"), ("Me Vale", "Maná"),
  ("Después de Ti", "Alejandro Lerner"), ("Otra Como Tú", "Eros Ramazzotti"),
  ("Que Nadie Vea", "Ricardo Arjona"), ("Sigue Soñando", "Piter-G"),
  ("Tabaco y Chanel", "Bacilos & Morat"),
  ("Jesús Es Verbo, No Sustantivo", "Ricardo Arjona"),
  ("Apnea", "Ricardo Arjona"),
  ("Rap Soy Juego de Tronos", "Sharkness")],
"Zemrik": [("La Leyenda del Hada y el Mago", "Rata Blanca"),
  ("Fiesta Pagana", "Mägo de Oz"), ("El Lazarillo de Tormes", "Saurom"),
  ("El Poeta Dice la Verdad", "La Trampa")],
"ryguysix": [("El Amor de Su Vida", "Grupo Frontera"),
  ("Amor Propio", "Grupo Frontera"), ("Le Va a Doler", "Grupo Frontera"),
  ("La Cherry", "Junior H"), ("Más Altas Que Bajadas", "Natanael Cano"),
  ("Mi Bello Ángel", "Natanael Cano"), ("Rápido Soy", "Clave Especial"),
  ("Dijeron Que No la Iba a Lograr", "Chino Pacas"),
  ("El Gordo Trae el Mando", "Chino Pacas"), ("Según Quién", "Maluma"),
  ("Nueva Vida", "Peso Pluma")],
"StringAggressive544": [("Ya Lo Sé", "Jenni Rivera"),
  ("Motivos", "Jenni Rivera"), ("Paloma Negra", "Jenni Rivera"),
  ("Cybertruck", "Bad Bunny"), ("Después de la Playa", "Bad Bunny"),
  ("Ganas de Ti", "Arcángel"), ("Bien Canijo", "Becky G"),
  ("Tukuntazo", "Tokischa")],
"kegira": [("Desesperado", "Andrés Cepeda")],
"Gabyyxviii": [("Mr. E", "Eduardo Gómez")],
"East-Operation-6907": [("Where (Perfecta)", "Nikolas Xes")],
"deleted-cuarteto": [("Yendo a la Casa de Damián", "El Cuarteto de Nos")],
"deleted-baron": [("Cuerdas de Acero", "Barón Rojo")],
"deleted-navaja": [("Pedro Navaja", "Rubén Blades")],
}

counts = defaultdict(set)
for user, songs in B.items():
    for song, artist in songs:
        counts[(song, artist)].add(user)

rows = sorted(
    ({"song": s, "artist": a, "mentions": len(u)} for (s, a), u in counts.items()),
    key=lambda r: (-r["mentions"], r["song"].lower()))

json.dump({"thread": THREAD, "rows": rows}, open("espanol.json", "w"),
          ensure_ascii=False, separators=(",", ":"))

with open("canciones-en-espanol.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["Year", "Artist", "Track", "Album"])
    for r in rows:
        w.writerow(["", r["artist"], r["song"], ""])

once = sum(1 for r in rows if r["mentions"] == 1)
print(len(rows), "canciones de", len(B), "personas;",
      sum(r["mentions"] for r in rows), "menciones;", once, "nombradas una vez")
for r in rows[:10]:
    print(f'  {r["mentions"]}x  {r["song"]} — {r["artist"]}')
