# game_data.py
# A comprehensive content database for HollywoodSim.
# This file acts as the central "content bible" for the game, defining everything
# from genre specifics to random events. Its data-driven design allows for easy
# expansion and balancing.

# ==============================================================================
# 1. SOURCE MATERIAL DATABASE
# Defines the rights that can be acquired to start a script.
# - base_buzz: Starting public excitement (0-100).
# - cost_multiplier: Base cost to acquire the rights.
# - prestige_multiplier: Affects the film's critical potential.
# - franchise_potential: Likelihood of spawning successful sequels (0-10).
# - associated_genres: Genres likely to come from this source.
# ==============================================================================
SOURCE_TYPES = {
    "ORIGINAL_SCREENPLAY": {
        "name": "Original Screenplay",
        "base_buzz": 5,
        "cost_multiplier": 0.5,
        "prestige_multiplier": 1.0,
        "franchise_potential": 3,
        "availability": 40,
        "associated_genres": ["Drama", "Comedy", "Thriller"]
    },
    "NOVEL": {
        "name": "Bestselling Novel",
        "base_buzz": 35,
        "cost_multiplier": 1.2,
        "prestige_multiplier": 1.2,
        "franchise_potential": 5,
        "availability": 20,
        "associated_genres": ["Drama", "Romance", "Thriller"]
    },
    "COMIC_BOOK": {
        "name": "Comic Book Series",
        "base_buzz": 50,
        "cost_multiplier": 1.8,
        "prestige_multiplier": 0.8,
        "franchise_potential": 9,
        "availability": 15,
        "associated_genres": ["Action", "Sci-Fi", "Fantasy", "Horror",]
    },
    "VIDEO_GAME": {
        "name": "Popular Video Game",
        "base_buzz": 60,
        "cost_multiplier": 2.5,
        "prestige_multiplier": 0.6,
        "franchise_potential": 8,
        "availability": 5,
        "associated_genres": ["Action", "Adventure", "Fantasy", "Horror"]
    },
    "STAGE_PLAY": {
        "name": "Award-Winning Stage Play",
        "base_buzz": 20,
        "cost_multiplier": 0.8,
        "prestige_multiplier": 1.5,
        "franchise_potential": 1,
        "availability": 10,
        "associated_genres": ["Drama", "Musical", "Comedy"]
    },
    "SHORT_STORY": {
        "name": "Cult Short Story",
        "base_buzz": 15,
        "cost_multiplier": 0.7,
        "prestige_multiplier": 1.1,
        "franchise_potential": 2,
        "availability": 10,
        "associated_genres": ["Sci-Fi", "Horror", "Thriller", "Drama"]
    }

}

SEASONS = {
    1: "winter", 2: "winter", 3: "spring",
    4: "spring", 5: "spring", 6: "summer",
    7: "summer", 8: "summer", 9: "fall",
    10: "fall", 11: "fall", 12: "winter"
}

