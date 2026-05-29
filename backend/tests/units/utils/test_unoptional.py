import pytest
from fastapi import HTTPException

from src.utils.unoptional import unoptional


class TestUnoptional:
    def test_returns_value_when_not_none(self):
        assert unoptional(42) == 42
        assert unoptional("hello") == "hello"
        assert unoptional([1, 2, 3]) == [1, 2, 3]

    def test_raises_value_error_by_default_when_none(self):
        with pytest.raises(ValueError, match="my_field"):
            unoptional(None, "my_field")

    def test_raises_http_exception_when_to_raise_is_httpexception(self):
        with pytest.raises(HTTPException) as exc_info:
            unoptional(None, "not found", to_raise="HttpException")

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "not found"

    def test_falls_back_to_value_error_for_unknown_to_raise(self):
        with pytest.raises(ValueError):
            unoptional(None, "msg", to_raise="UnknownType")

    def test_returns_falsy_but_non_none_values(self):
        assert unoptional(0) == 0
        assert unoptional("") == ""
        assert unoptional(False) is False
