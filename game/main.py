from scripts import generate_script
from actors import generate_actor
from studio import Studio
from calendar import GameCalendar

def main():
    calendar = GameCalendar()
    studio = Studio()

    print("🎬 Welcome to HollywoodSim!")

    for _ in range(12):  # Simulate 12 months
        print(f"📅 Current Date: {calendar.display()}")
        print(f"🔥 Trending Genres: {', '.join(calendar.trending_genres)}")
        print(f"🔮 Next Quarter Forecast: {', '.join(calendar.forecast_genres)}")
        print(f"🏦 Balance: ${studio.balance:.2f}M | 👑 Prestige: {studio.prestige}")


        if studio.is_bankrupt():
            print("💀 Your studio is bankrupt! You can no longer produce films.")
            print("🧾 Consider releasing existing movies to earn money...")
        else:
            # Generate and try to produce a movie
            # Offer player a choice of 3 scripts
            scripts = [generate_script() for _ in range(3)]
            print("\n📜 Choose a script to produce:")
            for i, s in enumerate(scripts, 1):
                print(f"{i}. {s['title']} ({s['genre']}, {s['budget_class']}, Appeal: {s['appeal']})")

            choice = input("Enter number (1–3): ").strip()
            while choice not in ["1", "2", "3"]:
                choice = input("Invalid choice. Enter 1, 2, or 3: ").strip()

            script = scripts[int(choice) - 1]

            # Offer player a choice of 3 actors
            actors = [generate_actor() for _ in range(3)]

            print("\n🎬 Choose a lead actor:")
            for i, a in enumerate(actors, 1):
                print(f"{i}. {a['name']} — Fame: {a['fame']} | Salary: ${a['salary']}M")

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
        
            # Produce the movie
            movie = studio.produce_movie(script, actor, calendar, months_ahead)

            if movie:
                y, m = movie["release_date"]
                print(f"🗓️  Scheduled: {movie['title']} ({movie['genre']}, {movie['budget_class']}) "
                      f"with {actor['name']} — releasing {m}/{y} (Cost: ${movie['cost']}M)")
            else:
                print("⚠️ Skipped production due to insufficient funds.")

        # Release any scheduled movies
        released_movies = studio.check_for_releases(calendar)
        for movie in released_movies:
            print(f"💥 Released: {movie['title']} | Earnings: ${movie['box_office']}M | Quality: {movie['quality']}")

        # Monthly expenses
        # This simulates monthly operating costs
        monthly_expenses = studio.expenses()
        studio.balance -= monthly_expenses
        print(f"💸 Monthly Expenses: ${monthly_expenses:.2f}M")

        # Advance the calendar
        calendar.advance()

    print(f"\n🏁 Final Balance: ${studio.balance:.2f}M")
    if studio.is_bankrupt():
        print("☠️  You ended in bankruptcy. Try again with better budgeting!")
    else:
        print("🎉 You survived the year in Hollywood!")

if __name__ == "__main__":
    main()
