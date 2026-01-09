from pydantic import BaseModel


class TextBlock(BaseModel):
    id: int
    title: str | None
    content: str | None
    creator_id: int
    entity_id: int

class InputTextBlock(BaseModel):
    title: str | None
    content: str | None
    entity_id: int
