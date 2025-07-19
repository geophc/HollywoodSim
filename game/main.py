import random

from scripts import generate_script
from actors import generate_actor
from studio import Studio
from calendar import GameCalendar
from casting import CastingPool
from casting import CastingManager



def main():
    # Initialize game calendar and studio
    calendar = GameCalendar()
    casting_pool = CastingPool()
    studio = Studio(year=calendar.year)
    casting_manager = CastingManager()

    # Populate the casting pool with actors
    for _ in range(30):
        casting_pool.add_actor(generate_actor(calendar.year))

    print("🎬 Welcome to HollywoodSim!")

    # Main game loop: Simulate 12 months
    for _ in range(12):  # Simulate 12 months
        # Display current game state
        print(f"📅 Current Date: {calendar.display()}")
        print(f"🔥 Trending Genres: {', '.join(calendar.trending_genres)}")
        print(f"🔮 Next Quarter Forecast: {', '.join(calendar.forecast_genres)}")
        print(f"🏦 Balance: ${studio.balance:.2f}M | 👑 Prestige: {studio.prestige}")

        # Bankruptcy check
        if studio.is_bankrupt():
            print("💀 Your studio is bankrupt! You can no longer produce films.")
            print("🧾 Consider releasing existing movies to earn money...")
        else:
            # Generate and try to produce a movie
            # Offer player a choice of 3 scripts
            scripts = [generate_script() for _ in range(3)]
            print("\n📜 Choose a script to produce:")
            for i, s in enumerate(scripts, 1):
                tags = ', '.join(s['tags'])
                print(f"{i}. {s['title']} ({s['genre']}, {s['budget_class']}, Appeal: {s['appeal']}) [{tags}]")


            choice = input("Enter number (1–3): ").strip()
            while choice not in ["1", "2", "3"]:
                choice = input("Invalid choice. Enter 1, 2, or 3: ").strip()

            script = scripts[int(choice) - 1]

            # Offer player a choice of 3 actors
            actors = casting_pool.get_actor_choices(3)
            print("\n🎬 Choose a lead actor:")

        for i, a in enumerate(actors, 1):
            memory = casting_manager.get_history(a["name"])
            if memory:
                history_note = f"🎞️  Past: {memory['count']}x | Avg Q: {memory['avg_quality']} | Box: ${memory['avg_box_office']}M"
            else:
                history_note = "🆕 No history"

            tag_str = ', '.join(a['tags'])
            print(f"{i}. {a['name']} — Fame: {a['fame']} | Salary: ${a['salary']}M [{tag_str}] | {history_note}")


        actor_choice = input("Enter number (1–3): ").strip()
        while actor_choice not in ["1", "2", "3"]:
            actor_choice = input("Invalid choice. Enter 1, 2, or 3: ").strip()

        actor = actors[int(actor_choice) - 1]

        # Ask player for release window
        print("\n📆 Choose a release window (1–6 months from now):")
        months_ahead = input("Enter number of months (default = 1): ").strip()

        if not months_ahead.isdigit():
            months_ahead = 1
        else:
            months_ahead = max(1, min(int(months_ahead), 6))  # clamp to 1–6
        
   # Monthly expenses
        # Calculate and deduct expenses
        expense = studio.expenses()
        studio.balance -= expense["total"]

        # Show expense breakdown
        base = 5.0
        staff = len(studio.released_movies) * 0.2
        in_production = len(studio.scheduled_movies) * 1.0
        prestige_cost = studio.prestige * 0.1

        print(f"💸 Monthly Expenses:")
        print(f"   - Base: $5.0M")
        print(f"   - Staff: ${staff:.2f}M")
        print(f"   - In-Production: ${in_production:.2f}M")
        print(f"   - Prestige: ${prestige_cost:.2f}M")
        print(f"   = Total: ${expense['total']:.2f}M")


        # Produce the movie
        movie = studio.produce_movie(script, actor, calendar, months_ahead)

        if movie:
            y, m = movie["release_date"]
            print(f"🗓️  Scheduled: {movie['title']} ({movie['genre']}, {movie['budget_class']}) "
                      f"with {actor['name']} — releasing {m}/{y} (Cost: ${movie['cost']}M)")
            # Show synergy bonus if any
            matching_tags = set(script['tags']) & set(actor['tags'])
            if matching_tags:
                print(f"✨ Tag synergy bonus! Matching tags: {', '.join(matching_tags)}")

        else:
            print("⚠️ Skipped production due to insufficient funds.")

        # Release any scheduled movies
        released_movies = studio.check_for_releases(calendar)
       
        for movie in released_movies:
            print(f"💥 Released: {movie['title']} | Earnings: ${movie['box_office']}M | Quality: {movie['quality']}")
            actor = movie["cast"]
            casting_manager.record_collaboration(actor, movie)

            score, review = studio.generate_review(movie)
            print(f"📝 Critics Score: {score}/100 — {review}")

        # 💀 Hard bankruptcy: no money and no films coming
        if studio.is_bankrupt() and not studio.scheduled_movies:
            print("☠️  Your studio is bankrupt and has no upcoming films.")
            print("💥 GAME OVER.")
            break

     

        # Show recent news
        if studio.newsfeed:
            print("\n📰 Hollywood News:")
            for story in studio.newsfeed[-3:]:  # show most recent 3
                print(f"• {story}")

        # Advance the calendar
        calendar.advance()

    # --- End of year summary ---
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

    print(f"\n🏁 Final Balance: ${studio.balance:.2f}M")


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


    # --- End game message ---
    if studio.is_bankrupt():
        print("☠️  You ended in bankruptcy. Try again with better budgeting!")
    else:
        print("🎉 You survived the year in Hollywood!")

if __name__ == "__main__":
    main()
