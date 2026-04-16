from fastapi import HTTPException, status
from typing import List, Optional, Dict

from src.models.entity import Entity
from src.models.universe import InputUniverse, PartialUniverse, Universe
from src.models.user import UserToken
from src.services.universe import UniverseService

class UniverseController:
    def __init__(self, universe_service: UniverseService):
        self.universe_service = universe_service

    async def create_universe(self, universe_data: InputUniverse, creator_id: int) -> PartialUniverse:
        try:
            return await self.universe_service.create_universe(universe_data, creator_id)
        except HTTPException:
            raise  # Re-lève les erreurs HTTP existantes
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_all_universes(self) -> List[Universe]:
        try:
            return await self.universe_service.get_all_universes()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_universe_by_id(self, universe_id: int) -> Universe | None:
        try:
            universe = await self.universe_service.get_universe_by_id(universe_id)
            if universe is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Universe not found with the provided Id: {universe_id}"
                )
            return universe
        except HTTPException:
            raise  # Re-lève les erreurs HTTP existantes
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_universes_by_creator(self, creator_id: int) -> List[PartialUniverse]:
        try:
            return await self.universe_service.get_universes_by_creator(creator_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def update_universe(self, universe_id: int, universe_patch: PartialUniverse) -> PartialUniverse | None:
        try:
            updated_universe = await self.universe_service.update_universe(universe_id, universe_patch)
            if updated_universe is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Universe not found with the provided Id: {universe_id}"
                )
            return updated_universe
        except HTTPException:
            raise  # Re-lève les erreurs HTTP existantes
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def delete_universe(self, universe_id: int) -> bool:
        try:
            success = await self.universe_service.delete_universe(universe_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Universe not found with the provided Id: {universe_id}"
                )
            return success
        except HTTPException:
            raise  # Re-lève les erreurs HTTP existantes
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_universe_entities(
        self,
        user: UserToken,
        universe_id: int,
    ) -> list[Entity] | Dict[str, list[Entity]]:
        try:
            return await self.universe_service.get_universe_entities(user, universe_id)
        except HTTPException:
            raise  # Re-lève les erreurs HTTP existantes
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )