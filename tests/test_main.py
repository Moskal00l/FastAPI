import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Модульная Async API" in data["message"]


@pytest.mark.asyncio
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
    assert data["id"] > 0


@pytest.mark.asyncio
async def test_create_recipe_invalid_time(client: AsyncClient):
    """Test creating recipe with invalid cooking time (0)."""
    recipe_data = {
        "name": "Некорректный рецепт",
        "cooking_time": 0,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    
    response = await client.post("/recipes/", json=recipe_data)
    # Pydantic V2 возвращает 422 для ошибок валидации
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    # Проверяем, что ошибка связана с cooking_time
    error_detail = str(data["detail"]).lower()
    assert "cooking_time" in error_detail or "greater than 0" in error_detail


@pytest.mark.asyncio
async def test_create_recipe_negative_time(client: AsyncClient):
    """Test creating recipe with negative cooking time."""
    recipe_data = {
        "name": "Некорректный рецепт",
        "cooking_time": -5,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    
    response = await client.post("/recipes/", json=recipe_data)
    assert response.status_code == 422  # Pydantic валидация


@pytest.mark.asyncio
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
    
    # Получаем все рецепты
    response = await client.get("/recipes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    
    if len(data) >= 2:
        assert data[0]["cooking_time"] <= data[1]["cooking_time"]


@pytest.mark.asyncio
async def test_get_recipe_detail(client: AsyncClient, sample_recipe):
    """Test getting recipe detail."""
    recipe_id = sample_recipe.id
    
    response = await client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == recipe_id
    assert data["name"] == sample_recipe.name
    assert data["cooking_time"] == sample_recipe.cooking_time
    assert data["ingredients"] == sample_recipe.ingredients
    assert data["description"] == sample_recipe.description
    assert data["views"] >= 0


@pytest.mark.asyncio
async def test_get_recipe_detail_increments_views(client: AsyncClient, sample_recipe):
    """Test that views increment when getting recipe detail."""
    recipe_id = sample_recipe.id
    
    # Первый запрос
    response1 = await client.get(f"/recipes/{recipe_id}")
    assert response1.status_code == 200
    data1 = response1.json()
    initial_views = data1["views"]
    
    # Второй запрос
    response2 = await client.get(f"/recipes/{recipe_id}")
    assert response2.status_code == 200
    data2 = response2.json()
    
    # Просмотры должны увеличиться
    assert data2["views"] > initial_views
    assert data2["views"] == initial_views + 1


@pytest.mark.asyncio
async def test_get_nonexistent_recipe(client: AsyncClient):
    """Test getting nonexistent recipe."""
    response = await client.get("/recipes/99999")
    assert response.status_code == 404
    data = response.json()
    assert "Рецепт не найден" in data["detail"]


@pytest.mark.asyncio
async def test_update_recipe(client: AsyncClient, sample_recipe):
    """Test updating a recipe."""
    recipe_id = sample_recipe.id
    update_data = {
        "name": "Обновленный рецепт",
        "cooking_time": 60,
        "ingredients": "Новые ингредиенты",
        "description": "Новое описание"
    }
    
    response = await client.put(f"/recipes/{recipe_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["cooking_time"] == update_data["cooking_time"]
    assert data["ingredients"] == update_data["ingredients"]
    assert data["description"] == update_data["description"]
    assert data["id"] == recipe_id


@pytest.mark.asyncio
async def test_update_nonexistent_recipe(client: AsyncClient):
    """Test updating nonexistent recipe."""
    update_data = {
        "name": "Обновленный рецепт",
        "cooking_time": 60,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    
    response = await client.put("/recipes/99999", json=update_data)
    assert response.status_code == 404
    data = response.json()
    assert "Рецепт не найден" in data["detail"]


@pytest.mark.asyncio
async def test_delete_recipe(client: AsyncClient, sample_recipe):
    """Test deleting a recipe."""
    recipe_id = sample_recipe.id
    
    # Удаляем рецепт
    response = await client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 204
    
    # Проверяем, что рецепт удален
    get_response = await client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_recipe(client: AsyncClient):
    """Test deleting nonexistent recipe."""
    response = await client.delete("/recipes/99999")
    assert response.status_code == 404
    data = response.json()
    assert "Рецепт не найден" in data["detail"]


@pytest.mark.asyncio
async def test_get_recipes_pagination(client: AsyncClient):
    """Test recipes pagination."""
    for i in range(10):
        response = await client.post("/recipes/", json={
            "name": f"Рецепт {i}",
            "cooking_time": 30,
            "ingredients": f"Ингредиенты {i}",
            "description": f"Описание {i}"
        })
        assert response.status_code == 201
    
    response = await client.get("/recipes/?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    
    response = await client.get("/recipes/?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    
    response1 = await client.get("/recipes/?skip=0&limit=5")
    response2 = await client.get("/recipes/?skip=5&limit=5")
    data1 = response1.json()
    data2 = response2.json()
    ids1 = [item["id"] for item in data1]
    ids2 = [item["id"] for item in data2]
    assert len(set(ids1) & set(ids2)) == 0


@pytest.mark.asyncio
async def test_get_recipes_ordering(client: AsyncClient):
    """Test recipes ordering by views and cooking_time."""

    recipes = [
        {"name": "Популярный быстрый", "cooking_time": 10, "views": 100},
        {"name": "Популярный медленный", "cooking_time": 60, "views": 100},
        {"name": "Непопулярный быстрый", "cooking_time": 15, "views": 0},
        {"name": "Непопулярный медленный", "cooking_time": 45, "views": 0},
    ]
    
    for recipe_data in recipes:
        response = await client.post("/recipes/", json={
            "name": recipe_data["name"],
            "cooking_time": recipe_data["cooking_time"],
            "ingredients": "Ингредиенты",
            "description": "Описание"
        })
        assert response.status_code == 201

        recipe_id = response.json()["id"]
        for _ in range(recipe_data["views"]):
            await client.get(f"/recipes/{recipe_id}")
    

    response = await client.get("/recipes/")
    assert response.status_code == 200
    data = response.json()


    positions = {}
    for i, item in enumerate(data):
        positions[item["name"]] = i
    

    assert positions["Популярный быстрый"] < positions["Популярный медленный"]
    assert positions["Популярный медленный"] < positions["Непопулярный быстрый"]
    assert positions["Непопулярный быстрый"] < positions["Непопулярный медленный"]
