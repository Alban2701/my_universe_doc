from db_connection import DbConnection, get_db

class BaseRepository:
    def __init__(self):
        self.db: DbConnection = get_db()