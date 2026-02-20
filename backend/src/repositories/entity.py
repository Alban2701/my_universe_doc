from models.entity import Entity, InputEntity, PartialEntity
from db_connection import DbConnection
from typing import List, Optional

async def create_entity(entity: InputEntity, creator_id: int, universe_id: int, db: DbConnection) -> PartialEntity:
    """
    create a new entity in the database

    Parameters:
    - entity: InputEntity with name and optional parent
    - creator_id: id of the user creating the entity
    - universe_id: id of the universe where the entity belongs

    Returns:
    PartialEntity: the created entity
    """
    sql = (
        "INSERT INTO entities (name, not_discovered_name, parent, creator_id, universe_id) "
        "VALUES (%(name)s, %(not_discovered_name)s, %(parent)s, %(creator_id)s, %(universe_id)s) "
        "RETURNING *"
    )
    model_entity = entity.model_dump()
    model_entity["creator_id"] = creator_id
    model_entity["universe_id"] = universe_id
    if "not_discovered_name" not in model_entity or model_entity["not_discovered_name"] is None:
        model_entity["not_discovered_name"] = "???"
    rows = await db.execute(sql, model_entity)
    returned_entity = PartialEntity.model_validate(rows[0])
    return returned_entity


async def get_entity_by_id(entity_id: int, db: DbConnection) -> Optional[PartialEntity]:
    """
    get an entity by its id

    Parameters:
    - entity_id (int): id of the entity

    Returns:
    PartialEntity or None if not found
    """
    sql = "SELECT * FROM entities WHERE id = %(id)s"
    rows = await db.execute(sql, {"id": entity_id})
    if not rows:
        return None
    returned_entity = PartialEntity.model_validate(rows[0])
    return returned_entity


async def get_entities_by_universe(universe_id: int, db: DbConnection) -> List[PartialEntity]:
    """
    get all entities belonging to a universe

    Parameters:
    - universe_id (int): id of the universe

    Returns:
    List[PartialEntity]: list of entities
    """
    sql = "SELECT * FROM entities WHERE universe_id = %(universe_id)s"
    rows = await db.execute(sql, {"universe_id": universe_id})
    return [PartialEntity.model_validate(row) for row in rows]


async def update_entity(entity_id: int, entity_patch: PartialEntity, db: DbConnection) -> Optional[PartialEntity]:
    """
    update an entity with new data

    Parameters:
    - entity_id (int): id of the entity to update
    - entity_patch (PartialEntity): fields to update

    Returns:
    PartialEntity: the updated entity or None if not found
    """
    sql = (
        "UPDATE entities SET "
        "name = COALESCE(%(name)s, name), "
        "not_discovered_name = COALESCE(%(not_discovered_name)s, not_discovered_name), "
        "parent = COALESCE(%(parent)s, parent), "
        "updated_at = NOW() "
        "WHERE id = %(id)s "
        "RETURNING *"
    )
    model_patch = entity_patch.model_dump()
    model_patch["id"] = entity_id
    rows = await db.execute(sql, model_patch)
    if not rows:
        return None
    returned_entity = PartialEntity.model_validate(rows[0])
    return returned_entity


async def delete_entity(entity_id: int, db: DbConnection) -> bool:
    """
    delete an entity from the database

    Parameters:
    - entity_id (int): id of the entity to delete

    Returns:
    bool: True if deleted, False otherwise
    """
    sql = "DELETE FROM entities WHERE id = %(id)s RETURNING id"
    rows = await db.execute(sql, {"id": entity_id})
    return bool(rows)
