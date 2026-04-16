from fastapi import APIRouter, HTTPException, status, Response, Request
from models.entity import InputEntity, PartialEntity
from controllers.entity import EntityController
from factory import get_factory
from src.models.user import UserToken

entity_router = APIRouter(prefix="/entity")

factory = get_factory()
entity_controller: EntityController = factory.entity_controller

@entity_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_entity(entity_data: InputEntity, request: Request):
    user: UserToken = request.state.user
    try:
        return await entity_controller.create_entity(entity_data, user.id, entity_data.universe_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@entity_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_entities(request: Request):
    user: UserToken = request.state.user
    try:
        # Récupère toutes les entités (à adapter selon tes besoins)
        entities = await entity_controller.get_all_entities()
        return entities
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@entity_router.get("/{entity_id}", status_code=status.HTTP_200_OK)
async def get_entity(entity_id: int, request: Request):
    user: UserToken = request.state.user
    try:
        entity = await entity_controller.get_entity_by_id(entity_id)
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
            detail=str(e)
        )

@entity_router.patch("/{entity_id}", status_code=status.HTTP_200_OK)
async def update_entity(entity_id: int, entity_patch: PartialEntity, request: Request):
    user: UserToken = request.state.user
    try:
        updated_entity = await entity_controller.update_entity(entity_id, entity_patch)
        return updated_entity
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@entity_router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entity(entity_id: int, request: Request):
    user: UserToken = request.state.user
    try:
        success = await entity_controller.delete_entity(entity_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Entity with id {entity_id} not found or not allowed to delete"
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@entity_router.get("/{entity_id}/children", status_code=status.HTTP_200_OK)
async def get_entity_children(entity_id: int, request: Request):
    user: UserToken = request.state.user
    try:
        children = await entity_controller.get_entity_and_children(entity_id)
        return children
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@entity_router.get("/{entity_id}/direct_children", status_code=status.HTTP_200_OK)
async def get_entity_direct_children(entity_id: int, request: Request):
    user: UserToken = request.state.user
    try:
        children = await entity_controller.get_entity_direct_children(entity_id)
        return children
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@entity_router.get("/{entity_id}/parents", status_code=status.HTTP_200_OK)
async def get_entity_parents(entity_id: int, request: Request):
    user: UserToken = request.state.user
    try:
        parents = await entity_controller.get_entity_parents(entity_id)
        return parents
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@entity_router.get("/universe/{universe_id}/reader-access", status_code=status.HTTP_200_OK)
async def get_entities_where_user_has_reader_access(universe_id: int, request: Request):
    user: UserToken = request.state.user
    try:
        entities = await entity_controller.get_entities_where_user_has_reader_access(user.id, universe_id)
        return entities
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )