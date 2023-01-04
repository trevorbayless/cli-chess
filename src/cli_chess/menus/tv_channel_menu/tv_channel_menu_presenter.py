# Copyright (C) 2021-2023 Trevor Bayless <trevorbayless1@gmail.com>
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
from cli_chess.menus import MenuPresenter
from cli_chess.menus.tv_channel_menu import TVChannelMenuView
from cli_chess.core.game.online_game.watch_tv import start_watching_tv
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.tv_channel_menu import TVChannelMenuModel


class TVChannelMenuPresenter(MenuPresenter):
    def __init__(self, model: TVChannelMenuModel):
        self.model = model
        self.view = TVChannelMenuView(self)

        super().__init__(self.model, self.view)

    def handle_start_watching_tv(self) -> None:
        """Changes the view to start watching tv"""
        start_watching_tv(self.selection)
