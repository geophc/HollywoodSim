
import random
import game_data

from game_data import FIRST_NAMES, LAST_NAMES
GENRES = game_data.GENRES

# === ACTORS ===
def generate_actor(current_year):
    TAG_POOL = [
        "serious", "comedic", "dramatic", "musical", "sci-fi regular", "rom-com star",
        "method actor", "action hero", "diva", "low-budget favourite", "award-winning", "up-and-comer"
    ]
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    fame = round(random.gauss(60, 15))
    fame = min(99, max(20, fame))
    salary = round(fame * 0.1, 1)
    tags = random.sample(TAG_POOL, k=random.choice([1, 2]))

    return {
        "name": name,
        "fame": fame,
        "salary": salary,
        "tags": tags,
        "age": random.randint(20, 35),
        "debut_year": current_year,
        "film_history": []
    }

# === WRITERS ===
def generate_writer(current_year=2025):
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
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
    specialty = GENRES[random.choice(list(GENRES.keys()))]
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
        "tags": [specialty["name"]] + signature_tags,
        "notable_script": None,
        "fame": fame,
        "salary": round(0.3 + fame * 0.02, 2),
        "film_history": [],
        "awards": [],
        "reputation": "Rising Star" if fame < 40 else "Established",
        "prestige": 0
    }

# === DIRECTORS ===
def generate_director(current_year=2025):
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    TAGS = ["visual", "blockbuster", "methodical", "actor-friendly", "gritty", "stylized", "experimental"]
    fame = random.randint(20, 75)
    return {
        "name": name,
        "age": random.randint(30, 60),
        "fame": fame,
        "salary": round(0.5 + fame * 0.03, 2),
        "debut_year": current_year - random.randint(0, 10),
        "education": random.choice(["Film School", "MFA", "Self-Taught"]),
        "film_history": [],
        "genre_focus": random.choice(list(GENRES.keys())),
        "style_tags": random.sample(TAGS, k=2)
    }

# === STAFF ===
STAFF_SPECIALTIES = {
    "Editor": ["tight pacing", "montage", "non-linear", "character-focused"],
    "Cinematographer": ["stylized", "naturalistic", "moody", "grand scale"],
    "Production Designer": ["futuristic", "historical", "minimalist", "opulent"],
    "Sound Designer": ["immersive", "realistic", "experimental", "atmospheric"],
    "Composer": ["orchestral", "electronic", "jazz", "world music"],
    "Visual Effects Artist": ["CGI", "practical effects", "motion capture", "animation"],
    "Costume Designer": ["period accurate", "futuristic", "fantasy", "everyday"],
    "Producer": ["budget management", "scheduling", "resource allocation", "team leadership"],
    "Script Supervisor": ["continuity", "script analysis", "on-set coordination", "revision tracking"],
    "Location Manager": ["urban", "rural", "exotic", "studio-based"],
    "Marketing Manager": ["social media", "traditional", "viral campaigns", "event planning"]
}

STAFF_TAGS = {
    "Editor": ["post-production", "cutting room", "final polish"],
    "Cinematographer": ["lighting", "camera", "visual style"],
    "Production Designer": ["set design", "props", "world-building"],
    "Sound Designer": ["audio", "sound effects", "mixing"],
    "Composer": ["music", "score", "soundtrack"],
    "Visual Effects Artist": ["CGI", "animation", "special effects"],
    "Costume Designer": ["wardrobe", "fashion", "character design"],
    "Producer": ["budget", "scheduling", "team management"],
    "Script Supervisor": ["continuity", "script management", "on-set"],
    "Location Manager": ["scouting", "permits", "logistics"],
    "Marketing Manager": ["promotion", "advertising", "public relations"]
}

def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def generate_staff_member(role, year):
    if role not in STAFF_SPECIALTIES:
        raise ValueError(f"Unsupported staff role: {role}")

    return {
        "name": random_name(),
        "role": role,
        "experience": random.randint(1, 30),
        "specialty": random.choice(STAFF_SPECIALTIES[role]),
        "fame": random.randint(10, 90),
        "tags": STAFF_TAGS.get(role, []),
        "year_joined": year,
        "education": random.choice(["Film School", "Apprenticeship", "Self-Taught", "Conservatory"])
    }
