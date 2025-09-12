# main.py

import random
import events


from scripts import generate_script, finalize_script, rewrite_script, generate_script_description
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
from market import init_market, refresh_market, visit_market, adjust_market_prices
from game_data import STAFF_SPECIALTIES
from draft_production import draft_production
from post_production import run_post_production_phase
from rivals import RivalStudio


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

def get_contracted_writers(studio):
    return [
        c for c in studio.contracts.get("writers", [])
        if "person" in c and "name" in c["person"]
    ]

# --- in main.py ---
def manage_scripts(managed_scripts, casting_pool, calendar, studio):
    """Allows the player to manage scripts, choosing to finalize or rewrite."""
    if not managed_scripts:
        return

    print("\n📚 Script Management:")
    for i, s in enumerate(managed_scripts, 1):
        desc = s.get("description") or generate_script_description(s)
        print(f"{i}. {s['title']} ({s['genre']}, Draft {s['draft_number']})")
        print(f" 📝 Status: {s['status']} | Quality: {s['quality']}/{s['potential_quality']}")
        print(f" 📖 {desc}")

    choice = input("Enter script number to manage or [Enter] to skip: ").strip()
    if not choice or not choice.isdigit():
        return

    selected = managed_scripts[int(choice) - 1]
    action = input("Type [f] to finalize or [r] to rewrite: ").strip().lower()

    if action == "f":
        finalize_script(selected, studio, calendar)
        selected["status"] = "approved"  # mark as approved and ready for production


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
            selected["status"] = "draft" # ✅ Keep draft status until finalized


def display_scripts_for_production(scripts):
    """Displays scripts that are approved and ready for production."""
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
            buzz = script.get("buzz", 0)
            budget_desc = budget_meanings.get(script.get("budget_class", "Unknown"))
            writer = script.get("writer", {})
            print(f"{idx}. {script['title']} ({script['genre']}, Rated: {script.get('rating', 'NR')})")
            print(f" ✨ Appeal: {script.get('appeal', 0.0):.2f} | Buzz: {buzz} | Budget: {budget_desc}")
            print(f" 🏷️ Tags: {', '.join(script.get('tags', []) or ['None'])}")
            print(f" ✍️ Writer: {writer.get('name', 'Unknown')} ({writer.get('specialty', {}).get('name', 'N/A')})")
            print(f" 📖 {script.get('description', generate_script_description(script))}")
            

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


def print_writer_recap(scripts):
    """Prints a recap of writers who contributed scripts this year, regardless of being hired."""
    print("\n🖋️ Writer Contribution Recap:")

    writer_stats = {}

    for s in scripts:
        writer = s.get("writer")
        if not writer:
            continue
        name = writer["name"]
        if name not in writer_stats:
            writer_stats[name] = {
                "scripts": 0,
                "avg_quality": 0,
                "genres": set(),
                "appeal_sum": 0,
            }
        writer_stats[name]["scripts"] += 1
        writer_stats[name]["avg_quality"] += s.get("quality", 0)
        writer_stats[name]["appeal_sum"] += s.get("appeal", 0)
        writer_stats[name]["genres"].add(s.get("genre", "Unknown"))

    for name, stats in writer_stats.items():
        count = stats["scripts"]
        avg_quality = stats["avg_quality"] / count
        avg_appeal = stats["appeal_sum"] / count
        genres = ", ".join(stats["genres"])
        print(
            f"✍️ {name} — Scripts: {count}, Avg Quality: {avg_quality:.1f}, "
            f"Avg Appeal: {avg_appeal:.2f}, Genres: {genres}"
        )


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
    game_setup(calendar, studio, market_pool, casting_pool)

    # Rival studios
    rival_studios = [
        RivalStudio("Silver Screen Studios", balance=150, prestige=10),
        RivalStudio("Golden Gate Films", balance=120, prestige=8),
        RivalStudio("Sunset Pictures", balance=100, prestige=5),
    ]
    print(f"🏢 Competing against: {', '.join(r.name for r in rival_studios)}")

    # Populate starting talent pool
    for _ in range(30):
        casting_pool.add_actor(generate_actor(calendar.year))
    for _ in range(10):
        casting_pool.add_writer(generate_writer(calendar.year))
    for _ in range(5):
        casting_pool.add_director(generate_director(calendar.year))

    print_banner()

    # --- Main Loop: 12 Months ---
    for _ in range(12):
        display_game_state(calendar, studio, casting_pool)

        if studio.is_bankrupt():
            print("💀 Your studio is bankrupt! You can no longer produce films.")
            break

        # 1. Refresh Market
        refresh_market(market_pool, casting_pool, calendar, studio)
        print("\n🛒 Market refreshed with new scripts & talent.")

        # 2. Rivals Act
        print("\n🏢 Rival studios are making their moves...")
        for rival in rival_studios:
            actions = rival.act_month(market_pool, calendar)
            for action in actions:
                print(f"   - {action}")

        # 3. Market Prices Adjust
        adjust_market_prices(market_pool, calendar)
        print("📉 Market prices adjusted based on supply & demand.")

        # 4. Player Market Phase
        run_market_phase(market_pool, casting_pool, calendar, studio)

        # 5. Script Development
        writers = get_contracted_writers(studio)
        if writers:
            print("Select a contracted writer to generate a new script:")
            for i, w in enumerate(writers, 1):
                person = w["person"]
                print(f"{i}. {person['name']} (Fame {person.get('fame', 0)}, Style {', '.join(person.get('signature_tags', []))})")
            choice = input("Choose writer [Enter to skip]: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(writers):
                selected_writer = writers[int(choice) - 1]["person"]
                script = generate_script(calendar, selected_writer)
                studio.scripts.append(script)
                print(f"✅ New script '{script['title']}' written by {selected_writer['name']}!")

        # 6. Script Management
        scheduled_titles = {m["title"] for m in studio.scheduled_movies}
        released_titles = {m["title"] for m in studio.released_movies}
        managed_scripts = [
            s for s in studio.scripts
            if s["title"] not in scheduled_titles and s["title"] not in released_titles
        ]
        manage_scripts(managed_scripts, casting_pool, calendar, studio)

        # 7. Draft Production
        print("\n🎬 Drafting Production...")
        draft_production(studio, calendar, casting_pool, market_pool)

        # 8. Post-Production & Marketing
        run_post_production_phase(studio, calendar)

        # 9. Releases
        releases = studio.check_for_releases(calendar)
        for movie in releases:
            logs = studio.apply_post_production(movie)
            for l in logs:
                print(f"🛠️ {movie['title']} — {l}")
            print(f"💥 Released: {movie['title']} (Quality: {movie.get('quality')})")
            casting_manager.record_collaboration(movie.get("cast", {}), movie)
            score, review = studio.generate_review(movie)
            print(f"📝 Critics: {score}/100 — {review}")

        # 10. Monthly Revenue
        studio.update_revenue()
        print("\n📈 Revenue Update:")
        for movie in studio.released_movies:
            if movie.get("monthly_revenue"):
                print(f"• {movie['title']}: ${movie['monthly_revenue'][0]:.2f}M")

        # 11. Monthly Expenses
        expense = studio.expenses()
        print(f"💸 Expenses: Total ${expense['total']:.2f}M")

        # 12. Events & News
        events.run_random_events(studio, calendar)
        if studio.newsfeed:
            print("\n📰 Hollywood News:")
            for story in studio.newsfeed[-3:]:
                print(f"• {story}")

        # 13. Advance Time
        calendar.advance()

    # End of Year Report
    end_of_year_report(studio, casting_pool)



if __name__ == "__main__":
    hollywood_sim()