from __future__ import annotations
from cli_chess.modules.chat.chat_view import ChatView
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.chat import ChatModel


class ChatPresenter:
    def __init__(self, model: ChatModel):
        self.model = model
        self.view = ChatView(self)
        self.model.add_event_listener(self.update)

    def update(self):
        self.view.update(self.model.get_messages())
