# game/scripts.py

import random

RATINGS = {
    "G": {"min_age": 0, "max_audience": 1.00},
    "PG": {"min_age": 10, "max_audience": 0.90},
    "PG-13": {"min_age": 13, "max_audience": 0.85},
    "R": {"min_age": 17, "max_audience": 0.75},
    "NC-17": {"min_age": 18, "max_audience": 0.50}
}

GENRE_RATING_LIMITS = {
    "Drama": {"G", "PG", "PG-13", "R", "NC-17"},
    "Comedy": {"G", "PG", "PG-13", "R"},
    "Romance": {"G", "PG", "PG-13", "R"},
    "Action": {"PG", "PG-13", "R"},
    "Sci-Fi": {"PG", "PG-13", "R"},
    "Thriller": {"PG-13", "R", "NC-17"},
    "Horror": {"PG-13", "R", "NC-17"},
    "Family": {"G", "PG"},
    "Documentary": {"G", "PG", "PG-13"},
}


def assign_rating(tags, genre):
    adult_tags = {"sexual", "explicit", "violent", "dark", "gritty"}
    family_tags = {"family", "emotional", "musical", "lighthearted"}

    # Base rating logic
    if any(tag in tags for tag in adult_tags):
        if "sexual" in tags or "explicit" in tags:
            rating = "NC-17"
        else:
            rating = "R"
    elif any(tag in tags for tag in family_tags):
        rating = "PG"
    elif "quirky" in tags or "adventure" in tags:
        rating = "PG-13"
    else:
        rating = "G"

    # Apply genre restrictions
    allowed = GENRE_RATING_LIMITS.get(genre, {"G", "PG", "PG-13", "R", "NC-17"})
    if rating not in allowed:
        # Fallback to closest allowed rating
        fallback_order = ["G", "PG", "PG-13", "R", "NC-17"]
        for r in fallback_order:
            if r in allowed:
                return r
        return "PG-13"  # Default safe fallback

    return rating


def generate_script(calendar, current_year=2025, writer=None, director=None):
    titles = [
        "The Bitter End", "Quantum Hearts", "Midnight at the Arcade", "The Secret Dream",
        "Echoes of Tomorrow", "Painted Lies", "Beyond the Hollow", "Love in Low Orbit"
    ]

    genres = ["Drama", "Comedy", "Thriller", "Sci-Fi", "Romance", "Horror", "Action", "Family", "Documentary"]
    budget_classes = ["Low", "Mid", "High"]
    tag_pool = ["gritty", "emotional", "fast-paced", "cerebral", "quirky", "low-budget", "experimental", "action-heavy", "stylized"]
   
    title = random.choice(titles)
    genre = random.choice(genres)
    budget_class = random.choice(budget_classes)
    tags = random.sample(tag_pool, 2)
    rating = assign_rating(tags, genre)
    

    appeal = random.randint(1, 5)
    base_quality = random.randint(50, 70)

    pop = calendar.genre_popularity.get(genre, 50)
    appeal += (pop - 50) * 0.05

    # If writer is assigned, apply bonuses
    if writer:
        # 🎯 Genre match
        if genre == writer["specialty"]:
            base_quality += 10

        # ❤️ Shared tags
        overlap_tags = set(tags) & set(writer["tags"])
        base_quality += len(overlap_tags) * 1.5

        # 🎓 Education bonus
        if writer["education"] in ["Film School", "MFA Program", "Playwriting"]:
            base_quality += 3

        # 📚 Experience bonus (years active)
        career_length = current_year - writer["debut_year"]
        base_quality += min(career_length * 0.5, 5)

        # Clamp to range
        quality = round(min(100, max(40, base_quality)))

        # If writer has a notable script, increase quality
        #if writer:
         #   writer["film_history"].append({
          #      "title": title,
          #      "genre": genre,
          #      "budget_class": budget_class,
          #      "quality": quality,
          #      "year": current_year
          #  })
    
    else:
        quality = random.randint(50, 70)

        # Create a dummy writer if none provided
        writer = {
            "name": "Staff Writer",
            "specialty": genre,
            "tags": [],
            "education": "Self-Taught",
            "debut_year": current_year - 1,
            "fame": 10,
            "salary": 0.5,
            "film_history": [],
            "awards": [],
            "reputation": "Unknown",
            "prestige": 0,
            "interests": [],
        }

    


    return {
        "title": title,
        "genre": genre,
        "budget_class": budget_class,
        "appeal": appeal,
        "tags": tags,
        "quality": quality,
        "writer": writer,
        "director": director,
        "rating": rating,
        "release_year": current_year,
    }
