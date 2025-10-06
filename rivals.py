#HollywoodSim/game/rivals.py

import random

class RivalStudio:
    def __init__(self, name, balance=100, prestige=0):
        self.name = name
        self.balance = balance
        self.prestige = prestige
        self.released_movies = []

    def act_month(self, market_pool, calendar):
        """Simple AI to simulate rival activity."""
        actions = []

        # Random chance to buy a script, prefers trending genres
        if market_pool.scripts and random.random() < 0.3:
            # Prioritize buying scripts in trending genres
            trending_scripts = [s for s in market_pool.scripts if s['genre'] in calendar.trending_genres]
            script_to_buy = random.choice(trending_scripts) if trending_scripts else random.choice(market_pool.scripts)
            
            if self.balance >= script_to_buy.get("value", 5):
                self.balance -= script_to_buy["value"]
                market_pool.scripts.remove(script_to_buy)
                actions.append(f"{self.name} acquired script '{script_to_buy['title']}'.")

        # Random chance to sign a high-fame actor
        if market_pool.actors and random.random() < 0.2:
            top_actors = sorted(market_pool.actors, key=lambda x: x.get("fame", 0), reverse=True)
            if top_actors:
                actor = top_actors[0] # Rivals go for top talent
                market_pool.actors.remove(actor)
                actions.append(f"{self.name} signed top actor {actor['name']}.")

        return actions