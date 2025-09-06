from crud import ConversationCRUD, MessageCRUD, UserCRUD
from services import AuthService, ConversationService, MessageService, UserService


class ServiceContainer:
    def __init__(self) -> None:
        self.user_crud = UserCRUD()
        self.conversation_crud = ConversationCRUD()
        self.message_crud = MessageCRUD()

    def get_auth_service(self) -> AuthService:
        return AuthService(self.user_crud)

    def get_user_service(self) -> UserService:
        return UserService(self.user_crud)

    def get_conversation_service(self) -> ConversationService:
        return ConversationService(self.conversation_crud)

    def get_message_service(self) -> MessageService:
        return MessageService(self.message_crud)


services = ServiceContainer()
