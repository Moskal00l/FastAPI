from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import create_tables, get_db
from models import RecipeDB
from schemas import RecipeCreate, RecipeDetail, RecipeList


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""

    await create_tables()
    yield



app = FastAPI(
    title="Кулинарная книга API (Async Modular)",
    description="Модульная async версия. /docs для Swagger.",
    version="3.0.0",
    lifespan=lifespan,
)


@app.get("/recipes/", response_model=List[RecipeList])
async def get_recipes(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> List[RecipeList]:
    """
    Получить список рецептов для главного экрана.
    Сортировка: по просмотрам (убывание), затем по времени готовки (возрастание).
    """
    result = await db.execute(
        select(RecipeDB)
        .order_by(RecipeDB.views.desc(), RecipeDB.cooking_time.asc())
        .offset(skip)
        .limit(limit)
    )
    recipes = result.scalars().all()
    return [RecipeList.model_validate(r) for r in recipes]


@app.get("/recipes/{recipe_id}", response_model=RecipeDetail)
async def get_recipe_detail(
    recipe_id: int,
    db: AsyncSession = Depends(get_db),
) -> RecipeDetail:
    """
    Получить детальную информацию о рецепте.
    Автоматически увеличивает счетчик просмотров на 1.
    """
    # Атомарное обновление просмотров
    await db.execute(
        update(RecipeDB)
        .where(RecipeDB.id == recipe_id)
        .values(views=RecipeDB.views + 1)
    )
    await db.commit()

    # Получаем обновленный рецепт
    result = await db.execute(select(RecipeDB).where(RecipeDB.id == recipe_id))
    recipe = result.scalar_one_or_none()

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рецепт не найден",
        )

    return RecipeDetail.model_validate(recipe)


@app.post("/recipes/", response_model=RecipeDetail, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe: RecipeCreate,
    db: AsyncSession = Depends(get_db),
) -> RecipeDetail:
    """
    Создать новый рецепт.
    """
    if recipe.cooking_time <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Время приготовления должно быть больше 0",
        )

    # Используем model_dump() вместо dict() (Pydantic V2)
    db_recipe = RecipeDB(**recipe.model_dump(), views=0)
    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)

    return RecipeDetail.model_validate(db_recipe)


@app.put("/recipes/{recipe_id}", response_model=RecipeDetail)
async def update_recipe(
    recipe_id: int,
    recipe_update: RecipeCreate,
    db: AsyncSession = Depends(get_db),
) -> RecipeDetail:
    """
    Обновить рецепт.
    """
    result = await db.execute(select(RecipeDB).where(RecipeDB.id == recipe_id))
    recipe = result.scalar_one_or_none()

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рецепт не найден",
        )

    # Обновляем поля
    recipe.name = recipe_update.name
    recipe.cooking_time = recipe_update.cooking_time
    recipe.ingredients = recipe_update.ingredients
    recipe.description = recipe_update.description

    await db.commit()
    await db.refresh(recipe)

    return RecipeDetail.model_validate(recipe)


@app.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Удалить рецепт."""
    result = await db.execute(select(RecipeDB).where(RecipeDB.id == recipe_id))
    recipe = result.scalar_one_or_none()

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рецепт не найден",
        )

    await db.delete(recipe)
    await db.commit()


@app.get("/")
async def root() -> dict:
    """Корневой эндпоинт."""
    return {"message": "Модульная Async API. /docs"}
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe
