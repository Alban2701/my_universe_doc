from pydantic import BaseModel
from src.models.enums import InvitationStatus


class Invitation(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    universe_id: int
    status: InvitationStatus

class InputInvitation(BaseModel):
    receiver_id: int
    universe_id: int

class PartialInvitation(BaseModel):
    id: int | None
    sender_id: int | None
    receiver_id: int | None
    universe_id: int | None
    status: InvitationStatus | None

