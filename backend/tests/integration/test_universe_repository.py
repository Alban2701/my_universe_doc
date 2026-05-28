from src.factory import Factory

factory = Factory()


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
