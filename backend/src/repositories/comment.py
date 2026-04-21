from pydantic import TypeAdapter

from models.comments import Comment, InputComment, PartialComment
from typing import List, Optional
from src.repositories.base_repository import BaseRepository
from src.utils.unoptional import unoptional

class CommentRepository(BaseRepository):
    async def create_comment(self, comment: InputComment, creator_id: int) -> Comment:
        """
        Create a new comment in the database

        Parameters:
        - comment: InputComment with content, entity_id, optional text_block_id, optional comment_id
        - creator_id: id of the user creating the comment

        Returns:
        Comment: the created comment
        """
        sql = (
            "INSERT INTO comments (content, creator_id, entity_id, text_block_id, comment_id) "
            "VALUES (%(content)s, %(creator_id)s, %(entity_id)s, %(text_block_id)s, %(comment_id)s) "
            "RETURNING *"
        )
        model_comment = comment.model_dump()
        model_comment["creator_id"] = creator_id
        rows = unoptional(await self.db.execute(sql, model_comment))
        returned_comment = Comment.model_validate(rows[0])
        return returned_comment

    async def get_comment_by_id(self, comment_id: int) -> Optional[PartialComment]:
        """
        Get a comment by its id

        Parameters:
        - comment_id (int): id of the comment

        Returns:
        PartialComment or None if not found
        """
        sql = "SELECT * FROM comments WHERE id = %(id)s"
        rows = await self.db.execute(sql, {"id": comment_id})
        if not rows:
            return None
        returned_comment = PartialComment.model_validate(rows[0])
        return returned_comment

    async def get_comments_by_entity(self, entity_id: int) -> List[PartialComment]:
        """
        Get all comments for a given entity

        Parameters:
        - entity_id (int): id of the entity

        Returns:
        List[PartialComment]: list of comments
        """
        sql = "SELECT * FROM comments WHERE entity_id = %(entity_id)s ORDER BY created_at ASC"
        rows = await self.db.execute(sql, {"entity_id": entity_id})
        adapter = TypeAdapter(List[PartialComment])
        return adapter.validate_python(rows)

    async def get_comments_by_text_block(self, text_block_id: int) -> List[PartialComment]:
        """
        Get all comments for a given text block

        Parameters:
        - text_block_id (int): id of the text block

        Returns:
        List[PartialComment]: list of comments
        """
        sql = "SELECT * FROM comments WHERE text_block_id = %(text_block_id)s ORDER BY created_at ASC"
        rows = await self.db.execute(sql, {"text_block_id": text_block_id})
        adapter = TypeAdapter(List[PartialComment])
        return adapter.validate_python(rows)

    async def update_comment(self, comment_id: int, comment_patch: PartialComment) -> Optional[PartialComment]:
        """
        Update a comment's content

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
        rows = await self.db.execute(sql, model_patch)
        if not rows:
            return None
        returned_comment = PartialComment.model_validate(rows[0])
        return returned_comment

    async def delete_comment(self, comment_id: int) -> bool:
        """
        Delete a comment from the database

        Parameters:
        - comment_id (int): id of the comment to delete

        Returns:
        bool: True if deleted, False otherwise
        """
        sql = "DELETE FROM comments WHERE id = %(id)s RETURNING id"
        rows = await self.db.execute(sql, {"id": comment_id})
        return bool(rows)