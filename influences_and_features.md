# HollywoodSim – Influences & Feature Ideas

## 🎬 Major Influences

- **Hollywood Mogul**

  - Text-driven studio simulation
  - Budget class, genre planning, and release windows

- **The Movies (Lionhead)**

  - Staff and studio management, talent development
  - Strategic release of films over time

- **Liberal Crime Squad (Bay 12 Games)**

  - Minimal UI, procedural characters, emergent systems

- **Total Extreme Wrestling (Grey Dog Software)**

  - Deep simulation with minimal graphics
  - Procedural talent, event scheduling, reputation tracking

- **Game Dev Tycoon / Software Inc.**

  - Turn-based project loops
  - Strategic growth from humble beginnings

- **Bullfrog / MicroProse sims**

  - System interactions > visual fidelity
  - Emphasis on player storytelling via gameplay

  https://docs.google.com/spreadsheets/d/e/2PACX-1vTJgRjVUVjmw09rCRYm5hIOkHpR-nWNFg5hMmc9KuDQnKIOTUoVJRAl3PLNGpwtTLuOwybXj-WU02Oj/pubhtml#

---

## 💡 Core Design Philosophy

- Minimal graphics, maximum replayability
- Text-driven clarity
- Let systems evolve naturally
- No player action should feel wasted

---

## ✅ Implemented Features (as of now)

- Monthly time progression (calendar)
- Script and actor procedural generation
- Studio budget system
- Movie scheduling and release
- Box office calculation
- Prestige gain from high-quality releases
- Monthly operating expenses
- Script choice each turn

---

## 🧭 Next Feature Ideas (Phase 5+)

### 🎭 Actor Selection

- Offer 2–3 actors each month
- Fame, salary, and future potential visible

### 🎯 Genre Popularity System

- Rotating seasonal trends (e.g., Sci-Fi is hot)
- Player sees quarterly forecast
- Bonus/penalty to box office by alignment

### 🗓️ Release Window Strategy

- Let player delay release (e.g. summer, awards season)
- Tradeoff: holding costs or risks

### 🏆 Awards & Events

- Annual award show with prestige rewards
- Random monthly events (PR disasters, viral success, etc.)

### 📊 Studio Reputation & Milestones

- Prestige unlocks better scripts/actors
- Rankings: "Rising Studio", "Industry Titan"

### 🧮 Reports & Stats

- Year-end summaries
- High score boards
- CSV export or in-game logs

### 🎨 Optional GUI / Interface

- Rich CLI formatting
- Textual or Tkinter interface for desktop
- Web viewer for output

---

## 📁 Long-Term Expansion Ideas

- Rival studios / market share simulation
- Writers and Directors teams - that progress with their own levels of presitige and skill
- Generative script description like that of Dwarf Fortress
- Backgroud profiles for actors, that include the school, reputations for behaviours and if they have a pet project, or things that they are good at or not 
- Marketing campaigns and budgets
- Genre specialization paths
- Studio upgrades (production slots, departments)
- Critical review system
- Save/load system and game persistence
- Refine the script creation system, buying scripts and may have aspects like act or director attached, Creating you own script,



## Phase 7 Idea Outline
HollywoodSim: Long-Term Talent System (Phase 7 Draft)

🎯 Objective
- Introduce career arcs, aging, and historical memory for actors (and eventually directors/writers). This adds depth to casting decisions and creates long-term strategy.

🧓 Aging System
- Each actor has an internal "age" stat (not visible yet) that progresses monthly.
- Actors age each month (or year if preferred)
- Over time, their fame peaks and declines
- Optional: introduce "types" (heartthrob, character actor, action lead) that age differently

Fame Curve Example (simplified):
    Age     Fame Modifier
    18-25   +5
    26-35   peak
    36-45   -5
    46-60   -10
    61+     -20

Fame still varies with project success but is influenced by age curve.

📈 Career Arcs
Track basic career trajectory:
- Debut Year (first appearance)
- Most recent movie
- Number of hits/flops (based on critic scores or box office)
- Prestige or "Respected Actor" flag for high average review score

Possible Arcs:
- Rising Star 🌟
- Blockbuster Regular 🎬
- Cult Icon 🧛
- Washed Up ❌
- Comeback Story 🔁
Could be flavor-only or affect casting availability / cost.

🧠 Studio Memory
Track actor's past work with your studio:
- Total films together
- Average quality/revenue
- Actor "trust" or preference toward your studio (optional future flag)

✅ Immediate Implementation Goals
- Add age, debut_year, film_history to actor objects
- Increment age each year in game loop
- Record film_history with titles, review, earnings

