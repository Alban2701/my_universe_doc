import traceback

from fastapi import HTTPException, status
from typing import Optional

from src.models.user import InputUser, LoginUser, PartialUser, User, UserToken
from src.services.user import UserService

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def register(self, user: InputUser) -> PartialUser:
        try:
            return await self.user_service.register(user)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def login(self, credentials: LoginUser) -> str:
        try:
            return await self.user_service.login(credentials)
        except HTTPException:
            raise  # Re-lève l'erreur HTTP existante
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def logout(self, user_id: int) -> None:
        try:
            await self.user_service.logout(user_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_current_user(self, token_value: str) -> UserToken:
        try:
            return await self.user_service.get_current_user(token_value)
        except HTTPException:
            raise  # Re-lève l'erreur HTTP existante
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def is_logged_in(self, user_id: int) -> bool:
        try:
            return await self.user_service.is_logged_in(user_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_user_by_id(self, user_id: int) -> Optional[PartialUser]:
        try:
            return await self.user_service.get_user_by_id(user_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_user_by_email(self, email: str) -> Optional[PartialUser]:
        try:
            return await self.user_service.get_user_by_email(email)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_user_admin_rights(self, user_id: int, universe_id: int) -> Optional[str]:
        try:
            return await self.user_service.get_user_admin_rights(user_id, universe_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def is_super_admin_in(self, user_id: int, universe_id: int) -> bool:
        try:
            return await self.user_service.is_super_admin(user_id, universe_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def patch_user(self, user_id: int, user_patch: PartialUser) -> User | None:
        try:
            return await self.user_service.patch_user(user_id, user_patch)
        except Exception as e:
            print(traceback.format_exc())
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def get_user_with_session_token(self, token_value) -> UserToken | None:
        try:
            return await self.user_service.get_user_with_session_token(token_value)
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))