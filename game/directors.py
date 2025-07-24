# game/directors.py

import random


def generate_director(current_year=2025):
    name = random.choice([
        "Alex Monroe", "Jamie Kingsley", "Morgan Rivers", "Taylor Chen",
        "Jordan Clarke", "Riley Foster", "Drew Patel", "Hayden Lee"
    ])
    GENRES = ["Action", "Comedy", "Drama", "Romance", "Sci-Fi", "Horror", "Thriller"]
    TAGS = ["visual", "blockbuster", "methodical", "actor-friendly", "gritty", "stylized", "experimental"]
    fame = random.randint(20, 75) # Add fame

    director = {
        "name": name,
        "age": random.randint(30, 60),
        "fame": fame,
        "salary": round(0.5 + fame * 0.03, 2), # Add salary
        "debut_year": current_year - random.randint(0, 10),
        "education": random.choice(["Film School", "MFA", "Self-Taught"]),
        "film_history": [],
        "genre_focus": random.choice(GENRES),
        "style_tags": random.sample(TAGS, k=2)
    }
    return director
