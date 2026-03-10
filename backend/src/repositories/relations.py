from db_connection import DbConnection
from typing import List, Optional
from pydantic import TypeAdapter
from src.models.enums import UserEntityRole
from src.utils.model_validator import model_validate_list
from src.models.relations import UserEntity

async def get_user_entities_by_user_id(user_id: int, db: DbConnection) -> list[UserEntity]:
    """
    Get all user_entity relationships from user_id
    
    Parameters:
    -  user_id (int): the user's id
    
    Returns:
    list[UserEntity]: The entities the user has access
    """
    sql = ("SELECT * FROM user_entity WHERE user_id = %{user_id}s")
    params = {"user_id": user_id}
    rows = await db.execute(sql, params)
    adapter = TypeAdapter(list[UserEntity])
    return adapter.validate_python(rows)


async def get_user_entity_in_universe_by_user_id(user_id: int, universe_id: int, role: UserEntityRole, db: DbConnection) -> list[UserEntity]:
    """
    get the UserEntity rows for one universe
    
    Parameters:
    - user_id (int): the user's id
    - universe_id (int): the universe's id
    - db: the db's pool 
    
    Returns:
    list[UserEntity]: The UserEntity rows in this universe for this user
    """
    sql = (
        "SELECT ue.* FROM user_entity as ue "
        "JOIN entities as e "
        "ON ue.entity_id = e.id "
        "WHERE e.universe_id = %{universe_id}s "
        "AND ue.user_id = %{user_id}s" \
        "AND ue.role = %{role}s"
    )
    params = {
        "user_id": user_id,
        "universe_id": universe_id,
        "role": role
    }
    rows = await db.execute(sql, params)    
    adapter = TypeAdapter(list[UserEntity])
    return adapter.validate_python(rows)