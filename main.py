# HollywoodSim/game/main.py


import sys
import random

# --- Core Systems ---
from studio import Studio
from calendar_1 import GameCalendar
from rivals import RivalStudio
from contracts import print_roster
import events

# --- Personnel & Casting ---
from personnel import (
    generate_actor,
    generate_writer,
    generate_director,
    generate_staff_member,
    STAFF_SPECIALTIES,
    CastingPool,
    CastingManager,
)

# --- Scripts ---
from scripts import (
    generate_script,
    finalize_script,
    rewrite_script,
    generate_script_description,  # make sure this exists in scripts.py
)

# --- Market ---
from market import (
    init_market,
    refresh_market,
    adjust_market_prices,
    visit_market,
)

# --- Production ---
from draft_production import draft_production
from post_production import run_post_production_phase


# --- Utility Functions ---
def print_banner():
    print("🎬 Welcome to HollywoodSim!")


def display_game_state(calendar, studio, casting_pool):
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
    print(f"🎭 Talent Pool           : {len(casting_pool.actors)} Actors | {len(casting_pool.writers)} Writers")
    print(f"🎬 In Production         : {len(studio.scheduled_movies)}")
    print(f"📽️  Released Films        : {len(studio.released_movies)}")
    print(f"🏆 Top-Grossing Film     : {studio.highest_grossing['title'] if studio.highest_grossing else 'N/A'}")
    print(f"📝 Scripts on Hand       : {len(studio.scripts)}")
    print("=" * 60 + "\n")


def input_number(prompt, valid_choices):
    """
    valid_choices: iterable of string choices (e.g. ['1','2','3'])
    Returns: int(choice) or None on cancel/empty
    """
    valid_set = set(valid_choices)
    while True:
        val = input(prompt).strip()
        if val == "":
            return None
        if val.lower() in {"q", "quit", "cancel"}:
            return None
        if val in valid_set:
            return int(val)
        print(f"Invalid input. Expected one of: {', '.join(sorted(valid_choices))} (or press Enter to cancel)")



def choose_item(prompt, items, formatter):
    for i, item in enumerate(items, 1):
        print(f"{i}. {formatter(item)}")
    valid_choices = [str(i) for i in range(1, len(items) + 1)]
    choice = input_number(prompt, valid_choices)
    if choice:
        return items[choice - 1]
    return None


# --- Game Setup ---
def generate_starting_free_agents(calendar, market_pool):
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
    print("\n--- Setting up HollywoodSim ---")
    generate_starting_free_agents(calendar, market_pool)
    casting_pool.clear()
    print(
        f"Market initialized with {len(market_pool.actors)} actors, "
        f"{len(market_pool.directors)} directors, "
        f"{len(market_pool.writers)} writers, and "
        f"{len(market_pool.staff)} staff members."
    )


# --- Market Phase ---
def run_market_phase(market_pool, casting_pool, calendar, studio):
    print("\n🛒 Market Phase:")
    refresh_market(market_pool, casting_pool, calendar, studio)
    market_choice = input("\n🏬 Visit the Free Market this month? [y]/[Enter]: ").strip().lower()
    if market_choice == "y":
        visit_market(studio, market_pool)
    else:
        print("⏩ Skipping market visit this month. (You can still manage scripts or draft production.)")


    roster_choice = input("\n👥 View studio roster? Type 'view_roster' or press [Enter]: ").strip().lower()
    if roster_choice == "view_roster":
        print_roster(studio)


def get_contracted_writers(studio):
    return [c for c in studio.contracts.get("writers", []) if "person" in c and "name" in c["person"]]


