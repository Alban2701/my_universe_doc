from fastapi import FastAPI
from models.user import User, InputUser, PartialUser
from db_connection import DbConnection
from contextlib import asynccontextmanager


db = DbConnection()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.close()

app = FastAPI(title="My Universe Doc")
app.state.db = db

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/signup")
async def signup(user: User):
    """
    signup the user
    
    Parameters:
    - user: the user to register
    """
    
    return