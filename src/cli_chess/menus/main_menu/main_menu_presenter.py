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
from cli_chess.menus.main_menu import MainMenuView, MainMenuOptions
from cli_chess.menus.play_online_menu import PlayOnlineMenuModel, PlayOnlineMenuPresenter
from cli_chess.menus.play_offline_menu import PlayOfflineMenuModel, PlayOfflineMenuPresenter
from cli_chess.menus.settings_menu import SettingsMenuModel, SettingsMenuPresenter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.menus.main_menu import MainMenuModel


class MainMenuPresenter(MenuPresenter):
    """Defines the Main Menu"""
    def __init__(self, model: MainMenuModel):
        self.model = model
        self.play_online_menu_presenter = PlayOnlineMenuPresenter(PlayOnlineMenuModel())
        self.play_offline_menu_presenter = PlayOfflineMenuPresenter(PlayOfflineMenuModel())
        self.settings_menu_presenter = SettingsMenuPresenter(SettingsMenuModel())
        self.view = MainMenuView(self)
        self.selection = self.model.get_menu_options()[0].option

        super().__init__(self.model, self.view)
