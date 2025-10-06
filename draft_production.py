# HollywoodSim/game/draft_production.py

"""
Expanded production drafting system for HollywoodSim.
Handles selecting script, casting lead roles, attaching director,
and assigning staff for production + post-production.

This version:
 - Uses signed talent first (from studio.contracts) then free agents (casting_pool)
 - Does not assume non-existent fields like `skill` or `salary` on staff objects
 - Stores staff assignments on the movie dict for future phases
 - Marks the script as 'in_production' after scheduling
 - Returns the scheduled movie (or None)
"""

from personnel import generate_staff_member


def _pick_from_signed_then_pool(signed_contracts, pool_choices, role_name):
    """
    Helper: present signed people first (if any) then pool choices.
    signed_contracts is a list of contract dicts (each with "person").
    pool_choices is a list of person dicts.
    Returns the chosen person dict or None.
    """
    options = []

    # add signed talent (contract -> person)
    for c in signed_contracts:
        if "person" in c:
            p = c["person"]
            options.append(("signed", p))

    # add free agents from pool_choices
    for p in pool_choices:
        options.append(("free", p))

    if not options:
        return None

    print(f"\n{role_name} options:")
    for i, (tag, p) in enumerate(options, 1):
        tag_mark = "(Signed)" if tag == "signed" else "(Free)"
        # show basic, safe fields
        extra = []
        if p.get("fame") is not None:
            extra.append(f"Fame {p.get('fame')}")
        if p.get("age") is not None:
            extra.append(f"Age {p.get('age')}")
        if p.get("genre_focus"):
            extra.append(f"Focus {p.get('genre_focus')}")
        if p.get("tags"):
            extra.append(", ".join(p.get("tags")))
        print(f"{i}. {p.get('name', 'Unknown')} {tag_mark} — {' | '.join(extra)}")

    idx = input(f"Select {role_name} number (or press Enter to cancel): ").strip()
    if not idx:
        print("Canceled selection.")
        return None
    if not idx.isdigit() or not (1 <= int(idx) <= len(options)):
        print("❌ Invalid choice.")
        return None

    _, person = options[int(idx) - 1]
    return person


def draft_production(studio, calendar, casting_pool, market_pool):
    """
    Walk the player through drafting a movie production.
    Includes script selection, casting, director, and staff.
    Returns the scheduled movie dict (or None on cancel/failure).
    """
    # Step 0: Ensure there are scripts
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
        print(f"{i}. {s['title']} ({s['genre']} — Quality {s.get('quality',0)} / Appeal {s.get('appeal',0):.2f})")
    idx = input("Select a script number (or press Enter to cancel): ").strip()
    if not idx:
        print("Canceled drafting.")
        return None
    if not idx.isdigit() or not (1 <= int(idx) <= len(approved_scripts)):
        print("❌ Invalid choice.")
        return None
    script = approved_scripts[int(idx) - 1]

    # --- Step 2: Choose Lead Actor ---
    # signed actors from contracts
    signed_actor_contracts = studio.contracts.get("actors", [])
    actor_pool = casting_pool.get_actor_choices(3)
    actor = _pick_from_signed_then_pool(signed_actor_contracts, actor_pool, "Actor")
    if not actor:
        print("⚠️ No actor selected; aborting draft.")
        return None

    # --- Step 3: Choose Director ---
    signed_dir_contracts = studio.contracts.get("directors", [])
    director_pool = casting_pool.get_director_choices(3)
    director = _pick_from_signed_then_pool(signed_dir_contracts, director_pool, "Director")
    if not director:
        print("⚠️ No director selected; aborting draft.")
        return None

    # --- Step 4: Assign Staff (Post-production & Support) ---
    required_staff_roles = ["Editor", "Sound Designer", "Marketing Manager"]
    staff_assignments = {}
    print("\n👩‍💻 Assign Staff (Post-Production & Support):")
    for role in required_staff_roles:
        # prefer studio signed staff (contracts), then market pool
        signed_staff_contracts = [c for c in studio.contracts.get("staff", []) if c.get("person", {}).get("role") == role]
        # flatten to person objects
        signed_people = [c["person"] for c in signed_staff_contracts if "person" in c]
        available_market = [s for s in market_pool.staff if s.get("role") == role]

        # if nothing in market, generate one and add to market
        if not available_market and not signed_people:
            new_staff = generate_staff_member(role, calendar.year)
            # attempt to provide a salary/experience field if absent (non-destructive)
            if "salary" not in new_staff:
                # estimate a salary from fame/experience if present
                est = round((new_staff.get("fame", 30) * 0.02) + (new_staff.get("experience", 1) * 0.01), 2)
                new_staff["salary"] = est
            market_pool.add_staff(new_staff)
            available_market = [new_staff]

        # present choices: signed first, then market
        choices = signed_people + available_market
        if not choices:
            print(f"⚠️ No available candidates for {role}.")
            continue

        print(f"\n{role} options:")
        for i, s in enumerate(choices, 1):
            # show safe fields
            parts = [f"Experience {s.get('experience','N/A')}"]
            if s.get("specialty"):
                parts.append(f"Specialty: {s.get('specialty')}")
            if s.get("fame") is not None:
                parts.append(f"Fame {s.get('fame')}")
            # salary might not exist; if not, show estimated
            salary = s.get("salary") if s.get("salary") is not None else round((s.get("fame",30)*0.02),2)
            parts.append(f"Salary ${salary}M")
            print(f"{i}. {s.get('name','Unknown')} — {' | '.join(parts)}")

        idx = input(f"Select {role} number (or press Enter to skip): ").strip()
        if not idx:
            print(f"⏩ Skipping assignment of {role}.")
            continue
        if not idx.isdigit() or not (1 <= int(idx) <= len(choices)):
            print(f"⚠️ Invalid choice for {role}, skipping.")
            continue

        picked = choices[int(idx) - 1]
        staff_assignments[role] = picked

        # optional: remove from market if picked from market (so they aren't double-hired)
        if picked in market_pool.staff:
            try:
                market_pool.staff.remove(picked)
            except ValueError:
                pass

    # --- Step 5: Release Window ---
    months_ahead_str = input("\n📆 Choose a release window (1–6 months from now): ").strip()
    months_ahead = int(months_ahead_str) if months_ahead_str.isdigit() else 1
    months_ahead = max(1, min(months_ahead, 6))

    # --- Step 6: Produce / Schedule Movie ---
    movie = studio.produce_movie(
        script,
        [actor],
        director,
        calendar,
        staff_assignments,
        months_ahead
    )

    if not movie:
        print("❌ Production failed (insufficient funds or scheduling error).")
        return None

    # store staff assignments for future application in post-production
    movie["staff"] = staff_assignments

    # mark script status so other systems know it's in production
    script["status"] = "in_production"

    # Inform player
    print(f"\n✅ Drafted '{movie.get('title','Untitled')}' with {actor.get('name')} and {director.get('name')}.")
    if staff_assignments:
        staff_list = ", ".join(f"{r}: {s.get('name')}" for r, s in staff_assignments.items())
        print(f"   👩‍💻 Staff: {staff_list}")
    print(f"   Scheduled Release: {movie['release_date'][1]}/{movie['release_date'][0]}")
    return movie
