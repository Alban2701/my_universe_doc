from src.models.text_block import InputTextBlock, PartialTextBlock, TextBlock
from typing import List, Optional
from src.repositories.base_repository import BaseRepository

class TextBlockRepository(BaseRepository):
    async def create_text_block(self, text_block: InputTextBlock, creator_id: int) -> PartialTextBlock:
        """
        Create a new text block in the database

        Parameters:
        - text_block: InputTextBlock with title, content, entity_id
        - creator_id: id of the user creating the text block

        Returns:
        PartialTextBlock: the created text block
        """
        sql_update = """
            UPDATE text_blocks
            SET position = position + 1
            WHERE entity_id = %(entity_id)s AND position >= %(position)s;
        """
        sql_insert = """
            INSERT INTO text_blocks (title, content, position, creator_id, entity_id)
            VALUES (%(title)s, %(content)s, %(position)s, %(creator_id)s, %(entity_id)s)
            RETURNING *;
        """

        model_tb = text_block.model_dump()
        model_tb["creator_id"] = creator_id

        await self.db.execute(sql_update, model_tb)

        rows = await self.db.execute(sql_insert, model_tb)
        returned_tb = PartialTextBlock.model_validate(rows[0])
        return returned_tb
    
    async def get_text_block_by_id(self, text_block_id: int) -> Optional[PartialTextBlock]:
        """
        Get a text block by its id

        Parameters:
        - text_block_id (int): id of the text block

        Returns:
        PartialTextBlock or None if not found
        """
        sql = "SELECT * FROM text_blocks WHERE id = %(id)s"
        rows = await self.db.execute(sql, {"id": text_block_id})
        if not rows:
            return None
        returned_tb = PartialTextBlock.model_validate(rows[0])
        return returned_tb

    async def get_text_blocks_by_entity(self, entity_id: int) -> List[PartialTextBlock]:
        """
        Get all text blocks belonging to a specific entity

        Parameters:
        - entity_id (int): id of the entity

        Returns:
        List[PartialTextBlock]: list of text blocks
        """
        sql = "SELECT * FROM text_blocks WHERE entity_id = %(entity_id)s"
        rows = await self.db.execute(sql, {"entity_id": entity_id})
        return [PartialTextBlock.model_validate(row) for row in rows]

    async def update_text_block(self, text_block_id: int, text_block_patch: PartialTextBlock) -> Optional[PartialTextBlock]:
        """
        Update a text block with new data

        Parameters:
        - text_block_id (int): id of the text block to update
        - text_block_patch (PartialTextBlock): fields to update

        Returns:
        PartialTextBlock: the updated text block or None if not found
        """
        # Récupère l'ancienne position
        old_position_sql = "SELECT position, entity_id FROM text_blocks WHERE id = %(id)s"
        old_position_rows = await self.db.execute(old_position_sql, {"id": text_block_id})
        if not old_position_rows:
            return None
        old_position = old_position_rows[0]["position"]
        entity_id = old_position_rows[0]["entity_id"]

        # Si la position est modifiée, décale les autres text blocks
        new_position = text_block_patch.position
        if new_position is not None and new_position != old_position:
            # Requête pour décaler les positions et mettre à jour le text_block en une seule fois
            sql = """
                UPDATE text_blocks
                SET position = CASE
                    WHEN id = %(text_block_id)s THEN %(new_position)s
                    WHEN position >= %(new_position)s AND position < %(old_position)s THEN position + 1
                    WHEN position > %(old_position)s AND position <= %(new_position)s THEN position - 1
                    ELSE position
                END
                WHERE id IN (
                    SELECT id FROM text_blocks
                    WHERE entity_id = %(entity_id)s
                    AND position BETWEEN LEAST(%(new_position)s, %(old_position)s) AND GREATEST(%(new_position)s, %(old_position)s)
                )
                RETURNING *;
            """
            params = {
                "text_block_id": text_block_id,
                "new_position": new_position,
                "old_position": old_position,
                "entity_id": entity_id,
            }
            rows = await self.db.execute(sql, params)
        else:
            # Mise à jour normale si la position n'est pas modifiée
            sql = (
                "UPDATE text_blocks SET "
                "title = COALESCE(%(title)s, title), "
                "content = COALESCE(%(content)s, content), "
                "updated_at = NOW() "
                "WHERE id = %(id)s "
                "RETURNING *"
            )
            model_patch = text_block_patch.model_dump()
            model_patch["id"] = text_block_id
            rows = await self.db.execute(sql, model_patch)

        if not rows:
            return None
        returned_tb = PartialTextBlock.model_validate(rows[0])
        return returned_tb
        

    async def delete_text_block(self, text_block_id: int) -> Optional[TextBlock]:
        """
        Delete a text block from the database

        Parameters:
        - text_block_id (int): id of the text block to delete

        Returns:
        bool: True if deleted, False otherwise
        """
        
        sql = "DELETE FROM text_blocks WHERE id = %(id)s RETURNING id"
        deleted_rows = await self.db.execute(sql, {"id": text_block_id})
        if not deleted_rows:
            return None
        deleted = TextBlock.model_validate(deleted_rows[0])
        switch_sql = ("UPDATE text_blocks "
                    "SET position = position - 1 "
                    "WHERE position > %(position)s "
                    "AND entity_id = %(entity_id)")
        await self.db.execute(switch_sql, {"position": deleted.position, "entity_id": deleted.entity_id})

        return deleted