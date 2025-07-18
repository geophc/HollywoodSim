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
