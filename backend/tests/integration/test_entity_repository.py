from src.factory import Factory

factory = Factory()


class TestFunctionalEntity:
    controller = factory.entity_controller

    async def test_get_entity_by_id(self):
        entity = await self.controller.get_entity_by_id(2)

        assert entity is not None
        assert entity.id == 2
        assert entity.name == "Forteresse de Glace"
        assert entity.parent == 1
        assert entity.universe_id == 1
        assert entity.creator_id == 1
        assert entity.not_discovered_name == "???"

    async def test_get_entity_direct_children(self):
        children = await self.controller.get_entity_direct_children(1)

        assert len(children) == 6
        assert {c.id for c in children} == {2, 3, 4, 5, 6, 7}