# --- Script Management ---
def manage_scripts(managed_scripts, casting_pool, calendar, studio):
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
        selected["status"] = "approved"

    elif action == "r":
        signed_writers = [c["person"] for c in studio.contracts.get("writers", []) if "person" in c]
        needed = max(0, 3 - len(signed_writers))
        free_agents = casting_pool.get_writer_choices(needed) if needed > 0 and hasattr(casting_pool, "get_writer_choices") else []
        rewrite_choices = signed_writers + free_agents

        if not rewrite_choices:
            print("⚠️ No available writers to rewrite the script.")
        else:
            print("\n✍️ Choose a writer to rewrite the script:")
            writer_choice = choose_item(
                "Enter number: ",
                rewrite_choices,
                lambda w: f"{w.get('name','Unknown')} | Specialty: {w.get('specialty',{}).get('name','N/A')} | Interests: {', '.join(w.get('interests',[]))}"
            )
            if writer_choice:
                rewrite_script(selected, writer_choice, calendar)
                selected["status"] = "draft"




def display_scripts_for_production(scripts):
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
        print(f" ✍️ Writer: {writer.get('name', 'Unknown')}")


# --- End of Year ---
def print_awards_summary(awards):
    print("\n🎖️ End of Year Awards:")
    print(f"🏅 Best Picture: {awards['Best Picture']['title']} (Quality: {awards['Best Picture']['quality']})")
    print(f"🌟 Star of the Year: {awards['Star of the Year']['name']} (Fame: {awards['Star of the Year']['fame']})")
    director_award = awards.get("Best Director")
    if director_award:
        print(f"🎥 Best Director: {director_award['name']} (Fame: {director_award['fame']})")


def print_studio_summary(studio):
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
    print("\n🎞️ Studio Filmography Recap:")
    for movie in movies:
        writer = movie.get("writer", {}).get("name", "Unknown")
        director = movie.get("director", {}).get("name", "Unknown")
        cast = movie.get("cast", [])
        lead = cast[0]["name"] if cast else "Unknown"

        # Release date can be stored various ways; try to handle common forms
        rd = movie.get("release_date")
        if isinstance(rd, (list, tuple)) and len(rd) >= 2:
            # try (year, month) or (month, day)
            release_str = f"{rd[1]}/{rd[0]}"
        elif isinstance(rd, str):
            release_str = rd
        else:
            release_str = "Unknown"

        print(f"🎬 {movie['title']} ({movie.get('genre','Unknown')}, {movie.get('budget_class','Unknown')}) - Released {release_str} | Quality: {movie.get('quality','N/A')} | Box Office: ${movie.get('box_office', 0):.1f}M")
        print(f"     ✍️ Writer: {writer} 🎬 Director: {director} 🎭 Lead: {lead}")


def print_actor_recap(actors):
    print("\n🎭 Actor Career Recap:")
    for actor in actors:
        films = actor.get("film_history", [])
        if not films:
            continue
        avg_quality = sum(f["quality"] for f in films) / len(films)
        avg_box_office = sum(f["box_office"] for f in films) / len(films)
        print(f"\n🧑 {actor['name']} — Age: {actor['age']} | Debut: {actor['debut_year']}")
        print(f"🎬 Films: {len(films)} | Avg Quality: {avg_quality:.1f} | Avg Box Office: ${avg_box_office:.1f}M")

def print_talent_recap(talent_list, icon, role_name):
    """
    Print a simple recap for a list of talent (writers/directors).
    Expects talent_list to be an iterable of dicts with 'name', 'fame' optionally.
    """
    if not talent_list:
        print(f"\n{icon} No {role_name}s to recap.")
        return

    print(f"\n{icon} {role_name} Recap:")
    for person in talent_list:
        name = person.get("name", "Unknown")
        fame = person.get("fame", 0)
        credits = len(person.get("film_history", [])) if person.get("film_history") else 0
        print(f" • {name} — Fame: {fame} | Credits: {credits}")


def end_of_year_report(studio, casting_pool):
    awards = studio.evaluate_awards()
    if awards:
        print_awards_summary(awards)
    else:
        print("\n🤷 No awards this year.")

    print_studio_summary(studio)

    seen = set()
    used_actors = []
    for m in studio.released_movies:
        for actor in m.get("cast", []):
            if actor["name"] not in seen:
                seen.add(actor["name"])
                used_actors.append(actor)

    print_filmography(studio.released_movies)
    print_actor_recap(used_actors)
    print_talent_recap(casting_pool.writers, "🖋️", "Writer")
    print_talent_recap(casting_pool.directors, "🎬", "Director")


