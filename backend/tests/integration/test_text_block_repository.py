from src.factory import Factory

factory = Factory()


class TestFunctionalTextBlock:
    controller = factory.text_block_controller

    async def test_get_text_blocks_by_entity(self):
        text_blocks = await self.controller.get_text_blocks_by_entity(1)

        assert len(text_blocks) == 2
        titles = {tb.title for tb in text_blocks}
        assert titles == {"Histoire", "Géographie"}

        for tb in text_blocks:
            assert tb.entity_id == 1
            assert tb.creator_id == 1
            assert tb.position in {1, 2}

    async def test_get_text_block_by_id(self):
        text_blocks = await self.controller.get_text_blocks_by_entity(1)
        first = next(tb for tb in text_blocks if tb.position == 1)

        fetched = await self.controller.get_text_block_by_id(first.id)

        assert fetched is not None
        assert fetched == first
