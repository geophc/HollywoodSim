# HollywoodSim/game/library.py
import random
from game_data import SCRIPT_RESALE

def manage_script_library(studio):
    print("\n📚 Script Library Options:")
    print("1. Move a script to shelf")
    print("2. View shelf")
    print("3. Sell one script from shelf")
    print("4. Sell all shelved scripts")
    print("[Enter] to skip.")

    choice = input("Choose an option: ").strip()
    if not choice:
        return

    if choice == "1":
        move_script_to_shelf(studio)

    elif choice == "2":
        view_shelf(studio)

    elif choice == "3":
        sell_one_from_shelf(studio)

    elif choice == "4":
        sell_all_from_shelf(studio)

    else:
        print("Invalid input. Returning to game.")

def move_script_to_shelf(studio):
    active = [s for s in studio.scripts if s["status"] != "released"]
    if not active:
        print("No scripts available to move.")
        return
    print("\nAvailable scripts:")
    for i, s in enumerate(active, 1):
        print(f"{i}. {s['title']} (Status: {s['status']}, Quality: {s['quality']}/{s['potential_quality']})")
    idx = input("Enter number to move to shelf: ").strip()
    if idx.isdigit() and 1 <= int(idx) <= len(active):
        script = active[int(idx)-1]
        studio.scripts.remove(script)
        studio.script_library.append(script)
        print(f"📦 Moved '{script['title']}' to the shelf.")
    else:
        print("Invalid selection.")

def view_shelf(studio):
    if not studio.script_library:
        print("🗃️ Shelf is empty.")
        return
    print("\n🗃️ Scripts on the Shelf:")
    for s in studio.script_library:
        value = get_script_resale_value(s, getattr(studio, "calendar", None))
        print(f"- {s['title']} (Potential: {s['potential_quality']}, Status: {s['status']}, Value: ${value}M)")

def sell_one_from_shelf(studio):
    if not studio.script_library:
        print("🗃️ Shelf is empty.")
        return
    print("\nChoose a script to sell:")
    for i, s in enumerate(studio.script_library, 1):
        value = get_script_resale_value(s, getattr(studio, "calendar", None))
        print(f"{i}. {s['title']} - Value: ${value}M")
    idx = input("Enter number to sell: ").strip()
    if idx.isdigit() and 1 <= int(idx) <= len(studio.script_library):
        script = studio.script_library.pop(int(idx)-1)
        value = get_script_resale_value(script, getattr(studio, "calendar", None))
        studio.balance += value
        print(f"💰 Sold '{script['title']}' for ${value:.2f}M.")
    else:
        print("Invalid selection.")

def sell_all_from_shelf(studio):
    if not studio.script_library:
        print("🗃️ Shelf is empty. Nothing to sell.")
        return
    total = 0
    for script in studio.script_library:
        total += get_script_resale_value(script, getattr(studio, "calendar", None))
    studio.balance += total
    count = len(studio.script_library)
    studio.script_library.clear()
    print(f"💰 Sold {count} scripts for ${total:.2f}M.")

def get_script_resale_value(script, calendar=None):
    """Calculates current resale value of a shelved script."""
    base = SCRIPT_RESALE["base_multiplier"]
    volatility = random.uniform(-SCRIPT_RESALE["volatility"], SCRIPT_RESALE["volatility"])
    genre_bonus = SCRIPT_RESALE["genre_bonus"].get(script["genre"], 0)

    multiplier = base + volatility + genre_bonus
    value = round(script["potential_quality"] * multiplier, 2)
    return max(value, 0.1)  # ensure minimum floor
