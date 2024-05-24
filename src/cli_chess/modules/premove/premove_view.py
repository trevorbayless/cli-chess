# Copyright (C) 2021-2024 Trevor Bayless <trevorbayless1@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations
from prompt_toolkit.layout import Container, ConditionalContainer, VSplit, D, Window, FormattedTextControl, WindowAlign
from prompt_toolkit.widgets import Box
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.premove import PremovePresenter


class PremoveView:
    def __init__(self, presenter: PremovePresenter, premove: str | None = None):
        self.presenter = presenter
        self.premove = premove if premove else "None"
        self._premove_control = FormattedTextControl(text=lambda: "Premove: " + self.premove, style="class:pre-move")
        self._container = self._create_container()

    def _create_container(self) -> Container:
        return VSplit([
                Box(Window(self._premove_control, align=WindowAlign.LEFT, dont_extend_width=True), padding=0, padding_right=1),
        ], width=D(min=1), height=D(max=1), window_too_small=ConditionalContainer(Window(), False))

    def update(self, premove: str) -> None:
        """Updates the pre-move text display with the pre-move passed in"""
        self.premove = premove if premove else "None"

    def __pt_container__(self) -> Container:
        """Returns this views container"""
        return self._container
