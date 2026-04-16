from datetime import datetime, timedelta, timezone
from utils.token_creator import create_token
from db_connection import DbConnection
from models.session_token import SessionToken
from models.user import PartialUser
from errors import errors
from src.repositories.base_repository import BaseRepository

class SessionTokenRepository(BaseRepository):
    async def create_session_token(self, user_id: int, expires_in_days: int = 7, nb_bytes: int = 32) -> SessionToken:
        """
        Create a session token for a user

        Parameters:
        - user_id (int): the id of the user who is logged_in
        - expires_in_days (int): expire time in days
        - nb_bytes (int): number of bytes for the token

        Returns:
        SessionToken: the created session token
        """
        token = create_token(nb_bytes=nb_bytes)
        expires_at = datetime.now() + timedelta(days=expires_in_days)

        sql = ("INSERT INTO session_token (value, user_id, expires_at)"
               " VALUES (%(value)s, %(user_id)s, %(expires_at)s)"
               " RETURNING id, value, user_id, created_at, updated_at, expires_at")
        params = {
            "value": token,
            "user_id": user_id,
            "expires_at": expires_at,
        }
        rows = await self.db.execute(sql, params)
        returned_session = SessionToken.model_validate(rows[0])
        return returned_session

    async def get_token_by_user_id(self, user_id: int) -> SessionToken:
        """
        Get a token thanks to a user_id

        Parameters:
        - user_id (int): the id of the user we are checking

        Returns:
        SessionToken: the session token
        """
        sql = ("SELECT * from session_token WHERE user_id = %(user_id)s;")
        params = {"user_id": user_id}
        rows = await self.db.execute(sql, params)
        if len(rows) == 0:
            raise errors.SessionNotFoundError

        session = SessionToken.model_validate(rows[0])

        if session.expires_at < datetime.now():
            await self.delete_session_token(session_value=session.value)
            raise errors.SessionExpiredError

        return session

    async def update_expires_date_token(self, user_id: int, expires_in_days: int = 7) -> None:
        """
        Update the expire_date of a token

        Parameters:
        - user_id (int): the id of the user we are checking
        - expires_in_days (int): expire time in days
        """
        expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)
        sql = ("UPDATE session_token SET "
               "updated_at = NOW(), "
               "expires_at = %(expires_at)s "
               "WHERE user_id = %(user_id)s;")
        params = {"expires_at": expires_at, "user_id": user_id}
        await self.db.execute(sql, params)
        return

    async def delete_session_token(self, user_id: int | None = None, session_value: str | None = None) -> None:
        """
        Delete a session_token

        Parameters:
        - user_id (int): the user's id who is being disconnected
        - session_value (str): the session token value to delete
        """
        if user_id:
            sql = ("DELETE FROM session_token WHERE user_id = %(user_id)s;")
            params = {"user_id": user_id}
        else:
            sql = ("DELETE FROM session_token WHERE value = %(value)s;")
            params = {"value": session_value}
        await self.db.execute(sql, params)
        return

    async def delete_expired_token(self) -> None:
        """
        Delete every expired session_token
        """
        sql = ("DELETE FROM session_token WHERE expires_at < NOW();")
        await self.db.execute(sql)
        return