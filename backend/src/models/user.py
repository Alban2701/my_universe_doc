from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    username: str
    bio: str | None = None
    picture: bytes | None = None
    created_at: datetime
    updated_at: datetime | None = None

class InputUser(BaseModel):
    email: EmailStr
    password: str
    username: str
    bio: str | None = None
    picture: bytes | None = None

class PartialUser(BaseModel):
    id: int | None = None
    email: EmailStr | None = None
    password: str | None = None
    username: str | None = None
    bio: str | None = None
    picture: bytes | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UserToken(BaseModel):
    id: int
    username: str
    picture: bytes | None = None


