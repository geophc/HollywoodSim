# main.py

import random
import events


from scripts import generate_script, finalize_script, rewrite_script
from personnel import (
    generate_actor,
    generate_writer,
    generate_director,
    generate_staff_member,
    CastingPool,
    CastingManager,
    TalentPool,
)
from studio import Studio
from calendar import GameCalendar
from contracts import (
    find_active_contracts,
    print_roster,
)
from library import manage_script_library
from market import init_market, refresh_market, visit_market
from game_data import STAFF_SPECIALTIES


# --- Utility Functions ---
def print_banner():
    """Prints the game's welcome banner."""
    print("🎬 Welcome to HollywoodSim!")


def display_game_state(calendar, studio, casting_pool):
    """Displays the current state of the game, including date, finances, and studio stats."""
    print("\n" + "=" * 60)
    print(f"📅  DATE: {calendar.display():<20}     💰 BALANCE: ${studio.balance:,.2f}M")
    print("=" * 60)
    print(f"🔥 Trending Genres       : {', '.join(calendar.trending_genres)}")
    print(f"🔮 Next Quarter Forecast : {', '.join(calendar.forecast_genres)}")
    print()
    print(f"🏦 Studio Prestige       : 👑 {studio.prestige}")
    print(f"💰 Total Earnings        : ${studio.total_earnings:,.2f}M")
    print(f"💸 Total Expenses        : ${studio.total_expenses:,.2f}M")
    print()
    print(
        f"🎭 Talent Pool           : {len(casting_pool.actors)} Actors | {len(casting_pool.writers)} Writers"
    )
    print(f"🎬 In Production         : {len(studio.scheduled_movies)}")
    print(f"📽️  Released Films        : {len(studio.released_movies)}")
    print(
        f"🏆 Top-Grossing Film     : {studio.highest_grossing['title'] if studio.highest_grossing else 'N/A'}"
    )
    print("=" * 60 + "\n")


def input_number(prompt, valid_choices):
    """Safely gets a numerical input from the user from a list of valid choices."""
    while True:
        val = input(prompt).strip()
        if not val:
            return None
        if val in valid_choices:
            return int(val)
        print(f"Invalid input. Expected one of: {', '.join(valid_choices)}")


def choose_item(prompt, items, formatter):
    """Generic function to display a list of items and get a user's choice."""
    for i, item in enumerate(items, 1):
        print(f"{i}. {formatter(item)}")
    valid_choices = [str(i) for i in range(1, len(items) + 1)]
    choice = input_number(prompt, valid_choices)
    if choice:
        return items[choice - 1]
    return None


# --- Game Setup Functions ---
def generate_starting_free_agents(calendar, market_pool):
    """Generates initial market talent (actors, directors, writers, staff)."""
    START_ACTORS = 30
    START_DIRECTORS = 5
    START_WRITERS = 10
    START_STAFF_PER_ROLE = 3

    for _ in range(START_ACTORS):
        market_pool.add_actor(generate_actor(calendar.year))
    for _ in range(START_DIRECTORS):
        market_pool.add_director(generate_director(calendar.year))
    for _ in range(START_WRITERS):
        market_pool.add_writer(generate_writer(calendar.year))
    for role in STAFF_SPECIALTIES.keys():
        for _ in range(START_STAFF_PER_ROLE):
            market_pool.add_staff(generate_staff_member(role, calendar.year))


def game_setup(calendar, studio, market_pool, casting_pool):
    """Initializes the market and studio for a new game."""
    print("\n--- Setting up HollywoodSim ---")
    generate_starting_free_agents(calendar, market_pool)
    casting_pool.clear()
    print(
        f"Market initialized with {len(market_pool.actors)} actors, "
        f"{len(market_pool.directors)} directors, "
        f"{len(market_pool.writers)} writers, and "
        f"{len(market_pool.staff)} staff members."
    )


