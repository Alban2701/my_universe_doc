from src.factory import Factory
from src.models.enums import UserUniverseRole

factory = Factory()


class TestFunctionalUserUniverse:
    user_repository = factory.user_repository

    async def test_get_role_for_creator(self):
        role = await self.user_repository.get_user_role(user_id=1, universe_id=1)

        assert role is not None
        assert role.user_id == 1
        assert role.universe_id == 1
        assert role.admin_role == UserUniverseRole.creator

    async def test_get_role_for_super_administrator(self):
        role = await self.user_repository.get_user_role(user_id=3, universe_id=1)

        assert role is not None
        assert role.user_id == 3
        assert role.universe_id == 1
        assert role.admin_role == UserUniverseRole.super_administrator

    async def test_get_role_returns_none_when_no_link(self):
        role = await self.user_repository.get_user_role(user_id=999, universe_id=1)
        assert role is None
