import random

def generate_actor(current_year):
    first_names = ["Taylor", "Morgan", "Jamie", "Alex", "Jordan"]
    last_names = ["Stone", "Ray", "Knight", "Monroe", "Lee"]

    TAG_POOL = [
        "serious", "comedic", "dramatic", "musical", "sci-fi regular", "rom-com star",
        "method actor", "action hero", "diva", "low-budget favourite", "award-winning", "up-and-comer"
    ]

    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    fame = round(random.gauss(60, 15))
    fame = min(99, max(20, fame))
    salary = round(fame * 0.1, 1)
    tags = random.sample(TAG_POOL, k=random.choice([1, 2]))

    return {
        "name": name,
        "fame": fame,
        "salary": salary,
        "tags": tags,
        "age": random.randint(20, 35),        # New
        "debut_year": current_year,           # New
        "film_history": []                    # New
    }
