# talent.py
import random

class Actor:
    def __init__(self, name, current_year):
        self.name = name
        self.age = random.randint(20, 35)
        self.gender = random.choice(["Male", "Female", "Non-binary"])
        self.fame = random.randint(10, 60)
        self.salary = round(self.fame * 0.1, 1)
        self.tags = random.sample(["action", "comedic", "dramatic", "heartthrob", "quirky", "respected"], 2)
        self.debut_year = current_year
        self.film_history = []
        self.career_arc = "Rising Star"
        self.fan_base = random.randint(1, 5)
        self.award_nominations = 0
        self.award_wins = 0
        self.personality = random.choice(["easygoing", "demanding", "charming", "mysterious"])

    def add_film(self, title, year, quality, box_office):
        self.film_history.append({
            "title": title,
            "year": year,
            "quality": quality,
            "box_office": box_office
        })

class Writer:
    def __init__(self, name, current_year):
        self.name = name
        self.age = random.randint(30, 50)
        self.genre_specialties = random.sample(["Drama", "Romance", "Sci-Fi", "Comedy", "Thriller"], 2)
        self.quality_floor = random.randint(40, 60)
        self.quality_ceiling = random.randint(80, 100)
        self.debut_year = current_year - random.randint(0, 10)
        self.tags = random.sample(["award-winning", "indie", "studio-favourite", "fast turnaround"], 2)
        self.filmography = []
        self.prestige_level = random.randint(1, 5)
        self.award_nominations = 0
        self.award_wins = 0

    def add_script(self, title, year, appeal):
        self.filmography.append({
            "title": title,
            "year": year,
            "appeal": appeal
        })

class Director:
    def __init__(self, name, current_year):
        self.name = name
        self.age = random.randint(35, 60)
        self.style_tags = random.sample(["visual", "blockbuster", "methodical", "actor-friendly"], 2)
        self.genre_focus = random.sample(["Action", "Sci-Fi", "Drama", "Horror", "Comedy"], 2)
        self.hit_ratio = round(random.uniform(0.3, 0.9), 2)
        self.debut_year = current_year - random.randint(5, 20)
        self.filmography = []
        self.reputation = random.choice(["Reliable", "Risky", "Respected", "Inconsistent"])
        self.ego = random.choice(["Low", "Medium", "High"])
        self.award_nominations = 0
        self.award_wins = 0

    def add_film(self, title, year, quality):
        self.filmography.append({
            "title": title,
            "year": year,
            "quality": quality
        })
