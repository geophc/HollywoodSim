# game/casting.py

import random

class CastingPool:
    def __init__(self):
        self.actors = []
        self.writers = []
        self.directors = []

    def add_actor(self, actor):
        self.actors.append(actor)

    def add_writer(self, writer):
        self.writers.append(writer)

    def get_actor_choices(self, count=3):
        return random.sample(self.actors, k=min(count, len(self.actors)))

    def get_writer_choices(self, count=3):
        return random.sample(self.writers, k=min(count, len(self.writers)))

    def age_all_talent(self):
        for actor in self.actors:
            actor["age"] += 1
        for writer in self.writers:
            writer["age"] += 1
        # You can add director aging when implemented


class CastingManager:
    def __init__(self):
        # Tracks collaborations (currently actor-only, will expand to include writer/director)
        self.collaborations = {}  # Keys: (actor_name), (actor_name, writer_name)

    def record_collaboration(self, actor, movie):
        actor_key = actor["name"]
        if actor_key not in self.collaborations:
            self.collaborations[actor_key] = []
        self.collaborations[actor_key].append({
            "title": movie["title"],
            "quality": movie["quality"],
            "box_office": movie["box_office"]
        })

        # Track actor-writer pair if writer is provided
        if "writer" in movie:
            pair_key = (actor["name"], movie["writer"]["name"])
            if pair_key not in self.collaborations:
                self.collaborations[pair_key] = []
            self.collaborations[pair_key].append({
                "title": movie["title"],
                "quality": movie["quality"],
                "box_office": movie["box_office"]
            })

    def get_history(self, actor_name):
        records = self.collaborations.get(actor_name, [])
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
            return "🆕 First-time pairing."
        avg_quality = self.get_average_quality(actor, writer)
        avg_box = self.get_average_box_office(actor, writer)
        return (
            f"🎞️  {actor['name']} and {writer['name']} have collaborated {count}x. "
            f"Avg Quality: {avg_quality}, Avg Box Office: ${avg_box}M"
        )
