from pydantic import BaseModel


class Entity(BaseModel):
    id: int
    name: str
    not_discovered_name: str | None = None
    parent: int | None = None
    universe_id: int
    creator_id: int

class InputEntity(BaseModel):
    name: str
    not_discoverd_name: str | None = None
    parent: int | None
    universe_id: int

class PartialEntity(BaseModel):
    id: int | None = None
    name: str | None = None
    not_discovered_name: str | None = None
    parent: int | None = None
    universe_id: int | None = None
    creator_id: int | None = None