# ==============================================================================
# 2. GENRE DATABASE
# Detailed attributes for each movie genre.
# - budget_affinity: The typical budget range this genre thrives in.
# - prestige_multiplier: Natural affinity for awards (1.0 is baseline).
# - marketing_focus: Key selling points for marketing campaigns.
# ==============================================================================
GENRES = {
    "Action": {
        "name": "Action",
        "primary_audience": "Males, 18-35",
        "production_focus": ["Stunts", "Visual Effects"],
        "budget_affinity": ["Mid", "High"],
        "prestige_multiplier": 0.7,
        "marketing_focus": ["Stars", "Spectacle"],
        "common_tags": ["fast-paced", "explosions", "gritty", "blockbuster"],
        "peak_seasons": ["spring", "summer"],
        "trend_bonus": 10
    },
    "Comedy": {
        "name": "Comedy",
        "primary_audience": "All, 18-49",
        "production_focus": ["Dialogue", "Performance"],
        "budget_affinity": ["Low", "Mid"],
        "prestige_multiplier": 0.8,
        "marketing_focus": ["Concept", "Stars"],
        "common_tags": ["quirky", "feel-good", "satirical", "character-driven"],
        "peak_seasons": ["spring", "summer", "fall", "winter"],
        "trend_bonus": 5
    },
    "Drama": {
        "name": "Drama",
        "primary_audience": "Adults, 25+",
        "production_focus": ["Character", "Emotion", "Dialogue"],
        "budget_affinity": ["Low", "Mid"],
        "prestige_multiplier": 1.5,
        "marketing_focus": ["Awards Buzz", "Story"],
        "common_tags": ["emotional", "cerebral", "award-winning", "serious"],
        "peak_seasons": ["fall", "winter"],
        "trend_bonus": 15
    },
    "Horror": {
        "name": "Horror",
        "primary_audience": "All, 17-29",
        "production_focus": ["Suspense", "Sound Design", "Atmosphere"],
        "budget_affinity": ["Low"],
        "prestige_multiplier": 0.6,
        "marketing_focus": ["Concept", "Scare Factor"],
        "common_tags": ["supernatural", "jump-scares", "gritty", "low-budget"],
        "peak_seasons": ["fall"],
        "trend_bonus": 12
    },
    "Sci-Fi": {
        "name": "Sci-Fi",
        "primary_audience": "Males, 18-49",
        "production_focus": ["Visual Effects", "World-Building", "Concept"],
        "budget_affinity": ["Mid", "High"],
        "prestige_multiplier": 1.0,
        "marketing_focus": ["Spectacle", "Concept"],
        "common_tags": ["cerebral", "futuristic", "blockbuster", "dystopian"],
        "peak_seasons": ["summer"],
        "trend_bonus": 8
    },
    "Thriller": {
        "name": "Thriller",
        "primary_audience": "Adults, 18-49",
        "production_focus": ["Suspense", "Pacing", "Plot Twists"],
        "budget_affinity": ["Low", "Mid"],
        "prestige_multiplier": 1.2, # Thrillers often get critical acclaim
        "marketing_focus": ["Mystery", "Stars"],
        "common_tags": ["suspenseful", "psychological", "plot-twists", "gritty"],
        "peak_seasons": ["fall", "winter"],
        "trend_bonus": 10
    },
    "Family": {
        "name": "Family",
        "primary_audience": "All, especially children",
        "production_focus": ["Heartwarming", "Adventure", "Fun"],
        "budget_affinity": ["Low", "Mid"],  
        "prestige_multiplier": 0.9,
        "marketing_focus": ["Family-Friendly", "Adventure"],
        "common_tags": ["adventure", "heartwarming", "fun", "family-friendly"],
        "peak_seasons": ["summer"],
        "trend_bonus": 7
    },
    "Documentary": {
        "name": "Documentary",
        "primary_audience": "Adults, 25+",
        "production_focus": ["Real-Life", "Educational", "Social Issues"],
        "budget_affinity": ["Low", "Mid"],
        "prestige_multiplier": 1.3,
        "marketing_focus": ["Real-Life", "Educational"],
        "common_tags": ["informative", "real-life", "social issues", "educational"],
        "peak_seasons": ["spring", "fall"],
        "trend_bonus": 3
    },
    "Romance": {
        "name": "Romance",  # Added Romance genre
        "primary_audience": "Females, 18-49",
        "production_focus": ["Character", "Emotion", "Dialogue"],
        "budget_affinity": ["Low", "Mid"],
        "prestige_multiplier": 1.2,
        "marketing_focus": ["Stars", "Love Story"],
        "common_tags": ["heartwarming", "emotional", "romantic", "feel-good"],
        "peak_seasons": ["winter"],
        "trend_bonus": 20
    },
    "Fantasy": {   
        "name": "Fantasy",
        "primary_audience": "All, especially children",
        "production_focus": ["World-Building", "Magic", "Adventure"],
        "budget_affinity": ["Mid", "High"],
        "prestige_multiplier": 1.1,
        "marketing_focus": ["Magic", "Adventure"],
        "common_tags": ["magical", "adventurous", "imaginative", "family-friendly"],
        "peak_seasons": ["summer"],
        "trend_bonus": 6
    },
    "Mystery": {
        "name": "Mystery",
        "primary_audience": "Adults, 18-49",
        "production_focus": ["Plot Twists", "Suspense", "Character"],
        "budget_affinity": ["Low", "Mid"],
        "prestige_multiplier": 1.0,
        "marketing_focus": ["Intrigue", "Stars"],
        "common_tags": ["enigmatic", "suspenseful", "plot-twists", "gritty"],
        "peak_seasons": ["fall", "winter"],
        "trend_bonus": 8
    },
    "Adventure": {
        "name": "Adventure",
        "primary_audience": "All, especially children",
        "production_focus": ["Exploration", "Action", "Fun"],
        "budget_affinity": ["Mid", "High"],
        "prestige_multiplier": 0.9,
        "marketing_focus": ["Exploration", "Adventure"],
        "common_tags": ["explorative", "action-packed", "fun", "family-friendly"],
        "peak_seasons": ["summer"],
        "trend_bonus": 5
    },
    "Musical": {
        "name": "Musical",
        "primary_audience": "All, especially families",
        "production_focus": ["Music", "Dance", "Performance"],
        "budget_affinity": ["Mid", "High"],
        "prestige_multiplier": 1.4,
        "marketing_focus": ["Music", "Stars"],
        "common_tags": ["musical", "dance", "performance", "family-friendly"],
        "peak_seasons": ["winter"],
        "trend_bonus": 4
    }, 
    "Documentary": {
        "name": "Documentary",
        "primary_audience": "Adults, 25+",
        "production_focus": ["Real-Life", "Educational", "Social Issues"],
        "budget_affinity": ["Low", "Mid"],
        "prestige_multiplier": 1.3,
        "marketing_focus": ["Real-Life", "Educational"],
        "common_tags": ["informative", "real-life", "social issues", "educational"],
        "peak_seasons": ["spring", "fall"],
        "trend_bonus": 3
    },
    "Animation": {
        "name": "Animation",
        "primary_audience": "Children, Families",
        "production_focus": ["Visuals", "Storytelling", "Voice Acting"],
        "budget_affinity": ["Mid", "High"],
        "prestige_multiplier": 1.2,
        "marketing_focus": ["Family-Friendly", "Visuals"],
        "common_tags": ["colorful", "imaginative", "family-friendly", "fun"],
        "peak_seasons": ["summer", "winter"],
        "trend_bonus": 5
    },
    "Western": {
        "name": "Western",
        "primary_audience": "Adults, 30+",
        "production_focus": ["Action", "Character", "Setting"],
        "budget_affinity": ["Low", "Mid"],
        "prestige_multiplier": 0.8,
        "marketing_focus": ["Nostalgia", "Action"],
        "common_tags": ["nostalgic", "action-packed", "gritty", "character-driven"],
        "peak_seasons": ["fall", "winter"],
        "trend_bonus": 2
    },
        
    # ... etc. for all other genres
}

