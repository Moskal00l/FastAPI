import pytest
from pydantic import ValidationError

from schemas import RecipeList, RecipeCreate, RecipeDetail


def test_recipe_list_valid():
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
    data = {
        "id": 1,
        "name": "Тестовый рецепт",
        "views": -1,
        "cooking_time": 30
    }
    with pytest.raises(ValidationError):
        RecipeList(**data)


def test_recipe_create_valid():
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
    data = {
        "name": "Новый рецепт",
        "cooking_time": 0,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    with pytest.raises(ValidationError) as exc_info:
        RecipeCreate(**data)
    assert "Время приготовления должно быть больше 0" in str(exc_info.value)


def test_recipe_create_empty_name():
    data = {
        "name": "",
        "cooking_time": 30,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    with pytest.raises(ValidationError) as exc_info:
        RecipeCreate(**data)
    assert "Название не может быть пустым" in str(exc_info.value)


def test_recipe_detail_valid():
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
