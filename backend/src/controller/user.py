from models.user import User, InputUser, PartialUser
from db_connection import DbConnection
from pydantic import EmailStr

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
            " RETURNING (id, username, email)")
    model_user = user.model_dump()
    print(model_user)
    row = await db.execute(sql, model_user)
    return row[0]

async def get_user_by_id(id: int, db: DbConnection) -> User:
    """
    get a user in database with the provided id
    
    Parameters:
    - id (int): the id of the user to be get
    
    Returns:
    User: the user get
    """
    sql = "SELECT * from users WHERE id = %(id)s"
    row = await db.execute(sql, {"id": id})
    return  row[0]

async def get_user_by_email(email: EmailStr, db: DbConnection) -> User:
    """
    get a user in database with the provided email
    
    Parameters:
    - email (EmailStr): the email of the user to be get
    
    Returns:
    User: the user get
    """
    sql = "SELECT * from users WHERE email = %(email)s"
    print(sql)
    row =await db.execute(sql, {"email": email})
    return row[0] 