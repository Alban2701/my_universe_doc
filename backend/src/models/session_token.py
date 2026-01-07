from pydantic import BaseModel
from datetime import datetime

class SessionToken(BaseModel):
    id: int
    value: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    expires_at: datetime