from crud import ConversationCRUD, UserCRUD
from services import AuthService, ConversationService, UserService


class ServiceContainer:
    def __init__(self) -> None:
        self.user_crud = UserCRUD()
        self.conversation_crud = ConversationCRUD()

    def get_auth_service(self) -> AuthService:
        return AuthService(self.user_crud)

    def get_user_service(self) -> UserService:
        return UserService(self.user_crud)

    def get_conversation_service(self) -> ConversationService:
        return ConversationService(self.conversation_crud)


services = ServiceContainer()
