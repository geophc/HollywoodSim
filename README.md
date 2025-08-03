# 🎬 HollywoodSim

A minimalist, turn-based Hollywood studio simulator built in Python.  
Inspired by classics like *The Movies*, *Hollywood Mogul*, and *Total Extreme Wrestling*, it emphasizes strategic decision-making, script curation, casting, and market timing — all via a clean, text-based interface.

---

## 🚀 Core Features (Phase 1 Complete)

These systems form the foundation of gameplay:

- ✅ Monthly time progression with seasonal genre trends
- ✅ Procedural generation of scripts, actors, and directors
- ✅ Script quality influenced by writer attributes and rewrite cycles
- ✅ Movie production flow: cast, shoot, finalize, release
- ✅ Revenue simulation influenced by actor fame, genre alignment, and film quality
- ✅ Operating expenses, budget constraints, and studio cash tracking
- ✅ Prestige-based gating for high-quality scripts and talent

---

## 🧠 Simulation Highlights

Additional mechanics shaping outcomes:

- 🎭 **Prestige System** – Boost access to elite scripts and collaborators by releasing highly rated films
- ✍️ **Rewrite Passes** – Improve scripts through costly rewrites with diminishing returns
- 📉 **Monthly Expenses** – Studio costs scale with active projects and reputation
- 📊 **Detailed Logs** – Month-by-month breakdown of finances, decisions, and results
- 🏁 **End-of-Year Report** – Shows studio performance based on cash, reputation, and critical success
- 📰 **Newsfeed & Reviews** – Simulated press coverage and critic reactions for released films

---

## 🧪 In Development (Phase 2+ Roadmap)

These features are being designed or prototyped:

- 🎥 Casting Memory – Actors, writers, and directors remember past collaborations
- 🏆 Award Season – Year-end award nominations and wins affect fame and prestige
- 🔁 Rewrites by New Writers – Let unproduced scripts be salvaged by different writers
- 📚 Script Shelf – Store unproduced scripts for later use or sale
- 🤝 Agent Loyalty – Actors and directors may favour familiar collaborators
- 🎯 Marketing System – Optional budgets to boost opening weekend potential
- 🌐 Critical Network – Reviewers may show preferences or biases based on themes, studios, or past work

---

## 📂 Project Structure

game/
├── actors.py # Actor creation, fame, and film history
├── calendar.py # Monthly tracking and seasonal genre bonuses
├── casting.py # Cast selection and synergy logic
├── directors.py # Procedural director profiles
├── events.py # Random events (under development)
├── game_data.py # Genre definitions, tag pools, and system constants
├── main.py # Entry point and game loop
├── scripts.py # Script generation, rewriting, and ratings
├── studio.py # Core studio simulation: production, finances, and output
├── writers.py # Writer profiles, career data, and skill modeling

---

## 🛠️ How to Run

Make sure you have Python 3.10+ installed. Then from the project root:

```bash
python game/main.py
