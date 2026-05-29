"""
Integration tests for the multi-text_block operations:
- create_multiple_text_blocks
- delete_multiple_text_blocks (+ pull_down_text_blocks_for_entity)
- update_multiple_text_block (patch)
- move_multiple_tb
- update_multiple_text_blocks (service-level orchestration)

Seed reminder (src/data/99.sql) for entity_id=1, creator_id=1:
    id=1, title="Histoire",    position=1
    id=2, title="Géographie",  position=2
"""

from src.factory import Factory
from src.models.text_block import (
    InputTextBlock,
    MovingTextBlock,
    PartialTextBlock,
    UpdateTextBlocks,
)

factory = Factory()


def _by_position(blocks):
    return sorted(blocks, key=lambda tb: tb.position)


class TestCreateMultipleTextBlocks:
    repository = factory.text_block_repository
    controller = factory.text_block_controller

    async def test_create_multiple_in_ascending_order(self):
        """Insert 2 new blocks at positions 3 and 4 of an entity that already
        has 2 blocks (positions 1 and 2). The seed blocks should be untouched."""
        new_blocks = [
            InputTextBlock(title="N1", content="c1", position=3, entity_id=1),
            InputTextBlock(title="N2", content="c2", position=4, entity_id=1),
        ]

        created = await self.repository.create_multiple_text_blocks(
            new_blocks, creator_id=1
        )

        assert created is not None
        assert len(created) == 2

        all_blocks = _by_position(await self.controller.get_text_blocks_by_entity(1))
        titles = [tb.title for tb in all_blocks]
        positions = [tb.position for tb in all_blocks]
        assert titles == ["Histoire", "Géographie", "N1", "N2"]
        assert positions == [1, 2, 3, 4]

    async def test_create_multiple_unsorted_payload(self):
        """Same intent as previous test but client sends positions in
        non-ascending order (4 then 3). The fix sorts by position before
        executemany — the result should be identical."""
        new_blocks = [
            InputTextBlock(title="N2", content="c2", position=4, entity_id=1),
            InputTextBlock(title="N1", content="c1", position=3, entity_id=1),
        ]

        created = await self.repository.create_multiple_text_blocks(
            new_blocks, creator_id=1
        )

        assert created is not None
        assert len(created) == 2

        all_blocks = _by_position(await self.controller.get_text_blocks_by_entity(1))
        titles = [tb.title for tb in all_blocks]
        positions = [tb.position for tb in all_blocks]
        assert titles == ["Histoire", "Géographie", "N1", "N2"]
        assert positions == [1, 2, 3, 4]

    async def test_create_multiple_shifts_existing_blocks(self):
        """Insert 2 new blocks at positions 1 and 2 of an entity that already
        has 2 blocks. The existing blocks must be pushed to positions 3 and 4."""
        new_blocks = [
            InputTextBlock(title="N1", content="c1", position=1, entity_id=1),
            InputTextBlock(title="N2", content="c2", position=2, entity_id=1),
        ]

        await self.repository.create_multiple_text_blocks(new_blocks, creator_id=1)

        all_blocks = _by_position(await self.controller.get_text_blocks_by_entity(1))
        titles = [tb.title for tb in all_blocks]
        positions = [tb.position for tb in all_blocks]
        assert titles == ["N1", "N2", "Histoire", "Géographie"]
        assert positions == [1, 2, 3, 4]


class TestDeleteMultipleTextBlocks:
    repository = factory.text_block_repository
    service = factory.text_block_service
    controller = factory.text_block_controller

    async def test_delete_multiple_returns_full_rows(self):
        """RETURNING * must produce rows that validate as TextBlock (so
        entity_id, position, etc. are present)."""
        deleted = await self.repository.delete_multiple_text_blocks((1, 2))

        assert deleted is not None
        assert {tb.id for tb in deleted} == {1, 2}
        # All fields must be populated (RETURNING *, not RETURNING id).
        for tb in deleted:
            assert tb.entity_id == 1
            assert tb.creator_id == 1
            assert tb.title in {"Histoire", "Géographie"}

        remaining = await self.controller.get_text_blocks_by_entity(1)
        assert remaining == []

    async def test_delete_through_service_pulls_down_positions(self):
        """After deleting block id=1 (pos=1) via the batch service, the
        remaining block (Géographie, was pos=2) must be re-packed to pos=1."""
        payload = UpdateTextBlocks(
            to_create=[],
            to_delete=[PartialTextBlock(id=1)],
            to_move=[],
            to_patch=[],
        )

        result = await self.service.update_multiple_text_blocks(payload, creator_id=1)

        assert result.deleted is not None and len(result.deleted) == 1

        remaining = await self.controller.get_text_blocks_by_entity(1)
        assert len(remaining) == 1
        assert remaining[0].title == "Géographie"
        assert remaining[0].position == 1


class TestUpdateMultipleTextBlock:
    repository = factory.text_block_repository
    controller = factory.text_block_controller

    async def test_patch_multiple_titles_and_contents(self):
        patches = [
            PartialTextBlock(id=1, title="Histoire v2"),
            PartialTextBlock(id=2, content="Nouveau contenu"),
        ]

        patched = await self.repository.update_multiple_text_block(patches)

        assert patched is not None
        assert len(patched) == 2

        by_id = {tb.id: tb for tb in patched}
        # id=1: title changed, content preserved (COALESCE).
        assert by_id[1].title == "Histoire v2"
        assert by_id[1].content is not None and "millénaire" in by_id[1].content
        # id=2: content changed, title preserved.
        assert by_id[2].title == "Géographie"
        assert by_id[2].content == "Nouveau contenu"


