import random
import events
from scripts import generate_script, finalize_script, rewrite_script
from personnel import generate_actor, generate_writer, generate_director
from studio import Studio
from calendar import GameCalendar
from casting import CastingPool, CastingManager
from contracts import find_active_contracts
from library import manage_script_library
from market import init_market, refresh_market, visit_market
from game_data import SOURCE_TYPES, SCRIPT_TITLES_BY_GENRE, TITLE_STRUCTURES

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
    print("=" * 60 + "\n")


def input_number(prompt, valid_choices):
    while True:
        val = input(prompt).strip()
        if not val:
            return None
        if val in valid_choices:
            return int(val)
        print(f"Invalid input. Expected one of: {', '.join(valid_choices)}")

def run_market_phase(market_pool, casting_pool, calendar, studio):
    print("\n🛒 Market Phase:")
    refresh_market(market_pool, casting_pool, calendar, studio)
    market_choice = input("\n🏬 Would you like to visit the Free Market this month? [y]/[Enter]: ").strip().lower()
    if market_choice == 'y':
        visit_market(studio, market_pool)
    else:
        print("⏩ Skipping market visit this month.")

def calculate_script_buzz(script, calendar=None):
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

    buzz = int((base_quality * 0.3) + tag_bonus + appeal_bonus + writer_bonus + trend_bonus)
    return buzz


def display_scripts_for_production(scripts):
    if not scripts:
        print("📭 No scripts available for production.")
        return

    print("\n📜 Available Scripts for Production\n")
    budget_meanings = {
        "Low": "Low (Under $25M)",
        "Mid": "Mid ($25–60M)",
        "High": "High (Over $60M)"
    }

    for idx, script in enumerate(scripts, 1):
        buzz = calculate_script_buzz(script)
        budget_level = script.get("budget_class", "Unknown")
        budget_desc = budget_meanings.get(budget_level, budget_level)
        appeal = script.get("appeal", 0.0)
        tags = ", ".join(script.get("tags", [])) or "None"
        writer = script.get("writer", {})
        
        print(f"{idx}. {script['title']} ({script['genre']}, Rated: {script.get('rating', 'NR')})")
        print(f"   ✨ Appeal: {appeal:.2f} | Buzz: {buzz} | Budget: {budget_desc}")
        print(f"   🏷️ Tags: {tags}")
        print(f"   ✍️ Writer: {writer.get('name', 'Unknown')} ({writer.get('specialty', {}).get('name', 'N/A')})")


def inhouse_script_production(scripts):
    print("\n🎞️ Production Slate Review")
    print("Available In-House Scripts:")

    def get_appeal_level(score):
        potential = int(score * 100)
        if potential >= 75:
            return "High"
        elif potential >= 50:
            return "Medium"
        else:
            return "Low"

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

    for i, s in enumerate(scripts, 1):
        potential = int(s["appeal"] * 100)
        appeal = get_appeal_level(s["appeal"])
        buzz = buzz_rating(s["appeal"])
        writer = s["writer"]
        print(f"{i}. {s['title']} ({s['genre']}, Rated: {s['rating']})")
        print(f"   ✨ Appeal: {appeal} | Buzz: {buzz} | Potential: {potential} | Budget Class: {s['budget_class']}")
        print(f"   🏷️ Tags: {', '.join(s['tags'])}")
        print(f"   ✍️ Writer: {writer['name']} ({writer['specialty']['name']}) | Interests: {', '.join(writer['interests'])} | School: {writer['education']}")
    
    print("\n📌 Appeal Levels: Low (<50), Medium (50–74), High (75+)")
    print("📡 Buzz Ratings: 🔥 Hot (85+), Trending (70–84), Lukewarm (50–69), Cold (<50)")

    return input_number("Enter number to greenlight (or press [enter] to skip): ", [str(i+1) for i in range(len(scripts))])


