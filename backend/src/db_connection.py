import psycopg as pg
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv
import os
from typing import Any, Sequence, Mapping

class Db_connection():
    host: str
    port: int
    db_name: str
    db_username: str
    password: str
    conninfo: str
    pool: pg.AsyncConnection

    def __init__(self):
        load_dotenv()
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.db_name = os.getenv("DATABASE_NAME")
        self.db_username = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.conninfo = f"host={self.host} port={self.port} dbname={self.db_name} user={self.db_username} password={self.password}"
        self.pool = AsyncConnectionPool(self.conninfo)
    
    async def execute(self, query: str, params: Sequence[Any] | Mapping[str, Any] | None = None):
        async with self.pool.connection() as conn:
            conn: pg.AsyncConnection
            async with conn.cursor() as cur:
                cur: pg.AsyncCursor
                try:
                    await cur.execute(query, params)
                    await conn.commit()
                except Exception:
                    await conn.rollback()
                    raise