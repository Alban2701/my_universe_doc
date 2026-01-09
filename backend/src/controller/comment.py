from models.comments import Comment, InputComment, PartialComment
from db_connection import DbConnection
from typing import List, Optional

async def create_comment(comment: InputComment, creator_id: int, db: DbConnection) -> PartialComment:
    """
    create a new comment in the database

    Parameters:
    - comment: InputComment with content, entity_id, optional text_block_id, optional comment_id
    - creator_id: id of the user creating the comment

    Returns:
    PartialComment: the created comment
    """
    sql = (
        "INSERT INTO comments (content, creator_id, entity_id, text_block_id, comment_id) "
        "VALUES (%(content)s, %(creator_id)s, %(entity_id)s, %(text_block_id)s, %(comment_id)s) "
        "RETURNING *"
    )
    model_comment = comment.model_dump()
    model_comment["creator_id"] = creator_id
    rows = await db.execute(sql, model_comment)
    returned_comment = PartialComment.model_validate(rows[0])
    return returned_comment


async def get_comment_by_id(comment_id: int, db: DbConnection) -> Optional[PartialComment]:
    """
    get a comment by its id

    Parameters:
    - comment_id (int): id of the comment

    Returns:
    PartialComment or None if not found
    """
    sql = "SELECT * FROM comments WHERE id = %(id)s"
    rows = await db.execute(sql, {"id": comment_id})
    if not rows:
        return None
    returned_comment = PartialComment.model_validate(rows[0])
    return returned_comment


async def get_comments_by_entity(entity_id: int, db: DbConnection) -> List[PartialComment]:
    """
    get all comments for a given entity

    Parameters:
    - entity_id (int): id of the entity

    Returns:
    List[PartialComment]: list of comments
    """
    sql = "SELECT * FROM comments WHERE entity_id = %(entity_id)s ORDER BY created_at ASC"
    rows = await db.execute(sql, {"entity_id": entity_id})
    return [PartialComment.model_validate(row) for row in rows]


async def get_comments_by_text_block(text_block_id: int, db: DbConnection) -> List[PartialComment]:
    """
    get all comments for a given text block

    Parameters:
    - text_block_id (int): id of the text block

    Returns:
    List[PartialComment]: list of comments
    """
    sql = "SELECT * FROM comments WHERE text_block_id = %(text_block_id)s ORDER BY created_at ASC"
    rows = await db.execute(sql, {"text_block_id": text_block_id})
    return [PartialComment.model_validate(row) for row in rows]


async def update_comment(comment_id: int, comment_patch: PartialComment, db: DbConnection) -> Optional[PartialComment]:
    """
    update a comment's content

    Parameters:
    - comment_id (int): id of the comment
    - comment_patch (PartialComment): new content

    Returns:
    PartialComment: the updated comment or None if not found
    """
    sql = (
        "UPDATE comments SET "
        "content = COALESCE(%(content)s, content), "
        "updated_at = NOW() "
        "WHERE id = %(id)s "
        "RETURNING *"
    )
    model_patch = comment_patch.model_dump()
    model_patch["id"] = comment_id
    rows = await db.execute(sql, model_patch)
    if not rows:
        return None
    returned_comment = PartialComment.model_validate(rows[0])
    return returned_comment


async def delete_comment(comment_id: int, db: DbConnection) -> bool:
    """
    delete a comment from the database

    Parameters:
    - comment_id (int): id of the comment to delete

    Returns:
    bool: True if deleted, False otherwise
    """
    sql = "DELETE FROM comments WHERE id = %(id)s RETURNING id"
    rows = await db.execute(sql, {"id": comment_id})
    return bool(rows)
