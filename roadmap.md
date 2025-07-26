# 📍 DEVELOPMENT ROADMAP – HollywoodSim (Updated July 2025)

A structured, modular plan for building out the minimalist, text-driven Hollywood studio simulator. Each phase builds logically on the last, and you can pause at any point to iterate, refine, or polish.

---

## ✅ PHASE 1: Core Loop Prototype  
**Status:** Completed

**Focus:** Get the game running end-to-end, even with placeholder data.

**Features Built:**
- Basic game loop (`main.py`)
- Script generator (`scripts.py`)
- Actor generator (`actors.py`)
- Movie production logic (`studio.py`)
- Printed output to terminal

---

## ✅ PHASE 2: Calendar & Scheduling  
**Status:** Completed

**Focus:** Introduce time progression and event timing.

**Features Built:**
- `GameCalendar` month/year tracking
- Movie release date assignment
- Release automation
- Box office simulation (based on quality and fame)

---

## ✅ PHASE 3: Financial System  
**Status:** Completed

**Focus:** Introduce budget management and financial consequences.

**Features Built:**
- Studio cash balance
- Actor salaries + script budget class affect cost
- Revenue on release
- Soft bankruptcy (production blocked if broke)

**Planned Enhancements:**
- Monthly operating expenses (rent, staff)
- Hard bankruptcy (optional game over)

---

## ⚠️ PHASE 4: Studio Class Expansion  
**Status:** Completed

**Focus:** Consolidate state and add structural clarity.

**Planned Systems:**
- A centralized `Studio` object that stores:
  - Balance
  - Scheduled/released films
  - Prestige/reputation (future)
- Central logic hub for expansion

---

## ⏳ PHASE 5: Strategic Depth  
**Status:** Completed

**Focus:** Give players choices and influence over strategy.

**Planned Systems:**
- Offer player 2–3 script or actor choices each month
- Budget class and genre shown before production
- Add script tags ("Sequel", "Oscar Bait", "Controversial")
- Genre popularity and seasonal trends that rise and fall
- Basic trend forecast each quarter to help plan ahead
- Multiple production slots: player can manage more than one film at once
- Allow the player to choose release dates (e.g., summer, awards season)
- Allow player to delay or cancel productions (with penalties)
---

## ✨ PHASE 6: Narrative & Events  
**Status:** In Progress

**Focus:** Add drama, flavour, and unpredictability.

**Planned Systems:**
- Random events (scandals, lawsuits, delays, awards)
- Awards season + prestige points
- Actor conflicts, critical reception, rival studios (abstracted)
- Modifiers for reputation, press, genre timing
- Recurring characters: actors can develop careers over time
- Critics: reviews can boost or tank earnings

---

## ✨ PHASE 7: Studio Progression & Reputation
**Status:** Future Phase

**Focus:** Introduce long-term studio growth and prestige.

**Planned Systems:**
- Reputation meter based on quality, success, critical reception
- Unlock better scripts, actors, and marketing tools at higher rep
- Studio upgrades (e.g., genre specialization, budget boosts)
- Investor events and offers (risk/reward trade-offs)
- Annual reports and rankings

## 🗄️ BONUS PHASE: Interface & Polish
**Optional: For usability or future expansion**

**Options:**
- Terminal visual improvements via `rich` or `textual`
- Desktop GUI (e.g., `tkinter`, `PySimpleGUI`)
- Web interface via Flask or Remi
- Export save/load data in JSON or SQLite

---

## 🔧 DEVELOPMENT VALUES
- Strategic depth > visual fidelity
- Replayability through systems
- Text-driven clarity
- Flexible, incremental builds

---

**Next Step:** Finalize Studio class, and begin adding choice-driven logic (script selection, costs, and scheduling).

