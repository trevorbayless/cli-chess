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
from cli_chess.utils.config import GameConfig, game_config


class ProgramSettingsMenuModel(MultiValueMenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    def _create_menu(self) -> MenuCategory:
        """Create the program settings menu options"""
        menu_options = [
            MultiValueMenuOption(GameConfig.Keys.SHOW_BOARD_COORDINATES, "", self.get_available_gc_options(GameConfig.Keys.SHOW_BOARD_COORDINATES), display_name="Show board coordinates"),  # noqa: E501
            MultiValueMenuOption(GameConfig.Keys.SHOW_BOARD_HIGHLIGHTS, "", self.get_available_gc_options(GameConfig.Keys.SHOW_BOARD_HIGHLIGHTS), display_name="Show board highlights"),  # noqa: E501
            MultiValueMenuOption(GameConfig.Keys.BLINDFOLD_CHESS, "", self.get_available_gc_options(GameConfig.Keys.BLINDFOLD_CHESS), display_name="Blindfold chess"),  # noqa: E501
            MultiValueMenuOption(GameConfig.Keys.USE_UNICODE_PIECES, "", self.get_available_gc_options(GameConfig.Keys.USE_UNICODE_PIECES), display_name="Use unicode pieces"),  # noqa: E501
            MultiValueMenuOption(GameConfig.Keys.SHOW_MOVE_LIST_IN_UNICODE, "", self.get_available_gc_options(GameConfig.Keys.SHOW_MOVE_LIST_IN_UNICODE), display_name="Show move list in unicode"),  # noqa: E501
            MultiValueMenuOption(GameConfig.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE, "", self.get_available_gc_options(GameConfig.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE), display_name="Unicode material difference"),  # noqa: E501
            MultiValueMenuOption(GameConfig.Keys.PAD_UNICODE, "", self.get_available_gc_options(GameConfig.Keys.PAD_UNICODE), display_name="Pad unicode (fix overlap)"),  # noqa: E501
        ]
        return MenuCategory("Program Settings", menu_options)

    @staticmethod
    def get_available_gc_options(key: GameConfig.Keys) -> list:
        return ["Yes", "No"] if game_config.get_boolean(key) else ["No", "Yes"]

    @staticmethod
    def save_selected_setting(key: GameConfig.Keys, enabled: bool):
        game_config.set_value(key, str(enabled))
