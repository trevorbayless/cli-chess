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
from cli_chess.utils.config import game_config, terminal_config
from cli_chess.utils.common import VALID_COLOR_DEPTHS, COLOR_DEPTH_MAP
from cli_chess.utils.logging import log


class ProgramSettingsMenuModel(MultiValueMenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    def _create_menu(self) -> MenuCategory:
        """Create the program settings menu options"""
        menu_options = [
            MultiValueMenuOption(game_config.Keys.SHOW_BOARD_COORDINATES, "", self._get_available_game_config_options(game_config.Keys.SHOW_BOARD_COORDINATES), display_name="Show board coordinates"),  # noqa: E501
            MultiValueMenuOption(game_config.Keys.SHOW_BOARD_HIGHLIGHTS, "", self._get_available_game_config_options(game_config.Keys.SHOW_BOARD_HIGHLIGHTS), display_name="Show board highlights"),  # noqa: E501
            MultiValueMenuOption(game_config.Keys.BLINDFOLD_CHESS, "", self._get_available_game_config_options(game_config.Keys.BLINDFOLD_CHESS), display_name="Blindfold chess"),  # noqa: E501
            MultiValueMenuOption(game_config.Keys.USE_UNICODE_PIECES, "", self._get_available_game_config_options(game_config.Keys.USE_UNICODE_PIECES), display_name="Use unicode pieces"),  # noqa: E501
            MultiValueMenuOption(game_config.Keys.SHOW_MOVE_LIST_IN_UNICODE, "", self._get_available_game_config_options(game_config.Keys.SHOW_MOVE_LIST_IN_UNICODE), display_name="Show move list in unicode"),  # noqa: E501
            MultiValueMenuOption(game_config.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE, "", self._get_available_game_config_options(game_config.Keys.SHOW_MATERIAL_DIFF_IN_UNICODE), display_name="Unicode material difference"),  # noqa: E501
            MultiValueMenuOption(game_config.Keys.PAD_UNICODE, "", self._get_available_game_config_options(game_config.Keys.PAD_UNICODE), display_name="Pad unicode (fix overlap)"),  # noqa: E501
            MultiValueMenuOption(terminal_config.Keys.TERMINAL_COLOR_DEPTH, "", self._get_available_color_depth_options(), display_name="Terminal color depth"),  # noqa: E501
        ]
        return MenuCategory("Program Settings", menu_options)

    @staticmethod
    def _get_available_game_config_options(key: game_config.Keys) -> list:
        """Returns a list of available game configuration options for the passed in key"""
        return ["Yes", "No"] if game_config.get_boolean(key) else ["No", "Yes"]

    @staticmethod
    def _get_available_color_depth_options() -> list:
        """Returns a list of friendly named color depth options.
           The currently set color depth will be the first in the list.
        """
        cdl = VALID_COLOR_DEPTHS.copy()
        current_color_depth = terminal_config.get_value(terminal_config.Keys.TERMINAL_COLOR_DEPTH)
        cdl.insert(0, cdl.pop(cdl.index(current_color_depth)))
        for idx, depth in enumerate(cdl):
            cdl[idx] = COLOR_DEPTH_MAP[depth]
        return cdl

    @staticmethod
    def save_selected_game_config_setting(key: game_config.Keys, enabled: bool):
        """Saves the selected option in the game configuration"""
        game_config.set_value(key, str(enabled))

    @staticmethod
    def save_terminal_color_depth_setting(depth: str):
        """Saves the selected option in the terminal configuration"""
        if depth in VALID_COLOR_DEPTHS:
            terminal_config.set_value(terminal_config.Keys.TERMINAL_COLOR_DEPTH, depth)
        else:
            log.error(f"Invalid color depth value: {depth}")
