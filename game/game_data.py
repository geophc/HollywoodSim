# game_data.py
# Central database for game content, inspired by Hollywood Mogul.
# This file consolidates data for genres, source material, names, and tags
# to make the game easier to balance and expand.

# ==============================================================================
# SCRIPT SOURCE MATERIAL DATABASE
# ==============================================================================
# Defines the different types of source material a script can be based on.
# - 'name': The display name of the source type.
# - 'base_buzz': A starting value for public excitement (0-100).
# - 'cost_multiplier': Affects the purchase price. 1.0 is standard.
# - 'availability': How often this source type appears. Higher is more common.
# - 'associated_genres': Genres that are more likely to come from this source.
# ==============================================================================
SOURCE_TYPES = {
    "ORIGINAL_SCREENPLAY": {
        "name": "Original Screenplay",
        "base_buzz": 10,
        "cost_multiplier": 0.5, # Cheaper because it's just the writer's fee
        "availability": 40,
        "associated_genres": ["Drama", "Comedy", "Thriller"]
    },
    "NOVEL": {
        "name": "Novel",
        "base_buzz": 30,
        "cost_multiplier": 1.0,
        "availability": 25,
        "associated_genres": ["Drama", "Romance", "Thriller", "Historical"]
    },
    "COMIC_BOOK": {
        "name": "Comic Book",
        "base_buzz": 50,
        "cost_multiplier": 1.5,
        "availability": 15,
        "associated_genres": ["Action", "Sci-Fi", "Fantasy", "Superhero"]
    },
    "SCI_FI_NOVEL": {
        "name": "Science Fiction Novel",
        "base_buzz": 45,
        "cost_multiplier": 1.2,
        "availability": 15,
        "associated_genres": ["Sci-Fi", "Adventure", "Thriller"]
    },
    "STAGE_PLAY": {
        "name": "Stage Play",
        "base_buzz": 20,
        "cost_multiplier": 0.8,
        "availability": 10,
        "associated_genres": ["Drama", "Comedy", "Musical"]
    },
    "GRAPHIC_NOVEL": {
        "name": "Graphic Novel",
        "base_buzz": 40,
        "cost_multiplier": 1.3,
        "availability": 10,
        "associated_genres": ["Drama", "Noir", "Fantasy", "Sci-Fi"]
    },
    "VIDEO_GAME": {
        "name": "Video Game",
        "base_buzz": 60,
        "cost_multiplier": 2.0,
        "availability": 5,
        "associated_genres": ["Action", "Adventure", "Fantasy", "Sci-Fi"]
    }
}


# ==============================================================================
# GENRE DATABASE
# ==============================================================================
# Provides detailed attributes for each movie genre.
# - 'name': The display name.
# - 'primary_audience': The core demographic.
# - 'production_focus': Key elements that are important for this genre's success.
# - 'common_tags': Descriptive tags often associated with the genre.
# ==============================================================================
GENRES = {
    "Action": {
        "name": "Action",
        "primary_audience": "Males, 18-35",
        "production_focus": ["Visual Effects", "Stunts"],
        "common_tags": ["fast-paced", "explosions", "gritty", "blockbuster"]
    },
    "Comedy": {
        "name": "Comedy",
        "primary_audience": "All, 18-49",
        "production_focus": ["Dialogue", "Performance"],
        "common_tags": ["quirky", "feel-good", "satirical", "character-driven"]
    },
    "Drama": {
        "name": "Drama",
        "primary_audience": "Females, 25+",
        "production_focus": ["Character Development", "Emotion"],
        "common_tags": ["emotional", "cerebral", "award-winning", "serious"]
    },
    "Horror": {
        "name": "Horror",
        "primary_audience": "All, 17-29",
        "production_focus": ["Suspense", "Sound Design"],
        "common_tags": ["supernatural", "jump-scares", "gritty", "low-budget"]
    },
    "Romance": {
        "name": "Romance",
        "primary_audience": "Females, 18-35",
        "production_focus": ["Chemistry", "Emotion"],
        "common_tags": ["feel-good", "emotional", "charming", "heartfelt"]
    },
    "Sci-Fi": {
        "name": "Sci-Fi",
        "primary_audience": "Males, 18-49",
        "production_focus": ["Visual Effects", "World-Building"],
        "common_tags": ["cerebral", "futuristic", "blockbuster", "adventure"]
    },
    "Thriller": {
        "name": "Thriller",
        "primary_audience": "All, 25+",
        "production_focus": ["Plot Twists", "Tension"],
        "common_tags": ["gritty", "cerebral", "fast-paced", "noir"]
    },
    "Fantasy": {
        "name": "Fantasy",
        "primary_audience": "All, 12-29",
        "production_focus": ["World-Building", "Visual Effects"],
        "common_tags": ["adventure", "epic", "magical", "blockbuster"]
    },
    "Musical": {
        "name": "Musical",
        "primary_audience": "Females, All",
        "production_focus": ["Music", "Choreography"],
        "common_tags": ["feel-good", "charming", "award-winning", "family-friendly"]
    }
    # You can easily add more genres here, like "War", "Western", "Mystery", etc.
}


