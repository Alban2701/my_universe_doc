from fastapi import FastAPI, HTTPException, Response, status, Request
from models.user import User, InputUser, PartialUser, LoginUser
import controller.user as cuser
import controller.session_token as ctoken
from db_connection import DbConnection
from contextlib import asynccontextmanager
from pwdlib import PasswordHash
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict


db = DbConnection()

@asynccontextmanager
async def lifespan(app: FastAPI):
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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: InputUser):
    """
    signup the user
    
    Parameters:
    - user(InputUser): the user to register
    """
    hasher = PasswordHash.recommended()
    user.password = hasher.hash(user.password)
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
    hasher = PasswordHash.recommended()
    user: PartialUser = await cuser.get_user_by_email(credentials.email, db)
    password = user.password

    if not hasher.verify(credentials.password, password):
        raise HTTPException(401, "wrong password")
    else:
        session = await ctoken.create_session_token(user["id"], db)
        response.set_cookie(
            key="session_token",
            value=session["value"],
            httponly=True,
            samesite="lax",
            secure=False,
            max_age=3600,               
        )

@app.get("/me", status_code=status.HTTP_200_OK)
async def me(req: Request):
    cookies = req.cookies
    session_token = cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="not authenticated")
    print("cookies :", session_token)
    user = await cuser.get_user_with_session_token(session_token, db)
    return user