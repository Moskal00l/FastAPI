"""Tests for database module."""

import pytest
from sqlalchemy import inspect

from app.database import engine, Base, create_tables, drop_tables


@pytest.mark.anyio
async def test_create_tables():
    """Test creating tables."""
    await create_tables()

    async with engine.begin() as conn:
        def check_tables(sync_conn):
            inspector = inspect(sync_conn)
            tables = inspector.get_table_names()
            assert "recipes" in tables

        await conn.run_sync(check_tables)


@pytest.mark.anyio
async def test_drop_tables():
    """Test dropping tables."""
    await create_tables()

    async with engine.begin() as conn:
        def check_table_exists(sync_conn):
            inspector = inspect(sync_conn)
            tables = inspector.get_table_names()
            assert "recipes" in tables

        await conn.run_sync(check_table_exists)

    await drop_tables()

    async with engine.begin() as conn:
        def check_table_dropped(sync_conn):
            inspector = inspect(sync_conn)
            tables = inspector.get_table_names()
            assert "recipes" not in tables

        await conn.run_sync(check_table_dropped)