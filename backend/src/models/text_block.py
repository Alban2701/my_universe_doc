from typing import List

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
    id: int | None = None
    title: str | None = None
    content: str | None = None
    position: int | None = None
    creator_id: int | None = None
    entity_id: int | None = None


class MovingTextBlock(BaseModel):
    id: int
    old_position: int
    new_position: int
    entity_id: int


class UpdateTextBlocks(BaseModel):
    to_create: List[InputTextBlock]
    to_delete: List[PartialTextBlock]
    to_move: List[MovingTextBlock]
    to_patch: List[PartialTextBlock]


class UpdatedTextBlocks(BaseModel):
    created: List[TextBlock] | None = None
    deleted: List[TextBlock] | None = None
    moved: List[TextBlock] | None = None
    patched: List[TextBlock] | None = None
