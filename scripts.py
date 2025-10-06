# HollywoodSim/game/scripts.py
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
    "Fantasy": {"PG", "PG-13", "R"},
}


def assign_rating(tags, genre):
    """Assign a rating based on tags and genre constraints.

    If the computed rating isn't allowed for the genre, pick the
    most permissive rating from the allowed set (lowest min_age).
    """
    adult_tags = {"sexual", "explicit", "violent", "dark", "gritty"}
    family_tags = {"family", "emotional", "musical", "lighthearted"}

    # Defensive: ensure `tags` is iterable
    tags = tags or []

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
        # fallback: choose the most permissive rating allowed (lowest min_age)
        allowed_list = sorted(list(allowed), key=lambda r: RATINGS.get(r, {}).get("min_age", 0))
        rating = allowed_list[0] if allowed_list else "PG-13"

    return rating


# --- Script Description Generator ---
def generate_script_description(script):
    """Generate a flavourful description for a script market listing."""
    # Genre-based moods (defensive: supply fallback mood)
    moods = {
        "Drama": ["an intense character study", "an emotional journey", "a gritty exploration of truth"],
        "Comedy": ["a light-hearted romp", "a clever satire", "an offbeat misadventure"],
        "Action": ["a high-octane thrill ride", "an explosive adventure", "an adrenaline-fuelled spectacle"],
        "Horror": ["a chilling nightmare", "a slow-burning terror", "a twisted tale of fear"],
        "Romance": ["a sweeping love story", "a bittersweet romance", "an unexpected connection"],
        "Sci-Fi": ["a mind-bending odyssey", "a futuristic vision", "a speculative adventure"],
        "Fantasy": ["a sprawling epic", "a magical journey", "a mythic tale"],
    }

    q = script.get("quality", 0)
    if q >= 80:
        quality_desc = random.choice(["festival-ready draft", "polished and ambitious script", "award-bait material"])
    elif q >= 60:
        quality_desc = random.choice(["solid working draft", "promising rewrite", "refined treatment"])
    else:
        quality_desc = random.choice(["rough outline", "uneven draft", "early concept"])

    b = script.get("buzz", 0)
    if b >= 8:
        buzz_desc = random.choice(["Producers are buzzing about it.", "Studios are already circling.", "Hot topic at industry mixers."])
    elif b >= 5:
        buzz_desc = random.choice(["Industry whispers suggest potential.", "A script with quiet momentum.", "Some critics are curious."])
    else:
        buzz_desc = random.choice(["Mostly ignored for now.", "Still waiting for attention.", "Unnoticed in the market — so far."])

    source_flair = {
        "original": "entirely original concept",
        "adaptation": "based on existing material",
        "remake": "a bold reimagining",
        "sequel": "a continuation of a known story",
    }

    genre = script.get("genre", "Unknown")
    mood = random.choice(moods.get(genre, ["a unique story"]))

    return (
        f"A {script.get('length', 'feature')} {genre} — {mood}, "
        f"{quality_desc}. It’s {source_flair.get(script.get('source', '').lower(), 'an original idea')}, {buzz_desc}"
    )