# --- Main Loop ---
def hollywood_sim():
    calendar = GameCalendar()
    casting_pool = CastingPool()
    studio = Studio(year=calendar.year)
    casting_manager = CastingManager()
    market_pool = init_market()
    game_setup(calendar, studio, market_pool, casting_pool)

    rival_studios = [
        RivalStudio("Silver Screen Studios", balance=150, prestige=10),
        RivalStudio("Golden Gate Films", balance=120, prestige=8),
        RivalStudio("Sunset Pictures", balance=100, prestige=5),
    ]
    print(f"🏢 Competing against: {', '.join(r.name for r in rival_studios)}")

    for _ in range(30):
        casting_pool.add_actor(generate_actor(calendar.year))
    for _ in range(10):
        casting_pool.add_writer(generate_writer(calendar.year))
    for _ in range(5):
        casting_pool.add_director(generate_director(calendar.year))

    print_banner()

    for _ in range(12):
        display_game_state(calendar, studio, casting_pool)

        if studio.is_bankrupt():
            print("💀 Your studio is bankrupt!")
            break

        refresh_market(market_pool, casting_pool, calendar, studio)
        print("\n🛒 Market refreshed.")

        print("\n🏢 Rival studios move...")
        for rival in rival_studios:
            for action in rival.act_month(market_pool, calendar):
                print(f"   - {action}")

        adjust_market_prices(market_pool, calendar)
        print("📉 Market prices adjusted.")

        run_market_phase(market_pool, casting_pool, calendar, studio)

        writers = get_contracted_writers(studio)
        if writers:
            print("Select a contracted writer to generate a script:")
            for i, w in enumerate(writers, 1):
                person = w["person"]
                print(f"{i}. {person['name']} (Fame {person.get('fame', 0)})")
            choice = input("Choose writer [Enter to skip]: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(writers):
                selected_writer = writers[int(choice) - 1]["person"]
                script = generate_script(calendar, selected_writer)
                studio.scripts.append(script)
                print(f"✅ New script '{script['title']}' written by {selected_writer['name']}!")

        scheduled_titles = {m["title"] for m in studio.scheduled_movies}
        released_titles = {m["title"] for m in studio.released_movies}
        managed_scripts = [s for s in studio.scripts if s["title"] not in scheduled_titles and s["title"] not in released_titles]
        manage_scripts(managed_scripts, casting_pool, calendar, studio)

        print("\n🎬 Drafting Production...")
        draft_production(studio, calendar, casting_pool, market_pool)

        run_post_production_phase(studio, calendar)

        releases = studio.check_for_releases(calendar)
        for movie in releases:
            logs = studio.apply_post_production(movie)
            for l in logs:
                print(f"🛠️ {movie['title']} — {l}")
            print(f"💥 Released: {movie['title']} (Quality: {movie.get('quality')})")
            for actor in movie.get("cast", []):
                casting_manager.record_collaboration(actor, movie)
            score, review = studio.generate_review(movie)
            print(f"📝 Critics: {score}/100 — {review}")

        studio.update_revenue()
        print("\n📈 Revenue Update:")
        for movie in studio.released_movies:
            if movie.get("monthly_revenue"):
                print(f"• {movie['title']}: ${movie['monthly_revenue'][0]:.2f}M")

        expense = studio.expenses()
        print(f"💸 Expenses: Total ${expense['total']:.2f}M")

        events.run_random_events(studio, calendar)
        if studio.newsfeed:
            print("\n📰 Hollywood News:")
            for story in studio.newsfeed[-3:]:
                print(f"• {story}")

        calendar.advance()

    end_of_year_report(studio, casting_pool)


if __name__ == "__main__":
    hollywood_sim()