# ==============================================================================
# 3. THEME DATABASE (NEW)
# Defines narrative themes that can be added to scripts.
# - synergy_genres: Genres this theme works particularly well with.
# - prestige_modifier: Bonus/penalty to critical reception.
# - audience_modifier: Bonus/penalty to general audience appeal.
# ==============================================================================
THEMES = {
    "Revenge": {
        "name": "Revenge",
        "synergy_genres": ["Action", "Thriller", "Drama"],
        "prestige_modifier": 0.1,
        "audience_modifier": 0.2
    },
    "Coming of Age": {
        "name": "Coming of Age",
        "synergy_genres": ["Drama", "Comedy"],
        "prestige_modifier": 0.3,
        "audience_modifier": 0.1
    },
    "Political Intrigue": {
        "name": "Political Intrigue",
        "synergy_genres": ["Thriller", "Drama", "Sci-Fi"],
        "prestige_modifier": 0.4,
        "audience_modifier": -0.2
    },
    "Forbidden Love": {
        "name": "Forbidden Love",
        "synergy_genres": ["Romance", "Drama", "Fantasy", "Adventure", "Musical"],
        "prestige_modifier": 0.2,
        "audience_modifier": 0.3
    },
    "Survival": {
        "name": "Survival",
        "synergy_genres": ["Action", "Adventure", "Horror"],
        "prestige_modifier": 0.1,
        "audience_modifier": 0.2
    },
}