📅 Future Options
- Actor retires or dies after certain age
- Age-relevant casting penalties/bonuses ("too old for action blockbusters")
- Mentorship paths (old actors become directors?)
- Award history / legacy rankings
- Television - Internet - Mini-Series



🎬 Major Eras of Hollywood
1. The Golden Age (1920s–1950s)
Studios like MGM, Warner Bros., Paramount dominated.

Actors were under exclusive studio contracts.

Genres: Musicals, Westerns, War Films, Film Noir.

Star system: actors were "owned" by studios.

Marketing was heavily controlled by the studios.

2. New Hollywood (1967–1980)
Rise of the director as auteur (Scorsese, Coppola, Spielberg).

Edgier, character-driven dramas. Big shift from musicals to realism.

Ratings system (MPAA) introduced.

Independent films began to matter.

3. Blockbuster Era (1980s–2000s)
Star-driven action and sci-fi dominated.

Summer tentpole releases became essential (Jaws, Star Wars).

Marketing budgets exploded.

Franchises and merchandise started to influence film development.

4. Franchise and IP Dominance (2010s–present)
Marvel, DC, Disney live-action remakes, shared universes.

Decline in mid-budget films.

Streaming services disrupted the theatrical model.

Studios now heavily data-driven and globally focused.

💰 Real Film Economics
Film Tier	Budget Range	Example Films
Microbudget	<$1M	Paranormal Activity, Clerks
Indie	$1M–$10M	Lady Bird, Moonlight
Mid-Budget	$10M–$40M	Knives Out, Whiplash
Blockbuster	$100M+	Avengers, Avatar
Marketing Spend	50–100% of budget	e.g., $200M movie = $100M ads

Fun Fact: Marketing often costs more than production for major releases.

🌟 Actor Careers (Based on Real Patterns)
Fame rises fast with 1–2 breakout roles.

Career peaks often last ~5–10 years at the top.

Afterward, actors shift to:

Indie films

TV/miniseries

Director/producer roles

Comeback arcs (The Whale, John Travolta, Ke Huy Quan)

🏆 Awards & Reviews Impact
Critical acclaim can revive careers (e.g. Brendan Fraser)

Awards season (Oscars, Golden Globes) shapes:

Casting availability

Salary negotiations

Studio prestige

🎯 Gameplay Hooks from History
You could use these historical insights to:

Add Studio Era Mode: players run a 1950s-style studio

Model Actor Contracts: lock stars for X years, or risk losing them

Implement Streaming vs Theatrical

Introduce Oscar Bait Mechanics: prestige-heavy projects with low commercial return

Create Aging out arcs where actors become directors or leave the business

Cimrnatophyers and Editors,

Better contractor negoitiations for 




Game Play: Genre, Script Development, Audience Rating, Themes & Seasonal Elements
Bringing the heart of Hollywood to life means giving players meaningful choices around what stories they tell, when they release them, and how they polish them. Below is a blueprint for how these systems can interlock—drawing inspiration from Hollywood Animals, The Executive, Hollywood Mogul 3, and The Movies—while fitting neatly into your existing roadmap.

1. Genre Popularity & Trend Cycles
- Each month/quarter, every genre has a popularity index (0–100) that fluctuates.
- Initial values seeded randomly, then drift based on player releases and global events.
- Quarterly “Trend Forecast” gives players a 3‐month outlook:
- Action: +10% in Q2–Q3 (summer blockbuster)
- Drama/Romance: +15% in Q4–Q1 (award season & holidays)
- Sci-Fi/Comedy: moderate spikes around festivals or global events
| Genre | Peak Season | Quarterly Trend Bonus | 
| Action | Apr–Sep | +10% | 
| Drama | Oct–Mar | +15% | 
| Romance | Dec–Feb | +20% | 
| Sci-Fi | Jun–Aug, Nov | +8% | 
| Comedy | Year-round | +5% | 


- Impact: Boosts script’s base appeal and film’s quality when release date falls in the genre’s sweet spot.

2. Script Development & Thematic Depth
- Script Attributes
- genre (from GENRES)
- budget_class: Low/Mid/Blockbuster
- initial_appeal (1–10)
- themes: list (e.g., “Revenge”, “Family”, “Sci-Fi Mystery”)
- complexity: scale 1–5 (higher = longer development & higher cost)
- Development Choice
- After choosing a script pitch, player can invest extra funds (e.g., +1M per development point) to:
- Raise appeal by +1–3
- Add or swap one theme
- Increase complexity, unlocking richer narrative—and press score potential later
- Thematic Synergy
- If a script’s theme matches a seasonal event (Valentine’s Day for “Romance”, Halloween for “Horror” tag), it gains a one-time bump to appeal or box office.

