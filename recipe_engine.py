"""
Rule-based recipe matching engine.

This module implements the "recipe generator" logic for Community Recipe
Guide. Given a free-text list of ingredients a user has on hand, it:

  1. Normalizes and tokenizes the input against a known ingredient vocabulary.
  2. Scores every recipe in the database based on how many of the recipe's
     required and optional ingredients are matched.
  3. Ranks recipes by match quality, then by cost-per-serving (to support
     the project's health-equity goal of surfacing affordable options first).

No external AI API is used. This is intentional: the matching logic below
is fully deterministic and runs offline, so the app has zero external
dependencies or API keys at runtime.
"""

import re
from data.recipes import RECIPES, all_ingredient_names

# Common synonyms/aliases so casual user input still matches the database.
INGREDIENT_ALIASES = {
    "white rice": "rice",
    "brown rice": "rice",
    "black beans": "beans",
    "kidney beans": "beans",
    "pinto beans": "beans",
    "canned beans": "beans",
    "tomato": "canned tomatoes",
    "tomatoes": "canned tomatoes",
    "diced tomatoes": "canned tomatoes",
    "egg": "eggs",
    "potato": "potatoes",
    "onions": "onion",
    "garlic clove": "garlic",
    "garlic cloves": "garlic",
    "spaghetti": "pasta",
    "noodles": "pasta",
    "chicken breast": "chicken",
    "chicken thighs": "chicken",
    "soy": "soy sauce",
    "tortilla": "tortillas",
    "lentil": "lentils",
    "oat": "oats",
    "oatmeal": "oats",
}


def normalize_ingredient(raw_text):
    """Lowercase, strip, and resolve a single ingredient string to a canonical name."""
    cleaned = raw_text.strip().lower()
    cleaned = re.sub(r"[^a-z\s]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return INGREDIENT_ALIASES.get(cleaned, cleaned)


def parse_user_ingredients(user_text):
    """
    Parse a free-text ingredient list (comma, 'and', or newline separated)
    into a set of normalized ingredient names.
    """
    if not user_text:
        return set()

    # Split on commas, "and", semicolons, or newlines.
    parts = re.split(r",|\band\b|;|\n", user_text.lower())
    normalized = {normalize_ingredient(p) for p in parts if p.strip()}
    normalized.discard("")
    return normalized


def score_recipe(recipe, user_ingredients):
    """
    Score a single recipe against the user's available ingredients.

    Scoring rules:
      +2 points for each required ingredient the user has
      +1 point for each optional ingredient the user has
      -1.5 points for each required ingredient the user is missing

    Returns a dict with the score and match details, or None if the
    recipe shares no ingredients at all with the user's input.
    """
    required = set(recipe["ingredients"])
    optional = set(recipe["optional_ingredients"])

    matched_required = required & user_ingredients
    matched_optional = optional & user_ingredients
    missing_required = required - user_ingredients

    if not matched_required and not matched_optional:
        return None

    score = (len(matched_required) * 2.0) + (len(matched_optional) * 1.0) - (len(missing_required) * 1.5)
    completeness = len(matched_required) / len(required) if required else 0

    return {
        "recipe": recipe,
        "score": score,
        "completeness": completeness,
        "matched_required": sorted(matched_required),
        "matched_optional": sorted(matched_optional),
        "missing_required": sorted(missing_required),
    }


def generate_recipes(user_text, max_results=3):
    """
    Main entry point for the recipe generator. Takes raw user input
    describing available ingredients and returns a ranked list of
    recipe matches.
    """
    user_ingredients = parse_user_ingredients(user_text)

    if not user_ingredients:
        return {
            "user_ingredients": [],
            "matches": [],
            "message": "I couldn't find any recognizable ingredients in that. "
                       "Try listing what you have, like: rice, beans, onion, garlic."
        }

    results = []
    for recipe in RECIPES:
        match = score_recipe(recipe, user_ingredients)
        if match:
            results.append(match)

    # Rank by score first, then prefer lower cost-per-serving (health-equity goal),
    # then by how complete the match is.
    results.sort(key=lambda m: (-m["score"], m["recipe"]["est_cost_per_serving"], -m["completeness"]))

    top_matches = results[:max_results]

    if not top_matches:
        message = (
            "No close matches yet. Try adding a staple like rice, beans, pasta, "
            "or eggs to your list and I'll find something."
        )
    else:
        message = f"Found {len(top_matches)} recipe(s) based on what you have on hand."

    return {
        "user_ingredients": sorted(user_ingredients),
        "matches": top_matches,
        "message": message,
    }
