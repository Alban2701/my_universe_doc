# -*- coding: utf-8 -*-
from src.factory import Factory
from src.models.user import PartialUser

factory = Factory()

# Les champs `created_at` et `updated_at` ne sont pas pertinents pour ces tests :
# ils sont générés/modifiés automatiquement par la DB (DEFAULT NOW() et NOW() au
# moment du patch), donc leur valeur exacte dépend de l'instant d'exécution.
# Les inclure dans les assertions rendrait les tests fragiles et non
# déterministes, sans rien valider de l'API.
#
# Le `password` est également ignoré : le repository ne le renvoie pas dans le
# `RETURNING` (volontaire — pas de fuite de hash) et ces tests d'intégration ne
# cherchent qu'à vérifier que la DB et l'API communiquent correctement.
IGNORED_FIELDS = {"created_at", "updated_at", "password"}


class TestFunctionalUser:
    controller = factory.user_controller
    user_1 = PartialUser(
        id=1, email="alban@mail.com", username="Alban", bio="Le Créateur"
    )

    async def test_get_user_by_id(self):
        user = await self.controller.get_user_by_id(1)

        assert user is not None
        assert user.model_dump(exclude=IGNORED_FIELDS) == self.user_1.model_dump(
            exclude=IGNORED_FIELDS
        )

    async def test_update_user(self):
        # On patche un champ géré par le repository (bio) — on cherche juste à
        # vérifier que l'API met bien à jour la donnée en DB et la renvoie.
        patch = PartialUser(bio="Le Créateur de l'univers")
        updated = await self.controller.patch_user(1, patch)

        assert updated is not None

        expected = PartialUser(
            id=1,
            email="alban@mail.com",
            username="Alban",
            bio="Le Créateur de l'univers",
        )
        assert updated.model_dump(exclude=IGNORED_FIELDS) == expected.model_dump(
            exclude=IGNORED_FIELDS
        )
