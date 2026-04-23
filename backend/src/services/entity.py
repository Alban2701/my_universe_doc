from typing import List, Optional
from models.entity import Entity, InputEntity, PartialEntity
from fastapi import HTTPException, status

from src.repositories.entity import EntityRepository

class EntityService:
    def __init__(self, entity_repository: EntityRepository):
        self.entity_repository = entity_repository

    async def get_all_entities(self) -> List[Entity]:
        """
        Return all existing entities

        Returns:
        List[Entity]: The existing entities
        """
        try:
            return await self.entity_repository.get_all_entities()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get all entities: {str(e)}"
            )

    async def create_entity(self, entity: InputEntity, creator_id: int, universe_id: int) -> Entity:
        """
        Create a new entity in the database

        Parameters:
        - entity: InputEntity with name and optional parent
        - creator_id: id of the user creating the entity
        - universe_id: id of the universe where the entity belongs

        Returns:
        Entity: the created entity
        """
        try:
            return await self.entity_repository.create_entity(entity, creator_id, universe_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create entity: {str(e)}"
            )

    async def get_entity_by_id(self, entity_id: int) -> Optional[PartialEntity]:
        """
        Get an entity by its id

        Parameters:
        - entity_id (int): id of the entity

        Returns:
        PartialEntity or None if not found
        """
        try:
            entity = await self.entity_repository.get_entity_by_id(entity_id)
            if entity is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Entity with id {entity_id} not found"
                )
            return entity
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get entity: {str(e)}"
            )

    async def get_entities_by_universe(self, universe_id: int) -> List[Entity]:
        """
        Get all entities belonging to a universe

        Parameters:
        - universe_id (int): id of the universe

        Returns:
        List[Entity]: list of entities
        """
        try:
            return await self.entity_repository.get_entities_by_universe(universe_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get entities by universe: {str(e)}"
            )

    async def update_entity(self, entity_id: int, entity_patch: PartialEntity) -> Optional[Entity]:
        """
        Update an entity with new data

        Parameters:
        - entity_id (int): id of the entity to update
        - entity_patch (Entity): fields to update

        Returns:
        Entity: the updated entity or None if not found
        """
        try:
            updated_entity = await self.entity_repository.update_entity(entity_id, entity_patch)
            if updated_entity is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Entity with id {entity_id} not found"
                )
            return updated_entity
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update entity: {str(e)}"
            )

    async def delete_entity(self, entity_id: int) -> bool:
        """
        Delete an entity from the database

        Parameters:
        - entity_id (int): id of the entity to delete

        Returns:
        bool: True if deleted, False otherwise
        """
        try:
            success = await self.entity_repository.delete_entity(entity_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Entity with id {entity_id} not found"
                )
            return success
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete entity: {str(e)}"
            )

    async def get_entity_and_children(self, entity_id: int) -> List[Entity]:
        """
        Gets the entity's children recursively

        Parameters:
        - entity_id (int): id of the entity

        Returns:
        List[Entity]: a list of all the entity and its children
        """
        try:
            return await self.entity_repository.get_entity_and_children(entity_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get entity and children: {str(e)}"
            )

    async def get_entity_direct_children(self, entity_id: int) -> List[Entity]:
        """
        Gets the entity's direct children

        Parameters:
        - entity_id (int): id of the entity

        Returns:
        List[Entity]: a list of the entity's direct children
        """
        try:
            return await self.entity_repository.get_entity_direct_children(entity_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get entity direct children: {str(e)}"
            )

    async def get_entities_where_user_has_reader_access(self, user_id: int, universe_id: int) -> List[Entity]:
        """
        For a universe, access to all entities the user has access to text_bloc in

        Parameters:
        - user_id (int): the user's id
        - universe_id (int): the universe the entities must be in

        Returns:
        List[Entity]: Entities the user has access as reader
        """
        try:
            return await self.entity_repository.get_entities_where_user_has_reader_access(user_id, universe_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get entities where user has reader access: {str(e)}"
            )

    async def get_entity_parents(self, entity_id: int) -> List[Entity]:
        """
        Returns recursively the parents of the entity until there is no more

        Parameters:
        - entity_id (int): the entity's id

        Returns:
        List[Entity]: The parents
        """
        try:
            return await self.entity_repository.get_entity_parents(entity_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get entity parents: {str(e)}"
            )