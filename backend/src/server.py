from fastapi import FastAPI, HTTPException, Response, status, Request
from models.user import User, InputUser, PartialUser, LoginUser
import controller.user as cuser
import controller.session_token as ctoken
from db_connection import DbConnection
from contextlib import asynccontextmanager
from pwdlib import PasswordHash
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from router.user import user_router
from src.db_connection import get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db()
    await db.connect()
    yield
    await db.close()

app = FastAPI(title="My Universe Doc", lifespan=lifespan)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],   
)

app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


