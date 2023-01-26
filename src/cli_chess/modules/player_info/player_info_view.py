# Copyright (C) 2021-2022 Trevor Bayless <trevorbayless1@gmail.com>
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
from prompt_toolkit.filters import Condition
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.player_info import PlayerInfoPresenter


class PlayerInfoView:
    def __init__(self, presenter: PlayerInfoPresenter, player_info: dict):
        self.presenter = presenter
        self.player_title = player_info.get('title', "")
        self.player_name = player_info.get('name', "Unknown")
        self.player_rating = str(player_info.get('rating', ""))
        self._player_title_control = FormattedTextControl(text=lambda: self.player_title, style="class:player-info.title")
        self._player_name_control = FormattedTextControl(text=lambda: self.player_name, style="class:player-info")
        self._player_rating_control = FormattedTextControl(text=lambda: self.player_rating, style="class:player-info")
        self._container = self._create_container()

    def _create_container(self) -> Container:
        return VSplit([
            ConditionalContainer(
                Box(Window(self._player_title_control, align=WindowAlign.LEFT, dont_extend_width=True), padding=0, padding_right=1),
                Condition(lambda: self.player_title != "")
            ),
            Box(Window(self._player_name_control, align=WindowAlign.LEFT, dont_extend_width=True), padding=0, padding_right=1),
            Box(Window(self._player_rating_control, align=WindowAlign.RIGHT, dont_extend_width=True), padding=0, padding_right=1),

        ], width=D(min=1), height=D(max=1), window_too_small=ConditionalContainer(Window(), False))

    def update(self, player_info: dict) -> None:
        """Updates the player info using the data passed in"""
        self.player_title = player_info.get('title', '')
        self.player_name = player_info.get('name', 'Unknown')
        self.player_rating = f"({str(player_info.get('rating', ''))})" if player_info.get('rating') else ""

        if self.player_title == "BOT":
            self._player_title_control.style = "class:player-info.title.bot"

    def __pt_container__(self) -> Container:
        """Returns this views container"""
        return self._container
