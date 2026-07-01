"""
Test suite for Community Recipe Guide.

Run with: python3 -m pytest tests/test_app.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app
from recipe_engine import generate_recipes, parse_user_ingredients, normalize_ingredient, score_recipe
from data.recipes import RECIPES


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------- Route tests ----------

def test_homepage_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Community Recipe Guide" in resp.data


def test_about_page_loads(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"mission" in resp.data.lower() or b"Mission" in resp.data


def test_generate_endpoint_returns_matches(client):
    resp = client.post("/api/generate", json={"ingredients": "rice, beans, onion, garlic"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["matches"]) > 0
    assert data["matches"][0]["name"] == "Rice and Bean Power Bowl"


def test_generate_endpoint_empty_input(client):
    resp = client.post("/api/generate", json={"ingredients": ""})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["matches"] == []


def test_generate_endpoint_rejects_oversized_input(client):
    resp = client.post("/api/generate", json={"ingredients": "a" * 1000})
    assert resp.status_code == 400


def test_generate_endpoint_rejects_non_string(client):
    resp = client.post("/api/generate", json={"ingredients": 12345})
    assert resp.status_code == 400


def test_ingredients_list_endpoint(client):
    resp = client.get("/api/ingredients")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "rice" in data["ingredients"]
    assert "beans" in data["ingredients"]


# ---------- Recipe engine unit tests ----------

def test_normalize_ingredient_handles_aliases():
    assert normalize_ingredient("white rice") == "rice"
    assert normalize_ingredient("Black Beans") == "beans"
    assert normalize_ingredient("  Onions ") == "onion"


def test_parse_user_ingredients_comma_separated():
    result = parse_user_ingredients("rice, beans, onion")
    assert result == {"rice", "beans", "onion"}


def test_parse_user_ingredients_handles_and():
    result = parse_user_ingredients("rice and beans and onion")
    assert result == {"rice", "beans", "onion"}


def test_parse_user_ingredients_empty_string():
    assert parse_user_ingredients("") == set()
    assert parse_user_ingredients(None) == set()


def test_score_recipe_full_match():
    recipe = next(r for r in RECIPES if r["id"] == "rice-bean-bowl")
    user_ingredients = {"rice", "beans", "onion", "garlic", "canned tomatoes"}
    match = score_recipe(recipe, user_ingredients)
    assert match is not None
    assert len(match["missing_required"]) == 0
    assert match["completeness"] == 1.0


def test_score_recipe_partial_match():
    recipe = next(r for r in RECIPES if r["id"] == "rice-bean-bowl")
    user_ingredients = {"rice", "beans"}
    match = score_recipe(recipe, user_ingredients)
    assert match is not None
    assert len(match["missing_required"]) == 3
    assert 0 < match["completeness"] < 1.0


def test_score_recipe_no_overlap_returns_none():
    recipe = next(r for r in RECIPES if r["id"] == "rice-bean-bowl")
    user_ingredients = {"chocolate", "vanilla"}
    match = score_recipe(recipe, user_ingredients)
    assert match is None


def test_generate_recipes_ranks_cheaper_first_on_tie():
    result = generate_recipes("eggs")
    # Should not error and should return a usable structure
    assert "matches" in result
    assert "message" in result


def test_generate_recipes_nonsense_input():
    result = generate_recipes("xyznonsenseword")
    assert result["matches"] == []
    assert "no close matches" in result["message"].lower()


def test_generate_recipes_truly_empty_input():
    result = generate_recipes("")
    assert result["matches"] == []
    assert "couldn't find" in result["message"].lower()


def test_all_recipes_have_required_fields():
    required_fields = {"id", "name", "ingredients", "optional_ingredients", "steps",
                        "est_cost_per_serving", "servings", "nutrition"}
    for recipe in RECIPES:
        assert required_fields.issubset(recipe.keys()), f"{recipe['id']} missing fields"
        assert len(recipe["steps"]) > 0
        assert recipe["est_cost_per_serving"] > 0


def test_recipe_ids_are_unique():
    ids = [r["id"] for r in RECIPES]
    assert len(ids) == len(set(ids))
