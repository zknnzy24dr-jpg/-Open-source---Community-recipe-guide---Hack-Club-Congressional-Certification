"""
Community Recipe Guide
-----------------------
A Flask web application that helps users turn the ingredients they already
have at home into accessible, low-cost, nutritious recipes. Built as a
Congressional App Challenge submission focused on food and health equity.

The recipe generator uses a deterministic, rule-based matching engine
(see recipe_engine.py) rather than a third-party AI API, so the app has
no external dependencies and runs fully offline.
"""

from flask import Flask, render_template, request, jsonify
from recipe_engine import generate_recipes
from data.recipes import all_ingredient_names, RECIPES

app = Flask(__name__)


@app.route("/")
def home():
    """Landing page with mission statement and chat-style recipe generator."""
    return render_template("index.html", recipe_count=len(RECIPES))


@app.route("/about")
def about():
    """About page explaining the project's health-equity mission."""
    return render_template("about.html")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """
    Accepts JSON: { "ingredients": "rice, beans, onion" }
    Returns JSON with matched recipes ranked by relevance and cost.
    """
    payload = request.get_json(silent=True) or {}
    user_text = payload.get("ingredients", "")

    if not isinstance(user_text, str) or len(user_text) > 500:
        return jsonify({"error": "Invalid input."}), 400

    result = generate_recipes(user_text)

    # Serialize recipe matches into JSON-friendly form.
    serialized_matches = []
    for match in result["matches"]:
        recipe = match["recipe"]
        serialized_matches.append({
            "id": recipe["id"],
            "name": recipe["name"],
            "steps": recipe["steps"],
            "servings": recipe["servings"],
            "prep_time_minutes": recipe["prep_time_minutes"],
            "cook_time_minutes": recipe["cook_time_minutes"],
            "est_cost_per_serving": recipe["est_cost_per_serving"],
            "nutrition": recipe["nutrition"],
            "dietary_tags": recipe["dietary_tags"],
            "matched_required": match["matched_required"],
            "matched_optional": match["matched_optional"],
            "missing_required": match["missing_required"],
        })

    return jsonify({
        "user_ingredients": result["user_ingredients"],
        "message": result["message"],
        "matches": serialized_matches,
    })


@app.route("/api/ingredients", methods=["GET"])
def api_ingredients():
    """Returns the full list of known ingredients, used for input autocomplete."""
    return jsonify({"ingredients": all_ingredient_names()})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
