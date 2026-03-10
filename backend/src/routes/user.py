from fastapi import APIRouter, HTTPException, Response, status, Request, Depends
from models.user import InputUser, PartialUser, LoginUser
import repositories.user as ruser
import repositories.session_token as ctoken
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
    hasher = PasswordHash.recommended() # argon2i
    user.password = hasher.hash(user.password)
    res = await ruser.register(user, db=db)
    return res

@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login(credentials: LoginUser, response: Response, db: DbConnection=Depends(get_db)):
    """
    login the user
    
    Parameters:
    - email(EmailStr): the user's email
    - password(str): the user's password
    """
    hasher = PasswordHash.recommended()
    option_user = await ruser.get_user_by_email(credentials.email, db)
    if option_user is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        user = option_user
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
async def me(req: Request):
    user = req.state.user
    return user

@user_router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(req: Request, db: DbConnection=Depends(get_db)):
    user = PartialUser.model_validate(req.state.user)
    await ctoken.delete_session_token(db, user.id)
    res = Response({"message": "logout successful"}, status_code=status.HTTP_200_OK)
    res.delete_cookie('session_token', httponly=True, samesite="lax", secure=False)
    return res