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
from cli_chess.menus import MenuPresenter
from cli_chess.menus.main_menu import MainMenuView
from cli_chess.menus.online_games_menu import OnlineGamesMenuModel, OnlineGamesMenuPresenter
from cli_chess.menus.offline_games_menu import OfflineGamesMenuModel, OfflineGamesMenuPresenter
from cli_chess.menus.settings_menu import SettingsMenuModel, SettingsMenuPresenter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.main_menu import MainMenuModel


class MainMenuPresenter(MenuPresenter):
    """Defines the Main Menu"""
    def __init__(self, model: MainMenuModel):
        self.model = model
        self.online_games_menu_presenter = OnlineGamesMenuPresenter(OnlineGamesMenuModel())
        self.offline_games_menu_presenter = OfflineGamesMenuPresenter(OfflineGamesMenuModel())
        self.settings_menu_presenter = SettingsMenuPresenter(SettingsMenuModel())
        self.view = MainMenuView(self)
        self.selection = self.model.get_menu_options()[0].option

        super().__init__(self.model, self.view)