def manage_scripts(managed_scripts, casting_pool, calendar, studio_prestige):
    if not managed_scripts:
        return
    print("\n📚 Script Management:")
    for i, s in enumerate(managed_scripts, 1):
        print(f"{i}. {s['title']} ({s['genre']}, Draft {s['draft_number']}) — Status: {s['status']} | Quality: {s['quality']}/{s['potential_quality']}")
    choice = input("Enter script number to manage or [Enter] to skip: ").strip()
    if choice and choice.isdigit():
        selected = managed_scripts[int(choice) - 1]
        action = input("Type [f] to finalize or [r] to rewrite: ").strip().lower()
        if action == 'f':
            finalize_script(selected, studio_prestige=studio_prestige)
        elif action == 'r':
            rewrite_choices = casting_pool.get_writer_choices(3)
            print("Choose a writer to rewrite the script:")
            for idx, w in enumerate(rewrite_choices, 1):
                print(f"{idx}. {w['name']} | Specialty: {w['specialty']['name']} | Interests: {', '.join(w['interests'])}")
            writer_choice = input_number("Enter number: ", ['1', '2', '3'])
            if writer_choice:
                rewrite_script(selected, rewrite_choices[writer_choice - 1], calendar)

def choose_item(prompt, items, formatter):
    for i, item in enumerate(items, 1):
        print(f"{i}. {formatter(item)}")
    valid_choices = [str(i) for i in range(1, len(items) + 1)]
    choice = input_number(prompt, valid_choices)
    if choice:
        return items[choice - 1]
    return None

def produce_film(studio, script, calendar, casting_pool, casting_manager):
    print("\n🎬 Choose a director:")
    directors = casting_pool.get_director_choices(3)
    if len(directors) < 2:
        print("⚠️ Not enough directors available to start production this month. Try again next turn.")
        return None
    director = choose_item("Enter number: ", directors, lambda d: f"{d['name']} — Genre: {d['genre_focus']} | Style: {', '.join(d['style_tags'])}")

    actors = find_active_contracts(studio.contracts, "actors")
    if not actors:
        actors = casting_pool.get_actor_choices(3)
    print("\n🎬 Choose a lead actor:")
    if len(actors) < 2:
        print("⚠️ Not enough actors for production this month.")
        return None

    def actor_fmt(a):
        hist = casting_manager.get_history(a["name"])
        note = f"🎞️ Past: {hist['count']}x | Avg Q: {hist['avg_quality']:.1f} | Box: ${hist['avg_box_office']:.1f}M" if hist else "🆕 No history"
        return f"{a['name']} — Fame: {a['fame']} | Salary: ${a['salary']}M [{', '.join(a['tags'])}] | {note}"

    actor = choose_item("Enter number: ", actors, actor_fmt)
    if not actor or not director:
        return None

    # Release window
    months_ahead = input("\n📆 Choose a release window (1–6 months from now): ").strip()
    months_ahead = int(months_ahead) if months_ahead.isdigit() else 1
    months_ahead = max(1, min(months_ahead, 6))

    movie = studio.produce_movie(script, actor, director, calendar, months_ahead)
    if movie:
        print(f"🗓️ Scheduled: {movie['title']} ({movie['genre']}, {movie['budget_class']}) with {actor['name']} — releasing {movie['release_date'][1]}/{movie['release_date'][0]} (Cost: ${movie['cost']}M)")
        matching_tags = set(script['tags']) & set(actor['tags'])
        if matching_tags:
            print(f"✨ Tag synergy bonus! Matching tags: {', '.join(matching_tags)}")
    else:
        print("⚠️ Skipped production due to insufficient funds.")
    return movie

