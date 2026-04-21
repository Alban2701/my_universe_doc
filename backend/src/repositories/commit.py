from pydantic import TypeAdapter

from src.models.commit import Commit, InputCommit, PartialCommit
from src.models.enums import CommitsStatus
from typing import List, Optional
from src.repositories.base_repository import BaseRepository
from src.utils.unoptional import unoptional

class CommitRepository(BaseRepository):
    async def create_commit(self, commit: InputCommit, creator_id: int) -> Commit:
        """
        Create a new commit in the database

        Parameters:
        - commit: InputCommit with message and content (JSON)
        - creator_id: id of the user creating the commit

        Returns:
        Commit: the created commit
        """
        sql = (
            "INSERT INTO commits (message, creator_id, content, status, admin_comment) "
            "VALUES (%(message)s, %(creator_id)s, %(content)s, %(status)s, %(admin_comment)s) "
            "RETURNING *"
        )
        model_commit = commit.model_dump()
        model_commit["creator_id"] = creator_id
        model_commit["status"] = CommitsStatus.pending
        model_commit["admin_comment"] = None
        rows = unoptional(await self.db.execute(sql, model_commit))
        returned_commit = Commit.model_validate(rows[0])
        return returned_commit

    async def get_commit_by_id(self, commit_id: int) -> Optional[PartialCommit]:
        """
        Get a commit by its id

        Parameters:
        - commit_id (int): id of the commit

        Returns:
        PartialCommit or None if not found
        """
        sql = "SELECT * FROM commits WHERE id = %(id)s"
        rows = await self.db.execute(sql, {"id": commit_id})
        if not rows:
            return None
        returned_commit = PartialCommit.model_validate(rows[0])
        return returned_commit

    async def get_commits_by_creator(self, creator_id: int) -> List[PartialCommit]:
        """
        Get all commits created by a user

        Parameters:
        - creator_id (int): id of the creator

        Returns:
        List[PartialCommit]: list of commits
        """
        sql = "SELECT * FROM commits WHERE creator_id = %(creator_id)s ORDER BY created_at DESC"
        rows = unoptional(await self.db.execute(sql, {"creator_id": creator_id}))
        adapter = TypeAdapter(List[PartialCommit])
        return adapter.validate_python(rows)

    async def update_commit_status(self, commit_id: int, status: CommitsStatus, admin_comment: str | None) -> Optional[PartialCommit]:
        """
        Update the status of a commit (pending, accepted, rejected) and optional admin comment

        Parameters:
        - commit_id (int): id of the commit
        - status (CommitsStatus): new status
        - admin_comment (str | None): optional comment from admin

        Returns:
        PartialCommit: the updated commit or None if not found
        """
        sql = (
            "UPDATE commits SET "
            "status = %(status)s, "
            "admin_comment = %(admin_comment)s, "
            "updated_at = NOW() "
            "WHERE id = %(id)s "
            "RETURNING *"
        )
        rows = await self.db.execute(sql, {"id": commit_id, "status": status, "admin_comment": admin_comment})
        if not rows:
            return None
        returned_commit = PartialCommit.model_validate(rows[0])
        return returned_commit

    async def delete_commit(self, commit_id: int) -> bool:
        """
        Delete a commit from the database

        Parameters:
        - commit_id (int): id of the commit to delete

        Returns:
        bool: True if deleted, False otherwise
        """
        sql = "DELETE FROM commits WHERE id = %(id)s RETURNING id"
        rows = await self.db.execute(sql, {"id": commit_id})
        return bool(rows)