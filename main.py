from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, create_tables
from models import RecipeDB
from schemas import RecipeList, RecipeCreate, RecipeDetail

app = FastAPI(
    title="Кулинарная книга API (Async Modular)",
    description="Модульная async версия. /docs для Swagger.",
    version="3.0.0"
)



@app.on_event("startup")
async def startup():
    await create_tables()


@app.get("/recipes/", response_model=list[RecipeList])
async def get_recipes(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """
    Таблица для 1-го экрана. Сортировка: views↓, cooking_time↑.
    """
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
        recipe_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Детали для 2-го экрана. Авто views += 1.
    """
    result = await db.execute(
        select(RecipeDB).where(RecipeDB.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()

    if recipe is None:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    recipe.views += 1
    await db.flush()

    return RecipeDetail.from_orm(recipe)


@app.post("/recipes/", response_model=RecipeDetail, status_code=201)
async def create_recipe(
        recipe: RecipeCreate,
        db: AsyncSession = Depends(get_db)
):
    """
    Новый рецепт. Валидация: cooking_time > 0.
    """
    if recipe.cooking_time <= 0:
        raise HTTPException(400, "Время приготовления > 0")

    db_recipe = RecipeDB(**recipe.dict(), views=0)
    db.add(db_recipe)
    await db.flush()

    return RecipeDetail.from_orm(db_recipe)



@app.get("/")
async def root():
    return {"message": "Модульная Async API. /docs"}