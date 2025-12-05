from fastapi import FastAPI, HTTPException, Response
from models.user import User, InputUser, PartialUser, LoginUser
import controller.user as cuser
import controller.session_token as ctoken
from db_connection import DbConnection
from contextlib import asynccontextmanager
from pwdlib import PasswordHash


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
    user = await cuser.get_user_by_email(credentials.email, db)
    if len(user) == 0:
        raise HTTPException(404, "user not found")
    else:
        password = user[2]

        if not hasher.verify_and_update(password, credentials.password):
            raise HTTPException(401, "wrong password")
        else:
            session = await ctoken.create_session_token(user[0], db)
            response.set_cookie("session_token", session[1], session[5])

    return