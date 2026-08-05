"""Pytest configuration and fixtures for async tests."""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Column, Integer, String, Text, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.database import get_db
from app.main import app

# Создаем отдельную MetaData и Base для тестов
test_metadata = MetaData()
TestBase = declarative_base(metadata=test_metadata)


class TestRecipeDB(TestBase):
    """Test recipe model with isolated metadata."""
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cooking_time = Column(Integer)
    ingredients = Column(Text)
    description = Column(Text)
    views = Column(Integer, default=0)


# Тестовая база данных (асинхронная, в памяти)
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
async def setup_database():
    """Create and drop test database tables."""
    # Создаем таблицы
    async with test_engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.create_all)
    yield
    # Удаляем таблицы после теста
    async with test_engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(setup_database):
    """Create async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def sample_recipe(setup_database):
    """Create sample recipe for testing."""
    async with TestAsyncSessionLocal() as db:
        recipe = TestRecipeDB(
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