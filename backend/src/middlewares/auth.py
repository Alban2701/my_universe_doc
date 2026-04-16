from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from repositories import user as cuser
from errors import errors
from src.factory import get_factory
from src.models.user import UserToken

factory = get_factory()
user_controller = factory.user_controller


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, req: Request, call_next):
        """
        Check if the user is logged in. 
        """

        public_paths = {
            "/",
            "/user/login",
            "/user/signup",
            "/docs",
            "/openapi.json"
        }

        if req.url.path in public_paths:
            return await call_next(req)
        
        session_token = req.cookies.get("session_token")
        if not session_token:
            res = JSONResponse(
                status_code=401,
                content={"detail": "session not initialized"}
            )
            print(res.body)
            return res
        try:
            user: UserToken = await user_controller.get_user_with_session_token(session_token)
            logged_in = await user_controller.is_logged_in(user.id)
            if logged_in:
                req.state.user = user
                return await call_next(req)
            
            else:
                res = JSONResponse(
                status_code=401,
                content={"detail": "user not connected"}
            )
                res.delete_cookie("session_token")
                print(res.body)
                return res
        
        except (errors.SessionNotFoundError, errors.SessionExpiredError) as e:
            
            res = JSONResponse(
                status_code=401,
                content={"detail": e.message}
            )
            res.delete_cookie("session_token")
            print(res.body)
            return res
        
        except Exception as e:
            res = JSONResponse(
                status_code=500,
                content={"detail": "An server error occured"}
            )
            print(e)
            print(res.body)
            return res