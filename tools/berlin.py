"""Isabel's "Berlin Restaurants" Google Maps list → the Places shelf.

A Canon, not a Tally: one person decided this list. Kept in her saved order
rather than re-sorted by rating, because the order is hers.

Two places Google marks permanently closed (Mariona, Cooquin Café) are left
out — a list you're meant to eat your way down shouldn't send you to a closed
door. Xigon is only temporarily closed, so it stays, flagged.

Links are Google Maps *searches* scoped to Berlin rather than saved place ids,
for the same reason the book links are Goodreads searches: an id can be merged
or retired, a search for the name still finds the place.
"""
import json
from urllib.parse import quote

def maps(name):
    return "https://www.google.com/maps/search/?api=1&query=" + quote(f"{name} Berlin")

# name, rating, reviews, price, cuisine  — in the order they appear in the list
P = [
 ("VINO e CUCINA", "4.6", "€20–60", "Italian"),
 ("Blaue Bohne Rösterei", "4.7", "€1–10", "Coffee shop"),
 ("Suigyo Izakaya", "4.7", "€10–20", "Japanese"),
 ("Jemenitisches Restaurant", "4.5", "€10–20", "Yemeni"),
 ("893 Ryōtei", "4.6", "€100+", "Japanese"),
 ("Umami", "4.6", "€10–20", "Vietnamese"),
 ("Xigon", "4.7", "Temporarily closed", "Vietnamese"),
 ("Favorit Gemüse Kebap", "4.7", "€1–10", "Kebab"),
 ("El Reda", "4.7", "€10–20", "Lebanese"),
 ("Agni", "4.5", "€10–20", "Indian"),
 ("Schnitzelei Mitte", "4.5", "€20–30", "German"),
 ("Taquería El Oso", "4.5", "€10–20", "Mexican"),
 ("Dunya Gemüse Kebab", "4.9", "€1–10", "Kebab"),
 ("Salami Social Club", "4.6", "€10–20", "Pizza"),
 ("Silo Coffee", "4.5", "€10–20", "Breakfast"),
 ("Burgermeister Schlesisches Tor", "4.7", "€10–20", "Burgers"),
 ("Koy", "4.6", "€10–20", "Thai"),
 ("Imren Grill", "4.0", "€1–10", "Turkish"),
 ("Gemüse Kebap & Friends", "4.8", "€1–10", "Kebab"),
 ("Night Kitchen", "4.7", "€40–80", "Mediterranean"),
 ("Niko Niko Ramen", "4.4", "€10–20", "Ramen"),
 ("60 seconds to napoli", "4.5", "€20–30", "Pizza"),
 ("YOSOY Tapas Berlin", "4.7", "", "Tapas"),
 ("Chinarestaurant Shanghai", "4.4", "€10–20", "Chinese"),
 ("Transit", "4.4", "€20–30", "Thai"),
 ("The Factory Pizza & Pasta", "4.7", "€10–20", "Italian"),
 ("Iro Izakaya", "4.5", "€20–30", "Japanese"),
 ("Gaffel Haus Berlin", "4.5", "€20–30", "German"),
 ("Trattoria bar Lambretta", "4.8", "€20–30", "Italian"),
 ("Jolly", "4.6", "€20–30", "Chinese"),
 ("Cocolo Ramen X-berg", "4.4", "€10–20", "Ramen"),
 ("li.ke : serious thai vegan", "4.7", "€10–20", "Thai · vegan"),
 ("Shōdo Udon Lab", "4.4", "€10–20", "Udon"),
 ("Tom'n'Jerry", "4.8", "€10–20", "Pizza"),
 ("Zhou's Five", "4.0", "€20–30", "Chinese buffet"),
 ("Huong Que", "4.4", "€10–20", "Vietnamese"),
 ("BABIKYU", "4.5", "€20–30", "Korean BBQ"),
 ("Good Morning Vietnam Vegan", "4.5", "€10–20", "Vietnamese · vegan"),
 ("Tibet Haus Restaurant", "4.6", "€10–20", "Nepalese"),
]

rows = []
for name, rating, price, cuisine in P:
    r = {
      "key": f"berlin|{name}",
      "lead": f"{rating}★",
      "sec": cuisine,
      "pri": name,
      "links": [{"url": maps(name), "label": "Map ↗"}],
    }
    if price:
        r["extra"] = price
    rows.append(r)

json.dump(rows, open("berlin.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(len(rows), "restaurants")
