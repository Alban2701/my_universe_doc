from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch


from src.middlewares.auth import AuthMiddleware
from src.models.user import UserToken

from src.errors import errors


def make_request(path: str = "/protected", session_token: str | None = None):
    request = MagicMock()
    request.url.path = path
    request.cookies = {"session_token": session_token} if session_token else {}
    request.state = SimpleNamespace()
    return request


async def make_call_next():
    response = MagicMock(name="downstream-response")
    call_next = AsyncMock(return_value=response)
    return call_next, response


class TestAuthMiddleware:
    async def test_public_paths_are_let_through(self):
        middleware = AuthMiddleware(app=MagicMock())
        call_next, response = await make_call_next()

        result = await middleware.dispatch(make_request("/user/login"), call_next)

        assert result is response
        call_next.assert_awaited_once()

    async def test_returns_401_when_no_session_cookie(self):
        middleware = AuthMiddleware(app=MagicMock())
        call_next, _ = await make_call_next()

        result = await middleware.dispatch(make_request(), call_next)

        assert result.status_code == 401
        call_next.assert_not_awaited()

    async def test_returns_401_when_session_is_expired(self):
        with patch("src.middlewares.auth.user_controller") as user_ctrl:
            user_ctrl.get_user_with_session_token = AsyncMock(
                side_effect=errors.SessionExpiredError()
            )
            middleware = AuthMiddleware(app=MagicMock())
            call_next, _ = await make_call_next()

            result = await middleware.dispatch(
                make_request(session_token="tok"), call_next
            )

        assert result.status_code == 401
        call_next.assert_not_awaited()

    async def test_returns_401_when_user_is_not_logged_in(self):
        user = UserToken(id=1, username="bob")
        with patch("src.middlewares.auth.user_controller") as user_ctrl:
            user_ctrl.get_user_with_session_token = AsyncMock(return_value=user)
            user_ctrl.is_logged_in = AsyncMock(return_value=False)
            middleware = AuthMiddleware(app=MagicMock())
            call_next, _ = await make_call_next()

            result = await middleware.dispatch(
                make_request(session_token="tok"), call_next
            )

        assert result.status_code == 401
        call_next.assert_not_awaited()

    async def test_lets_through_and_sets_user_when_logged_in(self):
        user = UserToken(id=42, username="bob")
        with patch("src.middlewares.auth.user_controller") as user_ctrl:
            user_ctrl.get_user_with_session_token = AsyncMock(return_value=user)
            user_ctrl.is_logged_in = AsyncMock(return_value=True)
            middleware = AuthMiddleware(app=MagicMock())
            call_next, response = await make_call_next()
            request = make_request(session_token="tok")

            result = await middleware.dispatch(request, call_next)

        assert result is response
        assert request.state.user is user
        call_next.assert_awaited_once_with(request)
