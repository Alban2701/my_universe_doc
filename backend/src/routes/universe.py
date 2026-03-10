from typing import Dict

from fastapi import APIRouter, HTTPException, Response, status, Request, Depends
from models.universe import Universe, InputUniverse, PartialUniverse
import repositories.universe as runiverse
from src.controller.entity import get_entity_accessed_by_user_as_admin, get_entity_accessed_by_user_as_editor
from src.db_connection import DbConnection, get_db
from src.models.entity import Entity
from src.models.user import UserToken
import src.controller.user  as cuser
import src.repositories.entity as rentity


universe_router = APIRouter(prefix="/universe")

@universe_router.get("/all", status_code=status.HTTP_200_OK)
async def all_universes(db: DbConnection=Depends(get_db)) -> list[Universe]:
    """
    Returns all the universes. Admin only
    
    Parameters:
    -  db: The db's pool
    
    Returns:
    list[Universe]: all the universes
    """
    
    try:
        universes = await runiverse.get_all_universes(db)
        return universes
    except:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@universe_router.get("/{universe_id}", status_code=status.HTTP_200_OK)
async def get_universe(universe_id: int, db: DbConnection=Depends(get_db)) -> Universe:
    """
    Returns the universe with the provided id
    
    Parameters:
    - universe_id (int): the id of the universe asked
    - db (DbConnection): The db's pool
    
    Returns:
    Universe: The universe with the provided id
    """
    try:
        universe = await runiverse.get_universe_by_id(universe_id, db)
        return universe
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@universe_router.get("/", status_code=status.HTTP_200_OK)
async def get_my_universe(req: Request, db: DbConnection=Depends(get_db)) -> list[Universe]:
    """
    Returns the user's universes
    
    Parameters:
    - db (DbConnection): The db's pool
    
    Returns:
    list[Universe]: The user's universes
    """
    user: UserToken = req.state.user
    try:
        universes = await runiverse.get_universes_by_creator(user.id, db)
        return universes
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@universe_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_universe(req: Request, universe_data: InputUniverse, db: DbConnection=Depends(get_db)):
    """
    Create a universe with the provided informations
    
    Parameters:
    - req (Request): The Request Data, for getting the user data
    - universe_data (InputUniverse): The universe's information (name, description[optional])
    - db (DbConnection): The db's pool
    """
    
    user: UserToken = req.state.user
    try:
        await runiverse.create_universe(universe_data, user.id, db)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@universe_router.delete("/{universe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_universe(req: Request, universe_id: int, db: DbConnection=Depends(get_db)):
    """
    Delete a universe which the id is provided. Check if the user is the creator of this universe
    
    Parameters:
    - req (Request): The Request Data, for getting the user data
    - universe_id (int): the universe's id the user want to delete
    """
    user: UserToken = req.state.user
    try:
        universe: Universe | None = await runiverse.get_universe_by_id(universe_id, db)
        if not universe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Universe not found with the provided Id : {universe_id}")
        elif universe.creator_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The user is not the creator of the universe")
        else:
            await runiverse.delete_universe(universe_id, db)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@universe_router.patch("/{universe_id}", status_code=status.HTTP_200_OK)
async def update_universe(req: Request, universe_id: int, db: DbConnection=Depends(get_db)):
    """
    Update a universe with the provided id. Check if the user is the creator of this universe
    
    Parameters:
    - req (Request): The request Data, for getting the user's data
    - universe_id (int): The universe's id the user want to update
    - db (DbConnection): th db's pool
    """
    user: UserToken = req.state.user
    try:
        universe: Universe | None = await runiverse.get_universe_by_id(universe_id, db)
        if not universe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Universe not found with the provided Id : {universe_id}")
        elif universe.creator_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The user is not the creator of the universe")
        else:
            await runiverse.update_universe(universe_id, db)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return

@universe_router.get("/{universe_id}/entities", status_code=status.HTTP_200_OK)
async def get_universe_entities(req: Request, universe_id: int, db: DbConnection=Depends(get_db)) -> list[Entity] | Dict[str, list[Entity]]:
    """
    If the user is the creator of the universe or a superadmin, returns all the universe's entities. 
    Else, returns the entities the user can access.
    Parameters:
    - req (Request): The request Data, for getting the user's data
    - universe_id (int): The universe's id the user want to update
    - db (DbConnection): th db's pool
    
    Returns:
    list[Entity]: The entities the user can access
    """
    # raise NotImplementedError
    user: UserToken = req.state.user
    try:
        universe = await runiverse.get_universe_by_id(universe_id, db)
        if not universe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"universe_id": universe_id})
        elif await cuser.is_user_superadmin_universe(user.id, universe_id, db):
            entities = rentity.get_entities_by_universe(universe.id, db)
            return entities
        else:
            entities_as_admin = await get_entity_accessed_by_user_as_admin(user.id, universe.id, db)
            entities_as_editor = await get_entity_accessed_by_user_as_editor(user.id, universe.id, db)
            return {"as_editor": entities_as_editor,
                    "as_admin": entities_as_admin}
    
    except:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)