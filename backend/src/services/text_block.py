from typing import List, Optional
from src.models.text_block import InputTextBlock, PartialTextBlock
from fastapi import HTTPException, status

from src.repositories.text_block import TextBlockRepository

class TextBlockService:
    def __init__(self, text_block_repository: TextBlockRepository):
        self.text_block_repository = text_block_repository

    async def create_text_block(self, text_block: InputTextBlock, creator_id: int) -> PartialTextBlock:
        """
        Create a new text block in the database

        Parameters:
        - text_block: InputTextBlock with title, content, entity_id
        - creator_id: id of the user creating the text block

        Returns:
        PartialTextBlock: the created text block
        """
        try:
            return await self.text_block_repository.create_text_block(text_block, creator_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create text block: {str(e)}"
            )

    async def get_text_block_by_id(self, text_block_id: int) -> Optional[PartialTextBlock]:
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
                detail=f"Failed to get text block: {str(e)}"
            )

    async def get_text_blocks_by_entity(self, entity_id: int) -> List[PartialTextBlock]:
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
                detail=f"Failed to get text blocks by entity: {str(e)}"
            )

    async def update_text_block(self, text_block_id: int, text_block_patch: PartialTextBlock) -> Optional[PartialTextBlock]:
        """
        Update a text block with new data

        Parameters:
        - text_block_id (int): id of the text block to update
        - text_block_patch (PartialTextBlock): fields to update

        Returns:
        PartialTextBlock: the updated text block or None if not found
        """
        try:
            updated_text_block = await self.text_block_repository.update_text_block(text_block_id, text_block_patch)
            if updated_text_block is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Text block with id {text_block_id} not found"
                )
            return updated_text_block
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update text block: {str(e)}"
            )

    async def delete_text_block(self, text_block_id: int) -> bool:
        """
        Delete a text block from the database

        Parameters:
        - text_block_id (int): id of the text block to delete

        Returns:
        bool: True if deleted, False otherwise
        """
        try:
            success = await self.text_block_repository.delete_text_block(text_block_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Text block with id {text_block_id} not found"
                )
            return success
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete text block: {str(e)}"
            )