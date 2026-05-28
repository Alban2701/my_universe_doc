import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from dotenv import load_dotenv
import psycopg
import os
import sys
from psycopg.rows import dict_row
from typing import cast, LiteralString
import platform

# Aliase src.db_connection et db_connection vers le MÊME module
# (le code de prod importe sans préfixe, les tests avec — sinon deux _db distincts)
import src.db_connection
sys.modules["db_connection"] = sys.modules["src.db_connection"]

from src.server import app  # ton app FastAPI
from src.db_connection import DbConnection, get_db
import src.db_connection as db_module

if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# ------------------------------------------------------------------ #
# 1. Pool de test — créé une seule fois pour toute la session pytest  #
# ------------------------------------------------------------------ #
@pytest_asyncio.fixture(scope="session")
async def test_db():
    db = DbConnection(".env.test")
    await db.connect()
    original_db = db_module._db
    db_module._db = db
    yield db
    db_module._db = original_db
    await db.close()


# ------------------------------------------------------------------ #
# 2. Remise à zéro avant chaque test                                  #
# ------------------------------------------------------------------ #
@pytest_asyncio.fixture(autouse=True)
async def reset_db(test_db: DbConnection):
    conninfo = test_db.conninfo  # on réutilise le conninfo déjà construit

    async with await psycopg.AsyncConnection.connect(conninfo) as conn:
        # Truncate — adapte à tes vraies tables
        await conn.execute(
            "TRUNCATE TABLE users, universe, text_blocks, entities, user_entity,"
            " comments, commits, invitations, user_universe RESTART IDENTITY CASCADE"
        )
        # Reseed avec le contenu de 99.sql
        seed_path = os.path.join("src", "data", "99.sql")
        with open(seed_path, "r") as f:
            seed_sql = f.read()
        await conn.execute(cast(LiteralString, seed_sql))
        await conn.commit()

    yield


# ------------------------------------------------------------------ #
# 3. Client HTTP avec injection de la DB de test                      #
# ------------------------------------------------------------------ #
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
