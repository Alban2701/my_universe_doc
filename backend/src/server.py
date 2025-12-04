from fastapi import FastAPI, HTTPException, Response
from models.user import User, InputUser, PartialUser, LoginUser
import controller.user as cuser
from db_connection import DbConnection
from contextlib import asynccontextmanager


db = DbConnection()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.close()

app = FastAPI(title="My Universe Doc", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/signup")
async def signup(user: InputUser):
    """
    signup the user
    
    Parameters:
    - user(InputUser): the user to register
    """
    res = await cuser.register(user, db=db)
    return res

@app.post("/login")
async def login(credentials: LoginUser, response: Response):
    """
    login the user
    
    Parameters:
    - email(EmailStr): the user's email
    - password(str): the user's password
    """
    user = await cuser.get_user_by_email(credentials.email, db)
    if len(user) == 0:
        raise HTTPException(404, "user not found")
    else:
        user = user[0]
        print(user)
        password = user[2]
        print(password)
        print(credentials)
        if password != credentials.password:
            raise HTTPException(401, "wrong password")
    return