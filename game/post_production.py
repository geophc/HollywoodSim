# draft_production.py

"""
Expanded production drafting system for HollywoodSim.
Handles selecting script, casting lead roles, attaching director, 
and assigning staff for production + post-production.
"""

from personnel import generate_staff_member

def draft_production(studio, calendar, casting_pool, market_pool):
    """
    Walk the player through drafting a movie production.
    Includes script selection, casting, director, and staff.
    """
    if not studio.scripts:
        print("📭 No scripts available. Generate or acquire one first.")
        return None

    # --- Step 1: Choose Script ---
    print("\n📜 Available Scripts:")
    approved_scripts = [s for s in studio.scripts if s.get("status") == "approved"]
    if not approved_scripts:
        print("⚠️ No approved scripts available for production.")
        return None

    for i, s in enumerate(approved_scripts, 1):
        print(f"{i}. {s['title']} ({s['genre']} — Quality {s['quality']} / Appeal {s['appeal']:.2f})")
    idx = input("Select a script number: ").strip()
    if not idx.isdigit() or not (1 <= int(idx) <= len(approved_scripts)):
        print("❌ Invalid choice.")
        return None
    script = approved_scripts[int(idx) - 1]

    # --- Step 2: Choose Actor ---
    actors = casting_pool.get_actor_choices(3)
    if not actors:
        print("⚠️ No actors available.")
        return None
    print("\n🎭 Actor Choices:")
    for i, a in enumerate(actors, 1):
        print(f"{i}. {a['name']} — Fame {a['fame']} | Salary ${a['salary']}M | Tags: {', '.join(a['tags'])}")
    idx = input("Select an actor number: ").strip()
    if not idx.isdigit() or not (1 <= int(idx) <= len(actors)):
        print("❌ Invalid choice.")
        return None
    actor = actors[int(idx) - 1]

    # --- Step 3: Choose Director ---
    directors = casting_pool.get_director_choices(3)
    if not directors:
        print("⚠️ No directors available.")
        return None
    print("\n🎬 Director Choices:")
    for i, d in enumerate(directors, 1):
        print(f"{i}. {d['name']} — Fame {d['fame']} | Focus {d.get('genre_focus', 'N/A')}")
    idx = input("Select a director number: ").strip()
    if not idx.isdigit() or not (1 <= int(idx) <= len(directors)):
        print("❌ Invalid choice.")
        return None
    director = directors[int(idx) - 1]

    # --- Step 4: Assign Staff ---
    required_staff_roles = ["Editor", "Sound Designer", "Marketing Manager"]
    staff_assignments = {}
    print("\n👩‍💻 Assign Staff (Post-Production & Support):")
    for role in required_staff_roles:
        available_staff = [s for s in market_pool.staff if s["role"] == role]
        if not available_staff:
            # auto-generate if none exist
            new_staff = generate_staff_member(role, calendar.year)
            market_pool.add_staff(new_staff)
            available_staff = [new_staff]

        print(f"\n{role} options:")
        for i, s in enumerate(available_staff, 1):
            print(f"{i}. {s['name']} — Skill {s['skill']} | Salary ${s['salary']}M")
        idx = input(f"Select {role} number: ").strip()
        if idx.isdigit() and (1 <= int(idx) <= len(available_staff)):
            staff_assignments[role] = available_staff[int(idx) - 1]
        else:
            print(f"⚠️ No {role} assigned.")

    # --- Step 5: Release Window ---
    months_ahead_str = input("\n📆 Choose a release window (1–6 months from now): ").strip()
    months_ahead = int(months_ahead_str) if months_ahead_str.isdigit() else 1
    months_ahead = max(1, min(months_ahead, 6))

    # --- Step 6: Produce Movie ---
    movie = studio.produce_movie(script, actor, director, calendar, months_ahead)

    if movie:
        # ✅ Store staff for future phases (no bonuses applied yet)
        movie["staff"] = staff_assignments

        print(f"\n✅ Drafted '{movie['title']}' with {actor['name']} and {director['name']}")
        if staff_assignments:
            staff_list = ", ".join(f"{r}: {s['name']}" for r, s in staff_assignments.items())
            print(f"   👩‍💻 Staff: {staff_list}")
        print(f"   Scheduled Release: {movie['release_date'][1]}/{movie['release_date'][0]}")
    else:
        print("❌ Production failed due to insufficient funds.")

