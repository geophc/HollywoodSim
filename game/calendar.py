# game/calendar.py
# game/calendar.py

class GameCalendar:
    def __init__(self):
        self.month = 1
        self.year = 2025

    def advance(self):
        """Advance to the next month. Roll over to next year if needed."""
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1

    def display(self):
        """Return a human-readable version of the current date."""
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        return f"{months[self.month - 1]} {self.year}"

    def current_date(self):
        """Return the current date as a tuple: (year, month)"""
        return (self.year, self.month)

    def matches(self, date_tuple):
        """Check if a (year, month) tuple matches the current date."""
        return self.current_date() == date_tuple
