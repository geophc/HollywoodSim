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
    # Sort by restrictiveness (based on min_age)
        valid_ratings = sorted(allowed_ratings, key=lambda r: RATINGS[r]["min_age"], reverse=True)
        rating = valid_ratings[0] if valid_ratings else "PG-13"
        if "PG-13" in allowed_ratings: return "PG-13"
        if "PG" in allowed_ratings: return "PG"
        if "G" in allowed_ratings: return "G"
        else:
            if "PG-13" in allowed_ratings: return "PG-13"
            if "R" in allowed_ratings: return "R"

    return rating


def generate_script(calendar, writer, source_key=None):
    
    """
    Generates a script based on a chosen source material and writer.
    This version is fully driven by the game_data.py file.
    """
    current_year = calendar.year
    source_key = source_key or random.choice(list(game_data.SOURCE_TYPES.keys()))
    source_data = game_data.SOURCE_TYPES[source_key]
        
    # 1. Determine Genre from Source Material
    genre = random.choice(source_data["associated_genres"])
    genre_data = game_data.GENRES[genre]

    # 2. Generate a more varied Thematic Title

    # Choose title structure format
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

    # Word data for filling the structure
    title_parts = game_data.SCRIPT_TITLES_BY_GENRE.get(genre, {
    "prefixes": ["The"], 
    "nouns": ["Dream"], 
    "noun2": ["Dream"]
    })
    # If no specific parts, use a default
    if not title_parts:
        title_parts = {
            "prefixes": ["The"],
            "nouns": ["Story"],
            "noun2": ["Dream"]
        }       

    # Select structure template
    structure_pool = genre_format_bias.get(genre, game_data.TITLE_STRUCTURES)
    structure = random.choice(structure_pool)

    # Fill in blanks for the chosen structure
    title_data = {
        "prefix": random.choice(title_parts.get("prefixes", ["The"])),
        "noun": random.choice(title_parts.get("nouns", ["Story"])),
        "noun2": random.choice(title_parts.get("nouns", ["Dream"])),
        "mid_phrase": random.choice(game_data.MID_PHRASES),
        "place": random.choice(game_data.PLACES),
        "adjective": random.choice(game_data.ADJECTIVES),
    }

    # Format title
    try:
        title = structure.format(**title_data)
    except KeyError as e:
        print(f"⚠️ Missing field in title format: {e}")
        title = f"{random.choice(title_data['prefixes'])} {random.choice(title_data['nouns'])}"

    title = title.title()

    # 3. Determine Tags and Themes
    # Pull tags from the genre's common tags and add a random theme
    tags = random.sample(genre_data["common_tags"], k=2)
    chosen_theme_key = random.choice(list(game_data.THEMES.keys()))
    chosen_theme = game_data.THEMES[chosen_theme_key]
    tags.append(chosen_theme["name"]) # Add the theme as a tag

    # 4. Assign Rating
    rating = assign_rating(tags, genre)

    # 5. Calculate Potential Quality
    # This now incorporates the writer's skill AND the source material's potential
    potential_quality = 50 # Base potential
    
    # Writer contribution
    if writer.get("specialty") == genre:
        potential_quality += 15 # Writer is in their element
    if writer.get("education") in ["Film School", "MFA Program"]:
        potential_quality += 5
    career_length = current_year - writer.get("debut_year", current_year)
    potential_quality += min(career_length * 0.5, 10) # Experience bonus

    # Source Material & Theme contribution
    potential_quality += (source_data["prestige_multiplier"] - 1.0) * 10
    potential_quality += chosen_theme["prestige_modifier"] * 10

    # Ensure quality is within bounds (e.g., 30-100)
    potential_quality = round(max(30, min(100, potential_quality)))
    initial_quality = round(potential_quality * random.uniform(0.60, 0.85))
    appeal = round(random.uniform(0.3, 1.0), 2)  # You can customize how it's calculated

    return {
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
        "base_buzz": source_data["base_buzz"], # Pass buzz from source
        "budget_class": random.choice(genre_data["budget_affinity"]),
    }

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