from __future__ import annotations
from prompt_toolkit.layout import Window, FormattedTextControl, WindowAlign, D
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from cli_chess.modules.clock import ClockPresenter


class ClockView:
    def __init__(self, presenter: ClockPresenter, get_time_str: Callable[[], str]):
        self.presenter = presenter
        self._clock_control = FormattedTextControl(text=get_time_str, style="class:clock")
        self._container = Box(Window(self._clock_control, align=WindowAlign.LEFT), padding=0, padding_right=1, height=D(max=1))

    def update(self, is_ticking: bool) -> None:
        """Updates the clock style using the data passed in"""
        if is_ticking:
            self._clock_control.style = "class:clock.ticking"
        else:
            self._clock_control.style = "class:clock"

    def __pt_container__(self) -> Box:
        """Returns this views container"""
        return self._container
