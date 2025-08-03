# 🎬 Hollywood History Reference for Game Design

This document provides a summarized reference for different eras, trends, and mechanics in Hollywood's real history that can be adapted into gameplay features for *HollywoodSim*.

---

## ✨ Major Eras of Hollywood

### 1. **Golden Age (1920s–1950s)**
- Dominated by "The Big Five" studios (MGM, Warner Bros., Paramount, Fox, RKO)
- **Studio System**: Actors signed exclusive contracts
- Genres: Musicals, Westerns, Noir, Historical Epics
- Controlled marketing, strict moral codes (Hays Code)

**Game Ideas:**
- Studio ownership of actors
- Genre quotas (e.g., must produce 1 musical/year)
- Morality system: scandals hurt prestige

---

### 2. **New Hollywood (1967–1980)**
- Collapse of studio control
- Directors became stars (Spielberg, Scorsese, Coppola)
- Rise of personal storytelling, political themes
- Ratings system (G, PG, R) introduced

**Game Ideas:**
- Director system with creative vision
- Risky scripts can gain critical prestige
- Ratings affect box office earnings

---

### 3. **Blockbuster Era (1980s–2000s)**
- High-budget spectacle films dominate
- Franchises & sequels become king
- Stars drive box office more than directors
- Action, Sci-Fi, and Fantasy peak

**Game Ideas:**
- Blockbuster tier with big risk/reward
- Star power has huge influence on revenue
- Franchise-building system

---

### 4. **IP & Streaming Era (2010s–Present)**
- Dominance of superhero & remake content
- Mid-budget movies vanish
- Streaming platforms change distribution
- Global markets affect casting and genres

**Game Ideas:**
- Introduce streaming release strategy
- Regional appeal scores for scripts
- Licensing IP from book/comic deals

---

## 💰 Real Film Economics

| Tier           | Budget Range   | Example                         |
|----------------|----------------|---------------------------------|
| Microbudget    | <$1M           | *Clerks*, *Paranormal Activity* |
| Indie          | $1M–$10M       | *Moonlight*, *Lady Bird*        |
| Mid-Budget     | $10M–$40M      | *Whiplash*, *Knives Out*        |
| Blockbuster    | $100M+         | *Avatar*, *Avengers*            |

**Marketing**: Often 50-100% of production cost

**Game Ideas:**
- Tie marketing budget to potential earnings
- Allow micro-budget surprise hits

---

## 🌟 Actor Career Patterns

### Fame Curve (Generalized):
- **18-25**: Up-and-coming, niche appeal
- **26-35**: Peak fame potential
- **36-50**: Versatile, prestige
- **51+**: Lower casting frequency (unless legendary)

**Game Ideas:**
- Introduce actor age stat
- Age-based casting suitability
- Career arcs: breakout, peak, decline, comeback

---

## 🏆 Awards & Critics

- Awards season boosts studio and actor prestige
- Reviews impact earnings for prestige films
- Flop avoidance matters for long-term star value

**Game Ideas:**
- Add critical reviews per film
- Implement "Oscar bait" mechanics
- Awards affect studio and actor fame

---

## 🚀 Gameplay Inspiration Summary

| Mechanic | Inspired By | In-Game Equivalent |
|---------|-------------|---------------------|
| Star Contracts | Studio Era | Multi-film deal, cheaper salary |
| Director Impact | New Hollywood | Script boosts from auteur power |
| Genre Cycles | Real Trends | Quarterly trending genres |
| Marketing Budgets | Blockbuster Era | Spending influences earnings |
| Streaming Shift | Modern Era | Alternative release option |

---

Let me know if you'd like sections for:
- Real scandals & PR management
- Studio rivalries or acquisitions
- Historical templates (e.g. run MGM in 1935)



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
- Market fuctionality like Drug-Wars for buying and selling scripts, and finished moviess, maybe even a transfer market for actors, writers, and staff. Influenced by seasonality and event demands.

This integrated approach ensures every script choice, theme decision, and release date becomes a strategic puzzle—reflecting the dynamic, seasonal dance of Hollywood’s real‐world box office. Let me know which piece you’d like to prototype first

