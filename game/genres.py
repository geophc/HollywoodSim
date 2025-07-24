# game/genres.py

import random

SEASONS = {
    1: "winter", 2: "winter", 3: "spring",
    4: "spring", 5: "spring", 6: "summer",
    7: "summer", 8: "summer", 9: "fall",
    10: "fall", 11: "fall", 12: "winter"
}

GENRES = {
    "Action": {
        "themes": ["heroic", "explosive", "revenge", "military"],
        "peak_seasons": ["spring", "summer"],
        "trend_bonus": 10
    },
    "Drama": {
        "themes": ["family", "trauma", "justice", "relationships"],
        "peak_seasons": ["fall", "winter"],
        "trend_bonus": 15
    },
    "Romance": {
        "themes": ["love", "heartbreak", "weddings", "self-discovery"],
        "peak_seasons": ["winter"],
        "trend_bonus": 20
    },
    "Sci-Fi": {
        "themes": ["space", "future", "technology", "alien"],
        "peak_seasons": ["summer", "fall"],
        "trend_bonus": 8
    },
    "Comedy": {
        "themes": ["buddy", "satire", "awkward", "coming-of-age"],
        "peak_seasons": ["spring", "summer", "fall", "winter"],
        "trend_bonus": 5
    },
    "Horror": {
        "themes": ["supernatural", "slasher", "paranoia", "haunted"],
        "peak_seasons": ["fall"],
        "trend_bonus": 12
    }
}

def season_for_month(month: int) -> str:
    return SEASONS.get(month, "summer")

def seasonal_bonus(genre: str, month: int) -> float:
    season = season_for_month(month)
    info = GENRES.get(genre, {})
    bonus = info.get("trend_bonus", 0) if season in info.get("peak_seasons", []) else 0
    return bonus / 100  # convert percent into multiplier (e.g. 0.10 = +10%)
