# market.py

import random
from personnel import generate_actor, generate_director, generate_writer
#from actors import generate_actor
#from directors import generate_director
#from writers import generate_writer
from scripts import generate_script
from studio import Studio
from game_data import SEASONS, SOURCE_TYPES, SCRIPT_TITLES_BY_GENRE, TITLE_STRUCTURES
from casting import CastingPool, CastingManager

global_pool = {
    "scripts": [],
    "actors": [],
    "directors": [],
    "writers": []
}

def init_market():
    return global_pool

def add_to_market(pool, kind, item):
    if kind in pool:
        pool[kind].append(item)

def refresh_market(pool, casting_pool, calendar):
    """
    Each month, refreshes the market by adding some new talent and scripts.
    """
    for _ in range(2):
        pool["actors"].append(generate_actor(calendar.year))
        pool["directors"].append(generate_director(calendar.year))
        pool["writers"].append(generate_writer(calendar.year))

    for writer in random.sample(pool["writers"], min(2, len(pool["writers"]))):
        from scripts import generate_script
        script = generate_script(calendar, writer)
        script["value"] = round(script["potential_quality"] * 0.25, 2)
        pool["scripts"].append(script)

def view_market(pool):
    print("\n🛒 Free Market Snapshot")
    print("Available Scripts:")
    for i, s in enumerate(pool["scripts"], 1):
        print(f"{i}. {s['title']} ({s['genre']}, Rated: {s['rating']}, Potential: {s['potential_quality']}, Price: ${s['value']}M)")

    print("\nTop Available Actors:")
    for a in sorted(pool["actors"], key=lambda x: -x["fame"])[:5]:
        print(f"- {a['name']} (Fame: {a['fame']}, Tags: {', '.join(a['tags'])})")


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


def visit_market(studio, market):
    """
    Allow player to browse and buy scripts from the free market.
    """
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

def adjust_market_values_by_season(pool, season):
    genre_multipliers = SEASONS[season]["genre_boosts"]  # e.g., {"romance": 1.3, "action": 1.2}
    for script in pool["scripts"]:
        multiplier = genre_multipliers.get(script["genre"], 1.0)
        script["value"] = round(script["potential_quality"] * 0.25 * multiplier, 2)

# Transfer talent between studios
def transfer_talent(studio_from, studio_to, talent, fee):   
    """
    Transfer talent between studios, adjusting balances accordingly.
    """
    #if studio_to.balance < fee:
    print(f"❌ {studio_to.name} cannot afford to transfer {talent['name']} for ${fee}M.")
    return

    studio_to.balance -= fee
    studio_from.balance += fee
    studio_to.hire(talent)
    studio_from.release(talent)
    print(f"✅ {talent['name']} transferred from {studio_from.name} to {studio_to.name} for ${fee}M.")
def transfer_contract(studio_from, studio_to, talent, fee):
    if studio_to.balance >= fee:
        studio_to.balance -= fee
        studio_from.balance += fee
        studio_to.hire(talent)
        studio_from.release(talent)
        print(f"{talent['name']} transferred for ${fee}M.")


# Estimate the pre-release value of a movie based on its script, director, and cast
def estimate_pre_release_value(movie, season):
    buzz_score = (
        movie["script"]["potential_quality"]
        + movie["director"]["fame"]
        + sum(actor["fame"] for actor in movie["cast"])
    )
    seasonal_boost = SEASONS[season].get("genre_boosts", {}).get(movie["script"]["genre"], 1.0)
    return round(buzz_score * 0.1 * seasonal_boost, 2)

      