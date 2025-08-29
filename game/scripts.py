import random
import game_data

# --- Ratings system ---
RATINGS = {
    "G": {"min_age": 0, "max_audience": 1.00},
    "PG": {"min_age": 10, "max_audience": 0.90},
    "PG-13": {"min_age": 13, "max_audience": 0.85},
    "R": {"min_age": 17, "max_audience": 0.75},
    "NC-17": {"min_age": 18, "max_audience": 0.50},
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

# --- Rating assignment ---
def assign_rating(tags, genre):
    """Assign a rating based on tags and genre constraints."""
    adult_tags = {"sexual", "explicit", "violent", "dark", "gritty"}
    family_tags = {"family", "emotional", "musical", "lighthearted"}

    rating = "PG-13"
    if any(tag in tags for tag in adult_tags):
        rating = "R"
    if "sexual" in tags or "explicit" in tags:
        rating = "NC-17"
    elif any(tag in tags for tag in family_tags):
        rating = "PG"
    elif genre == "Family":
        rating = "G"

    allowed = GENRE_RATING_LIMITS.get(genre, set(RATINGS.keys()))
    if rating not in allowed:
        # fallback: choose the most permissive rating allowed
        rating = sorted(allowed, key=lambda r: RATINGS[r]["min_age"], reverse=True)[0]

    return rating


# --- Script Description Generator ---
def generate_script_description(script):
    """Generate a flavourful description for a script market listing."""

    # Genre-based moods
    moods = {
        "Drama": ["an intense character study", "an emotional journey", "a gritty exploration of truth"],
        "Comedy": ["a light-hearted romp", "a clever satire", "an offbeat misadventure"],
        "Action": ["a high-octane thrill ride", "an explosive adventure", "an adrenaline-fuelled spectacle"],
        "Horror": ["a chilling nightmare", "a slow-burning terror", "a twisted tale of fear"],
        "Romance": ["a sweeping love story", "a bittersweet romance", "an unexpected connection"],
        "Sci-Fi": ["a mind-bending odyssey", "a futuristic vision", "a speculative adventure"],
        "Fantasy": ["a sprawling epic", "a magical journey", "a mythic tale"],
    }

    # Quality flavour
    q = script.get("quality", 0)
    if q >= 80:
        quality_desc = random.choice(["festival-ready draft", "polished and ambitious script", "award-bait material"])
    elif q >= 60:
        quality_desc = random.choice(["solid working draft", "promising rewrite", "refined treatment"])
    else:
        quality_desc = random.choice(["rough outline", "uneven draft", "early concept"])

    # Buzz flavour
    b = script.get("buzz", 0)
    if b >= 8:
        buzz_desc = random.choice(["Producers are buzzing about it.", "Studios are already circling.", "Hot topic at industry mixers."])
    elif b >= 5:
        buzz_desc = random.choice(["Industry whispers suggest potential.", "A script with quiet momentum.", "Some critics are curious."])
    else:
        buzz_desc = random.choice(["Mostly ignored for now.", "Still waiting for attention.", "Unnoticed in the market — so far."])

    # Source flavour
    source_flair = {
        "original": "entirely original concept",
        "adaptation": "based on existing material",
        "remake": "a bold reimagining",
        "sequel": "a continuation of a known story",
    }

    return (
        f"A {script.get('length', 'feature')} {script['genre']} — {random.choice(moods.get(script['genre'], ['unique story']))}, "
        f"{quality_desc}. It’s an {source_flair.get(script['source'], 'original idea')}, {buzz_desc}"
    )


# --- Script Generation ---
def generate_script(calendar, writer, source_key=None):
    """Generate a new script from a contracted writer."""
    if not writer:
        raise ValueError("Cannot generate a script without a writer.")

    current_year = calendar.year

    # Source material
    source_key = source_key or random.choice(list(game_data.SOURCE_TYPES.keys()))
    source_data = game_data.SOURCE_TYPES[source_key]

    # Genre influenced by writer specialty
    specialty = writer.get("specialty")
    possible_genres = [g for g in source_data["associated_genres"] if g == specialty]
    genre = random.choice(possible_genres) if possible_genres else random.choice(source_data["associated_genres"])
    genre_data = game_data.GENRES[genre]

    # Title generation
    title_formats = {"default": ["{prefix} {noun}", "{noun} of the {noun2}"]}
    title_parts = game_data.SCRIPT_TITLES_BY_GENRE.get(genre, {
        "prefixes": ["The"],
        "nouns": ["Story"],
        "noun2": ["Dream"],
    })
    structure = random.choice(title_formats.get(genre, title_formats["default"]))
    title_data = {
        "prefix": random.choice(title_parts.get("prefixes", ["The"])),
        "noun": random.choice(title_parts.get("nouns", ["Story"])),
        "noun2": random.choice(title_parts.get("noun2", ["Dream"])),
        "mid_phrase": random.choice(game_data.MID_PHRASES),
        "place": random.choice(game_data.PLACES),
        "adjective": random.choice(game_data.ADJECTIVES),
    }
    try:
        title = structure.format(**title_data).title()
    except KeyError:
        title = f"{title_data['prefix']} {title_data['noun']}"

    # Tags & theme
    genre_tags = random.sample(genre_data["common_tags"], k=2)
    writer_tags = random.sample(writer.get("tags", []), k=min(2, len(writer.get("tags", []))))
    theme_key = random.choice(list(game_data.THEMES.keys()))
    theme = game_data.THEMES[theme_key]["name"]
    tags = list(set(genre_tags + writer_tags + [theme]))

    # Rating
    rating = assign_rating(tags, genre)

    # Quality calculation
    potential_quality = 40
    if specialty == genre:
        potential_quality += 15
    if writer.get("education") in ["Film School", "MFA Program"]:
        potential_quality += 5
    potential_quality += min((current_year - writer.get("debut_year", current_year)) * 0.5, 10)
    potential_quality = round(max(30, min(100, potential_quality * writer.get("skill_level", 1.0))))

    initial_quality = round(potential_quality * random.uniform(0.6, 0.85))
    appeal = round(random.uniform(0.3, 1.0), 2)
    budget_class = random.choice(genre_data["budget_affinity"])

    # Script dict
    script = {
        "title": title,
        "genre": genre,
        "source": source_data["name"],
        "rating": rating,
        "tags": tags,
        "theme": theme,
        "writer": writer,
        "status": "first_draft",
        "quality": initial_quality,
        "appeal": appeal,
        "source_key": source_key,
        "potential_quality": potential_quality,
        "draft_number": 1,
        "rewrite_history": [writer["name"]],
        "base_buzz": source_data["base_buzz"],
        "budget_class": budget_class,
    }

    # Buzz calc
    buzz = 10 + int(potential_quality / 10)
    if genre == specialty:
        buzz += 5
    if "controversial" in tags and "edgy" in writer.get("style", []):
        buzz += 4
    if "family" in tags and "heartwarming" in writer.get("style", []):
        buzz += 3
    buzz += random.randint(-3, 3)
    script["buzz"] = max(0, buzz)

    # Description
    script["description"] = generate_script_description(script)

    return script


# --- Script Rewrite ---
def rewrite_script(script, writer, calendar):
    """Rewrite a script with a contracted writer."""
    if script["status"] == "approved":
        print(f"Cannot rewrite '{script['title']}', already approved.")
        return script

    improvement = 0
    if writer:
        if writer.get("specialty") == script["genre"]:
            improvement += 10
        overlap = set(script["tags"]) & set(writer.get("tags", []))
        improvement += len(overlap) * 4
        improvement += min((calendar.year - writer.get("debut_year", calendar.year)) * 0.25, 8)

    draft_penalty = (script["draft_number"] - 1) * 2
    net = max(0, improvement - draft_penalty)
    quality_gap = script["potential_quality"] - script["quality"]
    actual_improve = min(net, quality_gap)

    script["quality"] = min(100, round(script["quality"] + actual_improve))
    script["draft_number"] += 1
    if writer["name"] not in script["rewrite_history"]:
        script["rewrite_history"].append(writer["name"])

    # Buzz recalculation
    buzz = 10 + int(script["quality"] / 10)
    if writer.get("specialty") == script["genre"]:
        buzz += 5
    script["buzz"] = max(0, buzz)

    print(f"'{script['title']}' rewritten by {writer['name']}. Quality is now {script['quality']}.")
    return script


# --- Finalize Script ---
def finalize_script(script, studio, calendar, draft_pool=None):
    """Mark a script as approved and ready for production."""
    script["status"] = "approved"
    script["finalized_turn"] = (calendar.year, calendar.month)

    if not hasattr(studio, "finalized_scripts"):
        studio.finalized_scripts = []
    studio.finalized_scripts.append(script)

    if draft_pool and script in draft_pool:
        draft_pool.remove(script)

    print(f"\n✅ Script '{script['title']}' has been finalized and is ready for production!")
    return script
