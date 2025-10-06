# HollywoodSim/game/genres.py

import random
import game_data

GENRES = game_data.GENRES
SEASONS = game_data.SEASONS

def season_for_month(month: int) -> str:
    return game_data.SEASONS.get(month, "summer")

def seasonal_bonus(genre: str, month: int) -> float:
    season = season_for_month(month)
    genre_info = game_data.GENRES.get(genre, {})
    if season in genre_info.get("peak_seasons", []):
        return genre_info.get("trend_bonus", 0) / 100
    return 0.0
