# game/writers.py

import random

def generate_writer(current_year=2025):
    names = [
        "Jordan Quinn", "Alex Riley", "Casey Wells", "Sam Avery", "Taylor Banks",
        "Morgan Stone", "Riley James", "Quinn Harper", "Avery Blake", "Charlie West"
    ]

    educations = ["Film School", "Journalism", "Playwriting", "Self-Taught", "MFA Program"]
    experiences = [
        ["Sitcoms", "Sketch Comedy"],
        ["Short Films", "YouTube"],
        ["Stage Plays", "Poetry"],
        ["TV Dramas", "Serialized Fiction"],
        ["Documentaries", "Political Writing"]
    ]
    interests_pool = [
        "Romance", "Technology", "Family Drama", "Surrealism", "Crime", "Historical", "Adventure", "Philosophy"
    ]
    signature_tags_pool = ["quirky", "emotional", "cerebral", "gritty", "fast-paced", "low-budget", "experimental"]

    name = random.choice(names)
    specialty = random.choice(["Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Action", "Thriller"])
    education = random.choice(educations)
    experience = random.choice(experiences)
    interests = random.sample(interests_pool, 2)
    signature_tags = random.sample(signature_tags_pool, 2)
    fame = random.randint(10, 70)
    age = random.randint(28, 55)
    debut_year = current_year - random.randint(0, age - 22)

    return {
        "name": name,
        "age": age,
        "debut_year": debut_year,
        "education": education,
        "experience": experience,
        "interests": interests,
        "signature_tags": signature_tags,
        "specialty": specialty,
        "tags": [specialty] + signature_tags,
        "notable_script": None,
        "fame": fame,
        "salary": round(0.3 + fame * 0.02, 2),  # Example formula
        "film_history": [],
        "awards": [],
        "reputation": "Rising Star" if fame < 40 else "Established",
        "prestige": 0
    }


# Example usage:
# writer = 
   # "name": "Jordan Kim",
   # "age": 34,
   # "debut_year": 2022,
   # "education": "Film School",          # or "Journalism", "Playwriting", "Self-Taught"
   # "experience": ["Sitcoms", "Short Films"],
   # "interests": ["Romance", "Technology", "Family Drama"],
   # "signature_tags": ["quirky", "emotional", "low-budget"],
   # "notable_script": "The Bitter End",  # Optional
   # "fame": 12,  # Determines salary, hype
   # "salary": 1.2,
   # "film_history": [],  # [ {title, quality, box_office, year} ]
   # "awards": []  # [ {name, year, category} ]
   # "reputation": "Rising Star"  # or "Established", "Veteran", "Cult Favorite"
   # "prestige": 0  # New attribute for future phase     
  