class TestMoveMultipleTextBlocks:
    repository = factory.text_block_repository
    controller = factory.text_block_controller

    async def test_move_single_block_swaps_positions(self):
        """Move Histoire (pos=1) to pos=2. Géographie (pos=2) should slide to pos=1."""
        moves = [
            MovingTextBlock(id=1, old_position=1, new_position=2, entity_id=1),
        ]

        moved = await self.repository.move_multiple_tb(moves)

        assert len(moved) == 1
        assert moved[0].id == 1
        assert moved[0].position == 2

        all_blocks = _by_position(await self.controller.get_text_blocks_by_entity(1))
        assert [tb.title for tb in all_blocks] == ["Géographie", "Histoire"]
        assert [tb.position for tb in all_blocks] == [1, 2]

    async def test_move_with_stale_old_position(self):
        """The repository must re-read the current position from DB instead of
        trusting client-supplied old_position. Here we deliberately send a
        wrong old_position and check that the move still succeeds."""
        moves = [
            MovingTextBlock(id=1, old_position=99, new_position=2, entity_id=1),
        ]

        moved = await self.repository.move_multiple_tb(moves)

        assert len(moved) == 1
        assert moved[0].id == 1
        assert moved[0].position == 2

        all_blocks = _by_position(await self.controller.get_text_blocks_by_entity(1))
        assert [tb.title for tb in all_blocks] == ["Géographie", "Histoire"]

    async def test_move_two_blocks_sequentially_uses_fresh_positions(self):
        """Insert a third block so we have 3 blocks at positions 1,2,3, then
        move id=1 from 1→3 AND id=2 from 2→1 in the same batch. After the
        first move, id=2 was already shifted to position 1 by cascade, so
        the second move is a no-op — but the final state must still match."""
        await self.repository.create_text_block(
            InputTextBlock(title="N3", content="c3", position=3, entity_id=1),
            creator_id=1,
        )

        moves = [
            MovingTextBlock(id=1, old_position=1, new_position=3, entity_id=1),
            MovingTextBlock(id=2, old_position=2, new_position=1, entity_id=1),
        ]

        await self.repository.move_multiple_tb(moves)

        all_blocks = _by_position(await self.controller.get_text_blocks_by_entity(1))
        positions = [tb.position for tb in all_blocks]
        assert positions == [1, 2, 3]
        assert len({tb.id for tb in all_blocks}) == 3
        # id=1 ended up at position 3 (its explicit target).
        # id=2 ended up at position 1 (target reached via cascade).
        by_id = {tb.id: tb for tb in all_blocks}
        assert by_id[1].position == 3
        assert by_id[2].position == 1


class TestUpdateTextBlockSinglePositionAndContent:
    repository = factory.text_block_repository
    controller = factory.text_block_controller

    async def test_update_position_keeps_title_and_content_changes(self):
        """Regression test for fix F: when position changes, title and content
        from the patch must also be applied — previously they were dropped."""
        patch = PartialTextBlock(title="Histoire v2", content="contenu v2", position=2)

        updated = await self.repository.update_text_block(1, patch)

        assert updated is not None
        assert updated.id == 1
        assert updated.position == 2
        assert updated.title == "Histoire v2"
        assert updated.content == "contenu v2"

        all_blocks = _by_position(await self.controller.get_text_blocks_by_entity(1))
        by_id = {tb.id: tb for tb in all_blocks}
        assert by_id[1].position == 2
        assert by_id[1].title == "Histoire v2"
        assert by_id[1].content == "contenu v2"
        # The other block must have moved to position 1.
        assert by_id[2].position == 1


class TestBatchOrchestration:
    service = factory.text_block_service
    controller = factory.text_block_controller

    async def test_batch_create_and_patch(self):
        """Create 2 new blocks (positions 3,4) AND patch the existing block id=1."""
        payload = UpdateTextBlocks(
            to_create=[
                InputTextBlock(title="N1", content="c1", position=3, entity_id=1),
                InputTextBlock(title="N2", content="c2", position=4, entity_id=1),
            ],
            to_delete=[],
            to_move=[],
            to_patch=[PartialTextBlock(id=1, title="Histoire v2")],
        )

        result = await self.service.update_multiple_text_blocks(payload, creator_id=1)

        assert result.created is not None and len(result.created) == 2
        assert result.patched is not None and len(result.patched) == 1
        assert result.deleted is None
        assert result.moved is None

        all_blocks = _by_position(await self.controller.get_text_blocks_by_entity(1))
        assert [tb.title for tb in all_blocks] == [
            "Histoire v2",
            "Géographie",
            "N1",
            "N2",
        ]
        assert [tb.position for tb in all_blocks] == [1, 2, 3, 4]

    async def test_batch_delete_then_create(self):
        """Delete id=1 (Histoire), then create 1 new block at the freshly freed
        position 2 (after pull_down compacts Géographie to position 1)."""
        payload = UpdateTextBlocks(
            to_create=[
                InputTextBlock(title="Nouveau", content="c", position=2, entity_id=1),
            ],
            to_delete=[PartialTextBlock(id=1)],
            to_move=[],
            to_patch=[],
        )

        result = await self.service.update_multiple_text_blocks(payload, creator_id=1)

        assert result.deleted is not None and len(result.deleted) == 1
        assert result.created is not None and len(result.created) == 1

        all_blocks = _by_position(await self.controller.get_text_blocks_by_entity(1))
        assert [tb.title for tb in all_blocks] == ["Géographie", "Nouveau"]
        assert [tb.position for tb in all_blocks] == [1, 2]
