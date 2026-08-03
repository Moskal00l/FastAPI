import pytest
from fastapi.testclient import TestClient
from main import app


def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Модульная Async API" in data["message"]


def test_create_recipe(client: TestClient):
    recipe_data = {
        "name": "Новый рецепт",
        "cooking_time": 45,
        "ingredients": "Мука, яйца, сахар",
        "description": "Вкусный десерт"
    }
    
    response = client.post("/recipes/", json=recipe_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == recipe_data["name"]
    assert data["cooking_time"] == recipe_data["cooking_time"]
    assert data["views"] == 0
    assert "id" in data


def test_create_recipe_invalid_time(client: TestClient):
    recipe_data = {
        "name": "Некорректный рецепт",
        "cooking_time": 0,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    
    response = client.post("/recipes/", json=recipe_data)
    assert response.status_code == 400
    data = response.json()
    assert "Время приготовления должно быть больше 0" in data["detail"]


def test_get_recipes(client: TestClient):
    for i in range(3):
        client.post("/recipes/", json={
            "name": f"Рецепт {i}",
            "cooking_time": 30 + i * 5,
            "ingredients": f"Ингредиенты {i}",
            "description": f"Описание {i}"
        })
    
    response = client.get("/recipes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


def test_get_recipe_detail(client: TestClient, sample_recipe):
    """Test getting recipe detail."""
    recipe_id = sample_recipe.id
    
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == recipe_id
    assert data["name"] == sample_recipe.name
    assert data["views"] == 0


def test_get_recipe_detail_increments_views(client: TestClient, sample_recipe):
    """Test that views increment when getting recipe detail."""
    recipe_id = sample_recipe.id
    
    response1 = client.get(f"/recipes/{recipe_id}")
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["views"] == 1
    
    response2 = client.get(f"/recipes/{recipe_id}")
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["views"] == 2


def test_get_nonexistent_recipe(client: TestClient):
    response = client.get("/recipes/99999")
    assert response.status_code == 404
    data = response.json()
    assert "Рецепт не найден" in data["detail"]


def test_update_recipe(client: TestClient, sample_recipe):
    recipe_id = sample_recipe.id
    update_data = {
        "name": "Обновленный рецепт",
        "cooking_time": 60,
        "ingredients": "Новые ингредиенты",
        "description": "Новое описание"
    }
    
    response = client.put(f"/recipes/{recipe_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["cooking_time"] == update_data["cooking_time"]


def test_delete_recipe(client: TestClient, sample_recipe):
    recipe_id = sample_recipe.id
    
    response = client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 404


def test_get_recipes_pagination(client: TestClient):
    for i in range(10):
        client.post("/recipes/", json={
            "name": f"Рецепт {i}",
            "cooking_time": 30,
            "ingredients": f"Ингредиенты {i}",
            "description": f"Описание {i}"
        })
    
    response = client.get("/recipes/?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    
    response = client.get("/recipes/?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
