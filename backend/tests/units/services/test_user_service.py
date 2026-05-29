from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from src.models.user import InputUser, LoginUser, PartialUser
from src.services.user import UserService


def make_service():
    user_repo = AsyncMock()
    session_repo = AsyncMock()
    service = UserService(user_repo, session_repo)
    return service, user_repo, session_repo


class TestRegister:
    async def test_password_is_hashed_before_being_passed_to_repository(self):
        service, user_repo, _ = make_service()
        user_repo.register.return_value = PartialUser(id=1, username="bob")

        input_user = InputUser(
            email="bob@mail.com",
            password="plain-text-password",
            username="bob",
        )
        await service.register(input_user)

        sent_to_repo = user_repo.register.call_args.args[0]
        assert sent_to_repo.password != "plain-text-password"
        assert service.hasher.verify("plain-text-password", sent_to_repo.password)

    async def test_returns_what_the_repository_returns(self):
        service, user_repo, _ = make_service()
        expected = PartialUser(id=42, username="bob")
        user_repo.register.return_value = expected

        result = await service.register(
            InputUser(email="bob@mail.com", password="pw", username="bob")
        )

        assert result is expected


class TestLogin:
    async def test_raises_404_when_user_does_not_exist(self):
        service, user_repo, _ = make_service()
        user_repo.get_user_by_email.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await service.login(LoginUser(email="ghost@mail.com", password="pw"))

        assert exc_info.value.status_code == 404

    async def test_raises_401_when_password_is_wrong(self):
        service, user_repo, _ = make_service()
        hashed = service.hasher.hash("real-password")
        user_repo.get_user_by_email.return_value = PartialUser(
            id=1, password=hashed, username="bob"
        )

        with pytest.raises(HTTPException) as exc_info:
            await service.login(LoginUser(email="bob@mail.com", password="wrong"))

        assert exc_info.value.status_code == 401

    async def test_returns_session_token_value_on_success(self):
        service, user_repo, session_repo = make_service()
        hashed = service.hasher.hash("good-pw")
        user_repo.get_user_by_email.return_value = PartialUser(
            id=7, password=hashed, username="bob"
        )
        session = MagicMock(value="session-token-xyz")
        session_repo.create_session_token.return_value = session

        result = await service.login(
            LoginUser(email="bob@mail.com", password="good-pw")
        )

        assert result == "session-token-xyz"
        session_repo.create_session_token.assert_awaited_once_with(7)
