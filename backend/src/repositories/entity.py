from pydantic import TypeAdapter

from models.entity import Entity, InputEntity, PartialEntity
from db_connection import DbConnection
from typing import List, Optional

from src.utils.model_validator import model_validate_list

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
    return model_validate_list(Entity)


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

async def get_entity_and_children(entity_id: int, db: DbConnection) -> list[Entity]:
    """
    Gets the entity's children recursively 
    
    Parameters:
    - entity_id (int): 
    - db (DbConnection): the db's pool
    
    Returns:
    list[Entity]: a list of all the entity and its children.
    """
    
    sql = (
        "WITH RECURSIVE children_entity AS ( "
        "SELECT * "
        "FROM entities "
        "WHERE id = %(entity_id)s"
        "UNION ALL "
        "SELECT * "
        "FROM entities e "
        "JOIN children_entity ea ON e.parent = ea.id)"
        "SELECT * FROM children_entity"
    )
    params = {"entity_id": entity_id}
    rows = await db.execute(sql, params)
    adaptater = TypeAdapter(list[Entity])
    return adaptater.validate_python(rows)


async def get_entities_where_user_has_reader_acces(user_id: int, universe_id: int, db: DbConnection) -> list[Entity]:
    """
    For a universe, access to all entities the user has access to text_bloc in.
    
    Parameters:
    - user_id (int): the user's id
    - universe_id (int): the universe the entities must be in
    - db (DbConnectin): the db's pool
    
    Returns:
    list[Entity]: Entities the user has access has reader
    """
    sql = (
        "SELECT e.* FROM entities as e " \
        "JOIN text_blocks tb ON tb.entity_id = e.id " \
        "JOIN user_text_block utb ON utb.text_block_id = tb.id " \
        "WHERE utb.user_id = %(user_id)s " \
        "AND e.universe_id = %(universe_id)s"
    )
    params = {
        "user_id": user_id,
        "universe_id": universe_id
    }
    rows = await db.execute(sql, params)
    adaptater = TypeAdapter(list[Entity])
    return adaptater.validate_python(rows)
