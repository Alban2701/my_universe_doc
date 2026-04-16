from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import user_router
from routes.universe import universe_router
from routes.entity import entity_router
from db_connection import get_db
import os
from middlewares.auth import AuthMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db()
    await db.connect()
    yield
    await db.close()

app = FastAPI(title="My Universe Doc", lifespan=lifespan)

app.include_router(user_router)
app.include_router(universe_router)
app.include_router(entity_router)

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


