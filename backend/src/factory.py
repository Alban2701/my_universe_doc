from src.controllers.entity import EntityController
from src.controllers.text_block import TextBlockController
from src.controllers.universe import UniverseController
from src.controllers.user import UserController
from src.repositories.text_block import TextBlockRepository
from src.repositories.universe import UniverseRepository
from src.repositories.user import UserRepository
from src.repositories.session_token import SessionTokenRepository
from src.repositories.entity import EntityRepository
from src.repositories.user_entity import UserEntityRepository
from src.services.entity import EntityService
from src.services.text_block import TextBlockService
from src.services.universe import UniverseService
from src.services.user import UserService

class Factory:
    def __init__(self):
        self.build_repositories()
        self.build_services()
        self.build_controllers()

    # --- Builders ---
    def build_repositories(self):
        self._session_repository = SessionTokenRepository()
        self._user_repository = UserRepository(self.session_repository)
        self._universe_repository = UniverseRepository()
        self._entity_repository = EntityRepository()
        self._user_entity_repository = UserEntityRepository()
        self._text_block_repository = TextBlockRepository()

    def build_services(self):
        self._user_service = UserService(self.user_repository, self.session_repository)
        self._universe_service = UniverseService(self.universe_repository, self.user_repository, self.entity_repository)
        self._entity_service = EntityService(self.entity_repository)
        self._text_block_service = TextBlockService(self.text_block_repository)

    def build_controllers(self):
        self._user_controller = UserController(self.user_service)
        self._universe_controller = UniverseController(self.universe_service)
        self._entity_controller = EntityController(self.entity_service)
        self._text_block_controller = TextBlockController(self.text_block_service)

    # === PROPERTIES ===

    # --- Universe ---

    @property
    def universe_repository(self) -> UniverseRepository:
        return self._universe_repository

    @property
    def universe_service(self) -> UniverseService:
        return self._universe_service

    @property
    def universe_controller(self) -> UniverseController:
        return self._universe_controller

    # --- Session ---

    @property
    def session_repository(self) -> SessionTokenRepository:
        return self._session_repository

    # --- UserEntity ---

    @property
    def user_entity_repository(self) -> UserEntityRepository:
        return self._user_entity_repository
    
    # --- User ---

    @property
    def user_repository(self) -> UserRepository:
        return self._user_repository

    @property
    def user_service(self) -> UserService:
        return self._user_service

    @property
    def user_controller(self) -> UserController:
        return self._user_controller

    # --- Entity ---

    @property
    def entity_repository(self) -> EntityRepository:
        return self._entity_repository

    @property
    def entity_service(self) -> EntityService:
        return self._entity_service

    @property
    def entity_controller(self) -> EntityController:
        return self._entity_controller
    
    # --- Text block ---

    @property
    def text_block_repository(self) -> TextBlockRepository:
        return self._text_block_repository
    
    @property
    def text_block_service(self) -> TextBlockService:
        return self._text_block_service
    
    @property
    def text_block_controller(self) -> TextBlockController:
        return self._text_block_controller

_factory = Factory()

def get_factory():
    return _factory