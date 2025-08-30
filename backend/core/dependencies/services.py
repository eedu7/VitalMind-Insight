from crud import UserCRUD
from services import AuthService, UserService


class ServiceContainer:
    def __init__(self) -> None:
        self.user_crud = UserCRUD()

    def get_auth_service(self) -> AuthService:
        return AuthService(self.user_crud)

    def get_user_service(self) -> UserService:
        return UserService(self.user_crud)


services = ServiceContainer()
