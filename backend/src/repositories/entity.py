from pydantic import TypeAdapter
from models.entity import Entity, InputEntity, PartialEntity
from typing import List, Optional
from src.repositories.base_repository import BaseRepository
from src.utils.unoptional import unoptional

class EntityRepository(BaseRepository):
    async def get_all_entities(self) -> List[Entity]:
        """
        Return all existing entities

        Returns:
        List[Entity]: The existing entities
        """
        sql = "SELECT * FROM entities"
        rows = await self.db.execute(sql)
        adapter = TypeAdapter(List[Entity])
        return adapter.validate_python(rows)

    async def create_entity(self, entity: InputEntity, creator_id: int, universe_id: int) -> Entity:
        """
        Create a new entity in the database.
        If not_discovered_name is not set, then set it up by default as '???'

        Parameters:
        - entity: InputEntity with name and optional parent
        - creator_id: id of the user creating the entity
        - universe_id: id of the universe where the entity belongs

        Returns:
        Entity: the created entity
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
        rows = unoptional(await self.db.execute(sql, model_entity))
        returned_entity = Entity.model_validate(rows[0])
        return returned_entity

    async def get_entity_by_id(self, entity_id: int) -> Optional[PartialEntity]:
        """
        Get an entity by its id

        Parameters:
        - entity_id (int): id of the entity

        Returns:
        PartialEntity or None if not found
        """
        sql = "SELECT * FROM entities WHERE id = %(id)s"
        rows = await self.db.execute(sql, {"id": entity_id})
        if not rows:
            return None
        returned_entity = PartialEntity.model_validate(rows[0])
        return returned_entity

    async def get_entities_by_universe(self, universe_id: int) -> List[PartialEntity]:
        """
        Get all entities belonging to a universe

        Parameters:
        - universe_id (int): id of the universe

        Returns:
        List[PartialEntity]: list of entities
        """
        sql = "SELECT * FROM entities WHERE universe_id = %(universe_id)s"
        rows = await self.db.execute(sql, {"universe_id": universe_id})
        adapter = TypeAdapter(List[PartialEntity])
        return adapter.validate_python(rows)

    async def update_entity(self, entity_id: int, entity_patch: PartialEntity) -> Optional[PartialEntity]:
        """
        Update an entity with new data

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
        rows = await self.db.execute(sql, model_patch)
        if not rows:
            return None
        returned_entity = PartialEntity.model_validate(rows[0])
        return returned_entity

    async def delete_entity(self, entity_id: int) -> bool:
        """
        Delete an entity from the database

        Parameters:
        - entity_id (int): id of the entity to delete

        Returns:
        bool: True if deleted, False otherwise
        """
        sql = "DELETE FROM entities WHERE id = %(id)s RETURNING id"
        rows = await self.db.execute(sql, {"id": entity_id})
        return bool(rows)

    async def get_entity_and_children(self, entity_id: int) -> List[Entity]:
        """
        Gets the entity's children recursively

        Parameters:
        - entity_id (int): id of the entity

        Returns:
        List[Entity]: a list of all the entity and its children
        """
        sql = (
            "WITH RECURSIVE children_entity AS ( "
            "SELECT * FROM entities WHERE id = %(entity_id)s "
            "UNION ALL "
            "SELECT e.* FROM entities e "
            "JOIN children_entity ce ON e.parent = ce.id) "
            "SELECT * FROM children_entity"
        )
        params = {"entity_id": entity_id}
        rows = await self.db.execute(sql, params)
        adapter = TypeAdapter(List[Entity])
        return adapter.validate_python(rows)

    async def get_entity_direct_children(self, entity_id: int) -> List[Entity]:
        """
        Gets the entity's direct children

        Parameters:
        - entity_id (int): id of the entity

        Returns:
        List[Entity]: a list of the entity's direct children
        """
        sql = "SELECT * FROM entities WHERE parent = %(entity_id)s"
        params = {"entity_id": entity_id}
        rows = await self.db.execute(sql, params)
        adapter = TypeAdapter(List[Entity])
        return adapter.validate_python(rows)

    async def get_entities_where_user_has_reader_access(self, user_id: int, universe_id: int) -> List[Entity]:
        """
        For a universe, access to all entities the user has access to text_bloc in

        Parameters:
        - user_id (int): the user's id
        - universe_id (int): the universe the entities must be in

        Returns:
        List[Entity]: Entities the user has access as reader
        """
        sql = (
            "SELECT e.* FROM entities as e "
            "JOIN text_blocks tb ON tb.entity_id = e.id "
            "JOIN user_text_block utb ON utb.text_block_id = tb.id "
            "WHERE utb.user_id = %(user_id)s "
            "AND e.universe_id = %(universe_id)s"
        )
        params = {
            "user_id": user_id,
            "universe_id": universe_id
        }
        rows = await self.db.execute(sql, params)
        adapter = TypeAdapter(List[Entity])
        return adapter.validate_python(rows)

    async def get_entity_parents(self, entity_id: int) -> List[Entity]:
        """
        Returns recursively the parents of the entity until there is no more

        Parameters:
        - entity_id (int): the entity's id

        Returns:
        List[Entity]: The parents
        """
        sql = (
            "WITH RECURSIVE entity_parents AS ( "
            "SELECT *, 0 AS level FROM entities WHERE id = %(id)s "
            "UNION ALL "
            "SELECT e.*, ep.level + 1 FROM entities e "
            "JOIN entity_parents ep ON e.id = ep.parent "
            ") "
            "SELECT * FROM entity_parents ORDER BY level DESC"
        )
        params = {"id": entity_id}
        rows = await self.db.execute(sql, params)
        adapter = TypeAdapter(List[Entity])
        return adapter.validate_python(rows)