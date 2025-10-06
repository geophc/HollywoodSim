# HollywoodSim/game/talent_tasks.py

"""
Talent Task System
------------------
This module manages tasks that can be assigned to talent (actors, writers,
directors, staff). Tasks consume time and give benefits or risks.
They integrate with the monthly turn loop and contracts system.
"""

import random

# === TASK DEFINITIONS ===
# These can later be expanded or pulled from game_data.py
TASKS = {
        "actors": [
            {
            "name": "Stunt Training",
            "duration": 1,
            "effect": {"fame": +1, "quality_boost": 0.2},
            "risk": {"injury": 0.1},
            "desc": "Intense stunt practice adds realism to performances, but risks injury."
        },
        {
            "name": "Charity Appearance",
            "duration": 1,
            "effect": {"prestige": +2, "fame": +1},
            "risk": {"scandal": 0.02},
            "desc": "Public goodwill visit. Builds prestige with a minor chance of bad optics."
        },
        {
            "name": "Vacation",
            "duration": 1,
            "effect": {"stress_relief": True},
            "risk": {},
            "desc": "Time off to reset. Clears stress and reduces burnout chance."
        },
    ],
    "writers": [
            {
            "name": "Genre Experiment",
            "duration": 2,
            "effect": {"script_quality": +1, "theme_unlock": True},
            "risk": {"failure": 0.1},
            "desc": "Attempts a bold genre shift. Can inspire or flop."
        },
        {
            "name": "Ghostwriting",
            "duration": 1,
            "effect": {"cash": +3},
            "risk": {"burnout": 0.1},
            "desc": "Quick turnaround script for hire. Extra studio income but drains stamina."
        },
        {
            "name": "Writers’ Room Collaboration",
            "duration": 2,
            "effect": {"synergy": +1, "script_quality": +1},
            "risk": {},
            "desc": "Team workshop improves cohesion and future scripts."
        },
    ],
    "directors": [
            {
            "name": "Vision Workshop",
            "duration": 1,
            "effect": {"prestige": +1, "experience": +1},
            "risk": {},
            "desc": "Refines directing style. Boosts credibility and skill."
        },
        {
            "name": "Commercial Gig",
            "duration": 1,
            "effect": {"cash": +4},
            "risk": {"prestige_loss": 0.05},
            "desc": "Directs an ad campaign. Brings money but can cheapen image."
        },
        {
            "name": "Experimental Short",
            "duration": 2,
            "effect": {"buzz": +4, "script_concept": True},
            "risk": {"failure": 0.1},
            "desc": "A creative short film that might inspire a future full project."
        },
    ],
    "staff": [
            {
            "name": "Tech Upgrade",
            "duration": 2,
            "effect": {"synergy": +1, "experience": +1},
            "risk": {"failure": 0.05, "cash": -2},
            "desc": "Staff implement new tools. Improves future projects but can go over budget."
        },
        {
            "name": "Overtime Sprint",
            "duration": 1,
            "effect": {"buzz": +2},
            "risk": {"burnout": 0.1},
            "desc": "Puts in extra hours to push a project. Raises short-term hype, risks fatigue."
        },
        {
            "name": "Industry Workshop",
            "duration": 1,
            "effect": {"experience": +2, "prestige": +1},
            "risk": {},
            "desc": "Attends seminars and panels. Builds skill and reputation."
        },
    ],
}


# === TASK ASSIGNMENT & RESOLUTION ===

def assign_task(contract, task_name):
    """
    Assigns a task to a contracted person.
    Stores active task on the contract itself.
    """
    role = contract["type"]
    person = contract["person"]

    available = [t for t in TASKS.get(role, []) if t["name"] == task_name]
    if not available:
        raise ValueError(f"No such task '{task_name}' for role {role}")

    task = available[0].copy()
    contract["task"] = {
        "name": task["name"],
        "remaining": task["duration"],
        "effect": task["effect"],
        "risk": task.get("risk", {}),
        "desc": task["desc"],
    }

    print(f"📝 Assigned {person['name']} ({role[:-1]}) to task: {task['name']}")


def progress_tasks(contracts_by_type, studio):
    """
    Progresses all active tasks by one month.
    Applies effects when tasks are completed.
    """
    completed = []

    for role, contracts in contracts_by_type.items():
        for contract in contracts:
            task = contract.get("task")
            if not task:
                continue

            task["remaining"] -= 1
            if task["remaining"] <= 0:
                result = resolve_task(contract, task, studio)
                completed.append(result)
                contract.pop("task")  # clear task after completion

    return completed


def resolve_task(contract, task, studio):
    """
    Resolves the outcome of a finished task, applying effects to
    the person, the studio, or future scripts/movies.
    """
    person = contract["person"]
    effects = []

    # Apply guaranteed effects
    for key, value in task["effect"].items():
        if key == "fame":
            person["fame"] = person.get("fame", 0) + value
            effects.append(f"{person['name']} gained {value} Fame")

        elif key == "cash":
            studio.balance += value
            effects.append(f"Studio earned ${value}M from endorsements")

        elif key == "prestige":
            studio.prestige += value
            effects.append(f"Studio Prestige +{value}")

        elif key == "buzz":
            studio.newsfeed.append(f"{person['name']} generated {value} buzz with {task['name']}")
            effects.append(f"Buzz +{value}")

        elif key == "quality_boost":
            # Store a temporary boost on the contract (applies to next production)
            contract["quality_boost"] = contract.get("quality_boost", 0) + value
            effects.append(f"{person['name']} gained a +{value:.1f} Quality Boost for future roles")

        elif key == "script_quality":
            # Writers improve next script they work on
            contract["script_bonus"] = contract.get("script_bonus", 0) + value
            effects.append(f"{person['name']} will improve next script by +{value} Quality")

        elif key == "theme_unlock":
            studio.unlocked_themes = getattr(studio, "unlocked_themes", set())
            studio.unlocked_themes.add("new_theme")  # placeholder; could be randomized
            effects.append(f"{person['name']} unlocked a new theme for scripts")

        elif key == "script_concept":
            # Director creates a pitch for a new script
            studio.concept_pool = getattr(studio, "concept_pool", [])
            studio.concept_pool.append({"origin": person["name"], "concept": "Director Pitch"})
            effects.append(f"{person['name']} developed a new script concept")

        elif key == "experience":
            person["experience"] = person.get("experience", 0) + value
            effects.append(f"{person['name']} gained {value} Experience")

        elif key == "synergy":
            studio.synergy = getattr(studio, "synergy", 0) + value
            effects.append(f"Studio Team Synergy increased by {value}")

        else:
            effects.append(f"(Unhandled effect: {key} {value})")

    # Check risks
    for risk_type, chance in task.get("risk", {}).items():
        if random.random() < chance:
            effects.append(f"⚠️ Risk triggered: {person['name']} suffered {risk_type}")

    return {
        "person": person,
        "task": task["name"],
        "outcome": effects,
    }
