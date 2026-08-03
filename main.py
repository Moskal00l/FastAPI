import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app
from models import RecipeDB


# Тестовая база данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def sample_recipe(db):
    """Create sample recipe for testing."""
    recipe = RecipeDB(
        name="Тестовый рецепт",
        cooking_time=30,
        ingredients="Мука, яйца, сахар",
        description="Вкусный десерт",
        views=0
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe
