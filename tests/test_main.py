"""Tests for main application."""

import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.anyio


async def test_root(client: AsyncClient):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Модульная Async API. /docs"}


async def test_create_recipe(client: AsyncClient):
    """Test creating a recipe."""
    recipe_data = {
        "name": "Новый рецепт",
        "cooking_time": 45,
        "ingredients": "Мука, яйца, сахар",
        "description": "Вкусный десерт"
    }
    response = await client.post("/recipes/", json=recipe_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == recipe_data["name"]
    assert data["cooking_time"] == recipe_data["cooking_time"]
    assert data["views"] == 0
    assert "id" in data


async def test_create_recipe_invalid_time(client: AsyncClient):
    """Test creating recipe with invalid cooking time."""
    recipe_data = {
        "name": "Некорректный рецепт",
        "cooking_time": 0,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    response = await client.post("/recipes/", json=recipe_data)
    # Приложение возвращает 400 для cooking_time <= 0
    assert response.status_code == 400
    data = response.json()
    assert "Время приготовления должно быть больше 0" in data["detail"]


async def test_get_recipes(client: AsyncClient):
    """Test getting all recipes."""
    # Создаем несколько рецептов
    for i in range(3):
        response = await client.post("/recipes/", json={
            "name": f"Рецепт {i}",
            "cooking_time": 30 + i * 5,
            "ingredients": f"Ингредиенты {i}",
            "description": f"Описание {i}"
        })
        assert response.status_code == 201

    response = await client.get("/recipes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


async def test_get_recipe_detail(client: AsyncClient):
    """Test getting recipe detail."""
    # Создаем рецепт
    recipe_data = {
        "name": "Рецепт для деталей",
        "cooking_time": 30,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    create_response = await client.post("/recipes/", json=recipe_data)
    assert create_response.status_code == 201
    recipe_id = create_response.json()["id"]

    response = await client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == recipe_id
    assert data["name"] == recipe_data["name"]


async def test_get_recipe_detail_increments_views(client: AsyncClient):
    """Test that views increment when getting recipe detail."""
    # Создаем рецепт
    recipe_data = {
        "name": "Рецепт для просмотров",
        "cooking_time": 30,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    create_response = await client.post("/recipes/", json=recipe_data)
    assert create_response.status_code == 201
    recipe_id = create_response.json()["id"]

    # Первый запрос
    response1 = await client.get(f"/recipes/{recipe_id}")
    assert response1.status_code == 200
    data1 = response1.json()
    views1 = data1["views"]

    # Второй запрос
    response2 = await client.get(f"/recipes/{recipe_id}")
    assert response2.status_code == 200
    data2 = response2.json()
    views2 = data2["views"]

    # Views должны увеличиться
    assert views2 > views1


async def test_get_nonexistent_recipe(client: AsyncClient):
    """Test getting nonexistent recipe."""
    response = await client.get("/recipes/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Рецепт не найден"}


async def test_delete_recipe(client: AsyncClient):
    """Test deleting a recipe."""
    # Создаем рецепт
    recipe_data = {
        "name": "Рецепт для удаления",
        "cooking_time": 30,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    create_response = await client.post("/recipes/", json=recipe_data)
    assert create_response.status_code == 201
    recipe_id = create_response.json()["id"]

    # Удаляем
    response = await client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 204

    # Проверяем, что рецепт удален
    get_response = await client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 404


async def test_get_recipes_pagination(client: AsyncClient):
    """Test recipes pagination."""
    # Создаем 10 рецептов
    for i in range(10):
        response = await client.post("/recipes/", json={
            "name": f"Рецепт {i}",
            "cooking_time": 30,
            "ingredients": f"Ингредиенты {i}",
            "description": f"Описание {i}"
        })
        assert response.status_code == 201

    # Первая страница
    response = await client.get("/recipes/?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

    # Вторая страница
    response = await client.get("/recipes/?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5