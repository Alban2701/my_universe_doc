from src.db_connection import DbConnection
from src.models.entity import Entity, InputEntity, PartialEntity
from src.models.enums import UserEntityRole
import src.repositories.entity as rentity
from src.repositories.relations import get_user_entity_in_universe_by_user_id

async def get_entity_and_children(entity_id: int, db: DbConnection) -> list[Entity]:
    """
    get an entity and all its children
    
    Parameters:
    - entity_id (int): the entity's id
    - db (DbConnection): the db's pool
    
    Returns:
    list[Entity]: The entity and its children
    """
    entities = await rentity.get_entity_and_children(entity_id, db)
    return entities

async def get_entity_accessed_by_user_as_admin(user_id: int, universe_id: int, db: DbConnection) -> list[Entity]:
    """
    Get all the entities the user has access in an universe as entity administrator
    
    Parameters:
    - user_id (int): the user's id
    - universe_id (int): the universe's id
    - db (DbConnection): The db's pool
    
    Returns:
    list[Entity]: The entities the user can access
    """
    user_entities = await get_user_entity_in_universe_by_user_id(user_id, universe_id, UserEntityRole.administrator, db)
    entities: list[Entity] = []
    for relation in user_entities:
        existing_ids = {e.id for e in entities}
        new_entities: list[Entity] = await get_entity_and_children(relation.entity_id)
        entities.extend(n for n in new_entities if n.id not in existing_ids)
    return entities

async def get_entity_accessed_by_user_as_editor(user_id: int, universe_id: int, db: DbConnection) -> list[Entity]:
    """
    Get all the entities the user has access as editor in an universe
    
    Parameters:
    - user_id (int): the user's
    
    Returns:
    list[Entity]: The entities the user can access as editor
    """

    user_entities = await get_user_entity_in_universe_by_user_id(user_id, universe_id, UserEntityRole.editor, db)
    entities: list[Entity] = []
    for relation in user_entities:
        existing_ids = {e.id for e in entities}
        new_entities: list[Entity] = await rentity.get_entity_by_id(relation.entity_id)
        entities.extend(n for n in new_entities if n.id not in existing_ids)
    return entities

async def get_entity_accessed_by_user_as_reader(user_id: int, universe_id: int, db: DbConnection) -> list[Entity]:
    """
    Get all the entities the user has access as reader in an universe
    
    Parameters:
    - user_id (int): the user's
    
    Returns:
    list[Entity]: The entities the user can access as reader
    """

    user_entities = await get_user_entity_in_universe_by_user_id(user_id, universe_id, UserEntityRole.editor, db)
    entities: list[Entity] = []
    for relation in user_entities:
        existing_ids = {e.id for e in entities}
        new_entities: list[Entity] = await rentity.get_entity_by_id(relation.entity_id)
        entities.extend(n for n in new_entities if n.id not in existing_ids)
    return entities