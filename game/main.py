import random

from scripts import generate_script
from actors import generate_actor
from writers import generate_writer
from directors import generate_director
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
    # Populate the casting pool with writers
    for _ in range(10):
        casting_pool.add_writer(generate_writer(calendar.year))

    # Populate the casting pool with directors
    for _ in range(5):
        casting_pool.add_director(generate_director(calendar.year))
      
    print("🎬 Welcome to HollywoodSim!")

    # Main game loop: Simulate 12 months
    for _ in range(12):  # Simulate 12 months
        # Display current game state
        print(f"📅 Current Date: {calendar.display()}")
        print(f"🔥 Trending Genres: {', '.join(calendar.trending_genres)}")
        print(f"🔮 Next Quarter Forecast: {', '.join(calendar.forecast_genres)}")
        print(f"🏦 Balance: ${studio.balance:.2f}M | 👑 Prestige: {studio.prestige}")
        print(f"🎭 Actors: {len(casting_pool.actors)} | Writers: {len(casting_pool.writers)}")
        print(f"🎥 Movies in Production: {len(studio.scheduled_movies)} | Released: {len(studio.released_movies)}")
        print(f"💰 Total Earnings: ${studio.total_earnings:.2f}M | Total Expenses: ${studio.total_expenses:.2f}M")
        print(f"🏆 Highest Grossing: {studio.highest_grossing['title'] if studio.highest_grossing else 'N/A'}")
        # Bankruptcy check
        if studio.is_bankrupt():
            print("💀 Your studio is bankrupt! You can no longer produce films.")
            print("🧾 Consider releasing existing movies to earn money...")
        else:

            # --- Monthly phases ---

            # Production phase
                                
            print("\n🎥 Production Phase:")

            # 1. Generate a list of 3 writers
            writers = casting_pool.get_writer_choices(3)

            # 2. Each writer generates one script
            scripts = []
            for writer in writers:
                script = generate_script(calendar, writer=writer)
                scripts.append(script)

            # 3. Present scripts to player
            print("\n📜 Choose a script to produce:")
            for i, s in enumerate(scripts, 1):
                writer = s['writer']
                tags = ', '.join(s['tags'])
                print(f"{i}. {s['title']} ({s['genre']}, {s['budget_class']}, Appeal: {s['appeal']}, Rated: {s['rating']}) [{tags}]")
                print(f"   ✍️  Writer: {writer['name']} | Specialty: {writer['specialty']} | "
                    f"Interests: {', '.join(writer['interests'])} | Schooling: {writer['education']}")

            # 4. Let player choose a script
            choice = input("Enter number (1–3): ").strip()
            while choice not in ["1", "2", "3"]:
                choice = input("Invalid choice. Enter 1, 2, or 3: ").strip()

            script = scripts[int(choice) - 1]

            # 5. Offer player a choice of 3 directors
            print("\n🎬 Choose a director:")
            directors = casting_pool.get_director_choices(3)

            # Check if at least 2 directors are available
            if len(directors) < 2:
                print("⚠️ Not enough directors available to start production this month. Try again next turn.")
                continue # Skips the rest of the production phase for this month

            # Display the choices (Corrected loop)
            for i, d in enumerate(directors, 1):
                tags = ', '.join(d['style_tags'])
                print(f"{i}. {d['name']} — Genre: {d['genre_focus']} | Education: {d['education']} | Style: {tags}")

            # Get player's choice with dynamic validation
            num_choices = len(directors)
            valid_choices = [str(i) for i in range(1, num_choices + 1)]
            prompt = f"Enter number (1–{num_choices}): "
            
            choice = input(prompt).strip()
            while choice not in valid_choices:
                choice = input(f"Invalid choice. Please enter a number from 1 to {num_choices}: ").strip()

            director = directors[int(choice) - 1]


            # 6. Offer player a choice of 3 actors
            actors = casting_pool.get_actor_choices(3)
            print("\n🎬 Choose a lead actor:")

            # Check if at least 2 actors are available
            if len(actors) < 2:
                print("⚠️ Not enough actors available to start production this month. Try again next turn.")
                continue # Skips the rest of the production phase

            # Display the choices (Corrected loop indentation)
            for i, a in enumerate(actors, 1):
                memory = casting_manager.get_history(a["name"])
                if memory:
                    history_note = f"🎞️  Past: {memory['count']}x | Avg Q: {memory['avg_quality']} | Box: ${memory['avg_box_office']}M"
                else:
                    history_note = "🆕 No history"

                tag_str = ', '.join(a['tags'])
                print(f"{i}. {a['name']} — Fame: {a['fame']} | Salary: ${a['salary']}M [{tag_str}] | {history_note}")

            # Get player's choice with dynamic validation
            num_choices = len(actors)
            valid_choices = [str(i) for i in range(1, num_choices + 1)]
            prompt = f"Enter number (1–{num_choices}): "

            actor_choice = input(prompt).strip()
            while actor_choice not in valid_choices:
                actor_choice = input(f"Invalid choice. Please enter a number from 1 to {num_choices}: ").strip()

            actor = actors[int(actor_choice) - 1]

        # 7. Ask player for release window
        print("\n📆 Choose a release window (1–6 months from now):")
        months_ahead = input("Enter number of months (default = 1): ").strip()

        if not months_ahead.isdigit():
            months_ahead = 1
        else:
            months_ahead = max(1, min(int(months_ahead), 6))  # clamp to 1–6
        
   
        # 8. Produce the movie
        movie = studio.produce_movie(script, actor, director, calendar, months_ahead)

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
            print(f"💰 {movie['title']} will earn over {len(movie['monthly_revenue'])} months.")
            print("\n📈 Monthly Revenue Update:")
            for movie in studio.released_movies:
                if movie["monthly_revenue"]:
                    print(f"• {movie['title']}: ${movie['monthly_revenue'][0]}M incoming")
            actor = movie["cast"]
            casting_manager.record_collaboration(actor, movie)

            score, review = studio.generate_review(movie)
            print(f"📝 Critics Score: {score}/100 — {review}")
            writer = movie["writer"]["name"] if "writer" in movie else "Unknown"
            print(f"   ✍️ Written by: {writer}")

       

        # 💀 Hard bankruptcy: no money and no films coming
        if studio.is_bankrupt() and not studio.scheduled_movies:
            print("☠️  Your studio is bankrupt and has no upcoming films.")
            print("💥 GAME OVER.")
            break
   

        # Monthly expenses
        # Calculate and deduct expenses
        expense = studio.expenses()
        studio.balance -= expense["total"]

        # Show expense breakdown
        base = 15.0
        staff = len(studio.released_movies) * 0.2
        in_production = len(studio.scheduled_movies) * 1.0
        prestige_cost = studio.prestige * 0.1

        print(f"💸 Monthly Expenses:")
        print(f"   - Base: $15.0M")
        print(f"   - Staff: ${staff:.2f}M")
        print(f"   - In-Production: ${in_production:.2f}M")
        print(f"   - Prestige: ${prestige_cost:.2f}M")
        print(f"   = Total: ${expense['total']:.2f}M")

        if studio.newsfeed:
            print("\n📰 Hollywood News:")
            for story in studio.newsfeed[-3:]:  # show most recent 3
                print(f"• {story}")

        # Update the studio's revenue
        studio.update_revenue()        
        

        # Advance the calendar
        calendar.advance()

    # --- End of year summary ---
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
    main()
