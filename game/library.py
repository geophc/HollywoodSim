# library.py
import random
from game_data import SCRIPT_RESALE



def manage_script_library(studio):
    print("\n\U0001F4DA Script Library Options:")
    print("1. Move a script to shelf")
    print("2. View shelf")
    print("3. Sell all shelved scripts")
    print("Press [Enter] to skip.")

    choice = input("Choose an option: ").strip().lower()
    if not choice:
        return

    if choice == "1":
        # Show only non-released scripts
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
            print(f"\U0001F4E6 Moved '{script['title']}' to the shelf.")
        else:
            print("Invalid selection.")

    elif choice == "2":
        if not studio.script_library:
            print("\U0001F5C3️ Shelf is empty.")
            return
        print("\n\U0001F5C3️ Scripts on the Shelf:")
        for s in studio.script_library:
            value = get_script_resale_value(s, studio.calendar)
            print(f"- {s['title']} (Potential: {s['potential_quality']}, Status: {s['status']}, Value: ${value}M)")

        if not studio.script_library:
            print("\U0001F5D1️ Shelf is empty. Nothing to sell.")
            return
        total = 0
        for script in studio.script_library:
            value = get_script_resale_value(script, studio.calendar)
            total += value
        studio.cash += total
        print(f"\U0001F4B0 Sold {len(studio.script_library)} scripts for ${total:.2f}M.")
        studio.script_library.clear()

    else:
        print("Invalid input. Returning to game.")


def get_script_resale_value(script, calendar=None):
    """Calculates current resale value of a shelved script."""
    base = SCRIPT_RESALE["base_multiplier"]
    volatility = random.uniform(-SCRIPT_RESALE["volatility"], SCRIPT_RESALE["volatility"])
    genre_bonus = SCRIPT_RESALE["genre_bonus"].get(script["genre"], 0)

    multiplier = base + volatility + genre_bonus
    value = round(script["potential_quality"] * multiplier, 2)
    return max(value, 0.1)  # ensure minimum floor
