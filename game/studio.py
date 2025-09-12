# studio.py

import random
from personnel import generate_actor, STAFF_SPECIALTIES
from scripts import assign_rating, RATINGS
from genres import seasonal_bonus
from contracts import find_active_contracts
from post_production import apply_distribution_effects

class Studio:
    def __init__(self, name="Player Studio", starting_balance=150.0, year=2025):
        self.name = name
        self.balance = starting_balance  # in millions
        self.scripts = []          
        self.script_library = []
        self.scheduled_movies = []
        self.released_movies = []
        self.prestige = 0
        self.reputation = 0
        self.total_earnings = 0.0
        self.total_expenses = 0.0
        self.highest_grossing = None
        self.newsfeed = []

        # Talent pools
        self.actor_pool = [generate_actor(year) for _ in range(15)]
        self.staff_pool = []
        self.contracts = {"actors": [], "writers": [], "directors": [], "staff": []}

    # ---- Talent Management ----
    def hire(self, talent):
        """
        CORRECTED: Add a talent to the studio's internal roster/pools.
        Contract management is handled separately by the function that creates the contract.
        This prevents duplicate entries in the contracts list.
        """
        role = talent.get("role")
        if role == "actor":
            self.actor_pool.append(talent)
        elif role in STAFF_SPECIALTIES:
            self.staff_pool.append(talent)

    def release(self, talent):
        """Release a talent from the roster."""
        kind = talent.get("role")
        if kind == "actor" and talent in self.contracts["actors"]:
            self.contracts["actors"].remove(talent)
            if talent in self.actor_pool:
                self.actor_pool.remove(talent)
        elif kind == "director" and talent in self.contracts["directors"]:
            self.contracts["directors"].remove(talent)
        elif kind == "writer" and talent in self.contracts["writers"]:
            self.contracts["writers"].remove(talent)
        elif kind in STAFF_SPECIALTIES and talent in self.contracts["staff"]:
            self.contracts["staff"].remove(talent)
            if talent in self.staff_pool:
                self.staff_pool.remove(talent)

    def list_signed_talent(self, role):
        """Return a list of currently signed talent of a given role."""
        return find_active_contracts(self.contracts, role)

    def renew_contracts(self):
        """Reduce remaining time on contracts, expire if needed."""
        for role in ["actors", "writers", "directors", "staff"]:
            new_list = []
            for contract in self.contracts.get(role, []):
                contract["remaining"] -= 1
                if contract["remaining"] > 0:
                    new_list.append(contract)
                else:
                    print(f"📄 Contract expired: {contract['person']['name']} ({role[:-1]})")
            self.contracts[role] = new_list

    
    # ---- Script & Movie Evaluation ----
    def evaluate_script(self, script):
        buzz = script.get("buzz", 0)
        quality = script.get("potential_quality", script.get("quality", 50))
        genre_bonus = 10 if hasattr(self, "focus_genres") and script["genre"] in self.focus_genres else 0
        score = (buzz * 1.2) + quality + genre_bonus
        return round(score, 2)

    def choose_script_to_option(self, script_pool):
        if not script_pool:
            return None
        scored = [(self.evaluate_script(s), s) for s in script_pool]
        scored.sort(reverse=True, key=lambda x: x[0])
        best_score, best_script = scored[0]
        print(f"📝 {best_script['title']} selected for optioning (Score: {best_score})")
        return best_script
   

    # ---- Movie Production ----
    def produce_movie(self, script, actor, director, calendar, months_ahead=1):
        if script.get("status") != "approved":
            print(f"❌ Script '{script['title']}' must be approved before production.")
            return None

        final_quality = script.get('quality', 50)

        # Actor-Script tag synergy
        actor_tags = set(actor.get("tags", []))
        script_tags = set(script.get("tags", []))
        tag_bonus = len(actor_tags & script_tags) * 5
        final_quality += tag_bonus

        # Director-Genre synergy
        if "genre_focus" in director and script["genre"] == director["genre_focus"]:
            final_quality += 10

        final_quality = min(100, max(10, round(final_quality)))

        # Production cost
        budget_class = script.get("budget_class", "Mid")
        budget_multiplier = {"Low": 10, "Mid": 30, "High": 60}
        production_cost = budget_multiplier.get(budget_class, 30) + actor.get("salary", 0) + director.get("salary", 0)

        if self.balance < production_cost:
            print(f"❌ Not enough funds to produce {script['title']}! Needed ${production_cost}M, have ${self.balance}M")
            return None

        self.balance -= production_cost
        self.total_expenses += production_cost

        # Schedule movie
        release_month = calendar.month + months_ahead
        release_year = calendar.year
        if release_month > 12:
            release_month -= 12
            release_year += 1
        release_date = (release_year, release_month)

        movie = {
            "title": script["title"],
            "genre": script["genre"],
            "budget_class": budget_class,
            "quality": final_quality,
            "cast": actor,
            "director": director,
            "writer": script.get("writer"),
            "cost": production_cost,
            "release_date": release_date,
            "box_office": 0.0,
            "monthly_revenue": [],
            "remaining_revenue": 0,
            "buzz": script.get("buzz", 0),
            "script": script
        }

        self.scheduled_movies.append(movie)
        return movie

    # ---- Revenue & Releases ----
    def check_for_releases(self, calendar):
        released = []
        remaining = []

        for movie in self.scheduled_movies:
            if (calendar.year, calendar.month) == movie["release_date"]:
                # This call correctly sets up the monthly revenue stream for the movie
                self.simulate_box_office(movie, calendar)
                
                # Update talent film history
                for talent_key in ["cast", "director", "writer"]:
                    talent = movie.get(talent_key)
                    if talent is not None:
                        talent.setdefault("film_history", []).append({
                            "title": movie["title"],
                            "year": calendar.year,
                            "month": calendar.month if talent_key=="cast" else None,
                            "genre": movie["genre"],
                            "quality": movie["quality"],
                            "box_office": 0 # Box office starts at 0 and grows monthly
                        })
                
                if self.highest_grossing is None:
                    self.highest_grossing = movie

                # Generate news
                score, review = self.generate_review(movie)
                headline = f"{movie['title']} released to {score}/100 reviews — {review}"
                self.newsfeed.append(headline)
                self.newsfeed = self.newsfeed[-10:]

                # Prestige
                if movie["quality"] >= 75:
                    self.prestige += 1

                self.released_movies.append(movie)
                released.append(movie)
            else:
                remaining.append(movie)

        self.scheduled_movies = remaining
        return released

    def simulate_box_office(self, movie, calendar):
        """
        Determines a movie's financial success by creating a monthly revenue stream.
        This is called once at release to initialize revenue, then monthly via update_revenue().
        """
        quality = movie.get("quality", 50)
        buzz = movie.get("buzz", 0)

        # 🎯 Base potential (quality + buzz weighted)
        base = quality * 0.5 + buzz * 1.2

        # 🌟 Talent contribution
        fame_actor = movie["cast"].get("fame", 0)
        fame_director = movie["director"].get("fame", 0)
        talent_boost = 1.0 + ((fame_actor + fame_director) / 300.0)

        # 📦 Distribution effects
        from post_production import apply_distribution_effects
        dist_multiplier, dist_longevity = apply_distribution_effects(movie)

        # 📆 Seasonal bonus (e.g. Summer action movies do better)
        bonus_pct = seasonal_bonus(movie["genre"], calendar.month)

        # 🔞 Rating cap (family films = larger audience potential)
        rating = movie.get("rating", "PG-13")
        rating_cap = RATINGS.get(rating, {}).get("max_audience", 1.0)

        # 🔥 Genre trend bonus
        genre_bonus = 1.15 if calendar.trending_genres and movie["genre"] in calendar.trending_genres else 1.0

        # 📣 Marketing boost (spend → multiplier)
        marketing_spend = movie.get("marketing_spend", 0)
        marketing_boost = 1.0 + (marketing_spend * 0.04)

        # 🧮 Total box office potential
        total_potential = (
            base * talent_boost * genre_bonus * marketing_boost
        ) * (1 + bonus_pct) * rating_cap

        # Apply distribution multiplier (Wide vs Limited vs Streaming, etc.)
        total_potential *= dist_multiplier

        # 🎬 Rollout curve — how many months it earns
        # Longevity shifts the spread of earnings
        rollout_months = max(2, round(random.randint(3, 5) * (1 + dist_longevity)))

        # Balance: spread across months (heavier upfront for Wide releases, slower build for Limited)
        if rollout_months > 0:
            monthly_base = round(total_potential / rollout_months / 2.0, 2)
        else:
            monthly_base = 0

        # For realism: adjust distribution of revenue over months
        revenue_curve = []
        for i in range(rollout_months):
            if movie.get("release_strategy") == "Wide":
                # Front-loaded
                factor = 1.5 if i == 0 else (1.0 - (i * 0.15))
            elif movie.get("release_strategy") == "Limited":
                # Slow build then fade
                factor = 0.5 + (i * 0.2)
            elif movie.get("release_strategy") == "Streaming":
                # Flat revenue
                factor = 1.0
            elif movie.get("release_strategy") == "International":
                # Longer tail
                factor = 1.2 - (i * 0.05)
            else:
                factor = 1.0

            factor = max(0.3, factor)  # don’t go negative
            revenue_curve.append(round(monthly_base * factor, 2))

        movie["monthly_revenue"] = revenue_curve
        movie["remaining_revenue"] = sum(revenue_curve)

        # Initial box office is 0; grows as update_revenue() processes each month
        movie["box_office"] = 0.0


    def update_revenue(self):
        for movie in self.released_movies:
            if movie.get("monthly_revenue"):
                this_month_earning = movie["monthly_revenue"].pop(0)
                self.balance += this_month_earning
                self.total_earnings += this_month_earning
                
                # Update the movie's total gross
                current_box_office = movie.get("box_office", 0.0)
                movie["box_office"] = current_box_office + this_month_earning
                
                # Update highest grossing film check
                if self.highest_grossing and movie["box_office"] > self.highest_grossing.get("box_office", 0):
                    self.highest_grossing = movie

    # ---- Utilities ----
    def is_bankrupt(self):
        return self.balance < 0

    def expenses(self):
        base = 15.0
        staff_cost = len(self.staff_pool) * 0.5
        in_production = len(self.scheduled_movies) * 1.0
        prestige_cost = self.prestige * 0.1
        total = round(base + staff_cost + in_production + prestige_cost, 2)
        self.total_expenses += total
        return {"base": base, "staff": staff_cost, "in_production": in_production, "prestige": prestige_cost, "total": total}

    def generate_review(self, movie):
        quality = movie["quality"]
        score = round(min(100, max(10, quality + random.randint(-10, 10))))
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

    def evaluate_awards(self):
        if not self.released_movies:
            return {}
        sorted_by_quality = sorted(self.released_movies, key=lambda m: m["quality"], reverse=True)
        winners = {"Best Picture": sorted_by_quality[0]}
        winners["Star of the Year"] = max(self.released_movies, key=lambda m: m["cast"].get("fame",0))["cast"]
        directors = [m["director"] for m in self.released_movies if m.get("director")]
        if directors:
            winners["Best Director"] = max(directors, key=lambda d: d.get("fame",0))
        return winners

    
    #   ---- Post-Production ----
    def apply_post_production(self, movie):
        log = []
        if not movie:
            return log

        staff = movie.get("staff", {})

        # Editor -> quality bump
        editor = staff.get("Editor")
        if editor:
            exp = editor.get("experience", 3)
            fame = editor.get("fame", 20)
            q_bonus = int(exp * 0.6 + (fame / 50.0) * 2)
            movie["quality"] = min(100, int(movie.get("quality", 0) + q_bonus))
            log.append(f"Editor {editor.get('name')} boosted quality by +{q_bonus}.")

        # Sound Designer -> small buzz bump
        sound = staff.get("Sound Designer")
        if sound:
            exp = sound.get("experience", 2)
            fame = sound.get("fame", 15)
            b_bonus = int(exp * 1 + (fame / 70.0) * 2)
            movie["buzz"] = int(movie.get("buzz", 0) + b_bonus)
            log.append(f"Sound Designer {sound.get('name')} added +{b_bonus} buzz.")

        # Marketing Manager -> pre-release visibility
        marketer = staff.get("Marketing Manager")
        if marketer:
            exp = marketer.get("experience", 2)
            fame = marketer.get("fame", 10)
            vis = int(exp * 1 + (fame / 80.0) * 3)
            movie["buzz"] = int(movie.get("buzz", 0) + vis)
            log.append(f"Marketing Manager {marketer.get('name')} increased pre-release visibility by +{vis}.")

        # Ensure buzz and quality fields exist for downstream code
        movie.setdefault("quality", 0)
        movie.setdefault("buzz", 0)

        return log