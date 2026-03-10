from fastapi import FastAPI, HTTPException, Response, status, Request
from models.user import User, InputUser, PartialUser, LoginUser
import repositories.user as ruser
import repositories.session_token as ctoken
from db_connection import DbConnection
from contextlib import asynccontextmanager
from pwdlib import PasswordHash
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from routes.user import user_router
from src.db_connection import get_db
from middlewares.auth import AuthMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db()
    await db.connect()
    yield
    await db.close()

app = FastAPI(title="My Universe Doc", lifespan=lifespan)

app.include_router(user_router)

app.add_middleware(
    AuthMiddleware,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


