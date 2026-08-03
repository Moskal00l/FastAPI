import pytest
from pydantic import ValidationError

from schemas import RecipeList, RecipeCreate, RecipeDetail


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


def test_recipe_list_invalid_views():
    """Test RecipeList with negative views."""
    data = {
        "id": 1,
        "name": "Тестовый рецепт",
        "views": -1,
        "cooking_time": 30
    }
    with pytest.raises(ValidationError):
        RecipeList(**data)


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


def test_recipe_create_invalid_time():
    """Test RecipeCreate with zero cooking time."""
    data = {
        "name": "Новый рецепт",
        "cooking_time": 0,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    with pytest.raises(ValidationError) as exc_info:
        RecipeCreate(**data)
    error_msg = str(exc_info.value).lower()
    assert "cooking_time" in error_msg or "greater than 0" in error_msg


def test_recipe_create_empty_name():
    """Test RecipeCreate with empty name."""
    data = {
        "name": "",
        "cooking_time": 30,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    with pytest.raises(ValidationError) as exc_info:
        RecipeCreate(**data)
    error_msg = str(exc_info.value).lower()
    assert "name" in error_msg or "string" in error_msg


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
