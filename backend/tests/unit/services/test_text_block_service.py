from unittest.mock import AsyncMock, MagicMock

from src.models.text_block import (
    InputTextBlock,
    MovingTextBlock,
    PartialTextBlock,
    UpdateTextBlocks,
)
from src.services.text_block import TextBlockService


def make_service():
    repo = AsyncMock()
    service = TextBlockService(repo)
    return service, repo


class TestUpdateMultipleTextBlocks:
    async def test_pull_down_is_called_for_each_distinct_entity_when_deleting(self):
        service, repo = make_service()
        deleted = [
            MagicMock(entity_id=1),
            MagicMock(entity_id=1),
            MagicMock(entity_id=2),
        ]
        repo.delete_multiple_text_blocks.return_value = deleted

        payload = UpdateTextBlocks(
            to_delete=[PartialTextBlock(id=10), PartialTextBlock(id=11)],
            to_create=[],
            to_move=[],
            to_patch=[],
        )
        result = await service.update_multiple_text_blocks(payload, creator_id=1)

        called_entity_ids = {
            call.args[0]
            for call in repo.pull_down_text_blocks_for_entity.call_args_list
        }
        assert called_entity_ids == {1, 2}
        assert result.deleted == deleted

    async def test_created_blocks_are_set_on_result(self):
        service, repo = make_service()
        created = [MagicMock(), MagicMock()]
        repo.create_multiple_text_blocks.return_value = created

        payload = UpdateTextBlocks(
            to_delete=[],
            to_create=[
                InputTextBlock(title="t", content="c", position=1, entity_id=1)
            ],
            to_move=[],
            to_patch=[],
        )
        result = await service.update_multiple_text_blocks(payload, creator_id=42)

        repo.create_multiple_text_blocks.assert_awaited_once()
        assert result.created == created

    async def test_empty_payload_returns_an_empty_result(self):
        service, repo = make_service()

        payload = UpdateTextBlocks(
            to_delete=[], to_create=[], to_move=[], to_patch=[]
        )
        result = await service.update_multiple_text_blocks(payload, creator_id=1)

        repo.delete_multiple_text_blocks.assert_not_awaited()
        repo.create_multiple_text_blocks.assert_not_awaited()
        repo.update_multiple_text_block.assert_not_awaited()
        repo.move_multiple_tb.assert_not_awaited()
        assert result.created is None
        assert result.deleted is None
        assert result.patched is None
        assert result.moved is None

    async def test_moved_and_patched_branches(self):
        service, repo = make_service()
        repo.move_multiple_tb.return_value = ["moved"]
        repo.update_multiple_text_block.return_value = ["patched"]

        payload = UpdateTextBlocks(
            to_delete=[],
            to_create=[],
            to_move=[
                MovingTextBlock(
                    id=1, old_position=1, new_position=2, entity_id=1
                )
            ],
            to_patch=[PartialTextBlock(id=1, title="new")],
        )
        result = await service.update_multiple_text_blocks(payload, creator_id=1)

        assert result.moved == ["moved"]
        assert result.patched == ["patched"]
