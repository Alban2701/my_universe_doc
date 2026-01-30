from fastapi import APIRouter, FastAPI, HTTPException, Response, status, Request, Depends
from models.user import InputUser, PartialUser, LoginUser
import controller.user as cuser
import controller.session_token as ctoken
from pwdlib import PasswordHash
from src.db_connection import DbConnection, get_db

user_router = APIRouter(prefix="/user")

@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: InputUser, db: DbConnection=Depends(get_db)):
    """
    signup the user
    
    Parameters:
    - user(InputUser): the user to register
    """
    hasher = PasswordHash.recommended()
    user.password = hasher.hash(user.password)
    res = await cuser.register(user, db=db)
    return res

@user_router.post("/login")
async def login(credentials: LoginUser, response: Response, db: DbConnection=Depends(get_db)):
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
        session = await ctoken.create_session_token(user.id, db)
        response.set_cookie(
            key="session_token",
            value=session.value,
            httponly=True,
            samesite="lax",
            secure=False,
            max_age=3600,               
        )
        return {"message": "login successful"}

@user_router.get("/me", status_code=status.HTTP_200_OK)
async def me(req: Request, db: DbConnection=Depends(get_db)):
    cookies = req.cookies
    session_token = cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="not authenticated")
    print("cookies :", session_token)
    user = await cuser.get_user_with_session_token(session_token, db)
    return user