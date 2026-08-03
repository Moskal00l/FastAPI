from models import RecipeDB


def test_recipe_creation():
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
    assert recipe.views == 0

def test_recipe_repr():
    recipe = RecipeDB(
        id=1,
        name="Тестовый рецепт",
        cooking_time=30,
        ingredients="Ингредиенты",
        description="Описание",
        views=10
    )
    
    repr_str = repr(recipe)
    assert "RecipeDB" in repr_str
    assert "id=1" in repr_str
    assert "views=10" in repr_str


def test_recipe_to_dict():
    """Test recipe to_dict method."""
    recipe = RecipeDB(
        id=1,
        name="Тестовый рецепт",
        cooking_time=30,
        ingredients="Ингредиенты",
        description="Описание",
        views=10
    )
    
    assert hasattr(recipe, 'to_dict')
    recipe_dict = recipe.to_dict()
    assert isinstance(recipe_dict, dict)
    assert recipe_dict["id"] == 1
    assert recipe_dict["name"] == "Тестовый рецепт"
    assert recipe_dict["cooking_time"] == 30
    assert recipe_dict["views"] == 10
