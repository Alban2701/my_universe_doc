import pytest

from src.factory import Factory
from src.models.universe import InputUniverse

factory = Factory()


async def count_universes() -> int:
    rows = await factory.universe_repository.db.execute(
        "SELECT COUNT(*) AS nb FROM universe"
    )
    assert rows is not None
    return rows[0]["nb"]


class TestCreateUniverse:
    repository = factory.universe_repository
    user_repository = factory.user_repository
    new_universe = InputUniverse(name="Archipel d'Azur", description="Des îles")

    async def test_returns_the_created_universe(self):
        universe = await self.repository.create_universe(self.new_universe, 2)

        assert universe.id is not None
        assert universe.name == "Archipel d'Azur"
        assert universe.description == "Des îles"
        assert universe.creator_id == 2
        assert universe.version == "1"

        stored = await self.repository.get_universe_by_id(universe.id)
        assert stored is not None
        assert stored.name == "Archipel d'Azur"

    async def test_gives_the_creator_role_to_the_creator(self):
        universe = await self.repository.create_universe(self.new_universe, 2)

        role = await self.user_repository.get_user_role(2, universe.id)

        assert role is not None
        assert role.admin_role == "creator"

    async def test_gives_no_role_to_other_users(self):
        universe = await self.repository.create_universe(self.new_universe, 2)

        assert await self.user_repository.get_user_role(1, universe.id) is None

    async def test_unknown_creator_leaves_no_orphan_universe(self):
        """Both inserts are atomic: if one fails, nothing is written."""
        before = await count_universes()

        with pytest.raises(RuntimeError):
            await self.repository.create_universe(self.new_universe, 9999)

        assert await count_universes() == before


class TestFunctionalUniverse:
    controller = factory.universe_controller

    async def test_get_universe_by_id(self):
        universe = await self.controller.get_universe_by_id(1)

        assert universe is not None
        assert universe.id == 1
        assert universe.creator_id == 1
        assert universe.name == "Royaume de Boréalis"
        assert universe.version == "1.0"

    async def test_get_universes_by_creator(self):
        universes = await self.controller.get_universes_by_creator(1)

        assert len(universes) == 1
        assert universes[0].id == 1
        assert universes[0].name == "Royaume de Boréalis"
