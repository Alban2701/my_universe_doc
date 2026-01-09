from pydantic import BaseModel

class Universe(BaseModel):
    id: int
    creator_id: int
    name: str
    description: str | None
    version: str | None

class InputUniverse(BaseModel):
    name: str
    description: str | None
    version: str | None
