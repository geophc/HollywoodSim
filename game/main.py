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
    print(f"📅 Current Date: {calendar.display()}")
    print(f"🔥 Trending Genres: {', '.join(calendar.trending_genres)}")
    print(f"🔮 Next Quarter Forecast: {', '.join(calendar.forecast_genres)}")
    print(f"🏦 Balance: ${studio.balance:.2f}M | 👑 Prestige: {studio.prestige}")
    print(f"🎭 Actors: {len(casting_pool.actors)} | Writers: {len(casting_pool.writers)}")
    print(f"🎥 Movies in Production: {len(studio.scheduled_movies)} | Released: {len(studio.released_movies)}")
    print(f"💰 Total Earnings: ${studio.total_earnings:.2f}M | Total Expenses: ${studio.total_expenses:.2f}M")
    print(f"🏆 Highest Grossing: {studio.highest_grossing['title'] if studio.highest_grossing else 'N/A'}")

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
    refresh_market(market_pool, casting_pool, calendar)
    market_choice = input("\n🏬 Would you like to visit the Free Market this month? [y]/[Enter]: ").strip().lower()
    if market_choice == 'y':
        visit_market(studio, market_pool)
    else:
        print("⏩ Skipping market visit this month.")

def get_script_choice(scripts):
    print("\n📜 Choose a script to produce:")
    for i, s in enumerate(scripts, 1):
        writer = s['writer']
        print(f"{i}. {s['title']} ({s['genre']}, {s['budget_class']}, Appeal: {s['appeal']}, Rated: {s['rating']}) [{', '.join(s['tags'])}]")
        print(f"   ✍️ Writer: {writer['name']} ({writer['specialty']['name']}) | Interests: {', '.join(writer['interests'])} | School: {writer['education']}")
    return input_number("Enter number (1–3): ", ['1', '2', '3'])

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
            script_idx = get_script_choice(scripts)
            if script_idx is not None:
                studio.scripts.append(scripts[script_idx - 1])

            # Manage scripts
            scheduled_titles = [m['title'] for m in studio.scheduled_movies]
            released_titles = [m['title'] for m in studio.released_movies]
            managed_scripts = [s for s in studio.scripts if s['title'] not in scheduled_titles + released_titles]
            manage_scripts(managed_scripts, casting_pool, calendar, studio.prestige)

            # Production
            approved_scripts = [s for s in studio.scripts if s["status"] == "approved" and s["title"] not in scheduled_titles + released_titles]
            if not approved_scripts:
                print("\n⚠️ No scripts approved for production this month.")
            else:
                manage_script_library(studio)
                print("\n🎞 Approved Scripts Available for Production:")
                for i, s in enumerate(approved_scripts, 1):
                    print(f"{i}. {s['title']} (Genre: {s['genre']}, Quality: {s['quality']})")
                prod_choice = input("Enter number of script to produce, or press [Enter] to skip this month: ").strip()
                if prod_choice and prod_choice.isdigit() and 1 <= int(prod_choice) <= len(approved_scripts):
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

    # End of Year Awards, Summaries, Recaps...
        awards = studio.evaluate_awards()

    if awards:
        print("\n🎖️ End of Year Awards:")
        print(f"🏅 Best Picture: {awards['Best Picture']['title']} (Quality: {awards['Best Picture']['quality']})")
        print(f"🌟 Star of the Year: {awards['Star of the Year']['name']} (Fame: {awards['Star of the Year']['fame']})")
        director_award = awards.get("Best Director")
        if director_award:
            print(f"🎥 Best Director: {director_award['name']} (Fame: {director_award['fame']})")
        else:
            print("🎥 No Best Director award this year.")        
    else:
        print("\n🤷 No awards this year — better luck next time!")

    print(f"\n🏁 Final Balance: ${studio.balance:.2f}M")

    # Collect unique actors from released movies
    used_actors = []
    seen_names = set()
    for movie in studio.released_movies:
        actor = movie["cast"]
        if actor['name'] not in seen_names:
            used_actors.append(actor)
            seen_names.add(actor['name'])

    # --- Studio summary ---
    print("\n📊 Studio Summary:")
    print(f"🎬 Films Released: {len(studio.released_movies)}")
    print(f"💵 Total Earnings: ${studio.total_earnings:.2f}M")
    print(f"💸 Total Expenses: ${studio.total_expenses:.2f}M")
    print(f"👑 Final Prestige: {studio.prestige}")
    if studio.highest_grossing:
        hg = studio.highest_grossing
        print(f"🏅 Top Earner: {hg['title']} (${hg['box_office']}M, Quality: {hg['quality']})")

    # --- Full Filmography Recap ---
    print("\n🎞️ Studio Filmography Recap:")
    for movie in studio.released_movies:
        writer = movie.get("writer", {}).get("name", "Unknown")
        director = movie.get("director", {}).get("name", "Unknown")
        actor = movie.get("cast", {}).get("name", "Unknown")
        print(
            f"🎬 {movie['title']} ({movie['genre']}, {movie['budget_class']}) - "
            f"Released {movie['release_date'][1]}/{movie['release_date'][0]} | "
            f"Quality: {movie['quality']} | Box Office: ${movie['box_office']}M"
        )
        print(f"     ✍️ Writer: {writer} 🎬 Director: {director} 🎭 Lead: {actor}")
   
    # --- Actor career recap ---
    print("\n🎭 Actor Career Recap:")
    for actor in used_actors:
        films = actor["film_history"]
        if not films:
            continue
        avg_quality = sum(f["quality"] for f in films) / len(films)
        avg_box_office = sum(f["box_office"] for f in films) / len(films)

        print(f"\n🧑 {actor['name']} — Age: {actor['age']} | Debut: {actor['debut_year']}")
        print(f"🎬 Films: {len(films)} | Avg Quality: {avg_quality:.1f} | Avg Box Office: ${avg_box_office:.1f}M")

        for f in films:
            print(f"   🎬 {f['title']} ({f['year']}) - Quality: {f['quality']}, Earnings: ${f['box_office']}M")

    # --- Writer career recap ---
    print("\n🖋️ Writer Recap:")
    for writer in casting_pool.writers:
        total = len(writer["film_history"])
        if total == 0:
            continue
        avg_q = sum(s["quality"] for s in writer["film_history"]) / total
        avg_box_office = sum(s["box_office"] for s in writer["film_history"]) / total

        print(f"✍️ {writer['name']} — Scripts: {total}, Avg Quality: {avg_q:.1f}")

    # --- Director career recap ---
    print("\n🎬 Director Recap:")
    for director in casting_pool.directors:
        total = len(director["film_history"])
        if total == 0:
            continue
        avg_q = sum(film["quality"] for film in director["film_history"]) / total
        print(f"🎥 {director['name']} — Films: {total}, Avg Quality: {avg_q:.1f}")

    # --- End game message ---
    if studio.is_bankrupt():
        print("☠️  You ended in bankruptcy. Try again with better budgeting!")
    else:
        print("🎉 You survived the year in Hollywood!")

if __name__ == "__main__":
    hollywood_sim()