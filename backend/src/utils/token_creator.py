import secrets
from hashlib import sha256


def create_token(nb_bytes: int) -> str:
    """
    create an url safe token session

    Parameters:
    - nb_bytes(int): how many bytes in the token

    Returns:
    str: the token created
    """
    token_value = secrets.token_urlsafe(nb_bytes)
    return token_value


def hash_token(token_value: str) -> str:
    return sha256(token_value.encode()).hexdigest()
