# game/genres.py

import random
import game_data


SEASONS = {
    1: "winter", 2: "winter", 3: "spring",
    4: "spring", 5: "spring", 6: "summer",
    7: "summer", 8: "summer", 9: "fall",
    10: "fall", 11: "fall", 12: "winter"
}


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
        "common_tags": ["cerebral", "futuristic", "blockbuster", "dystopian"]
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
        
    # ... etc. for all other genres
}

def season_for_month(month: int) -> str:
    return game_data.SEASONS.get(month, "summer")

def seasonal_bonus(genre: str, month: int) -> float:
    season = season_for_month(month)
    genre_info = game_data.GENRES.get(genre, {})
    if season in genre_info.get("peak_seasons", []):
        return genre_info.get("trend_bonus", 0) / 100
    return 0.0
