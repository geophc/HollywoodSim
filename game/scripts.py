import random

GENRES = ["Action", "Drama", "Comedy", "Sci-Fi", "Romance"]

def generate_script():
    title_adjectives = ["Last", "Great", "Secret", "Final", "Golden"]
    title_nouns = ["Revenge", "Dream", "City", "Affair", "Hunt"]

    title = f"The {random.choice(title_adjectives)} {random.choice(title_nouns)}"
    genre = random.choice(GENRES)

    return {
        "title": title,
        "genre": genre,
        "budget_class": random.choice(["Low", "Mid", "Blockbuster"]),
        "appeal": random.randint(1, 10)
    }
