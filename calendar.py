# game/calendar.py
import random

GENRES = ["Action", "Comedy", "Drama", "Romance", "Sci-Fi", "Horror", "Thriller"]

class GameCalendar:
    def __init__(self):
        self.year = 2025
        self.month = 1
        self.trending_genres = self.new_trends()
        self.forecast_genres = self.generate_forecast()

    def advance(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1

        if self.month % 3 == 1:  # New quarter
            self.trending_genres = self.forecast_genres
            self.forecast_genres = self.generate_forecast()

    def new_trends(self):
        return random.sample(GENRES, k=2)  # Pick 2 trending genres

    def display(self):
        return f"{self.month_name()} {self.year}"

    def month_name(self):
        return [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ][self.month - 1]
    
    def generate_forecast(self):
        return random.sample(GENRES, k=2)
