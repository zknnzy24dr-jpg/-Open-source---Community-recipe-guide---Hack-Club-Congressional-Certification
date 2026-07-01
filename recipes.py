"""
Recipe database for Community Recipe Guide.

Each recipe is tagged with the pantry ingredients it primarily uses,
its estimated cost tier, and basic nutrition info. The matching engine
in recipe_engine.py scores recipes against user-provided ingredients.

Cost tiers are rough per-serving USD estimates based on common U.S.
grocery prices, used to support the project's health-equity goal of
surfacing low-cost, accessible meals first.
"""

RECIPES = [
    {
        "id": "rice-bean-bowl",
        "name": "Rice and Bean Power Bowl",
        "ingredients": ["rice", "beans", "onion", "garlic", "canned tomatoes"],
        "optional_ingredients": ["bell pepper", "cheese", "hot sauce", "lime"],
        "steps": [
            "Rinse 1 cup of rice and cook according to package directions.",
            "While rice cooks, dice the onion and mince the garlic.",
            "In a pan, saute onion and garlic in a little oil until soft, about 4 minutes.",
            "Add a can of beans (drained) and a can of diced tomatoes. Simmer 8-10 minutes.",
            "Season with salt, pepper, and any spices on hand (cumin or chili powder work well).",
            "Serve the bean mixture over rice. Top with cheese, hot sauce, or lime if available."
        ],
        "est_cost_per_serving": 1.25,
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "nutrition": {"calories": 380, "protein_g": 14, "fiber_g": 9},
        "dietary_tags": ["vegetarian", "vegan", "gluten-free"],
        "shelf_stable": True
    },
    {
        "id": "veggie-pasta",
        "name": "Pantry Vegetable Pasta",
        "ingredients": ["pasta", "canned tomatoes", "garlic", "olive oil"],
        "optional_ingredients": ["spinach", "carrots", "zucchini", "parmesan", "basil"],
        "steps": [
            "Bring a large pot of salted water to a boil and cook pasta until al dente.",
            "While pasta cooks, mince garlic and chop any available vegetables.",
            "Heat olive oil in a pan over medium heat and saute garlic for 1 minute.",
            "Add canned tomatoes and any chopped vegetables. Simmer 10 minutes.",
            "Drain pasta, reserving 1/4 cup of pasta water, and add pasta to the sauce.",
            "Toss together, adding pasta water if needed to loosen the sauce. Top with cheese if available."
        ],
        "est_cost_per_serving": 1.10,
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "nutrition": {"calories": 340, "protein_g": 10, "fiber_g": 5},
        "dietary_tags": ["vegetarian"],
        "shelf_stable": True
    },
    {
        "id": "egg-fried-rice",
        "name": "Leftover-Rice Fried Rice",
        "ingredients": ["rice", "eggs", "soy sauce", "onion"],
        "optional_ingredients": ["frozen peas", "carrots", "green onion", "garlic"],
        "steps": [
            "If using fresh rice, cook and let cool slightly (day-old rice works best).",
            "Beat 2-3 eggs in a bowl with a pinch of salt.",
            "Heat oil in a large pan or wok over medium-high heat.",
            "Scramble the eggs until just set, then remove and set aside.",
            "In the same pan, saute diced onion (and garlic, carrots, or peas if using).",
            "Add rice, breaking up clumps, and stir-fry 3-4 minutes.",
            "Return eggs to the pan, add soy sauce, and toss everything together."
        ],
        "est_cost_per_serving": 0.95,
        "servings": 3,
        "prep_time_minutes": 10,
        "cook_time_minutes": 15,
        "nutrition": {"calories": 310, "protein_g": 12, "fiber_g": 2},
        "dietary_tags": ["vegetarian"],
        "shelf_stable": False
    },
    {
        "id": "lentil-soup",
        "name": "One-Pot Lentil Soup",
        "ingredients": ["lentils", "onion", "carrots", "canned tomatoes", "garlic"],
        "optional_ingredients": ["celery", "spinach", "cumin", "bay leaf"],
        "steps": [
            "Rinse 1 cup of dry lentils.",
            "Dice onion and carrots, mince garlic.",
            "In a large pot, saute onion, carrots, and garlic in oil for 5 minutes.",
            "Add lentils, canned tomatoes, and 4 cups of water or broth.",
            "Bring to a boil, then reduce heat and simmer 25-30 minutes until lentils are tender.",
            "Season with salt, pepper, and cumin if available. Stir in spinach at the end if using."
        ],
        "est_cost_per_serving": 0.85,
        "servings": 6,
        "prep_time_minutes": 10,
        "cook_time_minutes": 30,
        "nutrition": {"calories": 210, "protein_g": 13, "fiber_g": 11},
        "dietary_tags": ["vegetarian", "vegan", "gluten-free"],
        "shelf_stable": True
    },
    {
        "id": "chicken-veggie-stirfry",
        "name": "Quick Chicken and Vegetable Stir-Fry",
        "ingredients": ["chicken", "soy sauce", "garlic", "onion"],
        "optional_ingredients": ["bell pepper", "broccoli", "carrots", "rice", "ginger"],
        "steps": [
            "Cut chicken into bite-sized pieces and season with salt and pepper.",
            "Heat oil in a large pan or wok over medium-high heat.",
            "Cook chicken until browned and cooked through, about 6-7 minutes. Remove and set aside.",
            "In the same pan, saute onion, garlic, and any available vegetables until tender-crisp.",
            "Return chicken to the pan, add soy sauce, and toss everything together for 2 minutes.",
            "Serve over rice if available."
        ],
        "est_cost_per_serving": 2.10,
        "servings": 4,
        "prep_time_minutes": 12,
        "cook_time_minutes": 15,
        "nutrition": {"calories": 290, "protein_g": 26, "fiber_g": 2},
        "dietary_tags": ["gluten-free-adaptable"],
        "shelf_stable": False
    },
    {
        "id": "oatmeal-bowl",
        "name": "Hearty Breakfast Oatmeal",
        "ingredients": ["oats", "milk"],
        "optional_ingredients": ["banana", "peanut butter", "cinnamon", "honey", "frozen berries"],
        "steps": [
            "Combine 1 cup oats with 2 cups milk (or water) in a pot.",
            "Bring to a simmer over medium heat, stirring occasionally.",
            "Cook 5-7 minutes until oats are soft and creamy.",
            "Remove from heat and stir in cinnamon if using.",
            "Top with banana, peanut butter, honey, or berries."
        ],
        "est_cost_per_serving": 0.55,
        "servings": 2,
        "prep_time_minutes": 2,
        "cook_time_minutes": 8,
        "nutrition": {"calories": 260, "protein_g": 9, "fiber_g": 6},
        "dietary_tags": ["vegetarian"],
        "shelf_stable": True
    },
    {
        "id": "bean-quesadillas",
        "name": "Black Bean Quesadillas",
        "ingredients": ["tortillas", "beans", "cheese"],
        "optional_ingredients": ["onion", "bell pepper", "hot sauce", "salsa"],
        "steps": [
            "Mash a can of drained beans lightly with a fork, leaving some texture.",
            "Spread the bean mixture onto half of a tortilla and top with cheese.",
            "Fold the tortilla over and cook in a dry pan over medium heat, 2-3 minutes per side.",
            "Repeat with remaining tortillas.",
            "Cut into wedges and serve with hot sauce or salsa if available."
        ],
        "est_cost_per_serving": 1.00,
        "servings": 4,
        "prep_time_minutes": 8,
        "cook_time_minutes": 12,
        "nutrition": {"calories": 320, "protein_g": 13, "fiber_g": 7},
        "dietary_tags": ["vegetarian"],
        "shelf_stable": True
    },
    {
        "id": "potato-hash",
        "name": "Skillet Potato Hash",
        "ingredients": ["potatoes", "onion", "eggs"],
        "optional_ingredients": ["bell pepper", "cheese", "paprika"],
        "steps": [
            "Dice potatoes into small cubes (leave skin on for extra fiber).",
            "Heat oil in a large skillet over medium heat.",
            "Add potatoes and cook, stirring occasionally, for 12-15 minutes until tender and browned.",
            "Add diced onion (and bell pepper if using) and cook another 5 minutes.",
            "Make small wells in the hash and crack eggs directly into the pan.",
            "Cover and cook until eggs reach desired doneness, about 4-5 minutes."
        ],
        "est_cost_per_serving": 0.90,
        "servings": 3,
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "nutrition": {"calories": 280, "protein_g": 11, "fiber_g": 4},
        "dietary_tags": ["vegetarian", "gluten-free"],
        "shelf_stable": True
    },
]


def all_ingredient_names():
    """Return the sorted set of all known ingredient names across recipes."""
    names = set()
    for recipe in RECIPES:
        names.update(recipe["ingredients"])
        names.update(recipe["optional_ingredients"])
    return sorted(names)
