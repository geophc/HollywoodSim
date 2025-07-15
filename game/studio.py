import random

class Studio:
    def __init__(self, name="Player Studio", starting_balance=200.0):
        self.name = name
        self.balance = starting_balance  # in millions
        self.scheduled_movies = []
        self.released_movies = []
        self.prestige = 0  # new attribute for future phase

    def produce_movie(self, script, actor, calendar, months_ahead=1):
        """
        Combines a script and actor into a movie, deducts cost, and schedules it.
        """
        compatibility = 1 if script["genre"] in ["Drama", "Romance"] else 0.8
        base_quality = script["appeal"] * 5 + actor["fame"] * 0.5 * compatibility
        quality = round(min(100, max(10, base_quality)))

        # Calculate production cost
        budget_multiplier = {"Low": 10, "Mid": 30, "Blockbuster": 60}
        production_cost = budget_multiplier[script["budget_class"]] + actor["salary"]

        if self.balance < production_cost:
            print(f"❌ Not enough funds to produce {script['title']}! Needed ${production_cost}M, have ${self.balance}M")
            return None

        self.balance -= production_cost

        # Schedule for X months ahead
        release_month = calendar.month + months_ahead
        release_year = calendar.year
        if release_month > 12:
            release_month -= 12
            release_year += 1

        release_date = (release_year, release_month)

        movie = {
            "title": script["title"],
            "genre": script["genre"],
            "budget_class": script["budget_class"],
            "quality": quality,
            "cast": actor,
            "cost": production_cost,
            "release_date": release_date,
            "box_office": None
        }

        self.scheduled_movies.append(movie)
        return movie

    def check_for_releases(self, calendar):
        """
        Releases movies scheduled for the current date. Adds revenue to balance.
        """
        released = []
        remaining = []

        for movie in self.scheduled_movies:
            if (calendar.year, calendar.month) == movie["release_date"]:
                movie["box_office"] = self.simulate_box_office(movie, trending_genres=calendar.trending_genres)
                self.balance += movie["box_office"]
                self.released_movies.append(movie)
                released.append(movie)
                # Optional prestige mechanic based on quality
                if movie["quality"] >= 75:
                    self.prestige += 1
            else:
                remaining.append(movie)

        self.scheduled_movies = remaining
        return released

    def simulate_box_office(self, movie, trending_genres=None):

        """ 
        Simulates box office earnings based on quality, fame, and genre trends.
        """
        base = movie["quality"] * 0.8
        fame = movie["cast"]["fame"] * 0.5
        random_bonus = random.randint(0, 30)
        genre_bonus = 10 if trending_genres and movie["genre"] in trending_genres else 0
        earnings = round(base + fame + random_bonus + genre_bonus, 2)
        return earnings
    
    def is_bankrupt(self):
        """
        Returns True if the studio's balance is below zero.
        """
        return self.balance < 0

    def expenses(self):
        """
        Calculates monthly operating costs.
        Expandable later to include dynamic costs.
        """
        base_expense = 5.0
        staff_expense = len(self.released_movies) * 0.2
        return round(base_expense + staff_expense, 2)
