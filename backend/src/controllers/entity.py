from fastapi import HTTPException, status
from typing import List, Optional
from models.entity import Entity, InputEntity, PartialEntity
from src.services.entity import EntityService

class EntityController:
    def __init__(self, entity_service: EntityService):
        self.entity_service = entity_service

    async def get_all_entities(self) -> List[Entity]:
        try:
            return await self.entity_service.get_all_entities()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get all entities: {str(e)}"
            )

    async def create_entity(self, entity: InputEntity, creator_id: int, universe_id: int) -> Entity:
        try:
            return await self.entity_service.create_entity(entity, creator_id, universe_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create entity: {str(e)}"
            )

    async def get_entity_by_id(self, entity_id: int) -> Optional[PartialEntity]:
        try:
            entity = await self.entity_service.get_entity_by_id(entity_id)
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

    async def get_entities_by_universe(self, universe_id: int) -> List[PartialEntity]:
        try:
            return await self.entity_service.get_entities_by_universe(universe_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get entities by universe: {str(e)}"
            )

    async def update_entity(self, entity_id: int, entity_patch: PartialEntity) -> Optional[PartialEntity]:
        try:
            updated_entity = await self.entity_service.update_entity(entity_id, entity_patch)
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
        try:
            success = await self.entity_service.delete_entity(entity_id)
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
        try:
            return await self.entity_service.get_entity_and_children(entity_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get entity and children: {str(e)}"
            )

    async def get_entity_direct_children(self, entity_id: int) -> List[Entity]:
        try:
            return await self.entity_service.get_entity_direct_children(entity_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get entity direct children: {str(e)}"
            )

    async def get_entities_where_user_has_reader_access(self, user_id: int, universe_id: int) -> List[Entity]:
        try:
            return await self.entity_service.get_entities_where_user_has_reader_access(user_id, universe_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get entities where user has reader access: {str(e)}"
            )

    async def get_entity_parents(self, entity_id: int) -> List[Entity]:
        try:
            return await self.entity_service.get_entity_parents(entity_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get entity parents: {str(e)}"
            )