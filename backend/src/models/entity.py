from pydantic import BaseModel


class Entity(BaseModel):
    id: int
    name: str
    not_discovered_name: str
    parent: int | None
    universe_id: int
    creator_id: int

class InputEntity(BaseModel):
    name: str
    parent: int | None


class PartialEntity(BaseModel):
    id: int | None
    name: str | None
    not_discovered_name: str | None
    parent: int | None
    universe_id: int | None
    creator_id: int | None