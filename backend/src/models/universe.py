from pydantic import BaseModel

class Universe(BaseModel):
    id: int
    creator_id: int
    name: str
    description: str | None = None
    version: str | None = None

class InputUniverse(BaseModel):
    name: str
    description: str | None = None

class PartialUniverse(BaseModel):
    id: int | None = None
    creator_id: int | None  = None
    name: str | None = None
    description: str | None
    version: str | None = None
