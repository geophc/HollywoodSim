# game/scripts.py

import random
import game_data

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
    "Musical": {"G", "PG", "PG-13", "R"},
    "Animation": {"G", "PG", "PG-13"},
    "Western": {"G", "PG", "PG-13", "R"},
}


def assign_rating(tags, genre):
    """
    Determines a script's movie rating based on its tags and genre.
    """
    adult_tags = {"sexual", "explicit", "violent", "dark", "gritty"}
    family_tags = {"family", "emotional", "musical", "lighthearted"}

    rating = "PG-13"  # Start with a neutral default

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
        # Fallback: Pick the highest (most restrictive) allowed rating
        valid_ratings = sorted(allowed_ratings, key=lambda r: RATINGS[r]["min_age"], reverse=True)
        rating = valid_ratings[0] if valid_ratings else "PG-13"

    return rating


def generate_script_buzz(script):
    base = 10  # minimum baseline buzz
    buzz = base

    # Quality and potential influence
    buzz += int(script.get("potential_quality", 50) / 10)

    # Genre effects
    genre = script.get("genre", "")
    writer = script.get("writer", {})
    if genre in ["Horror", "Thriller", "Action"]:
        buzz += 5
    if genre == writer.get("specialty"):
        buzz += 3

    # Tag influence
    tags = script.get("tags", [])
    if "fresh_voice" in tags:
        buzz += 4
    if "based_on_book" in tags or "true_story" in tags:
        buzz += 5
    if "controversial" in tags:
        buzz += 6
    if "debut_writer" in tags:
        buzz += 2

    # Random market noise
    buzz += random.randint(-3, 3)

    return max(0, buzz)

def generate_script(calendar, writer, source_key=None):
    """
    Generates a script based on a chosen source material and writer.
    All data is pulled from game_data.py.
    """
    current_year = calendar.year
    source_key = source_key or random.choice(list(game_data.SOURCE_TYPES.keys()))
    source_data = game_data.SOURCE_TYPES[source_key]

    # 1. Determine Genre from Source Material
    genre = random.choice(source_data["associated_genres"])
    genre_data = game_data.GENRES[genre]

    # 2. Generate a thematic Title
    genre_format_bias = {
        "Horror": ["{adjective} {noun}", "{noun} of the {noun2}"],
        "Romance": ["The {noun} {mid_phrase} {place}", "{prefix} {noun}"],
        "Sci-Fi": ["{prefix} {noun} {mid_phrase} {place}", "{noun} from the {place}"],
        "Thriller": ["{adjective} {noun}", "{noun} in the {place}"],
        "Family": ["{noun} of {place}", "{adjective} {noun}"],
        "Comedy": ["{noun} {mid_phrase} {place}", "{prefix} {noun}"],
        "Drama": ["{noun} {mid_phrase} {place}", "{prefix} {noun}"],
        "Action": ["{adjective} {noun}", "{noun} of the {place}"],
        "Documentary": ["{noun} of {place}", "{adjective} {noun}"],
        "Musical": ["{noun} {mid_phrase} {place}", "{prefix} {noun}"],
        "Animation": ["{noun} {mid_phrase} {place}", "{prefix} {noun}"],
        "Western": ["{noun} of the {place}", "{adjective} {noun}"],
        "default": ["{prefix} {noun}", "{noun} of the {noun2}"]
    }

    title_parts = game_data.SCRIPT_TITLES_BY_GENRE.get(genre, {
        "prefixes": ["The"],
        "nouns": ["Dream"],
        "noun2": ["Dream"]
    })

    structure_pool = genre_format_bias.get(genre, genre_format_bias["default"])
    structure = random.choice(structure_pool)

    title_data = {
        "prefix": random.choice(title_parts.get("prefixes", ["The"])),
        "noun": random.choice(title_parts.get("nouns", ["Story"])),
        "noun2": random.choice(title_parts.get("noun2", ["Dream"])),
        "mid_phrase": random.choice(game_data.MID_PHRASES),
        "place": random.choice(game_data.PLACES),
        "adjective": random.choice(game_data.ADJECTIVES)
    }

    try:
        title = structure.format(**title_data)
    except KeyError as e:
        print(f"⚠️ Missing field in title format: {e}")
        title = f"{title_data['prefix']} {title_data['noun']}"
    title = title.title()

    # 3. Determine Tags and Themes
    tags = random.sample(genre_data["common_tags"], k=2)
    chosen_theme_key = random.choice(list(game_data.THEMES.keys()))
    chosen_theme = game_data.THEMES[chosen_theme_key]
    tags.append(chosen_theme["name"])

    # 4. Assign Rating
    rating = assign_rating(tags, genre)


    # 5. Calculate Potential Quality
    potential_quality = 50
    if writer.get("specialty") == genre:
        potential_quality += 15
    if writer.get("education") in ["Film School", "MFA Program"]:
        potential_quality += 5
    career_length = current_year - writer.get("debut_year", current_year)
    potential_quality += min(career_length * 0.5, 10)
    potential_quality += max(0, (source_data["prestige_multiplier"] - 1.0) * 10)
    potential_quality += chosen_theme["prestige_modifier"] * 10
    potential_quality = round(max(30, min(100, potential_quality)))
    initial_quality = round(potential_quality * random.uniform(0.60, 0.85))
    appeal = round(random.uniform(0.3, 1.0), 2)

    script = {
        "title": title,
        "genre": genre,
        "source": source_data["name"],
        "rating": rating,
        "tags": tags,
        "theme": chosen_theme["name"],
        "writer": writer,
        "status": "first_draft",
        "quality": initial_quality,
        "appeal": appeal,
        "source_key": source_key,
        "potential_quality": potential_quality,
        "draft_number": 1,
        "rewrite_history": [writer["name"]],
        "base_buzz": source_data["base_buzz"],
        "budget_class": random.choice(genre_data["budget_affinity"])
    }

    # Calculate and assign buzz now
    script["buzz"] = generate_script_buzz(script)

    return script


def rewrite_script(script, new_writer, calendar):
    """
    Improves a script's quality through a rewrite pass by a new writer.
    """
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
        career_length = current_year - new_writer.get("debut_year", current_year)
        improvement_points += min(career_length * 0.25, 8)

    draft_penalty = (script["draft_number"] - 1) * 2
    net_improvement = max(0, improvement_points - draft_penalty)
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
    Finalizes a script, approving it for production or shelving it based on its quality and the studio's prestige.
    """
    required_quality = 30 + (studio_prestige * 1.5)
    if script["quality"] >= required_quality:
        script["status"] = "approved"
        print(f"✅ '{script['title']}' has been approved for production! (Quality: {script['quality']})")
    else:
        script["status"] = "shelved"
        print(f"❌ '{script['title']}' was shelved. (Quality: {script['quality']}, Required: {required_quality})")
    return script