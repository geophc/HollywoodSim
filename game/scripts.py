# game/scripts.py
import random

# Centralized data for movie ratings and their restrictions by genre.
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
    """
    Determines a script's movie rating based on its tags and genre.
    """
    adult_tags = {"sexual", "explicit", "violent", "dark", "gritty"}
    family_tags = {"family", "emotional", "musical", "lighthearted"}
    
    rating = "PG-13" # Start with a neutral default

    if any(tag in tags for tag in adult_tags):
        rating = "R"
    if "sexual" in tags or "explicit" in tags:
        rating = "NC-17"
    elif any(tag in tags for tag in family_tags):
        rating = "PG"
    elif genre == "Family":
        rating = "G"

    # Ensure the assigned rating is allowed for the genre
    allowed_ratings = GENRE_RATING_LIMITS.get(genre, set(RATINGS.keys()))
    if rating not in allowed_ratings:
        if rating in ["R", "NC-17"]:
             if "PG-13" in allowed_ratings: return "PG-13"
             if "PG" in allowed_ratings: return "PG"
             if "G" in allowed_ratings: return "G"
        else:
            if "PG-13" in allowed_ratings: return "PG-13"
            if "R" in allowed_ratings: return "R"

    return rating


# FIX: Changed function signature to accept the 'calendar' object.
def generate_script(calendar, writer=None):
    """
    Generates a first draft of a script, calculating its initial quality
    and potential quality based on the writer's skills.
    """
    # FIX: Extract the integer year from the calendar object.
    current_year = calendar.year

    titles = [
        "The Bitter End", "Quantum Hearts", "Midnight at the Arcade", "The Secret Dream",
        "Echoes of Tomorrow", "Painted Lies", "Beyond the Hollow", "Love in Low Orbit"
    ]
    genres = ["Drama", "Comedy", "Thriller", "Sci-Fi", "Romance", "Horror", "Action", "Family", "Documentary"]
    tag_pool = ["gritty", "emotional", "fast-paced", "cerebral", "quirky", "low-budget", "experimental", "action-heavy", "stylized", "family", "violent"]
    
    if not writer:
        writer = {
            "name": "Staff Writer", "specialty": random.choice(genres), "tags": [],
            "education": "Self-Taught", "debut_year": current_year - 1, "fame": 10,
            "salary": 0.5, "film_history": [], "interests": [],
        }

    title = random.choice(titles)
    genre = random.choice(genres)
    tags = random.sample(tag_pool, 2)
    rating = assign_rating(tags, genre)
    
    potential_quality = 65
    if writer:
        if genre == writer.get("specialty"):
            potential_quality += 15
        
        overlap_tags = set(tags) & set(writer.get("tags", []))
        potential_quality += len(overlap_tags) * 3
        
        if writer.get("education") in ["Film School", "MFA Program", "Playwriting"]:
            potential_quality += 5
        
        # FIX: This line now works correctly because current_year is an integer.
        career_length = current_year - writer.get("debut_year", current_year)
        potential_quality += min(career_length * 0.5, 10)

    potential_quality = round(min(100, potential_quality))
    initial_quality = round(potential_quality * random.uniform(0.60, 0.85))

    return {
        "title": title,
        "genre": genre,
        "rating": rating,
        "tags": tags,
        "writer": writer,
        "status": "first_draft",
        "quality": initial_quality,
        "potential_quality": potential_quality,
        "draft_number": 1,
        "rewrite_history": [writer["name"]],
        "budget_class": random.choice(["Low", "Mid", "High"]), # Added for compatibility
        "appeal": random.randint(1, 5), # Added for compatibility
    }


# FIX: Changed function signature to accept the 'calendar' object.
def rewrite_script(script, new_writer, calendar):
    """
    Improves a script's quality through a rewrite pass by a new writer.
    """
    # FIX: Extract the integer year from the calendar object.
    current_year = calendar.year

    if script["status"] == "approved":
        print(f"Cannot rewrite '{script['title']}', it is already approved.")
        return script

    improvement_points = 0
    if new_writer:
        if script["genre"] == new_writer.get("specialty"):
            improvement_points += 10
        
        overlap_tags = set(script["tags"]) & set(new_writer.get("tags", []))
        improvement_points += len(overlap_tags) * 4
        
        # FIX: This line now works correctly.
        career_length = current_year - new_writer.get("debut_year", current_year)
        improvement_points += min(career_length * 0.25, 8)

    # Diminishing returns for each subsequent rewrite
    draft_penalty = (script["draft_number"] - 1) * 2
    net_improvement = max(0, improvement_points - draft_penalty)

    # The quality can only increase up to its potential
    quality_gap = script["potential_quality"] - script["quality"]
    actual_improvement = min(net_improvement, quality_gap)

    script["quality"] = min(100, round(script["quality"] + actual_improvement))
    script["draft_number"] += 1
    
    if new_writer["name"] not in script["rewrite_history"]:
        script["rewrite_history"].append(new_writer["name"])

    print(f"'{script['title']}' rewritten by {new_writer['name']}. Quality improved to {script['quality']}.")
    return script


def finalize_script(script, studio_prestige=0):
    """
    Finalizes a script, approving it for production or shelving it
    based on its quality and the studio's prestige.
    """
    required_quality = 30 + (studio_prestige * 1.5)

    if script["quality"] >= required_quality:
        script["status"] = "approved"
        print(f"✅ '{script['title']}' has been approved for production! (Quality: {script['quality']})")
    else:
        script["status"] = "shelved"
        print(f"❌ '{script['title']}' was shelved. (Quality: {script['quality']}, Required: {required_quality})")
    
    return script