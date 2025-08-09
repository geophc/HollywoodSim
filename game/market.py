# market.py

import random
from personnel import generate_actor, generate_director, generate_writer
from scripts import generate_script
from game_data import SEASONS
from casting import CastingPool, CastingManager

# Global market state
global_pool = {
    "scripts": [],
    "actors": [],
    "directors": [],
    "writers": []
}

# Initialize a new market pool
def init_market():
    return global_pool

# Add a single item to the market pool
def add_to_market(pool, kind, item):
    if kind in pool:
        pool[kind].append(item)

# Refresh market contents for the new month
def refresh_market(pool, casting_pool, calendar, studio):
    """
    Each month, add new writers, actors, directors, and scripts to the market.
    """
    for _ in range(2):
        pool["actors"].append(generate_actor(calendar.year))
        pool["directors"].append(generate_director(calendar.year))
        pool["writers"].append(generate_writer(calendar.year))

    # Generate new scripts from available writers
    for writer in random.sample(pool["writers"], min(2, len(pool["writers"]))):
        script = generate_script(calendar, writer)
        script["value"] = round(script["potential_quality"] * 0.25, 2)
        pool["scripts"].append(script)

# Visualize the current market state
def view_market(pool):
    print("\n🛒 Free Market Snapshot")
    print("Available Scripts:")

    def appeal_level(potential):
        if potential >= 75:
            return "High"
        elif potential >= 50:
            return "Medium"
        return "Low"

    def buzz_rating(potential):
        if potential >= 85:
            return "🔥 Hot"
        elif potential >= 70:
            return "Trending"
        elif potential >= 50:
            return "Lukewarm"
        return "Cold"

    for i, script in enumerate(pool["scripts"], 1):
        appeal = appeal_level(script["potential_quality"])
        buzz = buzz_rating(script["potential_quality"])
        print(f"{i}. {script['title']} ({script['genre']}, Rated: {script['rating']})")
        print(f"   ✨ Appeal: {appeal} | Buzz: {buzz} | Potential: {script['potential_quality']} | Price: ${script['value']}M")

    print("\n📌 Appeal Levels: Low (<50), Medium (50–74), High (75+)")
    print("📡 Buzz Ratings: 🔥 Hot (85+), Trending (70–84), Lukewarm (50–69), Cold (<50)")

    print("\nTop Available Actors:")
    for actor in sorted(pool["actors"], key=lambda x: -x["fame"])[:5]:
        print(f"- {actor['name']} (Fame: {actor['fame']}, Tags: {', '.join(actor['tags'])})")

# Purchase logic for a script from the market
def buy_script_from_market(pool, studio):
    if not pool["scripts"]:
        print("No scripts available for purchase this month.")
        return

    view_market(pool)
    choice = input("\nEnter script number to buy or [enter] to skip: ").strip()
    if not choice or not choice.isdigit():
        print("Skipped script purchase.")
        return

    index = int(choice) - 1
    if index >= len(pool["scripts"]):
        print("Invalid choice.")
        return

    script = pool["scripts"][index]
    cost = script["value"]

    if studio.balance < cost:
        print(f"❌ Not enough funds to buy '{script['title']}' — costs ${cost}M, you have ${studio.balance:.2f}M.")
        return

    studio.balance -= cost
    studio.scripts.append(script)
    pool["scripts"].remove(script)
    print(f"✅ Purchased script: {script['title']} for ${cost}M.")

# Main interface for interacting with the market
def visit_market(studio, market):
    print("\n🌍 Visit the Free Market")
    while True:
        print("\n[1] View Market")
        print("[2] Buy Script")
        print("[Enter] Return to studio")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_market(market)
        elif choice == "2":
            buy_script_from_market(market, studio)
        else:
            print("🛍️ Leaving the Free Market and returning to the studio.")
            break

# Apply seasonal multipliers to script value
def adjust_market_values_by_season(pool, season):
    genre_multipliers = SEASONS[season]["genre_boosts"]
    for script in pool["scripts"]:
        multiplier = genre_multipliers.get(script["genre"], 1.0)
        script["value"] = round(script["potential_quality"] * 0.25 * multiplier, 2)

# Shared transfer logic
def handle_talent_transfer(studio_from, studio_to, talent, fee):
    if studio_to.balance < fee:
        print(f"❌ {studio_to.name} cannot afford to transfer {talent['name']} for ${fee}M.")
        return

    studio_to.balance -= fee
    studio_from.balance += fee
    studio_to.hire(talent)
    studio_from.release(talent)
    print(f"✅ {talent['name']} transferred from {studio_from.name} to {studio_to.name} for ${fee}M.")

# Estimate movie buzz/pre-release value
def estimate_pre_release_value(movie, season):
    buzz_score = (
        movie["script"]["potential_quality"]
        + movie["director"]["fame"]
        + sum(actor["fame"] for actor in movie["cast"])
    )
    seasonal_boost = SEASONS[season].get("genre_boosts", {}).get(movie["script"]["genre"], 1.0)
    return round(buzz_score * 0.1 * seasonal_boost, 2)

# Basic studio talent handling (attach to Studio class in actual implementation)
def hire(self, talent):
    kind = talent.get("role")
    if kind == "actor":
        self.actor_pool.append(talent)
        self.contracts["actors"].append(talent)
    elif kind == "director":
        self.contracts["directors"].append(talent)
    elif kind == "writer":
        self.contracts["writers"].append(talent)

def release(self, talent):
    kind = talent.get("role")
    if kind == "actor":
        if talent in self.actor_pool:
            self.actor_pool.remove(talent)
        if talent in self.contracts["actors"]:
            self.contracts["actors"].remove(talent)
    elif kind == "director" and talent in self.contracts["directors"]:
        self.contracts["directors"].remove(talent)
    elif kind == "writer" and talent in self.contracts["writers"]:
        self.contracts["writers"].remove(talent)
