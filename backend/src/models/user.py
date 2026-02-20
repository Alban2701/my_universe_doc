from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    username: str
    bio: str | None = None
    picture: bytes | None = None

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

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UserToken(BaseModel):
    id: int
    username: str
    picture: bytes | None = None


