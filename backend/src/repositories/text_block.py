from pydantic import TypeAdapter
from psycopg.rows import dict_row

from src.models.text_block import (
    InputTextBlock,
    MovingTextBlock,
    PartialTextBlock,
    TextBlock,
)
from typing import Any, Dict, List, Optional, Tuple
from src.repositories.base_repository import BaseRepository
from src.utils.unoptional import unoptional


class TextBlockRepository(BaseRepository):
    async def create_text_block(
        self, text_block: InputTextBlock, creator_id: int
    ) -> TextBlock:
        """
        Create a new text block in the database

        Parameters:
        - text_block: InputTextBlock with title, content, entity_id
        - creator_id: id of the user creating the text block

        Returns:
        PartialTextBlock: the created text block
        """
        # Two-phase shift to dodge UNIQUE(entity_id, position) row-by-row:
        # Phase 1 negates affected positions (they become unique negatives),
        # Phase 2 restores them shifted by +1 (negatives -> positives, no
        # overlap with the source set, no collisions). Then the INSERT lands
        # in the freshly vacated slot.
        phase1_sql = (
            "UPDATE text_blocks SET position = -position "
            "WHERE entity_id = %(entity_id)s AND position >= %(position)s"
        )
        phase2_sql = (
            "UPDATE text_blocks SET position = -position + 1 "
            "WHERE entity_id = %(entity_id)s AND position < 0"
        )
        insert_sql = (
            "INSERT INTO text_blocks (title, content, position, creator_id, entity_id) "
            "VALUES (%(title)s, %(content)s, %(position)s, %(creator_id)s, %(entity_id)s) "
            "RETURNING *"
        )

        model_tb = text_block.model_dump()
        model_tb["creator_id"] = creator_id

        rows = unoptional(
            await self.db.execute_transactional(
                [
                    (phase1_sql, model_tb),
                    (phase2_sql, model_tb),
                    (insert_sql, model_tb),
                ]
            )
        )
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

    async def update_text_block(
        self, text_block_id: int, text_block_patch: PartialTextBlock
    ) -> Optional[TextBlock]:
        """
        Update a text block with new data

        Parameters:
        - text_block_id (int): id of the text block to update
        - text_block_patch (PartialTextBlock): fields to update

        Returns:
        PartialTextBlock: the updated text block or None if not found
        """
        # Get old position
        old_position_sql = (
            "SELECT position, entity_id FROM text_blocks WHERE id = %(id)s"
        )
        old_position_rows = await self.db.execute(
            old_position_sql, {"id": text_block_id}
        )
        if not old_position_rows:
            return None
        old_position = old_position_rows[0]["position"]
        entity_id = old_position_rows[0]["entity_id"]

        # If position is changed, increments the position of other blocks
        new_position = text_block_patch.position
        if new_position is not None and new_position != old_position:
            # Two-phase update to avoid violating UNIQUE(entity_id, position)
            # mid-statement. Phase 1: park every block in the affected range at
            # its negated position (still unique, but out of the positive range,
            # so no row-level collision can happen during phase 2). Phase 2:
            # assign the final positions; sources are negative, targets are
            # positive, so no collisions either.
            phase1_sql = """
                UPDATE text_blocks
                SET position = -position
                WHERE entity_id = %(entity_id)s
                AND position BETWEEN LEAST(%(new_position)s, %(old_position)s)
                                 AND GREATEST(%(new_position)s, %(old_position)s)
            """
            phase2_sql = """
                UPDATE text_blocks
                SET
                    position = CASE
                        WHEN id = %(text_block_id)s THEN %(new_position)s
                        WHEN -position >= %(new_position)s AND -position < %(old_position)s THEN -position + 1
                        WHEN -position > %(old_position)s AND -position <= %(new_position)s THEN -position - 1
                        ELSE -position
                    END,
                    title = CASE
                        WHEN id = %(text_block_id)s THEN COALESCE(%(title)s, title)
                        ELSE title
                    END,
                    content = CASE
                        WHEN id = %(text_block_id)s THEN COALESCE(%(content)s, content)
                        ELSE content
                    END,
                    updated_at = CASE
                        WHEN id = %(text_block_id)s THEN NOW()
                        ELSE updated_at
                    END
                WHERE entity_id = %(entity_id)s AND position < 0
                RETURNING *
            """
            params = {
                "text_block_id": text_block_id,
                "new_position": new_position,
                "old_position": old_position,
                "entity_id": entity_id,
                "title": text_block_patch.title,
                "content": text_block_patch.content,
            }
            rows = await self.db.execute_transactional(
                [(phase1_sql, params), (phase2_sql, params)]
            )
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
        # The position-change branch returns several rows (all the shifted
        # blocks). Return the one matching the targeted id.
        target_row = next((row for row in rows if row["id"] == text_block_id), rows[0])
        returned_tb = TextBlock.model_validate(target_row)
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

    async def update_multiple_text_block(
        self, text_blocks: List[PartialTextBlock]
    ) -> List[TextBlock]:
        sql = (
            "UPDATE text_blocks SET "
            "title = COALESCE(%(title)s, title), "
            "content = COALESCE(%(content)s, content), "
            "updated_at = NOW() "
            "WHERE id = %(id)s "
            "RETURNING *"
        )
        params = [
            {"title": tb.title, "content": tb.content, "id": tb.id}
            for tb in text_blocks
        ]
        rows = await self.db.execute_many(sql, params)
        adapter = TypeAdapter(List[TextBlock])
        return adapter.validate_python(rows)

    async def move_multiple_tb(
        self, text_blocks: List[MovingTextBlock]
    ) -> List[TextBlock]:
        # Apply moves one at a time, re-reading the current position from DB
        # before each swap. The client-provided `old_position` becomes stale
        # as soon as the first move shifts other blocks, so we cannot trust it.
        # Two-phase update (negate then assign) to avoid mid-statement UNIQUE
        # violations on (entity_id, position). The two phases run in the same
        # transaction because phase 2 must see phase 1's negations.
        phase1_sql = """
            UPDATE text_blocks
            SET position = -position
            WHERE entity_id = %(entity_id)s
            AND position BETWEEN LEAST(%(new_position)s, %(old_position)s)
                             AND GREATEST(%(new_position)s, %(old_position)s)
        """
        phase2_sql = """
            UPDATE text_blocks
            SET position = CASE
                WHEN id = %(text_block_id)s THEN %(new_position)s
                WHEN -position >= %(new_position)s AND -position < %(old_position)s THEN -position + 1
                WHEN -position > %(old_position)s AND -position <= %(new_position)s THEN -position - 1
                ELSE -position
            END
            WHERE entity_id = %(entity_id)s AND position < 0
            RETURNING *
        """
        current_position_sql = "SELECT position FROM text_blocks WHERE id = %(id)s"

        moved: List[TextBlock] = []
        for tb in text_blocks:
            current_rows = await self.db.execute(current_position_sql, {"id": tb.id})
            if not current_rows:
                continue
            current_position = current_rows[0]["position"]
            if current_position == tb.new_position:
                continue

            params = {
                "text_block_id": tb.id,
                "new_position": tb.new_position,
                "old_position": current_position,
                "entity_id": tb.entity_id,
            }
            rows = await self.db.execute_transactional(
                [(phase1_sql, params), (phase2_sql, params)]
            )
            if not rows:
                continue
            target_row = next((row for row in rows if row["id"] == tb.id), None)
            if target_row is not None:
                moved.append(TextBlock.model_validate(target_row))
        return moved

    async def delete_text_block(self, text_block_id: int) -> Optional[TextBlock]:
        """
        Delete a text block from the database

        Parameters:
        - text_block_id (int): id of the text block to delete

        Returns:
        bool: True if deleted, False otherwise
        """

        # Two-step: delete the row, then pull subsequent positions down by 1.
        # Both must be in the same transaction so we never leave a hole if the
        # second step fails.
        delete_sql = "DELETE FROM text_blocks WHERE id = %(id)s RETURNING *"
        reshift_sql = (
            "UPDATE text_blocks "
            "SET position = position - 1 "
            "WHERE position > %(position)s "
            "AND entity_id = %(entity_id)s"
        )

        # The reshift's params depend on the delete's RETURNING, so we cannot
        # use execute_transactional (which only forwards predefined params).
        # Drive the cursor ourselves on a single connection / single transaction.
        if self.db.pool is None:
            raise RuntimeError("Database not connected.")
        async with self.db.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                try:
                    await cur.execute(delete_sql, {"id": text_block_id})
                    deleted_rows = await cur.fetchall() if cur.description else []
                    if not deleted_rows:
                        await conn.rollback()
                        return None
                    deleted = TextBlock.model_validate(deleted_rows[0])
                    await cur.execute(
                        reshift_sql,
                        {
                            "position": deleted.position,
                            "entity_id": deleted.entity_id,
                        },
                    )
                    await conn.commit()
                    return deleted
                except Exception as e:
                    await conn.rollback()
                    raise RuntimeError(f"SQL Error: {str(e)}")

    async def delete_multiple_text_blocks(
        self, tb_ids: Tuple[int, ...]
    ) -> Optional[List[TextBlock]]:
        """
        Delete multiple text blocks from the database. Mainly used whene user change an entity

        Parameters:
        - tb_ids (tuple): text_blocks' ids the user want to delete

        Returns:
        Optional[List[TextBlock]]: the text_blocks deleted
        """
        sql = "DELETE FROM text_blocks WHERE id = ANY(%(tb_ids)s) RETURNING *"
        deleted_rows = await self.db.execute(sql, params={"tb_ids": list(tb_ids)})
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
            "WITH ranked_blocks AS ( "
            "SELECT "
            "id, "
            "ROW_NUMBER() OVER (ORDER BY position) AS new_position "
            "FROM text_blocks "
            "WHERE entity_id = %(entity_id)s "
            ") "
            "UPDATE text_blocks "
            "SET position = ranked_blocks.new_position "
            "FROM ranked_blocks "
            "WHERE text_blocks.id = ranked_blocks.id; "
        )
        await self.db.execute(sql, {"entity_id": entity_id})

    async def create_multiple_text_blocks(
        self, text_blocks: List[InputTextBlock], creator_id: int
    ) -> List[TextBlock]:
        """
        Create multiple textblocks at once

        Parameters:
        - text_blocks (List[TextBlocks]): The textblocks the user want to insert in database
        - creator_id (int): the creator's id

        Returns:
        Optional[List[TextBlock]]: The TextBlocks created
        """

        phase1_sql = (
            "UPDATE text_blocks SET position = -position "
            "WHERE entity_id = %(entity_id)s AND position >= %(position)s"
        )
        phase2_sql = (
            "UPDATE text_blocks SET position = -position + 1 "
            "WHERE entity_id = %(entity_id)s AND position < 0"
        )
        insert_sql = (
            "INSERT INTO text_blocks (title, content, position, creator_id, entity_id) "
            "VALUES (%(title)s, %(content)s, %(position)s, %(creator_id)s, %(entity_id)s) "
            "RETURNING *"
        )
        # Insert in ascending position order so that each per-row shift is
        # contained to existing blocks (not the ones we just inserted).
        sorted_blocks = sorted(text_blocks, key=lambda tb: tb.position)

        created: List[TextBlock] = []
        for tb in sorted_blocks:
            params = {
                "title": tb.title,
                "content": tb.content,
                "position": tb.position,
                "creator_id": creator_id,
                "entity_id": tb.entity_id,
            }
            rows = await self.db.execute_transactional(
                [
                    (phase1_sql, params),
                    (phase2_sql, params),
                    (insert_sql, params),
                ]
            )
            if rows:
                created.append(TextBlock.model_validate(rows[0]))
        return created
