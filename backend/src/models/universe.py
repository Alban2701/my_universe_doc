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

class PartialUniverse(BaseModel):
    id: int | None
    creator_id: int | None
    name: str | None
    description: str | None
    version: str | None
