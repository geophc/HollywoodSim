# calendar.py
import random
from game_data import GENRES as GENRE_LIST

class GameCalendar:
    def __init__(self):
        self.year = 2025
        self.month = 1
        self.trending_genres = self.new_trends()
        self.forecast_genres = self.generate_forecast()
        self.events = self.generate_annual_events(self.year)

    def advance(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
            # Regenerate annual events for the new year
            self.events = self.generate_annual_events(self.year)

        # Update quarterly trends
        if self.month % 3 == 1:
            self.trending_genres = self.forecast_genres
            self.forecast_genres = self.generate_forecast()

    def new_trends(self):
        keys = list(GENRE_LIST.keys())
        return random.sample(keys, k=min(2, len(keys)))

    def display(self):
        return f"{self.month_name()} {self.year}"

    def month_name(self):
        return [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ][self.month - 1]

    def generate_forecast(self):
        keys = list(GENRE_LIST.keys())
        return random.sample(keys, k=min(2, len(keys)))
    
    def generate_annual_events(self, year):
        """Create a fixed annual schedule of events that can influence the market."""
        return {
            1: "Awards Season Kick-off",
            2: "Oscars Buzz",
            6: "Summer Blockbuster Season",
            7: "Summer Blockbuster Season",
            8: "Summer Blockbuster Season",
            10: "Holiday Movie Rush",
            12: "Holiday Movie Rush"
        }

    def get_current_event(self):
        """Returns the event for the current month, if any."""
        return self.events.get(self.month)