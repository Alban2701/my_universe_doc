from datetime import datetime, timedelta, timezone
from src.utils.unoptional import unoptional
from utils.token_creator import create_token, hash_token
from models.session_token import SessionToken
from src.repositories.base_repository import BaseRepository


class SessionTokenRepository(BaseRepository):
    async def create_session_token(
        self, user_id: int, expires_in_days: int = 30, nb_bytes: int = 32
    ) -> SessionToken:
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
        hashed_token = hash_token(token)

        sql = (
            "INSERT INTO session_token (value, user_id, expires_at)"
            " VALUES (%(value)s, %(user_id)s, NOW() + MAKE_INTERVAL(days => %(days)s))"
            " RETURNING id, value, user_id, created_at, updated_at, expires_at"
        )
        params = {
            "value": hashed_token,
            "user_id": user_id,
            "days": expires_in_days,
        }
        rows = unoptional(await self.db.execute(sql, params))
        returned_session = SessionToken.model_validate(rows[0])
        returned_session.value = token
        return returned_session

    async def update_expires_date_token(
        self, token: str, expires_in_days: int = 30
    ) -> None:
        """
        Update the expire_date of a token

        Parameters:
        - user_id (int): the id of the user we are checking
        - expires_in_days (int): expire time in days
        """
        sql = (
            "UPDATE session_token SET "
            "updated_at = NOW(), "
            "expires_at = NOW() + MAKE_INTERVAL(days => %(days)s) "
            "WHERE value = %(hash)s AND expires_at > NOW();"
        )
        params = {"days": expires_in_days, "hash": hash_token(token)}
        await self.db.execute(sql, params)
        return

    async def delete_session_token(self, session_value: str) -> None:
        """
        Delete a session_token

        Parameters:
        - user_id (int): the user's id who is being disconnected
        - session_value (str): the session token value to delete
        """
        sql = "DELETE FROM session_token WHERE value = %(value)s;"
        params = {"value": hash_token(session_value)}
        await self.db.execute(sql, params)
        return

    async def delete_all_user_session_token(self, user_id: int) -> None:
        """
        Delete all user's session_token

        Parameters:
        - user_id (int): the user's id who is being disconnected
        """

        sql = "DELETE FROM session_token WHERE user_id = %(user_id)s;"
        params = {"user_id": user_id}
        await self.db.execute(sql, params)
        return

    async def delete_expired_token(self) -> None:
        """
        Delete every expired session_token
        """
        sql = "DELETE FROM session_token WHERE expires_at < NOW();"
        await self.db.execute(sql)
        return
