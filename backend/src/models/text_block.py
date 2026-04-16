from pydantic import BaseModel


class TextBlock(BaseModel):
    id: int
    title: str | None
    content: str | None
    position: int
    creator_id: int
    entity_id: int

class InputTextBlock(BaseModel):
    title: str | None
    content: str | None
    position: int
    entity_id: int

class PartialTextBlock(BaseModel):
    id: int | None=None
    title: str | None=None
    content: str | None=None
    position: int | None=None
    creator_id: int | None=None
    entity_id: int | None=None