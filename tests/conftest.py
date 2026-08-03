import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database import Base, get_db
from main import app
from models import RecipeDB

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

TestAsyncSessionLocal = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
)


async def override_get_db():
    """Override database dependency for testing."""
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
async def db():
    """Create test database with tables."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestAsyncSessionLocal() as session:
        yield session
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client():
    """Create async test client."""
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest.fixture(scope="function")
async def sample_recipe(db):
    """Create sample recipe for testing."""
    recipe = RecipeDB(
        name="Тестовый рецепт",
        cooking_time=30,
        ingredients="Мука, яйца, сахар",
        description="Вкусный десерт",
        views=0
    )
    db.add(recipe)
    await db.commit()
    await db.refresh(recipe)
    return recipe
