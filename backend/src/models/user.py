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

class InputUser(BaseModel):
    email: EmailStr
    password: str
    username: str
    bio: str | None
    picture: bytes | None

class PartialUser(BaseModel):
    id: int | None
    email: EmailStr | None
    password: str | None
    username: str | None
    bio: str | None
    picture: bytes | None

class LoginUser(BaseModel):
    email: EmailStr
    password: str