# --- Phase-Specific Functions ---
def run_market_phase(market_pool, casting_pool, calendar, studio):
    """Handles the monthly market activities."""
    print("\n🛒 Market Phase:")
    refresh_market(market_pool, casting_pool, calendar, studio)
    market_choice = (
        input("\n🏬 Would you like to visit the Free Market this month? [y]/[Enter]: ")
        .strip()
        .lower()
    )
    if market_choice == "y":
        visit_market(studio, market_pool)
    else:
        print("⏩ Skipping market visit this month.")

    # 🎭 Optional check for roster viewing before next phase
    roster_choice = (
        input("\n👥 Would you like to view your studio roster? Type 'view_roster' or press [Enter] to continue: ")
        .strip()
        .lower()
    )
    if roster_choice == "view_roster":
        print_roster(studio)


def calculate_script_buzz(script, calendar=None):
    """Calculates the buzz rating for a given script."""
    base_quality = script.get("potential_quality", 50)
    tag_bonus = len(script.get("tags", [])) * 2
    appeal_bonus = int((script.get("appeal", 0.5)) * 10)
    writer_bonus = 0
    writer = script.get("writer", {})
    if writer:
        specialty = writer.get("specialty", {})
        if isinstance(specialty, dict):
            writer_bonus += specialty.get("prestige_multiplier", 1.0) * 2
            if calendar and calendar.season in specialty.get("peak_seasons", []):
                writer_bonus += 3
    trend_bonus = 0
    if calendar and script.get("genre") in calendar.trending_genres:
        trend_bonus += 5
    return int((base_quality * 0.3) + tag_bonus + appeal_bonus + writer_bonus + trend_bonus)

def get_contracted_writers(studio):
    return [
        c for c in studio.contracts.get("writers", [])
        if "person" in c and "name" in c["person"]
    ]

 

def inhouse_script_production(scripts):
    """Displays in-house scripts and prompts the user to greenlight one."""
    print("\n🎞️ Production Slate Review")
    
    # Only show scripts that are finalized and not yet in production
    available_scripts = [s for s in scripts if s.get("status") == "finalized"]

    if not available_scripts:
        print("📭 No finalized scripts available for production.")
        return None

    print("Available In-House Scripts:")

    def get_appeal_level(score):
        potential = int(score * 100)
        return "High" if potential >= 75 else "Medium" if potential >= 50 else "Low"

    def buzz_rating(score):
        potential = int(score * 100)
        if potential >= 85:
            return "🔥 Hot"
        elif potential >= 70:
            return "Trending"
        elif potential >= 50:
            return "Lukewarm"
        else:
            return "Cold"

    for i, s in enumerate(available_scripts, 1):
        potential = int(s["appeal"] * 100)
        appeal = get_appeal_level(s["appeal"])
        buzz = buzz_rating(s["appeal"])
        writer = s["writer"]
        print(f"{i}. {s['title']} ({s['genre']}, Rated: {s['rating']})")
        print(
            f"   ✨ Appeal: {appeal} | Buzz: {buzz} | Potential: {potential} | Budget Class: {s['budget_class']}"
        )
        print(f"   🏷️ Tags: {', '.join(s['tags'])}")
        print(
            f"   ✍️ Writer: {writer['name']} ({writer['specialty']['name']}) | Interests: {', '.join(writer['interests'])} | School: {writer['education']}"
        )

    print("\n📌 Appeal Levels: Low (<50), Medium (50–74), High (75+)")
    print("📡 Buzz Ratings: 🔥 Hot (85+), Trending (70–84), Lukewarm (50–69), Cold (<50)")

    choice = input_number(
        "Enter number to greenlight (or press [enter] to skip): ",
        [str(i + 1) for i in range(len(available_scripts))],
    )

    if choice is not None:
        selected = available_scripts[int(choice) - 1]
        selected["status"] = "in_production"  # mark script as moved into production
        return selected
    
    return None


