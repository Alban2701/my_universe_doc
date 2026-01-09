from models.text_bloc import InputTextBlock, PartialTextBlock
from db_connection import DbConnection
from typing import List, Optional


async def create_text_block(text_block: InputTextBlock, creator_id: int, db: DbConnection) -> PartialTextBlock:
    """
    create a new text block in the database

    Parameters:
    - text_block: InputTextBlock with title, content, entity_id
    - creator_id: id of the user creating the text block

    Returns:
    PartialTextBlock: the created text block
    """
    sql = (
        "INSERT INTO text_blocks (title, content, creator_id, entity_id) "
        "VALUES (%(title)s, %(content)s, %(creator_id)s, %(entity_id)s) "
        "RETURNING *"
    )
    model_tb = text_block.model_dump()
    model_tb["creator_id"] = creator_id
    rows = await db.execute(sql, model_tb)
    returned_tb = PartialTextBlock.model_validate(rows[0])
    return returned_tb


async def get_text_block_by_id(text_block_id: int, db: DbConnection) -> Optional[PartialTextBlock]:
    """
    get a text block by its id

    Parameters:
    - text_block_id (int): id of the text block

    Returns:
    PartialTextBlock or None if not found
    """
    sql = "SELECT * FROM text_blocks WHERE id = %(id)s"
    rows = await db.execute(sql, {"id": text_block_id})
    if not rows:
        return None
    returned_tb = PartialTextBlock.model_validate(rows[0])
    return returned_tb


async def get_text_blocks_by_entity(entity_id: int, db: DbConnection) -> List[PartialTextBlock]:
    """
    get all text blocks belonging to a specific entity

    Parameters:
    - entity_id (int): id of the entity

    Returns:
    List[PartialTextBlock]: list of text blocks
    """
    sql = "SELECT * FROM text_blocks WHERE entity_id = %(entity_id)s"
    rows = await db.execute(sql, {"entity_id": entity_id})
    return [PartialTextBlock.model_validate(row) for row in rows]


async def update_text_block(text_block_id: int, text_block_patch: PartialTextBlock, db: DbConnection) -> Optional[PartialTextBlock]:
    """
    update a text block with new data

    Parameters:
    - text_block_id (int): id of the text block to update
    - text_block_patch (PartialTextBlock): fields to update

    Returns:
    PartialTextBlock: the updated text block or None if not found
    """
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
    rows = await db.execute(sql, model_patch)
    if not rows:
        return None
    returned_tb = PartialTextBlock.model_validate(rows[0])
    return returned_tb


async def delete_text_block(text_block_id: int, db: DbConnection) -> bool:
    """
    delete a text block from the database

    Parameters:
    - text_block_id (int): id of the text block to delete

    Returns:
    bool: True if deleted, False otherwise
    """
    sql = "DELETE FROM text_blocks WHERE id = %(id)s RETURNING id"
    rows = await db.execute(sql, {"id": text_block_id})
    return bool(rows)
