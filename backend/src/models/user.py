from pydantic import BaseModel
import psycopg as pg
import os
from db_connection import Db_connection


class User(BaseModel):
    email: str | None
    password: str | None
    username: str | None
    bio: str | None
    picture: bytes | None

    def __init__(self, email: str | None = None, password: str | None = None, username: str | None = None, bio: str | None = None, picture: bytes | None = None):
        self.email = email
        self.password = password
        self.username = username
        self.bio = bio
        self.picture = picture

    async def update(self, db_connection: Db_connection):
        sql = ""
        params = {}
        db_connection.execute(sql, params)
