"""Tests for schemas."""

from app.schemas import RecipeList, RecipeCreate, RecipeDetail


def test_recipe_list_valid():
    """Test valid RecipeList."""
    data = {
        "id": 1,
        "name": "Тестовый рецепт",
        "views": 10,
        "cooking_time": 30
    }
    recipe = RecipeList(**data)
    assert recipe.id == 1
    assert recipe.name == "Тестовый рецепт"
    assert recipe.views == 10
    assert recipe.cooking_time == 30


def test_recipe_list_optional_fields():
    """Test RecipeList with different values."""
    data = {
        "id": 2,
        "name": "Другой рецепт",
        "views": 0,
        "cooking_time": 45
    }
    recipe = RecipeList(**data)
    assert recipe.id == 2
    assert recipe.views == 0


def test_recipe_create_valid():
    """Test valid RecipeCreate."""
    data = {
        "name": "Новый рецепт",
        "cooking_time": 45,
        "ingredients": "Мука, яйца, сахар",
        "description": "Вкусный десерт"
    }
    recipe = RecipeCreate(**data)
    assert recipe.name == "Новый рецепт"
    assert recipe.cooking_time == 45
    assert recipe.ingredients == "Мука, яйца, сахар"
    assert recipe.description == "Вкусный десерт"


def test_recipe_create_with_zero_time():
    """Test RecipeCreate with zero cooking time (приложение обрабатывает это)."""
    data = {
        "name": "Новый рецепт",
        "cooking_time": 0,
        "ingredients": "Мука, яйца, сахар",
        "description": "Вкусный десерт"
    }
    recipe = RecipeCreate(**data)
    assert recipe.cooking_time == 0


def test_recipe_create_empty_name():
    """Test RecipeCreate with empty name."""
    data = {
        "name": "",
        "cooking_time": 30,
        "ingredients": "Мука, яйца, сахар",
        "description": "Вкусный десерт"
    }
    recipe = RecipeCreate(**data)
    assert recipe.name == ""


def test_recipe_detail_valid():
    """Test valid RecipeDetail."""
    data = {
        "id": 1,
        "name": "Детальный рецепт",
        "cooking_time": 30,
        "ingredients": "Ингредиенты",
        "description": "Описание",
        "views": 10
    }
    recipe = RecipeDetail(**data)
    assert recipe.id == 1
    assert recipe.name == "Детальный рецепт"
    assert recipe.views == 10