# --- in main.py ---
def manage_scripts(managed_scripts, casting_pool, calendar, studio):
    """Allows the player to manage scripts, choosing to finalize or rewrite."""
    if not managed_scripts:
        return

    print("\n📚 Script Management:")
    for i, s in enumerate(managed_scripts, 1):
        print(
            f"{i}. {s['title']} ({s['genre']}, Draft {s['draft_number']}) "
            f"— Status: {s['status']} | Quality: {s['quality']}/{s['potential_quality']}"
        )

    choice = input("Enter script number to manage or [Enter] to skip: ").strip()
    if not choice or not choice.isdigit():
        return

    selected = managed_scripts[int(choice) - 1]
    action = input("Type [f] to finalize or [r] to rewrite: ").strip().lower()

    if action == "f":
        finalize_script(selected, studio, calendar)


    elif action == "r":
        signed_writers = [
            c["person"] for c in studio.contracts.get("writers", [])
            if "person" in c and "name" in c["person"]
        ]
        needed = max(0, 3 - len(signed_writers))
        free_agents = casting_pool.get_writer_choices(needed) if needed > 0 else []
        rewrite_choices = signed_writers + free_agents

        print("\n✍️ Choose a writer to rewrite the script:")
        writer_choice = choose_item(
            "Enter number: ",
            rewrite_choices,
            lambda w: (
                f"{w['name']} | Specialty: {w['specialty']['name']} | "
                f"Interests: {', '.join(w['interests'])} | School: {w['education']}"
            )
        )
        if writer_choice:
            rewrite_script(selected, writer_choice, calendar)



def display_scripts_for_production(scripts):
    """Displays scripts that are approved and ready for production."""
    # The 'scripts' list is now passed in directly, so we no longer need the old logic to find them.
    if not scripts:
        print("📭 No scripts available for production.")
        return

    print("\n📜 Available Scripts for Production\n")
    budget_meanings = {
        "Low": "Low (Under $25M)",
        "Mid": "Mid ($25–60M)",
        "High": "High (Over $60M)",
    }
    for idx, script in enumerate(scripts, 1):
        buzz = calculate_script_buzz(script)
        budget_desc = budget_meanings.get(script.get("budget_class", "Unknown"))
        writer = script.get("writer", {})
        print(f"{idx}. {script['title']} ({script['genre']}, Rated: {script.get('rating', 'NR')})")
        print(f"   ✨ Appeal: {script.get('appeal', 0.0):.2f} | Buzz: {buzz} | Budget: {budget_desc}")
        print(f"   🏷️ Tags: {', '.join(script.get('tags', []) or ['None'])}")
        print(f"   ✍️ Writer: {writer.get('name', 'Unknown')} ({writer.get('specialty', {}).get('name', 'N/A')})")


