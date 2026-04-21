from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from models.text_block import InputTextBlock, PartialTextBlock, TextBlock
from controllers.text_block import TextBlockController
from factory import Factory, get_factory

text_block_router = APIRouter(prefix="/text-block")

factory: Factory = get_factory()
text_block_controller = factory.text_block_controller

@text_block_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_text_block(
    req: Request,
    text_block_data: InputTextBlock,
) -> TextBlock:
    """
    Create a new text block
    """
    user = req.state.user
    try:
        return await text_block_controller.create_text_block(text_block_data, user.id)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@text_block_router.get("/{text_block_id}", status_code=status.HTTP_200_OK)
async def get_text_block_by_id(text_block_id: int) -> PartialTextBlock:
    """
    Get a text block with the provided ID
    """
    try:
        text_block = await text_block_controller.get_text_block_by_id(text_block_id)
        if text_block is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Text block not found with id {text_block_id}"
            )
        return text_block
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@text_block_router.get("/entity/{entity_id}", status_code=status.HTTP_200_OK)
async def get_text_blocks_by_entity(entity_id: int) -> list[PartialTextBlock]:
    """
    Get all the TextBlock from an entity
    """
    try:
        text_blocks = await text_block_controller.get_text_blocks_by_entity(entity_id)
        return text_blocks
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@text_block_router.patch("/{text_block_id}", status_code=status.HTTP_200_OK)
async def update_text_block(
    text_block_id: int,
    text_block_patch: PartialTextBlock,
) -> PartialTextBlock:
    """
    Patch a text block.
    """
    try:
        updated_text_block = await text_block_controller.update_text_block(text_block_id, text_block_patch)
        if updated_text_block is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Text block not found with id {text_block_id}"
            )
        return updated_text_block
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@text_block_router.delete("/{text_block_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_text_block(text_block_id: int) -> Response:
    """
    delete a text block
    """
    try:
        success = await text_block_controller.delete_text_block(text_block_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Text block not found with id {text_block_id}"
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )