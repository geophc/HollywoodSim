# game/scripts.py

import random

def generate_script(current_year=2025, writer=None, director=None):
    titles = [
        "The Bitter End", "Quantum Hearts", "Midnight at the Arcade", "The Secret Dream",
        "Echoes of Tomorrow", "Painted Lies", "Beyond the Hollow", "Love in Low Orbit"
    ]

    genres = ["Drama", "Comedy", "Thriller", "Sci-Fi", "Romance", "Horror", "Action"]
    budget_classes = ["Low", "Mid", "High"]
    tag_pool = ["gritty", "emotional", "fast-paced", "cerebral", "quirky", "low-budget", "experimental", "action-heavy", "stylized"]

    title = random.choice(titles)
    genre = random.choice(genres)
    budget_class = random.choice(budget_classes)
    tags = random.sample(tag_pool, 2)

    appeal = random.randint(1, 5)

    # --- Base quality ---
    base_quality = random.randint(50, 70)

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
        if writer:
            writer["film_history"].append({
                "title": title,
                "genre": genre,
                "budget_class": budget_class,
                "quality": quality,
                "year": current_year
            })
    
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
    }
