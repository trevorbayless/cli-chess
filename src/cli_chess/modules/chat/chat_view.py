from __future__ import annotations
from prompt_toolkit.widgets import TextArea, Box
from prompt_toolkit.layout import D
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.chat import ChatPresenter


class ChatView:
    def __init__(self, presenter: ChatPresenter):
        self.presenter = presenter
        self._chat_output = TextArea(
            text="",
            style="class:move-list",
            multiline=True,
            wrap_lines=True,
            focus_on_click=False,
            scrollbar=False,
            read_only=True
        )
        self._container = self._create_container()

    def _create_container(self) -> Box:
        return Box(self._chat_output, height=D(max=6), padding=0)

    def update(self, messages: list):
        output = ""
        for msg in messages[-20:]:
            output += f"{msg['username']}: {msg['text']}\n"
        self._chat_output.text = output
        line_count = self._chat_output.buffer.document.line_count
        self._chat_output.buffer.cursor_down(line_count)

    def __pt_container__(self) -> Box:
        return self._container