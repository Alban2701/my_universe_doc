from models.user import User, InputUser, PartialUser
from db_connection import DbConnection
from pydantic import EmailStr
from models.user import PartialUser

async def register(user: InputUser, db: DbConnection) -> User:
    """
    register a new user in the database
    
    Parameters:
    - user: the user to register
    
    Returns:
    User: the user registered
    """
    sql = ("INSERT INTO users (email, password, username, bio, picture)"
            " VALUES (%(email)s, %(password)s, %(username)s, %(bio)s, %(picture)s)"
            " RETURNING id, username, email")
    model_user = user.model_dump()
    print(model_user)
    rows = await db.execute(sql, model_user)
    returned_user = PartialUser.model_validate(rows[0])
    return returned_user

async def get_user_by_id(id: int, db: DbConnection) -> User | None:
    """
    get a user in database with the provided id
    
    Parameters:
    - id (int): the id of the user to be get
    
    Returns:
    User: the user get
    """
    sql = "SELECT * from users WHERE id = %(id)s"
    rows = await db.execute(sql, {"id": id})
    returned_user = PartialUser.model_validate(rows[0])
    return returned_user

async def get_user_by_email(email: EmailStr, db: DbConnection) -> User:
    """
    get a user in database with the provided email
    
    Parameters:
    - email (EmailStr): the email of the user to be get
    
    Returns:
    User: the user get
    """
    sql = "SELECT * from users WHERE email = %(email)s"
    rows =await db.execute(sql, {"email": email})
    returned_user = PartialUser.model_validate(rows[0])
    return returned_user

async def get_user_with_session_token(token_value: str, db: DbConnection) -> User:
    """
    take a session_token_value and return a user thanks to it

    Parameters:
    - session_token(str): the value of the session_token
    
    Returns:
    User: The user get
    """
    sql = ("SELECT * from users as u "
        "JOIN session_token as s "
        "ON u.id = s.user_id "
        "WHERE s.value = %(token_value)s")
    params = {"token_value": token_value}
    rows = await db.execute(sql, params)
    returned_user = PartialUser.model_validate(rows[0])

    return returned_user