def produce_film(studio, script, calendar, casting_pool, casting_manager):
    """
    Guides the player through producing a new film.
    
    Steps:
      1. Select a director (must be available in free agent pool).
      2. Select a lead actor (prefer signed staff, fallback to free agents).
      3. Pick release window (1–6 months ahead).
      4. Schedule the film and apply bonuses/synergies.
    """

    # --- Step 1: Director selection ---
    # First check if studio has signed directors under contract
    signed_directors = [
        c["person"] for c in studio.contracts.get("directors", []) if "person" in c and "name" in c["person"]
    ]

    # Determine how many more choices are needed to reach a target of 3
    needed = max(0, 3 - len(signed_directors))
    free_agents = casting_pool.get_director_choices(needed) if needed > 0 else []

    # Combine the lists, signed directors will be listed first
    all_directors = signed_directors + free_agents

    if all_directors:  # <--- use the combined list here
        print("\n🎬 Choose a director for your film:")

        def director_fmt(d):
            name = d.get("name", "Unknown")
            fame = d.get("fame", 0)
            hist = casting_manager.get_history(name)
            note = (
                f"🎞️ Past: {hist['count']}x | Avg Q: {hist['avg_quality']:.1f} | "
                f"Box: ${hist['avg_box_office']:.1f}M"
                if hist
                else "🆕 No history"
            )
            genre = d.get("genre_focus", "N/A")
            style = ", ".join(d.get("tags", []))
            return f"{name} — Fame: {fame} | Genre: {genre} | Style: {style} | {note}"

        director = choose_item("Enter number: ", all_directors, director_fmt)
    else:
        print("⚠️ No directors available for production this month.")
        return None

    
    # --- Step 2: Actor selection ---
    # First check if studio has signed actors under contract
    signed_actors = [
        c["person"] for c in studio.contracts.get("actors", []) if "person" in c and "name" in c["person"]
    ]

    # Determine how many more choices are needed
    needed = max(0, 3 - len(signed_actors))
    free_agents = casting_pool.get_actor_choices(needed) if needed > 0 else []

    # Combine the lists
    all_actors = signed_actors + free_agents

    if all_actors:  # <--- use the combined list here
        print("\n🎬 Choose an actor for your film:")

        def actor_fmt(a):
            name = a.get("name", "Unknown")
            fame = a.get("fame", 0)
            salary = a.get("salary", 0)
            tags = ", ".join(a.get("tags", []))
            hist = casting_manager.get_history(name)
            note = (
                f"🎞️ Past: {hist['count']}x | Avg Q: {hist['avg_quality']:.1f} | "
                f"Box: ${hist['avg_box_office']:.1f}M"
                if hist
                else "🆕 No history"
            )
            return f"{name} — Fame: {fame} | Salary: ${salary}M [{tags}] | {note}"

        actor = choose_item("Enter number: ", all_actors, actor_fmt)
    else:
        print("⚠️ No actors available for production this month.")
        return None


    # --- Step 3: Release window selection ---
    months_ahead_str = input("\n📆 Choose a release window (1–6 months from now): ").strip()
    months_ahead = int(months_ahead_str) if months_ahead_str.isdigit() else 1
    months_ahead = max(1, min(months_ahead, 6))  # clamp between 1–6 months


    # --- Step 4: Schedule movie in studio ---
    movie = studio.produce_movie(script, actor, director, calendar, months_ahead)

    if movie:
        print(
            f"\n🗓️ Scheduled: {movie['title']} ({movie['genre']}, {movie['budget_class']})"
            f"\n   Cast: {actor['name']} | Director: {director['name']}"
            f"\n   Release: {movie['release_date'][1]}/{movie['release_date'][0]}"
            f"\n   Cost: ${movie['cost']}M"
        )

        # Check for synergy bonuses between actor and script
        matching_tags = set(script["tags"]) & set(actor["tags"])
        if matching_tags:
            print(f"✨ Tag synergy bonus! Matching tags: {', '.join(matching_tags)}")

    else:
        print("⚠️ Skipped production due to insufficient funds.")

    return movie




# --- End-of-Year Report ---
def print_awards_summary(awards):
    """Prints the end-of-year awards summary."""
    print("\n🎖️ End of Year Awards:")
    print(f"🏅 Best Picture: {awards['Best Picture']['title']} (Quality: {awards['Best Picture']['quality']})")
    print(f"🌟 Star of the Year: {awards['Star of the Year']['name']} (Fame: {awards['Star of the Year']['fame']})")
    director_award = awards.get("Best Director")
    if director_award:
        print(f"🎥 Best Director: {director_award['name']} (Fame: {director_award['fame']})")
    else:
        print("🎥 No Best Director award this year.")


def print_studio_summary(studio):
    """Prints the studio's financial and prestige summary."""
    print("\n📊 Studio Summary:")
    print(f"🎬 Films Released: {len(studio.released_movies)}")
    print(f"💵 Total Earnings: ${studio.total_earnings:.2f}M")
    print(f"💸 Total Expenses: ${studio.total_expenses:.2f}M")
    print(f"👑 Final Prestige: {studio.prestige}")
    print(f"🏁 Final Balance: ${studio.balance:.2f}M")
    if studio.highest_grossing:
        hg = studio.highest_grossing
        print(f"🏅 Top Earner: {hg['title']} (${hg['box_office']}M, Quality: {hg['quality']})")


