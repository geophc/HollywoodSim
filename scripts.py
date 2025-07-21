import random
from writers import generate_writer

GENRES = ["Action", "Drama", "Comedy", "Sci-Fi", "Romance", "Horror", "Thriller"]

BUDGET_CLASSES = ["Low", "Mid", "Blockbuster"]

TAG_POOL = [
    "ensemble", "period", "musical", "biopic", "reboot", "sequel", "based on true story",
    "action-heavy", "rom-com", "sci-fi epic", "animated", "experimental", "holiday", "thriller-driven"
]

def generate_script(current_year=2025, writer=None):
    title_prefixes = ["The Last", "The Secret", "The Final", "Return of", "Rise of", "Fall of"]
    title_nouns = ["Dream", "Hunt", "Affair", "Code", "City", "Revenge", "Heart"]
    title = f"{random.choice(title_prefixes)} {random.choice(title_nouns)}"

    genre = random.choice(GENRES)
    budget = random.choice(BUDGET_CLASSES)
    tags = random.sample(TAG_POOL, 2)

    if writer is None:
        writer = generate_writer(current_year)

    # Base appeal randomized between 3 and 7
    appeal = random.randint(3, 7)

    # 🎯 Bonus: Genre synergy
    if genre == writer.get("genre_specialty"):
        appeal += 2
    if genre in writer.get("interests", []):
        appeal += 1
    if genre in writer.get("life_experience", []):
        appeal += 1

    # 🎓 Schooling bonuses
    schooling = writer.get("schooling")
    if schooling == "Film School":
        appeal += 1
    elif schooling == "Technical College" and genre in ["Sci-Fi", "Thriller"]:
        appeal += 1
    elif schooling == "Literature Degree" and genre in ["Drama", "Romance"]:
        appeal += 1

    # 📊 Cap appeal at 10
    appeal = min(10, appeal)

    script = {
        "title": title,
        "genre": genre,
        "budget_class": budget,
        "appeal": appeal,
        "tags": tags,
        "writer": writer
    }

    return script
