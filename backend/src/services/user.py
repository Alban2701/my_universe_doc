from models.user import User, InputUser, PartialUser, UserToken, LoginUser
from repositories.user import UserRepository
from repositories.session_token import SessionTokenRepository
from pwdlib import PasswordHash
from fastapi import HTTPException, status
from typing import Dict, Optional

from src.models.enums import UserUniverseRole

class UserService:
    def __init__(self, user_repository: UserRepository, session_token_repository: SessionTokenRepository):
        self.user_repository = user_repository
        self.session_token_repository = session_token_repository
        self.hasher = PasswordHash.recommended()

    async def register(self, user: InputUser) -> PartialUser:
        """
        Register a new user in the database, hashing the password before saving.

        Parameters:
        - user: InputUser with email, password, username, bio, picture

        Returns:
        PartialUser: the registered user (without sensitive data)
        """
        user.password = self.hasher.hash(user.password)
        return await self.user_repository.register(user)

    async def login(self, credentials: LoginUser) -> str:
        """
        Authenticate a user and create a session token.

        Parameters:
        - credentials: LoginUser with email and password

        Returns:
        str: the session token value

        Raises:
        HTTPException: if email not found or password is wrong
        """
        user = await self.user_repository.get_user_by_email(credentials.email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if not self.hasher.verify(credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")

        session = await self.session_token_repository.create_session_token(user.id)
        return session.value
    
    async def patch_user(self, user_id: int, user_patch: PartialUser) -> User | None:
        if user_patch.password:
            user_patch.password = self.hasher.hash(user_patch.password)

        user = await self.user_repository.patch_user(user_id, user_patch)
        return user

    async def logout(self, user_id: int) -> None:
        """
        Delete the session token for the given user.

        Parameters:
        - user_id: the id of the user to logout
        """
        await self.session_token_repository.delete_session_token(user_id=user_id)

    async def get_current_user(self, token_value: str) -> UserToken:
        """
        Get the current user from a session token.

        Parameters:
        - token_value: the session token value

        Returns:
        UserToken: the user associated with the token

        Raises:
        HTTPException: if token is not found or expired
        """
        return await self.user_repository.get_user_with_session_token(token_value)

    async def is_logged_in(self, user_id: int) -> bool:
        """
        Check if a user is currently logged in.

        Parameters:
        - user_id: the id of the user

        Returns:
        bool: True if the user has an active session, False otherwise
        """
        try:
            token = await self.session_token_repository.get_token_by_user_id(user_id)
            return token is not None
        except Exception:
            return False

    async def get_user_by_id(self, user_id: int) -> Optional[PartialUser]:
        """
        Get a user by their id.

        Parameters:
        - user_id: the id of the user

        Returns:
        PartialUser or None: the user if found, None otherwise
        """
        return await self.user_repository.get_user_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[PartialUser]:
        """
        Get a user by their email.

        Parameters:
        - email: the email of the user

        Returns:
        PartialUser or None: the user if found, None otherwise
        """
        return await self.user_repository.get_user_by_email(email)

    async def get_user_admin_rights(self, user_id: int, universe_id: int) -> Optional[Dict[str, UserUniverseRole]]:
        """
        Get the admin role of a user in a specific universe.

        Parameters:
        - user_id: the id of the user
        - universe_id: the id of the universe

        Returns:
        UserUniverseRole or None: the admin role if exists, None otherwise
        """
        return await self.user_repository.get_user_admin_rights(user_id, universe_id)
    
    async def is_super_admin(self, user_id: int, universe_id: int) -> bool:
        """
        Returns:
        - True if the user is super admin
        - False otherwise
        
        Parameters:
        - user_id: the user's id
        - universe_id: the universe's id
        """
        rights = await self.user_repository.get_user_admin_rights(user_id, universe_id)
        if not rights:
            return False
        return True
    
    async def get_user_with_session_token(self, token_value: str) -> UserToken | None:
        user_token = await self.user_repository.get_user_with_session_token(token_value)
        return user_token