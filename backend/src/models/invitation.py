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

from enum import Enum

