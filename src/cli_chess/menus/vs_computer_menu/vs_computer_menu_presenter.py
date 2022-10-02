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

from cli_chess.utils.logging import log
from cli_chess.menus.vs_computer_menu import VsComputerMenuModel
from cli_chess.menus import MenuPresenter, MultiValueMenuView


class VsComputerMenuPresenter(MenuPresenter):
    """Defines the VsComputer menu"""
    def __init__(self):
        self.model = VsComputerMenuModel()
        self.view = MultiValueMenuView(self, container_width=40, column_width=22)
        super().__init__(self.model, self.view)

    def select_handler(self, selected_option: int):
        """Handles option selection"""
        pass

    # def process_input(self, menu_selections: dict) -> None:
    #     game_parameters = OfflineGameOptions().transpose_selection_dict(menu_selections)
    #     start_offline_game(game_parameters)
