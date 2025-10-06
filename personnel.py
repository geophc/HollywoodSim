# HollywoodSim/game/personnel.py

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
        "film_history": []  # Each entry: {title, year, month, role, genre, quality, box_office}
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
        "tags": random.sample(TAGS, k=2)
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
        "education": random.choice(["Film School", "Apprenticeship", "Self-Taught", "Conservatory"]),
        "film_history": []  # keep staff trackable like others
    }


# === CASTING LOGIC (moved from casting.py) ===
class CastingPool:
    def __init__(self):
        self.actors = []
        self.writers = []
        self.directors = []
        self.staff = []

    def add_actor(self, actor): self.actors.append(actor)
    def add_writer(self, writer): self.writers.append(writer)
    def add_director(self, director): self.directors.append(director)
    def add_staff(self, staff_member): self.staff.append(staff_member)

    def get_actor_choices(self, count=3): return random.sample(self.actors, k=min(count, len(self.actors)))
    def get_writer_choices(self, count=3): return random.sample(self.writers, k=min(count, len(self.writers)))
    def get_director_choices(self, count=3): return random.sample(self.directors, k=min(count, len(self.directors)))
    def get_staff_choices(self, count=3): return random.sample(self.staff, k=min(count, len(self.staff)))

    def age_all_talent(self):
        for actor in self.actors: actor["age"] += 1
        for writer in self.writers: writer["age"] += 1
        for director in self.directors: director["age"] += 1
        for staff_member in self.staff: staff_member["experience"] += 1

    def clear(self):
        """Remove all talent from this casting pool (quick reset)."""
        self.actors.clear()
        self.writers.clear()
        self.directors.clear()
        self.staff.clear()


class CastingManager:
    def __init__(self):
        self.collaborations = {}

    def record_collaboration(self, actor, movie):
        """Record collaborations between actor–writer and actor–director pairs."""
        actor_key = actor["name"]
        self.collaborations.setdefault(actor_key, []).append({
            "title": movie["title"],
            "quality": movie["quality"],
            "box_office": movie["box_office"]
        })

        # Actor–Writer pair
        if movie.get("writer"):
            writer = movie["writer"]
            pair_key = (actor["name"], writer["name"])
            self.collaborations.setdefault(pair_key, []).append({
                "title": movie["title"],
                "quality": movie["quality"],
                "box_office": movie["box_office"]
            })

        # Actor–Director pair
        if movie.get("director"):
            director = movie["director"]
            pair_key = (actor["name"], director["name"])
            self.collaborations.setdefault(pair_key, []).append({
                "title": movie["title"],
                "quality": movie["quality"],
                "box_office": movie["box_office"]
            })

    def get_history(self, actor_name):
        records = self.collaborations.get(actor_name, [])
        if not records:
            return None
        avg_quality = sum(r["quality"] for r in records) / len(records)
        avg_box_office = sum(r["box_office"] for r in records) / len(records)
        return {
            "count": len(records),
            "avg_quality": round(avg_quality, 1),
            "avg_box_office": round(avg_box_office, 1)
        }

    def get_collaboration_count(self, actor, writer):
        key = (actor["name"], writer["name"])
        return len(self.collaborations.get(key, []))

    def get_average_quality(self, actor, writer):
        key = (actor["name"], writer["name"])
        history = self.collaborations.get(key, [])
        if not history:
            return None
        return round(sum(f["quality"] for f in history) / len(history), 2)

    def get_average_box_office(self, actor, writer):
        key = (actor["name"], writer["name"])
        history = self.collaborations.get(key, [])
        if not history:
            return None
        return round(sum(f["box_office"] for f in history) / len(history), 2)

    def describe_pairing(self, actor, writer):
        count = self.get_collaboration_count(actor, writer)
        if count == 0:
            return "🆕 First-time pairing."
        avg_quality = self.get_average_quality(actor, writer)
        avg_box = self.get_average_box_office(actor, writer)
        return (
            f"🎞️  {actor['name']} and {writer['name']} have collaborated {count}x. "
            f"Avg Quality: {avg_quality}, Avg Box Office: ${avg_box}M"
        )


# === TALENT POOL (Unified) ===
class TalentPool:
    """Unified talent pool that manages actors, writers, directors, and staff."""

    def __init__(self):
        self.actors = []
        self.writers = []
        self.directors = []
        self.staff = []

    # === Generation Methods ===
    def generate_starting_actors(self, count, current_year=2025):
        for _ in range(count): self.actors.append(generate_actor(current_year))

    def generate_starting_writers(self, count, current_year=2025):
        for _ in range(count): self.writers.append(generate_writer(current_year))

    def generate_starting_directors(self, count, current_year=2025):
        for _ in range(count): self.directors.append(generate_director(current_year))

    def generate_starting_staff(self, count, current_year=2025):
        roles = list(STAFF_SPECIALTIES.keys())
        for _ in range(count):
            role = random.choice(roles)
            self.staff.append(generate_staff_member(role, current_year))

    # === Accessors ===
    def get_all_talent(self):
        return {"actors": self.actors, "writers": self.writers,
                "directors": self.directors, "staff": self.staff}

    def get_random_talent(self, role, count=3):
        if role == "actor": return random.sample(self.actors, k=min(count, len(self.actors)))
        elif role == "writer": return random.sample(self.writers, k=min(count, len(self.writers)))
        elif role == "director": return random.sample(self.directors, k=min(count, len(self.directors)))
        elif role == "staff": return random.sample(self.staff, k=min(count, len(self.staff)))
        else: raise ValueError(f"Unknown role type: {role}")

    # === Aging Logic ===
    def age_all(self):
        for actor in self.actors: actor["age"] += 1
        for writer in self.writers: writer["age"] += 1
        for director in self.directors: director["age"] += 1
        for staff_member in self.staff: staff_member["experience"] += 1

    def clear(self):
        """Reset all talent lists in the unified TalentPool."""
        self.actors.clear()
        self.writers.clear()
        self.directors.clear()
        self.staff.clear()
