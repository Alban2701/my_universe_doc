from src.db_connection import DbConnection
from src.repositories import user as ruser

async def is_user_superadmin_universe(user_id: int, universe_id: int, db: DbConnection) -> bool:
    """
    Check if the user is superadmin or creator of a universe
    
    Parameters:
    - user_id (int): the user's id
    - universe_id (int): the universe's id
    - db: the db's pool
    
    Returns:
    bool: True if the user is a superadmin or the creator of the universe, else False
    """
    role = await ruser.get_user_admin_rights(user_id, universe_id, db)
    return bool(role)