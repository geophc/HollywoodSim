# post_production.py

import random

# ---- Campaign Types ----
MARKETING_PLANS = {
    "None": {"cost": 0, "buzz": 0, "desc": "No marketing, rely on word of mouth."},
    "Modest": {"cost": 2, "buzz": 5, "desc": "Grassroots/viral attempt, cheap but risky."},
    "Standard": {"cost": 5, "buzz": 10, "desc": "Balanced campaign, steady gains."},
    "Aggressive": {"cost": 10, "buzz": 15, "desc": "Big push, lots of coverage."},
    "Blockbuster": {"cost": 30, "buzz": 35, "desc": "Massive hype, short-term explosion."},
    "Prestige": {"cost": 5, "buzz": 12, "desc": "Critics/festival campaign, boosts awards chances."},
}

RELEASE_STRATEGIES = {
    "Wide": {"multiplier": 1.2, "longevity": -0.2, "desc": "Nationwide release, strong start, fast decline."},
    "Limited": {"multiplier": 0.6, "longevity": +0.3, "desc": "Small rollout, builds over time."},
    "Streaming": {"multiplier": 0.8, "longevity": 0.0, "desc": "Flat revenue curve, no huge opening."},
    "International": {"multiplier": 1.1, "longevity": +0.1, "desc": "Target overseas, boosts Action/Animation."},
}

def run_post_production_phase(studio, calendar):
    """Handles marketing + distribution planning for scheduled movies before release."""
    print("\n🎬 Post-Production Phase")
    if not studio.scheduled_movies:
        print("📭 No movies currently in post-production.")
        return

    for movie in studio.scheduled_movies:
        print(f"\n--- {movie['title']} ---")
        print(f"Release Date: {movie['release_date'][1]}/{movie['release_date'][0]}")
        print(f"Current Buzz: {movie.get('buzz', 0)} | Budget Class: {movie['budget_class']}")

        # ---- Marketing Choice ----
        print("\n📣 Marketing Campaign Options:")
        for i, (plan, data) in enumerate(MARKETING_PLANS.items(), 1):
            print(f"{i}. {plan} — ${data['cost']}M | +{data['buzz']} Buzz | {data['desc']}")
        m_choice = input(f"Choose marketing plan (1-{len(MARKETING_PLANS)}) or [Enter] to skip: ").strip()
        if m_choice.isdigit() and 1 <= int(m_choice) <= len(MARKETING_PLANS):
            plan_name = list(MARKETING_PLANS.keys())[int(m_choice) - 1]
            plan = MARKETING_PLANS[plan_name]
            movie["buzz"] = movie.get("buzz", 0) + plan["buzz"]
            studio.balance -= plan["cost"]
            studio.total_expenses += plan["cost"]
            movie["marketing_plan"] = plan_name
            
            # ADD THIS LINE to make it compatible with studio.py's simulation
            movie["marketing_spend"] = plan["cost"] 
            
            print(f"✅ Selected {plan_name} marketing. New Buzz: {movie['buzz']}")
        else:
            print("⏩ No marketing selected.")

        # ---- Release Strategy ----
        print("\n🎥 Release Strategies:")
        for i, (strategy, data) in enumerate(RELEASE_STRATEGIES.items(), 1):
            print(f"{i}. {strategy} — {data['desc']}")
        r_choice = input(f"Choose release strategy (1-{len(RELEASE_STRATEGIES)}) or [Enter] default Wide: ").strip()
        if r_choice.isdigit() and 1 <= int(r_choice) <= len(RELEASE_STRATEGIES):
            strat_name = list(RELEASE_STRATEGIES.keys())[int(r_choice) - 1]
            movie["release_strategy"] = strat_name
            print(f"✅ Release strategy set: {strat_name}")
        else:
            movie["release_strategy"] = "Wide"
            print("➡️ Default release: Wide")

        # Tagging for later revenue sim
        movie.setdefault("buzz", 0)
        movie.setdefault("marketing_plan", "None")
        movie.setdefault("release_strategy", "Wide")


def apply_distribution_effects(movie):
    """
    Called during revenue simulation to apply strategy modifiers.
    """
    strat = RELEASE_STRATEGIES.get(movie.get("release_strategy", "Wide"), {})
    return strat.get("multiplier", 1.0), strat.get("longevity", 0.0)
