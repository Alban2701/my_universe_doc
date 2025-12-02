from pydantic import BaseModel, EmailStr
from pydantic_tooltypes import Omit, Partial
import psycopg as pg
import os
from db_connection import DbConnection


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    username: str
    bio: str | None
    picture: bytes | None

InputUser = Omit[User, ["id"]] # pyright: ignore[reportInvalidTypeForm]
PartialUser = Partial[User]



