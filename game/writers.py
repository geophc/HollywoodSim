# game/writers.py

import random

def generate_writer():
    """
    Creates a writer with a name, genre specialty, and fame.
    Future extensions can include film history and compatibility effects.
    """
    names = [
        "Jordan Quinn", "Alex Riley", "Casey Wells", "Sam Avery", "Taylor Banks",
        "Morgan Stone", "Riley James", "Quinn Harper", "Avery Blake", "Charlie West"
    ]
    
    specialties = ["Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Action", "Thriller"]
    
    name = random.choice(names)
    specialty = random.choice(specialties)
    fame = random.randint(20, 80)  # This could influence script appeal in the future

    return {
        "name": name,
        "specialty": specialty,
        "fame": fame,
        "tags": [specialty],
        "age": random.randint(28, 55),
        "debut_year": 2025,
        "history": []  # Fill this with scripts as their work accumulates
    }
