from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from src.models.user import UserToken
from src.models.universe import InputUniverse, PartialUniverse, Universe
from src.factory import get_factory

universe_router = APIRouter(prefix="/universe")
factory = get_factory()
universe_controller = factory.universe_controller

@universe_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_universe(
    req: Request,
    universe_data: InputUniverse,
):
    """
    Create a new universe
    """
    user: UserToken = req.state.user
    try:
        universe = await universe_controller.create_universe(universe_data, user.id)
        return universe
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@universe_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_universes() -> List[Universe]:
    """
    Returns all universes
    """
    try:
        universes = await universe_controller.get_all_universes()
        return universes
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@universe_router.get("/my-universes", status_code=status.HTTP_200_OK)
async def update_universe(req: Request) -> List[Universe]:
    """
    Returns all universes created by the user
    """
    user: UserToken = req.state.user
    try:
        universes = await universe_controller.get_universes_by_creator(user.id)
        return universes
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@universe_router.get("/{universe_id}", status_code=status.HTTP_200_OK)
async def get_universe_by_id(universe_id: int) -> Universe:
    """
    Returns the universe with the provided id
    """
    try:
        universe = await universe_controller.get_universe_by_id(universe_id)
        return universe
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@universe_router.get("/created-by/{user_id}", status_code=status.HTTP_200_OK)
async def update_universe(user_id: int) -> List[Universe]:
    """
    Returns all universes created by a user with the provided user id
    """
    try:
        universes = await universe_controller.get_universes_by_creator(user_id)
        return universes
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@universe_router.patch("/{universe_id}", status_code=status.HTTP_200_OK)
async def update_universe(universe_id: int, universe_patch: PartialUniverse) -> Universe:
    """
    Update a universe
    """
    try:
        updated_universe = await universe_controller.update_universe(universe_id, universe_patch)
        return updated_universe
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@universe_router.delete("/{universe_id}", status_code=status.HTTP_200_OK)
async def delete_universe(universe_id: int) -> Universe:
    """
    Delete a universe
    """
    try:
        deleted_universe = await universe_controller.delete_universe(universe_id)
        if deleted_universe is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"universe with it {universe_id} not found"
            )
        return deleted_universe
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@universe_router.get("/{universe_id}/entities", status_code=status.HTTP_200_OK)
async def get_universe_entities(
    req: Request,
    universe_id: int,
):
    """
    Récupère les entités d'un univers accessibles par l'utilisateur.
    """
    user: UserToken = req.state.user
    try:
        entities = await universe_controller.get_universe_entities(user, universe_id)
        return entities
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