3. Release Scheduling & Seasonal Windows
- Players choose release month for each scheduled film.
- Each slot shows:
- Forecasted genre popularity
- Competing releases (AI studio output)
- Award‐season meter (Q4–Q1 prestige boost)
- Trade-off:
- Summer high earnings but high competition
- Award season prestige at the cost of marketing spend
Release scheduling UI (example):
| Film Title | Genre | Quality | Best Slot | Comp. Films | 
| The Final Hunt | Action | 78 | Jul (+12%) | 3 | 
| Last Secrets | Drama | 85 | Dec (Awards) | 1 | 



4. Audience Rating & Box Office Mechanics
- Audience Score (0–100) computed on release:
- Base: film quality
- Genre Popularity Bonus
- Theme/Event Bonus
- Actor/Director Fame bonus
- – Competition penalty (number of same‐genre releases that month)
- Box Office Formula
earnings = (
  audience_score * 0.5
  + fame_modifier
  + random.randint(0, 20)
) * budget_multiplier
- Critic vs. Audience Ratings
- Add a critic_score based on quality + script complexity.
- Negative critic score can dent next month’s script appeal or actor fame.

5. Monthly Flow & Player Choices
Each month, the player sees:
- Trend Dashboard: genre popularity charts & event calendar
- Script Pitches: 2–3 scripts (with genre, theme, appeal, complexity, cost)
- Staff Offers: 1–2 actor/director pools with fame, salary, specialty
- Development Decision: pay to boost script or lock in scheduling
- Release Management: view/edit upcoming films’ release months
- Month’s End:
- Pay operating expenses
- Release films and calculate earnings + ratings
- Apply press/critic modifiers to next month

6. Future Expansions
- Festivals & Awards Shows as mid‐year events (Cannes, Comic-Con)
- Audience Segments: family, teens, block-busters, art-house
- Marketing Campaigns: spend budget to boost genre or theme affinity
- Global Markets: regional trends (Asia, Europe, North America)

This integrated approach ensures every script choice, theme decision, and release date becomes a strategic puzzle—reflecting the dynamic, seasonal dance of Hollywood’s real‐world box office. Let me know which piece you’d like to prototype first


🧠 Script Creation System: Core Concepts
1. Genre Blending
Let players mix genres for hybrid appeal:
- Primary genre: defines core tone (e.g. Drama)
- Secondary genre: adds flavor (e.g. Sci-Fi)
- Genre synergy affects appeal, complexity, and marketability
script["genres"] = ["Drama", "Sci-Fi"]


2. Style & Tone
Introduce stylistic sliders:
- Tone: Lighthearted ↔ Dark
- Pacing: Slow Burn ↔ Fast-Paced
- Structure: Linear ↔ Nonlinear
These influence:
- Critic score
- Actor/director compatibility
- Audience segment targeting
3. Theme Tags
Let players choose 1–3 themes:
- Examples: “Revenge”, “Coming of Age”, “Political Intrigue”, “Forbidden Love”
- Seasonal synergy (e.g. “Romance” in February) boosts appeal
- Actor/director tag matching adds quality bonuses
4. Complexity & Development Time
Scripts have a complexity rating (1–5):
- Higher complexity = longer dev time, higher cost
- Unlocks prestige potential and critic score
- Can be reduced by hiring top-tier writers

🛠️ Gameplay Flow
- Script Builder UI
- Choose genre(s), tone, themes, complexity
- See projected appeal, cost, and development time
- Optional: hire a writer to boost stats
- Development Phase
- Spend budget to refine script (e.g. +1M for +2 appeal)
- Add rewrites, test screenings, or genre pivots
- Risk: delays, budget overruns, writer burnout
- Final Script Output
{
  "title": "The Final Dream",
  "genres": ["Drama", "Sci-Fi"],
  "themes": ["Revenge", "Legacy"],
  "tone": "Dark",
  "complexity": 4,
  "appeal": 8,
  "writer": {...}
}



🔮 Future Enhancements
- Script Archetypes: “Oscar Bait”, “Franchise Starter”, “Cult Classic”
- Writer Specialties: genre mastery, theme affinity, fame curve
- Script Aging: shelved scripts lose relevance over time
- Script Auctions: bid against rival studios for hot IPs

Want to start prototyping the genre blending and theme tag system first? I can help you refactor generate_script() into a full builder module with player input and dynamic scoring. Let’s turn scriptwriting into a strategic art form. 🖋️📽️💡