def hollywood_sim():
    # Setup
    calendar = GameCalendar()
    casting_pool = CastingPool()
    studio = Studio(year=calendar.year)
    casting_manager = CastingManager()
    market_pool = init_market()

    for _ in range(30): casting_pool.add_actor(generate_actor(calendar.year))
    for _ in range(10): casting_pool.add_writer(generate_writer(calendar.year))
    for _ in range(5):  casting_pool.add_director(generate_director(calendar.year))

    print_banner()

    for _ in range(12):  # Simulate months
        display_game_state(calendar, studio, casting_pool)

        if studio.is_bankrupt():
            print("💀 Your studio is bankrupt! You can no longer produce films.")
            print("🧾 Consider releasing existing movies to earn money...")
        else:
            run_market_phase(market_pool, casting_pool, calendar, studio)

            # Script phase
            writers = casting_pool.get_writer_choices(3)
            scripts = [generate_script(calendar, writer=w) for w in writers]
            script_idx = inhouse_script_production(scripts)
            if script_idx is not None:
                studio.scripts.append(scripts[script_idx - 1])

            # Manage scripts
            scheduled_titles = [m['title'] for m in studio.scheduled_movies]
            released_titles = [m['title'] for m in studio.released_movies]
            managed_scripts = [s for s in studio.scripts if s['title'] not in scheduled_titles + released_titles]
            manage_scripts(managed_scripts, casting_pool, calendar, studio.prestige)

            
            # Production
            approved_scripts = [s for s in studio.scripts if s["status"] == "approved" and s["title"] not in scheduled_titles + released_titles]

            # Use the new, detailed display function
            display_scripts_for_production(approved_scripts)

            if approved_scripts:
                prod_choice = input("Enter number of script to produce, or press [Enter] to skip this month: ").strip()
                if prod_choice and prod_choice.isdigit() and 1 <= int(prod_choice) <= len(approved_scripts):
                    # The rest of the logic remains the same
                    produce_film(studio, approved_scripts[int(prod_choice) - 1], calendar, casting_pool, casting_manager)
                else:
                    print("⏩ Skipping production this month.")

        # Release movies, monthly updates, advance calendar, events, expenses, news
        for movie in studio.check_for_releases(calendar):
            print(f"💥 Released: {movie['title']} | Earnings: ${movie.get('box_office', '(Est.)')}M | Quality: {movie['quality']}")
            casting_manager.record_collaboration(movie["cast"], movie)
            score, review = studio.generate_review(movie)
            print(f"📝 Critics Score: {score}/100 — {review}")


        # Check for bankruptcy
        if studio.is_bankrupt() and not studio.scheduled_movies:
            print("💔 Your studio has no movies in production and is bankrupt.")
            print("☠️ GAME OVER.")
            end_of_year_report(studio, casting_pool)
            break

        studio.update_revenue()
        print("\n📈 Monthly Revenue Update:")
        for movie in studio.released_movies:
            if movie.get("monthly_revenue"):
                print(f"• {movie['title']}: ${movie['monthly_revenue'][0]}M incoming")

        calendar.advance()
        events.run_random_events(studio, calendar)

        # Expenses
        expense = studio.expenses()
        studio.balance -= expense["total"]
        print(f"💸 Monthly Expenses: - Base $15M, Staff ${len(studio.released_movies)*0.2:.2f}M, Production ${len(studio.scheduled_movies):.2f}M, Prestige ${studio.prestige*0.1:.2f}M = Total ${expense['total']:.2f}M")
        if studio.newsfeed:
            print("\n📰 Hollywood News:")
            for story in studio.newsfeed[-3:]:
                print(f"• {story}")

# End of year summary
def print_awards_summary(awards):
    print("\n🎖️ End of Year Awards:")
    print(f"🏅 Best Picture: {awards['Best Picture']['title']} (Quality: {awards['Best Picture']['quality']})")
    print(f"🌟 Star of the Year: {awards['Star of the Year']['name']} (Fame: {awards['Star of the Year']['fame']})")

    director_award = awards.get("Best Director")
    if director_award:
        print(f"🎥 Best Director: {director_award['name']} (Fame: {director_award['fame']})")
    else:
        print("🎥 No Best Director award this year.")


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
        actor = movie.get("cast", {}).get("name", "Unknown")

        print(f"🎬 {movie['title']} ({movie['genre']}, {movie['budget_class']}) - "
              f"Released {movie['release_date'][1]}/{movie['release_date'][0]} | "
              f"Quality: {movie['quality']} | Box Office: ${movie['box_office']}M")
        print(f"     ✍️ Writer: {writer} 🎬 Director: {director} 🎭 Lead: {actor}")


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

        for f in films:
            print(f"   🎬 {f['title']} ({f['year']}) - Quality: {f['quality']}, Earnings: ${f['box_office']}M")


