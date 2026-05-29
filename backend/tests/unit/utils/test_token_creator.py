from src.utils.token_creator import create_token


class TestCreateToken:
    def test_returns_a_string(self):
        token = create_token(32)
        assert isinstance(token, str)

    def test_token_is_not_empty(self):
        token = create_token(32)
        assert len(token) > 0

    def test_two_tokens_are_different(self):
        assert create_token(32) != create_token(32)
