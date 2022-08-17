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
from cli_chess.utils.logging import log


def show_vs_computer_menu():
    return VsComputerMenuPresenter().show_menu()


class VsComputerMenuPresenter:
    def __init__(self):
        self.model = VsComputerMenuModel()
        self.view = VsComputerMenuView(self)

    def get_questions(self):
        return self.model.get_questions()

    def show_menu(self) -> None:
        try:
            menu_selections = self.view.show()
            log.info(f"menu_selections: {menu_selections}")
            self.process_input(menu_selections)
        except KeyboardInterrupt:
            log.info("User quit - keyboard interrupt")
            exit(0)

    def process_input(self, menu_selections: dict) -> None:
        game_parameters = OfflineGameOptions().transpose_selection_dict(menu_selections)
        log.info(f"game_parameters: {game_parameters}")
        start_offline_game(game_parameters)
