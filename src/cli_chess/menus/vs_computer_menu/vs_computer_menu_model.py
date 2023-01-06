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

from cli_chess.menus import MultiValueMenuModel, MultiValueMenuOption, MenuCategory
from cli_chess.modules.game_options import OnlineGameOptions, OfflineGameOptions
from enum import Enum


class OnlineVsComputerMenuOptions(Enum):
    VARIANT = "Variant"
    TIME_CONTROL = "Time Control"
    COMPUTER_SKILL_LEVEL = "Computer Level"
    COLOR = "Side to play as"


class OfflineVsComputerMenuOptions(Enum):
    VARIANT = "Variant"
    TIME_CONTROL = "Time Control"
    COMPUTER_SKILL_LEVEL = "Computer Level"
    SPECIFY_ELO = "Specify Elo"
    COMPUTER_ELO = "Computer Elo"
    COLOR = "Side to play as"


class VsComputerMenuModel(MultiValueMenuModel):
    def __init__(self, menu: MenuCategory):
        self.menu = menu
        super().__init__(self.menu)


class OnlineVsComputerMenuModel(VsComputerMenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    @staticmethod
    def _create_menu() -> MenuCategory:
        """Create the online menu options"""
        menu_options = [
            MultiValueMenuOption(OnlineVsComputerMenuOptions.VARIANT, "Choose the variant to play", [option for option in OnlineGameOptions.variant_options_dict]),
            MultiValueMenuOption(OnlineVsComputerMenuOptions.TIME_CONTROL, "Choose the time control", [option for option in OnlineGameOptions.time_control_options_dict]),
            MultiValueMenuOption(OnlineVsComputerMenuOptions.COMPUTER_SKILL_LEVEL, "Choose the skill level of the computer", [option for option in OnlineGameOptions.skill_level_options_dict]),
            MultiValueMenuOption(OnlineVsComputerMenuOptions.COLOR, "Choose the side you would like to play as", [option for option in OnlineGameOptions.color_options_dict]),
        ]
        return MenuCategory("Play Online vs Computer", menu_options)


class OfflineVsComputerMenuModel(VsComputerMenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    @staticmethod
    def _create_menu() -> MenuCategory:
        """Create the offline menu options"""
        menu_options = [
            # Todo: Implement ability to use custom or lichess fairy-stockfish defined strength levels
            MultiValueMenuOption(OfflineVsComputerMenuOptions.VARIANT, "Choose the variant to play", [option for option in OfflineGameOptions.variant_options_dict]),
            MultiValueMenuOption(OfflineVsComputerMenuOptions.TIME_CONTROL, "Choose the time control", [option for option in OfflineGameOptions.time_control_options_dict]),
            MultiValueMenuOption(OfflineVsComputerMenuOptions.SPECIFY_ELO, "Would you like the computer to play as a specific Elo?", ["No", "Yes"]),
            MultiValueMenuOption(OfflineVsComputerMenuOptions.COMPUTER_SKILL_LEVEL, "Choose the skill level of the computer", [option for option in OfflineGameOptions.skill_level_options_dict]),
            MultiValueMenuOption(OfflineVsComputerMenuOptions.COMPUTER_ELO, "Choose the Elo of the computer", list(range(500, 2850)), visible=False),
            MultiValueMenuOption(OfflineVsComputerMenuOptions.COLOR, "Choose the side you would like to play as", [option for option in OfflineGameOptions.color_options_dict]),
        ]
        return MenuCategory("Play Offline vs Computer", menu_options)

    def show_elo_selection_option(self, show: bool):
        """Show/hide the Computer Elo option. Enabling the 'Specify Elo' selection
           Will disable the 'Computer SKill' Level option as only of these can be set
        """
        # Todo: Figure out a cleaner way so a loop isn't required
        for i, opt in enumerate(self.menu.category_options):
            if opt.option == OfflineVsComputerMenuOptions.COMPUTER_ELO:
                opt.visible = show
            if opt.option == OfflineVsComputerMenuOptions.COMPUTER_SKILL_LEVEL:
                opt.visible = not show
