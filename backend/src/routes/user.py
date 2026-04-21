from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from models.user import InputUser, LoginUser, PartialUser, User, UserToken
from controllers.user import UserController
from factory import get_factory
import traceback

from db_connection import get_db

user_router = APIRouter(prefix="/user")

factory = get_factory()
user_controller: UserController = factory.user_controller

@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: InputUser):
    try:
        return await user_controller.register(user)
    except HTTPException:
        print(traceback.format_exc())
        raise
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login(credentials: LoginUser, response: Response):
    try:
        token = await user_controller.login(credentials)
        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,
            samesite="lax",
            secure=False,
            max_age=3600,
        )
        return {"message": "login successful"}
    except HTTPException:
        print(traceback.format_exc())
        raise
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user_router.get("/me", status_code=status.HTTP_200_OK)
async def me(req: Request):
    try:
        user: UserToken = req.state.user
        return await user_controller.get_user_by_id(user.id)
    except HTTPException:
        print(traceback.format_exc())
        raise
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        

@user_router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(request: Request):
    try:
        user: UserToken = request.state.user
        await user_controller.logout(user.id)
        response = Response(status_code=status.HTTP_200_OK)
        response.delete_cookie('session_token', httponly=True, samesite="lax", secure=False)
        return response
    except HTTPException:
        print(traceback.format_exc())
        raise
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@user_router.patch("/myself", status_code=status.HTTP_200_OK)
async def patch_myself(req: Request, user_patch: PartialUser) -> PartialUser:
    try:
        user: UserToken = req.state.user
        patched_user = await user_controller.patch_user(user.id, user_patch)
        if patched_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found with id {user.id}")
        return patched_user
    
    except HTTPException:
        print(traceback.format_exc())
        raise

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@user_router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def patch_user(user_id: int, user_patch: PartialUser) -> PartialUser:
    try:
        patched_user = await user_controller.patch_user(user_id, user_patch)
        if patched_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found with id {user_id}")
        return patched_user
    
    except HTTPException:
        print(traceback.format_exc())
        raise

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        

@user_router.get("/is-superadmin-in/{universe_id}", status_code=status.HTTP_200_OK)
async def is_superadmin_in(universe_id: int, req: Request):
    try: 
        user: UserToken = req.state.user
        return await user_controller.is_super_admin_in(user.id, universe_id)
    except HTTPException:
        print(traceback.format_exc())
        raise
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))