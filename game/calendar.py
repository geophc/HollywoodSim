# game/calendar.py
import random
# Import the dictionary as 'GENRE_DATA' and the function
from genres import GENRES as GENRE_DATA, season_for_month

GENRE_LIST = ["Action", "Comedy", "Drama", "Romance", "Sci-Fi", "Horror", "Thriller"]

class GameCalendar:
    def __init__(self):
        self.year = 2025
        self.month = 1
        self.trending_genres = self.new_trends()
        self.forecast_genres = self.generate_forecast()
        self.genre_popularity = {g: random.randint(40, 60) for g in GENRE_LIST}

    def advance(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1

        if self.month % 3 == 1:  # New quarter
            self.trending_genres = self.forecast_genres
            self.forecast_genres = self.generate_forecast()

        for genre, props in GENRE_DATA.items():
            current = self.genre_popularity.get(genre, 50) # Use .get() for safety
            bonus = props["trend_bonus"] if season_for_month(self.month) in props["peak_seasons"] else 0
            drift = random.randint(-3, 3) + bonus // 2
            self.genre_popularity[genre] = max(0, min(100, current + drift))

    def new_trends(self):
        return random.sample(GENRE_LIST, k=2)  # Pick 2 trending genres

    def display(self):
        return f"{self.month_name()} {self.year}"
        print("🔮 3‑Month Genre Forecast:")
        for genre, val in self.genre_popularity.items():
            print(f"   {genre}: {val:.0f}% popular")

    def month_name(self):
        return [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ][self.month - 1]
    
    def generate_forecast(self):
        return random.sample(GENRE_LIST, k=2)
