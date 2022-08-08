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

from .vs_computer_menu_model import VsComputerMenuModel
from .vs_computer_menu_view import VsComputerMenuView
from cli_chess.menus import OfflineGameOptions
from cli_chess.game.offline import start_offline_game


def show_vs_computer_menu():
    return VsComputerMenuPresenter().show_menu()


class VsComputerMenuPresenter:
    def __init__(self):
        self.model = VsComputerMenuModel()
        self.view = VsComputerMenuView(self)

    def get_questions(self):
        return self.model.get_questions()

    def show_menu(self) -> None:
        menu_selections = self.view.show()
        self.process_input(menu_selections)

    def process_input(self, menu_selections: dict) -> None:
        # Todo: Validate answers
        game_parameters = OfflineGameOptions().transpose_selection_dict(menu_selections)
        start_offline_game(game_parameters)
