import os
from typing import cast, LiteralString

import psycopg
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.server import app
from src.db_connection import DbConnection, get_db
import src.db_connection as db_module


@pytest_asyncio.fixture(scope="session")
async def test_db():
    db = DbConnection(".env.test")
    await db.connect()
    original_db = db_module._db
    db_module._db = db
    yield db
    db_module._db = original_db
    await db.close()


@pytest_asyncio.fixture(autouse=True)
async def reset_db(test_db: DbConnection):
    conninfo = test_db.conninfo

    async with await psycopg.AsyncConnection.connect(conninfo) as conn:
        await conn.execute(
            "TRUNCATE TABLE users, universe, text_blocks, entities, user_entity,"
            " comments, commits, invitations, user_universe RESTART IDENTITY CASCADE"
        )
        seed_path = os.path.join("src", "data", "99.sql")
        with open(seed_path, "r", encoding="utf-8") as f:
            seed_sql = f.read()
        await conn.execute(cast(LiteralString, seed_sql))
        await conn.commit()

    yield


@pytest_asyncio.fixture
async def client(test_db: DbConnection):
    """
    Client HTTP qui remplace get_db par la DB de test.
    Permet de tester les routes sans toucher la DB de prod/dev.
    """
    app.dependency_overrides[get_db] = lambda: test_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