# ==============================================================================
# TALENT ATTRIBUTE POOLS
# ==============================================================================
# These pools provide a variety of descriptive attributes for generating
# unique actors, writers, and directors.
# ==============================================================================

# --- For Writers ---
WRITER_ATTRIBUTES = {
    "educations": ["Film School", "Journalism", "Playwriting", "Self-Taught", "MFA Program", "Ivy League"],
    "experiences": [
        ["Sitcoms", "Sketch Comedy"],
        ["Short Films", "Indie Features"],
        ["Stage Plays", "Poetry"],
        ["TV Dramas", "Serialized Fiction"],
        ["Documentaries", "News Writing"]
    ],
    "interests": [
        "Technology", "Family Drama", "Surrealism", "Crime", "Historical Events",
        "Adventure", "Philosophy", "Politics", "Teen Angst", "Urban Life"
    ],
    "signature_tags": ["quirky", "emotional", "cerebral", "gritty", "fast-paced", "high-concept", "experimental", "witty-dialogue"]
}

# --- For Actors ---
ACTOR_ATTRIBUTES = {
    "tags": [
        "serious", "comedic", "dramatic", "musical", "sci-fi regular", "rom-com star",
        "method actor", "action hero", "diva", "low-budget favourite", "award-winning",
        "up-and-comer", "character actor", "heartthrob", "reliable", "box-office draw"
    ],
    "personalities": ["easygoing", "demanding", "charming", "mysterious", "professional", "volatile"]
}

# --- For Directors ---
DIRECTOR_ATTRIBUTES = {
    "style_tags": ["visual", "blockbuster", "methodical", "actor-friendly", "efficient", "visionary", "indie-darling", "auteur"],
    "reputations": ["Reliable", "Risky", "Respected", "Inconsistent", "Visionary", "On-Budget", "Perfectionist"]
}


# ==============================================================================
# MISCELLANEOUS GAME DATA
# ==============================================================================
# A place for other data like names, titles, etc.
# ==============================================================================

# --- Potential Script Titles ---
# You could even categorize these by genre for more thematic naming.
SCRIPT_TITLES = [
    "The Bitter End", "Quantum Hearts", "Midnight at the Arcade", "The Secret Dream",
    "Echoes of Tomorrow", "Painted Lies", "Beyond the Hollow", "Love in Low Orbit",
    "City of Glass", "The Last Signal", "Velvet Cage", "Sundown Protocol"
]

# --- Names for Talent Generation ---
FIRST_NAMES = ["Taylor", "Morgan", "Jamie", "Alex", "Jordan", "Casey", "Riley", "Quinn", "Drew", "Sam"]
LAST_NAMES = ["Stone", "Ray", "Knight", "Monroe", "Lee", "Wells", "Avery", "Banks", "Clarke", "Foster"]
