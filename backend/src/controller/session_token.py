from datetime import datetime, timedelta
from utils.token_creator import create_token
from db_connection import DbConnection

async def create_session_token(user_id: int, db: DbConnection, expires_in_days: int = 7, nb_bytes: int = 32):
    """
    create a session token for a user 
    
    Parameters:
    - user_id (int): the id of the user who is logged_in
    - db (DbConnection): the db to connect to
    - expires_in_hours(int): expire time
    """

    token = create_token(nb_bytes=nb_bytes)
    expires_at = datetime.now() + timedelta(days=expires_in_days)

    sql = ("INSERT INTO session_token (value, user_id, expires_at, updated_at)"
    " VALUES (%(value)s, %(user_id)s, %(expires_at)s, %(updated_at)s)"
    "RETURNING id, value, user_id, created_at, updated_at, expires_at")
    params = {
        "value": token,
        "user_id": user_id,
        "expires_at": expires_at,
        "updated_at": datetime.now()
    }
    row = await db.execute(sql, params)
    return row[0]

async def get_token_by_user_id(user_id: int, db: DbConnection):
    """
    Get a token thanks to a user_id
    
    Parameters:
    -  user_id(int): the id of the user we are checking
    - db(DbConnection): the database info
    
    """
    sql = ("SELECT * from session_token WHERE user_id = %(user_id)s;")
    params = {"user_id": user_id}
    row = await db.execute(sql, params)
    return row[0]

async def update_expires_date_token(user_id: int, db: DbConnection, expires_in_days: int = 7):
    """
    update the expire_date of a token
    
    Parameters:
    -  user_id(int): the id of the user we are checking
    - db(DbConnection): the database info
    
    """
    expires_at = datetime.now() + timedelta(hours=expires_in_days)
    sql = ("UPDATE session_token"
    "expires_at = %(expires_at)s"
    "WHERE user_id = %(user_id)s;")
    params = {"expires_at": expires_at, "user_id": user_id}
    row = await db.execute(sql, params)
    return row[0]

async def delete_session_token(user_id: int, db: DbConnection):
    """
    delete a session_token
    
    Parameters:
    - user_id(int): the user's id who is beeing disconnected
    - db(DbCOnnection): the database info
    """

    sql = ("DELETE session_token WHERE user_id = %(user_id)s;")
    params = {"user_id" : user_id}
    row = await db.execute(sql, params)
    return row[0]

async def delete_expired_token(db: DbConnection):
    """
    delete every expired session_token
    
    Parameters:
    - db(DbConnection): the database info
    """
    sql = ("DELETE session_token WHERE expires_at < NOW();")
    db.execute(sql)
    return