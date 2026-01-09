from enum import Enum
from typing import Any
from pydantic import BaseModel
from src.models.enums import CommitStatus

class Commit(BaseModel):
    id: int
    message: str | None
    creator_id: int
    content: dict[str, Any]
    status: CommitStatus | None
    admin_comment: str | None

class InputCommit(BaseModel):
    message: str | None
    content: dict[str, Any]

class PartialCommit(BaseModel):
    id: int | None
    message: str | None
    creator_id: int | None
    content: dict[str, Any] | None
    status: CommitStatus | None
    admin_comment: str | None