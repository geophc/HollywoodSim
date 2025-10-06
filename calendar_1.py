# HollywoodSim/game/calendar_1.py
# Dynamic in-game calendar with economic cycles, competition, and event-driven market effects

import random
from genres import GENRES as GENRE_LIST

class GameCalendar:
    def __init__(self, start_year=2025):
        self.year = start_year
        self.month = 1
        self.week = 1
        self.day = 1

        # Market + Economic State
        self.market_sentiment = 1.0
        self.economy_state = "stable"
        self.market_index = 100.0  # 📈 baseline for dashboard
        self.streaming_impact = 0.0
        self.competition_level = "medium"

        # Genre Trends
        self.trending_genres = self.new_trends()
        self.forecast_genres = self.generate_forecast()

        # Events
        self.events = self.generate_annual_events(self.year)
        self.special_events = []
        self.historical_events = []

        # Release strategy
        self.release_windows = self.calculate_release_windows()
        self.competition_releases = []
        self.box_office_history = {}

    def calculate_release_windows(self):
        return {
            "Q1": ["January", "February", "March"],
            "Q2": ["April", "May", "June"],
            "Q3": ["July", "August", "September"],
            "Q4": ["October", "November", "December"],
        }

    def month_name_from_num(self, m):
        return ["January","February","March","April","May","June","July","August","September","October","November","December"][m-1]


    # === Core Progression ===
    def advance(self, days=30):
        """Advance by ~month (default 30 days)."""
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
            self.on_year_change()

        self.on_month_change()
        self.update_market_conditions()
        self.update_market_index()
        return self.get_market_report()

    # === Event Hooks ===
    def on_month_change(self):
        if self.month % 3 == 1:
            self.trending_genres = self.forecast_genres
            self.forecast_genres = self.generate_forecast()
        if random.random() < 0.2:
            self.generate_special_event()
        self.generate_competition_releases()
        self.record_monthly_stats()

    def on_year_change(self):
        self.events = self.generate_annual_events(self.year)
        self.update_economy()

    # === Trend + Forecast ===
    def new_trends(self):
        return random.sample(list(GENRE_LIST.keys()), k=3)

    def generate_forecast(self):
        return random.sample(list(GENRE_LIST.keys()), k=3)

    def generate_annual_events(self, year):
        # ADDED 'importance' and 'description' for use in CalendarView
        return {
            1: {"name": "Awards Season", "bonus_genres": ["Drama", "Biography"], "market_boost": 1.1, "importance": "high", "description": "The peak of critical recognition. High-quality dramas and biographies perform exceptionally well."},
            6: {"name": "Summer Blockbuster", "bonus_genres": ["Action", "Sci-Fi"], "market_boost": 1.4, "importance": "high", "description": "The season for big budget spectacles. Action and Sci-Fi rule the box office."},
            10: {"name": "Halloween Horror Fest", "bonus_genres": ["Horror", "Thriller"], "market_boost": 1.3, "importance": "normal", "description": "Audiences crave thrills. Horror and Thrillers see a significant boost."},
            12: {"name": "Holiday Movie Rush", "bonus_genres": ["Family", "Comedy"], "market_boost": 1.4, "importance": "high", "description": "Families flock to cinemas for feel-good films. Comedies and Family movies dominate."},
        }

    def get_current_event(self):
        return self.events.get(self.month)

    # === Market Logic ===
    def update_market_conditions(self):
        self.market_sentiment = round(max(0.5, min(1.5, self.market_sentiment + random.uniform(-0.05, 0.05))), 2)
        self.streaming_impact = round(max(-0.3, min(0.3, self.streaming_impact + random.uniform(-0.02, 0.02))), 2)

    def update_economy(self):
        roll = random.random()
        if roll < 0.15:
            self.economy_state = "recession"
        elif roll < 0.30:
            self.economy_state = "boom"
        else:
            self.economy_state = "stable"

    def get_market_modifier(self):
        mod = self.market_sentiment
        if self.economy_state == "boom": mod *= 1.1
        elif self.economy_state == "recession": mod *= 0.9
        event = self.get_current_event()
        if event: mod *= event.get("market_boost", 1.0)
        for e in self.get_active_special_events():
            mod *= (1 + e["impact"])
        return round(mod, 2)

    def update_market_index(self):
        """Track overall market performance like a stock index."""
        mod = self.get_market_modifier()
        change = (mod - 1.0) * random.uniform(5, 10)
        self.market_index = round(max(50, min(150, self.market_index + change)), 2)

    def get_market_index_trend(self):
        """Returns 📈 or 📉 depending on last sentiment."""
        return "📈" if self.market_sentiment > 1.0 else "📉"
        
    def get_hype_index(self):
        """Calculates a 0-100 index for market hype/forecast gauge based on market_index."""
        # Normalize the typical market_index range (e.g., 50-150) to 0-100 for the progress bar.
        normalized_index = max(0, min(100, (self.market_index - 50)))
        return int(normalized_index)

    def generate_competition_releases(self):
        """
        Simulate other studios releasing films this month.
        These affect competition and box office performance indirectly.
        """
        num_releases = random.randint(1, 5)  # e.g. 1–5 competing releases
        self.competition_releases = []

        for _ in range(num_releases):
            genre = random.choice(list(GENRE_LIST.keys()))
            performance = round(random.uniform(40, 100), 2)  # arbitrary success index
            self.competition_releases.append({
                "title": f"Rival Film {random.randint(100,999)}",
                "genre": genre,
                "performance": performance
            })

        # Optional: adjust competition level
        avg_perf = sum(r["performance"] for r in self.competition_releases) / len(self.competition_releases)
        if avg_perf > 80:
            self.competition_level = "high"
        elif avg_perf < 50:
            self.competition_level = "low"
        else:
            self.competition_level = "medium"

    # === Events ===
    def generate_special_event(self):
        events = [
            {"name": "Streaming Wars Intensify", "impact": -0.1, "duration": 3},
            {"name": "New Tech Breakthrough", "impact": 0.15, "duration": 2},
            {"name": "Major Scandal Hits Competitor", "impact": -0.2, "duration": 2},
            {"name": "Prestigious Festival Buzz", "impact": 0.1, "duration": 1},
        ]
        e = random.choice(events).copy()
        e["start"] = (self.year, self.month)
        e["end"] = (self.year, min(12, self.month + e["duration"]))
        self.special_events.append(e)
        self.historical_events.append(e)

    def get_active_special_events(self):
        return [e for e in self.special_events if e["end"][0] > self.year or (e["end"][0] == self.year and e["end"][1] >= self.month)]

    # === Reporting ===
    def display(self):
        return f"{self.month_name()} {self.year}"

    def month_name(self):
        return ["January","February","March","April","May","June","July","August","September","October","November","December"][self.month-1]

    def record_monthly_stats(self):
        key = f"{self.year}-{self.month:02d}"
        self.box_office_history[key] = {
            "sentiment": self.market_sentiment,
            "market_index": self.market_index,
            "event": self.get_current_event()["name"] if self.get_current_event() else None,
            "economy": self.economy_state,
        }

    def get_market_report(self):
        e = self.get_current_event()
        return {
            "date": self.display(),
            "event": e["name"] if e else "None",
            "economy": self.economy_state,
            "sentiment": self.market_sentiment,
            "market_index": self.market_index,
            "trend": self.get_market_index_trend(),
            "trending_genres": self.trending_genres,
            "forecast_genres": self.forecast_genres,
            "special_events": [x["name"] for x in self.get_active_special_events()],
        }

    def simulate_forward(self, months=3):
        forecast = []
        for i in range(1, months + 1):
            m = (self.month - 1 + i) % 12 + 1
            y = self.year + ((self.month - 1 + i) // 12)
            e = self.events.get(m)
            forecast.append({
                "month": m,
                "year": y,
                "name": e["name"] if e else "None",
                "boost": e["market_boost"] if e else 1.0,
            })
        return forecast