import random
from writers import generate_writer

GENRES = ["Action", "Drama", "Comedy", "Sci-Fi", "Romance"]

def generate_script():
    title_prefixes = ["The Last", "The Secret", "The Final", "Return of", "Rise of", "Fall of"]
    title_nouns = ["Dream", "Hunt", "Affair", "Code", "City", "Revenge", "Heart"]
    genres = ["Action", "Comedy", "Drama", "Romance", "Sci-Fi", "Horror", "Thriller"]
    budgets = ["Low", "Mid", "Blockbuster"]
    TAG_POOL = [
        "ensemble", "period", "musical", "biopic", "reboot", "sequel", "based on true story",
        "action-heavy", "rom-com", "sci-fi epic", "animated", "experimental", "holiday", "thriller-driven"
    ]
    
    writer = generate_writer()

    return {
        "title": f"{random.choice(title_prefixes)} {random.choice(title_nouns)}",
        "genre": random.choice(genres),
        "budget_class": random.choice(budgets),
        "appeal": min(10, max(1, round(random.gauss(5.5, 2)))),
        "tags": random.sample(TAG_POOL, k=random.choice([1, 2])),
        "writer": writer
    }