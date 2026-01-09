from enum import Enum


class UserUniverseRole(str, Enum):
    creator = "creator"
    super_administrator = "super administrator"

class UserEntityRole(str, Enum):
    administrator = "entity administrator"
    editor = "editor"


class InvitationStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class CommitStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"