# ==============================================================================
# 4. STUDIO UPGRADES DATABASE (NEW)
# Permanent improvements the player can purchase for their studio.
# ==============================================================================
STUDIO_UPGRADES = {
    "casting_office": {
        "name": "Expanded Casting Office",
        "cost": 15.0, # in millions
        "monthly_upkeep": 0.5,
        "prestige_req": 10,
        "effect_description": "Reveals one hidden tag on all talent in the hiring pool."
    },
    "marketing_dept": {
        "name": "In-House Marketing Department",
        "cost": 25.0,
        "monthly_upkeep": 1.0,
        "prestige_req": 20,
        "effect_description": "Unlocks advanced marketing campaigns and provides +5% base buzz to all releases."
    },
    "post_prod_house": {
        "name": "Post-Production House",
        "cost": 50.0,
        "monthly_upkeep": 2.0,
        "prestige_req": 50,
        "effect_description": "Gives a chance to 'save' a troubled film in post-production, adding up to 5 quality points."
    }
}


# ==============================================================================
# 5. MARKETING CAMPAIGNS DATABASE (NEW)
# Specific marketing actions unlocked via upgrades.
# ==============================================================================
MARKETING_CAMPAIGNS = {
    "social_media_blitz": {
        "name": "Social Media Blitz",
        "min_cost": 2.0,
        "max_cost": 10.0,
        "unlocks_with": "marketing_dept",
        "effect_description": "High variance campaign that can create massive buzz or fall flat. Most effective for Comedy, Horror, and Sci-Fi."
    },
    "film_festival_circuit": {
        "name": "Film Festival Circuit",
        "min_cost": 5.0,
        "max_cost": 15.0,
        "unlocks_with": "marketing_dept",
        "effect_description": "Generates 'Awards Buzz', boosting prestige multiplier and critic scores. Most effective for Drama."
    }
}


# ==============================================================================
# 6. RANDOM EVENTS DATABASE (NEW)
# A structured way to define random events, their triggers, and outcomes.
# ==============================================================================
EVENTS = {
    "scandal_hit": {
        "name": "Scandal Hits Star!",
        "type": "NEGATIVE",
        "trigger": "has_actor_with_fame > 80_and_personality == 'volatile'",
        "description": "Your lead actor for '{movie_title}', {actor_name}, has been involved in a public scandal! The press is having a field day. What do you do?",
        "choices": [
            {"text": "Fire the actor and reshoot.", "cost": "reshoot_cost", "effect": "replace_actor_on_project"},
            {"text": "Hire a PR firm to manage it.", "cost": 5.0, "effect": "mitigate_scandal_chance"},
            {"text": "Release a statement of support.", "cost": 0.0, "effect": "loyalty_up_fame_down"}
        ]
    },
    "surprise_hit": {
        "name": "Surprise Indie Darling",
        "type": "POSITIVE",
        "trigger": "released_film_with_budget == 'Low'_and_quality > 85",
        "description": "Critics are raving about '{movie_title}'! It's become a surprise hit on the festival circuit, generating immense buzz.",
        "effect": "add_buzz_and_prestige"
    }
}


