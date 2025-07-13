from scripts import generate_script
from actors import generate_actor
from studio import Studio
from calendar import GameCalendar

def main():
    calendar = GameCalendar()
    studio = Studio()

    print("🎬 Welcome to HollywoodSim!")

    for _ in range(12):  # Simulate 12 months
        print(f"\n📅 Current Date: {calendar.display()}")
        print(f"🏦 Balance: ${studio.balance:.2f}M")

        if studio.is_bankrupt():
            print("💀 Your studio is bankrupt! You can no longer produce films.")
            print("🧾 Consider releasing existing movies to earn money...")
        else:
            # Generate and try to produce a movie
            script = generate_script()
            actor = generate_actor()
            movie = studio.produce_movie(script, actor, calendar)

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

        calendar.advance()

    print(f"\n🏁 Final Balance: ${studio.balance:.2f}M")
    if studio.is_bankrupt():
        print("☠️  You ended in bankruptcy. Try again with better budgeting!")
    else:
        print("🎉 You survived the year in Hollywood!")

if __name__ == "__main__":
    main()
