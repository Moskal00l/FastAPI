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


@pytest.mark.asyncio
async def test_create_recipe_invalid_time(client: AsyncClient):
    """Test creating recipe with invalid cooking time."""
    recipe_data = {
        "name": "Некорректный рецепт",
        "cooking_time": 0,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    
    response = await client.post("/recipes/", json=recipe_data)
    # Pydantic V2 возвращает 422 для ошибок валидации
    assert response.status_code == 422


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
    
    response = await client.get("/recipes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


@pytest.mark.asyncio
async def test_get_recipe_detail(client: AsyncClient, sample_recipe):
    """Test getting recipe detail."""
    recipe_id = sample_recipe.id
    
    response = await client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == recipe_id
    assert data["name"] == sample_recipe.name
    assert data["views"] >= 0


@pytest.mark.asyncio
async def test_get_recipe_detail_increments_views(client: AsyncClient, sample_recipe):
    """Test that views increment when getting recipe detail."""
    recipe_id = sample_recipe.id
    
    response1 = await client.get(f"/recipes/{recipe_id}")
    assert response1.status_code == 200
    data1 = response1.json()
    views1 = data1["views"]
    
    response2 = await client.get(f"/recipes/{recipe_id}")
    assert response2.status_code == 200
    data2 = response2.json()
    views2 = data2["views"]
    
    # Views должны увеличиться
    assert views2 > views1


@pytest.mark.asyncio
async def test_get_nonexistent_recipe(client: AsyncClient):
    """Test getting nonexistent recipe."""
    response = await client.get("/recipes/99999")
    assert response.status_code == 404
    data = response.json()
    assert "Рецепт не найден" in data["detail"]


@pytest.mark.asyncio
async def test_delete_recipe(client: AsyncClient, sample_recipe):
    """Test deleting a recipe."""
    recipe_id = sample_recipe.id
    
    response = await client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 204
    
    get_response = await client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
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
    
    response = await client.get("/recipes/?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    
    response = await client.get("/recipes/?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


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
