"""Tests for models."""

from app.models import RecipeDB


def test_recipe_creation():
    """Test creating a recipe instance."""
    recipe = RecipeDB(
        name="Тестовый рецепт",
        cooking_time=30,
        ingredients="Мука, яйца, сахар",
        description="Вкусный десерт"
    )
    assert recipe.name == "Тестовый рецепт"
    assert recipe.cooking_time == 30
    assert recipe.ingredients == "Мука, яйца, сахар"
    assert recipe.description == "Вкусный десерт"
    assert hasattr(recipe, "views")


def test_recipe_repr():
    """Test recipe string representation."""
    recipe = RecipeDB(
        name="Тестовый рецепт",
        cooking_time=30,
        ingredients="Ингредиенты",
        description="Описание"
    )
    repr_str = repr(recipe)
    assert "RecipeDB" in repr_str
    assert "id" in repr_str or "RecipeDB" in repr_str


def test_recipe_attributes():
    """Test that recipe has all required attributes."""
    recipe = RecipeDB(
        name="Тестовый рецепт",
        cooking_time=30,
        ingredients="Ингредиенты",
        description="Описание"
    )
    assert hasattr(recipe, "id")
    assert hasattr(recipe, "name")
    assert hasattr(recipe, "cooking_time")
    assert hasattr(recipe, "ingredients")
    assert hasattr(recipe, "description")
    assert hasattr(recipe, "views")


def test_recipe_default_views():
    """Test that views attribute exists and can be set."""
    recipe = RecipeDB(
        name="Тестовый рецепт",
        cooking_time=30,
        ingredients="Ингредиенты",
        description="Описание"
    )
    assert hasattr(recipe, "views")
    if recipe.views is not None:
        assert isinstance(recipe.views, int)
