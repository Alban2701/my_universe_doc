from src.models.commit import Commit, InputCommit, PartialCommit, CommitsStatus
from db_connection import DbConnection
from typing import List, Optional

async def create_commit(commit: InputCommit, creator_id: int, db: DbConnection) -> PartialCommit:
    """
    create a new commit in the database

    Parameters:
    - commit: InputCommit with message and content (JSON)
    - creator_id: id of the user creating the commit

    Returns:
    PartialCommit: the created commit
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
    rows = await db.execute(sql, model_commit)
    returned_commit = PartialCommit.model_validate(rows[0])
    return returned_commit


async def get_commit_by_id(commit_id: int, db: DbConnection) -> Optional[PartialCommit]:
    """
    get a commit by its id

    Parameters:
    - commit_id (int): id of the commit

    Returns:
    PartialCommit or None if not found
    """
    sql = "SELECT * FROM commits WHERE id = %(id)s"
    rows = await db.execute(sql, {"id": commit_id})
    if not rows:
        return None
    returned_commit = PartialCommit.model_validate(rows[0])
    return returned_commit


async def get_commits_by_creator(creator_id: int, db: DbConnection) -> List[PartialCommit]:
    """
    get all commits created by a user

    Parameters:
    - creator_id (int): id of the creator

    Returns:
    List[PartialCommit]: list of commits
    """
    sql = "SELECT * FROM commits WHERE creator_id = %(creator_id)s ORDER BY created_at DESC"
    rows = await db.execute(sql, {"creator_id": creator_id})
    return [PartialCommit.model_validate(row) for row in rows]


async def update_commit_status(commit_id: int, status: CommitsStatus, admin_comment: str | None, db: DbConnection) -> Optional[PartialCommit]:
    """
    update the status of a commit (pending, accepted, rejected) and optional admin comment

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
    rows = await db.execute(sql, {"id": commit_id, "status": status, "admin_comment": admin_comment})
    if not rows:
        return None
    returned_commit = PartialCommit.model_validate(rows[0])
    return returned_commit


async def delete_commit(commit_id: int, db: DbConnection) -> bool:
    """
    delete a commit from the database

    Parameters:
    - commit_id (int): id of the commit to delete

    Returns:
    bool: True if deleted, False otherwise
    """
    sql = "DELETE FROM commits WHERE id = %(id)s RETURNING id"
    rows = await db.execute(sql, {"id": commit_id})
    return bool(rows)
