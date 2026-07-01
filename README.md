# Community Recipe Guide

**A Congressional App Challenge submission** — a Python/Flask web application that helps users turn the ingredients they already have at home into accessible, low-cost, nutritious recipes. Built around food and health equity: the tool is designed for families navigating food access challenges, tight grocery budgets, or food deserts, where an extra shopping trip isn't always possible.

Live site: [communityrecipeguide.com](https://communityrecipeguide.com)

---

## What it does

You type in what you have — "rice, beans, onion, garlic" — and the app finds recipes you can make right now, ranked by how well they match your ingredients and how affordable they are per serving.

The recipe generator is fully rule-based and deterministic. It runs entirely on the server with no external API calls, no AI subscriptions, and no API keys required. That means it runs offline, loads instantly, and never has an availability dependency.

**Features:**
- Ingredient-to-recipe matching with a custom scoring engine
- Recipes ranked by match quality, then by estimated cost per serving
- Visual match tags showing which ingredients you have vs. which you'd still need
- "Quick example" chips so first-time users can explore without typing
- `/api/generate` and `/api/ingredients` JSON endpoints
- Responsive layout down to mobile
- 19 passing automated tests covering routes, engine logic, and input validation

---

## Project structure

```
community-recipe-guide/
├── app.py                  # Flask app: routes and API endpoints
├── recipe_engine.py        # Rule-based ingredient matching & scoring logic
├── requirements.txt        # Python dependencies (Flask only)
├── data/
│   ├── __init__.py
│   └── recipes.py          # Recipe database with nutrition and cost data
├── templates/
│   ├── base.html           # Shared site layout (header, nav, footer)
│   ├── index.html          # Home page: hero, generator, mission cards
│   └── about.html          # Mission and how-it-works page
├── static/
│   ├── css/
│   │   └── style.css       # Design system and all styles
│   └── js/
│       └── generator.js    # Frontend: calls the API, renders recipe cards
└── tests/
    └── test_app.py         # pytest suite (19 tests)
```

---

## How the matching engine works

The core logic lives in `recipe_engine.py`. Given a raw text string like `"rice, beans, onion"`, it:

1. **Tokenizes and normalizes** the input — splits on commas, "and", semicolons, and newlines; lowercases everything; resolves known aliases (`"white rice"` → `"rice"`, `"black beans"` → `"beans"`, `"egg"` → `"eggs"`, etc.)

2. **Scores every recipe** using this formula:
   ```
   score = (matched required ingredients × 2)
         + (matched optional ingredients × 1)
         - (missing required ingredients × 1.5)
   ```

3. **Ranks results** by score descending, then by estimated cost-per-serving ascending (cheaper meals surface first among ties), then by completeness ratio.

4. Returns the top 3 matches with full details: steps, nutrition, per-serving cost, which ingredients you have, and which ones you'd still need.

The scoring weights were chosen to prioritize recipes where you already have most of what's needed, while still surfacing partial matches that only need one or two additions.

---

## Setup and running locally

**Requirements:** Python 3.10+

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/community-recipe-guide.git
cd community-recipe-guide

# 2. Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the development server
python3 app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Running the tests

```bash
python3 -m pytest tests/test_app.py -v
```

Expected output: **19 passed**

The test suite covers:
- All Flask routes (homepage, about, API generate, API ingredients list)
- Input validation (empty input, oversized payload, non-string type)
- Engine unit tests: alias normalization, ingredient parsing, scoring logic
- Data integrity: all recipes have required fields, all IDs are unique

---

## API reference

### `POST /api/generate`

Accepts a JSON body, returns ranked recipe matches.

**Request:**
```json
{ "ingredients": "rice, beans, onion, garlic" }
```

**Response:**
```json
{
  "user_ingredients": ["beans", "garlic", "onion", "rice"],
  "message": "Found 3 recipe(s) based on what you have on hand.",
  "matches": [
    {
      "id": "rice-bean-bowl",
      "name": "Rice and Bean Power Bowl",
      "steps": ["..."],
      "servings": 4,
      "prep_time_minutes": 10,
      "cook_time_minutes": 20,
      "est_cost_per_serving": 1.25,
      "nutrition": { "calories": 380, "protein_g": 14, "fiber_g": 9 },
      "dietary_tags": ["vegetarian", "vegan", "gluten-free"],
      "matched_required": ["beans", "garlic", "onion", "rice"],
      "matched_optional": [],
      "missing_required": ["canned tomatoes"]
    }
  ]
}
```

### `GET /api/ingredients`

Returns the full list of known ingredient names (used for autocomplete suggestions).

**Response:**
```json
{ "ingredients": ["banana", "beans", "bell pepper", "..."] }
```

---

## Health equity context

Most recipe platforms assume the user is shopping for a specific dish. Community Recipe Guide flips that assumption: start from what you have, not what you'd need to buy.

The recipe database is built around low-cost, shelf-stable staples — rice, beans, lentils, pasta, oats, canned tomatoes, eggs — with per-serving cost estimates between $0.55 and $2.10. The ranking algorithm surfaces the cheapest matching option first among equally good matches.

The platform was featured on the **NYC Department of Health and Mental Hygiene's biweekly email list** and has been used in outreach to state nutrition departments, food pantry networks, and community health programs.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask 3.0 |
| Templating | Jinja2 (built into Flask) |
| Frontend | Vanilla HTML/CSS/JS (no framework) |
| Testing | pytest |
| Fonts | Fraunces, Inter, JetBrains Mono (Google Fonts) |
| Deployment | Communityrecipeguide.com (external) |

No database. No external API calls. No build step. `pip install -r requirements.txt` and `python3 app.py` is the full setup.

---

## Congressional App Challenge certification

This repository contains the original source code for the Community Recipe Guide, built from scratch in Python and Flask for the Hack Club Congressional App Challenge certification requirement. The live site at communityrecipeguide.com runs the same application logic documented here.

Submitted by: Matthew  
School: Solon High School, Class of 2027  
District: Ohio's 11th Congressional District
