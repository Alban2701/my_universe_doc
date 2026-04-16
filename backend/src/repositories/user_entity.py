from typing import List
from pydantic import TypeAdapter
from src.models.enums import UserEntityRole
from src.models.relations import UserEntity
from src.repositories.base_repository import BaseRepository

class UserEntityRepository(BaseRepository):
    async def get_user_entities_by_user_id(self, user_id: int) -> List[UserEntity]:
        """
        Get all user_entity relationships from user_id

        Parameters:
        - user_id (int): the user's id

        Returns:
        List[UserEntity]: The entities the user has access to
        """
        sql = "SELECT * FROM user_entity WHERE user_id = %(user_id)s"
        params = {"user_id": user_id}
        rows = await self.db.execute(sql, params)
        adapter = TypeAdapter(List[UserEntity])
        return adapter.validate_python(rows)

    async def get_user_entity_in_universe_by_user_id(
        self, user_id: int, universe_id: int, role: UserEntityRole
    ) -> List[UserEntity]:
        """
        Get the UserEntity rows for one universe

        Parameters:
        - user_id (int): the user's id
        - universe_id (int): the universe's id
        - role (UserEntityRole): the role to filter by

        Returns:
        List[UserEntity]: The UserEntity rows in this universe for this user
        """
        sql = (
            "SELECT ue.* FROM user_entity as ue "
            "JOIN entities as e "
            "ON ue.entity_id = e.id "
            "WHERE e.universe_id = %(universe_id)s "
            "AND ue.user_id = %(user_id)s "
            "AND ue.role = %(role)s"
        )
        params = {
            "user_id": user_id,
            "universe_id": universe_id,
            "role": role
        }
        rows = await self.db.execute(sql, params)
        adapter = TypeAdapter(List[UserEntity])
        return adapter.validate_python(rows)