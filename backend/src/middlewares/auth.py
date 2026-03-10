from fastapi import FastAPI, HTTPException, Request, Depends, Response
from fastapi.responses import JSONResponse
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import BaseRoute
from starlette.types import ASGIApp
from repositories import user as cuser, session_token as ctoken
from errors import errors
from src.db_connection import get_db
from src.models.user import UserToken

db = get_db()

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
            return res
        try:
            user = await cuser.get_user_with_session_token(session_token, db)
            await cuser.is_logged_in(user.id, db)
            req.state.user = {"id": user.id, "username": user.username, "picture": user.picture}
            return await call_next(req)
        
        except (errors.SessionNotFoundError, errors.SessionExpiredError) as e:
            res = JSONResponse(
                status_code=401,
                content={"detail": e.message}
            )
            res.delete_cookie("session_token")
            return res