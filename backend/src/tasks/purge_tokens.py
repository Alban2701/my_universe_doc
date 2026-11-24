import asyncio
import logging

from src.repositories.session_token import SessionTokenRepository

logger = logging.getLogger(__name__)


async def purge_expired_tokens(
    repo: SessionTokenRepository, every_x_seconds: int = 3600
) -> None:
    while True:
        try:
            await repo.delete_expired_token()
        except Exception:
            logger.exception("token purge failed")
        await asyncio.sleep(every_x_seconds)
