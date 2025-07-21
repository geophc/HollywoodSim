import random
from writers import generate_writer

GENRES = ["Action", "Drama", "Comedy", "Sci-Fi", "Romance", "Horror", "Thriller"]
BUDGET_CLASSES = ["Low", "Mid", "Blockbuster"]
TAG_POOL = [
    "ensemble", "period", "musical", "biopic", "reboot", "sequel", "based on true story",
    "action-heavy", "rom-com", "sci-fi epic", "animated", "experimental", "holiday", "thriller-driven"
]

def generate_script(current_year=2025):
    title_prefixes = ["The Last", "The Secret", "The Final", "Return of", "Rise of", "Fall of"]
    title_nouns = ["Dream", "Hunt", "Affair", "Code", "City", "Revenge", "Heart"]
    title = f"{random.choice(title_prefixes)} {random.choice(title_nouns)}"
    
    genre = random.choice(GENRES)
    budget = random.choice(BUDGET_CLASSES)
    tags = random.sample(TAG_POOL, 2)
    writer = generate_writer(current_year)

    script = {
        "title": title,
        "genre": genre,
        "budget_class": budget,
        "appeal": random.randint(3, 10),
        "tags": tags,
        "writer": writer  # ✅ Writer is attached here properly
    }

    return script
