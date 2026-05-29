from db_connection import DbConnection, get_db


class BaseRepository:
    @property
    def db(self) -> DbConnection:
        return get_db()
