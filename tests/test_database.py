import pytest
from sqlalchemy import inspect

from database import engine, Base, create_tables, drop_tables


@pytest.mark.asyncio
async def test_create_tables():
    await create_tables()
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "recipes" in tables


@pytest.mark.asyncio
async def test_drop_tables():
    await create_tables()
    await drop_tables()
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "recipes" not in tables