def print_filmography(movies):
    """Prints a recap of all films released by the studio."""
    print("\n🎞️ Studio Filmography Recap:")
    for movie in movies:
        writer = movie.get("writer", {}).get("name", "Unknown")
        director = movie.get("director", {}).get("name", "Unknown")
        actor = movie.get("cast", {}).get("name", "Unknown")
        print(
            f"🎬 {movie['title']} ({movie['genre']}, {movie['budget_class']}) - "
            f"Released {movie['release_date'][1]}/{movie['release_date'][0]} | "
            f"Quality: {movie['quality']} | Box Office: ${movie['box_office']}M"
        )
        print(f"     ✍️ Writer: {writer} 🎬 Director: {director} 🎭 Lead: {actor}")


def print_actor_recap(actors):
    """Prints a career recap for actors who worked with the studio."""
    print("\n🎭 Actor Career Recap:")
    for actor in actors:
        films = actor.get("film_history", [])
        if not films:
            continue
        avg_quality = sum(f["quality"] for f in films) / len(films)
        avg_box_office = sum(f["box_office"] for f in films) / len(films)
        print(f"\n🧑 {actor['name']} — Age: {actor['age']} | Debut: {actor['debut_year']}")
        print(f"🎬 Films: {len(films)} | Avg Quality: {avg_quality:.1f} | Avg Box Office: ${avg_box_office:.1f}M")
        for f in films:
            print(f"   🎬 {f['title']} ({f['year']}) - Quality: {f['quality']}, Earnings: ${f['box_office']}M")


def print_talent_recap(talent_list, role_emoji, role_title):
    """Generic function to print a recap for a list of talent (writers, directors)."""
    print(f"\n{role_emoji} {role_title} Recap:")
    for talent in talent_list:
        films = talent.get("film_history", [])
        if not films:
            continue
        avg_quality = sum(f["quality"] for f in films) / len(films)
        summary = f"{role_emoji} {talent['name']} — Films: {len(films)}, Avg Quality: {avg_quality:.1f}"
        if "box_office" in films[0]:
            avg_box_office = sum(f["box_office"] for f in films) / len(films)
            summary += f", Avg Box Office: ${avg_box_office:.1f}M"
        print(summary)


def end_of_year_report(studio, casting_pool):
    """Handles the display of all end-of-year summaries and reports."""
    awards = studio.evaluate_awards()
    if awards:
        print_awards_summary(awards)
    else:
        print("\n🤷 No awards this year — better luck next time!")

    print_studio_summary(studio)

    seen = set()
    used_actors = []
    for m in studio.released_movies:
        actor = m["cast"]
        if actor["name"] not in seen:
            seen.add(actor["name"])
            used_actors.append(actor)

    print_filmography(studio.released_movies)
    print_actor_recap(used_actors)
    print_talent_recap(casting_pool.writers, "🖋️", "Writer")
    print_talent_recap(casting_pool.directors, "🎬", "Director")

    if studio.is_bankrupt():
        print("\n☠️  You ended in bankruptcy. Try again with better budgeting!")
    else:
        print("\n🎉 You survived the year in Hollywood!")


