# market.py

import random
from personnel import generate_actor, generate_writer, generate_director, generate_staff_member
from scripts import generate_script
from contracts import create_contract
from game_data import SEASONS, STAFF_SPECIALTIES

class MarketPool:
    def __init__(self):
        self.scripts = []
        self.actors = []
        self.directors = []
        self.writers = []
        self.staff = []

    # Convenience methods
    def add_actor(self, actor): self.actors.append(actor)
    def add_director(self, director): self.directors.append(director)
    def add_writer(self, writer): self.writers.append(writer)
    def add_staff(self, staff): self.staff.append(staff)
    def add_script(self, script): self.scripts.append(script)


def init_market():
    return MarketPool()


def add_to_market(pool, kind, item):
    if hasattr(pool, kind):
        getattr(pool, kind).append(item)


def refresh_market(pool, casting_pool, calendar, studio):
    MAX_STAFF = 20
    if len(pool.staff) > MAX_STAFF:
        pool.staff = pool.staff[-MAX_STAFF:]

    # Add new talent safely
    pool.add_actor(generate_actor(calendar.year))
    pool.add_director(generate_director(calendar.year))
    pool.add_writer(generate_writer(calendar.year))

    # Generate scripts
    if pool.writers:
        for writer in random.sample(pool.writers, min(2, len(pool.writers))):
            script = generate_script(calendar, writer)
            script["value"] = round(script["potential_quality"] * 0.25, 2)
            pool.add_script(script)

    # Add staff
    staff_roles = list(STAFF_SPECIALTIES.keys())
    for _ in range(2):
        role = random.choice(staff_roles)
        pool.add_staff(generate_staff_member(role, calendar.year))


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

    # --- Scripts Section ---
    for i, script in enumerate(pool.scripts, 1):
        appeal = appeal_level(script["potential_quality"])
        buzz = buzz_rating(script["potential_quality"])
        print(f"{i}. {script['title']} ({script['genre']}, Rated: {script['rating']})")
        print(f"   ✨ Appeal: {appeal} | Buzz: {buzz} | Potential: {script['potential_quality']} | Price: ${script['value']}M")
        print(f"   🏷️ Tags: {', '.join(script.get('tags', []))}")
        print(f"   ✍️ Writer: {script['writer']['name'] if script.get('writer') else 'TBD'}")

    print("\n📌 Appeal Levels: Low (<50), Medium (50–74), High (75+)")
    print("📡 Buzz Ratings: 🔥 Hot (85+), Trending (70–84), Lukewarm (50–69), Cold (<50)")

    # --- Talent Section ---
    def print_top(talent_list, title):
        if not talent_list:
            print(f"\nNo {title} available.")
            return
        print(f"\nTop Available {title}:")
        for t in sorted(talent_list, key=lambda x: -x.get("fame", 0))[:5]:
            tags = ', '.join(t.get("tags", []))
            info_lines = [
                f"- {t['name']} (Fame: {t.get('fame',0)})",
                f"   Age: {t.get('age', 'N/A')}, Salary: ${t.get('salary', 0)}M",
            ]
            if "specialty" in t:
                info_lines.append(f"   Specialty: {t['specialty']}")
            if "experience" in t:
                info_lines.append(f"   Experience: {t['experience']} years")
            if "education" in t:
                info_lines.append(f"   Education: {t['education']}")
            if "signature_tags" in t:
                info_lines.append(f"   Signature Tags: {', '.join(t['signature_tags'])}")
            if "genre_focus" in t:
                info_lines.append(f"   Genre Focus: {t['genre_focus']}")
            print("\n".join(info_lines))

    print_top(pool.actors, "Actors")
    print_top(pool.directors, "Directors")
    print_top(pool.writers, "Writers")
    print_top(pool.staff, "Staff Members")