# ==============================================================================
# 7. TALENT ATTRIBUTES (EXPANDED)
# ==============================================================================
# --- For Actors ---
ACTOR_ATTRIBUTES = {
    "tags": [ # Visible tags
        "Serious", "Comedic", "Action Hero", "Rom-Com Star", "Character Actor",
        "Award-Winning", "Box-Office Draw", "Indie Darling"
    ],
    "hidden_traits": [ # Traits revealed through work or the Casting Office
        "Reliable", "Professional", "Volatile", "Difficult", "Method Actor",
        "Perfectionist", "Gives 110%", "Lazy"
    ]
}
# ... similar expansions for Writer and Director attributes ...


# ==============================================================================
# 8. SCRIPT TITLES (EXPANDED)
# Categorized by genre for more thematic procedural naming.
# ==============================================================================
#TITLE_PARTS = {
SCRIPT_TITLES_BY_GENRE = {
    "Action": {
        "prefixes": ["Code", "Operation", "Last", "Agent", "Dead", "Red", "Final", "Zero", "Iron", "Black"],
        "nouns": ["Strike", "Target", "Storm", "Zone", "Protocol", "Force", "Run", "Edge", "Mission", "Kill"],
    },
    "Comedy": {
        "prefixes": ["My", "Accidental", "Bad", "Worst", "Funny", "Couch", "Misfit", "Roommate", "Disaster", "Awkward"],
        "nouns": ["Vacation", "Breakup", "Plan", "Date", "Mistake", "Dinner", "Fiasco", "Room", "Dance", "Neighbor"]
    },
    "Drama": {
        "prefixes": ["The", "Broken", "Silent", "Glass", "Paper", "Winter", "Lost", "Letters from", "Weight of", "Beyond"],
        "nouns": ["Truth", "House", "Season", "Dream", "River", "Promise", "Hope", "Whispers", "Sunset", "Burden"]
    },
    "Horror": {
        "prefixes": ["Don't", "Whispers", "The", "It", "Last", "House of", "Shadows of", "Voices from", "The 13th", "Midnight"],
        "nouns": ["Cellar", "Harvest", "Ritual", "Room", "Mirror", "Eyes", "Crying", "Mask", "Forest", "Tapes"]
    },
    "Sci-Fi": {
        "prefixes": ["Quantum", "Neon", "Project", "Chrono", "Hyper", "Star", "Void", "Gravity", "Future", "Second"],
        "nouns": ["Protocol", "Exodus", "Echo", "Divide", "Loop", "Drift", "System", "Planet", "Signal", "Orbit"]
    },
    "Romance": {
        "prefixes": ["First", "Falling", "Love in", "The Summer of", "Letters to", "Hearts at", "Kiss Me", "If", "Where", "Always"],
        "nouns": ["Love", "Us", "Paris", "Midnight", "You", "Goodbye", "Stars", "Dawn", "Luna", "Roses"]
    },
    "Thriller": {
        "prefixes": ["The", "Silent", "Hidden", "Final", "Last", "Dark", "Edge of", "Behind", "In the", "Deadly"],
        "nouns": ["Game", "Witness", "Secret", "Truth", "Line", "Mask", "Enemy", "Code", "Face", "Trap"]
    },
    "Family": {
        "prefixes": ["Adventure", "Magic", "Journey", "Quest", "Secret", "Lost", "Wonder", "Dreams of", "Tales of", "Heart"],
        "nouns": ["Friendship", "Family", "Fun", "Summer", "Magic", "World", "Adventure", "Home", "Dreams", "Joy"]
    },
    "Documentary": {
        "prefixes": ["Inside", "Beyond", "The", "Voices of", "Stories from", "Life in", "Truth about", "Nature's", "Hidden", "Real"],
        "nouns": ["World", "People", "Nature", "History", "Culture", "Life", "Journey", "Struggles", "Beauty", "Voices"]
    },
    "Fantasy": {
        "prefixes": ["Realm of", "Tales from", "Magic of", "Chronicles of", "Legends of", "Kingdom of", "Wonders of", "Secrets of", "Journey to", "Quest for"],
        "nouns": ["Magic", "Dragons", "Elves", "Kingdoms", "Heroes", "Wizards", "Myths", "Fables", "Adventures", "Legends"]
    },
    "Mystery": {
        "prefixes": ["The", "Case of", "Secrets of", "Mysteries of", "Whispers in", "Clues from", "Hidden", "Unsolved", "Darkness of", "Echoes of"],
        "nouns": ["Mystery", "Clue", "Secret", "Whisper", "Shadow", "Enigma", "Puzzle", "Riddle", "Code", "Truth"]
    },
    "Adventure": {
        "prefixes": ["Journey to", "Quest for", "Tales of", "Legends of", "Secrets of", "Chronicles of", "Saga of", "Voyage to", "Expedition to", "Odyssey of"],
        "nouns": ["Adventure", "Treasure", "Island", "World", "Heroes", "Explorers", "Legends", "Myths", "Fables", "Saga"]
    },
    "Musical": {
        "prefixes": ["The", "Songs of", "Melodies from", "Rhythms of", "Dances of", "Voices of", "Harmony in", "Symphony of", "Chorus of", "Ballads from"],
        "nouns": ["Music", "Dreams", "Love", "Stars", "Heart", "Life", "Joy", "Harmony", "Melody", "Rhythm"]
    },
    "Animation": {
        "prefixes": ["The", "Magic of", "Tales from", "Adventures in", "Dreams of", "World of", "Journey to", "Legends of", "Stories from", "Wonders of"],
        "nouns": ["Animation", "Adventure", "Dreams", "Magic", "Heroes", "Fantasy", "Fun", "Joy", "Imagination", "Wonder"]
    },
    "Western": {
        "prefixes": ["The", "Tales of", "Legends of", "Journey to", "Quest for", "Saga of", "Outlaws of", "Heroes of", "Frontier of", "Dusty Trails of"],
        "nouns": ["West", "Frontier", "Outlaws", "Heroes", "Gold Rush", "Cattle Drive", "Showdown", "Saloon", "Ranchers", "Pioneers"]
    },   

}

