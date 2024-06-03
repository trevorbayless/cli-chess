from __future__ import annotations
from prompt_toolkit.layout import Window, FormattedTextControl, WindowAlign, D
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.clock import ClockPresenter


class ClockView:
    def __init__(self, presenter: ClockPresenter, initial_time_str: str):
        self.presenter = presenter
        self.time_str = initial_time_str
        self._clock_control = FormattedTextControl(text=lambda: self.time_str, style="class:clock")
        self._container = Box(Window(self._clock_control, align=WindowAlign.LEFT), padding=0, padding_right=1, height=D(max=1))

    def update(self, time: str) -> None:
        """Updates the clock using the data passed in"""
        self.time_str = time

    def __pt_container__(self) -> Box:
        """Returns this views container"""
        return self._container
