import traceback

import psycopg as pg
from psycopg.sql import SQL
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv
import os
from typing import Any, List, LiteralString, Sequence, Mapping
from psycopg.rows import dict_row, DictRow
from src.utils.unoptional import unoptional


class DbConnection:
    host: str
    port: int
    db_name: str
    db_username: str
    password: str
    conninfo: str
    pool: AsyncConnectionPool

    def __init__(self, env_path: str | None = None):
        try:
            load_dotenv(env_path, override=True)
            self.port = int(unoptional(os.getenv("POSTGRES_PORT", 5432), "db_port"))
            self.host = unoptional(os.getenv("POSTGRES_HOST"), "db_host")
            self.db_name = unoptional(os.getenv("DATABASE_NAME"), "db_name")
            self.db_username = unoptional(os.getenv("POSTGRES_USER"), "db_user")
            self.password = unoptional(os.getenv("POSTGRES_PASSWORD"), "db_password")
            self.conninfo = f"host={self.host} port={self.port} dbname={self.db_name} user={self.db_username} password={self.password}"
            print(self.conninfo)

        except Exception:
            print(traceback.format_exc())
            raise Exception

    async def connect(self):
        """
        startup de database connection

        """
        self.pool = AsyncConnectionPool(
            self.conninfo,
            min_size=1,
            max_size=10,
            timeout=30,
            open=False,
        )  # type: ignore
        await self.pool.open()
        await self.pool.wait()

    async def close(self):
        """
        close de database connection

        """
        await self.pool.close()
        print("Connection pool closed")
        return

    async def execute(
        self,
        query: LiteralString | SQL,
        params: Sequence[Any] | Mapping[str, Any] | None = None,
    ):
        if self.pool is None:
            raise RuntimeError("Database not connected.")

        async with self.pool.connection() as conn:
            conn: pg.AsyncConnection
            cur: pg.AsyncCursor[DictRow]
            async with conn.cursor(row_factory=dict_row) as cur:
                try:
                    await cur.execute(query, params)
                    if cur.description:
                        rows = await cur.fetchall()
                        await conn.commit()
                        return rows

                    await conn.commit()
                    return None
                except Exception as e:
                    await conn.rollback()
                    raise RuntimeError(f"SQL Error: {str(e)}")

    async def execute_many(self, query, params: List[Any]):
        if self.pool is None:
            raise RuntimeError("Database not connected.")

        async with self.pool.connection() as conn:
            conn: pg.AsyncConnection
            cur: pg.AsyncCursor[DictRow]
            async with conn.cursor(row_factory=dict_row) as cur:
                try:
                    await cur.executemany(query, params, returning=True)
                    if cur.description:
                        rows = await cur.fetchall()
                        await conn.commit()
                        return rows

                    await conn.commit()
                    return None

                except Exception as e:
                    await conn.rollback()
                    raise RuntimeError(f"SQL Error: {str(e)}")


_db = DbConnection()


def get_db() -> DbConnection:
    return _db
