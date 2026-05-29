from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from src.models.enums import UserEntityRole, UserUniverseRole
from src.models.relations import UserUniverse
from src.models.user import UserToken
from src.services.universe import UniverseService


def make_service():
    universe_repo = AsyncMock()
    user_repo = AsyncMock()
    entity_repo = AsyncMock()
    service = UniverseService(universe_repo, user_repo, entity_repo)
    return service, universe_repo, user_repo, entity_repo


class TestIsUserSuperadminUniverse:
    async def test_returns_false_when_user_has_no_role(self):
        service, _, user_repo, _ = make_service()
        user_repo.get_user_role.return_value = None

        assert await service.is_user_superadmin_universe(1, 1) is False

    async def test_returns_true_when_user_has_a_role(self):
        service, _, user_repo, _ = make_service()
        user_repo.get_user_role.return_value = UserUniverse(
            user_id=1, universe_id=1, admin_role=UserUniverseRole.creator
        )

        assert await service.is_user_superadmin_universe(1, 1) is True


class TestGetUniverseEntities:
    async def test_raises_404_when_universe_does_not_exist(self):
        service, universe_repo, _, _ = make_service()
        universe_repo.get_universe_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await service.get_universe_entities(
                UserToken(id=1, username="bob"), universe_id=42
            )
        assert exc_info.value.status_code == 404

    async def test_returns_all_entities_when_user_is_superadmin(self):
        service, universe_repo, user_repo, entity_repo = make_service()
        universe_repo.get_universe_by_id.return_value = MagicMock(id=1)
        user_repo.get_user_role.return_value = UserUniverse(
            user_id=1, universe_id=1, admin_role=UserUniverseRole.creator
        )
        all_entities = [MagicMock(), MagicMock()]
        entity_repo.get_entities_by_universe.return_value = all_entities

        result = await service.get_universe_entities(
            UserToken(id=1, username="bob"), universe_id=1
        )

        assert result is all_entities
        entity_repo.get_entities_with_user_role.assert_not_awaited()

    async def test_returns_grouped_dict_when_user_is_not_superadmin(self):
        service, universe_repo, user_repo, entity_repo = make_service()
        universe_repo.get_universe_by_id.return_value = MagicMock(id=1)
        user_repo.get_user_role.return_value = None
        entity_repo.get_entities_with_user_role.side_effect = [
            ["reader_entity"],
            ["editor_entity"],
            ["admin_entity"],
        ]

        result = await service.get_universe_entities(
            UserToken(id=1, username="bob"), universe_id=1
        )

        assert result == {
            "as_reader": ["reader_entity"],
            "as_editor": ["editor_entity"],
            "as_admin": ["admin_entity"],
        }
        roles_called = [
            call.args[2]
            for call in entity_repo.get_entities_with_user_role.call_args_list
        ]
        assert set(roles_called) == {
            UserEntityRole.reader,
            UserEntityRole.editor,
            UserEntityRole.administrator,
        }
