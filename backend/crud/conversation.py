from crud.base import BaseCRUD
from db.models import Conversation


class ConversationCRUD(BaseCRUD[Conversation]):
    def __init__(
        self,
    ) -> None:
        super().__init__(Conversation)
