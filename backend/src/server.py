import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db_connection import get_db
from factory import get_factory
from middlewares.auth import AuthMiddleware
from routes.entity import entity_router
from routes.text_block import text_block_router
from routes.universe import universe_router
from routes.user import user_router
from src.tasks.purge_tokens import purge_expired_tokens


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db()
    await db.connect()
    purge_task = asyncio.create_task(
        purge_expired_tokens(get_factory().session_repository)
    )
    try:
        yield
    finally:
        purge_task.cancel()
        try:
            await purge_task  # Laisse la tache se terminer tranquillement avant la fermeture du serveur
        except asyncio.CancelledError:
            pass
        await db.close()


app = FastAPI(title="My Universe Doc", lifespan=lifespan)

app.include_router(user_router)
app.include_router(universe_router)
app.include_router(entity_router)
app.include_router(text_block_router)

if os.getenv("IN_DEV"):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173/", "http://localhost:5174/"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(
    AuthMiddleware,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