TITLE_STRUCTURES = [
    "{prefix} {noun}",
    "{noun} of the {noun2}",
    "{prefix} {noun} {mid_phrase} {noun2}",
    "The {noun} {mid_phrase} {place}",
    "{adjective} {noun}"
]

MID_PHRASES = ["of the", "in the", "from", "beyond", "within"]
PLACES = ["Forest", "City", "Stars", "Night", "Hollow", "Past", "Future"]
ADJECTIVES = ["Dark", "Silent", "Lonely", "Burning", "Golden", "Wicked"]


# ==============================================================================
# 9. NAMES FOR TALENT GENERATION
# ==============================================================================
FIRST_NAMES = [
    "Taylor", "Morgan", "Jamie", "Alex", "Jordan", "Casey", "Riley", "Quinn", "Drew", "Sam", "Kai", "Rowan",
    "Cameron", "Skyler", "Shannon", "Robin", "Tracy", "Terry", "Dana", "Leslie", "Jessie", "Kerry", "Devin", "Blake",
    "Shawn", "Jody", "Chris", "Corey", "Pat", "Lee", "Avery", "Kris", "Reese", "Lane", "Marion", "Toby", "Perry",
    "Stevie", "Noel", "Frankie", "Kendall", "Hunter", "Elliot", "Brett", "Dallas", "Jamie", "Sage", "Alexis", "Rene"
]
LAST_NAMES = [
    "Stone", "Ray", "Knight", "Monroe", "Lee", "Wells", "Avery", "Banks", "Clarke", "Foster", "Shaw", "Chen",
    "Harper", "Grant", "Flynn", "Parker", "Reed", "West", "Greene", "Hayes", "Ford", "Drake", "Logan", "Morgan",
    "Kennedy", "Chase", "Hale", "Page", "Brooks", "Dane", "Quinn", "Rhodes", "Day", "Ross", "Lane", "Vaughn",
    "Cross", "Blair", "Fox", "Sloan", "Dean", "Beck", "Carson", "Tyler", "Cole", "Adler", "Lowell", "Shields", "Dalton"
]
# ==============================================================================]