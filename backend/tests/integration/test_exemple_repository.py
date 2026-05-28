from src.factory import Factory
from src.models.user import User, PartialUser
from src.db_connection import DbConnection

factory = Factory()


class TestFunctionalUser:
    controller = factory.user_controller
    user_1 = PartialUser(
        id=1, email="alban@mail.com", username="Alban", bio="Le Créateur"
    )

    async def test_get_user_by_id(self):
        user = await self.controller.get_user_by_id(1)

        assert user == self.user_1

    async def test_update_user(self):
        patch = PartialUser(password="Password123", username="Axiy")
        updated = await self.controller.patch_user(1, patch)

        assert updated == PartialUser(
            id=1, email="alban@mail.com", username="Axiy", bio="Le Créateur"
        )
