import random

class Studio:
    def __init__(self, name="Player Studio", starting_balance=100.0):
        self.name = name
        self.balance = starting_balance  # in millions
        self.scheduled_movies = []
        self.released_movies = []
        self.prestige = 0  # new attribute for future phase
        self.total_earnings = 0.0
        self.total_expenses = 0.0
        self.highest_grossing = None
        self.newsfeed = []  # stores recent news headlines
      

    def produce_movie(self, script, actor, calendar, months_ahead=1):
        """
        Combines a script and actor into a movie, deducts cost, and schedules it.
        """
        compatibility = 1 if script["genre"] in ["Drama", "Romance"] else 0.8
        base_quality = script["appeal"] * 5 + actor["fame"] * 0.5 * compatibility
        quality = round(min(100, max(10, base_quality)))

        # Tag synergy bonus
        tag_bonus = 0
        for tag in script["tags"]:
            if tag in actor["tags"]:
                tag_bonus += 5  # You can fine-tune this later

        quality = round(min(100, max(10, quality + tag_bonus)))

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

                # Record film to actor's history
                actor = movie["cast"]
                actor["film_history"].append({
                    "title": movie["title"],
                    "year": calendar.year,
                    "month": calendar.month,
                    "genre": movie["genre"],
                    "quality": movie["quality"],
                    "box_office": movie["box_office"]
                    })

                
                # ✅ Track total earnings and highest-grossing movie
                self.total_earnings += movie["box_office"]
                if (self.highest_grossing is None or 
                    movie["box_office"] > self.highest_grossing["box_office"]):
                    self.highest_grossing = movie

                # Generate review + add to newsfeed
                score, review = self.generate_review(movie)
                headline = f"{movie['title']} released to {score}/100 reviews — {review}"
                self.newsfeed.append(headline)
                self.newsfeed = self.newsfeed[-10:]  # Keep last 10 headlines
    

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
        random_bonus = round(random.gauss(10, 5), 2)  # average 10, std dev 5
        if random_bonus < 0:
            random_bonus = 0
        # Genre trend bonus
        if trending_genres and movie["genre"] in trending_genres:
            genre_bonus = 10
        else:  
            genre_bonus = 0
        earnings = round(base + fame + random_bonus + genre_bonus, 2)
        return earnings
                        
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
        base = 15.0
        staff = len(self.released_movies) * 0.2
        in_production = len(self.scheduled_movies) * 1.0
        prestige = self.prestige * 0.1
        total = round(base + staff + in_production + prestige, 2)
        self.total_expenses += total
        return {
            "base": base,
            "staff": staff,
            "in_production": in_production,
            "prestige": prestige,
            "total": total
        }
    def generate_review(self, movie):
        quality = movie["quality"]

        # Simulated critic score out of 100, with slight randomness
        score = round(min(100, max(10, quality + random.randint(-10, 10))))

        # Review text based on score
        if score >= 85:
            review = "🌟 A masterpiece! Critics are raving."
        elif score >= 70:
            review = "👍 A solid release with strong performances."
        elif score >= 50:
            review = "😐 Mixed reception. Audiences may be split."
        elif score >= 30:
            review = "👎 Critics were not impressed."
        else:
            review = "💀 An outright disaster."

        return score, review
    

        
      
    
