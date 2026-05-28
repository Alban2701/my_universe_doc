from typing import List, Optional
from src.models.text_block import (
    InputTextBlock,
    PartialTextBlock,
    TextBlock,
    TextBlock,
    UpdateTextBlocks,
    UpdatedTextBlocks,
)
from fastapi import HTTPException, status

from src.repositories.text_block import TextBlockRepository


class TextBlockService:
    def __init__(self, text_block_repository: TextBlockRepository):
        self.text_block_repository = text_block_repository

    async def create_text_block(
        self, text_block: InputTextBlock, creator_id: int
    ) -> TextBlock:
        """
        Create a new text block in the database

        Parameters:
        - text_block: InputTextBlock with title, content, entity_id
        - creator_id: id of the user creating the text block

        Returns:
        PartialTextBlock: the created text block
        """
        try:
            return await self.text_block_repository.create_text_block(
                text_block, creator_id
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create text block: {str(e)}",
            )

    async def get_text_block_by_id(self, text_block_id: int) -> Optional[TextBlock]:
        """
        Get a text block by its id

        Parameters:
        - text_block_id (int): id of the text block

        Returns:
        PartialTextBlock or None if not found
        """
        try:
            return await self.text_block_repository.get_text_block_by_id(text_block_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get text block: {str(e)}",
            )

    async def get_text_blocks_by_entity(self, entity_id: int) -> List[TextBlock]:
        """
        Get all text blocks belonging to a specific entity

        Parameters:
        - entity_id (int): id of the entity

        Returns:
        List[PartialTextBlock]: list of text blocks
        """
        try:
            return await self.text_block_repository.get_text_blocks_by_entity(entity_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get text blocks by entity: {str(e)}",
            )

    async def update_text_block(
        self, text_block_id: int, text_block_patch: PartialTextBlock
    ) -> Optional[TextBlock]:
        """
        Update a text block with new data

        Parameters:
        - text_block_id (int): id of the text block to update
        - text_block_patch (PartialTextBlock): fields to update

        Returns:
        PartialTextBlock: the updated text block or None if not found
        """
        try:
            updated_text_block = await self.text_block_repository.update_text_block(
                text_block_id, text_block_patch
            )
            if updated_text_block is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Text block with id {text_block_id} not found",
                )
            return updated_text_block
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update text block: {str(e)}",
            )

    async def delete_text_block(self, text_block_id: int) -> Optional[TextBlock]:
        """
        Delete a text block from the database

        Parameters:
        - text_block_id (int): id of the text block to delete

        Returns:
        bool: True if deleted, False otherwise
        """
        try:
            tb = await self.text_block_repository.delete_text_block(text_block_id)
            return tb
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete text block: {str(e)}",
            )

    async def update_multiple_text_blocks(
        self, payload: UpdateTextBlocks, creator_id: int
    ):
        """
        Update text_blocks from an entity.

        Parameters:
        - payload: text_blocks which need to be created, deleted or updated

        Returns:
        return_type: return_description
        """

        to_delete = payload.to_delete
        to_create = payload.to_create
        to_move = payload.to_move
        to_patch = payload.to_patch
        to_return = UpdatedTextBlocks()

        if to_delete:
            ids = tuple([tb.id for tb in to_delete if tb.id is not None])
            deleted = await self.text_block_repository.delete_multiple_text_blocks(ids)
            if deleted:
                await self.text_block_repository.pull_down_text_blocks_for_entity(
                    deleted[0].entity_id
                )
                to_return.deleted = deleted

        if to_create:
            created = await self.text_block_repository.create_multiple_text_blocks(
                to_create, creator_id
            )
            if created:
                to_return.created = created

        if to_patch:
            patched = await self.text_block_repository.update_multiple_text_block(
                to_patch
            )
            if patched:
                to_return.patched = patched

        if to_move:
            moved = await self.text_block_repository.move_multiple_tb(to_move)
            if moved:
                to_return.moved = moved

        return to_return
