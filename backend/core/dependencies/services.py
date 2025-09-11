from crud import ConversationCRUD, MessageCRUD, UserCRUD
from services import AuthService, ConversationService, MessageService, UserService
from services.llm.manager import LLMManager


class ServiceContainer:
    def __init__(self) -> None:
        self.user_crud = UserCRUD()
        self.conversation_crud = ConversationCRUD()
        self.message_crud = MessageCRUD()

        self.llm_manager = LLMManager()

    def get_auth_service(self) -> AuthService:
        return AuthService(self.user_crud)

    def get_user_service(self) -> UserService:
        return UserService(self.user_crud)

    def get_conversation_service(self) -> ConversationService:
        message_service: MessageService = self.get_message_service()
        return ConversationService(self.conversation_crud, self.llm_manager, message_service)

    def get_message_service(self) -> MessageService:
        return MessageService(self.message_crud)


services = ServiceContainer()
