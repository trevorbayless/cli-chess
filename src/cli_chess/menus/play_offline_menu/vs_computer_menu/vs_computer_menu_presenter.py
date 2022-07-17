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
from cli_chess.menus.menu_options import OfflineGameOptions
from pprint import pprint


def show_vs_computer_menu():
    return VsComputerMenuPresenter().show_menu()


class VsComputerMenuPresenter:
    def __init__(self):
        self.model = VsComputerMenuModel()
        self.view = VsComputerMenuView(self)

    def get_questions(self):
        return self.model.get_questions()

    def show_menu(self) -> None:
        game_parameters = self.view.show()
        self.process_input(game_parameters)

    def process_input(self, game_parameters: dict) -> None:
        # Todo: Validate answers
        pprint(game_parameters)
        pprint(OfflineGameOptions.skill_level_options_dict[game_parameters['strength']])
