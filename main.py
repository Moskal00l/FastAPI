from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import create_tables, get_db
from models import RecipeDB
from schemas import RecipeCreate, RecipeDetail, RecipeList

app = FastAPI(
    title="Кулинарная книга API (Async Modular)",
    description="Модульная async версия. /docs для Swagger.",
    version="3.0.0",
)


@app.on_event("startup")
async def startup() -> None:
    await create_tables()


@app.get("/recipes/", response_model=List[RecipeList])
async def get_recipes(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
) -> List[RecipeList]:

    result = await db.execute(
        select(RecipeDB)
        .order_by(RecipeDB.views.desc(), RecipeDB.cooking_time.asc())
        .offset(skip)
        .limit(limit)
    )
    recipes = result.scalars().all()
    return [RecipeList.from_orm(r) for r in recipes]


@app.get("/recipes/{recipe_id}", response_model=RecipeDetail)
async def get_recipe_detail(
    recipe_id: int, db: AsyncSession = Depends(get_db)
) -> RecipeDetail:

    await db.execute(
        update(RecipeDB)
        .where(RecipeDB.id == recipe_id)
        .values(views=RecipeDB.views + 1)
    )
    await db.commit()

    result = await db.execute(select(RecipeDB).where(RecipeDB.id == recipe_id))
    recipe = result.scalar_one_or_none()

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Рецепт не найден"
        )

    return RecipeDetail.from_orm(recipe)


@app.post("/recipes/", response_model=RecipeDetail, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe: RecipeCreate, db: AsyncSession = Depends(get_db)
) -> RecipeDetail:
    if recipe.cooking_time <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Время приготовления должно быть больше 0",
        )

    db_recipe = RecipeDB(**recipe.dict(), views=0)
    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)

    return RecipeDetail.from_orm(db_recipe)


@app.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)) -> None:
    result = await db.execute(select(RecipeDB).where(RecipeDB.id == recipe_id))
    recipe = result.scalar_one_or_none()

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Рецепт не найден"
        )

    await db.delete(recipe)
    await db.commit()


@app.get("/")
async def root() -> dict:
    return {"message": "Модульная Async API. /docs"}
