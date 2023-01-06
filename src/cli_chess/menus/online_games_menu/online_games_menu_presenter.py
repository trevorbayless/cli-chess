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
from cli_chess.menus.online_games_menu import OnlineGamesMenuView
from cli_chess.menus.vs_computer_menu import OnlineVsComputerMenuModel, OnlineVsComputerMenuPresenter
from cli_chess.menus.tv_channel_menu import TVChannelMenuModel, TVChannelMenuPresenter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.online_games_menu import OnlineGamesMenuModel


class OnlineGamesMenuPresenter(MenuPresenter):
    """Defines the online games menu"""
    def __init__(self, model: OnlineGamesMenuModel):
        self.model = model
        self.vs_computer_menu_presenter = OnlineVsComputerMenuPresenter(OnlineVsComputerMenuModel())
        self.tv_channel_menu_presenter = TVChannelMenuPresenter(TVChannelMenuModel())
        self.view = OnlineGamesMenuView(self)
        super().__init__(self.model, self.view)
