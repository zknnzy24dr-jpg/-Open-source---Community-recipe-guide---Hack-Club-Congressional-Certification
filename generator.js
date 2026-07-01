/**
 * Community Recipe Guide — Recipe generator frontend
 *
 * Sends the user's ingredient list to the Flask backend (/api/generate),
 * which runs it through the rule-based matching engine in recipe_engine.py,
 * then renders the ranked recipe matches as cards.
 */

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("ingredient-input");
  const button = document.getElementById("generate-btn");
  const resultsEl = document.getElementById("results");
  const exampleChips = document.querySelectorAll(".example-chip");

  async function generateRecipes(ingredientText) {
    if (!ingredientText || !ingredientText.trim()) {
      resultsEl.innerHTML = `<p class="results-message">Add a few ingredients above to get started.</p>`;
      return;
    }

    resultsEl.innerHTML = `<p class="results-message">Searching the pantry...</p>`;

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredients: ingredientText }),
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      const data = await response.json();
      renderResults(data);
    } catch (err) {
      resultsEl.innerHTML = `<p class="results-message">Something went wrong reaching the recipe generator. Please try again.</p>`;
      console.error(err);
    }
  }

  function renderResults(data) {
    if (!data.matches || data.matches.length === 0) {
      resultsEl.innerHTML = `<p class="results-message">${escapeHtml(data.message)}</p>`;
      return;
    }

    const cardsHtml = data.matches.map(buildRecipeCard).join("");
    resultsEl.innerHTML = `
      <p class="results-message">${escapeHtml(data.message)}</p>
      ${cardsHtml}
    `;
  }

  function buildRecipeCard(recipe) {
    const haveTags = [...recipe.matched_required, ...recipe.matched_optional]
      .map((ing) => `<span class="tag have">✓ ${escapeHtml(ing)}</span>`)
      .join("");

    const missingTags = recipe.missing_required
      .map((ing) => `<span class="tag missing">+ ${escapeHtml(ing)}</span>`)
      .join("");

    const stepsHtml = recipe.steps
      .map((step) => `<li>${escapeHtml(step)}</li>`)
      .join("");

    return `
      <article class="recipe-card">
        <div class="recipe-card-header">
          <h3>${escapeHtml(recipe.name)}</h3>
          <span class="cost-badge">~$${recipe.est_cost_per_serving.toFixed(2)} / serving</span>
        </div>
        <div class="recipe-meta">
          <span><strong>${recipe.servings}</strong> servings</span>
          <span><strong>${recipe.prep_time_minutes + recipe.cook_time_minutes}</strong> min total</span>
          <span><strong>${recipe.nutrition.calories}</strong> cal/serving</span>
          <span><strong>${recipe.nutrition.protein_g}g</strong> protein</span>
        </div>
        <div class="match-tags">
          ${haveTags}
          ${missingTags}
        </div>
        <ol class="recipe-steps">
          ${stepsHtml}
        </ol>
      </article>
    `;
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  button.addEventListener("click", () => generateRecipes(input.value));

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      generateRecipes(input.value);
    }
  });

  exampleChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      input.value = chip.dataset.example;
      generateRecipes(input.value);
      input.focus();
    });
  });
});
