from pydantic import TypeAdapter

from models.invitation import Invitation, InputInvitation, PartialInvitation, InvitationStatus
from typing import List, Optional
from src.repositories.base_repository import BaseRepository
from src.utils.unoptional import unoptional

class InvitationRepository(BaseRepository):
    async def create_invitation(self, sender_id: int, invitation: InputInvitation) -> Invitation:
        """
        Create a new invitation in the database

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
        rows = unoptional(await self.db.execute(sql, model_invitation))
        returned_invitation = Invitation.model_validate(rows[0])
        return returned_invitation

    async def get_invitation_by_id(self, invitation_id: int) -> Optional[PartialInvitation]:
        """
        Get an invitation by its id

        Parameters:
        - invitation_id (int): id of the invitation

        Returns:
        PartialInvitation or None if not found
        """
        sql = "SELECT * FROM invitations WHERE id = %(id)s"
        rows = await self.db.execute(sql, {"id": invitation_id})
        if not rows:
            return None
        returned_invitation = PartialInvitation.model_validate(rows[0])
        return returned_invitation

    async def get_invitations_by_receiver(self, receiver_id: int) -> List[PartialInvitation]:
        """
        Get all invitations received by a user

        Parameters:
        - receiver_id (int): id of the receiver

        Returns:
        List[PartialInvitation]: list of invitations
        """
        sql = "SELECT * FROM invitations WHERE receiver_id = %(receiver_id)s"
        rows = await self.db.execute(sql, {"receiver_id": receiver_id})
        adapter = TypeAdapter(List[PartialInvitation])
        return adapter.validate_python(rows)

    async def update_invitation_status(self, invitation_id: int, status: InvitationStatus) -> Optional[PartialInvitation]:
        """
        Update the status of an invitation (pending, accepted, rejected)

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
        rows = await self.db.execute(sql, {"id": invitation_id, "status": status})
        if not rows:
            return None
        returned_invitation = PartialInvitation.model_validate(rows[0])
        return returned_invitation

    async def delete_invitation(self, invitation_id: int) -> bool:
        """
        Delete an invitation from the database

        Parameters:
        - invitation_id (int): id of the invitation to delete

        Returns:
        bool: True if deleted, False otherwise
        """
        sql = "DELETE FROM invitations WHERE id = %(id)s RETURNING id"
        rows = await self.db.execute(sql, {"id": invitation_id})
        return bool(rows)