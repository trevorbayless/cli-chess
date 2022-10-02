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

from cli_chess.menus import MenuModel, MultiValueMenuOption, MenuCategory
from cli_chess.game import OfflineGameOptions


class VsComputerMenuModel(MenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    def _create_menu(self) -> MenuCategory:
        """Create the menu options"""
        menu_options = [
            # Todo: Implement ELO selector
            # Todo: Implement ability to use custom or lichess fairy-stockfish defined strength levels
            MultiValueMenuOption("Variant", "Choose the variant to play", [option for option in OfflineGameOptions.variant_options_dict]),
            MultiValueMenuOption("Time Control", "Choose the time control", [option for option in OfflineGameOptions.time_control_options_dict]),
            MultiValueMenuOption("Computer Strength", "Choose the strength of the computer", [option for option in OfflineGameOptions.skill_level_options_dict]),
            MultiValueMenuOption("Side to play as", "Choose the side you would like to play as", [option for option in OfflineGameOptions.color_options_dict]),
        ]

        return MenuCategory("Game settings", menu_options)
