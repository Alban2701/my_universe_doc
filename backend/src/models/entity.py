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
