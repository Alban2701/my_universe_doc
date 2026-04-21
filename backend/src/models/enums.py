from enum import Enum


class UserUniverseRole(str, Enum):
    creator = "creator"
    super_administrator = "super administrator"
    contributor = "contributor"

class UserEntityRole(str, Enum):
    administrator = "entity administrator"
    editor = "editor"
    reader = "reader"

class InvitationStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class CommitsStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"