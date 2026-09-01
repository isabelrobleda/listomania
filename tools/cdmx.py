"""r/travel — "Best meals you had in Mexico City?"

Counted by distinct redditor: naming a place counts, and endorsing it in a reply
counts. Answers that name no place — "literally just walk into any restaurant",
"the quesadilla vendor outside my hotel" — are dropped with regret, because they
are the truest answers in the thread and there is no row to put them in.
"""
import json, urllib.parse

THREAD = {
    "q": "Best meals you had in Mexico City?",
    "site": "Reddit · r/travel",
    "year": 2024,
    "meta": "141 points · 260 comments",
    "url": "https://www.reddit.com/r/travel/comments/1hi420n/best_meals_you_had_in_mexico_city/",
}

# (place, what it is, times named)
D = [
 ("Contramar","Seafood",18),
 ("Pujol","Fine dining",17),
 ("Quintonil","Fine dining",9),
 ("Masala y Maiz","Mexican–Indian–East African",9),
 ("Rosetta","Italian-Mexican · bakery",8),
 ("Máximo Bistrot","Fine dining",6),
 ("La Casa de Toño","Pozole · late night",4),
 ("Mi Compa Chava","Marisquería",4),
 ("Taquería Los Cocuyos","Tacos · suadero",3),
 ("Expendio de Maíz Sin Nombre","No-menu Mexican",3),
 ("Fónico","Fine dining",3),
 ("Taquería El Greco","Tacos árabes",3),
 ("Taquería Orinoco","Tacos · chicharrón",3),
 ("Casa Virginia","French-Mexican",3),
 ("Meroma","Modern Mexican",2),
 ("El Vilsito","Tacos al pastor",2),
 ("Entremar","Seafood",2),
 ("Casa 1900","Bakery",2),
 ("Carmela y Sal","Modern Mexican",2),
 ("Marigold","Breakfast",2),
 ("La Esquina del Chilaquil","Torta de chilaquiles",2),
 ("El Pescadito","Fish & shrimp tacos",2),
 ("Taquería El Turix","Cochinita pibil",1),
 ("Carajillo","Vegetarian-friendly",1),
 ("Balcón del Zócalo","Fine dining · view",1),
 ("Azul Histórico","Traditional Mexican",1),
 ("Azul Condesa","Traditional Mexican",1),
 ("El Hidalguense","Barbacoa · weekends only",1),
 ("El Bajío","Traditional Mexican",1),
 ("Marcello","Italian",1),
 ("Carnitas Los Panchos","Carnitas",1),
 ("Maizajo","Masa-focused · taquería",1),
 ("La Pitahaya Vegana","Vegan tacos",1),
 ("Lorea","Fine dining",1),
 ("Sartoria","Italian",1),
 ("Pizza Félix","Pizza",1),
 ("Tetetlán","Modern Mexican",1),
 ("Botánico","Modern Mexican",1),
 ("Tigre Silencioso","Modern Mexican",1),
 ("Cariñito Tacos","Asian-Mexican tacos",1),
 ("Voraz","Elevated Mexican",1),
 ("Blanca Colima","Modern Mexican",1),
 ("Amari","Italian",1),
 ("Huset","Wood-fired",1),
 ("Lalo!","Brunch",1),
 ("Chilakillers","Chilaquiles",1),
 ("Filigrana","Modern Mexican",1),
 ("Takotl","Queso fundido",1),
 ("Tacos Don Juan","Birria",1),
 ("El Moro","Churros",1),
 ("Alchef","Sandwiches",1),
 ("La Única","Mexican",1),
 ("Villa María","Mexican · cantina",1),
 ("La Gruta","Mexican · in a cave",1),
 ("Saks Polanco","Breakfast",1),
 ("Ling Ling","Sushi",1),
 ("Arango","Steak · view",1),
 ("Pargot","Modern Mexican",1),
 ("Esquina Común","Modern Mexican",1),
 ("La Fonda del Recuerdo","Traditional Mexican",1),
 ("La Poblanita de Tacubaya","Traditional Mexican",1),
 ("Costa Guadiana","Seafood",1),
 ("Parole Polanco","Italian",1),
 ("Los Loosers","Vegan",1),
 ("El Cazador","Traditional Mexican",1),
 ("Mux","Modern Mexican",1),
 ("Tacobar","Tacos · bar",1),
 ("Odette","Pastries",1),
 ("Bistro Máximo","Bistro",1),
 ("Pigeon","Modern Mexican",1),
 ("Baltra Bar","Cocktails",1),
 ("La Capital","Modern Mexican",1),
 ("Mérito","Peruvian-Mexican",1),
 ("Tacos Los Juanes","Tacos",1),
]

def maps(name):
    return ("https://www.google.com/maps/search/?api=1&query="
            + urllib.parse.quote(name + " Mexico City"))

rows = [{"key": "cdmx|" + p, "lead": f"{n}×", "sec": what, "pri": p,
         "links": [{"url": maps(p), "label": "Map ↗"}],
         "src": {"label": "r/travel", "url": THREAD["url"]}}
        for p, what, n in sorted(D, key=lambda r: (-r[2], r[0].lower()))]

json.dump({"thread": THREAD, "rows": rows}, open("cdmx.json", "w"),
          ensure_ascii=False, separators=(",", ":"))
print(len(rows), "places;", sum(n for _, _, n in D), "recommendations")