# --- Script Generation ---
def generate_script(calendar, writer, source_key=None):
    """Generate a new script from a contracted writer.

    Uses safe defaults so missing writer/game_data fields don't crash.
    """
    if not writer:
        raise ValueError("Cannot generate a script without a writer.")

    current_year = getattr(calendar, "year", 2025)

    # Source material - safe lookup and default
    source_key = source_key or random.choice(list(getattr(game_data, "SOURCE_TYPES", {"original": {"name": "Original", "associated_genres": list(getattr(game_data, 'GENRES', {}).keys()), "base_buzz": 0}}).keys()))
    source_data = getattr(game_data, "SOURCE_TYPES", {}).get(source_key, {"name": source_key, "associated_genres": list(getattr(game_data, "GENRES", {}).keys()), "base_buzz": 0})

    # Writer attributes with safe defaults
    specialty = writer.get("specialty") or writer.get("tags", [None])[0]
    writer_tags = writer.get("tags", []) or []
    writer_style = writer.get("style", []) or []
    writer_skill = float(writer.get("skill_level", 1.0)) if writer.get("skill_level") is not None else 1.0
    writer_education = writer.get("education", "")

    # Determine genre: prefer writer specialty if it's valid for the source; otherwise random
    possible_genres = source_data.get("associated_genres", list(getattr(game_data, "GENRES", {}).keys()))
    if specialty in possible_genres:
        genre = specialty
    else:
        genre = random.choice(possible_genres) if possible_genres else random.choice(list(getattr(game_data, "GENRES", {}).keys()))

    genre_data = getattr(game_data, "GENRES", {}).get(genre, {"common_tags": [], "budget_affinity": ["Low", "Medium", "High"]})

    # Title generation (resilient)
    title_formats = getattr(game_data, "TITLE_FORMATS_BY_GENRE", {"default": ["{prefix} {noun}", "{noun} of the {noun2}"]})
    title_parts = getattr(game_data, "SCRIPT_TITLES_BY_GENRE", {}).get(genre, {
        "prefixes": ["The"],
        "nouns": ["Story"],
        "noun2": ["Dream"],
    })
    structure = random.choice(title_formats.get(genre, title_formats.get("default", ["{prefix} {noun}"])))
    title_data = {
        "prefix": random.choice(title_parts.get("prefixes", ["The"])),
        "noun": random.choice(title_parts.get("nouns", ["Story"])),
        "noun2": random.choice(title_parts.get("noun2", ["Dream"])),
        "mid_phrase": random.choice(getattr(game_data, "MID_PHRASES", ["of the Ages"])),
        "place": random.choice(getattr(game_data, "PLACES", ["Nowhere"])),
        "adjective": random.choice(getattr(game_data, "ADJECTIVES", ["Lonely"])),
    }
    try:
        title = structure.format(**title_data).title()
    except Exception:
        title = f"{title_data['prefix']} {title_data['noun']}"

    # Tags & theme
    genre_tags = random.sample(genre_data.get("common_tags", []), k=min(2, max(1, len(genre_data.get("common_tags", [])))))
    theme_key = random.choice(list(getattr(game_data, "THEMES", {"default":{"name":"Everyman"}}).keys()))
    theme = getattr(game_data, "THEMES", {}).get(theme_key, {}).get("name", theme_key)
    tags = list(dict.fromkeys(genre_tags + writer_tags + [theme]))  # preserve order, dedupe

    # Rating
    rating = assign_rating(tags, genre)

    # Potential quality calculation (safe math)
    potential_quality = 40
    if specialty == genre:
        potential_quality += 15
    if writer_education in ["Film School", "MFA Program"]:
        potential_quality += 5
    debut_year = writer.get("debut_year", current_year)
    potential_quality += min((current_year - debut_year) * 0.5, 10)
    potential_quality = round(max(30, min(100, potential_quality * writer_skill)))

    initial_quality = max(1, round(potential_quality * random.uniform(0.6, 0.85)))
    appeal = round(random.uniform(0.3, 1.0), 2)
    budget_class = random.choice(genre_data.get("budget_affinity", ["Low", "Medium", "High"]))

    # Build script dict
    script = {
        "title": title,
        "genre": genre,
        "source": source_data.get("name", source_key),
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
        "rewrite_history": [writer.get("name", "Unknown")],
        "base_buzz": source_data.get("base_buzz", 0),
        "budget_class": budget_class,
        "length": random.choice(getattr(game_data, "POSSIBLE_LENGTHS", ["feature"])),
    }

    # Buzz calc (defensively)
    buzz = 10 + int(potential_quality / 10)
    if genre == specialty:
        buzz += 5
    if "controversial" in tags and "edgy" in writer_style:
        buzz += 4
    if "family" in tags and "heartwarming" in writer_style:
        buzz += 3
    buzz += random.randint(-3, 3)
    script["buzz"] = max(0, buzz)

    # Description
    script["description"] = generate_script_description(script)

    return script


# --- Script Rewrite ---
def rewrite_script(script, writer, calendar=None):
    """Rewrite a script with a contracted writer. Returns the modified script object."""
    if script.get("status") == "approved":
        # already finalized; return as-is
        return script

    improvement = 0
    if writer:
        if writer.get("specialty") == script.get("genre"):
            improvement += 10
        overlap = set(script.get("tags", [])) & set(writer.get("tags", []))
        improvement += len(overlap) * 4
        debut_year = writer.get("debut_year", getattr(calendar, "year", 2025))
        improvement += min((getattr(calendar, "year", debut_year) - debut_year) * 0.25, 8)

    draft_penalty = (script.get("draft_number", 1) - 1) * 2
    net = max(0, improvement - draft_penalty)
    quality_gap = script.get("potential_quality", 100) - script.get("quality", 0)
    actual_improve = min(net, quality_gap)

    script["quality"] = min(100, round(script.get("quality", 0) + actual_improve))
    script["draft_number"] = script.get("draft_number", 1) + 1
    if writer and writer.get("name") and writer.get("name") not in script.get("rewrite_history", []):
        script.setdefault("rewrite_history", []).append(writer["name"])

    # Buzz recalculation
    buzz = 10 + int(script["quality"] / 10)
    if writer and writer.get("specialty") == script.get("genre"):
        buzz += 5
    script["buzz"] = max(0, buzz)

    # Optionally print a debug line when running from command line tools
    print(f"'{script.get('title')}' rewritten by {writer.get('name','Unknown')}. Quality is now {script['quality']}.")
    return script


# --- Finalize Script ---
def finalize_script(script, studio, calendar, draft_pool=None):
    """Mark a script as approved and ready for production."""
    script["status"] = "approved"
    script["finalized_turn"] = (getattr(calendar, "year", 2025), getattr(calendar, "month", 1))

    studio.finalized_scripts = getattr(studio, "finalized_scripts", [])
    studio.finalized_scripts.append(script)

    if draft_pool and script in draft_pool:
        try:
            draft_pool.remove(script)
        except ValueError:
            pass

    print(f"\n✅ Script '{script.get('title','Untitled')}' has been finalized and is ready for production!")
    return script
