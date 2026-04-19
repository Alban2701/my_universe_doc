from models.universe import Universe, InputUniverse, PartialUniverse
from typing import List
from pydantic import TypeAdapter
from src.models.user import User
from src.repositories.base_repository import BaseRepository

class UniverseRepository(BaseRepository):
    async def create_universe(self, universe: InputUniverse, creator_id: int) -> PartialUniverse:
        """
        Create a new universe in the database

        Parameters:
        - universe: the universe data to insert
        - creator_id: the id of the user creating the universe

        Returns:
        PartialUniverse: the created universe
        """
        sql = (
            "INSERT INTO universe (creator_id, name, description, version) "
            "VALUES (%(creator_id)s, %(name)s, %(description)s, %(version)s) "
            "RETURNING *"
        )
        model_universe = universe.model_dump()
        model_universe["creator_id"] = creator_id
        model_universe["version"] = 1
        rows = await self.db.execute(sql, model_universe)
        returned_universe = PartialUniverse.model_validate(rows[0])
        return returned_universe

    async def get_all_universes(self) -> List[Universe]:
        """
        Returns every universe in the database

        Returns:
        List[Universe]: every universes in the database
        """
        sql = "SELECT * FROM universe"
        rows = await self.db.execute(sql)
        adapter = TypeAdapter(List[Universe])
        return adapter.validate_python(rows)

    async def get_universe_by_id(self, universe_id: int) -> Universe | None:
        """
        Get a universe in the database with the provided id

        Parameters:
        - universe_id (int): the id of the universe

        Returns:
        Universe: the universe retrieved or None if not found
        """
        sql = "SELECT * FROM universe WHERE id = %(id)s"
        rows = await self.db.execute(sql, {"id": universe_id})
        if not rows:
            return None
        returned_universe = Universe.model_validate(rows[0])
        return returned_universe

    async def get_universes_by_creator(self, creator_id: int) -> List[PartialUniverse]:
        """
        Get all universes created by a user

        Parameters:
        - creator_id (int): the id of the creator

        Returns:
        List[PartialUniverse]: list of universes
        """
        sql = "SELECT * FROM universe WHERE creator_id=%(creator_id)s"
        rows = await self.db.execute(sql, {"creator_id": creator_id})
        adapter = TypeAdapter(List[PartialUniverse])
        return adapter.validate_python(rows)

    async def update_universe(self, universe_id: int, universe_patch: PartialUniverse) -> PartialUniverse | None:
        """
        Update a universe with new data

        Parameters:
        - universe_id (int): the id of the universe to update
        - universe_patch (PartialUniverse): the fields to update

        Returns:
        PartialUniverse: the updated universe or None if not found
        """
        sql = (
            "UPDATE universe SET "
            "name = COALESCE(%(name)s, name), "
            "description = COALESCE(%(description)s, description), "
            "version = COALESCE(%(version)s, version), "
            "updated_at = NOW() "
            "WHERE id = %(id)s "
            "RETURNING *"
        )
        model_patch = universe_patch.model_dump()
        model_patch["id"] = universe_id
        rows = await self.db.execute(sql, model_patch)
        if not rows:
            return None
        returned_universe = PartialUniverse.model_validate(rows[0])
        return returned_universe

    async def delete_universe(self, universe_id: int) -> bool:
        """
        Delete a universe from the database

        Parameters:
        - universe_id (int): the id of the universe to delete

        Returns:
        bool: True if deleted, False otherwise
        """
        sql = "DELETE FROM universe WHERE id = %(id)s RETURNING *"
        rows = await self.db.execute(sql, {"id": universe_id})
        return Universe.model_validate(rows[0])