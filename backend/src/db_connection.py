import psycopg as pg
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv
import os
from typing import Any, Sequence, Mapping
from psycopg.rows import dict_row

class DbConnection():
    host: str | None
    port: int | None
    db_name: str | None
    db_username: str | None
    password: str | None
    conninfo: str | None
    pool: AsyncConnectionPool | None = None

    def __init__(self):
        load_dotenv()
        self.port = os.getenv("POSTGRES_PORT", 5432)
        self.host = os.getenv("POSTGRES_HOST")
        self.db_name = os.getenv("DATABASE_NAME")
        self.db_username = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.conninfo = f"host={self.host} port={self.port} dbname={self.db_name} user={self.db_username} password={self.password}"
        self.pool = None

    async def connect(self):
        """
        startup de database connection
        
        """
        self.pool = AsyncConnectionPool(
            self.conninfo,
            min_size=1,
            max_size=10,
            timeout=30,
        )
        print("Connection pool successfully initialised")
        print(f"Pool initialisé : {self.pool}")  # Doit afficher <AsyncConnectionPool ...>
        print(f"ID du pool : {id(self.pool)}")  # Doit être le même partout
        return
    
    async def close(self):
        """
        close de database connection
        
        """
        await self.pool.close()
        print("Connection pool closed")
        return
    
    
    async def execute(self, query: str, params: Sequence[Any] | Mapping[str, Any] | None = None):
        if self.pool == None:
            raise RuntimeError("Database not connected. Did you forget to call connect()?")
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
                except Exception as e:
                    await conn.rollback()
                    raise RuntimeError(f"SQL Error: {str(e)}")
    
_db = DbConnection()

def get_db() -> DbConnection:
    return _db