# --- Main Game Loop ---
def hollywood_sim():
    """The main function that runs the game simulation."""
    # Setup
    calendar = GameCalendar()
    casting_pool = CastingPool()
    studio = Studio(year=calendar.year)
    casting_manager = CastingManager()
    market_pool = init_market()
    

    # Populate initial talent pools
    for _ in range(30):
        casting_pool.add_actor(generate_actor(calendar.year))
    for _ in range(10):
        casting_pool.add_writer(generate_writer(calendar.year))
    for _ in range(5):
        casting_pool.add_director(generate_director(calendar.year))

    print_banner()

    # Main game loop for 12 months
    for _ in range(12):
        display_game_state(calendar, studio, casting_pool)

        if studio.is_bankrupt():
            print("💀 Your studio is bankrupt! You can no longer produce films.")
            print("🧾 Consider releasing existing movies to earn money...")
        else:
            run_market_phase(market_pool, casting_pool, calendar, studio)

            # --- Script Development Phase ---
            writers = get_contracted_writers(studio)

            if not writers:
                print("You have no contracted writers! Hire one before generating a script.")
            else:
                # Let player choose a writer safely
                print("Select a contracted writer to assign the script to (or press Enter to skip):")
                for i, w in enumerate(writers, 1):
                    print(f"{i}. {w['person']['name']} (Fame {w['person']['fame']}, Style {', '.join(w['person']['signature_tags'])})")

                selected_writer = None
                while True:
                    choice_str = input("Choose writer: ").strip()
                    if choice_str == "":
                        print("⏩ Skipped script assignment this month.")
                        break
                    if choice_str.isdigit() and 1 <= int(choice_str) <= len(writers):
                        selected_writer = writers[int(choice_str) - 1]["person"]
                        break
                    print(f"⚠️ Invalid choice. Enter a number between 1 and {len(writers)}, or press Enter to skip.")

                # Generate script only if a writer was selected
                if selected_writer:
                    script = generate_script(calendar, selected_writer)
                    studio.scripts.append(script)
                    print(f"✅ New script '{script['title']}' written by {selected_writer['name']}!")


            script_idx = inhouse_script_production(studio.scripts)
            if script_idx is not None:
                selected_script = studio.scripts[script_idx - 1]

            # Script Management Phase
            scheduled_titles = {m["title"] for m in studio.scheduled_movies}
            released_titles = {m["title"] for m in studio.released_movies}
            managed_scripts = [
                s
                for s in studio.scripts
                if s["title"] not in scheduled_titles and s["title"] not in released_titles
            ]
            manage_scripts(managed_scripts, casting_pool, calendar, studio)

            # Production Phase
            approved_scripts = [
                s
                for s in studio.scripts
                if s["status"] == "approved"
                and s["title"] not in scheduled_titles
                and s["title"] not in released_titles
            ]
            display_scripts_for_production(approved_scripts)

            if approved_scripts:
                prod_choice_str = input(
                    "Enter number of script to produce, or press [Enter] to skip this month: "
                ).strip()
                if (
                    prod_choice_str
                    and prod_choice_str.isdigit()
                    and 1 <= int(prod_choice_str) <= len(approved_scripts)
                ):
                    produce_film(
                        studio,
                        approved_scripts[int(prod_choice_str) - 1],
                        calendar,
                        casting_pool,
                        casting_manager,
                    )
                else:
                    print("⏩ Skipping production this month.")

        # Monthly Updates
        for movie in studio.check_for_releases(calendar):
            print(
                f"💥 Released: {movie['title']} | Earnings: ${movie.get('box_office', '(Est.)')}M | Quality: {movie['quality']}"
            )
            casting_manager.record_collaboration(movie["cast"], movie)
            score, review = studio.generate_review(movie)
            print(f"📝 Critics Score: {score}/100 — {review}")

        if studio.is_bankrupt() and not studio.scheduled_movies:
            print("\n💔 Your studio has no movies in production and is bankrupt.")
            print("☠️ GAME OVER.")
            end_of_year_report(studio, casting_pool)
            return  # End the simulation immediately

        studio.update_revenue()
        print("\n📈 Monthly Revenue Update:")
        for movie in studio.released_movies:
            if movie.get("monthly_revenue"):
                print(f"• {movie['title']}: ${movie['monthly_revenue'][0]}M incoming")

        expense = studio.expenses()
        print(
            f"💸 Monthly Expenses: - Base $15M, Staff ${len(studio.released_movies)*0.2:.2f}M, Production ${len(studio.scheduled_movies):.2f}M, Prestige ${studio.prestige*0.1:.2f}M = Total ${expense['total']:.2f}M"
        )

        if studio.newsfeed:
            print("\n📰 Hollywood News:")
            for story in studio.newsfeed[-3:]:
                print(f"• {story}")

        # Advance time and run events
        calendar.advance()
        events.run_random_events(studio, calendar)

    # End of simulation after 12 months
    end_of_year_report(studio, casting_pool)


if __name__ == "__main__":
    hollywood_sim()