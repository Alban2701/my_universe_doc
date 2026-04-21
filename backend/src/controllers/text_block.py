from fastapi import HTTPException, status
from typing import List, Optional
from src.models.text_block import InputTextBlock, PartialTextBlock, TextBlock
from src.services.text_block import TextBlockService

class TextBlockController:
    def __init__(self, text_block_service: TextBlockService):
        self.text_block_service = text_block_service

    async def create_text_block(self, text_block: InputTextBlock, creator_id: int) -> TextBlock:
        try:
            return await self.text_block_service.create_text_block(text_block, creator_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create text block: {str(e)}"
            )

    async def get_text_block_by_id(self, text_block_id: int) -> Optional[PartialTextBlock]:
        try:
            text_block = await self.text_block_service.get_text_block_by_id(text_block_id)
            if text_block is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Text block with id {text_block_id} not found"
                )
            return text_block
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get text block: {str(e)}"
            )

    async def get_text_blocks_by_entity(self, entity_id: int) -> List[PartialTextBlock]:
        try:
            return await self.text_block_service.get_text_blocks_by_entity(entity_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get text blocks by entity: {str(e)}"
            )

    async def update_text_block(self, text_block_id: int, text_block_patch: PartialTextBlock) -> Optional[PartialTextBlock]:
        try:
            updated_text_block = await self.text_block_service.update_text_block(text_block_id, text_block_patch)
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

    async def delete_text_block(self, text_block_id: int) -> TextBlock:
        try:
            tb = await self.text_block_service.delete_text_block(text_block_id)
            if not tb:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Text block with id {text_block_id} not found"
                )
            return tb
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete text block: {str(e)}"
            )