from typing import List, Optional, Dict
from models.universe import Universe, InputUniverse, PartialUniverse
from src.repositories.entity import EntityRepository
from src.repositories.universe import UniverseRepository
from src.models.user import UserToken
from src.models.entity import Entity
from src.controllers.entity import EntityController
from fastapi import HTTPException, status

from src.repositories.user import UserRepository

class UniverseService:
    def __init__(self,
                universe_repository: UniverseRepository,
                user_repository: UserRepository,
                entity_repository: EntityRepository):
        """
        Initialise le contrôleur pour la gestion des universes.

        Parameters:
        - universe_repository (UniverseRepository): Le repository pour interagir avec la base de données.
        """
        self.universe_repository = universe_repository
        self.user_repository = user_repository
        self.entity_repository = entity_repository

    async def create_universe(self, universe_data: InputUniverse, creator_id: int) -> PartialUniverse:
        """
        Crée un nouvel univers dans la base de données.

        Parameters:
        - universe_data (InputUniverse): Les données de l'univers à créer.
        - creator_id (int): L'ID du créateur de l'univers.

        Returns:
        PartialUniverse: L'univers créé.
        """
        return await self.universe_repository.create_universe(universe_data, creator_id)

    async def get_all_universes(self) -> List[Universe]:
        """
        Récupère tous les universes de la base de données.

        Returns:
        List[Universe]: La liste de tous les universes.
        """
        return await self.universe_repository.get_all_universes()

    async def get_universe_by_id(self, universe_id: int) -> Universe | None:
        """
        Récupère un univers par son ID.

        Parameters:
        - universe_id (int): L'ID de l'univers.

        Returns:
        Universe | None: L'univers trouvé ou None s'il n'existe pas.
        """
        return await self.universe_repository.get_universe_by_id(universe_id)

    async def get_universes_by_creator(self, creator_id: int) -> List[PartialUniverse]:
        """
        Récupère tous les universes créés par un utilisateur.

        Parameters:
        - creator_id (int): L'ID du créateur.

        Returns:
        List[PartialUniverse]: La liste des universes créés par l'utilisateur.
        """
        return await self.universe_repository.get_universes_by_creator(creator_id)

    async def update_universe(self, universe_id: int, universe_patch: PartialUniverse) -> PartialUniverse | None:
        """
        Met à jour un univers avec les nouvelles données fournies.

        Parameters:
        - universe_id (int): L'ID de l'univers à mettre à jour.
        - universe_patch (PartialUniverse): Les données à mettre à jour.

        Returns:
        PartialUniverse | None: L'univers mis à jour ou None s'il n'existe pas.
        """
        return await self.universe_repository.update_universe(universe_id, universe_patch)

    async def delete_universe(self, universe_id: int) -> Universe:
        """
        Supprime un univers de la base de données.

        Parameters:
        - universe_id (int): L'ID de l'univers à supprimer.

        Returns:
        bool: True si la suppression a réussi, False sinon.
        """
        return await self.universe_repository.delete_universe(universe_id)

    async def get_universe_entities(
        self,
        user: UserToken,
        universe_id: int,
    ) -> list[Entity] | Dict[str, list[Entity]]:
        """
        Récupère les entités d'un univers accessibles par un utilisateur.

        Parameters:
        - user (UserToken): L'utilisateur connecté.
        - universe_id (int): L'ID de l'univers.
        - db (DbConnection): La connexion à la base de données.

        Returns:
        list[Entity] | Dict[str, list[Entity]]:
            - Si l'utilisateur est superadmin ou créateur, retourne toutes les entités.
            - Sinon, retourne les entités accessibles en tant qu'admin ou éditeur.
        """
        universe = await self.get_universe_by_id(universe_id)
        if not universe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Universe not found with the provided Id: {universe_id}"
            )

        # Vérifie si l'utilisateur est superadmin de l'univers
        if await self.is_user_superadmin_universe(user.id, universe_id):
            from src.repositories.entity import EntityRepository
            entity_repo = EntityRepository()
            entities = await entity_repo.get_entities_by_universe(universe.id)
            return entities
        else:
            entities_as_admin = await self.entity_repository.get_entity_accessed_by_user_as_admin(user.id, universe.id)
            entities_as_editor = await self.get_entity_accessed_by_user_as_editor(user.id, universe.id)
            return {"as_editor": entities_as_editor, "as_admin": entities_as_admin}

    async def is_user_superadmin_universe(self, user_id: int, universe_id: int) -> bool:
        """
        Vérifie si un utilisateur est au moins superadmin d'un univers.

        Parameters:
        - user_id (int): L'ID de l'utilisateur.
        - universe_id (int): L'ID de l'univers.
        - db (DbConnection): La connexion à la base de données.

        Returns:
        bool: True si l'utilisateur est superadmin, False sinon.
        """
        # Logique pour vérifier si l'utilisateur est superadmin
        # Exemple: Vérifier dans une table user_universe ou similaire
        # À adapter selon ta base de données
        self.user_repository.get_user_admin_rights(user_id, universe_id)