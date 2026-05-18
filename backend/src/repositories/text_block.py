from pydantic import TypeAdapter

from src.models.text_block import InputTextBlock, MovingTextBlock, PartialTextBlock, TextBlock
from typing import Any, Dict, List, Optional, Tuple
from src.repositories.base_repository import BaseRepository
from src.utils.unoptional import unoptional

class TextBlockRepository(BaseRepository):
    async def create_text_block(self, text_block: InputTextBlock, creator_id: int) -> TextBlock:
        """
        Create a new text block in the database

        Parameters:
        - text_block: InputTextBlock with title, content, entity_id
        - creator_id: id of the user creating the text block

        Returns:
        PartialTextBlock: the created text block
        """
        sql = """
            UPDATE text_blocks
            SET position = position + 1
            WHERE entity_id = %(entity_id)s AND position >= %(position)s;

            INSERT INTO text_blocks (title, content, position, creator_id, entity_id)
            VALUES (%(title)s, %(content)s, %(position)s, %(creator_id)s, %(entity_id)s)
            RETURNING *;
        """

        model_tb = text_block.model_dump()
        model_tb["creator_id"] = creator_id

        rows = unoptional(await self.db.execute(sql, model_tb))
        returned_tb = TextBlock.model_validate(rows[0])
        return returned_tb
    
    async def get_text_block_by_id(self, text_block_id: int) -> Optional[TextBlock]:
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
        returned_tb = TextBlock.model_validate(rows[0])
        return returned_tb

    async def get_text_blocks_by_entity(self, entity_id: int) -> List[TextBlock]:
        """
        Get all text blocks belonging to a specific entity

        Parameters:
        - entity_id (int): id of the entity

        Returns:
        List[PartialTextBlock]: list of text blocks
        """
        sql = "SELECT * FROM text_blocks WHERE entity_id = %(entity_id)s"
        rows = await self.db.execute(sql, {"entity_id": entity_id})
        adapter = TypeAdapter(List[TextBlock])
        return adapter.validate_python(rows)

    async def update_text_block(self, text_block_id: int, text_block_patch: PartialTextBlock) -> Optional[TextBlock]:
        """
        Update a text block with new data

        Parameters:
        - text_block_id (int): id of the text block to update
        - text_block_patch (PartialTextBlock): fields to update

        Returns:
        PartialTextBlock: the updated text block or None if not found
        """
        # Get old position
        old_position_sql = "SELECT position, entity_id FROM text_blocks WHERE id = %(id)s"
        old_position_rows = await self.db.execute(old_position_sql, {"id": text_block_id})
        if not old_position_rows:
            return None
        old_position = old_position_rows[0]["position"]
        entity_id = old_position_rows[0]["entity_id"]

        # If position is changed, increments the position of other blocks
        new_position = text_block_patch.position
        if new_position is not None and new_position != old_position:
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
        returned_tb = TextBlock.model_validate(rows[0])
        return returned_tb
    
    async def get_position(self, text_block_id: int) -> Optional[int]:
        """
        return the position of a text_block
        
        Parameters:
        - text_block_id (int): the text_block's id
        
        Returns:
        int: the position
        """
        sql = "SELECT position FROM text_block WHERE id = %(tb_id)s"
        params = {"tb_id": text_block_id}
        rows = await self.db.execute(sql, params)
        if not rows:
            return None
        return PartialTextBlock.model_validate(rows[0]).position
    
    async def update_multiple_text_block(self, text_blocks: List[PartialTextBlock]) -> List[TextBlock]:
        sql = (
            "UPDATE text_block SET "
            "title = COALESCE(%(title)s) "
            "content = COALESCE(%(content)s) "
            "WHERE id = %(id)s "
            "RETURNING *")
        params = [{"title": tb.title, "content": tb.content, "id": tb.id} for tb in text_blocks]
        rows = await self.db.execute_many(sql, params)
        adapter = TypeAdapter(List[TextBlock])
        return adapter.validate_python(rows)
    
    async def move_multiple_tb(self, text_blocks: List[MovingTextBlock]) -> List[TextBlock]:
        sql = (
            "UPDATE text_blocks"
                "SET position = CASE"
                    "WHEN id = %(text_block_id)s THEN %(new_position)s"
                    "WHEN position >= %(new_position)s AND position < %(old_position)s THEN position + 1"
                    "WHEN position > %(old_position)s AND position <= %(new_position)s THEN position - 1"
                    "ELSE position"
                "END"
                "WHERE id IN ("
                    "SELECT id FROM text_blocks"
                    "WHERE entity_id = %(entity_id)s"
                    "AND position BETWEEN LEAST(%(new_position)s, %(old_position)s) AND GREATEST(%(new_position)s, %(old_position)s)"
                ")"
            "RETURNING *;"
        )

        params = [{
            "text_block_id": tb.id, 
            "new_position": tb.new_position, 
            "old_position":  tb.old_position, 
            "entity_id": tb.entity_id
            } 
            for tb in text_blocks]
        rows = await self.db.execute_many(sql, params)
        adapter = TypeAdapter(List[TextBlock])
        return adapter.validate_python(rows)
        

    async def delete_text_block(self, text_block_id: int) -> Optional[TextBlock]:
        """
        Delete a text block from the database

        Parameters:
        - text_block_id (int): id of the text block to delete

        Returns:
        bool: True if deleted, False otherwise
        """
        
        sql = "DELETE FROM text_blocks WHERE id = %(id)s RETURNING *"
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
    
    async def delete_multiple_text_blocks(self, tb_ids: Tuple[int, ...]) -> Optional[List[TextBlock]]:
        """
        Delete multiple text blocks from the database. Mainly used whene user change an entity
        
        Parameters:
        - tb_ids (tuple): text_blocks' ids the user want to delete
        
        Returns:
        Optional[List[TextBlock]]: the text_blocks deleted
        """
        sql = "DELETE FROM text_blocks WHERE id IN %(tb_ids)s RETURNING id"
        deleted_rows = await self.db.execute(sql, params={"tb_ids": tb_ids})
        if not deleted_rows:
            return None
        adapter = TypeAdapter(List[TextBlock])
        deleted = adapter.validate_python(deleted_rows)
        return deleted
    
    async def pull_down_text_blocks_for_entity(self, entity_id):
        """
        Set all position of texts blocks at the minimum respecting the order
        """
        sql = (
            "WITH ranked_blocks AS ("
                "SELECT"
                    "id,"
                    "ROW_NUMBER() OVER (ORDER BY position) AS new_position"
                "FROM text_block"
                "WHERE entity_id = %(entity_id)s"
            ")"
            "UPDATE text_block"
            "SET position = ranked_blocks.new_position"
            "FROM ranked_blocks"
            "WHERE text_block.id = ranked_blocks.id;"
            )
        await self.db.execute(sql, {"entity_id": entity_id})

    async def create_multiple_text_blocks(self, text_blocks: List[InputTextBlock], creator_id: int) -> List[TextBlock]:
        """
        Create multiple textblocks at once
        
        Parameters:
        - text_blocks (List[TextBlocks]): The textblocks the user want to insert in database
        - creator_id (int): the creator's id
        
        Returns:
        Optional[List[TextBlock]]: The TextBlocks created
        """

        sql = """
            UPDATE text_blocks
            SET position = position + 1
            WHERE entity_id = %(entity_id)s AND position >= %(position)s;

            INSERT INTO text_blocks (title, content, position, creator_id, entity_id)
            VALUES (%(title)s, %(content)s, %(position)s, %(creator_id)s, %(entity_id)s)
            RETURNING *;
        """
        params: List[Dict] = []
        for tb in text_blocks:
            params.append({
                "title": tb.title, 
                "content": tb.content, 
                "position": tb.position, 
                "creator_id": creator_id, 
                "entity_id": tb.entity_id
                })

        rows = await self.db.execute_many(sql, params)
        adapter = TypeAdapter(List[TextBlock])
        return adapter.validate_python(rows)
            

