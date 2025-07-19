# game/casting.py

import random

class CastingPool:
    def __init__(self):
        self.actors = []
        self.writers = []
        self.directors = []

    def add_actor(self, actor):
        self.actors.append(actor)

    def get_actor_choices(self, count=3):
        return random.sample(self.actors, k=min(count, len(self.actors)))

    def age_all_talent(self):
        for actor in self.actors:
            actor["age"] += 1

    # Extend with writers/directors when those systems are added

    

class CastingManager:
    def __init__(self):
        self.collaborations = {}  # {(actor_name): [qualities]}

    def record_collaboration(self, actor, movie):
        key = (actor["name"])
        if key not in self.collaborations:
            self.collaborations[key] = []
        self.collaborations[key].append({
            "title": movie["title"],
            "quality": movie["quality"],
            "box_office": movie["box_office"]
        })

    def get_history(self, actor_name):
        key = (actor_name)
        records = self.collaborations.get(key, [])
        if not records:
            return None
        avg_quality = sum(r["quality"] for r in records) / len(records)
        avg_box_office = sum(r["box_office"] for r in records) / len(records)
        return {
            "count": len(records),
            "avg_quality": round(avg_quality, 1),
            "avg_box_office": round(avg_box_office, 1)
        }

    def get_collaboration_count(self, actor, writer):
        key = (actor["name"], writer["name"])
        return len(self.collaborations.get(key, []))

    def get_average_quality(self, actor, writer):
        key = (actor["name"], writer["name"])
        history = self.collaborations.get(key, [])
        if not history:
            return None
        return round(sum(f["quality"] for f in history) / len(history), 2)

    def get_average_box_office(self, actor, writer):
        key = (actor["name"], writer["name"])
        history = self.collaborations.get(key, [])
        if not history:
            return None
        return round(sum(f["box_office"] for f in history) / len(history), 2)

    def describe_pairing(self, actor, writer):
        count = self.get_collaboration_count(actor, writer)
        if count == 0:
            return "First time working together."
        avg_quality = self.get_average_quality(actor, writer)
        avg_box = self.get_average_box_office(actor, writer)
        return (
            f"🎞️  {actor['name']} and {writer['name']} have worked together {count} times. "
            f"Avg Quality: {avg_quality}, Avg Box Office: ${avg_box}M"
        )