def print_talent_recap(talent_list, role_emoji, role_title):
    print(f"\n{role_emoji} {role_title} Recap:")
    for talent in talent_list:
        films = talent.get("film_history", [])
        if not films:
            continue
        avg_quality = sum(f["quality"] for f in films) / len(films)
        avg_box_office = sum(f["box_office"] for f in films) / len(films) if 'box_office' in films[0] else None

        summary = f"{role_emoji} {talent['name']} — Films: {len(films)}, Avg Quality: {avg_quality:.1f}"
        if avg_box_office is not None:
            summary += f", Avg Box Office: ${avg_box_office:.1f}M"
        print(summary)


# --- End-of-Year Report Handler ---
def end_of_year_report(studio, casting_pool):
    # Awards
    awards = studio.evaluate_awards()
    if awards:
        print_awards_summary(awards)
    else:
        print("\n🤷 No awards this year — better luck next time!")

    # Financial & Prestige Summary
    print_studio_summary(studio)

    # Collect unique actors
    seen = set()
    used_actors = []
    for m in studio.released_movies:
        actor = m["cast"]
        if actor["name"] not in seen:
            seen.add(actor["name"])
            used_actors.append(actor)

    # Recaps
    print_filmography(studio.released_movies)
    print_actor_recap(used_actors)
    print_talent_recap(casting_pool.writers, "🖋️", "Writer")
    print_talent_recap(casting_pool.directors, "🎬", "Director")

    # End Game Message
    if studio.is_bankrupt():
        print("☠️  You ended in bankruptcy. Try again with better budgeting!")
    else:
        print("🎉 You survived the year in Hollywood!")

#def test_end_of_year_report():
    from studio import Studio
    from casting import CastingPool
    import random

    studio = Studio("Test Studio")
    casting_pool = CastingPool()

    # Manually populate dummy movie
    studio.released_movies = [
        {
            "title": "Fake Hit",
            "genre": "Action",
            "budget_class": "Blockbuster",
            "release_date": (2025, 6),
            "quality": 85,
            "box_office": 220.0,
            "writer": {"name": "Jane Quill"},
            "director": {"name": "Max Cutter", "fame": 75},
            "cast": {"name": "Star Doe", "age": 33, "debut_year": 2022, "film_history": [], "fame": 88}
        },
        {
            "title": "Indie Darling",
            "genre": "Drama",
            "budget_class": "Indie",
            "release_date": (2025, 9),
            "quality": 91,
            "box_office": 15.0,
            "writer": {"name": "Alan Pen"},
            "director": {"name": "Sofia Lens", "fame": 70},
            "cast": {"name": "Star Doe", "age": 33, "debut_year": 2022, "film_history": [], "fame": 88}
        }
    ]

    # Add film history to cast    
    for movie in studio.released_movies:
        movie["cast"]["film_history"].append({
            "title": movie["title"],
            "quality": movie["quality"],
            "box_office": movie["box_office"],
            "year": movie["release_date"][0]
        })

    # Add to highest grossing and stats
    studio.highest_grossing = studio.released_movies[0]
    studio.total_earnings = sum(m["box_office"] for m in studio.released_movies)
    studio.total_expenses = 80.0
    studio.prestige = 12
    studio.balance = 135.0  # Positive ending

    # Add dummy casting pool
    casting_pool.writers = [{"name": "Jane Quill", "film_history": [studio.released_movies[0]]},
                            {"name": "Alan Pen", "film_history": [studio.released_movies[1]]}]
    casting_pool.directors = [{"name": "Max Cutter", "film_history": [studio.released_movies[0]]},
                              {"name": "Sofia Lens", "film_history": [studio.released_movies[1]]}]

    # Run the test report
    end_of_year_report(studio, casting_pool)


# Entry point
if __name__ == "__main__":
    #test_end_of_year_report()
    hollywood_sim()
