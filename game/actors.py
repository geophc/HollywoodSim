import random

FIRST_NAMES = ["Alex", "Jamie", "Taylor", "Jordan", "Morgan"]
LAST_NAMES = ["Stone", "Chase", "Knight", "Ray", "Monroe"]

def generate_actor():
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    fame = random.randint(20, 100)
    salary = round(fame * 0.1, 2)

    return {
        "name": name,
        "fame": fame,
        "salary": salary
    }
