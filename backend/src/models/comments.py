from pydantic import BaseModel


class Comment(BaseModel):
    id: int
    content: str
    creator_id: int
    entity_id: int
    text_block_id: int | None
    comment_id: int | None

class InputComment(BaseModel):
    content: str
    entity_id: int
    text_block_id: int | None
    comment_id: int | None
