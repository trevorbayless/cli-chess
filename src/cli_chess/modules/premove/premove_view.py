from __future__ import annotations
from prompt_toolkit.layout import Container, ConditionalContainer, VSplit, D, Window, FormattedTextControl, WindowAlign
from prompt_toolkit.filters import Condition
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.premove import PremovePresenter


class PremoveView:
    def __init__(self, presenter: PremovePresenter):
        self.presenter = presenter
        self.premove = ""
        self._premove_control = FormattedTextControl(text=lambda: "Premove: " + self.premove, style="class:pre-move")
        self._container = self._create_container()

    def _create_container(self) -> Container:
        return ConditionalContainer(
            VSplit([
                ConditionalContainer(
                    Box(Window(self._premove_control, align=WindowAlign.LEFT, dont_extend_width=True), padding=0, padding_right=1),
                    Condition(lambda: False if not self.premove else True)
                )
            ], width=D(min=1), height=D(max=1), window_too_small=ConditionalContainer(Window(), False)),
            Condition(lambda: False if not self.premove else True)
        )

    def update(self, premove: str) -> None:
        """Updates the pre-move text display with the pre-move passed in"""
        self.premove = premove if premove else ""

    def __pt_container__(self) -> Container:
        """Returns this views container"""
        return self._container
