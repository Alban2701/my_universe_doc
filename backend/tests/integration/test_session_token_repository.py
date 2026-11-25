"""
Integration tests for the session_token operations:
- refuse a session_token with a null or negative given expiration date
- accept a session_token with a positive given expiration date
- store a hash of the token, never the raw value
- delete one token / every token of a user / every expired token
"""

import pytest

from src.factory import Factory
from src.utils.token_creator import hash_token

factory = Factory()

USER_ID = 1
OTHER_USER_ID = 2


async def count_tokens(user_id: int) -> int:
    rows = await factory.session_repository.db.execute(
        "SELECT COUNT(*) AS nb FROM session_token WHERE user_id = %(user_id)s",
        {"user_id": user_id},
    )
    assert rows is not None
    return rows[0]["nb"]


async def seconds_until_expiration(session_id: int) -> float:
    """Remaining lifetime of a token in seconds, computed by Postgres."""
    rows = await factory.session_repository.db.execute(
        "SELECT EXTRACT(EPOCH FROM expires_at - NOW()) AS remaining"
        " FROM session_token WHERE id = %(id)s",
        {"id": session_id},
    )
    assert rows is not None
    return float(rows[0]["remaining"])


DAY = 24 * 60 * 60


class TestUpdateExpirationSessionToken:
    repository = factory.session_repository
    user_repository = factory.user_repository

    async def test_extends_the_presented_token(self):
        session = await self.repository.create_session_token(USER_ID, expires_in_days=1)

        await self.repository.update_expires_date_token(
            session.value, expires_in_days=30
        )

        remaining = await seconds_until_expiration(session.id)
        assert 29 * DAY < remaining <= 30 * DAY

    async def test_does_not_extend_other_sessions_of_the_user(self):
        presented = await self.repository.create_session_token(
            USER_ID, expires_in_days=1
        )
        other = await self.repository.create_session_token(USER_ID, expires_in_days=1)

        await self.repository.update_expires_date_token(
            presented.value, expires_in_days=30
        )

        assert await seconds_until_expiration(other.id) <= 1 * DAY

    async def test_does_not_revive_an_expired_token(self):
        session = await self.repository.create_session_token(
            USER_ID, expires_in_days=-1
        )

        await self.repository.update_expires_date_token(
            session.value, expires_in_days=30
        )

        assert (
            await self.user_repository.get_user_with_session_token(session.value)
            is None
        )


class TestInsertionSessionToken:
    repository = factory.session_repository
    user_repository = factory.user_repository

    async def test_returns_raw_token_and_stores_its_hash(self):
        session = await self.repository.create_session_token(USER_ID)

        assert session.user_id == USER_ID

        rows = await self.repository.db.execute(
            "SELECT value FROM session_token WHERE id = %(id)s", {"id": session.id}
        )
        assert rows is not None
        stored_value = rows[0]["value"]
        assert stored_value != session.value
        assert stored_value == hash_token(session.value)

    async def test_accepts_token_with_positive_expiration(self):
        session = await self.repository.create_session_token(USER_ID, expires_in_days=7)

        user = await self.user_repository.get_user_with_session_token(session.value)

        assert user is not None
        assert user.id == USER_ID

    @pytest.mark.parametrize("expires_in_days", [0, -1])
    async def test_refuses_token_with_null_or_negative_expiration(
        self, expires_in_days: int
    ):
        session = await self.repository.create_session_token(
            USER_ID, expires_in_days=expires_in_days
        )

        user = await self.user_repository.get_user_with_session_token(session.value)

        assert user is None

    async def test_refuses_unknown_token(self):
        user = await self.user_repository.get_user_with_session_token("not-a-token")

        assert user is None

    async def test_refuses_hash_presented_as_token(self):
        """The cookie must hold the raw token: presenting the stored hash fails."""
        session = await self.repository.create_session_token(USER_ID)

        user = await self.user_repository.get_user_with_session_token(
            hash_token(session.value)
        )

        assert user is None


class TestDeletionSessionToken:
    repository = factory.session_repository
    user_repository = factory.user_repository

    async def test_delete_session_token_removes_only_that_token(self):
        kept = await self.repository.create_session_token(USER_ID)
        deleted = await self.repository.create_session_token(USER_ID)

        await self.repository.delete_session_token(deleted.value)

        assert (
            await self.user_repository.get_user_with_session_token(deleted.value)
            is None
        )
        assert (
            await self.user_repository.get_user_with_session_token(kept.value)
            is not None
        )

    async def test_delete_all_user_session_token_keeps_other_users(self):
        await self.repository.create_session_token(USER_ID)
        await self.repository.create_session_token(USER_ID)
        other = await self.repository.create_session_token(OTHER_USER_ID)

        await self.repository.delete_all_user_session_token(USER_ID)

        assert await count_tokens(USER_ID) == 0
        assert (
            await self.user_repository.get_user_with_session_token(other.value)
            is not None
        )

    async def test_delete_expired_token_keeps_valid_ones(self):
        await self.repository.create_session_token(USER_ID, expires_in_days=-1)
        valid = await self.repository.create_session_token(USER_ID, expires_in_days=7)

        await self.repository.delete_expired_token()

        assert await count_tokens(USER_ID) == 1
        assert (
            await self.user_repository.get_user_with_session_token(valid.value)
            is not None
        )
