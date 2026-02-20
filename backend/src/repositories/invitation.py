from models.invitation import Invitation, InputInvitation, PartialInvitation, InvitationStatus
from db_connection import DbConnection
from typing import List

async def create_invitation(sender_id: int, invitation: InputInvitation, db: DbConnection) -> PartialInvitation:
    """
    create a new invitation in the database

    Parameters:
    - sender_id: id of the user sending the invitation
    - invitation: the invitation data (receiver_id, universe_id)
    
    Returns:
    PartialInvitation: the created invitation
    """
    sql = (
        "INSERT INTO invitations (sender_id, receiver_id, universe_id, status) "
        "VALUES (%(sender_id)s, %(receiver_id)s, %(universe_id)s, %(status)s) "
        "RETURNING *"
    )
    model_invitation = invitation.model_dump()
    model_invitation["sender_id"] = sender_id
    model_invitation["status"] = InvitationStatus.pending
    rows = await db.execute(sql, model_invitation)
    returned_invitation = PartialInvitation.model_validate(rows[0])
    return returned_invitation


async def get_invitation_by_id(invitation_id: int, db: DbConnection) -> PartialInvitation | None:
    """
    get an invitation by its id

    Parameters:
    - invitation_id (int): id of the invitation

    Returns:
    PartialInvitation or None if not found
    """
    sql = "SELECT * FROM invitations WHERE id = %(id)s"
    rows = await db.execute(sql, {"id": invitation_id})
    if not rows:
        return None
    returned_invitation = PartialInvitation.model_validate(rows[0])
    return returned_invitation


async def get_invitations_by_receiver(receiver_id: int, db: DbConnection) -> List[PartialInvitation]:
    """
    get all invitations received by a user

    Parameters:
    - receiver_id (int): id of the receiver

    Returns:
    List[PartialInvitation]: list of invitations
    """
    sql = "SELECT * FROM invitations WHERE receiver_id = %(receiver_id)s"
    rows = await db.execute(sql, {"receiver_id": receiver_id})
    return [PartialInvitation.model_validate(row) for row in rows]


async def update_invitation_status(invitation_id: int, status: InvitationStatus, db: DbConnection) -> PartialInvitation | None:
    """
    update the status of an invitation (pending, accepted, rejected)

    Parameters:
    - invitation_id (int): id of the invitation
    - status (InvitationStatus): new status

    Returns:
    PartialInvitation: the updated invitation or None if not found
    """
    sql = (
        "UPDATE invitations SET status = %(status)s, updated_at = NOW() "
        "WHERE id = %(id)s "
        "RETURNING *"
    )
    rows = await db.execute(sql, {"id": invitation_id, "status": status})
    if not rows:
        return None
    returned_invitation = PartialInvitation.model_validate(rows[0])
    return returned_invitation


async def delete_invitation(invitation_id: int, db: DbConnection) -> bool:
    """
    delete an invitation from the database

    Parameters:
    - invitation_id (int): id of the invitation to delete

    Returns:
    bool: True if deleted, False otherwise
    """
    sql = "DELETE FROM invitations WHERE id = %(id)s RETURNING id"
    rows = await db.execute(sql, {"id": invitation_id})
    return bool(rows)
