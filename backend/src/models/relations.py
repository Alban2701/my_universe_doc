from pydantic import BaseModel
from src.models.enums import UserEntityRole, UserUniverseRole


class UserUniverse(BaseModel):
    user_id: int
    universe_id: int
    admin_role: UserUniverseRole

class UserEntity(BaseModel):
    user_id: int
    entity_id: int
    role: UserEntityRole

class UserTextBlock(BaseModel):
    user_id: int
    text_block_id: int