import psycopg as pg
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv
import os
from typing import Any, Sequence, Mapping
from psycopg.rows import dict_row

class DbConnection():
    host: str
    port: int
    db_name: str
    db_username: str
    password: str
    conninfo: str
    pool: AsyncConnectionPool

    def __init__(self):
        load_dotenv()
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.db_name = os.getenv("DATABASE_NAME")
        self.db_username = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.conninfo = f"host={self.host} port={self.port} dbname={self.db_name} user={self.db_username} password={self.password}"

    async def connect(self):
        """
        startup de database connection
        
        """
        self.pool = AsyncConnectionPool(self.conninfo)
        return
    
    async def close(self):
        """
        close de database connection
        
        """
        await self.pool.close()
        return
    
    
    async def execute(self, query: str, params: Sequence[Any] | Mapping[str, Any] | None = None):
        async with self.pool.connection() as conn:
            conn: pg.AsyncConnection
            async with conn.cursor(row_factory=dict_row) as cur:
                cur: pg.AsyncCursor
                try:
                    await cur.execute(query, params)
                    if cur.description:
                        rows = await cur.fetchall()
                        await conn.commit()
                        return rows
                    
                    await conn.commit()
                    return None
                except Exception:
                    await conn.rollback()
                    raise

db = DbConnection()