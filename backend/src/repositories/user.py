from src.utils.unoptional import unoptional
import traceback
from typing import Optional

from models.user import User, InputUser, PartialUser, UserToken
from pydantic import EmailStr
from models.user import PartialUser
from errors import errors
from src.models.enums import UserUniverseRole
from src.repositories.base_repository import BaseRepository
from src.repositories.session_token import SessionTokenRepository


class UserRepository(BaseRepository):
    def __init__(self, session_token_repository: SessionTokenRepository):
        super().__init__()
        self.session_token_repository = session_token_repository

    async def register(self, user: InputUser) -> PartialUser:
        """
        register a new user in the database

        Parameters:
        - user: the user to register

        Returns:
        User: the user registered
        """
        sql = (
            "INSERT INTO users (email, password, username, bio, picture)"
            " VALUES (%(email)s, %(password)s, %(username)s, %(bio)s, %(picture)s)"
            " RETURNING id, username, email"
        )
        model_user = user.model_dump()
        print(model_user)
        rows = unoptional(await self.db.execute(sql, model_user))
        returned_user = PartialUser.model_validate(rows[0])
        return returned_user

    async def get_user_by_id(self, id: int) -> Optional[PartialUser]:
        """
        get a user in database with the provided id

        Parameters:
        - id (int): the id of the user to be get

        Returns:
        User: the user get
        """
        sql = (
            "SELECT id, email, username, bio, picture, created_at, updated_at"
            " FROM users WHERE id = %(id)s"
        )
        rows = await self.db.execute(sql, {"id": id})
        if rows is None or len(rows) == 0:
            return None
        returned_user = PartialUser.model_validate(rows[0])
        return returned_user

    async def get_user_by_email(self, email: EmailStr) -> Optional[PartialUser]:
        """
        get a user in database with the provided email

        Parameters:
        - email (EmailStr): the email of the user to be get

        Returns:
        User: the user get
        """
        sql = "SELECT * from users WHERE email = %(email)s"
        rows = await self.db.execute(sql, {"email": email})
        if rows is None or len(rows) == 0:
            return None
        returned_user = PartialUser.model_validate(rows[0])
        return returned_user

    async def get_user_with_session_token(
        self, token_value: str
    ) -> Optional[UserToken]:
        """
        take a session_token_value and return a user thanks to it

        Parameters:
        - session_token(str): the value of the session_token

        Returns:
        User: The user get
        """
        sql = (
            "SELECT u.* from users as u "
            "JOIN session_token as s "
            "ON s.user_id = u.id "
            "WHERE s.value = %(token_value)s"
        )
        params = {"token_value": token_value}
        rows = await self.db.execute(sql, params)
        if rows is None or len(rows) == 0:
            return None

        returned_user = UserToken.model_validate(rows[0])
        return returned_user

    async def is_logged_in(self, user_id: int) -> bool:
        """
        Check if a user is logged in

        Parameters:
        -   user_id: the id of the user
        -   db: the db object

        Returns:
        bool: True if the user is connected, False otherwise
        """

        try:
            token = await self.session_token_repository.get_token_by_user_id(
                user_id=user_id
            )
            return bool(token)
        except Exception as e:
            raise e

    async def get_user_admin_rights(
        self, user_id: int, universe_id: int
    ) -> UserUniverseRole | None:
        """
        Get the role of the user in an universe if exists

        Parameters:
        - user_id (int): the user's id
        - universe_id (int): the universe's id
        - db: the db's pool

        Returns:
        UserUniverseRole | None: If the user has a role in the universe, then the functions returns it, else, it returns None
        """

        sql = (
            "SELECT admin_role FROM user_universe "
            "WHERE user_id=%(user_id)s "
            "AND universe_id=%(universe_id)s"
        )
        params = {"user_id": user_id, "universe_id": universe_id}
        rows = await self.db.execute(sql, params)
        if rows is None or len(rows) == 0:
            return None
        return UserUniverseRole(rows[0])

    async def patch_user(
        self, user_id: int, user_patch: PartialUser
    ) -> PartialUser | None:
        sql = (
            "UPDATE users SET "
            "email = COALESCE(%(email)s, email), "
            "password = COALESCE(%(password)s, password), "
            "bio = COALESCE(%(bio)s, bio), "
            "picture = COALESCE(%(picture)s, picture), "
            "updated_at = NOW() "
            "WHERE id = %(id)s "
            "RETURNING id, username, email, bio, created_at, updated_at"
        )
        model_patch = user_patch.model_dump()
        model_patch["id"] = user_id
        print(model_patch)
        rows = await self.db.execute(sql, model_patch)
        print(f"rows: {rows}")
        if not rows:
            return None
        returned_user = PartialUser.model_validate(rows[0])

        return returned_user
