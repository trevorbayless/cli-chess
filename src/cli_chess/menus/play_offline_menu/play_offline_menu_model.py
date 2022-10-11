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

from cli_chess.menus import MenuModel, MenuOption, MenuCategory
from enum import Enum


class PlayOfflineMenuOptions(Enum):
    VS_COMPUTER = "Play vs Computer"
    PLAY_BOTH_SIDES = "Play both sides"


class PlayOfflineMenuModel(MenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    def _create_menu(self) -> MenuCategory:
        """Create the menu options"""
        menu_options = [
            MenuOption(PlayOfflineMenuOptions.VS_COMPUTER, "Play offline against the computer"),
            MenuOption(PlayOfflineMenuOptions.PLAY_BOTH_SIDES, "You play both sides"),
        ]

        return MenuCategory("Offline games", menu_options)