def buy_script_from_market(pool, studio):
    if not pool.scripts:
        print("No scripts available for purchase this month.")
        return

    view_market(pool)
    choice = input("\nEnter script number to buy or [enter] to skip: ").strip()
    if not choice or not choice.isdigit():
        print("Skipped script purchase.")
        return

    index = int(choice) - 1
    if index >= len(pool.scripts):
        print("Invalid choice.")
        return

    script = pool.scripts[index]
    cost = script.get("value", 0)

    if studio.balance < cost:
        print(f"❌ Not enough funds to buy '{script['title']}' — costs ${cost}M, you have ${studio.balance:.2f}M.")
        return

    studio.balance -= cost
    studio.scripts.append(script)
    pool.scripts.remove(script)
    print(f"✅ Purchased script: {script['title']} for ${cost}M.")


def sign_talent_from_market(pool, studio):
    print("\n📑 Sign Talent")
    categories = {
        "1": ("actors", pool.actors),
        "2": ("directors", pool.directors),
        "3": ("writers", pool.writers),
        "4": ("staff", pool.staff),
        "": (None, None),
    }
    print("1. Actor\n2. Director\n3. Writer\n4. Staff\n[Enter] Cancel")
    choice = input("Choose category: ").strip()
    if choice not in categories or choice == "":
        print("❌ Cancelled.")
        return

    role, candidates = categories[choice]
    if not candidates:
        print("No candidates available.")
        return

    for i, c in enumerate(candidates[:5], 1):
        if role == "writers":
            specialty = c.get("specialty", {}).get("name", "General")
            interests = ", ".join(c.get("interests", [])) or "None"
            tags = ", ".join(c.get("signature_tags", [])) or "None"
            print(f"{i}. {c['name']} — Fame: {c.get('fame', 0)}, Salary: ${c.get('salary', 1.0)}M")
            print(f"   ✍️ Genre/Specialty: {specialty}")
            print(f"   🎯 Interests: {interests}")
            print(f"   🏷️ Signature Tags: {tags}")
        else:
            print(f"{i}. {c['name']} — Fame: {c.get('fame', 0)}, Salary: ${c.get('salary', 1.0)}M")

    idx = input("Select number to sign: ").strip()
    if not idx.isdigit() or not (1 <= int(idx) <= len(candidates)):
        print("❌ Invalid selection.")
        return

    selected = candidates[int(idx) - 1]
    months = input("Contract length (1–12): ").strip()
    if not months.isdigit() or not (1 <= int(months) <= 12):
        print("❌ Invalid duration.")
        return

    contract = create_contract(selected, role, int(months), selected.get("salary", 1.0))
    studio.contracts[role].append(contract)
    studio.hire(selected)
    pool.__getattribute__(role).remove(selected)

    print(f"✅ Signed {selected['name']} for {months} months.")


def visit_market(studio, market):
    print("\n🌍 Visit the Free Market")
    while True:
        print("\n[1] View Market")
        print("[2] Buy Script")
        print("[3] Sign Talent")
        print("[Enter] Return to studio")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_market(market)
        elif choice == "2":
            buy_script_from_market(market, studio)
        elif choice == "3":
            sign_talent_from_market(market, studio)
        else:
            print("🛍️ Leaving the Free Market and returning to the studio.")
            break

def adjust_market_values_by_season(pool, season):
    genre_multipliers = SEASONS.get(season, {}).get("genre_boosts", {})
    for script in pool.scripts:
        multiplier = genre_multipliers.get(script.get("genre", ""), 1.0)
        script["value"] = round(script.get("potential_quality", 50) * 0.25 * multiplier, 2)


def handle_talent_transfer(studio_from, studio_to, talent, fee):
    if studio_to.balance < fee:
        print(f"❌ {studio_to.name} cannot afford to transfer {talent['name']} for ${fee}M.")
        return

    studio_to.balance -= fee
    studio_from.balance += fee
    studio_to.hire(talent)
    studio_from.release(talent)
    print(f"✅ {talent['name']} transferred from {studio_from.name} to {studio_to.name} for ${fee}M.")


def estimate_pre_release_value(movie, season):
    buzz_score = (
        movie["script"].get("potential_quality", 50)
        + movie["director"].get("fame", 0)
        + sum(actor.get("fame", 0) for actor in movie.get("cast", []))
    )
    seasonal_boost = SEASONS.get(season, {}).get("genre_boosts", {}).get(movie["script"].get("genre", ""), 1.0)
    return round(buzz_score * 0.1 * seasonal_boost, 2)
