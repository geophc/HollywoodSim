# HollywoodSim/game/events.py

import random

class Event:
    def __init__(self, title, description, effect_fn=None):
        self.title = title
        self.description = description
        self.effect_fn = effect_fn  # Optional function to apply effects

    def trigger(self, studio, calendar):
        print(f"\n🎭 EVENT: {self.title}")
        print(f"{self.description}")
        if self.effect_fn:
            self.effect_fn(studio, calendar)


class EventManager:
    def __init__(self):
        self.history = []  # past triggered events
    
    def roll_monthly_events(self, studio, calendar):
        events = run_random_events(studio, calendar)
        self.history.extend(events)
        return events

# --- EFFECT FUNCTIONS ---

def reduce_actor_fame(actor, amount):
    actor["fame"] = max(0, actor.get("fame", 0) - amount)

def delay_movie(movie):
    if "release_date" in movie:
        year, month = movie["release_date"]
        month += 1
        if month > 12:
            year += 1
            month = 1
        movie["release_date"] = (year, month)

def boost_prestige(studio, amount):
    studio.prestige += amount

# --- EVENT ROLLER ---

def run_random_events(studio, calendar):
    triggered_events = []

    for movie in studio.released_movies:
        if movie.get("event_checked", False):
            continue

        actors = movie.get("cast", [])
        director = movie.get("director", {})
        rating = movie.get("rating", "PG-13")
        genre = movie.get("genre")
        quality = movie.get("quality", 50)

        # Pick a lead actor for event purposes
        lead_actor = actors[0] if actors else None

        # 🎭 Actor-related events
        if lead_actor and "diva" in lead_actor.get("traits", []) and random.random() < 0.1:
            triggered_events.append(actor_conflict(movie, lead_actor))

        if lead_actor and lead_actor.get("fame", 0) > 75 and random.random() < 0.05:
            triggered_events.append(tabloid_scandal(lead_actor, movie))

        # 🎥 Director-related
        if director and director.get("education") == "Self-Taught" and random.random() < 0.08:
            triggered_events.append(director_rewrites(movie))

        # 🧨 Genre-specific events
        if genre == "Horror" and rating in ["R", "NC-17"] and random.random() < 0.15:
            triggered_events.append(moral_panic(movie))

        if genre == "Drama" and quality > 85 and random.random() < 0.2:
            triggered_events.append(critics_darling(movie))

        if genre == "Romance" and "emotional" in movie.get("tags", []) and random.random() < 0.1:
            triggered_events.append(fan_favourite(movie))

        movie["event_checked"] = True

    # 🏢 Studio-wide events
    if random.random() < 0.04:
        triggered_events.append(studio_lawsuit(studio))

    if random.random() < 0.03:
        triggered_events.append(investor_pressure(studio))

    studio.newsfeed += triggered_events
    return triggered_events

# --- Individual Event Functions ---

def actor_conflict(movie, actor):
    actor["reputation"] = "difficult"
    return f"⚠️ On-set clash: {actor['name']} created tension on the set of '{movie['title']}'."

def tabloid_scandal(actor, movie):
    actor["fame"] = max(10, actor.get("fame", 0) - 5)
    return f"🗞️ Scandal: Tabloids erupt over {actor['name']}'s behaviour during '{movie['title']}'. Fame drops."

def director_rewrites(movie):
    movie["quality"] = max(0, movie.get("quality", 0) - 2)
    return f"🎬 Director drama: Last-minute rewrites hurt '{movie['title']}'s cohesion."

def moral_panic(movie):
    return f"👻 Moral panic: Parents groups protest violent content in '{movie['title']}'! Unexpected attention."

def critics_darling(movie):
    movie["bonus_awards"] = movie.get("bonus_awards", 0) + 1
    return f"🏆 Awards buzz: '{movie['title']}' emerges as a critical favourite."

def fan_favourite(movie):
    movie["prestige"] = movie.get("prestige", 0) + 1
    return f"💖 Fan darling: Viewers are emotionally connecting with '{movie['title']}'. Fanbase is growing."

def studio_lawsuit(studio):
    studio.prestige = max(0, studio.prestige - 1)
    return "⚖️ Lawsuit: Former employee files suit against the studio—reputation hit."

def investor_pressure(studio):
    studio.balance += 10  # emergency funding
    return "💼 Investors intervene: Surprise funding granted—but expectations are rising."
